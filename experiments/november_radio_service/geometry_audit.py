#!/usr/bin/env python3
"""Audit odd-block retrieval and p132 B's two phase-change families.

Prepared by icekylinx and GPT-6 Astra Pro. Default verification checks all
strings, source witnesses, source hashes and retrospective template costs.
Optional model paths also recompute the frozen book/radio scores.
"""
import argparse
from array import array
import json
from pathlib import Path
import sys

from verify import HERE, CO, encode, inverse, reading, sha, transpose

ROOT = HERE.parents[1]
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def labels(stream, square):
    assert len(stream) % 2 == 0
    return "".join(square[6 * CO.index(a) + CO.index(b)] if a in CO and b in CO else "?"
                   for a, b in zip(stream[::2], stream[1::2]))


def score(text, model):
    vals = [ABC.index(char) for char in text]
    return sum(model[((a * 37 + b) * 37 + c) * 37 + d]
               for a, b, c, d in zip(vals, vals[1:], vals[2:], vals[3:])) / (len(text) - 3)


def load_models(args, snapshot):
    models = {}
    for name, path in [("book", args.book_model), ("radio", args.radio_model)]:
        if path is None:
            continue
        assert sha(path) == snapshot["models"][name]["sha256"]
        values = array("f")
        values.frombytes(path.read_bytes())
        if sys.byteorder != "little":
            values.byteswap()
        assert len(values) == 37 ** 4
        models[name] = values
    return models


def source_candidates(inputs):
    rec = next(r for r in inputs["records"] if r["id"] == "p132_B")
    key = next(k for k in inputs["keys"] if k["id"] == rec["key_id"])
    source = rec["analysis_source"]
    interim, origins = inverse(source, key["column_rank_order"])
    rows, prices = [], []
    encoded = encode(rec["editorial_text"], key["square"])
    for kind in ["insert_unknown", "remove_extra"]:
        for position in range(len(interim) + (kind == "insert_unknown")):
            modified = (interim[:position] + "?" + interim[position:] if kind == "insert_unknown"
                        else interim[:position] + interim[position + 1:])
            raw = labels(modified, key["square"])
            rows.append({"kind": kind, "interim_index": position,
                         "removed_coordinate": interim[position] if kind == "remove_extra" else None,
                         "plaintext": raw})
            if kind == "remove_extra":
                # Reinsert the same received coordinate before transposition;
                # it remains charged as an extraneous coordinate, not discarded.
                reconstructed = encoded[:position] + interim[position] + encoded[position:]
                witness = transpose(reconstructed, key["column_rank_order"])
                prices.append({"interim_removal_index": position,
                               "retained_source_index": origins[position],
                               "retained_coordinate": interim[position],
                               "known_coordinate_substitutions": sum(a != "?" and a != b
                                                                       for a, b in zip(source, witness)),
                               "source_erasure_fills": source.count("?"),
                               "extra_interim_coordinates": 1})
    assert len(rows) == 311 and len(prices) == 155
    minimum = min(p["known_coordinate_substitutions"] for p in prices)
    indices = [p["interim_removal_index"] for p in prices if p["known_coordinate_substitutions"] == minimum]
    assert minimum == 3 and indices == [54, 55, 56, 57]
    assert len({r["plaintext"] for r in rows if r["kind"] == "remove_extra" and r["interim_index"] in indices}) == 1
    return rows, prices, {"minimum_substitutions": minimum, "all_tied_indices": indices}


