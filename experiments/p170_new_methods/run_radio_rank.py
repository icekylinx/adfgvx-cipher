#!/usr/bin/env python3
"""Matched, full-square radio/book rank controls.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Control truths and ranks are evaluation-only; neither enters optimizer input.
"""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def score(plaintext, model):
    indices = [AL.index(c) for c in plaintext]
    return sum(float(model[((a * 37 + b) * 37 + c) * 37 + d])
               for a, b, c, d in zip(indices, indices[1:], indices[2:], indices[3:])) / (len(indices) - 3)


def verify(record):
    case, best = record["case"], record["best"]
    assert len(case["ciphertext"]) == 106
    assert best["square"] == case["full_square"]
    assert sorted(best["ranks"]) == list(range(1, case["width"] + 1))
    assert decrypt(case["ciphertext"], best["ranks"], best["square"]) == best["plaintexts"][0]
    assert encrypt(best["plaintexts"][0], best["ranks"], best["square"]) == case["ciphertext"]
    truth = case["evaluation_only"]
    assert encrypt(truth["plaintext"], truth["ranks"], case["full_square"]) == case["ciphertext"]
    expected = {
        "correct_plaintext_positions": sum(a == b for a, b in zip(truth["plaintext"], best["plaintexts"][0])),
        "plaintext_positions": len(truth["plaintext"]),
        "exact_plaintext": truth["plaintext"] == best["plaintexts"][0],
        "exact_ranks": truth["ranks"] == best["ranks"],
    }
    for key, value in expected.items():
        assert record["control_evaluation"][key] == value
    counts = record["actual_search_counts"]
    settings = record["recipe"]["settings"]
    assert counts["completed_restarts"] == settings["restarts"]
    assert counts["annealing_slots"] == settings["restarts"] * settings["iterations_per_restart"]
    # A complete square has no same-cell substitution proposals to skip.
    assert counts["annealing_fitness_calls"] == counts["annealing_slots"]
    assert counts["total_fitness_calls"] == (counts["annealing_fitness_calls"] +
                                           counts["polish_fitness_calls"] + counts["completed_restarts"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--engine", type=Path, default=Path("/tmp/p170-counted-anchored-joint"))
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    args = parser.parse_args()
    assert args.workers >= 1
    inputs_path = HERE / "radio_rank_inputs.json"
    inputs = json.loads(inputs_path.read_text())
    dataset = ROOT / inputs["dataset_path"]
    assert sha(dataset) == inputs["dataset_sha256"]
    engine = args.engine.resolve()
    model_paths = {
        "book": (args.book_model or Path(inputs["models"]["book"]["default_path"])).resolve(),
        "radio_mixture": (args.radio_model or Path(inputs["models"]["radio_mixture"]["default_path"])).resolve(),
    }
    models = {}
    for name, path in model_paths.items():
        assert sha(path) == inputs["models"][name]["sha256"]
        models[name] = np.fromfile(path, dtype="<f4")
        assert len(models[name]) == 37 ** 4
    recipe = {"inputs_sha256": sha(inputs_path), "runner_sha256": sha(Path(__file__)),
              "engine_source_sha256": sha(HERE / "counted_anchored_joint.c"),
              "engine_sha256": sha(engine), "settings": inputs["settings_frozen_before_search"],
              "model_sha256": {n: sha(p) for n, p in model_paths.items()}}
    fingerprint = canonical(recipe)
    jobs = [(case, name) for case in inputs["controls"] for name in model_paths]
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = args.output / "RUN.json"
    if manifest.exists():
        assert json.loads(manifest.read_text())["recipe_fingerprint"] == fingerprint
    manifest.write_text(json.dumps({"recipe": recipe, "recipe_fingerprint": fingerprint,
                                   "selected_jobs": [c["id"] + "__" + n for c, n in jobs]}, indent=2) + "\n")

    def run(job):
        case, name = job
        target = args.output / (case["id"] + "__" + name + ".json")
        if target.exists():
            record = json.loads(target.read_text())
            assert record["recipe_fingerprint"] == fingerprint and record["case"] == case
            verify(record)
            return record
        settings = inputs["settings_frozen_before_search"]
        engine_input = (f"{model_paths[name]} {case['width']} {settings['restarts']} "
                        f"{settings['iterations_per_restart']} {case['seed']} 1\n" +
                        case["full_square"] + "\n" + " ".join(["0"] * case["width"]) + "\n" +
                        case["ciphertext"] + "\n")
        start = time.monotonic()
        proc = subprocess.run([str(engine)], input=engine_input, text=True, capture_output=True, check=True)
        rows = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
        count_rows = [json.loads(line) for line in proc.stderr.splitlines() if line.startswith("{")]
        assert len(count_rows) == 1
        best = max(rows, key=lambda x: x["score"])
        truth = case["evaluation_only"]
        truth_score = score(truth["plaintext"], models[name])
        winner_score = score(best["plaintexts"][0], models[name])
        assert abs(winner_score - best["score"]) < 1e-7
        evaluation = {
            "correct_plaintext_positions": sum(a == b for a, b in zip(truth["plaintext"], best["plaintexts"][0])),
            "plaintext_positions": len(truth["plaintext"]),
            "exact_plaintext": truth["plaintext"] == best["plaintexts"][0],
            "exact_ranks": truth["ranks"] == best["ranks"],
            "truth_score": truth_score,
            "winning_candidate_score": winner_score,
            "truth_score_minus_winner": truth_score - winner_score,
        }
        record = {"case": case, "model": name, "best": best,
                  "control_evaluation": evaluation, "actual_search_counts": count_rows[0],
                  "elapsed_seconds": time.monotonic() - start,
                  "recipe_fingerprint": fingerprint, "recipe": recipe}
        verify(record)
        target.with_suffix(".jsonl").write_text(proc.stdout)
        target.write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps({"id": case["id"], "model": name, "evaluation": evaluation,
                          "plaintext": best["plaintexts"][0], "counts": count_rows[0]}), flush=True)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        records = list(executor.map(run, jobs))
    summary = {"completed_jobs": len(records),
               "per_model": {name: {"exact_plaintexts": sum(r["control_evaluation"]["exact_plaintext"]
                                                           for r in records if r["model"] == name),
                                     "control_count": len(inputs["controls"])} for name in model_paths},
               "total_actual_counts": {k: sum(r["actual_search_counts"][k] for r in records)
                                       for k in records[0]["actual_search_counts"]},
               "historical_plaintexts_tested": 0}
    (args.output / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
