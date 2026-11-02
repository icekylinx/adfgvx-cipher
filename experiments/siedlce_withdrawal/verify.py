#!/usr/bin/env python3
"""Verify the exact p200 A source edition and its independent identity witness.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published period key: Lasry, Niebel, Kopal and Wacker.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt
from experiments.withdrawal_recovery.verify import reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    source, context, key, record = (inputs[k] for k in ("source", "independent_context", "key", "record"))
    assert sha(HERE / source["crop"]) == source["crop_sha256"]
    for name in ("signature_crop", "title_crop"):
        assert sha(HERE / context[name]) == context[name + "_sha256"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"] if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    groups = " ".join(record["source_rows"]).split()
    assert len(groups) == 66 and all(len(g) == 5 for g in groups)
    literal = "".join(groups)
    assert len(literal) == record["source_slot_count"] == 330
    assert literal.count("-") == record["source_erasures"] == 1
    assert set(literal) <= set("ADFGVX-")
    analysis = literal.replace("-", "?")
    raw = reading(analysis, ranks, square)
    edition = repair(analysis, literal, record["editorial_recipe"], ranks, square, raw)
    assert len(edition["ciphertext"]) == len(analysis)
    assert len(edition["known_coordinate_substitutions"]) == 11
    assert len(edition["erasure_fills"]) == 1
    assert edition["erasure_fills"][0]["source_position_0based"] == 224
    assert edition["erasure_fills"][0]["proposed"] == "F"
    assert raw["fixed_positions"] == 163 and raw["plaintext_positions"] == 165
    assert edition["reading"]["fixed_positions"] == 165
    assert edition["reading"]["plaintext"] == record["editorial_recipe"]["text"]
    assert encrypt(edition["reading"]["plaintext"], ranks, square) == edition["ciphertext"]
    assert edition["reading"]["plaintext"].count("SIEDLCE") == 2
    for spelling in record["literal_spellings_retained"]:
        assert spelling in raw["plaintext"] and spelling in edition["reading"]["plaintext"]
    raw["global_witness"] = global_witness(analysis, ranks, square, raw)
    fixed_differences = sum(a != b for a, b in zip(analysis, edition["ciphertext"]) if a != "?")
    assert fixed_differences == 11
    for edit in edition["known_coordinate_substitutions"] + edition["erasure_fills"]:
        p = edit["source_position_0based"]
        edit["printed_group_1based"] = p // 5 + 1
        edit["coordinate_within_group_1based"] = p % 5 + 1
    return {
        "schema": "adfgvx-siedlce-withdrawal-certificate-v1",
        "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
        "inputs_sha256": sha(HERE / "inputs.json"),
        "source_literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
        "source_literal": literal, "analysis_ciphertext": analysis,
        "summary": {"source_slots": 330, "known_source_coordinates": 329,
                    "source_erasures": 1, "insertions": 0, "deletions": 0,
                    "plaintext_positions": 165, "raw_fixed_positions": 163,
                    "edition_fixed_positions": 165, "known_coordinate_substitutions": 11,
                    "erasure_fills": 1, "published_square_changes": 0},
        "raw": raw, "edition": edition,
        "same_length_roundtrip_under_unchanged_published_partial_square": True,
        "independent_context": context,
        "limits": ["The proposed wording is an editorial repair of eleven observed coordinates and one erased slot.",
                   "Exact re-encryption proves consistency and edit cost under the fixed key; it does not prove the original wording was unique.",
                   "GARISON and MINSKMAZIOWICKI remain as observed; no letters are inserted to normalize them.",
                   "The identity witness supports only the signer's name and office, not the reported troop movements."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--context-pdf", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    if args.pdf:
        assert sha(args.pdf) == inputs["source"]["pdf_sha256"]
    if args.context_pdf:
        assert sha(args.context_pdf) == inputs["independent_context"]["pdf_sha256"]
    result = run()
    target = HERE / "certificate.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
