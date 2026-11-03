#!/usr/bin/env python3
"""Verify the source transcription, bounded lexical repairs and remaining domains.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published keys: Lasry, Niebel, Kopal and Wacker.
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
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    assert key["square"] == published["square"]
    assert key["column_rank_order"] == published["column_rank_order"]
    ranks, square = key["column_rank_order"], key["square"]
    records, totals = [], Counter()
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-")
        cipher = literal.replace("-", "?")
        assert len(cipher) == rec["literal_source_slots"]
        if rec["advertised_length"] is not None:
            assert len(cipher) == rec["advertised_length"]
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, literal, {"text": rec["editorial_template"], "pair_overrides": []},
                         ranks, square, raw)
        assert len(edition["ciphertext"]) == len(cipher)
        for fill in edition["erasure_fills"]:
            assert cipher[fill["source_position_0based"]] == "?"
        for change in edition["known_coordinate_substitutions"]:
            assert cipher[change["source_position_0based"]] in "ADFGVX"
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        remaining = []
        for i, symbol in enumerate(edition["reading"]["plaintext"]):
            if symbol == "?":
                indices = edition["reading"]["source_position_pairs_0based"][i]
                remaining.append({"plaintext_position": i,
                                  "domain": edition["reading"]["domains"][i],
                                  "source_coordinate_indices": indices,
                                  "source_pair": "".join(cipher[j] for j in indices),
                                  "edited_pair": "".join(edition["ciphertext"][j] for j in indices)})
        labels = []
        for i, symbol in enumerate(raw["plaintext"]):
            if symbol.isdigit() or symbol in "JQY":
                indices = raw["source_position_pairs_0based"][i]
                labels.append({"plaintext_position": i, "raw_label": symbol,
                               "edition_label": edition["reading"]["plaintext"][i],
                               "coordinate_pair": "".join(cipher[j] for j in indices),
                               "source_coordinate_indices": indices,
                               "source_pair_changed": any(cipher[j] != edition["ciphertext"][j]
                                                          for j in indices)})
        records.append({"id": rec["id"], "source_literal": literal,
                        "source_slots": len(cipher), "analysis_frame": cipher,
                        "frame_to_source_indices": list(range(len(cipher))),
                        "raw": raw, "edition": edition, "remaining_positions": remaining,
                        "all_raw_digit_J_Q_Y_occurrences": labels})
        totals.update({"physical_source_parts": 1, "literal_source_slots": len(cipher),
                       "working_coordinates": len(cipher), "source_erasure_slots": cipher.count("?"),
                       "plaintext_positions": raw["plaintext_positions"],
                       "raw_fixed_positions": raw["fixed_positions"],
                       "edition_fixed_positions": edition["reading"]["fixed_positions"],
                       "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                       "source_erasure_fills": len(edition["erasure_fills"]),
                       "remaining_source_erasure_slots": edition["ciphertext"].count("?")})
    if records[0]["id"] == "p150_B1":
        assert [r["source_slots"] for r in records] == [194, 198, 204, 202, 214]
        assert [r["raw"]["fixed_positions"] for r in records] == [93, 92, 89, 92, 100]
        assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [97, 99, 101, 101, 107]
        assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [0, 3, 4, 0, 2]
        assert [len(r["edition"]["erasure_fills"]) for r in records] == [4, 7, 12, 9, 7]
        assert records[2]["remaining_positions"] == [{
            "plaintext_position": 28, "domain": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "source_coordinate_indices": [123, 183], "source_pair": "??", "edited_pair": "??"}]
        assert "WALACHEIEBENE" in records[2]["edition"]["reading"]["plaintext"]
        assert records[3]["edition"]["reading"]["plaintext"].endswith("KONSTANTAUX")
        assert inputs["records"][3]["advertised_length"] is None
    else:
        assert [r["id"] for r in records] == ["p157_B1", "p157_B2"]
        assert [r["source_slots"] for r in records] == [170, 272]
        assert [r["raw"]["fixed_positions"] for r in records] == [81, 121]
        assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [85, 135]
        assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [1, 5]
        assert [len(r["edition"]["erasure_fills"]) for r in records] == [4, 14]
        assert records[1]["remaining_positions"] == [{
            "plaintext_position": 135, "domain": "DEQTUX",
            "source_coordinate_indices": [40, 245], "source_pair": "?V", "edited_pair": "?V"}]
    return {"schema": inputs["schema"].replace("input", "certificate"),
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "added_coordinates": 0, "deleted_coordinates": 0,
                        "reordered_blocks": 0, "baseline_key_changes": 0,
                        "new_numeral_assignments": 0},
            "records": records, "limits": inputs["limits"] + [
                "Source-compatible lexical proposals and re-encryption do not prove unique historical wording.",
                "Any global completion witness is only a consistency example, not a recovered original key or erased ciphertext.",
                "All reference digits retain the published baseline labels; no new digit permutation is inferred.",
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