def verify_retrieval(snapshot, models):
    folder = HERE / "retrieval"
    provenance = json.loads((folder / "provenance.json").read_text())
    for field, path in [("original_driver_sha256", folder / "original_driver.py"),
                        ("original_results_sha256", folder / "original_results.json"),
                        ("selected_inputs_sha256", folder / "selected_inputs.json"),
                        ("key_and_model_snapshot_sha256", ROOT / provenance["key_and_model_snapshot"]),
                        ("engine_source_sha256", ROOT / provenance["engine_source"])]:
        assert sha(path) == provenance[field]
    selected = json.loads((folder / "selected_inputs.json").read_text())
    old = json.loads((folder / "original_results.json").read_text())
    assert selected["source_sha256"] == provenance["original_source_sha256"] == old["input_source_sha256"]
    sources = {row["block_id"]: row for row in selected["rows"]}
    assert len(sources) == old["blocks"] == 216
    assert old["completed_jobs"] == len(old["results"]) == 864
    keys = {key["id"]: key for key in snapshot["historical"]["frozen_keys"]}
    expected = {(row["block_id"], keyid, model) for row in sources.values()
                for keyid in [row["best"]["key"], row["runner_up"]["key"]] for model in ["book", "radio"]}
    assert {(r["block_id"], r["key_id"], r["model"]) for r in old["results"]} == expected
    selected_p132 = []
    for row in old["results"]:
        source, key = sources[row["block_id"]], keys[row["key_id"]]
        assert source["source_slots"] % 2 and 55 <= source["source_slots"] <= 700
        assert row["ciphertext"] == source["ciphertext"]
        interim, _ = inverse(row["ciphertext"], key["column_rank_order"])
        assert labels(interim[:-1], key["square"]) == row["unmodified_raw"]
        assert row["unpaired_coordinate"] == interim[-1]
        result = row["result"]
        assert result["completed"] and len(result["missing_interim_indices"]) == 1
        gap = result["missing_interim_indices"][0]
        complete = result["full_interim"]
        assert len(complete) == len(interim) + 1
        remaining = complete[:gap] + complete[gap + 1:]
        assert all(a == "?" or a == b for a, b in zip(interim, remaining))
        assert labels(complete, key["square"]) == result["plaintext"]
        if row["model"] in models:
            model = models[row["model"]]
            assert abs(score(row["unmodified_raw"], model) - row["baseline_mean"]) < 1e-9
            assert abs(score(result["plaintext"], model) - result["score_mean"]) < 1e-9
        if row["block_id"] == "p132_ocr_block2" and row["key_id"] == "Nov4-6":
            selected_p132.append({"model": row["model"], "interim_insertion": gap,
                                  "plaintext": result["plaintext"], "status": "Unreviewed OCR-based insertion candidate, superseded by a separately conditional source extra-coordinate edition."})
    return {"blocks": 216, "completed_jobs": 864,
            "states_expanded": sum(r["result"]["states_expanded"] for r in old["results"]),
            "transitions_evaluated": sum(r["result"]["transitions_evaluated"] for r in old["results"]),
            "p132_original_insertion_candidates": selected_p132,
            "all_results_remain_retrieval_candidates": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    snapshot = json.loads((ROOT / "experiments/p198_pretransposition_loss/inputs.json").read_text())
    models = load_models(args, snapshot)
    rows, prices, minimum = source_candidates(inputs)
    retrieval = verify_retrieval(snapshot, models)
    path = HERE / "geometry_audit.json"
    if args.verify:
        saved = json.loads(path.read_text())
        assert saved["inputs_sha256"] == sha(HERE / "inputs.json")
        assert saved["template_prices"] == prices and saved["conditional_template_minimum"] == minimum
        assert saved["retrieval_review"] == retrieval
        assert len(rows) == len(saved["source_candidates"])
        for row, stored in zip(rows, saved["source_candidates"]):
            assert row == {k: v for k, v in stored.items() if k != "scores"}
            for name, model in models.items():
                assert abs(score(row["plaintext"], model) - stored["scores"][name]) < 1e-12
    else:
        assert set(models) == {"book", "radio"}, "Both model paths are needed to create the score archive"
        for row in rows:
            row["scores"] = {name: score(row["plaintext"], model) for name, model in models.items()}
        saved = {"schema": "adfgvx-p132-B-extra-interim-coordinate-audit-v1",
                 "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
                 "source_candidate_count": len(rows), "source_candidates": rows,
                 "template_prices": prices, "conditional_template_minimum": minimum,
                 "retrospective_template": inputs["records"][1]["editorial_text"],
                 "model_sha256": {name: item["sha256"] for name, item in snapshot["models"].items()},
                 "retrieval_review": retrieval,
                 "limits": ["The one-insertion retrieval nominated a useful phase boundary; it did not identify the extra-coordinate mechanism.",
                            "The four equivalent V removals and the later editorial template are conditioned on source inspection and readable wording.",
                            "The language scores are heuristics; no unique historical error or broad exclusion is established."]}
        path.write_text(json.dumps(saved, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "source_candidates": len(rows),
                      "retrospective_template_positions": len(prices),
                      "conditional_minimum": minimum, "retrieval_jobs": retrieval["completed_jobs"],
                      "score_models_recomputed": sorted(models)}, indent=2))


if __name__ == "__main__":
    main()
