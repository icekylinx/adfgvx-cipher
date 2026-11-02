#!/usr/bin/env python3
"""Shared transport fields and explicitly conditional decimal scenarios.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No inferred digit is written into the historical key or source certificates.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def inspect_pair(ciphertext, ranks, position):
    order = [i for col in sorted(range(len(ranks)), key=ranks.__getitem__)
             for i in range(col, len(ciphertext), len(ranks))]
    source_indices = [None] * len(ciphertext)
    for received, written in enumerate(order):
        source_indices[written] = received
    indices = source_indices[2 * position:2 * position + 2]
    return "".join(ciphertext[i] for i in indices), indices


def analyze():
    old_path = ROOT / "data/certificates/p185_D_transport.json"
    new_path = ROOT / "data/certificates/p197_p198_transport.json"
    old = json.loads(old_path.read_text())
    new = json.loads(new_path.read_text())
    key = new["key"]
    ranks, square = key["column_rank_order"], key["square"]
    assert old["key"]["column_rank_order"] == ranks
    assert old["key"]["square"] == square
    existing = {r["source"]["id"]: r for r in old["direct_transport_context"]}
    recent = {r["id"]: r for r in new["records"]}
    slots = []

    def add(record_id, field, position, ciphertext, geometry, source_map=None):
        pair, indices = inspect_pair(ciphertext, ranks, position)
        assert all(c in COORDS for c in pair)
        cell = 6 * COORDS.index(pair[0]) + COORDS.index(pair[1])
        assert square[cell] == "?"
        slots.append(dict(source_id=record_id, field=field,
                          plaintext_index=position, coordinate_pair=pair,
                          square_cell=cell, geometry=geometry,
                          reconstructed_ciphertext_indices=indices,
                          original_source_indices=indices if source_map is None else
                          [source_map[i] for i in indices]))

    for identifier in ("p194_A", "p196_B"):
        row = existing[identifier]
        ct = row["source"]["analysis_ciphertext"]
        add(identifier, "planned_hour_units", 42, ct, "Literal source analysis")
    for identifier in ("p197_E", "p198_C"):
        row = existing[identifier]
        ct = row["source"]["analysis_ciphertext"]
        add(identifier, "departed_hour_units", 9, ct, "Literal source analysis")
        add(identifier, "remaining_men", 35, ct, "Literal source analysis")
        assert "13.45" in row["source"]["header_literal"]
    corrected_e = new["duplicate_group_repair"]["candidates"][0]
    corrected_d = next(r for r in new["erasure_relocation"]["best_alignments"]
                       if r["insert_erasure_before_surviving_source_index"] == 75)
    for identifier, row in (("p198_E", corrected_e), ("p197_D", corrected_d)):
        add(identifier, "lorry_tonnage", 10, row["corrected_ciphertext"],
            "Declared duplicate deletion or dash-relocation hypothesis",
            row["corrected_to_source_index"])
    add("p198_B", "readiness_hour_units", 74,
        recent["p198_B"]["analysis_ciphertext"], "Literal source analysis")
    corrected_c = new["missing_group_alignment"]["best_alignments"][-1]
    add("p197_C", "readiness_hour_units", 74, corrected_c["corrected_ciphertext"],
        "Declared five-slot gap hypothesis", corrected_c["corrected_to_source_index"])

    expected = {"planned_hour_units": "FV", "lorry_tonnage": "FV",
                "departed_hour_units": "AF", "readiness_hour_units": "GA",
                "remaining_men": "GD"}
    assert all(r["coordinate_pair"] == expected[r["field"]] for r in slots)
    assert len(set(expected.values())) == 4
    unused = sorted(set(ALPHABET) - set(square))
    assert unused == list("234789QY")
    cells = [6 * COORDS.index(p[0]) + COORDS.index(p[1])
             for p in ("FV", "AF", "GA", "GD")]
    digits = [ch for ch in unused if ch.isdigit()]
    numeric = list(itertools.permutations(digits, 4))
    same_day = [a for a in numeric if 10 * 60 + int(a[1]) * 60 <= 13 * 60 + 45]
    # The departure strings are 1<digit>00, so 10 + digit is the hour.
    assert all(10 + int(a[1]) <= 13 for a in same_day)
    not_early = [a for a in same_day if int(a[0]) <= int(a[1])]
    assert [len(numeric), len(same_day), len(not_early)] == [360, 120, 12]
    assert {a[:2] for a in not_early} == {("2", "3")}

    # Separate enumeration of all bijective square completions checks the
    # field-domain counts and keeps repeated-cell identities coupled.
    blanks = [i for i, ch in enumerate(square) if ch == "?"]
    actual = [set(), set(), set()]
    counts = [0, 0, 0]
    for values in itertools.permutations(unused):
        completed = list(square)
        for cell, value in zip(blanks, values):
            completed[cell] = value
        assert len(set(completed)) == 36
        fields = tuple(completed[c] for c in cells)
        if not all(v.isdigit() for v in fields):
            continue
        actual[0].add(fields); counts[0] += 1
        if 10 + int(fields[1]) > 13:
            continue
        actual[1].add(fields); counts[1] += 1
        if int(fields[0]) > int(fields[1]):
            continue
        actual[2].add(fields); counts[2] += 1
    assert actual == [set(numeric), set(same_day), set(not_early)]
    assert counts == [8640, 2880, 288]
    return dict(
        project="ADFGVX Cipher", authors=["icekylinx", "GPT-6 Astra Pro"],
        review_date="2026-11-02", historical_digits_assigned=False,
        input_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (old_path, new_path)},
        shared_key_id=key["id"], unused_symbols="".join(unused), occurrences=slots,
        field_order=["planned_hour_units_and_lorry_tonnage", "departed_hour_units",
                     "readiness_hour_units", "remaining_men"],
        square_cells=cells,
        unconditional_relationships=[
            "The planned departure hour's units character and the lorry tonnage use FV.",
            "The reported departure hour instead uses AF; those characters must differ under a bijective shared square.",
            "The readiness-hour character GA and remaining-men character GD are distinct from both and from each other."
        ],
        scenarios=[
            dict(assumptions="All four unresolved fields are ordinary single decimal digits; retain the stated source geometries and partial key.",
                 field_assignments=360, full_square_completions=8640),
            dict(assumptions="Also treat 13.45 as the departure report's same-day origin time and require its stated 1<AF>00 departure to be no later.",
                 field_assignments=120, full_square_completions=2880,
                 departed_hour_digit_domain=["2", "3"], departed_times=["12:00", "13:00"]),
            dict(assumptions="Also identify the scheduled and departed movements and assume departure was not earlier than the scheduled hour.",
                 field_assignments=12, full_square_completions=288,
                 conditional_cells={"FV": "2", "AF": "3"},
                 conditional_reading="Planned 12:00, departed 13:00, a 2-ton lorry; the other two digits remain distinct members of 4789.")
        ],
        limitations=[
            "The chronology, same-movement relation and no-early-departure condition are semantic hypotheses, not received coordinates.",
            "No ranking or probability is assigned to these scenarios; the narrowest scenario is not promoted to recovered historical digits.",
            "Headers and source errors could invalidate the semantic assumptions. All raw fields and the historical key remain unchanged.",
            "The readiness passage has additional 0/X and 5/F disagreements; interpreting it as a clock also selects between those observed alternatives."
        ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = analyze()
    path = HERE / "linked_fields.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(verified=True, historical_digits_assigned=False,
                         scenario_counts=[s["field_assignments"] for s in result["scenarios"]])))


if __name__ == "__main__":
    main()
