#!/usr/bin/env python3
"""Inventory earlier runtime jobs so planned and completed scope stay distinct.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
These prior jobs are excluded from the new-method campaign budgets.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchored-directory", type=Path,
                        default=Path("/tmp/adfgvx-anchored-full"))
    parser.add_argument("--chi-directory", type=Path,
                        default=Path("/tmp/adfgvx-p170-continuation"))
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    entries = []
    sets = (("five_nearby_anchors", sorted(args.anchored_directory.glob("p170*.json"))),
            ("CHI-Nov8", sorted(args.chi_directory.glob("p170_chi8_w*.json"))))
    for category, paths in sets:
        for path in paths:
            record = json.loads(path.read_text())
            case, best = record["case"], record["best"]
            partial = case.get("partial_square", record.get("partial_square"))
            assert len(case["ciphertext"]) == 106
            assert len(set(best["square"])) == 36
            assert all(a == "?" or a == b for a, b in zip(partial, best["square"]))
            assert decrypt(case["ciphertext"], best["ranks"], best["square"]) == best["plaintexts"][0]
            assert encrypt(best["plaintexts"][0], best["ranks"], best["square"]) == case["ciphertext"]
            restarts = record.get("requested_restarts", record.get("restarts"))
            iterations = record.get("iterations_per_restart", record.get("iterations"))
            assert restarts == 1000 and iterations == 100000
            entries.append({"category": category, "runtime_filename": path.name,
                "record_sha256": sha(path), "key_id": case.get("key_id", "CHI-Nov8-2026-recovery"),
                "width": case["width"], "partial_square": partial,
                "ciphertext_sha256": hashlib.sha256(case["ciphertext"].encode()).hexdigest(),
                "configured_restarts": restarts, "configured_iterations_per_restart": iterations,
                "best_score": best["score"], "roundtrip_checked_at_inventory": True,
                "no_new_plaintext_accepted_by_this_inventory": True})
    assert sum(entry["category"] == "five_nearby_anchors" for entry in entries) == 35
    assert sum(entry["category"] == "CHI-Nov8" for entry in entries) == 13
    output = {"schema": "p170-prior-runtime-scope-inventory-v1",
              "prepared_by": "icekylinx and GPT-6 Astra Pro",
              "purpose": "Prior work used to avoid repeating already completed branches; excluded from new campaign budgets.",
              "anchored_run_manifest_sha256": sha(args.anchored_directory / "RUN.json"),
              "limits": ["The shared anchored_search README freezes an earlier 2/70 snapshot.",
                         "This inventory records the later runtime files, not a change to that snapshot.",
                         "File hashes identify the prior raw records; this compact inventory is not a full result archive.",
                         "No exact fitness-call counts were instrumented in these earlier jobs."],
              "records": entries}
    path = HERE / "prior_scope_inventory.json"
    if args.verify:
        assert json.loads(path.read_text()) == output
    else:
        path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "prior_nearby_jobs": 35, "prior_chi_jobs": 13,
                      "included_in_new_campaign_budgets": False}))


if __name__ == "__main__":
    main()
