#!/usr/bin/env python3
"""Verify the conditional p170 D-coordinate budget and its source binding.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
The default check needs only Python's standard library and repository files.
Add --cache to reproduce the descriptive book comparison (NumPy required).
No key, plaintext, missing coordinate or historical digit assignment is inferred.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt  # noqa: E402

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"
LENGTH = 53
BUDGET = 7
KEY_IDS = ("Nov7-9", "Nov10-12")


def read_json(path):
    return json.loads(path.read_text())


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def character_costs(square):
    """One D for row D, one for column D; DD costs two."""
    return {ch: int(i // 6 == 1) + int(i % 6 == 1)
            for i, ch in enumerate(square) if ch != "?"}


def verify_completions(partial):
    """Check all cells and independent encodings for every digit completion."""
    missing = sorted(set(ALPHABET) - set(partial))
    assert set(missing) <= set("0123456789")
    assert len(missing) == partial.count("?")
    letters = {ch: cost for ch, cost in character_costs(partial).items()
               if ch.isalpha() and cost}
    rng = random.Random(170106)
    body = ALPHABET + "".join(rng.choices(ALPHABET, k=LENGTH - len(ALPHABET)))
    trace = []
    for fill in itertools.permutations(missing):
        values = iter(fill)
        square = "".join(next(values) if ch == "?" else ch for ch in partial)
        assert len(square) == 36 and set(square) == set(ALPHABET)
        # Independent table traversal checks every single-character weight.
        pairs = dict(zip(square, itertools.product(COORDINATES, repeat=2)))
        costs = character_costs(square)
        assert all(pair.count("D") == costs[ch] for ch, pair in pairs.items())
        interim = "".join("".join(pairs[ch]) for ch in body)
        exact = sum(costs[ch] for ch in body)
        lower = sum(letters.get(ch, 0) for ch in body)
        assert interim.count("D") == exact and lower <= exact
        for width in (12, 17, 20):
            ranks = list(range(1, width + 1))
            rng.shuffle(ranks)
            columns = [interim[c::width] for c in range(width)]
            order = sorted(range(width), key=ranks.__getitem__)
            independent = "".join(columns[c] for c in order)
            assert independent == encrypt(body, ranks, square)
            assert independent.count("D") == exact
            directions = rng.randrange(1 << width)
            directed = "".join(columns[c][::-1] if directions >> c & 1
                               else columns[c] for c in order)
            assert Counter(directed) == Counter(interim)
            trace.append([square, ranks, directions, exact, lower, digest(directed)])
    count = len(trace) // 3
    return {
        "unassigned_symbols": "".join(missing),
        "complete_squares_checked": count,
        "single_character_coordinate_checks": 36 * count,
        "ordinary_rank_controls": len(trace),
        "independent_column_direction_controls": len(trace),
        "fresh_alphanumeric_control_length": len(body),
        "fresh_alphanumeric_control_sha256": digest(body),
        "control_trace_sha256": digest(json.dumps(trace, separators=(",", ":"))),
    }


def operational_reference(record_id, key, path, source, frame, body, coefficients):
    assert len(source) == len(frame)
    assert all(a == b for a, b in zip(source, frame) if a in COORDINATES)
    assert body == decrypt(frame, key["column_rank_order"], key["square"])
    values = [sum(coefficients.get(ch, 0) for ch in body[i:i + LENGTH])
              for i in range(len(body) - LENGTH + 1)]
    assert values
    return {
        "id": record_id,
        "key_id": key["id"],
        "certificate": str(path.relative_to(ROOT)),
        "source_literal_sha256": digest(source),
        "analysis_frame_sha256": digest(frame),
        "known_coordinate_substitutions": 0,
        "raw_plaintext": body,
        "raw_plaintext_sha256": digest(body),
        "window_length": LENGTH,
        "windows": len(values),
        "minimum_known_letter_D_cost": min(values),
        "maximum_known_letter_D_cost": max(values),
        "window_cost_sha256": digest(json.dumps(values, separators=(",", ":"))),
        "unresolved_character_policy": "Zero contribution; no editorial restoration.",
    }


def necessary_not_sufficient_example(keys, target):
    """A real numerical telegram window can pass D alone without matching p170."""
    path = ROOT / "experiments/nov4_repetition_and_connections/inputs.json"
    data = read_json(path)
    record = next(r for r in data["records"] if r["id"] == "p121_A1")
    source = "".join("".join(record["source_rows"]).split())
    native_key = keys["Nov4-6"]
    assert data["key"]["square"] == native_key["square"]
    assert data["key"]["column_rank_order"] == native_key["column_rank_order"]
    assert len(source) == record["source_slots"] == 236
    assert set(source) <= set(COORDINATES)
    raw = decrypt(source, native_key["column_rank_order"], native_key["square"])
    assert raw == record["expected_raw"]
    window = raw[:LENGTH]
    assert len(window) == LENGTH and "?" not in window
    key = keys["Nov10-12"]
    costs = character_costs(key["square"])
    ordinary = sum(costs.get(ch, 0) for ch in window if ch.isalpha())
    assert ordinary == BUDGET
    missing = sorted(set(ALPHABET) - set(key["square"]))
    target_counts = Counter(target)
    trace = []
    fd_digits = set()
    for fill in itertools.permutations(missing):
        it = iter(fill)
        square = "".join(next(it) if c == "?" else c for c in key["square"])
        pairs = dict(zip(square, itertools.product(COORDINATES, repeat=2)))
        independent = Counter(c for ch in window for c in pairs[ch])
        wire = encrypt(window, key["column_rank_order"], square)
        assert Counter(wire) == independent and len(wire) == len(target)
        # Equal-length strings need at least half their histogram L1 distance
        # in substitutions, independently of every coordinate permutation.
        difference = sum(abs(independent[c] - target_counts[c]) for c in COORDINATES)
        assert difference % 2 == 0
        trace.append([square, independent["D"], difference // 2,
                      [independent[c] for c in COORDINATES]])
        if independent["D"] == BUDGET:
            fd_digits.add(square[2 * 6 + 1])
    distribution = Counter(row[1] for row in trace)
    assert len(trace) == 120 and distribution == {7: 72, 8: 24, 10: 24}
    assert fd_digits == set("679")
    assert min(row[2] for row in trace) == 18
    return {
        "source_record": record["id"],
        "source_inputs": str(path.relative_to(ROOT)),
        "native_key_id": native_key["id"],
        "literal_source_sha256": digest(source),
        "native_raw_plaintext_sha256": digest(raw),
        "native_source_substitutions_or_fills": 0,
        "window_start": 0, "window_length": LENGTH,
        "unrestored_raw_window": window,
        "digits_in_window": sum(ch.isdigit() for ch in window),
        "comparison_square_id": key["id"],
        "ordinary_letter_D_cost": ordinary,
        "digit_completions_checked": len(trace),
        "full_D_count_distribution": {str(n): count for n, count in sorted(distribution.items())},
        "FD_digits_meeting_seven_Ds": "".join(sorted(fd_digits)),
        "completions_matching_all_six_p170_coordinate_counts": sum(row[2] == 0 for row in trace),
        "minimum_full_histogram_substitution_lower_bound": min(row[2] for row in trace),
        "control_trace_sha256": digest(json.dumps(trace, separators=(",", ":"))),
        "interpretation": "A selected actual telegram window with dates and reference digits illustrates that the D budget is necessary, not sufficient. The source was encrypted under Nov4–6; its hypothetical Nov10–12 encodings are not a p170 reading. Even the best complete-square choice differs from p170's full six-coordinate histogram by at least 18 substitutions. This selected example is not a probability estimate.",
    }


def core_record():
    messages = read_json(ROOT / "data/messages.json")["messages"]
    target = next(m for m in messages if m["id"] == "p170")
    transcript = target["transcript"]
    literal = "".join(transcript["raw_source_grouped"].split())
    assert literal == transcript["raw_source_compact"] == transcript["analysis_ciphertext"]
    assert len(literal) == 2 * LENGTH and set(literal) <= set(COORDINATES)
    assert literal.count("D") == BUDGET
    assert target["source"]["advertised_length"] is None
    assert target["source"]["handwritten_count"] == len(literal)
    assert (target["source"]["printed_page"], target["source"]["pdf_page_1based"],
            target["source"]["section"]) == (170, 173, "A")
    assert transcript["analysis_slots"] == transcript["known_adfgvx_coordinates"] == len(literal)
    assert transcript["uncertain_coordinates"] == 0
    keys = {k["id"]: k for k in read_json(ROOT / "data/keys.json")["keys"]}
    rows = []
    for key_id in KEY_IDS:
        square = keys[key_id]["square"]
        assert len(square) == 36
        known = [ch for ch in square if ch != "?"]
        assert len(known) == len(set(known)) and set(known) <= set(ALPHABET)
        costs = character_costs(square)
        rows.append({
            "key_id": key_id,
            "partial_square": square,
            "partial_square_sha256": digest(square),
            "ordinary_letter_D_coefficients": {
                ch: costs[ch] for ch in ALPHABET[:26] if costs.get(ch, 0)},
            "known_digit_D_coefficients": {
                ch: costs[ch] for ch in ALPHABET[26:] if costs.get(ch, 0)},
            "unassigned_D_cells": [COORDINATES[i // 6] + COORDINATES[i % 6]
                for i, ch in enumerate(square)
                if ch == "?" and (i // 6 == 1 or i % 6 == 1)],
            "ordinary_letter_D_budget": BUDGET,
            "validation": verify_completions(square),
        })
    p155_path = ROOT / "data/certificates/p155.json"
    p155 = next(s for s in read_json(p155_path)["sections"] if s["id"] == "p155_A1")
    p155_body = next(v for v in p155["variants"] if v["id"] == "p155_A1_received_geometry")["raw_plaintext"]
    p155_frame = "".join(ch if ch in COORDINATES else "?" for ch in p155["raw_literal"])
    p179_path = ROOT / "experiments/november_armistice_orders/certificates.json"
    p179 = next(r for r in read_json(p179_path)["records"] if r["id"] == "p179_B")
    assert p179["key_id"] == "Nov10-12"
    assert p179["source_literal"] == p179["analysis_frame"]
    references = read_json(HERE / "heldout_sources.json")["sources"]
    training = read_json(ROOT / "experiments/joint_search/models/provenance.json")["sources"]
    assert not {s["id"] for s in references} & {s["id"] for s in training}
    return {
        "schema": "adfgvx-p170-coordinate-budget-v1",
        "prepared_by": "icekylinx and GPT-6 Astra Pro",
        "source": {
            "catalog_id": "p170", "section": "A", "printed_page": 170,
            "pdf_page_1based": 173,
            "header": target["source"]["header_transcription"],
            "literal_grouped": transcript["raw_source_grouped"],
            "literal_compact": literal, "literal_sha256": digest(literal),
            "coordinate_counts": {ch: literal.count(ch) for ch in COORDINATES},
            "received_coordinates": len(literal), "uncertain_slots": 0,
            "transmitted_numeric_length": None, "handwritten_count": len(literal),
        },
        "conditional_scope": "Exactly these 106 received coordinates as a complete 53-character ADFGVX body, with no substitutions and the specified square. Every width, rank order, independent column direction, pair reversal and unassigned digit completion preserves the count constraint.",
        "proof": "A character contributes one D in row D, one in column D, and two at DD. Any coordinate permutation preserves their total of seven. Omitting nonnegative digit contributions gives the ordinary-letter inequalities.",
        "keys": rows,
        "operational_references": [
            operational_reference("p155_A1", keys[KEY_IDS[0]], p155_path,
                p155["raw_literal"], p155_frame, p155_body,
                rows[0]["ordinary_letter_D_coefficients"]),
            operational_reference("p179_B", keys[KEY_IDS[1]], p179_path,
                p179["source_literal"], p179["analysis_frame"], p179["raw"]["plaintext"],
                rows[1]["ordinary_letter_D_coefficients"]),
        ],
        "necessary_not_sufficient_example": necessary_not_sufficient_example(keys, literal),
        "heldout_sources": references,
        "reference_method": "All 53-character sliding windows, stride one, separately within each pinned book and each plain or sentence_x normalization from p73_histogram.py. Only known ordinary-letter D costs are counted. No windows cross books; overlapping or differently normalized windows are not independent evidence.",
        "interpretation": "A necessary check for proposed readings and a reason to lower the priority of a complete ordinary-German body under these two squares. No key is excluded; no truncation, plaintext or digit assignment is established. Another square, truncation, unusual vocabulary, extensive numerals, code traffic or another language remains possible. Book comparisons are descriptive, not p-values.",
    }


def book_results(core, cache, download):
    from p73_histogram import normalized_streams, source_text
    rows = []
    for source in core["heldout_sources"]:
        text = source_text(source, cache, download)
        for convention, stream in normalized_streams(text):
            if convention == "word_x":
                continue
            for key in core["keys"]:
                coefficients = key["ordinary_letter_D_coefficients"]
                costs = [coefficients.get(ch, 0) for ch in stream]
                running = sum(costs[:LENGTH])
                minimum, at_most = running, int(running <= BUDGET)
                for left in range(len(costs) - LENGTH):
                    running += costs[left + LENGTH] - costs[left]
                    minimum = min(minimum, running)
                    at_most += running <= BUDGET
                rows.append({
                    "key_id": key["key_id"], "book_id": source["id"],
                    "convention": convention,
                    "normalized_characters": len(stream),
                    "normalized_sha256": digest(stream),
                    "window_length": LENGTH, "window_stride": 1,
                    "windows": len(stream) - LENGTH + 1,
                    "minimum_ordinary_letter_D_cost": minimum,
                    "windows_at_most_seven": at_most,
                })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", type=Path, default=HERE / "p170_coordinate_budget.json")
    parser.add_argument("--cache", type=Path, help="Pinned Gutenberg book cache; rerun all book windows.")
    parser.add_argument("--download", action="store_true", help="Download missing pinned books to --cache.")
    parser.add_argument("--output", type=Path, help="Write a regenerated full record; requires --cache.")
    args = parser.parse_args()
    if (args.download or args.output) and not args.cache:
        parser.error("--download and --output require --cache")
    result = core_record()
    if args.cache:
        result["reference_results"] = book_results(result, args.cache, args.download)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    else:
        expected = read_json(args.verify)
        if not args.cache:
            expected.pop("reference_results")
        assert result == expected, "Recorded result differs from independent replay"
    print("p170 source, square coefficients, all 122 digit completions, operational references, and D-budget counterexample: verified.")
    print("Held-out book windows: " + ("recomputed and verified." if args.cache and not args.output
          else "recomputed." if args.cache else "not rerun; add --cache to reproduce them."))


if __name__ == "__main__":
    main()
