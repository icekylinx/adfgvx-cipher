"""Exact joint optimization of coordinate losses and missing values.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The transposition and complete square are fixed. Filled coordinates and
the resulting text remain model hypotheses for historical cases.
"""
from __future__ import annotations

import argparse
import array
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
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"
SCALE = 1 << 24
MODEL_SHA = "fc450633e557d477d009fd9f682a0d6c96629d48a532c1dd2fbc42af0c73b46d"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fill_frame(source, losses, values):
    assert len(losses) == len(values)
    fills = dict(zip(losses, values))
    iterator = iter(source)
    frame = "".join(fills[position] if position in fills else next(iterator)
                    for position in range(len(source) + len(losses)))
    assert next(iterator, None) is None
    return frame


class Scorer:
    def __init__(self, model):
        floats = array.array("f")
        floats.frombytes(Path(model).read_bytes())
        self.units = []
        for value in floats:
            scaled = value * SCALE
            assert scaled.is_integer()
            self.units.append(int(scaled))
        assert len(self.units) == 36 ** 4

    def gram(self, text):
        code = 0
        for letter in text:
            code = code * 36 + ALPHABET.index(letter)
        return self.units[code]

    def score(self, text):
        return sum(self.gram(text[i:i + 4]) for i in range(len(text) - 3))


def execute(binary, case, model, work, name=None, allocation_count=0):
    name = name or case["id"]
    config, output = work / (name + ".cfg"), work / (name + ".engine.json")
    output.unlink(missing_ok=True)
    config.write_text(
        f"{len(case['column_rank_order'])} {case['missing_count']} 0 {allocation_count} 100000\n"
        + case["fixed_complete_square"] + "\n"
        + " ".join(map(str, case["column_rank_order"])) + "\n"
        + case["observed_ciphertext"] + "\n")
    subprocess.run([str(binary), "solve", str(config), str(model), str(output)],
                   check=True, stderr=subprocess.DEVNULL)
    return json.loads(output.read_text())


def exhaustive_controls(binary, model, scorer, square, work):
    reports = []
    settings = [([3, 1, 4, 2], "DERSTA", 1),
                ([4, 1, 6, 2, 5, 3], "DERSTAB", 2),
                ([3, 13, 2, 12, 1, 11, 15, 8, 9, 4, 5, 14, 6, 10, 7, 16], "DERSTABMEL", 2)]
    for ranks, text, missing in settings:
        full = encrypt(text, ranks, square)
        planted_losses = [1] if missing == 1 else [1, len(full) - 3]
        observed = "".join(c for i, c in enumerate(full) if i not in planted_losses)
        case = {"id": "small_width_" + str(len(ranks)), "column_rank_order": ranks,
                "fixed_complete_square": square, "observed_ciphertext": observed, "missing_count": missing}
        result = execute(binary, case, model, work)
        best, count = None, 0
        for losses in itertools.combinations(range(len(full)), missing):
            for values in itertools.product(COORDINATES, repeat=missing):
                fill = "".join(values)
                plaintext = decrypt(fill_frame(observed, losses, fill), ranks, square)
                candidate = (-scorer.score(plaintext), losses, fill)
                if best is None or candidate < best:
                    best = candidate
                count += 1
        assert count == math.comb(len(full), missing) * 6 ** missing
        assert -best[0] == result["best_integer_score"]
        assert list(best[1]) == result["missing_full_ciphertext_positions"]
        assert best[2] == result["filled_missing_coordinates"]
        reports.append({"case": case, "nominal_coordinates": len(full),
                        "loss_and_fill_witnesses_enumerated": count,
                        "best_integer_score": -best[0], "best_loss_positions": list(best[1]),
                        "best_fill": best[2], "exact_dp_matches_exhaustive_enumeration": True})
    constant = work / "constant-quad.bin"
    constant.write_bytes(struct.pack("<f", -4.0) * (36 ** 4))
    tied = execute(binary, reports[-1]["case"], constant, work, name="constant-tie-control")
    assert tied["missing_full_ciphertext_positions"] == [0, 1]
    assert tied["filled_missing_coordinates"] == "AA"
    return {"exhaustive_controls": reports,
            "total_loss_and_fill_witnesses_independently_enumerated": sum(row["loss_and_fill_witnesses_enumerated"] for row in reports),
            "constant_objective_tie_control": {"losses": [0, 1], "fill": "AA", "passed": True}}


def verify_winner(case, result, scorer):
    losses, values = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    assert losses == sorted(set(losses)) and len(losses) == len(values) == case["missing_count"]
    assert set(values) <= set(COORDINATES)
    filled = fill_frame(case["observed_ciphertext"], losses, values)
    plaintext = decrypt(filled, case["column_rank_order"], case["fixed_complete_square"])
    assert scorer.score(plaintext) == result["best_integer_score"]
    assert encrypt(plaintext, case["column_rank_order"], case["fixed_complete_square"]) == filled
    assert "".join(c for i, c in enumerate(filled) if i not in set(losses)) == case["observed_ciphertext"]
    padded = fill_frame(case["observed_ciphertext"], losses, "?" * len(losses))
    domains = plaintext_domains(padded, case["column_rank_order"], case["fixed_complete_square"])
    assert all(letter in domain for letter, domain in zip(plaintext, domains))
    return {"plaintext": plaintext, "filled_ciphertext": filled, "padded_ciphertext": padded,
            "source_coordinates_preserved": len(case["observed_ciphertext"]),
            "changed_retained_source_coordinates": 0,
            "model_selected_coordinate_fills": len(values),
            "singleton_positions_before_filling": sum(len(domain) == 1 for domain in domains),
            "positions_selected_from_non_singleton_domains": [i for i, domain in enumerate(domains) if len(domain) > 1],
            "integer_score_verified_independently": True, "complete_reencryption_verified": True,
            "mean_quad_score": result["best_integer_score"] / ((len(plaintext) - 3) * SCALE),
            "accepted_historical_plaintext": False}


