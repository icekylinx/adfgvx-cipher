#!/usr/bin/env python3
"""Verify p171 B's newspaper-sack route instruction.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Prior period key: Lasry, Niebel, Kopal and Wacker.
"""
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.withdrawal_recovery.verify import reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def check_pdf(path, inputs):
    import fitz
    assert sha(path) == inputs["source"]["pdf_sha256"]
    doc = fitz.open(path)
    for image in inputs["source_images"]:
        pix = doc[image["pdf_page_1based"] - 1].get_pixmap(
            matrix=fitz.Matrix(image["render_scale"], image["render_scale"]),
            clip=fitz.Rect(*image["crop_rectangle_pdf_points"]))
        saved = fitz.Pixmap(str(HERE / image["path"]))
        assert (pix.width, pix.height, pix.n, pix.samples) == (
            saved.width, saved.height, saved.n, saved.samples)


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    for image in inputs["source_images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
    assert sha(HERE / "prior_candidates.json") == inputs["prior_credit"]["prior_candidates_sha256"]
    key = inputs["key"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    records = []
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-")
        assert len(literal) == rec["source_slots"] == rec["advertised_length"]
        cipher = literal.replace("-", "?")
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, literal, rec["editorial_recipe"], ranks, square, raw)
        for change in edition["known_coordinate_substitutions"] + edition["erasure_fills"]:
            p = change["source_position_0based"]
            change["printed_group_1based"] = p // 5 + 1
            change["within_group_1based"] = p % 5 + 1
        raw["witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        records.append({"id": rec["id"], "source_literal": literal,
                        "raw": raw, "edition": edition})
    assert [r["raw"]["fixed_positions"] for r in records] == [98, 92]
    assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [100, 92]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [1, 5]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [2, 0]
    b2 = records[1]
    index = 49
    positions = b2["raw"]["source_position_pairs_0based"][index]
    assert positions == [172, 32]
    assert "".join(b2["source_literal"][p] for p in positions) == "XA"
    assert b2["raw"]["domains"][index] == "56"
    assert b2["edition"]["reading"]["domains"][index] == "56"
    assert all(b2["source_literal"][p] == b2["edition"]["ciphertext"][p] for p in positions)
    context = inputs["optional_existing_context"]
    assert sha(ROOT / context["path"]) == context["sha256"]
    prior = json.loads((ROOT / context["path"]).read_text())
    assert prior["contextual_cell_assignments"] == context["assignment_reused"]
    assert prior["published_partial_square"] == square
    conditional = reading(b2["edition"]["ciphertext"], ranks, prior["contextual_square"])
    assert conditional["plaintext"][48:57] == "753UND308"
    conditional["witness_not_original_reading"] = global_witness(
        b2["edition"]["ciphertext"], ranks, prior["contextual_square"], conditional)
    return {"schema": "adfgvx-newspaper-dispatch-certificate-v1",
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {"physical_source_parts": 2, "literal_source_slots": 386,
                        "plaintext_positions": 193, "raw_fixed_positions": 190,
                        "edition_fixed_positions": 192,
                        "known_coordinate_substitutions": 6, "printed_erasure_fills": 2,
                        "remaining_unknown_square_positions": 1,
                        "insertions": 0, "deletions": 0, "block_moves": 0,
                        "baseline_key_changes": 0},
            "records": records,
            "optional_existing_context": {"basis": context, "record_id": "p171_B2",
                                          "baseline_field": "7?3UND308",
                                          "conditional_field": "753UND308",
                                          "reading": conditional,
                                          "is_new_independent_numeral_evidence": False},
            "limits": [
                "The baseline field is 7?3, with a globally coupled56 key-cell domain; the source has no missing coordinate at that position.",
                "The optional753 is only propagation of the earlier separately conditional military-context assignments. This message supplies no independent proof of that digit.",
                "The printed text does not explicitly identify what the two routing references denote; no unsupported postal-office identification is added.",
                "This B telegram is distinct from Norbert's prior p171 A1 challenge reading.",
                "Exact re-encryption and witness completions establish consistency and costs, not unique historical wording.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    if args.pdf:
        check_pdf(args.pdf, inputs)
    result = run()
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
