"""Refresh unique completed-case counts from preserved research output folders.

This reads completed JSON records and does not launch or modify any search.
Configured proposal slots are not counts of accepted swaps or visited keys.
"""
from collections import defaultdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from search_common import FAMILIES, atomic_json, jobs, seed_for, validate_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-results", type=Path, required=True)
    parser.add_argument("--data-directory", type=Path, default=ROOT / "data")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidates-output", type=Path,
                        help="Export every completed best fit as explicitly unaccepted research output")
    args = parser.parse_args()
    reports = []
    all_outputs = []
    for family, config in FAMILIES.items():
        expected = list(jobs(family, args.data_directory))
        folder = args.research_results / config["results_directory"]
        complete, partial, invalid, candidates = [], [], [], defaultdict(list)
        completed_budget, recorded_seconds = 0, 0.0
        for job in expected:
            path = folder / (job["label"] + ".json")
            trace = folder / (job["label"] + ".jsonl")
            if not path.exists():
                if trace.exists():
                    partial.append(job["label"])
                continue
            try:
                raw = path.read_bytes()
                result = json.loads(raw)
                assert result["ranks"] == job["ranks"]
                assert result["seed"] == seed_for(family, job["label"])
                assert result["restarts"] == config["restarts"]
                assert result["iterations_per_restart"] == config["iterations"]
                validate_result(family, job, result["best"])
                if family == "fixed":
                    assert result["cells"] == job["cells"]
                elif family == "dictionary":
                    assert result["ciphertext"] == job["ciphertext"]
                    assert result["interim"] == job["interim"]
                else:
                    assert result["ciphertext_with_gap"] == job["ciphertext"]
                    assert result["gap_position"] == job["gap_position"]
                complete.append({"label": job["label"], "sha256": hashlib.sha256(raw).hexdigest()})
                all_outputs.append({"family": family, "label": job["label"], "target": job["id"],
                                    "ranks": job["ranks"], "seed": result["seed"], "best": result["best"],
                                    "source_record_sha256": hashlib.sha256(raw).hexdigest()})
                completed_budget += result["restarts"] * result["iterations_per_restart"]
                recorded_seconds += result.get("seconds", 0.0)
                candidates[job["id"]].append({"label": job["label"], "best": result["best"],
                                                "ranks": job["ranks"], "seed": result["seed"]})
            except (ValueError, KeyError, AssertionError) as error:
                invalid.append({"label": job["label"], "error": repr(error)})
        complete.sort(key=lambda item: item["label"])
        reports.append({"family": family, "planned_unique_cases": len(expected),
                        "completed_unique_cases": len(complete),
                        "not_completed_unique_cases": len(expected) - len(complete),
                        "configured_restarts_per_case": config["restarts"],
                        "configured_iterations_per_restart": config["iterations"],
                        "planned_proposal_slots": len(expected) * config["restarts"] * config["iterations"],
                        "completed_case_proposal_slots": completed_budget,
                        "recorded_sum_of_case_wall_seconds": recorded_seconds,
                        "completed_records": complete, "trace_without_completed_record": partial,
                        "unverified_records": invalid, "accepted_plaintexts_by_this_search": 0,
                        "top_unvalidated_candidates": {mid: sorted(rows, key=lambda x: x["best"]["score"], reverse=True)[:3]
                                                       for mid, rows in sorted(candidates.items())}})
    report = {"format_version": 1, "snapshot_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Unique completed records only; concurrent jobs may still be running. Repeated or skipped swap proposals are not distinct searched keys.",
              "acceptance_policy": "No objective score alone accepts a historical plaintext. None from these search branches has been accepted.",
              "families": reports}
    atomic_json(args.output, report)
    if args.candidates_output:
        atomic_json(args.candidates_output, {
            "format_version": 1, "snapshot_utc": report["snapshot_utc"],
            "status": "Unaccepted fitted outputs; no historical plaintext claim",
            "scope": "One best fit per completed unique case; complete inputs and model provenance are distributed separately.",
            "records": sorted(all_outputs, key=lambda row: (row["family"], row["label"]))})
    print(json.dumps({"snapshot_utc": report["snapshot_utc"], "families": [
        {k: row[k] for k in ["family", "planned_unique_cases", "completed_unique_cases", "not_completed_unique_cases"]}
        for row in reports]}, indent=2))


if __name__ == "__main__":
    main()
