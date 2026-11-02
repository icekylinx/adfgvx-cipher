#!/usr/bin/env python3
"""Certify p191's group displacement, exact repairs and retained uncertainty.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published key: Lasry, Niebel, Kopal and Wacker.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt, decrypt
from experiments.withdrawal_recovery.verify import AL, CO, reading, repair, sha
from experiments.operational_recovery.verify import global_witness
from geometry import run as geometry_run


def complete(square, cell=None, symbol=None):
    result = list(square)
    if cell is not None:
        if result[cell] == "?":
            assert symbol not in square
            result[cell] = symbol
        else:
            assert result[cell] == symbol
    unused = iter(sorted(set(AL) - set(result)))
    result = "".join(next(unused) if c == "?" else c for c in result)
    assert len(set(result)) == 36
    return result


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    source, key = inputs["source"], inputs["key"]
    assert sha(HERE / source["crop"]) == source["crop_sha256"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"] if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    geometry = geometry_run(inputs)
    assert geometry == json.loads((HERE / "geometry_certificate.json").read_text())
    assert geometry["target"]["minimum_known_coordinate_disagreements"] == 0
    assert geometry["target"]["minimum_distinct_candidates"] == 1
    assert geometry["fresh_control"]["unique_true_ciphertext_minimizer"]
    control = inputs["fresh_control"]
    assert encrypt(control["truth"], ranks, control["true_square"]) == control["full_ciphertext"]
    assert all(a == "?" or a == b for a, b in zip(square, control["true_square"]))
    records = []
    for rec in inputs["records"]:
        groups = " ".join(rec["source_rows"]).split()
        literal = "".join(groups)
        assert len(literal) == rec["printed_length"]
        assert set(literal) <= set(CO + "-")
        analysis = literal.replace("-", "?")
        literal_raw = reading(analysis, ranks, square)
        group_maps = []
        start = 0
        for group in groups:
            group_maps.append(list(range(start, start + len(group))))
            start += len(group)
        if rec["group_move"]:
            move = rec["group_move"]
            i, j = move["received_group_index_0based"], move["insert_before_received_group_index_0based"]
            assert i > j and groups[i] == move["literal_group"] == "AXFVA"
            assert len(groups[i]) == 5
            groups.insert(j, groups.pop(i))
            group_maps.insert(j, group_maps.pop(i))
        position_map = sum(group_maps, [])
        frame_literal = "".join(groups)
        frame = frame_literal.replace("-", "?")
        assert frame_literal == "".join(literal[i] for i in position_map)
        assert sorted(position_map) == list(range(len(literal)))
        assert sorted(frame_literal) == sorted(literal)
        raw = reading(frame, ranks, square)
        if rec["group_move"]:
            assert geometry["target"]["all_minima"][0]["ciphertext"] == frame
        edition = repair(frame, frame_literal, rec["editorial_recipe"], ranks, square, raw)
        assert len(edition["known_coordinate_substitutions"]) == 2
        assert rec["literal_spelling_retained"] in edition["reading"]["plaintext"]
        for edit in edition["known_coordinate_substitutions"] + edition["erasure_fills"]:
            framed = edit["source_position_0based"]
            physical = position_map[framed]
            edit["received_coordinate_position_0based"] = physical
            edit["received_group_1based"] = physical // 5 + 1
            edit["coordinate_within_group_1based"] = physical % 5 + 1
            assert literal[physical] == edit["observed"]
        literal_raw["global_witness"] = global_witness(analysis, ranks, square, literal_raw)
        raw["global_witness"] = global_witness(frame, ranks, square, raw)
        edition["reading"]["global_witness"] = global_witness(edition["ciphertext"], ranks, square, edition["reading"])
        records.append({"id": rec["id"], "source_slots": len(literal),
                        "literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
                        "literal_source": literal, "analysis_ciphertext": analysis,
                        "source_erasures": literal.count("-"),
                        "untouched_literal_reading": literal_raw,
                        "group_move": rec["group_move"],
                        "framed_ciphertext": frame,
                        "framed_position_to_received_position_0based": position_map,
                        "conditional_frame_reading": raw, "edition": edition})
    first, second = records
    unknown_first = []
    for i, domain in enumerate(first["edition"]["reading"]["domains"]):
        if len(domain) > 1:
            pair = "".join(first["edition"]["ciphertext"][j]
                           for j in first["edition"]["reading"]["source_position_pairs_0based"][i])
            unknown_first.append({"plaintext_position_0based": i, "pair": pair, "domain": domain})
    assert [x["pair"] for x in unknown_first] == ["GD", "FV", "XX"]
    assert len({x["pair"] for x in unknown_first}) == 3
    second_reading = second["edition"]["reading"]
    unresolved = [i for i, d in enumerate(second_reading["domains"]) if len(d) > 1]
    assert unresolved == [63]
    domain = second_reading["domains"][63]
    assert domain == "0234789OQUWY"
    remaining = second["edition"]["remaining_erased_source_positions_0based"]
    assert remaining == [88]
    pair_positions = second_reading["source_position_pairs_0based"][63]
    witnesses = []
    for symbol in domain:
        found = None
        for coordinate in CO:
            cipher = list(second["edition"]["ciphertext"])
            cipher[88] = coordinate
            cipher = "".join(cipher)
            pair = "".join(cipher[i] for i in pair_positions)
            cell = 6 * CO.index(pair[0]) + CO.index(pair[1])
            if square[cell] == symbol or (square[cell] == "?" and symbol not in square):
                whole = complete(square, cell, symbol)
                plain2 = decrypt(cipher, ranks, whole)
                plain1 = decrypt(first["edition"]["ciphertext"], ranks, whole)
                assert plain2[63] == symbol
                assert encrypt(plain2, ranks, whole) == cipher
                assert encrypt(plain1, ranks, whole) == first["edition"]["ciphertext"]
                for plain, r in [(plain1, first), (plain2, second)]:
                    assert all(c in d for c, d in zip(plain, r["edition"]["reading"]["domains"]))
                found = {"connective_symbol": symbol, "coordinate_fill": coordinate,
                         "full_square_witness": whole,
                         "part1_plaintext_witness": plain1, "part2_plaintext_witness": plain2,
                         "is_selected_reading": False}
                break
        assert found is not None
        witnesses.append(found)
    summary = {"source_parts": 2,
               "source_coordinate_slots": sum(r["source_slots"] for r in records),
               "source_erasures": sum(r["source_erasures"] for r in records),
               "plaintext_positions": sum(r["untouched_literal_reading"]["plaintext_positions"] for r in records),
               "untouched_literal_fixed_positions": sum(r["untouched_literal_reading"]["fixed_positions"] for r in records),
               "conditional_frame_fixed_positions": sum(r["conditional_frame_reading"]["fixed_positions"] for r in records),
               "edition_fixed_positions": sum(r["edition"]["reading"]["fixed_positions"] for r in records),
               "complete_group_moves": 1,
               "inserted_coordinates": 0, "deleted_coordinates": 0,
               "known_coordinate_substitutions": sum(len(r["edition"]["known_coordinate_substitutions"]) for r in records),
               "erasure_fills": sum(len(r["edition"]["erasure_fills"]) for r in records),
               "remaining_source_erasures": len(remaining), "published_square_changes": 0}
    assert summary["source_coordinate_slots"] == 400
    assert summary["plaintext_positions"] == 200 and summary["edition_fixed_positions"] == 196
    assert summary["known_coordinate_substitutions"] == 4 and summary["erasure_fills"] == 12
    return {"schema": "adfgvx-boots-source-certificate-v1", "prepared_by": inputs["prepared_by"],
            "prior_credit": inputs["prior_credit"], "inputs_sha256": sha(HERE / "inputs.json"),
            "geometry_certificate_sha256": sha(HERE / "geometry_certificate.json"),
            "summary": summary, "records": records,
            "part1_unresolved_key_cells": unknown_first,
            "part1_symbols_must_be_distinct": True,
            "part2_connective_domain": domain,
            "part2_all_domain_values_have_joint_global_witnesses": witnesses,
            "limits": ["The one-group move is a conditional source-order repair, not an assertion about how the reception or transcription error occurred.",
                       "The ordinary-word geometry comparison is posthoc and conditional on its frozen mask.",
                       "Unit and quantity symbols remain unassigned, and the complete connective domain is retained.",
                       "SELLV and BEKLEIDNG are preserved literally; expanded prose is separate from the fixed-length ciphertext edition."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.pdf:
        assert sha(args.pdf) == json.loads((HERE / "inputs.json").read_text())["source"]["pdf_sha256"]
    result = run()
    target = HERE / "certificate.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
