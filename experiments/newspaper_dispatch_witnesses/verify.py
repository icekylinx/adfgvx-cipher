#!/usr/bin/env python3
"""Verify the source transcription, bounded lexical repairs and remaining domains.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published keys: Lasry, Niebel, Kopal and Wacker.
"""
from pathlib import Path
import argparse
from collections import Counter
import json
import itertools
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
    assert sha(HERE / "prior_evidence.json") == inputs["prior_credit"]["prior_evidence_sha256"]
    prior_dir = ROOT / inputs["prior_credit"]["existing_source_package"]
    assert sha(prior_dir / "inputs.json") == inputs["prior_credit"]["existing_inputs_sha256"]
    assert sha(prior_dir / "certificates.json") == inputs["prior_credit"]["existing_certificates_sha256"]
    prior_certificate = json.loads((prior_dir / "certificates.json").read_text())
    published = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    for key_id, key in inputs["keys"].items():
        assert key["square"] == published[key_id]["square"]
        assert key["column_rank_order"] == published[key_id]["column_rank_order"]
    records, totals = [], Counter()
    for rec in inputs["records"]:
        key = inputs["keys"][rec["key_id"]]
        ranks, square = key["column_rank_order"], key["square"]
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-PQ")
        cipher = "".join(x if x in "ADFGVX" else "?" for x in literal)
        assert len(cipher) == rec["literal_source_slots"]
        if rec["advertised_length"] is not None:
            assert len(cipher) == rec["advertised_length"]
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        edition = repair(cipher, literal, {"text": rec["editorial_template"], "pair_overrides": rec["pair_overrides"]},
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
                       "noncoordinate_source_masks": sum(x not in "ADFGVX-" for x in literal),
                       "plaintext_positions": raw["plaintext_positions"],
                       "raw_fixed_positions": raw["fixed_positions"],
                       "edition_fixed_positions": edition["reading"]["fixed_positions"],
                       "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"]),
                       "source_erasure_fills": len(edition["erasure_fills"]),
                       "remaining_source_erasure_slots": edition["ciphertext"].count("?")})
    corroboration = {}
    if records[0]["id"] == "p79_A1":
        assert [r["source_slots"] for r in records] == [262, 336]
        assert [r["raw"]["fixed_positions"] for r in records] == [130, 168]
        assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [131, 168]
        assert totals["known_coordinate_substitutions"] == 0
        assert totals["source_erasure_fills"] == 1
        assert records[0]["source_literal"][134] == "P"
        prior = prior_certificate["records"][0]
        assert prior["id"] == "p83_B"
        assert records[1]["source_literal"] == prior["source_literal"]
        assert records[1]["raw"]["plaintext"] == prior["raw"]["plaintext"]
        corroboration = {"kind": "complete identical ciphertext", "new_record": "p79_A2",
                         "prior_record": "p83_B", "equal_observed_coordinates": 336,
                         "conflicts": 0, "missing_coordinates": 0,
                         "new_contiguous_first_part": "p79_A1",
                         "scope": "The source labels the two p79 parts as one message; its second part is byte-for-byte identical to the already reviewed p83 B."}
    else:
        assert [r["id"] for r in records] == ["p166_B1", "p166_B2"]
        assert [r["source_slots"] for r in records] == [200, 186]
        assert [r["raw"]["fixed_positions"] for r in records] == [99, 44]
        assert [r["edition"]["reading"]["fixed_positions"] for r in records] == [100, 92]
        assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [1, 7]
        assert [len(r["edition"]["erasure_fills"]) for r in records] == [1, 49]
        assert records[0]["source_literal"][174] == "Q"
        assert records[1]["source_literal"][137:] == "-" * 49
        assert records[1]["remaining_positions"] == [{"plaintext_position": 49,
                    "domain": "56", "source_coordinate_indices": [172, 32],
                    "source_pair": "?A", "edited_pair": "XA"}]
        families = []
        alltotals = Counter()
        for rec in records:
            prior_id = rec["id"].replace("p166", "p171")
            prior = next(r for r in prior_certificate["records"] if r["id"] == prior_id)
            old_cipher = "".join(x if x in "ADFGVX" else "?" for x in prior["source_literal"])
            old_raw = reading(old_cipher, ranks, square)
            assert old_raw["plaintext"] == prior["raw"]["plaintext"]
            target = prior["edition"]["ciphertext"]
            assert rec["edition"]["ciphertext"] == target
            positions = []
            subtotals = Counter()
            for i, indices in enumerate(rec["raw"]["source_position_pairs_0based"]):
                candidate_pair = "".join(target[j] for j in indices)
                raw_pairs = ["".join(c[j] for j in indices) for c in [rec["analysis_frame"], old_cipher]]
                def cost(pair):
                    return sum(x in "ADFGVX" and x != y for p in raw_pairs for x, y in zip(p, pair))
                minimum = min(cost("".join(pair)) for pair in itertools.product("ADFGVX", repeat=2))
                candidate_cost = cost(candidate_pair)
                if candidate_pair in raw_pairs:
                    support = "complete_pair_in_one_received_copy"
                elif all(any(p[j] == candidate_pair[j] for p in raw_pairs) for j in [0, 1]):
                    support = "observed_halves_from_different_copies"
                else:
                    support = "still_editorial_pair_choice"
                positions.append({"plaintext_position": i,
                                  "candidate_label": rec["edition"]["reading"]["plaintext"][i],
                                  "candidate_domain": rec["edition"]["reading"]["domains"][i],
                                  "source_coordinate_indices_in_each_native_frame": indices,
                                  "candidate_pair": candidate_pair,
                                  "raw_pairs_p166_then_p171": raw_pairs,
                                  "support": support,
                                  "minimum_common_coordinate_substitution_cost": minimum,
                                  "candidate_common_coordinate_substitution_cost": candidate_cost})
                subtotals.update({support: 1, "minimum_common_coordinate_substitution_cost": minimum,
                                  "candidate_common_coordinate_substitution_cost": candidate_cost})
            fills = []
            for fill in rec["edition"]["erasure_fills"]:
                j = fill["source_position_0based"]
                fills.append({"new_source_coordinate_index": j, "proposed": fill["proposed"],
                              "prior_raw_coordinate": old_cipher[j],
                              "directly_observed_in_prior_copy": old_cipher[j] == fill["proposed"]})
            supported_fills = sum(f["directly_observed_in_prior_copy"] for f in fills)
            subtotals["new_fills_directly_observed_in_prior_copy"] = supported_fills
            subtotals["new_fills_not_observed_in_prior_copy"] = len(fills) - supported_fills
            families.append({"new_record": rec["id"], "prior_record": prior_id,
                             "common_frame_length": len(target), "common_candidate_ciphertext": target,
                             "summary": dict(subtotals), "positions": positions,
                             "new_mask_fill_witnesses": fills})
            alltotals.update(subtotals)
        assert [f["summary"]["complete_pair_in_one_received_copy"] for f in families] == [100, 88]
        assert [(p["plaintext_position"], p["candidate_label"]) for p in families[1]["positions"]
                if p["support"] == "observed_halves_from_different_copies"] == [(28, "B"), (38, "R")]
        assert [(p["plaintext_position"], p["candidate_label"]) for p in families[1]["positions"]
                if p["support"] == "still_editorial_pair_choice"] == [(1, "O"), (6, "P"), (59, "D")]
        assert alltotals["minimum_common_coordinate_substitution_cost"] == 10
        assert alltotals["candidate_common_coordinate_substitution_cost"] == 14
        assert alltotals["new_fills_directly_observed_in_prior_copy"] == 49
        assert alltotals["new_fills_not_observed_in_prior_copy"] == 1
        corroboration = {"kind": "declared common-body comparison in unchanged native frames",
                         "counts_scope": "Families include prior p171 witnesses for comparison; the main source totals count only the two new p166 physical records.",
                         "common_plaintext_positions": 193, "summary": dict(alltotals),
                         "families": families,
                         "limits": ["The existing p171 edited body selected the comparison target; this is not a blind control.",
                                    "The coordinate-only lower bound is conditional on the common-frame model and does not identify the original wording.",
                                    "The unchanged partial square leaves the XA numeral cell in56; no numerical interpretation is inferred."]}
    return {"schema": inputs["schema"].replace("input", "certificate"),
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "added_coordinates": 0, "deleted_coordinates": 0,
                        "reordered_blocks": 0, "baseline_key_changes": 0,
                        "new_numeral_assignments": 0},
            "records": records, "cross_page_witness_comparison": corroboration,
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
