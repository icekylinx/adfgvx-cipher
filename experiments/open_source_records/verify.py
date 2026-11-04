#!/usr/bin/env python3
"""Verify four literal OPEN sources without inventing a decryption model.

Source review: icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.source_evidence import verify_source_evidence

IDS = {"p70_B1", "p127_B2", "p145_A", "p194_D1"}
COORDINATES = set("ADFGVX")


def verify(pdf=None):
    data = json.loads((HERE / "inputs.json").read_text())
    assert data["schema"] == "adfgvx-open-source-records-v1"
    original = ROOT / data["source_audit"]["path"]
    assert hashlib.sha256(original.read_bytes()).hexdigest() == data["source_audit"]["sha256"]
    audit = json.loads(original.read_text())
    assert data["source"] == audit["source"]
    original_records = {r["id"]: r for r in audit["records"]}
    original_images = {r["id"]: r for r in audit["source_images"]}
    assert len(data["records"]) == len(data["source_images"]) == len(IDS)
    assert {r["id"] for r in data["records"]} == {r["id"] for r in data["source_images"]} == IDS
    counts = []
    for record in data["records"]:
        ident = record["id"]
        old = original_records[ident]
        assert {key: record[key] for key in old} == old, (ident, "Frozen native audit changed")
        assert set(record) == set(old) | {"state", "case_path", "display_header_rows"}
        assert record["state"] == "OPEN"
        assert record["case_path"] == f"cases/open/{ident}.md"
        text = "".join("".join(record["source_rows"]).split())
        assert hashlib.sha256(text.encode()).hexdigest() == record["literal_sha256"]
        assert len(text) == record["source_slots"]
        masks = [{"source_index": i, "glyph": glyph} for i, glyph in enumerate(text)
                 if glyph not in COORDINATES]
        assert masks == record["masked_or_invalid_source_slots"]
        assert len(text) - len(masks) == record["valid_source_coordinates"]
        case = (ROOT / record["case_path"]).read_text()
        displays = re.findall(r"```text\n(.*?)\n```", case, flags=re.S)
        assert displays == ["\n".join(record["display_header_rows"]), "\n".join(record["source_rows"])], ident
        assert "**State: OPEN.**" in case
        assert "icekylinx and GPT-6 Astra Pro" in case
        assert f"| Received source slots | {len(text)} |" in case
        assert f"| Observed ADFGVX coordinates | {len(text) - len(masks)} |" in case
        assert f"| Printed erasure slots | {len(masks)} |" in case
        advertised = record["advertised_length"]
        assert f"| Advertised part length | {'Not printed' if advertised is None else advertised} |" in case
        counts.append({"id": ident, "state": "OPEN", "received_slots": len(text),
                       "observed_coordinates": len(text) - len(masks), "printed_erasures": len(masks),
                       "advertised_part_length": advertised, "accepted_plaintext": None})
    for image in data["source_images"]:
        old = original_images[image["id"]]
        assert image["storage"] == "embedded_png"
        assert {key: image[key] for key in old if key != "storage"} == {
            key: value for key, value in old.items() if key != "storage"}
    pixels = verify_source_evidence(pdf, data["source"], data["source_images"], HERE)
    return {"verified": True, "physical_sources": len(counts), "records": counts,
            "accepted_plaintext_records": 0, "source_evidence": pixels["summary"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.pdf), indent=2))


if __name__ == "__main__":
    main()
