#!/usr/bin/env python3
"""Verify the bounded follow-up display correction and its existing evidence.

Read-only; standard library only; works from any current directory.
Prepared by icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import json
import sys

from verify_semantic_readings import normalized_display, run as semantic_check

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def at_pointer(value, pointer):
    for component in pointer:
        value = value[component]
    return value


def run(snapshot_path, audit_path):
    result = semantic_check(snapshot_path, audit_path)
    audit = json.loads(audit_path.read_text())
    source_checks = []
    for mapping in audit["mappings"]:
        checks = []
        for label in ("source_input", "source_certificate"):
            reference = mapping[label]
            if reference["path"] not in audit["protected_unchanged"]:
                raise ValueError("A mapping source is not protected by the evidence digest ledger")
            source = json.loads((ROOT / reference["path"]).read_text())
            matched = at_pointer(source, reference["pointer"]) == mapping["source_fragment"]
            checks.append(matched)
            if not matched:
                result["failures"].append({"id": mapping["id"], "error": "Source template differs", "basis": label})
        counted = len(normalized_display(mapping["display_fragment"]))
        if counted != mapping["matched_nonseparator_labels"]:
            result["failures"].append({"id": mapping["id"], "error": "Display-label count differs"})
        source_checks.append({"id": mapping["id"], "matched_labels": counted,
                              "input_and_certificate_match": all(checks)})
    result.update({"schema": "adfgvx-readable-followup-check-v1",
                   "verified": not result["failures"],
                   "exact_source_bindings": source_checks,
                   "mapped_nonseparator_labels": sum(row["matched_labels"] for row in source_checks)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Read-only verification is also the default.")
    parser.add_argument("--snapshot", type=Path, default=HERE / "reading_conventions_followup_before.json")
    parser.add_argument("--audit", type=Path, default=HERE / "reading_conventions_followup_audit.json")
    parser.add_argument("--output", type=Path, help="Optional result file; cases and evidence are never written.")
    args = parser.parse_args()
    try:
        result = run(args.snapshot, args.audit)
    except (OSError, ValueError, KeyError, IndexError) as error:
        result = {"verified": False, "error": str(error)}
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
