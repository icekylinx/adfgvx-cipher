#!/usr/bin/env python3
"""Propagate one conditional Nov25 letter assignment without assigning numerals.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Published key: Lasry, Niebel, Kopal and Wacker. Standard library only.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse_indices(length, ranks):
    """Source positions in the original row-filled coordinate sequence."""
    ordered = [i for c in sorted(range(len(ranks)), key=lambda c: ranks[c])
               for i in range(c, length, len(ranks))]
    inverse = [None] * length
    for source, plain in enumerate(ordered):
        inverse[plain] = source
    return inverse


def read(cipher, ranks, square):
    assert len(cipher) % 2 == 0
    inverse = inverse_indices(len(cipher), ranks)
    unused = set(ALPHABET) - (set(square) - {"?"})
    positions = []
    for p in range(0, len(cipher), 2):
        indices = inverse[p:p + 2]
        pair = "".join(cipher[i] for i in indices)
        cells = [6 * r + c for r in range(6) for c in range(6)
                 if pair[0] in ("?", CO[r]) and pair[1] in ("?", CO[c])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == "?" else square[cell])
        assert domain
        positions.append({"index": p // 2, "pair": pair,
                          "frame_indices": indices, "cells": cells,
                          "domain": "".join(sorted(domain))})
    return {"plaintext": "".join(p["domain"] if len(p["domain"]) == 1 else "?"
                                 for p in positions), "positions": positions}


def encipher(plaintext, ranks, square):
    coords = "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6]
                     for c in plaintext)
    return "".join(coords[c::len(ranks)]
                   for c in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def witness(cipher, ranks, partial):
    missing = iter(sorted(set(ALPHABET) - (set(partial) - {"?"})))
    square = "".join(next(missing) if c == "?" else c for c in partial)
    assert len(square) == len(set(square)) == 36
    filled = cipher.replace("?", "A")
    plaintext = read(filled, ranks, square)["plaintext"]
    assert encipher(plaintext, ranks, square) == filled
    partial_domains = read(cipher, ranks, partial)["positions"]
    assert all(c in p["domain"] for c, p in zip(plaintext, partial_domains))
    return {"square": square, "ciphertext": filled, "plaintext": plaintext,
            "is_proposed_original_plaintext": False}


def normalized_records(manifest):
    records = []
    for source in manifest["sources"]:
        data = json.loads((ROOT / source["certificate"]).read_text())
        pool = {r["id"]: r for r in data.get("records", data.get("messages", []))}
        for record_id in source["record_ids"]:
            r = pool[record_id]
            if source["adapter"] == "corpus_readings":
                raw = r["direct_reading_under_stated_geometry"]
                edition = r["editorial_same_length_candidate"]
                rec = {"id": record_id, "literal": r["literal_ciphertext"],
                       "ciphertext": r["geometry"]["frame_ciphertext"],
                       "mapping": r["geometry"]["original_source_index_for_frame_index"],
                       "raw": raw["plaintext"],
                       "edition_ciphertext": edition["reencrypted_ciphertext"],
                       "edition": edition["plaintext"]}
            elif source["adapter"] == "source_editions":
                edition = r["readable_candidate"]
                rec = {"id": record_id, "literal": r["literal_source"],
                       "ciphertext": r["ciphertext"], "mapping": r["model_to_source_indices"],
                       "raw": r["raw"], "edition_ciphertext": edition["ciphertext"],
                       "edition": edition["raw"]}
            elif source["adapter"] == "liman":
                rec = {"id": record_id, "literal": r["source_literal"],
                       "ciphertext": r["source_literal"],
                       "mapping": list(range(r["source_slots"])),
                       "raw": r["raw_plaintext"],
                       "edition_ciphertext": r["editorial_ciphertext"],
                       "edition": r["editorial_plaintext"]}
            elif source["adapter"] == "mackensen_appeal":
                mapping = [None] * len(r["analysis_frame"])
                covered = set()
                for p in r["positions"]:
                    for frame, original in zip(p["working_coordinate_indices"],
                                               p["source_coordinate_indices"]):
                        assert frame not in covered
                        covered.add(frame)
                        mapping[frame] = original
                assert covered == set(range(len(mapping)))
                rec = {"id": record_id, "literal": r["source_literal"],
                       "ciphertext": r["analysis_frame"], "mapping": mapping,
                       "raw": r["raw_plaintext"],
                       "edition_ciphertext": r["editorial_ciphertext"],
                       "edition": r["editorial_plaintext"]}
            else:
                raise ValueError(source["adapter"])
            rec["certificate"] = source["certificate"]
            records.append(rec)
    assert len({r["id"] for r in records}) == len(records)
    return sorted(records, key=lambda r: r["id"])


def run():
    manifest = json.loads((HERE / "inputs.json").read_text())
    for dep in manifest["dependencies"]:
        assert sha(ROOT / dep["path"]) == dep["sha256"], dep["path"]
    key = manifest["key"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    square, ranks = key["square"], key["column_rank_order"]
    assert square == published["square"] and ranks == published["column_rank_order"]
    assert set(square) == set(ALPHABET) and len(square) == 36
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    ambiguous = manifest["hypothesis"]["cleared_baseline_labels"]
    assert set(ambiguous) == set("0123456789JQY")
    partial = ["?" if c in ambiguous else c for c in square]
    cell = 6 * CO.index("V") + CO.index("D")
    assert square[cell] == "9"
    partial[cell] = "J"
    partial = "".join(partial)
    assert len(set(partial) - {"?"}) == 24 and partial.count("?") == 12
    remaining = "".join(sorted(set(ALPHABET) - (set(partial) - {"?"})))
    assert remaining == "0123456789QY"
    assert partial[square.index("J")] == "?"
    records, raw9 = [], []
    label_counts = {"raw": Counter(), "edition": Counter()}
    totals = Counter()
    for rec in normalized_records(manifest):
        assert len(rec["ciphertext"]) == len(rec["edition_ciphertext"]) == len(rec["mapping"])
        assert len(rec["mapping"]) % 2 == 0
        assert len([i for i in rec["mapping"] if i is not None]) == len(set(i for i in rec["mapping"] if i is not None))
        for i, source in enumerate(rec["mapping"]):
            expected = "?" if source is None or rec["literal"][source] not in CO else rec["literal"][source]
            assert rec["ciphertext"][i] == expected, (rec["id"], i)
        previous_edits = [{"frame_index": i, "source_index": rec["mapping"][i],
                           "from": a, "to": b,
                           "kind": "erasure_fill" if a == "?" else "known_coordinate_substitution"}
                          for i, (a, b) in enumerate(zip(rec["ciphertext"], rec["edition_ciphertext"])) if a != b]
        out = {"id": rec["id"], "source_certificate": rec["certificate"],
               "literal_source": rec["literal"], "frame_to_source_indices": rec["mapping"],
               "earlier_edition_coordinate_changes": previous_edits,
               "additional_coordinate_edits_for_this_overlay": 0,
               "views": {}}
        totals["source_records"] += 1
        totals["plaintext_positions"] += len(rec["raw"])
        totals["source_slots"] += len(rec["literal"])
        for view, field in [("raw", "ciphertext"), ("edition", "edition_ciphertext")]:
            cipher = rec[field]
            baseline = read(cipher, ranks, square)
            assert baseline["plaintext"] == rec[view], (rec["id"], view)
            overlay = read(cipher, ranks, partial)
            inventory, possible = [], []
            for bp, op in zip(baseline["positions"], overlay["positions"]):
                i = bp["index"]
                pair = bp["pair"]
                entry = {"plaintext_index": i, "coordinate_pair": pair,
                         "frame_indices": bp["frame_indices"],
                         "source_indices": [rec["mapping"][j] for j in bp["frame_indices"]],
                         "baseline_domain": bp["domain"], "overlay_domain": op["domain"],
                         "baseline_context": rec[view][max(0, i - 16):i + 17],
                         "affected_by_previous_edition": any(rec["ciphertext"][j] != rec["edition_ciphertext"][j]
                                                            for j in bp["frame_indices"])}
                if len(bp["domain"]) == 1 and bp["domain"] in ambiguous:
                    inventory.append(entry)
                    label_counts[view][bp["domain"]] += 1
                elif len(bp["domain"]) > 1 and set(bp["domain"]) & set(ambiguous):
                    possible.append(entry)
                if view == "raw" and bp["domain"] == "9":
                    edition_pair = "".join(rec["edition_ciphertext"][j] for j in bp["frame_indices"])
                    raw9.append({"record_id": rec["id"], **entry,
                                 "conditional_raw_context": overlay["plaintext"][max(0, i - 16):i + 17],
                                 "previous_edition_label": rec["edition"][i],
                                 "previous_edition_pair": edition_pair,
                                 "previous_edition_coordinate_changes_at_this_position": [c for c in previous_edits if c["frame_index"] in bp["frame_indices"]]})
            out["views"][view] = {"ciphertext": cipher,
                                   "baseline_plaintext": baseline["plaintext"],
                                   "conditional_plaintext": overlay["plaintext"],
                                   "conditional_domains": [p["domain"] for p in overlay["positions"]],
                                   "all_definite_digit_J_Q_Y_occurrences": inventory,
                                   "erased_pairs_with_possible_digit_J_Q_Y": possible,
                                   "baseline_witness": witness(cipher, ranks, square),
                                   "conditional_global_witness": witness(cipher, ranks, partial)}
        records.append(out)
    assert [r["id"] for r in records] == sorted(manifest["coverage_snapshot"]["selected_record_ids"])
    anchors = manifest["hypothesis"]["lexical_anchors"]
    anchor_keys = {(a["record_id"], a["plaintext_index"]) for a in anchors}
    observed_keys = {(r["record_id"], r["plaintext_index"]) for r in raw9}
    assert anchor_keys <= observed_keys
    for item in raw9:
        key_id = (item["record_id"], item["plaintext_index"])
        if key_id in anchor_keys:
            anchor = next(a for a in anchors if (a["record_id"], a["plaintext_index"]) == key_id)
            record = next(r for r in records if r["id"] == item["record_id"])
            text = record["views"]["raw"]["baseline_plaintext"]
            start = anchor["word_start"]
            assert text[start:start + len(anchor["raw_word"])] == anchor["raw_word"]
            after = record["views"]["raw"]["conditional_plaintext"]
            assert after[start:start + len(anchor["interpreted_word"])] == anchor["interpreted_word"]
            assert not item["affected_by_previous_edition"]
            item["assessment"] = "lexical_anchor_used_to_propose_the_hypothesis_not_a_held_out_test"
        else:
            assert item["previous_edition_label"] in ("E", "S")
            item["assessment"] = "inconvenient_raw_occurrence_preexisting_source_repair_retained_separately"
    assert len(raw9) == manifest["expected_counts"]["raw9_occurrences"]
    assert len(anchor_keys) == manifest["expected_counts"]["lexical_anchors"]
    assert len(records) == manifest["expected_counts"]["reviewed_records"]
    counts = {k: dict(sorted(v.items())) for k, v in label_counts.items()}
    return {"schema": "adfgvx-nov25-letter-constraint-certificate-v1",
            "prepared_by": manifest["prepared_by"], "input_sha256": sha(HERE / "inputs.json"),
            "coverage_snapshot": manifest["coverage_snapshot"],
            "baseline_square": square, "conditional_partial_square": partial,
            "released_baseline_labels": ambiguous, "remaining_cell_domain": remaining,
            "unassigned_cells": partial.count("?"),
            "globally_bijective_square_completions": math.factorial(partial.count("?")),
            "summary": {**dict(totals), "raw9_observed_occurrences": len(raw9),
                        "lexical_anchors": len(anchors), "clean_held_out_raw9_occurrences": 0,
                        "inconvenient_raw9_occurrences": len(raw9) - len(anchors),
                        "additional_coordinate_edits": 0,
                        "raw_definite_digit_J_Q_Y_occurrences": sum(label_counts["raw"].values()),
                        "edition_definite_digit_J_Q_Y_occurrences": sum(label_counts["edition"].values()),
                        "per_view_label_counts": counts},
            "all_observed_raw9_occurrences": raw9, "records": records,
            "limits": manifest["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = run()
    target = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
