#!/usr/bin/env python3
"""Check the explicitly historical 6th Reserve Division completion.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Historical identification is sourced in military_context.json; this program
checks its cipher consequences, not the truth of a historical assertion.
"""
import argparse
import itertools
import json
from pathlib import Path
from verify_seifert import ALPHABET, COORD, HERE, arithmetic, digest, encode
from verify_military import verify as verify_base


def verify(french_pdf=None, calendar_pdf=None):
    base_report = verify_base()
    data = json.loads((HERE / "military_context.json").read_text())
    base = json.loads((HERE / "military_records.json").read_text())
    records = {record["id"]: record for record in base["records"]}
    partial = data["published_partial_square"]
    ranks = data["column_rank_order"]
    assert data["prepared_by"] == "icekylinx and GPT-6 Astra Pro"
    assert partial == records["p166_A2"]["partial_square"]
    assert ranks == records["p166_A2"]["column_rank_order"]
    unknown = [index for index, letter in enumerate(partial) if letter == "?"]
    assert unknown == [26, 30]
    assert [COORD[i // 6] + COORD[i % 6] for i in unknown] == ["VF", "XA"]
    assert set(ALPHABET) - set(partial) == set("56")
    square = data["contextual_square"]
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert all(a == "?" or a == b for a, b in zip(partial, square))
    assert data["contextual_cell_assignments"] == {"VF": "6", "XA": "5"}
    assert square[26] == "6" and square[30] == "5"
    source_ids = {source["id"]: source for source in data["sources"]}
    french = source_ids["franchet_1918_11_19"]
    assert french["transmission_date_time"] == "1918-11-19 22:40"
    assert french["reported_situation_date"] == "1918-11-11"
    assert french["publication_year"] == 1993
    assert french["document_number"] == 39
    assert french["relevant_printed_page"] == 79
    assert french["relevant_pdf_page_1based"] == 153
    assert len(french["short_quote"].split()) <= 25
    if french_pdf:
        assert digest(french_pdf) == french["pdf_sha256"]
    if calendar_pdf:
        assert digest(calendar_pdf) == source_ids["ruhmeshalle_calendar"]["pdf_sha256"]
    summaries = []
    assert len(data["views"]) == 4
    for view in data["views"]:
        source = (base["third_part_composite"]["editorial_emendation"]
                  if view["id"] == "p166_A3_composite"
                  else records[view["id"]]["editions"][0])
        cipher = source["ciphertext"]
        assert view["ciphertext"] == cipher
        assert view["ciphertext_changes_for_contextual_digit"] == 0
        raw, domains, cells = arithmetic(cipher, ranks, partial)
        selected, _, _ = arithmetic(cipher, ranks, square)
        assert raw == source["plaintext"] == view["cipher_only_plaintext"]
        assert selected == view["contextual_plaintext"]
        position = view["new_contextual_position_0based"]
        assert [i for i, (a, b) in enumerate(zip(raw, selected)) if a != b] == [position]
        assert raw[position] == "?" and domains[position] == "56"
        assert cells[position] == [26] and selected[position] == "6"
        assert view["cipher_only_domain"] == "56" and view["square_cell"] == "VF"
        assert encode(selected, ranks, square) == cipher
        # Both cipher-only alternatives remain exact global witnesses.
        witnesses = []
        for digits in itertools.permutations("56"):
            alternative = list(partial)
            for index, digit in zip(unknown, digits):
                alternative[index] = digit
            alternative = "".join(alternative)
            text, _, _ = arithmetic(cipher, ranks, alternative)
            assert encode(text, ranks, alternative) == cipher
            witnesses.append(text[position])
        assert sorted(witnesses) == ["5", "6"]
        summaries.append({"id": view["id"], "position_0based": position,
                          "cipher_only_domain": "56", "contextual_reading": "6",
                          "additional_ciphertext_edits": 0})
    return {"status": "passed", "base_source_records": base_report["source_records"],
            "contextual_digit_occurrences": len(summaries), "independent_digit_choices": 1,
            "cipher_only_alternatives_retained": [5, 6],
            "source_pdf_hashes_checked": {"french": bool(french_pdf), "calendar": bool(calendar_pdf)},
            "views": summaries,
            "scope": "Cipher consequences of an explicitly historical identification; the original key and cipher-only domains remain unchanged."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--french-pdf", type=Path)
    parser.add_argument("--calendar-pdf", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = verify(args.french_pdf, args.calendar_pdf)
    print(json.dumps(report, indent=2) if args.json else
          "Historical context: 4 reserve-division occurrences select 6 with 0 extra cipher edits; both cipher-only alternatives remain valid.")


if __name__ == "__main__":
    main()
