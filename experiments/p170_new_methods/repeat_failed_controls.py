#!/usr/bin/env python3
"""Stronger independent-seed repeats of the two failed fresh controls.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No evaluation-only plaintext or true rank enters the optimizer.
"""
from array import array
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time

from run_cross_period import HERE, ROOT, sha, verify, encrypt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--restarts", type=int, default=5000)
    args = parser.parse_args()
    inputs_path = HERE / "cross_period_inputs.json"
    inputs = json.loads(inputs_path.read_text())
    cases = [inputs["controls"][i] for i in (3, 5)]
    engine = ROOT / "experiments/joint_search/bin/anchored_joint"
    model = args.model.resolve()
    assert sha(model) == "2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e"
    scores = array("f")
    scores.frombytes(model.read_bytes())
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"
    def score(text):
        v = [alphabet.index(c) for c in text]
        return sum(scores[((a * 37 + b) * 37 + c) * 37 + d]
                   for a, b, c, d in zip(v, v[1:], v[2:], v[3:])) / (len(v) - 3)
    args.output.mkdir(parents=True, exist_ok=True)
    provenance = {"inputs_sha256": sha(inputs_path), "runner_sha256": sha(Path(__file__)),
                  "engine_sha256": sha(engine), "model_sha256": sha(model),
                  "restarts": args.restarts, "iterations": 100000,
                  "selection": "The two failures of the initial six controls, selected after that experiment."}
    records = []
    for case in cases:
        target = args.output / (case["id"] + ".json")
        if target.exists():
            rec = json.loads(target.read_text())
            assert rec["provenance"] == provenance
            verify(rec)
            records.append(rec)
            continue
        seed = int(hashlib.sha256((case["id"] + "__independent_stronger_repeat").encode()).hexdigest()[:15], 16)
        feed = f"{model} {case['width']} {args.restarts} 100000 {seed} 1\n" + case["partial_square"] + "\n" + " ".join(["0"] * case["width"]) + "\n" + case["ciphertext"] + "\n"
        start = time.monotonic()
        proc = subprocess.run([str(engine)], input=feed, text=True, capture_output=True, check=True)
        best = max((json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")), key=lambda r: r["score"])
        truth = case["evaluation_only"]
        rec = {"case": case, "best": best, "seed": seed,
               "elapsed_seconds": time.monotonic() - start, "provenance": provenance,
               "accepted_historical_plaintext": False,
               "control_evaluation": {"correct_plaintext_positions": sum(a == b for a, b in zip(truth["plaintext"], best["plaintexts"][0])),
                                      "plaintext_positions": len(truth["plaintext"]),
                                      "exact_plaintext": truth["plaintext"] == best["plaintexts"][0],
                                      "exact_ranks": truth["ranks"] == best["ranks"]},
               "structural_evaluation": {"truth_encrypts_under_returned_ranks_and_true_square": encrypt(truth["plaintext"], best["ranks"], truth["square"]) == case["ciphertext"],
                                         "planted_objective": score(truth["plaintext"]),
                                         "returned_objective": score(best["plaintexts"][0])}}
        verify(rec)
        assert abs(rec["structural_evaluation"]["returned_objective"] - best["score"]) < 1e-7
        target.write_text(json.dumps(rec, indent=2) + "\n")
        (args.output / (case["id"] + ".jsonl")).write_text(proc.stdout)
        records.append(rec)
        print(json.dumps({"id": case["id"], "best": best,
                          "control_evaluation": rec["control_evaluation"],
                          "structural_evaluation": rec["structural_evaluation"]}), flush=True)
    (args.output / "SUMMARY.json").write_text(json.dumps({"completed": len(records),
        "configured_proposal_slots": len(records) * args.restarts * 100000,
        "exact_plaintexts": sum(r["control_evaluation"]["exact_plaintext"] for r in records)}, indent=2) + "\n")


if __name__ == "__main__":
    main()
