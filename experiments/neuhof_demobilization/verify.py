#!/usr/bin/env python3
"""Verify p228 B's Neuhof instruction and separately limited middle opening.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Prior period key: Lasry, Niebel, Kopal and Wacker. No key changes or
numerical relabellings are applied by this source edition.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.withdrawal_recovery.verify import reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    for image in inputs["source_images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
    key = inputs["key"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    records = []
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-") and len(literal) == rec["source_slots"]
        cipher = literal.replace("-", "?")
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, literal, rec["editorial_recipe"], ranks, square, raw)
        start, end = rec["claimed_ordinary_language_span_0based"]
        assert 0 <= start < end <= raw["plaintext_positions"]
        if rec["id"] == "p228_B2":
            assert rec["editorial_recipe"]["text"][33:] == "?" * 99
            for index in range(33, raw["plaintext_positions"]):
                assert edition["reading"]["domains"][index] == raw["domains"][index]
        for edit in edition["known_coordinate_substitutions"] + edition["erasure_fills"]:
            source_index = edit["source_position_0based"]
            edit["printed_group_1based"] = source_index // 5 + 1
            edit["within_group_1based"] = source_index % 5 + 1
            assert start <= edit["plaintext_position_0based"] < end
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        labels = []
        for index, char in enumerate(raw["plaintext"]):
            if char.isdigit() or char in "JQY":
                positions = raw["source_position_pairs_0based"][index]
                labels.append({
                    "plaintext_position_0based": index, "raw_label": char,
                    "editorial_label": edition["reading"]["plaintext"][index],
                    "source_positions_0based": positions,
                    "source_pair": "".join(cipher[p] for p in positions),
                    "source_pair_changed": any(cipher[p] != edition["ciphertext"][p] for p in positions),
                    "within_claimed_ordinary_language_span": start <= index < end,
                })
        records.append({
            "id": rec["id"], "source_literal": literal,
            "source_literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
            "advertised_length_literal": rec["advertised_length_literal"],
            "counted_source_slots": len(literal), "printed_dash_slots": literal.count("-"),
            "raw": raw, "edition": edition,
            "claimed_ordinary_language_span_0based": [start, end],
            "positions_without_proposed_coherent_original_body": 99 if rec["id"] == "p228_B2" else 0,
            "raw_numeral_and_rare_label_inventory": labels,
        })
    assert [r["counted_source_slots"] for r in records] == [246, 264, 186]
    assert [r["printed_dash_slots"] for r in records] == [6, 43, 1]
    assert [r["raw"]["fixed_positions"] for r in records] == [117, 89, 92]
    assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [122, 99, 93]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [5, 5, 0]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [5, 10, 1]
    assert "NICHIN" in records[0]["edition"]["reading"]["plaintext"]
    assert "DARMSADT" in records[2]["edition"]["reading"]["plaintext"]
    return {
        "schema": "adfgvx-neuhof-demobilization-certificate-v1",
        "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
        "inputs_sha256": sha(HERE / "inputs.json"),
        "summary": {"physical_source_parts": 3, "counted_source_slots": 696,
                    "known_received_coordinates": 646, "printed_dash_slots": 50,
                    "plaintext_positions": 348, "raw_fixed_label_positions": 298,
                    "edition_fixed_label_positions": 314,
                    "known_coordinate_substitutions": 10, "erasure_fills": 16,
                    "middle_part_claimed_opening_positions": 33,
                    "middle_part_positions_without_coherent_original_reading": 99,
                    "insertions": 0, "deletions": 0, "reordered_blocks": 0,
                    "published_square_changes": 0},
        "records": records,
        "limits": [
            "The 314 fixed edition labels include untouched, uninterpreted labels in B2's final 99 positions; that total is not a count of recovered coherent original-language characters.",
            "B1 retains the shortened NICHIN and B3 retains DARMSADT. No missing T is silently inserted.",
            "B3 uses its actual 186 slots despite the uncertain printed RICHI-196? label. The source length discrepancy is preserved, not resolved by assumed missing ciphertext.",
            "The Flak unit's ?0 field, reference digits and rare-letter values remain unassigned. Raw Y is not globally relabelled.",
            "The middle opening is a conditional editorial reconstruction requiring five known-coordinate changes and ten erasure fills. Its remaining 99 positions have no proposed coherent original body.",
            "Globally consistent source-fill witnesses prove arithmetic consistency only; they are not original plaintext claims.",
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
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
