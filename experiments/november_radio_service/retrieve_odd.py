#!/usr/bin/env python3
"""Replay the bounded odd-OCR retrieval without changing the old corpus.

Prepared by icekylinx and GPT-6 Astra Pro. Outputs remain unreviewed candidates.
The original run is preserved separately in retrieval/original_results.json.
"""
import argparse
from array import array
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.p198_pretransposition_loss.run import decode, inverse, score, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--book-model", type=Path, required=True)
    parser.add_argument("--radio-model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--screen", type=Path, default=HERE / "retrieval/selected_inputs.json")
    parser.add_argument("--key-inputs", type=Path, default=ROOT / "experiments/p198_pretransposition_loss/inputs.json")
    parser.add_argument("--max-blocks", type=int)
    args = parser.parse_args()
    assert not args.output.exists(), "Refusing to overwrite a retrieval result"
    snapshot = json.loads(args.key_inputs.read_text())
    keys = {key["id"]: key for key in snapshot["historical"]["frozen_keys"]}
    models = {}
    for name, path in [("book", args.book_model), ("radio", args.radio_model)]:
        assert sha(path) == snapshot["models"][name]["sha256"]
        values = array("f")
        values.frombytes(path.read_bytes())
        if sys.byteorder != "little":
            values.byteswap()
        assert len(values) == 37 ** 4
        models[name] = (path, values)
    rows = [row for row in json.loads(args.screen.read_text())["rows"]
            if row["source_slots"] % 2 and 55 <= row["source_slots"] <= 700]
    if args.max_blocks is not None:
        assert args.max_blocks > 0
        rows = rows[:args.max_blocks]
    result, started = [], time.time()
    for row in rows:
        for keyid in dict.fromkeys([row["best"]["key"], row["runner_up"]["key"]]):
            key = keys[keyid]
            interim, _ = inverse(row["ciphertext"], key["column_rank_order"])
            baseline = decode(interim[:-1], key["square"])
            for name, (path, values) in models.items():
                completed = subprocess.run([str(args.engine), str(path), key["square"], "1", interim],
                                           capture_output=True, text=True, check=True)
                candidate = json.loads(completed.stdout)
                assert candidate["completed"]
                result.append({"block_id": row["block_id"], "key_id": keyid, "model": name,
                               "ciphertext": row["ciphertext"], "unmodified_raw": baseline,
                               "unpaired_coordinate": interim[-1],
                               "baseline_mean": score(baseline, values) / (len(baseline) - 3),
                               "result": candidate})
    output = {"schema": "adfgvx-odd-OCR-portable-replay-v1",
              "prepared_by": ["icekylinx", "GPT-6 Astra Pro"],
              "input_sha256": sha(args.screen), "key_inputs_sha256": sha(args.key_inputs),
              "model_sha256": {name: sha(path) for name, (path, _) in models.items()},
              "engine_binary_sha256": sha(args.engine), "blocks": len(rows),
              "completed_jobs": len(result), "elapsed_seconds": time.time() - started,
              "status": "Unreviewed OCR candidates; no historical mechanism or plaintext accepted by this runner.",
              "results": result}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"blocks": len(rows), "completed_jobs": len(result), "output": str(args.output)}))


if __name__ == "__main__":
    main()
