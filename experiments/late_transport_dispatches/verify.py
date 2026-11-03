#!/usr/bin/env python3
"""Verify six source parts on rail, motor and air transport, Childs p229.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published period key: Lasry, Niebel, Kopal and Wacker.
Default verification is standard-library-only. Optional PDF pixel checking
uses PyMuPDF and the pinned source PDF.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.withdrawal_recovery.verify import reading, repair, sha
from experiments.operational_recovery.verify import global_witness

CO = "ADFGVX"


def check_pdf(path):
    import fitz
    inputs = json.loads((HERE / "inputs.json").read_text())
    assert sha(path) == inputs["source"]["pdf_sha256"]
    doc = fitz.open(path)
    for image in inputs["source_images"]:
        page = doc[image["pdf_page_1based"] - 1]
        actual = page.get_pixmap(matrix=fitz.Matrix(image["render_scale"], image["render_scale"]),
                                 clip=fitz.Rect(*image["crop_rectangle_pdf_points"]))
        saved = fitz.Pixmap(str(HERE / image["path"]))
        assert (actual.width, actual.height, actual.n, actual.samples) == (
            saved.width, saved.height, saved.n, saved.samples), image["path"]


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    for image in inputs["source_images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
    prior = inputs["prior_credit"]
    assert sha(HERE / prior["prior_candidate_path"]) == prior["prior_candidate_sha256"]
    key = inputs["key"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    assert len(square) == len(set(square)) == 36
    records = []
    totals = Counter()
    for rec in inputs["records"]:
        groups = " ".join(rec["source_rows"]).split()
        assert all(len(g) == 5 for g in groups[:-1])
        literal = "".join(groups)
        assert set(literal) <= set(CO + "-Q")
        assert len(literal) == rec["source_slots"] == rec["advertised_length"]
        cipher = "".join(c if c in CO else "?" for c in literal)
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, literal, rec["editorial_recipe"], ranks, square, raw)
        for change in edition["known_coordinate_substitutions"] + edition["erasure_fills"]:
            index = change["source_position_0based"]
            change["printed_group_1based"] = index // 5 + 1
            change["within_group_1based"] = index % 5 + 1
        for field in rec["protected_fields"]:
            a, b = field["plaintext_start"], field["plaintext_end_exclusive"]
            assert raw["plaintext"][a:b] == field["raw_text"]
            assert edition["reading"]["plaintext"][a:b] == field["raw_text"]
            for index in range(a, b):
                assert all(cipher[p] == edition["ciphertext"][p]
                           for p in raw["source_position_pairs_0based"][index])
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        labels = []
        for i, label in enumerate(raw["plaintext"]):
            if label.isdigit() or label in "JQY":
                positions = raw["source_position_pairs_0based"][i]
                labels.append({"plaintext_position_0based": i, "raw_label": label,
                               "edition_label": edition["reading"]["plaintext"][i],
                               "source_pair": "".join(cipher[p] for p in positions),
                               "source_positions_0based": positions,
                               "source_pair_changed": any(cipher[p] != edition["ciphertext"][p]
                                                          for p in positions)})
        item = {"id": rec["id"], "source_literal": literal,
                "source_literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
                "counted_source_slots": len(literal), "advertised_length": rec["advertised_length"],
                "printed_dash_slots": literal.count("-"),
                "invalid_source_glyphs": [{"source_position_0based": i, "literal": c}
                                          for i, c in enumerate(literal) if c not in CO + "-"],
                "raw": raw, "edition": edition,
                "protected_fields": rec["protected_fields"],
                "all_raw_numeral_and_J_Q_Y_occurrences": labels,
                "remaining_uncertain_plaintext_positions": [
                    {"plaintext_position_0based": i, "domain": d,
                     "source_positions_0based": raw["source_position_pairs_0based"][i]}
                    for i, d in enumerate(edition["reading"]["domains"]) if len(d) > 1]}
        records.append(item)
        totals.update({"physical_source_parts": 1, "counted_source_slots": len(literal),
                       "known_received_coordinates": sum(c in CO for c in literal),
                       "printed_dash_slots": literal.count("-"),
                       "invalid_source_glyphs": len(item["invalid_source_glyphs"]),
                       "plaintext_positions": raw["plaintext_positions"],
                       "raw_fixed_label_positions": raw["fixed_positions"],
                       "edition_fixed_label_positions": edition["reading"]["fixed_positions"],
                       "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                       "erasure_fills": len(edition["erasure_fills"]),
                       "remaining_uncertain_plaintext_positions": len(item["remaining_uncertain_plaintext_positions"])})
    assert [r["counted_source_slots"] for r in records] == [228, 192, 176, 268, 248, 330]
    assert [r["raw"]["fixed_positions"] for r in records] == [114, 95, 88, 131, 118, 131]
    assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [114, 96, 88, 133, 123, 162]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [1, 1, 2, 1, 6, 3]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [0, 1, 0, 2, 5, 31]
    assert "TELRAMM" in records[4]["edition"]["reading"]["plaintext"]
    assert "WIEVIELKONNEN" in records[4]["edition"]["reading"]["plaintext"]
    assert records[5]["invalid_source_glyphs"] == [{"source_position_0based": 154, "literal": "Q"}]
    assert [p["plaintext_position_0based"] for p in records[5]["remaining_uncertain_plaintext_positions"]] == [81, 93, 157]
    return {"schema": "adfgvx-late-transport-dispatches-certificate-v1",
            "prepared_by": inputs["prepared_by"], "prior_credit": prior,
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "physical_telegrams": 3,
                        "insertions": 0, "deletions": 0, "block_moves": 0,
                        "published_key_changes": 0, "numeral_assignments": 0},
            "records": records,
            "limits": [
                "Fixed labels are baseline-key values, not authenticated historical digits or rare-letter meanings.",
                "The p229 A/B bodies were already visible in earlier unreviewed OCR-derived candidates; this package adds source review and priced editions, not universal first-decipherment claims.",
                "p229 C is a conditional source-priced restoration. Its destination remains HK?, its unit24 remains a raw label, and its boundary after WIRD and final reference remain incomplete.",
                "The p229 B1 quantity0 is not read as40: only the preceding corrupted OHL office abbreviation is repaired.",
                "B2 retains AKKS, TELRAMM and the six-character KONNEN; no characters are inserted to normalize those strings.",
                "The source330-slot p229 C is not the old323-slot OCR stream. Recovering seven previously omitted printed slots corrects transcription, not the source geometry.",
                "Globally consistent witness completions and exact re-encryption establish arithmetic consistency and repair prices, not uniquely original wording.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path,
                        help="Check pinned PDF digest and independently regenerate all crop pixels")
    args = parser.parse_args()
    if args.pdf:
        check_pdf(args.pdf)
    result = run()
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "source_pixels_checked": bool(args.pdf),
                      **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
