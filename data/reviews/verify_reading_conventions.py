#!/usr/bin/env python3
"""Check the frozen presentation snapshot against the current case files.

Read-only, standard-library verification. No git checkout or old workspace
path is required. Prepared by icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def fence_blocks(text):
    """Retain complete fenced blocks, including delimiters and newlines."""
    lines = text.splitlines(keepends=True)
    blocks, heading_lines = [], []
    opening = None
    start = None
    for number, line in enumerate(lines):
        if opening is None:
            match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*?)(?:\r?\n)?$", line)
            if match:
                opening = match.group(1)
                start = number
            elif re.match(r"^#{1,6} ", line):
                heading_lines.append(line.rstrip("\r\n"))
        else:
            closing = re.fullmatch(r" {0,3}" + re.escape(opening[0])
                                   + "{" + str(len(opening)) + r",}[ \t]*(?:\r?\n)?", line)
            if closing:
                blocks.append("".join(lines[start:number + 1]))
                opening = None
                start = None
    if opening is not None:
        raise ValueError("Unterminated fenced block")
    return blocks, heading_lines


def remove_reviewed_additions(text, additions):
    """Exclude only exact, separately reviewed supplements from an old snapshot.

    Each registered section is pinned in full, including its heading and
    displays. All original displays and headings still require exact equality.
    """
    for addition in additions:
        start, end = addition["start_heading"], addition["next_heading"]
        if text.count(start) != 1 or (end is not None and text.count(end) != 1):
            raise ValueError("Reviewed supplement boundaries are not unique")
        begin = text.index(start)
        finish = len(text) if end is None else text.index(end, begin + len(start))
        if sha_bytes(text[begin:finish].encode()) != addition["section_sha256"]:
            raise ValueError("Reviewed supplement digest mismatch")
        text = text[:begin] + text[finish:]
    return text


def run(snapshot_path, audit_path, check_headings):
    snapshot_bytes = snapshot_path.read_bytes()
    snapshot = json.loads(snapshot_bytes)
    audit = json.loads(audit_path.read_text()) if audit_path else None
    if audit and audit.get("before_snapshot_sha256"):
        if sha_bytes(snapshot_bytes) != audit["before_snapshot_sha256"]:
            raise ValueError("Frozen before-snapshot digest mismatch")
    failures, records = [], []
    for name, before in snapshot.items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("Snapshot path is outside the repository: " + name)
        current_bytes = path.read_bytes()
        additions = (audit or {}).get("reviewed_additive_sections", {}).get(name, [])
        comparison_text = remove_reviewed_additions(current_bytes.decode(), additions)
        current, headings = fence_blocks(comparison_text)
        originals = []
        for index, block in enumerate(before["fences"]):
            if sha_bytes(block["text"].encode()) != block["sha256"]:
                raise ValueError(f"Invalid frozen block digest: {name}, block {index}")
            originals.append(block["text"])
        unchanged = originals == current
        headings_equal = before["headings"] == headings
        if not unchanged:
            failures.append({"path": name, "error": "Fenced blocks differ",
                             "before_count": len(originals), "current_count": len(current)})
        if check_headings and not headings_equal:
            failures.append({"path": name, "error": "Existing section headings differ"})
        records.append({"path": name, "fenced_blocks": len(originals),
                        "reviewed_additive_sections": len(additions),
                        "fenced_blocks_identical": unchanged,
                        "section_headings_identical": headings_equal,
                        "current_file_sha256": sha_bytes(current_bytes)})
    protected = []
    if audit:
        for name, expected in audit.get("protected_unchanged", {}).items():
            actual = sha_bytes((ROOT / name).read_bytes())
            ok = actual == expected
            protected.append({"path": name, "unchanged": ok, "sha256": actual})
            if not ok:
                failures.append({"path": name, "error": "Protected evidence digest differs"})
    return {"schema": "adfgvx-reading-conventions-current-check-v1",
            "prepared_by": "icekylinx and GPT-6 Astra Pro",
            "scope": "Only files in the stated frozen before snapshot; no assertion of coverage of later new cases.",
            "snapshot_sha256": sha_bytes(snapshot_bytes),
            "case_files_checked": len(records),
            "fenced_blocks_checked": sum(r["fenced_blocks"] for r in records),
            "reviewed_additive_sections_checked": sum(r["reviewed_additive_sections"] for r in records),
            "check_section_headings": check_headings,
            "protected_evidence_files_checked": len(protected),
            "verified": not failures, "failures": failures,
            "files": records, "protected_evidence": protected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path,
                        default=HERE / "reading_conventions_safe_before.json")
    parser.add_argument("--audit", type=Path,
                        default=HERE / "reading_conventions_safe_audit.json")
    parser.add_argument("--allow-heading-changes", action="store_true",
                        help="Report heading equality without making it a required check")
    parser.add_argument("--output", type=Path,
                        help="Optional JSON report; case files are never written")
    args = parser.parse_args()
    try:
        result = run(args.snapshot, args.audit, not args.allow_heading_changes)
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({"verified": False, "error": str(error)}, indent=2))
        return 1
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "verified", "case_files_checked", "fenced_blocks_checked", "reviewed_additive_sections_checked",
        "check_section_headings", "protected_evidence_files_checked", "failures")}, indent=2))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
