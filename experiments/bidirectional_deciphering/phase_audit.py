#!/usr/bin/env python3
"""Rebuild the 8,892 bounded p138 B phase candidates and verify their archive.

Prepared by icekylinx and GPT-6 Astra Pro. Default --verify needs no model;
optional pinned model paths recompute all scores. --output writes a portable
replay, leaving the original result untouched.
"""
import argparse
from array import array
import json
import math
from pathlib import Path
import re
import sys

from verify import HERE, CO, reading, sha, undo

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def load_model(path, expected):
    assert sha(path) == expected
    values = array("f")
    values.frombytes(path.read_bytes())
    if sys.byteorder != "little":
        values.byteswap()
    assert len(values) == 37 ** 4
    return values


def score(text, model):
    labels = [ABC.index(c) for c in text]
    return math.fsum(model[((a * 37 + b) * 37 + c) * 37 + d]
                     for a, b, c, d in zip(labels, labels[1:], labels[2:], labels[3:])) / (len(text) - 3)


def candidates(inputs):
    rec, key = inputs["record"], inputs["key"]
    ranks, square = key["column_rank_order"], key["square"]
    for fill in CO:
        source = rec["analysis_source"].replace("?", fill)
        interim, _ = undo(source, ranks)
        for stage, frame in [("transmitted", source), ("interim", interim)]:
            for mode in ["insert", "remove"]:
                for position in range(len(frame) + (mode == "insert")):
                    for value in (CO if mode == "insert" else [frame[position]]):
                        changed = frame[:position] + (value + frame[position:] if mode == "insert"
                                                     else frame[position + 1:])
                        paired = undo(changed, ranks)[0] if stage == "transmitted" else changed
                        decoded = reading(paired, square)
                        assert decoded["unpaired_coordinate"] is None
                        assert decoded["fixed_positions"] == decoded["plaintext_positions"]
                        yield {"stage": stage, "mode": mode, "position": position,
                               "value": value, "source_R_fill": fill,
                               "plaintext": decoded["plaintext"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    parser.add_argument("--original-ocr-screen", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    assert args.verify or args.output, "Specify --verify and/or a separate replay --output"
    inputs = json.loads((HERE / "inputs.json").read_text())
    meta = inputs["search"]
    for field in ["original_driver", "original_results", "original_transcription", "header_inventory"]:
        assert sha(HERE / meta[field + "_path"]) == meta[field + "_sha256"]
    old = json.loads((HERE / meta["original_results_path"]).read_text())
    assert old["source_sha256"] == meta["original_transcription_sha256"]
    original_input = json.loads((HERE / meta["original_transcription_path"]).read_text())
    assert original_input["analysis_source"] == inputs["record"]["analysis_source"]
    for field in ["square", "column_rank_order"]:
        assert original_input["key"][field] == inputs["key"][field]
    models = {}
    for name, path in [("book", args.book_model), ("radio", args.radio_model)]:
        if path:
            models[name] = load_model(path, old["model_sha256"][name])
    rows = list(candidates(inputs))
    assert len(rows) == len(old["rows"]) == old["candidates_completed"] == 8892
    max_error = 0.0
    for row, stored in zip(rows, old["rows"]):
        assert row == {k: v for k, v in stored.items() if k != "scores"}
        new_scores = {}
        for name, model in models.items():
            value = score(row["plaintext"], model)
            error = abs(value - stored["scores"][name])
            assert error < 1e-12
            max_error = max(max_error, error)
            new_scores[name] = value
        if new_scores:
            row["scores"] = new_scores
    inventory = json.loads((HERE / meta["header_inventory_path"]).read_text())
    headers = inventory["all_header_rows"]
    assert len(headers) == inventory["blocks_in_original_screen"] == 622
    selected = [r for r in headers if any(re.search(r"14[.: ]?10", h) for h in r["headers_ocr"])]
    assert selected == [{k: r[k] for k in ["block_id", "printed_page", "headers_ocr"]}
                        for r in inventory["selected_rows"]]
    assert {r["block_id"] for r in selected} == {"p132_ocr_block2", "p138_ocr_block3", "p177_ocr_block3"}
    if args.original_ocr_screen:
        assert sha(args.original_ocr_screen) == inventory["original_full_ocr_screen_sha256"]
        original = json.loads(args.original_ocr_screen.read_text())
        assert [{k: r[k] for k in ["block_id", "printed_page", "headers_ocr"]}
                for r in original["rows"]] == headers
    per_family = []
    for stage in ["transmitted", "interim"]:
        for mode in ["insert", "remove"]:
            family = [r for r in old["rows"] if r["stage"] == stage and r["mode"] == mode]
            per_family.append({"stage": stage, "mode": mode, "candidate_records": len(family)})
    assert [f["candidate_records"] for f in per_family] == [3816, 630, 3816, 630]
    tied = {}
    for name in ["book", "radio"]:
        best = max(r["scores"][name] for r in old["rows"])
        winners = [r for r in old["rows"] if r["scores"][name] == best]
        assert [(r["stage"], r["mode"], r["position"], r["source_R_fill"]) for r in winners] == [
            ("transmitted", "remove", 103, "F"), ("transmitted", "remove", 104, "F")]
        tied[name] = {"score": best, "candidates": winners}
    if args.output:
        assert set(models) == {"book", "radio"}, "Replay output requires both pinned models"
        assert args.output.resolve() != (HERE / meta["original_results_path"]).resolve()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({"inputs_sha256": sha(HERE / "inputs.json"),
                                          "candidate_records_completed": len(rows),
                                          "model_sha256": old["model_sha256"], "rows": rows}, indent=2) + "\n")
    result = {"verified": True, "candidate_records": len(rows), "score_evaluations_in_original": 17784,
              "geometric_locations": 422, "per_family": per_family,
              "original_top_ties": tied, "score_models_recomputed": sorted(models),
              "maximum_score_error": max_error, "ocr_header_rows_checked": len(headers),
              "same_time_inventory_block_ids": [r["block_id"] for r in selected],
              "limits": "Original scores and equal top ties are retained. Candidate counts include repeated fill-value witnesses, not unique plaintexts. The header inventory is bounded to the preserved 622-block OCR screen."}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
