#!/usr/bin/env python3
"""Collect completed, bounded p170 campaigns without changing their records.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The complete improving-checkpoint logs are optional runtime files. Their hashes,
row counts and final checkpoints are retained with each collected campaign.
"""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(directory, selected, manifest=True):
    records = []
    logs = []
    for case_id in selected:
        record_path = directory / (case_id + ".json")
        log_path = directory / (case_id + ".jsonl")
        if not record_path.exists():
            raise RuntimeError(f"Incomplete campaign: missing {record_path}")
        record = load(record_path)
        assert record["case"]["id"] == case_id
        rows = [json.loads(line) for line in log_path.read_text().splitlines()
                if line.startswith("{")]
        assert rows and max(rows, key=lambda row: row["score"]) == record["best"]
        assert all(a["score"] < b["score"] for a, b in zip(rows, rows[1:]))
        records.append(record)
        logs.append({"case_id": case_id, "filename": log_path.name,
                     "sha256": digest(log_path), "improving_checkpoints": len(rows),
                     "final_checkpoint_is_archived_best": rows[-1] == record["best"]})
    result = {"summary": load(directory / "SUMMARY.json"),
              "records": records, "runtime_log_inventory": logs}
    if manifest:
        result["run"] = load(directory / "RUN.json")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cross-root", type=Path,
                        default=Path("/tmp/p170-cross-period"))
    parser.add_argument("--radio-historical", type=Path,
                        default=Path("/tmp/p170-radio-historical"))
    parser.add_argument("--only-radio", action="store_true")
    args = parser.parse_args()
    authors = "icekylinx and GPT-6 Astra Pro"
    if not args.only_radio:
        inputs = load(HERE / "cross_period_inputs.json")
        historical_path = args.cross_root / "historical_native_neighbours"
        selected = load(historical_path / "RUN.json")["selected_cases"]
        assert selected == [case["id"] for case in inputs["historical"][:54]]
        result = {
            "schema": "p170-cross-period-results-v1", "prepared_by": authors,
            "initial_controls": collect(args.cross_root / "controls",
                                        [case["id"] for case in inputs["controls"]]),
            "selected_failure_repeats": collect(
                args.cross_root / "controls_stronger",
                [inputs["controls"][i]["id"] for i in (3, 5)], manifest=False),
            "historical": collect(historical_path, selected),
            "limits": [
                "Only the first 54 of 234 frozen historical cases were requested.",
                "The two stronger controls were selected after the initial failures.",
                "The original engine did not instrument exact fitness-call totals.",
                "Configured loop slots are not unique states or actual fitness calls.",
                "No returned historical candidate is an accepted reading."
            ]}
        path = HERE / "cross_period_results.json"
        path.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"saved": path.name,
                          "historical_completed": len(result["historical"]["records"])}))
    selected = load(args.radio_historical / "RUN.json")["selected_jobs"]
    inputs = load(HERE / "radio_historical_inputs.json")
    assert selected == [case["id"] for case in inputs["cases"]]
    result = {"schema": "p170-radio-historical-results-v1", "prepared_by": authors,
              **collect(args.radio_historical, selected),
              "limits": ["All source coordinates and known square cells are fixed.",
                         "Counters count fitness calls, not distinct states.",
                         "No returned historical candidate is an accepted reading."]}
    path = HERE / "radio_historical_results.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"saved": path.name, "summary": result["summary"]}))


if __name__ == "__main__":
    main()
