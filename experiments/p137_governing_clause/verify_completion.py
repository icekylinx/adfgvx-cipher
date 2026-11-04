#!/usr/bin/env python3
"""Check the two separator fills completing the optional p137 A5 reading."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    inp = read(HERE / "completion_inputs.json")
    for path, expected in inp["dependencies"].items():
        assert digest(ROOT / path) == expected, path
    source = read(ROOT / inp["source_input"])
    key = source["key"]
    square, ranks = key["square"], key["column_rank_order"]
    prior = read(ROOT / inp["prior_certificate"])
    layer = prior["layers"][inp["prior_layer"]]
    wire = layer["wire"]
    # Original row-major coordinate positions in transmitted column order.
    order = [i for col in sorted(range(len(ranks)), key=ranks.__getitem__)
             for i in range(col, len(wire), len(ranks))]
    inverse = {i: j for j, i in enumerate(order)}

    def decode(full_wire):
        row = [full_wire[inverse[i]] for i in range(len(wire))]
        return "".join(square[6 * CO.index(a) + CO.index(b)]
                       for a, b in zip(row[::2], row[1::2]))

    def encode(text):
        row = "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6]
                      for c in text)
        return "".join(row[i] for i in order)

    unknown = [i for i, c in enumerate(wire) if c == "?"]
    assert unknown == [222, 246]
    variants = []
    for values in itertools.product(CO, repeat=2):
        trial = list(wire)
        for i, value in zip(unknown, values):
            trial[i] = value
        trial = "".join(trial)
        text = decode(trial)
        assert encode(text) == trial
        assert all(a == "?" or a == b for a, b in zip(layer["raw"], text))
        variants.append({"fills": "".join(values),
                         "labels_at_75_and_125": text[75] + text[125]})
    assert len({v["labels_at_75_and_125"] for v in variants}) == 36
    text = inp["expected_complete_text"]
    complete = encode(text)
    assert decode(complete) == text
    assert len(text) == 126 and "?" not in text
    assert [i for i, (a, b) in enumerate(zip(wire, complete)) if a != b] == unknown
    assert [i for i, (a, b) in enumerate(zip(layer["raw"], text)) if a != b] == inp["proposed_separators"]
    details = []
    for position in inp["proposed_separators"]:
        raw = prior["raw"]["positions"][position]
        assert raw["pair"].count("?") == 1 and "X" in raw["domain"]
        frame_positions = [inverse[2 * position], inverse[2 * position + 1]]
        assert frame_positions == raw["model_indices"]
        changed = next(i for i in frame_positions if wire[i] == "?")
        assert raw["source_indices"][frame_positions.index(changed)] is None
        details.append({"plaintext_index": position, "original_pair": raw["pair"],
                        "original_domain": raw["domain"],
                        "source_indices": raw["source_indices"],
                        "filled_model_index": changed, "filled_coordinate": complete[changed],
                        "proposed_label": "X"})
    final_cost = dict(layer["cost"])
    final_cost["missing_coordinate_fill"] += 2
    assert final_cost == {"observed_substitution": 7, "printed_mask_fill": 4,
                          "missing_coordinate_fill": 37}
    # Derive cumulative costs directly from the received 215 slots.
    rec = next(r for r in source["records"] if r["id"] == "p137_A5")
    literal = "".join("".join(rec["source_rows"]).split())
    for marker in ("{INTERFERENCE_1}", "{INTERFERENCE_2}"):
        literal = literal.replace(marker, "")
    assert len(literal) == 215
    costs = {"observed_substitution": 0, "printed_mask_fill": 0,
             "missing_coordinate_fill": len(complete) - len(literal)}
    for old, new in zip(literal, complete):
        if old not in CO:
            costs["printed_mask_fill"] += 1
        elif old != new:
            costs["observed_substitution"] += 1
    assert costs == final_cost
    sensitivity = dict(prior["visual_V_alternative"]["cost"])
    sensitivity["missing_coordinate_fill"] += 2
    assert sensitivity["observed_substitution"] == 6
    return {"schema": inp["schema"], "authors": inp["authors"],
            "input_sha256": digest(HERE / "completion_inputs.json"),
            "prior_fixed_positions": 124, "complete_fixed_positions": 126,
            "complete_proposed_text": text, "complete_proposed_ciphertext": complete,
            "separator_fills": details, "all_36_residual_label_pairs": variants,
            "incremental_cost": {"observed_substitution": 0,
                                 "printed_mask_fill": 0, "missing_coordinate_fill": 2},
            "total_cost": costs, "source68_V_sensitivity_total_cost": sensitivity,
            "interpretation": inp["interpretation"], "limits": inp["limits"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = run()
    path = HERE / "completion_certificate.json"
    if args.verify:
        assert result == read(path)
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "fixed_positions": 126,
                      "total_positions": 126, "incremental_cost": result["incremental_cost"]}))
