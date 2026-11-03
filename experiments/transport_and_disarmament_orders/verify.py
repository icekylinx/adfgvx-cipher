#!/usr/bin/env python3
"""Verify five native p209 source frames and their explicit lexical proposals.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published Nov19-21 key: Lasry, Niebel, Kopal and Wacker.
"""
from pathlib import Path
import argparse
from collections import Counter
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
    for spec in inputs["source_images"]:
        pix = doc[spec["pdf_page_1based"] - 1].get_pixmap(
            matrix=fitz.Matrix(spec["render_scale"], spec["render_scale"]),
            clip=fitz.Rect(*spec["crop_rectangle_pdf_points"]))
        saved = fitz.Pixmap(str(HERE / spec["path"]))
        assert (pix.width, pix.height, pix.n, pix.samples) == (
            saved.width, saved.height, saved.n, saved.samples)


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    for spec in inputs["source_images"]:
        assert sha(HERE / spec["path"]) == spec["sha256"]
    assert sha(HERE / "prior_candidates.json") == inputs["prior_credit"]["prior_candidates_sha256"]
    key = inputs["key"]
    ranks, square = key["column_rank_order"], key["square"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    assert (ranks, square) == (published["column_rank_order"], published["square"])
    records, totals = [], Counter()
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-")
        assert len(literal) == rec["literal_source_slots"] == rec["advertised_length"]
        cipher = literal.replace("-", "?")
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, literal,
                         {"text": rec["editorial_template"], "pair_overrides": rec["pair_overrides"]},
                         ranks, square, raw)
        assert len(edition["ciphertext"]) == len(cipher)
        for fill in edition["erasure_fills"]:
            assert literal[fill["source_position_0based"]] == "-"
        for change in edition["known_coordinate_substitutions"]:
            assert literal[change["source_position_0based"]] in "ADFGVX"
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        positions = []
        for i, pair in enumerate(raw["source_position_pairs_0based"]):
            positions.append({"plaintext_position": i, "source_coordinate_indices": pair,
                              "source_glyphs": "".join(literal[j] for j in pair),
                              "raw_pair": "".join(cipher[j] for j in pair),
                              "edited_pair": "".join(edition["ciphertext"][j] for j in pair),
                              "raw_symbol": raw["plaintext"][i], "raw_domain": raw["domains"][i],
                              "edited_symbol": edition["reading"]["plaintext"][i],
                              "edited_domain": edition["reading"]["domains"][i]})
        cost = {"physical_source_parts": 1, "literal_source_slots": len(literal),
                "working_coordinates": len(cipher), "source_erasure_slots": cipher.count("?"),
                "plaintext_positions": raw["plaintext_positions"],
                "raw_fixed_positions": raw["fixed_positions"],
                "edition_fixed_positions": edition["reading"]["fixed_positions"],
                "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                "source_erasure_fills": len(edition["erasure_fills"]),
                "remaining_source_erasure_slots": edition["ciphertext"].count("?")}
        totals.update(cost)
        records.append({"id": rec["id"], "key_id": key["id"], "source_literal": literal,
                        "source_slots": len(literal), "analysis_frame": cipher,
                        "frame_to_source_indices": list(range(len(cipher))),
                        "raw": raw, "edition": edition, "counts": cost,
                        "positions": positions,
                        "all_raw_digit_J_Q_Y_occurrences": [p for p in positions
                            if p["raw_symbol"].isdigit() or p["raw_symbol"] in "JQY"]})
    assert [r["id"] for r in records] == ["p209_A1", "p209_B1", "p209_B2", "p209_C1", "p209_C2"]
    assert [r["source_slots"] for r in records] == [224, 310, 230, 242, 182]
    assert [r["raw"]["fixed_positions"] for r in records] == [104, 155, 115, 121, 91]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [0, 4, 3, 4, 4]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [8, 0, 0, 0, 0]
    assert "TS8HESCHICHE" in records[0]["edition"]["reading"]["plaintext"]
    assert records[0]["source_literal"][97:105] == "--------"
    assert "ABMMD" in records[1]["edition"]["reading"]["plaintext"]
    assert records[1]["edition"]["reading"]["plaintext"].endswith("LEBENSMITTELM")
    assert records[2]["edition"]["reading"]["plaintext"].endswith("NOXJ0192SMXBEWEGEXBERLIN")
    assert records[3]["source_literal"][35:40] == "GFXAF"
    assert "HABENGROSSEANZAHL" in records[3]["edition"]["reading"]["plaintext"]
    assert records[4]["edition"]["reading"]["plaintext"].endswith("OHLXRMJAJJ970GEHXOP")
    return {"schema": inputs["schema"].replace("input", "certificate"),
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "added_coordinates": 0, "deleted_coordinates": 0,
                        "excluded_source_slots": 0, "reordered_blocks": 0,
                        "baseline_key_changes": 0, "new_numeral_assignments": 0},
            "records": records, "index_convention": "All indices are zero-based; every working frame equals the native source frame.",
            "limits": inputs["limits"] + [
                "The source-directed lexical proposals and exact re-encryption establish their price and consistency, not unique historical wording.",
                "Fixed output positions count the unchanged published square labels, not independently authenticated numerals or the absence of transmission errors.",
                "Global completion witnesses are consistency examples, not additional recovered plaintext or source observations.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.pdf:
        check_pdf(args.pdf, json.loads((HERE / "inputs.json").read_text()))
    result = run()
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
