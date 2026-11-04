#!/usr/bin/env python3
"""Check the canonical catalogue and its restricted evidence identifier alias.

Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx import catalog

OPEN_IDS = {"p73", "p170", "p198", "p70_B1", "p127_B2", "p145_A", "p194_D1"}


def verify():
    data = catalog.load_catalog()
    account = catalog.physical_source_accounting(data)
    rows = {r["id"]: r for group in ("challenge", "other") for r in data[group]}
    assert len(rows) == len(set(account["locations"].values())) == 679
    assert len(data["challenge"]) == 22 and len(data["other"]) == 657
    assert {r["id"] for r in rows.values() if r["state"] == "OPEN"} == OPEN_IDS
    assert "p132_B" not in rows and account["locations"]["p132"] == (132, "B")
    canonical = rows["p132"]
    assert canonical["path"] == "cases/p132.md"
    for credit in ("Thomas", "Norbert", "Max Baertl", "icekylinx", "GPT-6 Astra Pro"):
        assert credit in canonical["credit"]
    alias = next(r for r in catalog.source_record_aliases() if r["record_alias"] == "p132_B")
    assert canonical["prior_reading_credit"] == alias["prior_reading_credit"]
    for path in alias["evidence_paths"]:
        assert catalog.evidence_record_id(canonical, path) == "p132_B"
    assert catalog.evidence_record_id(canonical, "data/messages.json") == "p132"
    # Consolidation keeps the exact source/model streams on the canonical case.
    inputs = json.loads((ROOT / alias["alias_evidence"]["path"]).read_text())
    source = next(r for r in inputs["records"] if r["id"] == "p132_B")
    case = (ROOT / canonical["path"]).read_text()
    for field in ("expected_unmodified_raw", "expected_working_raw", "editorial_text"):
        assert case.count("```text\n" + source[field] + "\n```") == 1, field
    rendered = catalog.table([canonical], ROOT / "cases/README.md")
    assert rendered.splitlines()[0] == "| Source | State | Subject |"
    assert rendered.count("[p132](p132.md)") == 1 and "p132_B" not in rendered
    assert "Thomas" not in rendered  # attribution belongs in data and the case
    return {"verified": True, "physical_sources": 679, "canonical_entries": 679,
            "original_challenge_identifiers": 22, "open_sources": sorted(OPEN_IDS),
            "state_counts": account["state_counts"],
            "restricted_evidence_aliases": [{"canonical_id": r["canonical_id"],
                                              "record_alias": r["record_alias"]}
                                             for r in catalog.source_record_aliases()]}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
