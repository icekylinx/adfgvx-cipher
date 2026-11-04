#!/usr/bin/env python3
"""Verify the conditional p188 armistice edition and two provisions fragments.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published partial key: Lasry, Niebel, Kopal and Wacker.
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
    ranks, square = key["column_rank_order"], key["square"]
    assert (ranks, square) == (published["column_rank_order"], published["square"])
    records, totals, native_totals = [], Counter(), Counter()
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-BEK?")
        assert len(literal) == rec["literal_source_slots"]
        excluded = rec["excluded_source_mark_indices"]
        assert len(excluded) == len(set(excluded))
        mapping = [i for i in range(len(literal)) if i not in excluded]
        working_literal = "".join(literal[i] for i in mapping)
        cipher = "".join(c if c in "ADFGVX" else "?" for c in working_literal)
        assert len(cipher) == rec["advertised_length"]
        if rec["id"] == "p188_A":
            assert excluded == [80] and literal[80] == "K"
            assert literal[75:81] == "DDFXXK"
            assert literal[165] == "B"
            assert literal[116:121] == "AV?XF"
            assert rec["damaged_glyph"]["source_index"] == 118
            assert rec["damaged_glyph"]["literal_placeholder"] == literal[118] == "?"
            assert rec["damaged_glyph"]["conditional_coordinate_interpretation"] == "X"
            assert rec["damaged_glyph"]["independent_coordinate_witness_established"] is False
            prior = json.loads((HERE / "prior_candidates.json").read_text())
            assert "GDGAGAV?XF" in prior["cross_key_candidates"][0]["ciphertext"]
            assert working_literal.count("-") == 5 and cipher.count("?") == 7
        else:
            assert not excluded
        if rec["id"] == "p188_C1":
            assert literal[140:145] == "EFXGF"
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, working_literal,
                         {"text": rec["editorial_template"], "pair_overrides": rec["pair_overrides"]},
                         ranks, square, raw)
        assert len(edition["ciphertext"]) == len(cipher)
        for field in ["known_coordinate_substitutions", "erasure_fills"]:
            for change in edition[field]:
                index = change.pop("source_position_0based")
                change["working_coordinate_index"] = index
                change["source_coordinate_index"] = mapping[index]
                assert change["observed"] == literal[mapping[index]]
                assert (cipher[index] == "?") == (field == "erasure_fills")
        remaining_working = edition.pop("remaining_erased_source_positions_0based")
        edition["remaining_masked_working_indices"] = remaining_working
        edition["remaining_masked_source_indices"] = [mapping[i] for i in remaining_working]
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        positions = []
        for i, pair in enumerate(raw["source_position_pairs_0based"]):
            positions.append({"plaintext_position": i,
                              "working_coordinate_indices": pair,
                              "source_coordinate_indices": [mapping[j] for j in pair],
                              "source_glyphs": "".join(literal[mapping[j]] for j in pair),
                              "raw_pair": "".join(cipher[j] for j in pair),
                              "edited_pair": "".join(edition["ciphertext"][j] for j in pair),
                              "raw_symbol": raw["plaintext"][i],
                              "raw_domain": raw["domains"][i],
                              "edited_symbol": edition["reading"]["plaintext"][i],
                              "edited_domain": edition["reading"]["domains"][i]})
        cost = {"physical_source_parts": 1, "literal_source_slots": len(literal),
                "working_coordinates": len(cipher), "working_source_masked_slots": cipher.count("?"),
                "printed_erasure_slots": working_literal.count("-"),
                "working_noncoordinate_source_masks": sum(c not in "ADFGVX-?" for c in working_literal),
                "damaged_glyph_source_masks": working_literal.count("?"),
                "plaintext_positions": raw["plaintext_positions"],
                "raw_fixed_positions": raw["fixed_positions"],
                "edition_fixed_positions": edition["reading"]["fixed_positions"],
                "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                "source_mask_fills": len(edition["erasure_fills"]),
                "remaining_source_masked_slots": edition["ciphertext"].count("?"),
                "visible_marks_excluded": len(excluded)}
        totals.update(cost)
        if not excluded:
            native_totals.update(cost)
        records.append({"id": rec["id"], "key_id": key["id"],
                        "source_literal": literal, "source_slots": len(literal),
                        "analysis_frame_literal": working_literal, "analysis_frame": cipher,
                        "frame_to_source_indices": mapping,
                        "excluded_source_marks": [rec["excluded_mark"]] if excluded else [],
                        "geometry_status": rec.get("geometry_status", "Native source frame; no source slots excluded or added."),
                        "counts": cost, "raw": raw, "edition": edition,
                        "positions": positions,
                        "remaining_positions": [p for p in positions if p["edited_symbol"] == "?"],
                        "all_raw_digit_J_Q_Y_occurrences": [p for p in positions
                            if p["raw_symbol"].isdigit() or p["raw_symbol"] in "JQY"]})
        if rec["id"] == "p188_A":
            assert positions[42]["working_coordinate_indices"] == [117, 89]
            assert positions[42]["source_coordinate_indices"] == [118, 90]
            assert positions[42]["raw_pair"] == "?V"
            assert positions[42]["raw_domain"] == "234789ACMQVXY"
            assert positions[42]["edited_pair"] == "DV"
            assert positions[42]["edited_symbol"] == "X"
            assert [c for c in edition["erasure_fills"] if c["source_coordinate_index"] == 118] == [{
                "plaintext_position_0based": 42, "observed": "?", "proposed": "D",
                "working_coordinate_index": 117, "source_coordinate_index": 118}]
            # Preserve the former X reading as an explicit assumption, not an
            # additional physical witness or an observed coordinate in the totals.
            assumed_literal = working_literal[:117] + "X" + working_literal[118:]
            assumed_cipher = cipher[:117] + "X" + cipher[118:]
            assumed_raw = reading(assumed_cipher, ranks, square)
            assumed_edition = repair(assumed_cipher, assumed_literal,
                {"text": rec["editorial_template"], "pair_overrides": rec["pair_overrides"]},
                ranks, square, assumed_raw)
            assert assumed_raw["plaintext"] == raw["plaintext"][:42] + "C" + raw["plaintext"][43:]
            assert assumed_raw["fixed_positions"] == 105
            assert len(assumed_edition["known_coordinate_substitutions"]) == 15
            assert len(assumed_edition["erasure_fills"]) == 6
            assert assumed_edition["ciphertext"] == edition["ciphertext"]
            records[-1]["damaged_glyph"] = rec["damaged_glyph"]
            records[-1]["conditional_X_sensitivity"] = {
                "status": "Assumption only; excluded from the source and repair totals.",
                "source_coordinate_index": 118, "working_coordinate_index": 117,
                "assumed_coordinate": "X", "plaintext_position": 42,
                "raw_pair": "XV", "raw_symbol": "C",
                "raw_plaintext": assumed_raw["plaintext"],
                "raw_fixed_positions": assumed_raw["fixed_positions"],
                "known_coordinate_substitutions": len(assumed_edition["known_coordinate_substitutions"]),
                "source_mask_fills": len(assumed_edition["erasure_fills"]),
                "edited_ciphertext_unchanged": True,
                "source118_edit": {"observed_if_assumed": "X", "proposed": "D"}}
    assert [r["source_slots"] for r in records] == [225, 176, 268]
    assert [r["raw"]["fixed_positions"] for r in records] == [104, 84, 130]
    assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [112, 88, 130]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [14, 10, 4]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [7, 0, 0]
    assert "AVK1P" in records[0]["raw"]["plaintext"]
    assert "AOK1P" in records[0]["edition"]["reading"]["plaintext"]
    assert records[0]["edition"]["reading"]["plaintext"].endswith("AXOXKX11XXX")
    assert "LAENGSTENSOCH" in records[1]["edition"]["reading"]["plaintext"]
    assert "FELDINTENTENDANT" in records[1]["edition"]["reading"]["plaintext"]
    assert records[2]["edition"]["remaining_masked_source_indices"] == [140]
    return {"schema": inputs["schema"].replace("input", "certificate"),
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "known_coordinate_exclusion_cost_lower_bound": 0,
                        "known_coordinate_exclusion_cost_upper_bound": 1,
                        "added_coordinates": 0, "reordered_blocks": 0,
                        "baseline_key_changes": 0, "new_numeral_assignments": 0},
            "native_frame_B2_C1_summary": dict(native_totals),
            "records": records,
            "index_convention": "All indices are zero-based. Helper raw/edition source_position_pairs_0based fields index the working frame. The positions ledger and frame_to_source_indices separately identify the original visible source slots.",
            "limits": inputs["limits"] + [
                "No global geometry or repair-optimum search was performed. If the extra mark is X, deletion within its identical-X run can share a resulting stream; the exclusion's precise historical identity is not proved.",
                "A's seven fills comprise five printed dashes, one B-shaped noncoordinate glyph and one damaged glyph at source118; these are distinct from the excluded extra K/X-like mark.",
                "Global witnesses and exact re-encryption demonstrate consistency, not unique wording, the original complete square, or authentic numerical labels.",
                "Unassigned square cells share a global bijection. Per-position domains do not authorize independently choosing each occurrence.",
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
