#!/usr/bin/env python3
"""All one-full-group moves, selected by a masked ordinary-word objective.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The target anchors are posthoc; footer, numbers and names are not scored.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, transposition_indices

CO = "ADFGVX"


def expected_coordinates(mask, ranks, square):
    stream = []
    for char in mask:
        if char == "?":
            stream.extend("??")
        else:
            cell = square.index(char)
            stream.extend((CO[cell // 6], CO[cell % 6]))
    return "".join(stream[i] for i in transposition_indices(len(stream), ranks))


def enumerate_moves(received, mask, ranks, square):
    assert len(received) == 186 and len(mask) == 93
    assert mask[85:] == "?" * 8
    assert all(c == "?" or c.isalpha() for c in mask)
    groups = [received[i:i + 5] for i in range(0, 185, 5)]
    tail = received[185:]
    expected = expected_coordinates(mask, ranks, square)
    candidates = {received: [{"identity": True}]}
    operations = 1
    for source in range(37):
        for target in range(37):
            if source == target:
                continue
            g = groups.copy()
            g.insert(target, g.pop(source))
            cipher = "".join(g) + tail
            candidates.setdefault(cipher, []).append({"received_group_index_0based": source,
                                                       "insert_index_after_removal_0based": target})
            operations += 1
    assert operations == 1333
    rows = []
    digest_rows = []
    for cipher, aliases in candidates.items():
        mismatches = [i for i, (a, b) in enumerate(zip(cipher, expected))
                      if a != "?" and b != "?" and a != b]
        fills = [i for i, (a, b) in enumerate(zip(cipher, expected)) if a == "?" and b != "?"]
        row = {"known_coordinate_disagreements": len(mismatches),
               "disagreement_positions_0based": mismatches,
               "ordinary_mask_erasure_fills": len(fills),
               "operation_aliases": aliases, "ciphertext": cipher,
               "raw_plaintext": decrypt(cipher, ranks, square)}
        rows.append(row)
        digest_rows.append((cipher, len(mismatches), len(fills)))
    rows.sort(key=lambda r: (r["known_coordinate_disagreements"], r["ciphertext"]))
    minimum = rows[0]["known_coordinate_disagreements"]
    minima = [r for r in rows if r["known_coordinate_disagreements"] == minimum]
    baseline = next(r for r in rows if r["ciphertext"] == received)
    return {"enumerated_operations_including_identity": operations,
            "distinct_candidate_ciphertexts": len(rows),
            "ordinary_plaintext_positions_scored": sum(c != "?" for c in mask),
            "footer_plaintext_positions_scored": 0,
            "minimum_known_coordinate_disagreements": minimum,
            "minimum_distinct_candidates": len(minima), "all_minima": minima,
            "identity": baseline, "leading_distinct_candidates": rows[:10],
            "all_candidate_costs_sha256": hashlib.sha256(json.dumps(sorted(digest_rows), separators=(",", ":")).encode()).hexdigest()}


def run(inputs):
    key = inputs["key"]
    target = inputs["records"][1]
    received = "".join("".join(target["source_rows"]).split()).replace("-", "?")
    historical = enumerate_moves(received, inputs["geometry_selection"]["target_ordinary_word_mask"],
                                 key["column_rank_order"], key["square"])
    control = inputs["fresh_control"]
    synthetic = enumerate_moves(control["received_ciphertext"], control["ordinary_word_mask"],
                                key["column_rank_order"], key["square"])
    true_control = control["true_masked_ciphertext"]
    synthetic["true_geometry_in_minimizers"] = any(r["ciphertext"] == true_control for r in synthetic["all_minima"])
    synthetic["unique_true_ciphertext_minimizer"] = (synthetic["minimum_distinct_candidates"] == 1 and
                                                    synthetic["all_minima"][0]["ciphertext"] == true_control)
    return {"schema": "adfgvx-boots-group-move-screen-v1",
            "prepared_by": inputs["prepared_by"],
            "inputs_sha256": hashlib.sha256((HERE / "inputs.json").read_bytes()).hexdigest(),
            "target": historical, "fresh_control": synthetic,
            "limits": ["Target ordinary-word anchors were chosen after inspecting the damaged source; this is a conditional fixed-text comparison.",
                       "All footer positions, quantities, unit numbers and names are excluded from the selection objective.",
                       "All globally minimizing operations within the one-complete-group-move family are retained.",
                       "The fresh control validates this exact damage family and implementation; it is not a general decipherment-rate estimate."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    result = run(inputs)
    target = HERE / "geometry_certificate.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify,
                      "target_minimum": result["target"]["minimum_known_coordinate_disagreements"],
                      "target_minimum_candidates": result["target"]["minimum_distinct_candidates"],
                      "target_identity_cost": result["target"]["identity"]["known_coordinate_disagreements"],
                      "control_unique_true_minimizer": result["fresh_control"]["unique_true_ciphertext_minimizer"]}, indent=2))


if __name__ == "__main__":
    main()
