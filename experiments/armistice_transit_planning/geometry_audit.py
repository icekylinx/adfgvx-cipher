#!/usr/bin/env python3
"""Reproduce p126 A5's finite one-coordinate geometry comparison.

Prepared by icekylinx and GPT-6 Astra Pro. The proposed text is a
retrospective template, not an independent crib. Default verification
checks every candidate string and template price. Supplying both model
paths also independently recomputes the archived candidate-finding scores.
"""
import argparse
from array import array
import json
from pathlib import Path
import sys

from verify import HERE, digest, encode, inverse, reading, transpose

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def candidates(inputs):
    rec = next(r for r in inputs["records"] if r["id"] == "p126_A5")
    source, key = rec["analysis_source"], inputs["key"]
    ranks, square = key["column_rank_order"], key["square"]
    interim = inverse(source, ranks)[0]
    result = []
    for stage, original in [("transmitted", source), ("interim", interim)]:
        for kind in ["insert_unknown", "delete"]:
            for position in range(len(original) + (kind == "insert_unknown")):
                modified = (original[:position] + "?" + original[position:]
                            if kind == "insert_unknown" else
                            original[:position] + original[position + 1:])
                stream = inverse(modified, ranks)[0] if stage == "transmitted" else modified
                raw = reading(stream, list(range(len(stream))), square)
                result.append({"stage": stage, "kind": kind, "position": position,
                               "removed_coordinate": original[position] if kind == "delete" else None,
                               "plaintext": raw["plaintext"],
                               "fixed_positions_under_candidate_geometry": raw["raw_fixed_positions"]})
    assert len(result) == 1070
    encoded = encode(rec["editorial_text"], square)
    prices = []
    for position in range(len(encoded)):
        witness = transpose(encoded[:position] + encoded[position + 1:], ranks)
        prices.append({"interim_insertion_position": position,
                       "proposed_coordinate": encoded[position],
                       "known_coordinate_substitutions": sum(
                           a != "?" and a != b for a, b in zip(source, witness)),
                       "printed_source_erasure_fills": source.count("?"),
                       "inserted_interim_coordinates": 1})
    minimum = min(p["known_coordinate_substitutions"] for p in prices)
    tied = [p["interim_insertion_position"] for p in prices
            if p["known_coordinate_substitutions"] == minimum]
    assert minimum == 4 and tied == [136]
    return result, prices, {"minimum_known_coordinate_substitutions": minimum,
                            "all_tied_positions": tied}


def load_models(args):
    result = {}
    for name, path in [("book", args.book_model), ("radio", args.radio_model)]:
        if path is None:
            continue
        model = array("f")
        model.frombytes(path.read_bytes())
        if sys.byteorder != "little":
            model.byteswap()
        assert len(model) == 37 ** 4
        result[name] = (path, model)
    return result


def score(text, model):
    values = [ABC.index(char) for char in text]
    return sum(model[((a * 37 + b) * 37 + c) * 37 + d]
               for a, b, c, d in zip(values, values[1:], values[2:], values[3:])) / (len(text) - 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    rows, prices, minimum = candidates(inputs)
    models = load_models(args)
    path = HERE / "geometry_audit.json"
    if args.verify:
        saved = json.loads(path.read_text())
        assert saved["inputs_sha256"] == digest(HERE / "inputs.json")
        assert saved["candidate_count"] == len(rows) == len(saved["candidates"])
        assert saved["template_prices"] == prices and saved["conditional_template_minimum"] == minimum
        for name, (model_path, _) in models.items():
            assert digest(model_path) == saved["models"][name]["sha256"]
        for actual, stored in zip(rows, saved["candidates"]):
            assert actual == {key: value for key, value in stored.items() if key != "scores"}
            assert set(stored["scores"]) == {"book", "radio"}
            for name, (model_path, model) in models.items():
                assert abs(score(actual["plaintext"], model) - stored["scores"][name]) < 1e-12
    else:
        assert set(models) == {"book", "radio"}, "Supply both frozen marginal models to build scores"
        for row in rows:
            row["scores"] = {name: score(row["plaintext"], model)
                             for name, (_, model) in models.items()}
        saved = {"schema": "adfgvx-p126-A5-geometry-audit-v1",
                 "prepared_by": inputs["prepared_by"],
                 "inputs_sha256": digest(HERE / "inputs.json"),
                 "candidate_count": len(rows),
                 "scope": "535 transmitted-stage candidates and 535 interim-stage candidates: 268 one-unknown insertions and 267 single-coordinate deletions at each stage.",
                 "models": {name: {"filename": model_path.name, "sha256": digest(model_path)}
                            for name, (model_path, _) in models.items()},
                 "candidates": rows, "retrospective_editorial_template": inputs["records"][4]["editorial_text"],
                 "template_prices": prices, "conditional_template_minimum": minimum,
                 "limits": ["Candidate-finding scores are language-model heuristics, not source evidence.",
                            "The editorial template was read after inspecting the source and phase alternatives; it is not an independent crib.",
                            "The unique minimum is conditional on this template and the one-coordinate interim-insertion family.",
                            "No exclusion of other multi-error or historical mechanisms is claimed."]}
        path.write_text(json.dumps(saved, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "candidate_strings": len(rows),
                      "retrospective_template_placements": len(prices),
                      "recomputed_score_models": sorted(models),
                      "conditional_template_minimum": minimum}, indent=2))


if __name__ == "__main__":
    main()
