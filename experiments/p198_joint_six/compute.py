"""Calibrate exact joint loss-and-fill decoding with a five-letter context.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The complete true key is supplied to synthetic controls. No historical
plaintext is accepted from this language-model comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

COORDINATES = "ADFGVX"
SCALE = 1 << 24


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fill_frame(source, losses, fill):
    values = dict(zip(losses, fill))
    iterator = iter(source)
    result = "".join(values[i] if i in values else next(iterator)
                     for i in range(len(source) + len(losses)))
    assert next(iterator, None) is None
    return result


def coefficients(length, objective):
    if objective == "six":
        return 0, 1, (length - 5) * SCALE
    assert objective == "mixed_30_70"
    return 3 * (length - 5), 7 * (length - 3), 10 * (length - 3) * (length - 5) * SCALE


def components(text, tables):
    four = sum(tables.units(text[i:i + 4]) for i in range(len(text) - 3))
    six = sum(tables.units(text[i:i + 6]) for i in range(len(text) - 5))
    c4, c6, denominator = coefficients(len(text), "mixed_30_70")
    return {"quad_integer_sum": four, "six_integer_sum": six,
            "quad_mean": four / ((len(text) - 3) * SCALE),
            "six_mean": six / ((len(text) - 5) * SCALE),
            "mixed_30_70_mean": (c4 * four + c6 * six) / denominator}


def execute(binary, case, quad, six, work, objective, name=None, allocation_count=0):
    name = name or case["id"] + "_" + objective
    config, output = work / (name + ".cfg"), work / (name + ".engine.json")
    output.unlink(missing_ok=True)
    c4, c6, _ = coefficients((len(case["observed_ciphertext"]) + case["missing_count"]) // 2, objective)
    config.write_text(
        f"{len(case['column_rank_order'])} {case['missing_count']} 0 {allocation_count} 100000 {c4} {c6}\n"
        + case["fixed_complete_square"] + "\n"
        + " ".join(map(str, case["column_rank_order"])) + "\n"
        + case["observed_ciphertext"] + "\n")
    subprocess.run([str(binary), "solve", str(config), str(quad), str(six), str(output)],
                   check=True, stderr=subprocess.DEVNULL)
    return json.loads(output.read_text())


def exhaustive_controls(binary, quad, six, tables, square, work):
    rows = []
    settings = [([3, 1, 4, 2], "DERSTA", 1),
                ([4, 1, 6, 2, 5, 3], "DERSTAB", 2),
                ([3, 13, 2, 12, 1, 11, 15, 8, 9, 4, 5, 14, 6, 10, 7, 16], "DERSTABMEL", 2)]
    for ranks, text, missing in settings:
        full = encrypt(text, ranks, square)
        planted = [1] if missing == 1 else [1, len(full) - 3]
        observed = "".join(c for i, c in enumerate(full) if i not in planted)
        case = {"id": "small_width_" + str(len(ranks)), "column_rank_order": ranks,
                "fixed_complete_square": square, "observed_ciphertext": observed, "missing_count": missing}
        brute = {"six": None, "mixed_30_70": None}
        count = 0
        for losses in itertools.combinations(range(len(full)), missing):
            for values in itertools.product(COORDINATES, repeat=missing):
                fill = "".join(values)
                plaintext = decrypt(fill_frame(observed, losses, fill), ranks, square)
                scores = components(plaintext, tables)
                for objective in brute:
                    c4, c6, _ = coefficients(len(plaintext), objective)
                    score = c4 * scores["quad_integer_sum"] + c6 * scores["six_integer_sum"]
                    candidate = (-score, losses, fill)
                    if brute[objective] is None or candidate < brute[objective]:
                        brute[objective] = candidate
                count += 1
        checks = []
        for objective, best in brute.items():
            result = execute(binary, case, quad, six, work, objective)
            assert result["best_integer_score"] == -best[0]
            assert result["missing_full_ciphertext_positions"] == list(best[1])
            assert result["filled_missing_coordinates"] == best[2]
            checks.append({"objective": objective, "best_integer_score": -best[0],
                           "loss_positions": list(best[1]), "fill": best[2], "exact_match": True})
        rows.append({"case": case, "nominal_coordinates": len(full),
                     "loss_and_fill_witnesses_enumerated": count, "objective_checks": checks})
    constant_quad, constant_six = work / "constant-quad.bin", work / "constant-six.bin"
    constant_quad.write_bytes(struct.pack("<f", -4.0) * (36 ** 4))
    constant_six.write_bytes(struct.pack("<8sIIfIf", b"G6HASH2\0", 1, 0, -4.0, 0, -4.0))
    for objective in ["six", "mixed_30_70"]:
        tied = execute(binary, rows[-1]["case"], constant_quad, constant_six, work,
                       objective, name="constant_" + objective)
        assert tied["missing_full_ciphertext_positions"] == [0, 1]
        assert tied["filled_missing_coordinates"] == "AA"
    return {"cases": rows, "total_distinct_witnesses_enumerated": sum(r["loss_and_fill_witnesses_enumerated"] for r in rows),
            "objectives_compared_per_witness": 2, "constant_score_ties_passed_for_both_objectives": True}


def evaluate(case, result, tables, objective):
    losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    assert len(losses) == len(fill) == case["missing_count"]
    assert losses == sorted(set(losses)) and set(fill) <= set(COORDINATES)
    full = fill_frame(case["observed_ciphertext"], losses, fill)
    text = decrypt(full, case["column_rank_order"], case["fixed_complete_square"])
    assert encrypt(text, case["column_rank_order"], case["fixed_complete_square"]) == full
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    values = components(text, tables)
    c4, c6, denominator = coefficients(len(text), objective)
    score = c4 * values["quad_integer_sum"] + c6 * values["six_integer_sum"]
    assert score == result["best_integer_score"]
    truth = case["evaluation_only"]
    truth_values = components(truth["plaintext"], tables)
    true_score = c4 * truth_values["quad_integer_sum"] + c6 * truth_values["six_integer_sum"]
    return {"plaintext": text, "completed_ciphertext": full, "scores": values,
            "display_objective": score / denominator, "integer_denominator_for_display": denominator,
            "retained_source_coordinates_preserved": len(case["observed_ciphertext"]),
            "changed_retained_source_coordinates": 0, "model_selected_missing_coordinates": len(fill),
            "complete_reencryption_verified": True, "independent_integer_score_verified": True,
            "planted_plaintext": truth["plaintext"], "planted_scores": truth_values,
            "planted_integer_objective": true_score,
            "global_optimum_integer_advantage_over_truth": score - true_score,
            "plaintext_matches_truth": text == truth["plaintext"],
            "plaintext_hamming_distance_from_truth": sum(a != b for a, b in zip(text, truth["plaintext"])),
            "completed_ciphertext_matches_truth": full == truth["full_ciphertext"],
            "loss_mask_matches_planted_mask": losses == truth["missing_full_ciphertext_positions_0based"],
            "newly_accepted_historical_plaintext_characters": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quad", type=Path, required=True)
    parser.add_argument("--six", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if sys.byteorder != "little":
        parser.error("Little-endian model arrays required")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    library = load_module("language_tables", ROOT / "experiments/p215_completion/compute_completions.py")
    tables = library.Tables(args.quad, "military_quad", args.six)
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    inputs = json.loads(input_path.read_text())["cases"]
    controls = [case for case in inputs if case["kind"] == "control"]
    marginal = load_module("sparse_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    marginal.audit_provenance(inputs)
    binary = args.work_dir / "exact_joint_six"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                    str(HERE / "exact_joint_six.cpp"), "-o", str(binary)], check=True)
    checks = exhaustive_controls(binary, args.quad, args.six, tables, controls[0]["fixed_complete_square"], args.work_dir)
    quad_path = ROOT / "experiments/p198_joint_exact/results.json"
    quad_records = {r["case_id"]: r for r in json.loads(quad_path.read_text())["records"]}
    sensitivity = []
    for case in controls:
        winner = quad_records[case["id"]]
        text = winner["verification"]["plaintext"]
        # A feasible competitor is enough to rule out a planted global optimum.
        full = encrypt(text, case["column_rank_order"], case["fixed_complete_square"])
        losses = winner["exact_search"]["missing_full_ciphertext_positions"]
        assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
        truth_values = components(case["evaluation_only"]["plaintext"], tables)
        winner_values = components(text, tables)
        differences = {key: winner_values[key] - truth_values[key]
                       for key in ["quad_integer_sum", "six_integer_sum", "quad_mean", "six_mean", "mixed_30_70_mean"]}
        sensitivity.append({"case_id": case["id"], "quad_optimum_plaintext": text,
                            "planted": truth_values, "quad_optimum": winner_values,
                            "quad_optimum_minus_planted": differences,
                            "source_feasibility_independently_verified": True})
    assert sensitivity[0]["quad_optimum_minus_planted"]["six_integer_sum"] < 0
    assert sensitivity[1]["quad_optimum_minus_planted"]["six_integer_sum"] > 0
    assert sensitivity[1]["quad_optimum_minus_planted"]["mixed_30_70_mean"] > 0
    selected = next(case for case in controls if case["id"] == "control_CHI-Nov13")
    pilot = execute(binary, selected, args.quad, args.six, args.work_dir,
                    "six", name="pilot100", allocation_count=100)
    assert pilot["allocations_completed"] == 100 and not pilot["all_allocations_completed"]
    records = []
    for objective in ["six", "mixed_30_70"]:
        print("Exact five-letter-context search:", selected["id"], objective, flush=True)
        result = execute(binary, selected, args.quad, args.six, args.work_dir, objective)
        assert result["all_allocations_completed"] and result["allocations_completed"] == 15504
        verified = evaluate(selected, result, tables, objective)
        assert verified["global_optimum_integer_advantage_over_truth"] >= 0
        records.append({"case_id": selected["id"], "objective": objective,
                        "exact_search": result, "verification": verified})
        print(json.dumps({"objective": objective, "plaintext": verified["plaintext"],
                          "distance_from_truth": verified["plaintext_hamming_distance_from_truth"],
                          "score": verified["display_objective"],
                          "losses": result["missing_full_ciphertext_positions"],
                          "fill": result["filled_missing_coordinates"]}), flush=True)
    output = {"schema": "adfgvx-exact-joint-six-calibration-v1", "project": "ADFGVX Cipher",
              "authors": "icekylinx and GPT-6 Astra Pro", "input_sha256": digest(input_path),
              "quad_results_sha256": digest(quad_path), "engine_source_sha256": digest(HERE / "exact_joint_six.cpp"),
              "model_hashes": {"quad": digest(args.quad), "six": digest(args.six)},
              "integer_log_scale": SCALE, "controls": checks, "pilot100": pilot,
              "quad_winner_sensitivity": sensitivity, "records": records,
              "witnesses_per_full_search": str(math.comb(170, 5) * 6 ** 5),
              "exactness_scope": "All five-loss masks and all six-coordinate fills under one supplied complete true control key; additive original float32 language scores represented exactly as integers.",
              "omitted_full_control": {"case_id": "control_Nov13-15b",
                                       "reason": "Its feasible wrong quadgram optimum already scores above the planted text under both sixgram and mixed objectives, proving the truth cannot be their global optimum; another exhaustive run is unnecessary for this question."},
              "limitations": ["The four- and six-gram tables use the same independent training corpus; agreement is sensitivity evidence, not statistically independent evidence.",
                              "Optimizing a language objective exactly does not establish historical or planted truth.",
                              "Only synthetic calibration is performed here; no p198 historical plaintext is proposed."],
              "newly_accepted_historical_plaintext_characters": 0}
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored exact sixgram results differ from recomputation")
        print("Exact sixgram/mixed optima, controls and witnesses fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
