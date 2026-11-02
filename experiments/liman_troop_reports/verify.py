#!/usr/bin/env python3
"""Verify the source-exact p222 Liman troop-report request.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The period key is prior work by Lasry, Niebel, Kopal and Wacker.
This standalone verifier uses only the Python standard library.
"""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def columns(length, ranks):
    width = len(ranks)
    return [index for col in sorted(range(width), key=lambda c: ranks[c])
            for index in range(col, length, width)]


def read(cipher, ranks, square):
    order = columns(len(cipher), ranks)
    interim = [None] * len(cipher)
    positions = [None] * len(cipher)
    for source, index in enumerate(order):
        interim[index] = cipher[source]
        positions[index] = source
    text = "".join(square[6 * CO.index(interim[i]) + CO.index(interim[i + 1])]
                   for i in range(0, len(cipher), 2))
    return text, [positions[i:i + 2] for i in range(0, len(cipher), 2)]


def encipher(text, ranks, square):
    flat = "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)
    width = len(ranks)
    return "".join(flat[col::width] for col in sorted(range(width), key=lambda c: ranks[c]))


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    source, key = inputs["source"], inputs["key"]
    assert sha(HERE / source["crop"]) == source["crop_sha256"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    assert set(square) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") and len(square) == 36
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    records = []
    for rec in inputs["records"]:
        groups = " ".join(rec["source_rows"]).split()
        literal = "".join(groups)
        assert set(literal) <= set(CO)
        assert len(literal) == rec["source_slot_count"] == rec["advertised_length"]
        assert all(len(group) == 5 for group in groups[:-1])
        raw, pairs = read(literal, ranks, square)
        assert raw == rec["expected_raw"]
        assert encipher(raw, ranks, square) == literal
        text = rec["editorial_text"]
        assert len(text) == len(raw)
        edited = encipher(text, ranks, square)
        owner = {source_pos: index for index, pair in enumerate(pairs) for source_pos in pair}
        changes = [
            {"source_position_0based": i, "printed_group_1based": i // 5 + 1,
             "within_group_1based": i % 5 + 1,
             "observed": a, "proposed": b, "plaintext_position_0based": owner[i]}
            for i, (a, b) in enumerate(zip(literal, edited)) if a != b
        ]
        assert read(edited, ranks, square)[0] == text
        labels = []
        for i, char in enumerate(raw):
            if char.isdigit() or char in "JQY":
                assert text[i] == char
                pair = "".join(literal[p] for p in pairs[i])
                assert all(literal[p] == edited[p] for p in pairs[i])
                labels.append({"plaintext_position_0based": i, "raw_label": char,
                               "coordinate_pair": pair, "source_positions_0based": pairs[i]})
        records.append({
            "id": rec["id"], "source_literal": literal,
            "source_literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
            "source_slots": len(literal), "raw_plaintext": raw,
            "plaintext_positions": len(raw), "raw_fixed_label_positions": len(raw),
            "source_position_pairs_0based": pairs,
            "editorial_plaintext": text, "editorial_ciphertext": edited,
            "known_coordinate_substitutions": changes,
            "preserved_numeral_and_rare_label_fields": labels,
            "raw_and_edition_roundtrip": True,
        })
    assert [len(rec["known_coordinate_substitutions"]) for rec in records] == [0, 1]
    assert records[0]["preserved_numeral_and_rare_label_fields"] == [
        {"plaintext_position_0based": 34, "raw_label": "9", "coordinate_pair": "VD",
         "source_positions_0based": records[0]["source_position_pairs_0based"][34]}]
    return {
        "schema": "adfgvx-liman-troop-reports-certificate-v1",
        "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
        "inputs_sha256": sha(HERE / "inputs.json"),
        "summary": {"source_records": 2, "source_slots": 414,
                    "raw_fixed_label_positions": 207, "plaintext_positions": 207,
                    "known_coordinate_substitutions": 1,
                    "source_erasures": 0, "insertions": 0, "deletions": 0,
                    "reordered_blocks": 0, "published_square_changes": 0},
        "records": records,
        "limits": [
            "Raw label 9 in 9EDE and all J/digit footer labels are preserved; they are not certified original numeral or rare-letter meanings.",
            "The optional JEDE interpretation is lexical, not a source repair or a completed globally bijective square.",
            "The header's November 26 / December 18 distinction is preserved without resolving the chronology.",
            "One observed-coordinate substitution restores BESONDERE. Exact re-encryption certifies consistency and price, not unique historical wording.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.pdf:
        inputs = json.loads((HERE / "inputs.json").read_text())
        assert sha(args.pdf) == inputs["source"]["pdf_sha256"]
    result = run()
    output = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(output.read_text())
    else:
        output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
