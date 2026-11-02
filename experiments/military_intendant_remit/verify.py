#!/usr/bin/env python3
"""Certify p202 B's four source parts and the conditional five-loss opening.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The published Nov16-18 key remains unchanged. All gap alternatives and
editorial prices are retained; no unique historical loss position is claimed.
"""
from pathlib import Path
from array import array
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.withdrawal_recovery.verify import CO, reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def frame(record):
    literal = "".join("".join(record["source_rows"]).split())
    assert set(literal) <= set(CO + "?QR")
    source = "".join(c if c in CO else "?" for c in literal)
    mapping = list(range(len(source)))
    working_literal = literal
    model = record["frame_model"]
    if model["kind"] == "one_contiguous_gap":
        position = model["insertion_before_source_position_0based"]
        count = model["inserted_unknown_coordinates"]
        assert count == 5 and position == 145
        source = source[:position] + "?" * count + source[position:]
        working_literal = literal[:position] + "?" * count + literal[position:]
        mapping[position:position] = [None] * count
    else:
        assert model["kind"] == "identity"
    assert len(literal) == record["source_slot_count"]
    assert len(source) == record["advertised_length"]
    return literal, source, working_literal, mapping


def map_changes(edition, mapping):
    output = {"known_coordinate_substitutions": [], "masked_source_fills": [],
              "inserted_coordinate_fills": []}
    for kind in ["known_coordinate_substitutions", "erasure_fills"]:
        for edit in edition[kind]:
            framed = edit["source_position_0based"]
            original = mapping[framed]
            entry = {"frame_position_0based": framed,
                     "original_source_position_0based": original,
                     "plaintext_position_0based": edit["plaintext_position_0based"],
                     "observed": edit["observed"], "proposed": edit["proposed"]}
            if original is not None:
                entry["printed_group_1based"] = original // 5 + 1
                entry["within_group_1based"] = original % 5 + 1
            target = kind if kind == "known_coordinate_substitutions" else (
                "inserted_coordinate_fills" if original is None else "masked_source_fills")
            output[target].append(entry)
    return output


def gap_audit(inputs):
    rec = inputs["records"][0]
    literal = "".join("".join(rec["source_rows"]).split())
    assert len(literal) == 223 and set(literal) <= set(CO)
    key, definition = inputs["key"], inputs["gap_audit"]
    ranks, square = key["column_rank_order"], key["square"]
    rows = []
    for position in range(len(literal) + 1):
        source = literal[:position] + "?" * 5 + literal[position:]
        raw = reading(source, ranks, square)
        results = {}
        for name, template in [("ordinary_words", definition["ordinary_word_template"]),
                               ("unmasked_body", definition["unmasked_body_template"])]:
            proposed = repair(source, source, {"text": template, "pair_overrides": []},
                              ranks, square, raw)
            results[name] = {
                "known_coordinate_substitutions": len(proposed["known_coordinate_substitutions"]),
                "inserted_coordinate_fills": len(proposed["erasure_fills"]),
            }
        rows.append({"gap_before_source_position_0based": position,
                     "at_printed_group_boundary_or_end": position % 5 == 0 or position == len(literal),
                     "raw_plaintext": raw["plaintext"], "raw_fixed_positions": raw["fixed_positions"],
                     "editorial_prices": results})
    minima = {}
    for scope, candidates in [("all_positions", rows),
                              ("printed_group_boundaries_or_end",
                               [row for row in rows if row["at_printed_group_boundary_or_end"]])]:
        minima[scope] = {}
        for template in ["ordinary_words", "unmasked_body"]:
            best = min(row["editorial_prices"][template]["known_coordinate_substitutions"]
                       for row in candidates)
            minima[scope][template] = {
                "minimum_known_coordinate_substitutions": best,
                "all_tied_gap_positions_0based": [
                    row["gap_before_source_position_0based"] for row in candidates
                    if row["editorial_prices"][template]["known_coordinate_substitutions"] == best],
            }
    assert minima["all_positions"]["ordinary_words"]["all_tied_gap_positions_0based"] == [142, 143]
    assert minima["all_positions"]["unmasked_body"]["all_tied_gap_positions_0based"] == [143, 144]
    assert minima["printed_group_boundaries_or_end"]["unmasked_body"]["all_tied_gap_positions_0based"] == [145]
    return {
        "schema": "adfgvx-p202-B1-five-gap-audit-v1",
        "prepared_by": inputs["prepared_by"], "candidate_positions": len(rows),
        "candidate_group_boundaries_or_end": sum(row["at_printed_group_boundary_or_end"] for row in rows),
        "ordinary_word_template": definition["ordinary_word_template"],
        "unmasked_body_template": definition["unmasked_body_template"],
        "templates_are_independent_cribs": False,
        "conditional_minima": minima, "records": rows,
        "scope": definition["selection_scope"],
    }


def verify_candidate_scores(inputs, gaps, book_model=None, radio_model=None):
    path = HERE / "candidate_scores.json"
    assert sha(path) == inputs["gap_audit"]["candidate_scores_sha256"]
    saved = json.loads(path.read_text())["records"]
    assert len(saved) == len(gaps["records"]) == 224
    for old, new in zip(saved, gaps["records"]):
        assert old["insertion_before_source_position_0based"] == new["gap_before_source_position_0based"]
        assert old["raw_plaintext"] == new["raw_plaintext"]
        assert old["raw_fixed_positions"] == new["raw_fixed_positions"]
    settings = inputs["gap_audit"]["candidate_finding_scores"]
    for name, model_path in [("book", book_model), ("radio", radio_model)]:
        assert max(saved, key=lambda row: row["scores"][name])["insertion_before_source_position_0based"] == 146
        if model_path is None:
            continue
        assert sha(model_path) == settings[name + "_model_sha256"]
        model = array("f")
        model.frombytes(model_path.read_bytes())
        if sys.byteorder != "little":
            model.byteswap()
        assert len(model) == 37 ** 4
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"
        for row in saved:
            symbols = [alphabet.index(c) for c in row["raw_plaintext"]]
            value = sum(model[((a * 37 + b) * 37 + c) * 37 + d]
                        for a, b, c, d in zip(symbols, symbols[1:], symbols[2:], symbols[3:])) / (len(symbols) - 3)
            assert abs(value - row["scores"][name]) < 1e-12


