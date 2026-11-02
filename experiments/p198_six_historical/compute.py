"""Exact six-gram follow-up under one frozen p198 square completion.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The complete historical square is a conditional heuristic completion.
Success on a matched synthetic control does not establish this key.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quad", type=Path, required=True)
    parser.add_argument("--six", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    core = load_module("joint_six", ROOT / "experiments/p198_joint_six/compute.py")
    library = load_module("language_tables", ROOT / "experiments/p215_completion/compute_completions.py")
    tables = library.Tables(args.quad, "military_quad", args.six)
    inputs_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    cases = json.loads(inputs_path.read_text())["cases"]
    provenance = load_module("sparse_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    provenance.audit_provenance(cases)
    case = next(c for c in cases if c["id"] == "p198_CHI-Nov13")
    calibration_path = ROOT / "experiments/p198_joint_six/results.json"
    calibration = json.loads(calibration_path.read_text())
    pure_control = next(r for r in calibration["records"] if r["objective"] == "six")
    assert pure_control["verification"]["plaintext_matches_truth"]
    assert pure_control["exact_search"]["all_allocations_completed"]
    engine = ROOT / "experiments/p198_joint_six/exact_joint_six.cpp"
    assert calibration["engine_source_sha256"] == digest(engine)
    binary = args.work_dir / "exact_joint_six"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                    str(engine), "-o", str(binary)], check=True)
    print("Exact historical follow-up:", case["id"], flush=True)
    result = core.execute(binary, case, args.quad, args.six, args.work_dir, "six")
    assert result["all_allocations_completed"] and result["allocations_completed"] == 15504
    losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    full = core.fill_frame(case["observed_ciphertext"], losses, fill)
    plaintext = decrypt(full, case["column_rank_order"], case["fixed_complete_square"])
    values = core.components(plaintext, tables)
    assert values["six_integer_sum"] == result["best_integer_score"]
    assert encrypt(plaintext, case["column_rank_order"], case["fixed_complete_square"]) == full
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    padded = core.fill_frame(case["observed_ciphertext"], losses, "?" * len(losses))
    complete_domains = plaintext_domains(padded, case["column_rank_order"], case["fixed_complete_square"])
    partial_domains = plaintext_domains(padded, case["column_rank_order"], case["partial_historical_square"])
    assert all(letter in domain for letter, domain in zip(plaintext, partial_domains))
    quad_path = ROOT / "experiments/p198_joint_exact/results.json"
    previous = next(r for r in json.loads(quad_path.read_text())["records"] if r["case_id"] == case["id"])
    previous_text = previous["verification"]["plaintext"]
    previous_scores = core.components(previous_text, tables)
    previous_losses = previous["exact_search"]["missing_full_ciphertext_positions"]
    previous_padded = core.fill_frame(case["observed_ciphertext"], previous_losses, "?" * len(previous_losses))
    previous_domains = plaintext_domains(previous_padded, case["column_rank_order"], case["fixed_complete_square"])
    rows, counters = library.top_k(previous_domains, 1, 5,
                                   lambda suffix, position: tables.units(suffix[-6:]) if position >= 5 else 0)
    fixed_mask_score, fixed_mask_text = rows[0]
    fixed_full = encrypt(fixed_mask_text, case["column_rank_order"], case["fixed_complete_square"])
    assert "".join(c for i, c in enumerate(fixed_full) if i not in previous_losses) == case["observed_ciphertext"]
    assert result["best_integer_score"] >= fixed_mask_score >= previous_scores["six_integer_sum"]
    output = {"schema": "adfgvx-exact-six-historical-followup-v1", "project": "ADFGVX Cipher",
              "authors": "icekylinx and GPT-6 Astra Pro", "case_id": case["id"],
              "input_sha256": digest(inputs_path), "engine_source_sha256": digest(engine),
              "calibration_results_sha256": digest(calibration_path), "quad_results_sha256": digest(quad_path),
              "model_hashes": {"quad": digest(args.quad), "six": digest(args.six)},
              "exact_search": result,
              "verification": {"plaintext": plaintext, "completed_ciphertext": full,
                               "padded_ciphertext": padded, "scores": values,
                               "source_coordinates_preserved": len(case["observed_ciphertext"]),
                               "changed_retained_coordinates": 0, "model_selected_coordinate_fills": len(fill),
                               "model_selected_square_labels_in_frozen_completion": case["partial_historical_square"].count("?"),
                               "singleton_positions_under_frozen_complete_square_before_gap_fills": sum(len(d) == 1 for d in complete_domains),
                               "singleton_positions_under_recorded_partial_square_before_gap_fills": sum(len(d) == 1 for d in partial_domains),
                               "partial_square_domains_at_selected_geometry": partial_domains,
                               "reencryption_verified": True, "independent_integer_score_verified": True,
                               "accepted_historical_plaintext": False},
              "earlier_quad_optimum_rescored": {"plaintext": previous_text, "loss_positions": previous_losses,
                                                "scores": previous_scores,
                                                "six_integer_advantage_of_new_optimum": result["best_integer_score"] - previous_scores["six_integer_sum"]},
              "best_six_completion_at_earlier_quad_mask": {"plaintext": fixed_mask_text, "integer_six_score": fixed_mask_score,
                                                         "mean_six_score": fixed_mask_score / (80 * core.SCALE),
                                                         "loss_positions": previous_losses, "dp_counters": counters,
                                                         "new_geometry_integer_advantage": result["best_integer_score"] - fixed_mask_score},
              "loss_and_fill_witnesses_covered": str(math.comb(170, 5) * 6 ** 5),
              "scope": "All five-loss geometries and concrete missing-coordinate values, under one frozen complete CHI-Nov13 square and fixed transposition.",
              "limits": ["The supplied historical complete square is a heuristic completion of a partial key, unlike the supplied true square in the positive synthetic control.",
                         "Exactly five deletions is an explicit damage hypothesis; other damage models are outside this result.",
                         "No other complete-square extensions or transpositions are bounded by this optimization.",
                         "A globally maximum language score under a conditional key does not establish historical plaintext.",
                         "This reports the canonical optimum and does not enumerate all tied optimal plaintexts."],
              "newly_accepted_historical_plaintext_characters": 0}
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored historical sixgram result differs from recomputation")
        print("Exact historical sixgram optimum and source witness fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"plaintext": plaintext, "six_mean": values["six_mean"], "losses": losses, "fill": fill,
                      "partial_key_singletons_at_selected_geometry": output["verification"]["singleton_positions_under_recorded_partial_square_before_gap_fills"]}), flush=True)


if __name__ == "__main__":
    main()
