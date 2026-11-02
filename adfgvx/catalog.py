"""Build the two reader-facing ciphertext tables from one curated catalogue.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
This indexes reviewed readings; uninspected OCR candidates are not admitted.
"""
from __future__ import annotations

import argparse
import json
import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/reading_catalog.json"
START = "<!-- READING-CATALOG:START -->"
END = "<!-- READING-CATALOG:END -->"


def load_catalog():
    data = json.loads(DATA.read_text())
    source_ids = {m["id"] for m in json.loads((ROOT / "data/messages.json").read_text())["messages"]}
    assert {r["id"] for r in data["challenge"]} == source_ids
    assert len(data["challenge"]) == 22
    seen = set()
    for group in ("challenge", "other"):
        for row in data[group]:
            assert row["id"] not in seen, row["id"]
            seen.add(row["id"])
            for field in ("label", "subject", "status", "credit", "path"):
                assert isinstance(row[field], str) and row[field].strip(), (row["id"], field)
                assert "\n" not in row[field] and "|" not in row[field], (row["id"], field)
            path = row["path"].split("#")[0]
            assert (ROOT / path).is_file(), path
            for evidence in row.get("evidence", []):
                assert (ROOT / evidence).is_file(), evidence
            if group == "other":
                assert row["source_reviewed"] is True, row["id"]
                assert row["id"] not in source_ids
    return data


def relative_link(path, destination):
    relative_dir = destination.parent.relative_to(ROOT).as_posix()
    file, separator, anchor = path.partition("#")
    link = posixpath.relpath(file, relative_dir)
    return link + ("#" + anchor if separator else "")


def table(rows, destination):
    lines = ["| Ciphertext | Most likely content | Reading status | Reading or review credit |",
             "|---|---|---|---|"]
    for row in rows:
        link = relative_link(row["path"], destination)
        lines.append(f"| [{row['label']}]({link}) | {row['subject']} | {row['status']} | {row['credit']} |")
    return "\n".join(lines)


def render(data, destination):
    other = sorted(data["other"], key=lambda r: (r["printed_page"], r["source_section"], r["id"]))
    return "\n".join([
        START,
        "## The 22 challenge entries", "",
        "These retain the original challenge identifiers. Page numbers alone do not identify a message: p198 is section D, while p198 B/C/E are separate records below.",
        "", table(data["challenge"], destination), "",
        f"## Other ciphertexts — {len(other)} reviewed records", "",
        "Each row identifies a separate source record outside the 22-entry challenge. Multipart messages and repeated transmissions have separate rows even when one case page discusses them together. Direct readings, source-supported reconstructions and conjectural repairs retain their stated limits.",
        "", table(other, destination), "",
        "The catalogue covers source-reviewed records with published reading evidence; the wider OCR search pool contains additional unreviewed ciphertext candidates. Earlier authors retain their credits. Current source review and new research use **icekylinx and GPT-6 Astra Pro**; a review credit does not assert first-decipherment priority.",
        END,
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check committed tables without writing files")
    args = parser.parse_args()
    data = load_catalog()
    for path in (ROOT / "README.md", ROOT / "cases/README.md"):
        current = path.read_text()
        assert current.count(START) == current.count(END) == 1, path
        before, rest = current.split(START)
        _, after = rest.split(END)
        expected = before + render(data, path) + after
        if args.check:
            assert current == expected, f"Regenerate {path.relative_to(ROOT)} with python -m adfgvx.catalog"
        else:
            path.write_text(expected)
    print(f"Catalogue: 22 challenge entries and {len(data['other'])} other source-reviewed records; links and both tables agree.")


if __name__ == "__main__":
    main()
