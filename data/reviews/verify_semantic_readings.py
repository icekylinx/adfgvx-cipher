#!/usr/bin/env python3
"""Verify the bounded readable-display corrections and their frozen evidence.

This standard-library check proves preservation and the explicitly listed
character mappings. It does not judge German grammar, identify historical
people, solve a square, or certify a new coordinate repair.
Prepared by icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import unicodedata

from verify_reading_conventions import fence_blocks, run as preservation_check

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized_display(fragment, remove_bracketed_alternative=False):
    """Apply only the display transformations declared in this review."""
    if remove_bracketed_alternative:
        fragment = re.sub(r"\[[^\[\]]*\]", "", fragment)
    for before, after in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                          ("Ä", "AE"), ("Ö", "OE"), ("Ü", "UE"),
                          ("ß", "ss")):
        fragment = fragment.replace(before, after)
    fragment = unicodedata.normalize("NFD", fragment).upper()
    return re.sub(r"[^A-Z0-9?]", "", fragment)


def is_subsequence(before, after):
    iterator = iter(after)
    return all(any(value == old for value in iterator) for old in before)


def run(snapshot_path, audit_path):
    audit = json.loads(audit_path.read_text())
    snapshot = json.loads(snapshot_path.read_text())
    preservation = preservation_check(snapshot_path, audit_path, True)
    failures = list(preservation["failures"])
    mappings = []
    inline_total = 0
    for name, before in snapshot.items():
        current = (ROOT / name).read_text()
        prior_inline = before["inline_code"]
        current_inline = re.findall(r"(?<!`)`([^`\n]+)`(?!`)", current)
        inline_total += len(prior_inline)
        if not is_subsequence(prior_inline, current_inline):
            failures.append({"path": name, "error": "Prior inline-code occurrences no longer appear in order"})
    for record in audit["changes"]:
        name = record["path"]
        current = (ROOT / name).read_text()
        if record["display_before"] not in snapshot[name]["text"]:
            failures.append({"path": name, "error": "Recorded old display is absent from the frozen before text"})
        if record["display_after"] not in current:
            failures.append({"path": name, "error": "Reviewed new display changed"})
        for note in record["required_notes"]:
            if note not in current:
                failures.append({"path": name, "error": "Required local display qualification changed", "note": note})
    for record in audit["mappings"]:
        name = record["path"]
        current = (ROOT / name).read_text()
        blocks, _ = fence_blocks(current)
        block = blocks[record["fence_index"]]
        body = "\n".join(block.splitlines()[1:-1])
        source = record["source_fragment"]
        start = record["source_character_offset_in_fence_body"]
        source_ok = body[start:start + len(source)] == source
        display = record["display_fragment"]
        display_ok = display in current
        normalized = normalized_display(display, record.get("remove_bracketed_alternative", False))
        expected = source.replace("X", "") if record.get("source_X_as_spacing") else source
        if record["kind"] == "exact_display_mapping":
            relation_ok = normalized == expected
        elif record["kind"] == "attributed_interpretation":
            relation_ok = (normalized == record["attributed_display_labels"]
                           and normalized != expected
                           and record["qualification"] in current)
        else:
            relation_ok = False
        unknown_count_ok = ("unknown_positions" not in record or
                            source.count("?") == normalized.count("?") == record["unknown_positions"])
        ok = source_ok and display_ok and relation_ok and unknown_count_ok
        if not ok:
            failures.append({"id": record["id"], "path": name,
                             "error": "Declared source/display relation changed",
                             "source_ok": source_ok, "display_ok": display_ok,
                             "relation_ok": relation_ok, "unknown_count_ok": unknown_count_ok})
        mappings.append({"id": record["id"], "kind": record["kind"],
                         "source_fragment": source,
                         "display_labels_after_declared_transforms": normalized,
                         "verified": ok})
    return {"schema": "adfgvx-readable-semantic-check-v1",
            "prepared_by": "icekylinx and GPT-6 Astra Pro",
            "verified": not failures,
            "case_files_checked": len(snapshot),
            "fenced_blocks_checked": preservation["fenced_blocks_checked"],
            "prior_headings_checked": sum(len(x["headings"]) for x in snapshot.values()),
            "prior_inline_code_occurrences_checked": inline_total,
            "protected_evidence_files_checked": preservation["protected_evidence_files_checked"],
            "exact_display_mappings_checked": sum(x["kind"] == "exact_display_mapping" for x in mappings),
            "attributed_interpretations_checked": sum(x["kind"] == "attributed_interpretation" for x in mappings),
            "snapshot_sha256": sha(snapshot_path.read_bytes()),
            "audit_sha256": sha(audit_path.read_bytes()),
            "mappings": mappings, "failures": failures,
            "limits": audit["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=HERE / "reading_conventions_semantic_before.json")
    parser.add_argument("--audit", type=Path, default=HERE / "reading_conventions_semantic_audit.json")
    parser.add_argument("--output", type=Path, help="Optional JSON report; evidence and case files are never written")
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