def best_completion_at_fixed_mask(case, losses, scorer, top_k_module):
    padded = fill_frame(case["observed_ciphertext"], losses, "?" * len(losses))
    domains = plaintext_domains(padded, case["column_rank_order"], case["fixed_complete_square"])
    best, _ = top_k_module.top_k(domains, 1, 3,
                               lambda suffix, position: scorer.gram(suffix[-4:]) if position >= 3 else 0)
    score, text = best[0]
    assert score == scorer.score(text)
    encoded = encrypt(text, case["column_rank_order"], case["fixed_complete_square"])
    assert "".join(c for i, c in enumerate(encoded) if i not in set(losses)) == case["observed_ciphertext"]
    return {"loss_positions": losses, "best_integer_score": score, "best_plaintext": text,
            "tie_order": "ASCII lexical plaintext within this independent Python fixed-domain calculation",
            "mean_quad_score": score / ((len(text) - 3) * SCALE)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--input", type=Path, default=ROOT / "experiments/p198_exact_sparse/inputs.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if sys.byteorder != "little" or digest(args.model) != MODEL_SHA:
        parser.error("The recorded little-endian military quad model is required")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    binary = args.work_dir / "exact_joint"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                    str(HERE / "exact_joint.cpp"), "-o", str(binary)], check=True)
    cases = json.loads(args.input.read_text())["cases"]
    marginal_module = load_module("sparse_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    marginal_module.audit_provenance(cases)
    top_k_module = load_module("fixed_domain_completion", ROOT / "experiments/p215_completion/compute_completions.py")
    marginal_records = json.loads((ROOT / "experiments/p198_exact_sparse/results.json").read_text())["records"]
    marginal_by_id = {row["case_id"]: row for row in marginal_records}
    scorer = Scorer(args.model)
    controls = exhaustive_controls(binary, args.model, scorer, cases[0]["fixed_complete_square"], args.work_dir)
    records = []
    for case in cases:
        print("Exact joint loss-and-fill:", case["id"], flush=True)
        result = execute(binary, case, args.model, args.work_dir)
        assert result["all_allocations_completed"] and result["allocations_completed"] == 15504
        verified = verify_winner(case, result, scorer)
        previous_losses = marginal_by_id[case["id"]]["exact_search"]["missing_full_ciphertext_positions"]
        previous_completion = best_completion_at_fixed_mask(case, previous_losses, scorer, top_k_module)
        advantage = result["best_integer_score"] - previous_completion["best_integer_score"]
        assert advantage >= 0
        record = {"case_id": case["id"], "exact_search": result, "verification": verified,
                  "marginal_alignment_rescored_with_concrete_completion": previous_completion,
                  "joint_integer_advantage_over_best_filling_at_marginal_mask": advantage}
        if case["kind"] == "control":
            truth = case["evaluation_only"]
            record["control_evaluation"] = {
                "plaintext_matches_truth_exactly": verified["plaintext"] == truth["plaintext"],
                "plaintext_hamming_distance_from_truth": sum(a != b for a, b in zip(verified["plaintext"], truth["plaintext"])),
                "filled_ciphertext_matches_truth_exactly": verified["filled_ciphertext"] == truth["full_ciphertext"],
                "loss_mask_matches_planted_mask": result["missing_full_ciphertext_positions"] == truth["missing_full_ciphertext_positions_0based"],
                "true_plaintext_integer_score": scorer.score(truth["plaintext"]),
                "global_optimum_integer_advantage_over_truth": result["best_integer_score"] - scorer.score(truth["plaintext"]),
            }
        records.append(record)
        print(json.dumps({"case": case["id"], "score": verified["mean_quad_score"],
                          "losses": result["missing_full_ciphertext_positions"],
                          "fill": result["filled_missing_coordinates"], "plaintext": verified["plaintext"]}), flush=True)
    output = {
        "schema": "adfgvx-exact-joint-loss-and-fill-v1", "project": "ADFGVX Cipher",
        "authors": "icekylinx and GPT-6 Astra Pro", "input_sha256": digest(args.input),
        "input_reference": "experiments/p198_exact_sparse/inputs.json",
        "engine_source_sha256": digest(HERE / "exact_joint.cpp"), "model_sha256": MODEL_SHA,
        "geometry_masks_per_full_case": str(math.comb(170, 5)),
        "coordinate_fillings_per_geometry": 6 ** 5,
        "loss_and_fill_witnesses_per_full_case": str(math.comb(170, 5) * 6 ** 5),
        "objective": "Sum of the original float32 plaintext quadgram log frequencies, represented exactly at scale 2^24. Every gap receives one concrete coordinate value used consistently in all overlapping windows.",
        "exactness_scope": "Global optimum over all five-loss masks and all six-coordinate choices at each loss, for each fixed complete square and fixed transposition. Different witnesses can encode the same completed plaintext.",
        "tie_order": "Earliest increasing list of loss positions, then ADFGVX lexical order of the inserted coordinates at those positions",
        "controls": controls, "records": records,
        "limits": [
            "The historical complete squares are frozen heuristic completions, not established full historical keys.",
            "A maximum language score does not prove historical truth, and no error model outside exactly five deletions is covered.",
            "The source's 165 coordinates are preserved; five added coordinates are explicitly model-selected hypotheses.",
        ],
        "newly_accepted_historical_plaintext_characters": 0,
    }
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored exact joint results differ from full recomputation")
        print("Exact joint loss-and-fill optima, controls, and source witnesses fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
