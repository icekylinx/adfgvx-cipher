#!/usr/bin/env python3
"""Verify the literal source edition and exact ADFGVX repair costs.

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
        cipher = "".join("".join(rec["source_rows"]).split())
        assert set(cipher) <= set("ADFGVX")
        assert len(cipher) == rec["literal_source_slots"] == rec["advertised_length"]
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw"]
        assert raw["fixed_positions"] == raw["plaintext_positions"]
        edition = repair(cipher, cipher, {"text": rec["editorial_template"], "pair_overrides": []},
                         ranks, square, raw)
        assert not edition["erasure_fills"]
        assert len(edition["ciphertext"]) == len(cipher)
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
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
        records.append({"id": rec["id"], "source_literal": cipher,
                        "source_slots": len(cipher), "analysis_frame": cipher,
                        "frame_to_source_indices": list(range(len(cipher))),
                        "raw": raw, "edition": edition,
                        "all_raw_digit_J_Q_Y_occurrences": labels})
        totals.update({"physical_source_parts": 1, "literal_source_slots": len(cipher),
                       "working_coordinates": len(cipher),
                       "plaintext_positions": raw["plaintext_positions"],
                       "raw_fixed_positions": raw["fixed_positions"],
                       "edition_fixed_positions": edition["reading"]["fixed_positions"],
                       "known_coordinate_substitutions": len(edition["known_coordinate_substitutions"])})
    witnesses = []
    by_id = {r["id"]: r for r in records}
    if "p98_A2" in by_id:
        assert [r["source_slots"] for r in records] == [252, 264, 266]
        assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [3, 1, 3]
        assert "NUMEHR" in by_id["p98_A2"]["edition"]["reading"]["plaintext"]
        assert "NUMEHR" in by_id["p98_B"]["edition"]["reading"]["plaintext"]
        assert "NIKILJEW" in by_id["p98_A2"]["edition"]["reading"]["plaintext"]
        assert "NIKOLAJEW" in by_id["p98_B"]["edition"]["reading"]["plaintext"]
        for target_id, target_pos, witness_id, witness_pos in [
            ("p98_A2", 103, "p98_B", 104),
            ("p98_B", 16, "p98_A2", 16),
            ("p98_B", 24, "p98_A2", 24),
            ("p98_B", 34, "p98_A2", 34),
        ]:
            target, witness = by_id[target_id], by_id[witness_id]
            indices = target["raw"]["source_position_pairs_0based"][target_pos]
            observed_indices = witness["raw"]["source_position_pairs_0based"][witness_pos]
            proposed_pair = "".join(target["edition"]["ciphertext"][i] for i in indices)
            observed_pair = "".join(witness["source_literal"][i] for i in observed_indices)
            assert proposed_pair == observed_pair
            assert target["raw"]["plaintext"][target_pos] != witness["raw"]["plaintext"][witness_pos]
            assert target["edition"]["reading"]["plaintext"][target_pos] == witness["raw"]["plaintext"][witness_pos]
            witnesses.append({"target": target_id, "target_plaintext_position": target_pos,
                              "target_source_coordinate_indices": indices,
                              "witness": witness_id, "witness_plaintext_position": witness_pos,
                              "witness_source_coordinate_indices": observed_indices,
                              "directly_observed_witness_pair": observed_pair,
                              "raw_target_symbol": target["raw"]["plaintext"][target_pos],
                              "proposed_symbol": witness["raw"]["plaintext"][witness_pos]})
    else:
        assert [r["id"] for r in records] == ["p83_B"]
        assert totals["known_coordinate_substitutions"] == 0
        assert totals["literal_source_slots"] == 336
    return {"schema": inputs["schema"].replace("input", "certificate"),
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {**dict(totals), "source_erasure_slots": 0, "source_erasure_fills": 0,
                        "added_coordinates": 0, "deleted_coordinates": 0,
                        "reordered_blocks": 0, "baseline_key_changes": 0,
                        "new_numeral_assignments": 0},
            "records": records, "repairs_supported_by_other_received_copy": witnesses,
            "limits": inputs["limits"] + [
                "Round trips and exact edit counts establish compatibility, not unique historical wording.",
                "Reference digits remain published key labels. No new digit permutation or codebook meaning is assigned.",
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
