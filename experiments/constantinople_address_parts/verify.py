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
    published = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    for key_id, key in inputs["keys"].items():
        assert key["square"] == published[key_id]["square"]
        assert key["column_rank_order"] == published[key_id]["column_rank_order"]
    records, totals = [], Counter()
    for rec in inputs["records"]:
        key = inputs["keys"][rec["key_id"]]
        ranks, square = key["column_rank_order"], key["square"]
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-L")
        cipher = literal.replace("-", "?").replace("L", "?")
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
                       "working_coordinates": len(cipher), "source_masked_slots": cipher.count("?"),
                       "printed_erasure_slots": literal.count("-"),
                       "noncoordinate_source_masks": literal.count("L"),
                       "plaintext_positions": raw["plaintext_positions"],
                       "raw_fixed_positions": raw["fixed_positions"],
                       "edition_fixed_positions": edition["reading"]["fixed_positions"],
                       "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                       "source_erasure_fills": len(edition["erasure_fills"]),
                       "remaining_source_erasure_slots": edition["ciphertext"].count("?")})
    by_id = {r["id"]: r for r in records}
    corroboration = []
    if "p161_C1" in by_id:
        assert [r["source_slots"] for r in records] == [204, 154, 254, 190]
        assert [r["raw"]["fixed_positions"] for r in records] == [95, 77, 127, 95]
        assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [99, 77, 127, 95]
        assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [4, 0, 2, 0]
        assert [len(r["edition"]["erasure_fills"]) for r in records] == [4, 0, 0, 0]
        assert [(x["plaintext_position"], x["domain"]) for x in records[0]["remaining_positions"]] == [(19, "1GIKNY"), (58, "56"), (59, "56")]
        assert [x["source_pair"] for x in records[0]["remaining_positions"]] == ["?G", "XA", "VF"]
        assert records[3]["source_literal"] == records[3]["edition"]["ciphertext"]
        for r in records:
            assert "MISZION" in r["raw"]["plaintext"] or r["id"] == "p161_D2"
        prior_path = HERE / "prior_osthoff_witness.json"
        assert sha(prior_path) == inputs["prior_osthoff_witness_sha256"]
        old = json.loads(prior_path.read_text())
        for field in ["source_inputs", "source_results"]:
            assert sha(ROOT / old[field + "_path"]) == old[field + "_sha256"]
        old_key = published[old["old_key_id"]]
        old_cipher = old["selected_old_record"]["analysis_ciphertext"]
        old_raw = reading(old_cipher, old_key["column_rank_order"], old_key["square"])
        assert old_raw["plaintext"] == old["selected_old_record"]["raw_plaintext"]
        assert [i for i, c in enumerate(old["prior_likely_plaintext"])
                if c != old_raw["plaintext"][i]] == old["three_preexisting_editorial_positions"]
        witness = by_id[old["new_literal_witness"]]
        for old_pos, new_pos in zip(old["three_preexisting_editorial_positions"], old["new_positions"]):
            letter = old["prior_likely_plaintext"][old_pos]
            assert witness["raw"]["plaintext"][new_pos] == letter
            pair_indices = witness["raw"]["source_position_pairs_0based"][new_pos]
            pair = "".join(witness["source_literal"][i] for i in pair_indices)
            assert "?" not in pair and "-" not in pair
            assert witness["raw"]["domains"][new_pos] == letter
            corroboration.append({"old_record": "p149_A2", "old_plaintext_position": old_pos,
                                  "old_raw_label": old_raw["plaintext"][old_pos],
                                  "preexisting_editorial_letter": letter,
                                  "old_source_coordinate_indices": old_raw["source_position_pairs_0based"][old_pos],
                                  "new_record": old["new_literal_witness"],
                                  "new_plaintext_position": new_pos,
                                  "new_source_coordinate_indices": pair_indices,
                                  "new_observed_pair": pair,
                                  "new_raw_letter": witness["raw"]["plaintext"][new_pos],
                                  "new_source_edit_cost": 0,
                                  "scope": "Direct observed letter in a later differently keyed and abbreviated message; no common-ciphertext claim."})
        assert [r["new_raw_letter"] for r in corroboration] == list("DAT")
    else:
        assert [r["id"] for r in records] == ["p147_C1", "p148_B1", "p156_C1"]
        assert [r["source_slots"] for r in records] == [96, 328, 102]
        assert [r["raw"]["fixed_positions"] for r in records] == [48, 163, 51]
        assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [0, 2, 0]
        assert totals["source_erasure_fills"] == 0
        assert records[1]["source_literal"][49] == "L"
        assert records[1]["source_literal"][37] == "F"
        assert records[1]["edition"]["ciphertext"][37] == "X"
        assert records[1]["remaining_positions"] == [{"plaintext_position": 95, "domain": "9EKVXZ",
                                                     "source_coordinate_indices": [262, 49],
                                                     "source_pair": "F?", "edited_pair": "F?"}]
        assert "BUSSCHS" in records[2]["raw"]["plaintext"]
    return {"schema": inputs["schema"].replace("input", "certificate"),
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "added_coordinates": 0, "deleted_coordinates": 0,
                        "reordered_blocks": 0, "baseline_key_changes": 0,
                        "new_numeral_assignments": 0},
            "records": records, "cross_period_osthoff_corroboration": corroboration,
            "limits": inputs["limits"] + [
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
