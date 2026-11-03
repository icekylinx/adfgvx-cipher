#!/usr/bin/env python3
"""Check presentation coverage of every current, substantive case page.

This is a read-only inventory and regression check, not a cipher verifier or
an automatic semantic classifier. A reviewed manifest records the roles of
fenced and quoted displays; newly added cases require explicit review.
Prepared by icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import os
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LABELS = {
    "Raw output": "raw_output",
    "Edited output": "edited_output",
    "Readable German": "readable_german",
    "Conditional interpretation": "conditional_interpretation",
    "Source transcription": "source_transcription",
    "Re-encryption witness": "reencryption_witness",
    "Earlier attributed reading": "earlier_attributed_reading",
    "Recomputed prior reading": "recomputed_prior_variant",
    "Search diagnostic": "search_diagnostic",
    "Geometry alternatives": "geometry_alternatives",
    "Meaning": "meaning",
    "English meaning": "meaning",
}
LABEL_PATTERN = re.compile(r"\*\*(" + "|".join(
    re.escape(x) for x in sorted(LABELS, key=len, reverse=True)) + r")\b")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def expected_legend(path):
    link = os.path.relpath(ROOT / "docs/reading-conventions.md", path.parent)
    return ("**Reading layers:** [Raw output · Edited output · Readable German · "
            "Conditional interpretation](" + link + "). In decoded streams, "
            "`?` marks one unresolved position; `X` and numeral/letter labels "
            "remain literal.")


def preceding_paragraph(lines, start):
    end = start - 1
    while end >= 0 and not lines[end].strip():
        end -= 1
    begin = end
    while begin >= 0 and lines[begin].strip():
        if lines[begin].lstrip().startswith(("```", "~~~")):
            break
        begin -= 1
    return "".join(lines[begin + 1:end + 1]).rstrip("\r\n")


def caption_role(paragraph):
    match = LABEL_PATTERN.search(paragraph)
    return LABELS[match.group(1)] if match else None


def displays(text):
    """Return complete fenced records and explicit Markdown quote displays."""
    lines = text.splitlines(keepends=True)
    fences, quotes = [], []
    number = 0
    while number < len(lines):
        line = lines[number]
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})([^\r\n]*)", line)
        if opening:
            marker, language = opening.group(1), opening.group(2).strip()
            end = number + 1
            close = re.compile(r"^ {0,3}" + re.escape(marker[0]) + "{" +
                               str(len(marker)) + r",}[ \t]*(?:\r?\n)?$")
            while end < len(lines) and not close.fullmatch(lines[end]):
                end += 1
            if end == len(lines):
                raise ValueError("Unterminated fence at line " + str(number + 1))
            complete = "".join(lines[number:end + 1])
            body = "".join(lines[number + 1:end])
            paragraph = preceding_paragraph(lines, number)
            role = caption_role(paragraph)
            if role is None and (language in ("sh", "shell", "bash") or
                                 body.lstrip().startswith(("python ", "python3 "))):
                role = "reproduction_command"
            fences.append({"index": len(fences), "line": number + 1,
                           "sha256": sha(complete.encode()),
                           "body_sha256": sha(body.rstrip("\r\n").encode()),
                           "language": language, "role_from_caption": role,
                           "caption": paragraph})
            number = end + 1
        elif re.match(r"^ {0,3}>", line):
            end = number + 1
            while end < len(lines):
                if re.match(r"^ {0,3}>", lines[end]):
                    end += 1
                elif (not lines[end].strip() and end + 1 < len(lines)
                      and re.match(r"^ {0,3}>", lines[end + 1])):
                    end += 1
                else:
                    break
            paragraph = preceding_paragraph(lines, number)
            quotes.append({"index": len(quotes), "line": number + 1,
                           "sha256": sha("".join(lines[number:end]).encode()),
                           "role_from_caption": caption_role(paragraph),
                           "caption": paragraph})
            number = end
        else:
            number += 1
    return fences, quotes


def inventory():
    records, skipped, errors = [], [], []
    for path in sorted((ROOT / "cases").rglob("*.md")):
        name = path.relative_to(ROOT).as_posix()
        text = path.read_text()
        if path.name == "README.md":
            skipped.append({"path": name, "reason": "navigation README"})
            continue
        first_heading = next((line for line in text.splitlines()
                              if line.startswith("# ")), "")
        if first_heading == "# Reading location":
            skipped.append({"path": name, "reason": "compatibility redirect"})
            continue
        try:
            fences, quotes = displays(text)
        except ValueError as error:
            errors.append({"path": name, "error": str(error)})
            continue
        records.append({"path": name, "file_sha256": sha(text.encode()),
                        "legend_exact": text.count(expected_legend(path)) == 1,
                        "legend_occurrences": text.count("**Reading layers:**"),
                        "fences": fences, "quotes": quotes})
    return {"schema": "adfgvx-reading-presentation-inventory-v1",
            "prepared_by": "icekylinx and GPT-6 Astra Pro",
            "scope": "All current substantive cases, excluding README navigation and explicit compatibility redirects.",
            "files": records, "skipped": skipped, "errors": errors}


def check(current, manifest):
    failures = list(current["errors"])
    existing = {r["path"]: r for r in current["files"]}
    reviewed = {r["path"]: r for r in manifest["files"]}
    roles, quote_roles = Counter(), Counter()
    for name in sorted(existing.keys() - reviewed.keys()):
        failures.append({"path": name, "error": "New case has no reviewed classification"})
    for name in sorted(reviewed.keys() - existing.keys()):
        failures.append({"path": name, "error": "Reviewed case is missing or no longer substantive"})
    for name, record in existing.items():
        if not record["legend_exact"] or record["legend_occurrences"] != 1:
            failures.append({"path": name, "error": "Shared reading-layer legend is missing, changed or duplicated"})
        if name not in reviewed:
            continue
        expected = reviewed[name]
        if expected.get("review_status") != "reviewed":
            failures.append({"path": name, "error": "Case classification is not marked reviewed"})
        for kind, counts in (("fences", roles), ("quotes", quote_roles)):
            actual_items, wanted = record[kind], expected[kind]
            if len(actual_items) != len(wanted):
                failures.append({"path": name, "error": kind + " count differs",
                                 "expected": len(wanted), "actual": len(actual_items)})
                continue
            for actual, prior in zip(actual_items, wanted):
                label = prior.get("role")
                counts[label or "unclassified"] += 1
                if not label:
                    failures.append({"path": name, "kind": kind, "index": actual["index"],
                                     "error": "Display has no reviewed role"})
                if actual["index"] != prior["index"] or actual["sha256"] != prior["sha256"]:
                    failures.append({"path": name, "kind": kind, "index": actual["index"],
                                     "error": "Reviewed display bytes or order differ"})
                if prior.get("caption_required", True):
                    if actual["role_from_caption"] != label:
                        failures.append({"path": name, "kind": kind, "index": actual["index"],
                                         "error": "Visible layer caption is missing or disagrees with reviewed role",
                                         "expected_role": label,
                                         "actual_role": actual["role_from_caption"]})
                if actual["caption"] != prior.get("caption"):
                    failures.append({"path": name, "kind": kind, "index": actual["index"],
                                     "error": "Reviewed caption or local qualifier changed"})
    return {"schema": "adfgvx-reading-presentation-check-v1",
            "prepared_by": "icekylinx and GPT-6 Astra Pro",
            "verified": not failures, "scope": current["scope"],
            "substantive_case_files": len(existing),
            "reviewed_case_files": len(reviewed),
            "fenced_displays": sum(len(r["fences"]) for r in existing.values()),
            "quoted_displays": sum(len(r["quotes"]) for r in existing.values()),
            "skipped_readmes": sum(r["reason"] == "navigation README" for r in current["skipped"]),
            "skipped_redirects": sum(r["reason"] == "compatibility redirect" for r in current["skipped"]),
            "fence_roles": dict(sorted(roles.items())),
            "quote_roles": dict(sorted(quote_roles.items())),
            "failures": failures,
            "limits": ["Roles are reviewed editorial classifications, not automatically inferred semantic facts.",
                       "This check does not decrypt, certify repairs, authenticate source images or prove historical wording.",
                       "Existing before-snapshot audits separately prove that presentation edits preserved earlier machine strings and headings."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=HERE / "reading_layer_manifest.json")
    parser.add_argument("--output", type=Path, help="Write the check report as JSON")
    parser.add_argument("--inventory-output", type=Path,
                        help="Write a current inventory for review; does not update the manifest or cases")
    args = parser.parse_args()
    current = inventory()
    if args.inventory_output:
        args.inventory_output.write_text(json.dumps(current, indent=2) + "\n")
    try:
        manifest = json.loads(args.manifest.read_text())
        result = check(current, manifest)
        result["manifest_sha256"] = sha(args.manifest.read_bytes())
    except (OSError, ValueError, KeyError) as error:
        result = {"verified": False, "error": str(error),
                  "substantive_case_files": len(current["files"])}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
