#!/usr/bin/env python3
"""Verify Childs p179 radio, surrender, armistice and leave instructions.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published period keys: Lasry, Niebel, Kopal and Wacker.
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
    published = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    for key_id, key in inputs["keys"].items():
        assert key["square"] == published[key_id]["square"]
        assert key["column_rank_order"] == published[key_id]["column_rank_order"]
    records, totals = [], Counter()
    for rec in inputs["records"]:
        key = inputs["keys"][rec["key_id"]]
        ranks, square = key["column_rank_order"], key["square"]
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX")
        assert len(literal) == rec["literal_source_slots"]
        excluded = {i for a, b in rec["source_excluded_spans"] for i in range(a, b)}
        mapping = [i for i in range(len(literal)) if i not in excluded]
        cipher = "".join(literal[i] for i in mapping)
        if rec["id"] == "p179_A":
            assert literal[75:80] == literal[80:85] == "ADADG"
            assert excluded == set(range(80, 85))
            assert literal[190] == "X"
        else:
            assert not excluded
        assert len(cipher) == rec["advertised_length"]
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, cipher, {"text": rec["editorial_template"], "pair_overrides": []},
                         ranks, square, raw)
        assert not edition["erasure_fills"]
        for change in edition["known_coordinate_substitutions"]:
            index = change.pop("source_position_0based")
            change["working_coordinate_index"] = index
            change["source_coordinate_index"] = mapping[index]
        if rec["id"] == "p179_A":
            assert edition["reading"]["plaintext"].endswith("4B4??3?")
            assert "UXSX" in edition["reading"]["plaintext"]
        if rec["id"] in ("p179_D1", "p179_D2"):
            assert edition["ciphertext"] == cipher
        if rec["id"] == "p179_D1":
            assert "1560U61" in raw["plaintext"]
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        labels = []
        for i, label in enumerate(raw["plaintext"]):
            if label.isdigit() or label in "JQY":
                pair = raw["source_position_pairs_0based"][i]
                labels.append({"plaintext_position": i, "raw_label": label,
                               "edition_label": edition["reading"]["plaintext"][i],
                               "coordinate_pair": "".join(cipher[j] for j in pair),
                               "working_coordinate_indices": pair,
                               "source_coordinate_indices": [mapping[j] for j in pair],
                               "source_pair_changed": any(cipher[j] != edition["ciphertext"][j] for j in pair)})
        records.append({"id": rec["id"], "key_id": rec["key_id"],
                        "source_literal": literal, "source_slots": len(literal),
                        "source_coordinate_exclusions": [{"source_index": i, "observed": literal[i],
                                                          "basis": "printed cancellation of duplicate ADADG"}
                                                         for i in sorted(excluded)],
                        "analysis_frame": cipher, "frame_to_source_indices": mapping,
                        "raw": raw, "edition": edition,
                        "all_raw_digit_J_Q_Y_occurrences": labels})
        totals.update({"physical_source_parts": 1, "literal_source_slots": len(literal),
                       "working_coordinates": len(cipher),
                       "plaintext_positions": raw["plaintext_positions"],
                       "raw_fixed_positions": raw["fixed_positions"],
                       "edition_fixed_positions": edition["reading"]["fixed_positions"],
                       "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                       "observed_coordinates_excluded_at_printed_cancellation": len(excluded)})
    assert [r["source_slots"] for r in records] == [271, 158, 232, 190, 212]
    assert [r["raw"]["fixed_positions"] for r in records] == [128, 76, 116, 91, 100]
    assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [130, 76, 116, 91, 100]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [7, 1, 3, 0, 0]
    return {"schema": "adfgvx-november-armistice-orders-certificate-v1",
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "source_erasure_slots": 0,
                        "source_erasure_fills": 0, "added_coordinates": 0,
                        "reordered_blocks": 0, "baseline_key_changes": 0,
                        "new_numeral_assignments": 0},
            "records": records,
            "limits": [
                "A is not a zero-edit source: five observed coordinates at its printed duplicate cancellation are excluded, in addition to seven ordinary-word coordinate substitutions.",
                "U.S. remains an unexpanded source label. No American origin or equipment type is inferred.",
                "D1's raw1560U61 year-like field is retained without normalization. The D records' November12 source date and Nov13-15b key label both remain explicit.",
                "All remaining question marks arise from unassigned partial-key cells, not missing received coordinates. Those cells share one global bijection.",
                "B does not name the city of its citadel. C preserves its BEDING abbreviation, and damaged reference fields are not completed.",
                "The prior unreviewed B/C/D2 bodies are credited. New source readings of A/D1 do not establish universal decipherment priority.",
                "Global witnesses and re-encryption establish compatibility and exact repair costs, not unique historical wording or true numerical fields.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.pdf:
        check_pdf(args.pdf, json.loads((HERE / "inputs.json").read_text()))
    result = run()
    target = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
