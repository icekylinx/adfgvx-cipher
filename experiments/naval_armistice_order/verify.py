#!/usr/bin/env python3
"""Source-level edition of the p178 naval armistice order.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Prior body identification: Lasry, Niebel, Kopal and Wacker (2016/2017).
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.withdrawal_recovery.verify import CO, reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    source, key = inputs["source"], inputs["key"]
    assert sha(HERE / source["full_page_image"]) == source["full_page_image_sha256"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"] if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    unused = "".join(sorted(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") - set(square)))
    assert unused == "56789"
    records = []
    for record in inputs["records"]:
        assert sha(HERE / record["source_crop"]) == record["source_crop_sha256"]
        groups = " ".join(record["source_rows"]).split()
        received = "".join(groups)
        assert set(received) <= set(CO)
        framing = record.get("short_group")
        alternatives = []
        if framing:
            index = framing["group_index_0based"]
            start = sum(map(len, groups[:index]))
            assert groups[index] == framing["literal"] and len(groups[index]) == 4
            assert start == framing["received_coordinate_start_0based"]
            assert framing["candidate_gap_boundaries_0based"] == list(range(start, start + 5))
            for gap in framing["candidate_gap_boundaries_0based"]:
                candidate_frame = received[:gap] + "?" + received[gap:]
                candidate_raw = reading(candidate_frame, ranks, square)
                candidate = repair(candidate_frame, candidate_frame, record["editorial_recipe"], ranks, square, candidate_raw)
                alternatives.append({"gap_boundary_0based": gap,
                                     "known_coordinate_substitutions": len(candidate["known_coordinate_substitutions"]),
                                     "inserted_value": candidate["ciphertext"][gap]})
            chosen = framing["chosen_gap_boundary_0based"]
            frame = received[:chosen] + "?" + received[chosen:]
            minimum = min(a["known_coordinate_substitutions"] for a in alternatives)
            assert [a["gap_boundary_0based"] for a in alternatives if a["known_coordinate_substitutions"] == minimum] == [chosen]
        else:
            frame, chosen = received, None
        assert len(frame) == record["frame_length"]
        if record["advertised_length_reading"] is not None:
            assert record["frame_length"] == record["advertised_length_reading"]
        else:
            assert record["advertised_length_candidates"]
            assert record["header_glyphs_unresolved"] is True
        raw = reading(frame, ranks, square)
        proposal = repair(frame, frame, record["editorial_recipe"], ranks, square, raw)
        fills = proposal.pop("erasure_fills")
        proposal["inserted_coordinate_values"] = fills
        proposal["remaining_unknown_frame_positions_0based"] = proposal.pop("remaining_erased_source_positions_0based")
        assert len(fills) == (1 if framing else 0)
        if framing:
            assert fills[0]["source_position_0based"] == chosen
            assert fills[0]["proposed"] == framing["inserted_coordinate"]
        for edit in proposal["known_coordinate_substitutions"]:
            position = edit["source_position_0based"]
            assert position != chosen
            edit["received_coordinate_position_0based"] = position - (chosen is not None and position > chosen)
            assert received[edit["received_coordinate_position_0based"]] == edit["observed"]
        raw["global_witness"] = global_witness(frame, ranks, square, raw)
        proposal["reading"]["global_witness"] = global_witness(proposal["ciphertext"], ranks, square, proposal["reading"])
        if "?" not in proposal["reading"]["plaintext"]:
            assert encrypt(proposal["reading"]["plaintext"], ranks, square) == proposal["ciphertext"]
            proposal["exact_roundtrip_with_unchanged_partial_square"] = True
        records.append({"id": record["id"],
                        "advertised_length_reading": record["advertised_length_reading"],
                        "advertised_length_candidates": record.get("advertised_length_candidates", [record["advertised_length_reading"]]),
                        "header_glyphs_unresolved": record.get("header_glyphs_unresolved", False),
                        "received_coordinates": len(received),
                        "received_ciphertext": received,
                        "received_sha256": hashlib.sha256(received.encode()).hexdigest(),
                        "framed_coordinates": len(frame), "framed_ciphertext": frame,
                        "raw": raw, "edition": proposal,
                        "fixed_text_short_group_comparison": alternatives})
    assert len(set(r["edition"]["reading"]["global_witness"]["square"] for r in records)) == 1
    last = records[-1]
    unknown_fields = []
    for position, domain in enumerate(last["edition"]["reading"]["domains"]):
        if len(domain) > 1:
            pair = "".join(last["edition"]["ciphertext"][p] for p in last["edition"]["reading"]["source_position_pairs_0based"][position])
            unknown_fields.append({"plaintext_position_0based": position, "pair": pair, "domain": domain})
    assert [f["pair"] for f in unknown_fields] == ["XA", "XG"]
    numeric_witnesses = []
    for first, second in itertools.permutations(unused, 2):
        completed = list(square)
        for field, value in zip(unknown_fields, (first, second)):
            pair = field["pair"]
            completed[6 * CO.index(pair[0]) + CO.index(pair[1])] = value
        rest = iter(sorted(set(unused) - {first, second}))
        completed = "".join(next(rest) if c == "?" else c for c in completed)
        plain = decrypt(last["edition"]["ciphertext"], ranks, completed)
        assert encrypt(plain, ranks, completed) == last["edition"]["ciphertext"]
        assert all(c in domain for c, domain in zip(plain, last["edition"]["reading"]["domains"]))
        numeric_witnesses.append({"XA": first, "XG": second, "square": completed})
    assert len(numeric_witnesses) == 20
    summary = {"source_parts": len(records),
               "received_coordinates": sum(r["received_coordinates"] for r in records),
               "hypothesized_inserted_coordinates": sum(len(r["edition"]["inserted_coordinate_values"]) for r in records),
               "framed_coordinates": sum(r["framed_coordinates"] for r in records),
               "plaintext_positions": sum(r["raw"]["plaintext_positions"] for r in records),
               "raw_framed_fixed_positions": sum(r["raw"]["fixed_positions"] for r in records),
               "edition_fixed_positions": sum(r["edition"]["reading"]["fixed_positions"] for r in records),
               "known_coordinate_substitutions": sum(len(r["edition"]["known_coordinate_substitutions"]) for r in records),
               "source_erasures": 0, "unresolved_numeric_positions": len(unknown_fields)}
    assert summary["received_coordinates"] == 1436 and summary["plaintext_positions"] == 719
    assert summary["known_coordinate_substitutions"] == 14 and summary["edition_fixed_positions"] == 717
    return {"schema": "adfgvx-naval-armistice-certificate-v1", "prepared_by": inputs["prepared_by"],
            "prior_reading": inputs["prior_reading"], "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": summary, "records": records,
            "unresolved_fields": unknown_fields,
            "distinct_numeric_pair_witnesses": numeric_witnesses,
            "numeric_witnesses_are_proposed_readings": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--prior-paper", type=Path)
    args = parser.parse_args()
    result = run()
    inputs = json.loads((HERE / "inputs.json").read_text())
    if args.pdf:
        assert sha(args.pdf) == inputs["source"]["pdf_sha256"]
    if args.prior_paper:
        assert sha(args.prior_paper) == inputs["prior_reading"]["inspected_author_copy_sha256"]
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
