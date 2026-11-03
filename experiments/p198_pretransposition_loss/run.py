#!/usr/bin/env python3
"""Run the frozen interim-loss protocol, preserving only completed jobs.

Prepared by icekylinx and GPT-6 Astra Pro. The executable receives the key,
loss count and observed interim stream, never a control plaintext or mask.
"""
import argparse
from array import array
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
CO = "ADFGVX"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(cipher, ranks):
    width, length = len(ranks), len(cipher)
    heights = [length // width + (col < length % width) for col in range(width)]
    starts = [sum(heights[other] for other in range(width) if ranks[other] < ranks[col])
              for col in range(width)]
    origins = [starts[i % width] + i // width for i in range(length)]
    assert sorted(origins) == list(range(length))
    return "".join(cipher[i] for i in origins), origins


def transpose(stream, ranks):
    return "".join(stream[col::len(ranks)]
                   for col in sorted(range(len(ranks)), key=lambda col: ranks[col]))


def decode(stream, square):
    assert len(stream) % 2 == 0
    return "".join(square[6 * CO.index(a) + CO.index(b)] if a in CO and b in CO else "?"
                   for a, b in zip(stream[::2], stream[1::2]))


def score(text, model):
    values = [ABC.index(char) for char in text]
    return sum(model[((a * 37 + b) * 37 + c) * 37 + d]
               for a, b, c, d in zip(values, values[1:], values[2:], values[3:]))


def models_from_args(args, inputs):
    models = {}
    for name, path in [("book", args.book_model), ("radio", args.radio_model)]:
        assert sha(path) == inputs["models"][name]["sha256"]
        values = array("f")
        values.frombytes(path.read_bytes())
        if sys.byteorder != "little":
            values.byteswap()
        assert len(values) == 37 ** 4
        models[name] = (path, values)
    return models


def checked_witness(job, result, model):
    key, ciphertext = job["key"], job["received_ciphertext"]
    observed, origins = inverse(ciphertext, key["column_rank_order"])
    full, missing = result["full_interim"], result["missing_interim_indices"]
    assert result["completed"] and len(full) == len(observed) + job["loss_count"]
    assert missing == sorted(set(missing)) and len(missing) == job["loss_count"]
    shortened = "".join(c for i, c in enumerate(full) if i not in missing)
    assert len(shortened) == len(observed)
    assert all(a == "?" or a == b for a, b in zip(observed, shortened))
    assert decode(full, key["square"]) == result["plaintext"]
    assert abs(score(result["plaintext"], model) - result["score_sum"]) < 1e-9
    transmitted = transpose(shortened, key["column_rank_order"])
    assert all(a == "?" or a == b for a, b in zip(ciphertext, transmitted))
    return {"valid_observations_unchanged": True,
            "reencrypted_received_witness": transmitted,
            "observed_interim": observed,
            "received_coordinate_origins": origins}


def run_job(job, name, model_path, model, engine, output):
    observed, _ = inverse(job["received_ciphertext"], job["key"]["column_rank_order"])
    target = output / "logs" / (job["id"] + "__" + name + ".json")
    assert not target.exists(), f"Refusing to overwrite original log {target}"
    command = [str(engine), str(model_path), job["key"]["square"],
               str(job["loss_count"]), observed]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    result = json.loads(completed.stdout)
    witness = checked_witness(job, result, model)
    target.write_text(completed.stdout)
    row = {"id": job["id"], "model": name, "key_id": job["key"]["id"],
           "square": job["key"]["square"], "ranks": job["key"]["column_rank_order"],
           "loss_count": job["loss_count"], "received_ciphertext": job["received_ciphertext"],
           "original_log": str(target.relative_to(output)), "original_log_sha256": sha(target),
           "result": result, "witness": witness}
    truth = job.get("evaluation_only_truth")
    if truth:
        text = truth["plaintext"]
        row["evaluation"] = {"plaintext_exact": result["plaintext"] == text,
                             "correct_characters": sum(a == b for a, b in zip(result["plaintext"], text)),
                             "plaintext_positions": len(text), "truth_score_sum": score(text, model),
                             "full_interim_exact": result["full_interim"] == truth["full_interim"],
                             "loss_mask_exact": result["missing_interim_indices"] == truth["missing_interim_indices"],
                             "truth_not_supplied_to_optimizer": True}
        assert result["score_sum"] + 1e-9 >= row["evaluation"]["truth_score_sum"]
    elif "evaluation_only_conditional_target" in job:
        text = job["evaluation_only_conditional_target"]
        row["evaluation"] = {"reused_conditional_target_exact": result["plaintext"] == text,
                             "agreement_with_conditional_target": sum(a == b for a, b in zip(result["plaintext"], text)),
                             "positions": len(text), "target_not_independent_truth": True,
                             "selected_insertion": result["missing_interim_indices"],
                             "reference_insertion": [job["reference_interim_insertion"]]}
    print(json.dumps({"id": row["id"], "model": name,
                      "evaluation": row.get("evaluation"),
                      "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["controls", "contiguous", "historical"], required=True)
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--book-model", type=Path, required=True)
    parser.add_argument("--radio-model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    models = models_from_args(args, inputs)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "logs").mkdir(exist_ok=True)
    path = args.output / (args.stage + ".json")
    assert not path.exists(), f"Refusing to overwrite {path}"
    started = time.time()
    rows = []
    if args.stage == "contiguous":
        target = inputs["historical"]
        for key in target["frozen_keys"]:
            observed, _ = inverse(target["received_ciphertext"], key["column_rank_order"])
            for position in range(len(observed) + 1):
                stream = observed[:position] + "?" * target["loss_count"] + observed[position:]
                text = decode(stream, key["square"])
                rows.append({"key_id": key["id"], "insert_before_interim_index": position,
                             "partial_plaintext": text,
                             "fixed_label_positions": len(text) - text.count("?"),
                             "score_sums": {name: score(text, model)
                                            for name, (_, model) in models.items()}})
        assert len(rows) == 25 * 166
        extra = {"geometry_candidates": len(rows), "models_per_candidate": 2,
                 "score_evaluations": len(rows) * 2,
                 "scope": "Five contiguous unknown interim coordinates; unassigned square cells and incomplete pairs retain ? labels. These scores do not jointly optimize the fills."}
    else:
        assert args.engine and args.engine.is_file()
        if args.stage == "controls":
            jobs = inputs["controls"] + [inputs["reused_diagnostic"]]
        else:
            controls = json.loads((args.output / "controls.json").read_text())
            assert controls["inputs_sha256"] == sha(HERE / "inputs.json")
            qualifying = [row["id"] + "__" + row["model"] for row in controls["rows"]
                          if row["id"] != inputs["reused_diagnostic"]["id"] and row["loss_count"] == 5
                          and row["evaluation"]["plaintext_exact"]]
            assert qualifying, "Frozen fresh-five-loss gate was not passed"
            target = inputs["historical"]
            jobs = [{"id": target["id"] + "__" + key["id"], "key": key,
                     "received_ciphertext": target["received_ciphertext"],
                     "loss_count": target["loss_count"]} for key in target["frozen_keys"]]
        for job in jobs:
            for name, (model_path, model) in models.items():
                rows.append(run_job(job, name, model_path, model, args.engine, args.output))
        extra = {"completed_jobs": len(rows), "pending_jobs": 0,
                 "states_expanded": sum(r["result"]["states_expanded"] for r in rows),
                 "transitions_evaluated": sum(r["result"]["transitions_evaluated"] for r in rows),
                 "engine_source_sha256": sha(HERE / "interim_dp.cpp"),
                 "engine_binary_sha256": sha(args.engine)}
        if args.stage == "historical":
            extra["qualifying_fresh_control_runs"] = qualifying
    result = {"schema": "adfgvx-interim-loss-run-v1", "stage": args.stage,
              "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
              "model_sha256": {name: sha(model_path) for name, (model_path, _) in models.items()},
              "elapsed_seconds": time.time() - started, **extra, "rows": rows}
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"written": str(path), **extra}), flush=True)


if __name__ == "__main__":
    main()
