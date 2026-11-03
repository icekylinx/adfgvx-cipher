#!/usr/bin/env python3
"""Verify A2/A3 companions to Norbert's prior p171 A1 ruble-rate reading.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The conditional A2 geometry is retained explicitly; no new A1 record is made.
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


def frame(literal, excluded=(), gap=None):
    skipped = {i for start, end in excluded for i in range(start, end)}
    chars, original, mapping = [], [], []
    for i, c in enumerate(literal):
        if i == gap:
            chars.append("?")
            original.append("?")
            mapping.append(None)
        if i in skipped:
            continue
        chars.append(c if c in "ADFGVX" else "?")
        original.append(c)
        mapping.append(i)
    return "".join(chars), "".join(original), mapping


def price(literal, ranks, square, template, excluded=(), gap=None):
    cipher, working_literal, mapping = frame(literal, excluded, gap)
    raw = reading(cipher, ranks, square)
    edition = repair(cipher, working_literal, {"text": template, "pair_overrides": []},
                     ranks, square, raw)
    for field in ["known_coordinate_substitutions", "erasure_fills"]:
        for change in edition[field]:
            working = change.pop("source_position_0based")
            original = mapping[working]
            change["working_coordinate_index"] = working
            change["source_coordinate_index"] = original
            change["source_kind"] = "added_unknown" if original is None else "received_slot"
    return {"analysis_frame": cipher, "working_to_source_indices": mapping,
            "raw": raw, "edition": edition}


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    for image in inputs["source_images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
    assert sha(HERE / "prior_candidates.json") == inputs["prior_credit"]["prior_candidates_sha256"]
    prior = next(r for r in json.loads((ROOT / "data/prior_readings.json").read_text())["messages"]
                 if r["id"] == "p171")
    assert prior["first_source"] == inputs["prior_credit"]["first_part_source"]
    key = inputs["key"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    geometry = inputs["a2_geometry"]
    records, screens = [], []
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert len(literal) == rec["actual_source_slots"]
        assert set(literal) <= set("ADFGVX-")
        if rec["id"] == "p171_A2":
            spans = geometry["literal_excluded_spans_0based"]
            assert [literal[a:b] for a, b in spans] == geometry["literal_excluded_groups"]
            a, b = geometry["short_group_source_span"]
            assert literal[a:b] == geometry["short_group"]
            assert geometry["candidate_gap_boundaries_0based"] == list(range(a, b + 1))
            for gap in geometry["candidate_gap_boundaries_0based"]:
                full = price(literal, ranks, square, rec["editorial_template"], spans, gap)
                masked = price(literal, ranks, square, geometry["masked_word_template"], spans, gap)
                screens.append({"gap_boundary_in_literal_source": gap,
                                "full_template_known_substitutions": len(full["edition"]["known_coordinate_substitutions"]),
                                "masked_template_known_substitutions": len(masked["edition"]["known_coordinate_substitutions"]),
                                "full_template_fills": len(full["edition"]["erasure_fills"]),
                                "raw_plaintext": full["raw"]["plaintext"],
                                "corrected_ciphertext": full["edition"]["ciphertext"]})
            result = price(literal, ranks, square, rec["editorial_template"], spans,
                           geometry["selected_representative_gap"])
            deleted = [{"source_coordinate_index": i, "literal": literal[i],
                        "known_coordinate": literal[i] in "ADFGVX"}
                       for a, b in spans for i in range(a, b)]
        else:
            result = price(literal, ranks, square, rec["editorial_template"])
            deleted = []
        assert len(result["analysis_frame"]) == rec["advertised_length"]
        assert result["raw"]["plaintext"] == rec["expected_raw_under_selected_model"]
        for view, cipher in [(result["raw"], result["analysis_frame"]),
                             (result["edition"]["reading"], result["edition"]["ciphertext"])]:
            view["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, view)
            pairs = view.pop("source_position_pairs_0based")
            view["working_coordinate_pairs_0based"] = pairs
            view["literal_source_pairs_0based"] = [
                [result["working_to_source_indices"][i] for i in pair] for pair in pairs]
        records.append({"id": rec["id"], "source_literal": literal,
                        "source_slots": len(literal), "printed_dash_slots": literal.count("-"),
                        "advertised_length": rec["advertised_length"],
                        "source_coordinate_exclusions": deleted, **result})
    minimum = min(s["full_template_known_substitutions"] for s in screens)
    ties = [s["gap_boundary_in_literal_source"] for s in screens
            if s["full_template_known_substitutions"] == minimum]
    masked_min = min(s["masked_template_known_substitutions"] for s in screens)
    masked_ties = [s["gap_boundary_in_literal_source"] for s in screens
                   if s["masked_template_known_substitutions"] == masked_min]
    assert ties == geometry["full_template_tied_minimum_gaps"] == [202, 203]
    assert masked_ties == [202, 203, 204]
    assert len({s["corrected_ciphertext"] for s in screens if s["gap_boundary_in_literal_source"] in ties}) == 1
    assert [r["raw"]["fixed_positions"] for r in records] == [122, 74]
    assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [126, 76]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [6, 0]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [4, 2]
    assert sum(d["known_coordinate"] for d in records[0]["source_coordinate_exclusions"]) == 6
    assert "PARIXPARI" in records[1]["edition"]["reading"]["plaintext"]
    return {"schema": "adfgvx-ruble-rate-companions-certificate-v1",
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {"new_physical_parts": 2, "new_first_part_records": 0,
                        "literal_source_slots": 413, "working_coordinates": 404,
                        "plaintext_positions": 202, "raw_fixed_positions": 196,
                        "edition_fixed_positions": 202,
                        "known_coordinate_substitutions": 6,
                        "source_coordinate_exclusions": 10,
                        "known_coordinates_among_exclusions": 6,
                        "printed_erasures_among_exclusions": 4,
                        "added_unknown_coordinates": 1,
                        "printed_erasure_fills": 5, "added_coordinate_fills": 1,
                        "key_changes": 0, "reordered_blocks": 0},
            "records": records,
            "conditional_five_gap_screen": {"declared_scope": geometry["screen_scope"],
                                            "full_template_minimum": minimum,
                                            "all_full_template_minimizers": ties,
                                            "masked_template_minimum": masked_min,
                                            "all_masked_template_minimizers": masked_ties,
                                            "full_minimizers_share_corrected_ciphertext": True,
                                            "all_candidates": screens},
            "limits": [
                "A2's literal261-slot source is not its252-coordinate working model. Two whole groups are excluded, including six observed coordinates, and one unknown is added in the short group.",
                "Only one excluded group is visibly struck through. Excluding---DD is an explicit model decision, not a source-certified deletion.",
                "The full-template minimum has two tied local gap placements; the place/quantity-masked stencil has three. No unique original gap or global geometry is proved.",
                "This is an after-reading finite consistency/price check, not an independent control or statistical confidence measure.",
                "Norbert's earlier A1 body priority remains unchanged; A1 is neither recounted nor relabelled as a new physical record.",
                "The letter-spelled monetary quantities report what this telegram says; they are not independent evidence of actual market prices.",
                "PARI is repeated in the source reading and not silently deduplicated. Bons are not identified with a particular financial instrument.",
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
    print(json.dumps({"verified": args.verify, **result["summary"],
                      "gap_screen": {k: v for k, v in result["conditional_five_gap_screen"].items()
                                     if k != "all_candidates"}}, indent=2))


if __name__ == "__main__":
    main()
