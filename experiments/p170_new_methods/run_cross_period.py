#!/usr/bin/env python3
"""New p170 square-reuse scope with fresh length-matched controls.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The shared anchored_joint optimizer receives no control plaintext or true rank.
"""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def verify(record):
    case, best = record["case"], record["best"]
    assert len(case["ciphertext"]) == 106
    assert all(a == "?" or a == b for a, b in zip(case["partial_square"], best["square"]))
    assert sorted(best["ranks"]) == list(range(1, case["width"] + 1))
    assert decrypt(case["ciphertext"], best["ranks"], best["square"]) == best["plaintexts"][0]
    assert encrypt(best["plaintexts"][0], best["ranks"], best["square"]) == case["ciphertext"]
    if "evaluation_only" in case:
        truth = case["evaluation_only"]
        evaluation = {"correct_plaintext_positions": sum(a == b for a, b in zip(truth["plaintext"], best["plaintexts"][0])),
                      "plaintext_positions": len(truth["plaintext"]),
                      "exact_plaintext": truth["plaintext"] == best["plaintexts"][0],
                      "exact_ranks": truth["ranks"] == best["ranks"]}
        assert record["control_evaluation"] == evaluation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--engine", type=Path, default=ROOT / "experiments/joint_search/bin/anchored_joint")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--restarts", type=int, default=1000)
    parser.add_argument("--iterations", type=int, default=100000)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--min-known-cells", type=int, default=0)
    args = parser.parse_args()
    assert args.workers >= 1 and args.restarts >= 1 and args.iterations >= 1
    inputs_path = HERE / "cross_period_inputs.json"
    inputs = json.loads(inputs_path.read_text())
    selected = inputs["controls" if args.controls else "historical"]
    selected = [c for c in selected if 36 - c["partial_square"].count("?") >= args.min_known_cells]
    if args.limit:
        selected = selected[:args.limit]
    model, engine = args.model.resolve(), args.engine.resolve()
    assert sha(model) == "2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e"
    recipe = {"inputs_sha256": sha(inputs_path), "runner_sha256": sha(Path(__file__)),
              "engine_sha256": sha(engine), "model_sha256": sha(model),
              "restarts": args.restarts, "iterations": args.iterations}
    fingerprint = canonical(recipe)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = args.output / "RUN.json"
    if manifest.exists():
        old = json.loads(manifest.read_text())
        assert old["recipe_fingerprint"] == fingerprint
    manifest.write_text(json.dumps({"recipe": recipe, "recipe_fingerprint": fingerprint,
                                   "selected_cases": [c["id"] for c in selected]}, indent=2) + "\n")

    def run(case):
        target = args.output / (case["id"] + ".json")
        if target.exists():
            result = json.loads(target.read_text())
            assert result["recipe_fingerprint"] == fingerprint and result["case"] == case
            verify(result)
            return result
        seed = int(hashlib.sha256((case["id"] + "__fresh_20261102").encode()).hexdigest()[:15], 16)
        header = f"{model} {case['width']} {args.restarts} {args.iterations} {seed} 1\n"
        engine_input = header + case["partial_square"] + "\n" + " ".join(["0"] * case["width"]) + "\n" + case["ciphertext"] + "\n"
        started = time.monotonic()
        proc = subprocess.run([str(engine)], input=engine_input, text=True, capture_output=True, check=True)
        rows = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
        best = max(rows, key=lambda r: r["score"])
        record = {"case": case, "best": best, "seed": seed,
                  "elapsed_seconds": time.monotonic() - started,
                  "recipe_fingerprint": fingerprint, "provenance": recipe,
                  "accepted_historical_plaintext": False}
        if "evaluation_only" in case:
            truth = case["evaluation_only"]
            record["control_evaluation"] = {
                "correct_plaintext_positions": sum(a == b for a, b in zip(truth["plaintext"], best["plaintexts"][0])),
                "plaintext_positions": len(truth["plaintext"]),
                "exact_plaintext": truth["plaintext"] == best["plaintexts"][0],
                "exact_ranks": truth["ranks"] == best["ranks"]}
        verify(record)
        (args.output / (case["id"] + ".jsonl")).write_text(proc.stdout)
        target.write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps({"id": case["id"], "score": best["score"],
                          "plaintext": best["plaintexts"][0],
                          "control_evaluation": record.get("control_evaluation")}), flush=True)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(run, selected))
    summary = {"completed": len(results), "configured_proposal_slots": len(results) * args.restarts * args.iterations,
               "controls": args.controls, "accepted_historical_plaintexts": 0}
    if args.controls:
        summary["exact_control_plaintexts"] = sum(r["control_evaluation"]["exact_plaintext"] for r in results)
    (args.output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
