"""Known transposition / unknown injective square search, with complete logs.

This is a heuristic search, not an exclusion proof. Best-scoring gibberish is
retained in logs but is never classified as a recovered plaintext.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import time

from cipher import cell_stream, load_data

ROOT = Path(__file__).resolve().parent.parent


def jobs():
    messages, keys = load_data()
    keys += [
        {"name":"CHI-Nov13-ranks-only", "ranks":[3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16]},
        {"name":"TRUPPENVERSCHIEBUNG-ranks-only", "ranks":[16,13,17,11,12,3,9,19,4,14,15,2,7,8,5,1,18,10,6]},
    ]
    for name in ["p73", "p152", "p153a", "p153b", "p170", "p176b", "p189", "p198"]:
        ct = messages[name]["ciphertext"]
        if name == "p152":
            c = list(ct)
            c[29] = c[69] = "?"
            ct = "".join(c)
        for key in keys:
            cells = cell_stream(ct, key["ranks"])
            yield {"id": name, "key_name": key["name"], "ranks": key["ranks"],
                   "ciphertext": ct, "cells": cells, "variant": "raw"}
    for key in keys:
        cells = "????".join(cell_stream(messages[name]["ciphertext"], key["ranks"])
                               for name in ["p153a", "p153b"])
        yield {"id": "p153_joint", "key_name": key["name"], "ranks": key["ranks"],
               "cells": cells, "variant":"joint_raw"}


def run(job, args):
    label = f"{job['id']}__{job['key_name']}"
    output = ROOT / "results" / args.label
    output.mkdir(parents=True, exist_ok=True)
    path = output / (label + ".jsonl")
    seed = int.from_bytes(hashlib.sha256(label.encode()).digest()[:4], "little") + args.seed
    cmd = [str(ROOT/"subsolve36"), str(ROOT/"data"/"german36_quad.bin"), job["cells"],
           str(args.restarts), str(args.iterations), str(seed)]
    start = time.time()
    with path.open("w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    rows = [json.loads(x) for x in path.read_text().splitlines()]
    best = rows[-1]
    record = {**job, "best": best, "seconds": time.time()-start, "seed": seed,
              "restarts": args.restarts, "iterations_per_restart": args.iterations,
              "solver": "subsolve.c", "language_model": "german36_quad.bin",
              "classification": "unvalidated_search_candidate"}
    (output/(label+".json")).write_text(json.dumps(record, indent=2))
    print(json.dumps({"completed": label, "score": best["score"],
                      "plaintext": best["plaintext"], "seconds": record["seconds"]}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--restarts", type=int, default=1000)
    parser.add_argument("--iterations", type=int, default=60000)
    parser.add_argument("--seed", type=int, default=1918)
    parser.add_argument("--label", default="fixed_transposition")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, job, args) for job in jobs()]
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    main()
