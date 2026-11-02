#!/usr/bin/env python3
"""Verify the conditional p187 D1 frame and aviation-connection edition.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The proposed missing group is not present in the source image.
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


def edition(frame, suffix, ranks, square):
    raw = reading(frame, ranks, square)
    recipe = {"text": "?" * (len(frame) // 2 - len(suffix)) + suffix, "pair_overrides": []}
    result = repair(frame, frame, recipe, ranks, square, raw)
    return raw, result


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    source, key = inputs["source"], inputs["key"]
    assert sha(HERE / source["crop"]) == source["crop_sha256"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"] if k["id"] == key["id"])
    assert key["square"] == published["square"] and key["column_rank_order"] == published["column_rank_order"]
    ranks, square = key["column_rank_order"], key["square"]
    literal = "".join("".join(inputs["source_rows"]).split())
    mark = inputs["source_mark"]["literal_position_0based"]
    assert len(literal) == 248 and literal.count("-") == 1 and literal[mark] == "-"
    assert set(literal) <= set("ADFGVX-")
    received = literal[:mark] + literal[mark + 1:]
    assert len(received) == 247
    suffix = inputs["candidate_suffix"]
    assert len(suffix) == 76
    count = inputs["frame_hypothesis"]["inserted_coordinates"]
    assert count == 5 and len(received) + count == inputs["frame_hypothesis"]["advertised_length"]
    candidates = []
    for gap in inputs["frame_hypothesis"]["gap_boundaries_0based"]:
        frame = received[:gap] + "?" * count + received[gap:]
        raw, proposal = edition(frame, suffix, ranks, square)
        assert proposal["reading"]["plaintext"].endswith(suffix)
        assert len(proposal["known_coordinate_substitutions"]) == 2
        assert len(proposal["erasure_fills"]) == 5
        raw["global_witness"] = global_witness(frame, ranks, square, raw)
        proposal["reading"]["global_witness"] = global_witness(proposal["ciphertext"], ranks, square, proposal["reading"])
        substitutions = []
        for edit in proposal["known_coordinate_substitutions"]:
            index = edit["source_position_0based"]
            assert not gap <= index < gap + count
            received_index = index if index < gap else index - count
            literal_index = received_index if received_index < mark else received_index + 1
            substitutions.append({**edit, "received_coordinate_position_0based": received_index,
                                  "literal_slot_position_0based": literal_index})
        candidates.append({"gap_boundary_0based": gap, "framed_ciphertext": frame,
                           "inserted_group": proposal["ciphertext"][gap:gap + count],
                           "raw": raw, "edition": proposal,
                           "received_coordinate_substitutions": substitutions})
    assert len(set(c["edition"]["ciphertext"] for c in candidates)) == 1
    checks = []
    for mode, base, loss in [("exclude_mark_insert_five", received, 5),
                             ("retain_mark_as_erasure_insert_four", literal.replace("-", "?"), 4)]:
        costs = []
        for gap in range(len(base) + 1):
            frame = base[:gap] + "?" * loss + base[gap:]
            _, proposed = edition(frame, suffix, ranks, square)
            costs.append({"gap": gap,
                          "known_coordinate_substitutions": len(proposed["known_coordinate_substitutions"]),
                          "unknown_coordinate_fills": len(proposed["erasure_fills"])})
        minimum = min(c["known_coordinate_substitutions"] for c in costs)
        checks.append({"model": mode, "evaluated_boundaries": len(costs),
                       "minimum_substitutions_for_this_suffix": minimum,
                       "minimizers": [c for c in costs if c["known_coordinate_substitutions"] == minimum],
                       "all_costs": costs})
    assert checks[0]["minimum_substitutions_for_this_suffix"] == 2
    assert checks[1]["minimum_substitutions_for_this_suffix"] == 28
    primary = next(c for c in candidates if c["gap_boundary_0based"] == inputs["frame_hypothesis"]["primary_boundary"])
    return {"schema": "adfgvx-p187-aviation-certificate-v1", "prepared_by": inputs["prepared_by"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "source_literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
            "source_literal": literal, "received_coordinates": received,
            "summary": {"literal_slots_including_mark": len(literal), "received_coordinates": len(received),
                        "excluded_noncoordinate_marks": 1, "hypothesized_missing_coordinates": 5,
                        "frame_coordinates": 252, "plaintext_positions": 126,
                        "raw_framed_fixed_positions": primary["raw"]["fixed_positions"],
                        "edition_fixed_positions": primary["edition"]["reading"]["fixed_positions"],
                        "unresolved_reference_positions": primary["edition"]["reading"]["plaintext"].count("?"),
                        "known_coordinate_substitutions": 2, "inserted_coordinate_fills": 5,
                        "source_equivalent_gap_boundaries": [245, 246]},
            "candidates": candidates, "fixed_suffix_geometry_comparison": checks,
            "comparison_limit": "The suffix was proposed after inspection. The exhaustive comparison concerns this fixed suffix and these two frame families; it is not a proof that no other original text or damage model exists."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = run()
    if args.pdf:
        assert sha(args.pdf) == json.loads((HERE / "inputs.json").read_text())["source"]["pdf_sha256"]
    path = HERE / "certificate.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