def run(inputs):
    for image in inputs["source_images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
    key = inputs["key"]
    current = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                   if k["id"] == key["id"])
    assert current["square"] == key["square"] and current["column_rank_order"] == key["column_rank_order"]
    ranks, square = key["column_rank_order"], key["square"]
    records = []
    for rec in inputs["records"]:
        literal, source, working_literal, mapping = frame(rec)
        raw = reading(source, ranks, square)
        edition = repair(source, working_literal, rec["editorial_recipe"], ranks, square, raw)
        changes = map_changes(edition, mapping)
        assert edition["reading"]["plaintext"] == rec["editorial_recipe"]["text"]
        raw["global_witness_not_an_original_reading"] = global_witness(source, ranks, square, raw)
        edition["reading"]["global_witness_not_an_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        unresolved = []
        for i, domain in enumerate(edition["reading"]["domains"]):
            if len(domain) > 1:
                positions = edition["reading"]["source_position_pairs_0based"][i]
                unresolved.append({"plaintext_position_0based": i, "domain": domain,
                                   "frame_coordinate_positions_0based": positions,
                                   "original_source_positions_0based": [mapping[j] for j in positions]})
        records.append({
            "id": rec["id"], "literal_source": literal,
            "literal_source_sha256": hashlib.sha256(literal.encode()).hexdigest(),
            "received_slots": len(literal), "known_received_coordinates": sum(c in CO for c in literal),
            "masked_received_slots": [{"source_position_0based": i, "literal": c}
                                      for i, c in enumerate(literal) if c not in CO],
            "frame_model": rec["frame_model"], "analysis_frame": source,
            "frame_to_original_source_index": mapping,
            "raw_within_working_frame": raw,
            "edition_ciphertext": edition["ciphertext"], "edition": edition["reading"],
            "changes": changes, "unresolved_edition_positions": unresolved,
            "remaining_unknown_coordinates": [i for i, c in enumerate(edition["ciphertext"]) if c == "?"],
        })
    summary = {
        "physical_source_parts": len(records),
        "received_slots": sum(r["received_slots"] for r in records),
        "known_received_coordinates": sum(r["known_received_coordinates"] for r in records),
        "masked_received_slots": sum(len(r["masked_received_slots"]) for r in records),
        "working_frame_coordinates": sum(len(r["analysis_frame"]) for r in records),
        "plaintext_positions_in_working_frames": sum(r["edition"]["plaintext_positions"] for r in records),
        "raw_fixed_positions_in_working_frames": sum(r["raw_within_working_frame"]["fixed_positions"] for r in records),
        "edition_fixed_positions_in_working_frames": sum(r["edition"]["fixed_positions"] for r in records),
        "known_coordinate_substitutions": sum(len(r["changes"]["known_coordinate_substitutions"]) for r in records),
        "masked_source_fills": sum(len(r["changes"]["masked_source_fills"]) for r in records),
        "inserted_coordinate_slots": 5,
        "inserted_coordinate_fills": sum(len(r["changes"]["inserted_coordinate_fills"]) for r in records),
        "remaining_unknown_inserted_coordinates": 2,
        "deletions": 0, "reordered_blocks": 0, "published_square_changes": 0,
    }
    assert [r["raw_within_working_frame"]["fixed_positions"] for r in records] == [106, 108, 104, 103]
    assert [r["edition"]["fixed_positions"] for r in records] == [111, 110, 105, 106]
    assert summary["known_coordinate_substitutions"] == 10
    assert summary["masked_source_fills"] == 5 and summary["inserted_coordinate_fills"] == 3
    return {
        "schema": "adfgvx-military-intendant-remit-certificate-v1",
        "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
        "inputs_sha256": sha(HERE / "inputs.json"), "summary": summary, "records": records,
        "limits": [
            "B1 is conditional on a 228-coordinate frame with five consecutive missing coordinates; its representative gap position 145 is not uniquely established.",
            "No source coordinate is removed or permuted. Q/R and three undecidable glyphs are masked before analysis, with their locations and observed appearances preserved.",
            "Gap templates were derived after reading candidates. Their minimum repair costs and ties are finite conditional comparisons, not independent evidence or a recovery probability.",
            "The original numeral labels and every unfilled square cell are preserved. Remaining domains cannot be chosen independently when they share the same square cell.",
            "Global witnesses use arbitrary common square/source completions only to prove consistency; they are not original plaintext proposals.",
            "The edition's exact costs do not establish unique wording, a unique loss mechanism, or first historical decipherment.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    if args.pdf:
        assert sha(args.pdf) == inputs["source"]["pdf_sha256"]
    result = run(inputs)
    gaps = gap_audit(inputs)
    verify_candidate_scores(inputs, gaps, args.book_model, args.radio_model)
    for name, value in [("certificates.json", result), ("gap_audit.json", gaps)]:
        path = HERE / name
        if args.verify:
            assert value == json.loads(path.read_text())
        else:
            path.write_text(json.dumps(value, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"],
                      "gap_candidates": gaps["candidate_positions"],
                      "model_score_rechecks": 224 * (bool(args.book_model) + bool(args.radio_model))}, indent=2))


if __name__ == "__main__":
    main()
