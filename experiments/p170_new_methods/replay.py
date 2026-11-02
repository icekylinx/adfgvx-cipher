#!/usr/bin/env python3
"""Replay one archived p170 search job with explicit portable binary paths.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Evaluation-only plaintexts and ranks are never written to the engine input.
The counted engine can also replay the older uninstrumented search jobs:
its added counters do not alter the random-number stream or search decisions.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def campaigns():
    cross = json.loads((HERE / "cross_period_results.json").read_text())
    result = {name: cross[name]["records"] for name in
              ("initial_controls", "selected_failure_repeats", "historical")}
    for name, filename in (("radio_rank", "radio_rank_results.json"),
                           ("radio_historical", "radio_historical_results.json")):
        result[name] = json.loads((HERE / filename).read_text())["records"]
    return result


def job_id(record):
    return record["case"]["id"] + ("__" + record["model"] if "model" in record else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--campaign", choices=("initial_controls", "selected_failure_repeats",
                                               "historical", "radio_rank", "radio_historical"))
    parser.add_argument("--job")
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    all_campaigns = campaigns()
    if args.list:
        print(json.dumps({name: [job_id(record) for record in records]
                          for name, records in all_campaigns.items()}, indent=2))
        return
    if not all((args.campaign, args.job, args.engine, args.model, args.output)):
        parser.error("A replay requires --campaign, --job, --engine, --model and --output.")
    if any(character.isspace() for character in str(args.model.resolve())):
        parser.error("The C engine's model path must not contain whitespace.")
    record = next(record for record in all_campaigns[args.campaign] if job_id(record) == args.job)
    case = record["case"]
    recipe = record.get("recipe", record.get("provenance"))
    expected_model = recipe["model_sha256"]
    if isinstance(expected_model, dict):
        expected_model = expected_model[record["model"]]
    assert digest(args.model) == expected_model
    if "settings" in recipe:
        restarts = recipe["settings"]["restarts"]
        iterations = recipe["settings"]["iterations_per_restart"]
    else:
        restarts, iterations = recipe["restarts"], recipe["iterations"]
    seed = case.get("seed", record.get("seed"))
    square = case.get("partial_square", case.get("full_square"))
    feed = (f"{args.model.resolve()} {case['width']} {restarts} {iterations} {seed} 1\n"
            + square + "\n" + " ".join(["0"] * case["width"]) + "\n"
            + case["ciphertext"] + "\n")
    start = time.monotonic()
    proc = subprocess.run([str(args.engine.resolve())], input=feed, text=True,
                          capture_output=True, check=True)
    rows = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
    counts = [json.loads(line) for line in proc.stderr.splitlines() if line.startswith("{")]
    best = max(rows, key=lambda row: row["score"])
    result = {"prepared_by": "icekylinx and GPT-6 Astra Pro", "campaign": args.campaign,
              "job": args.job, "archive_recipe": recipe,
              "replay_engine_sha256": digest(args.engine),
              "same_engine_binary_as_archive": digest(args.engine) == recipe["engine_sha256"],
              "best": best, "same_best_as_archive": best == record["best"],
              "elapsed_seconds": time.monotonic() - start,
              "actual_counts_if_instrumented": counts[0] if len(counts) == 1 else None,
              "same_counts_as_archive": counts == [record["actual_search_counts"]]
              if "actual_search_counts" in record else None}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.output / "checkpoints.jsonl").write_text(proc.stdout)
    (args.output / "stderr.txt").write_text(proc.stderr)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
