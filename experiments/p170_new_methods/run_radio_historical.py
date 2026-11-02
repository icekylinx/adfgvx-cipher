#!/usr/bin/env python3
"""Bounded radio-model rank search for the unchanged p170 source.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
All known square cells remain fixed; no plaintext crib is supplied.
"""
from pathlib import Path
import argparse
import concurrent.futures
import json
import subprocess
import time

from run_radio_rank import HERE, ROOT, sha, canonical, decrypt, encrypt


def verify(record):
    case, best, counts = record["case"], record["best"], record["actual_search_counts"]
    assert len(case["ciphertext"]) == 106
    assert len(best["plaintexts"][0]) == 53
    assert len(set(best["square"])) == 36
    assert all(a == "?" or a == b for a, b in zip(case["partial_square"], best["square"]))
    assert sorted(best["ranks"]) == list(range(1, case["width"] + 1))
    assert decrypt(case["ciphertext"], best["ranks"], best["square"]) == best["plaintexts"][0]
    assert encrypt(best["plaintexts"][0], best["ranks"], best["square"]) == case["ciphertext"]
    settings = record["recipe"]["settings"]
    assert counts["completed_restarts"] == settings["restarts"]
    assert counts["annealing_slots"] == settings["restarts"] * settings["iterations_per_restart"]
    assert counts["annealing_fitness_calls"] <= counts["annealing_slots"]
    assert counts["total_fitness_calls"] == counts["annealing_fitness_calls"] + counts["polish_fitness_calls"] + counts["completed_restarts"]
    assert record["accepted_historical_plaintext"] is False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--engine", type=Path, default=Path("/tmp/p170-counted-anchored-joint"))
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    assert args.workers >= 1
    inputs_path = HERE / "radio_historical_inputs.json"
    inputs = json.loads(inputs_path.read_text())
    assert sha(HERE / "radio_rank_results.json") == inputs["calibration_results_sha256"]
    model = (args.model or Path(inputs["default_model_path"])).resolve()
    engine = args.engine.resolve()
    assert sha(model) == inputs["model_sha256"]
    keys = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    for case in inputs["cases"]:
        assert case["partial_square"] == keys[case["key_id"]]["square"]
    settings = inputs["settings_frozen_before_historical_search"]
    recipe = {"inputs_sha256": sha(inputs_path), "runner_sha256": sha(Path(__file__)),
              "engine_source_sha256": sha(HERE / "counted_anchored_joint.c"),
              "engine_sha256": sha(engine), "model_sha256": sha(model), "settings": settings}
    fingerprint = canonical(recipe)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = args.output / "RUN.json"
    if manifest.exists():
        assert json.loads(manifest.read_text())["recipe_fingerprint"] == fingerprint
    manifest.write_text(json.dumps({"recipe": recipe, "recipe_fingerprint": fingerprint,
                                   "selected_jobs": [c["id"] for c in inputs["cases"]]}, indent=2) + "\n")

    def run(case):
        target = args.output / (case["id"] + ".json")
        if target.exists():
            record = json.loads(target.read_text())
            assert record["recipe_fingerprint"] == fingerprint and record["case"] == case
            verify(record)
            return record
        feed = (f"{model} {case['width']} {settings['restarts']} {settings['iterations_per_restart']} "
                f"{case['seed']} 1\n" + case["partial_square"] + "\n" +
                " ".join(["0"] * case["width"]) + "\n" + case["ciphertext"] + "\n")
        start = time.monotonic()
        proc = subprocess.run([str(engine)], input=feed, text=True, capture_output=True, check=True)
        rows = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
        counts = [json.loads(line) for line in proc.stderr.splitlines() if line.startswith("{")]
        assert len(counts) == 1
        best = max(rows, key=lambda x: x["score"])
        record = {"case": case, "best": best, "actual_search_counts": counts[0],
                  "elapsed_seconds": time.monotonic() - start, "recipe": recipe,
                  "recipe_fingerprint": fingerprint, "accepted_historical_plaintext": False}
        verify(record)
        target.with_suffix(".jsonl").write_text(proc.stdout)
        target.write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps({"id": case["id"], "best": best, "counts": counts[0]}), flush=True)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        records = list(executor.map(run, inputs["cases"]))
    summary = {"completed_jobs": len(records), "accepted_historical_plaintexts": 0,
               "actual_search_counts": {k: sum(r["actual_search_counts"][k] for r in records)
                                        for k in records[0]["actual_search_counts"]}}
    (args.output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
