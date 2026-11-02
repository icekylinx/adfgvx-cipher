#!/usr/bin/env python3
"""Certify the single adjacent-coordinate repair of p187b's two word garbles.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
The normalized words were already published by Norbert in 2017. This audit
locates their exact source-coordinate cost without assigning unknown cells.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def source_map(length, ranks):
    """Map the row-written coordinate stream back to received positions."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    received_order = [
        written
        for column in sorted(range(width), key=ranks.__getitem__)
        for written in range(column, length, width)
    ]
    inverse = [None] * length
    for received, written in enumerate(received_order):
        inverse[written] = received
    assert sorted(inverse) == list(range(length))
    return inverse


def decode(ciphertext, square, mapping):
    stream = "".join(ciphertext[i] for i in mapping)
    pairs = [stream[i:i + 2] for i in range(0, len(stream), 2)]
    return "".join(square[6 * COORDS.index(p[0]) + COORDS.index(p[1])] for p in pairs), pairs


def encode(plaintext, square, mapping):
    assert len(set(square)) == 36 and set(square) == set(ALPHABET)
    inverse = {c: COORDS[i // 6] + COORDS[i % 6] for i, c in enumerate(square)}
    stream = "".join(inverse[c] for c in plaintext)
    ciphertext = [None] * len(stream)
    for written, received in enumerate(mapping):
        ciphertext[received] = stream[written]
    return "".join(ciphertext)


def compute():
    messages = json.loads((ROOT / "data/messages.json").read_text())["messages"]
    keys = json.loads((ROOT / "data/keys.json").read_text())["keys"]
    message = next(m for m in messages if m["id"] == "p187b")
    key = next(k for k in keys if k["id"] == "CHI-Nov13")
    source = message["transcript"]["analysis_ciphertext"]
    ranks, square = key["column_rank_order"], key["square"]
    assert source == message["transcript"]["raw_source_compact"]
    assert len(source) == 142 and len(square) == 36
    mapping = source_map(len(source), ranks)
    raw, raw_pairs = decode(source, square, mapping)
    expected = raw.replace("NITHTARBEICET", "NICHTARBEITET")
    assert expected != raw and len(expected) == len(raw) == 71
    matches = []
    checks = []
    for left in range(len(source) - 1):
        candidate = source[:left] + source[left:left + 2][::-1] + source[left + 2:]
        text, _ = decode(candidate, square, mapping)
        checks.append({"left_received_index": left, "matches_full_partial_reading": text == expected})
        if text == expected:
            matches.append(left)
    assert matches == [128]
    left = matches[0]
    repaired = source[:left] + source[left:left + 2][::-1] + source[left + 2:]
    text, repaired_pairs = decode(repaired, square, mapping)
    changes = []
    for pos, (before, after) in enumerate(zip(raw, text)):
        if before != after:
            changes.append({
                "plaintext_position_zero_based": pos,
                "raw": before, "repaired": after,
                "raw_digraph": raw_pairs[pos], "repaired_digraph": repaired_pairs[pos],
                "received_coordinate_indices_zero_based": mapping[2 * pos:2 * pos + 2],
            })
    assert [(r["plaintext_position_zero_based"], r["raw"], r["repaired"]) for r in changes] == [(27, "T", "C"), (35, "C", "T")]
    assert [i for i, (a, b) in enumerate(zip(source, repaired)) if a != b] == [128, 129]
    assert sorted(source) == sorted(repaired)
    assert text.count("?") == raw.count("?") == 7

    # A complete square is used only to check the mechanical roundtrip. The
    # evidence and both repaired letters use known cells, so the argument is
    # unchanged by any bijective assignment of the fourteen unknown cells.
    remaining = iter(c for c in ALPHABET if c not in square)
    complete_square = "".join(next(remaining) if c == "?" else c for c in square)
    for ciphertext in (source, repaired):
        complete_text, _ = decode(ciphertext, complete_square, mapping)
        assert encode(complete_text, complete_square, mapping) == ciphertext
    payload = {
        "schema": "adfgvx-p187b-adjacent-swap-v1",
        "prepared_by": "icekylinx and GPT-6 Astra Pro",
        "date": "2026-11-02",
        "scope": "Fixed published CHI-Nov13 ranks and attested square cells; no language model, no new cell assignments.",
        "index_convention": "All indices are zero-based unless explicitly labeled.",
        "prior_plaintext_credit": {
            "author": "Norbert", "date": "2017-05-03", "comment": 53,
            "url": "https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-878079",
        },
        "source": {
            "message_id": "p187b", "printed_page": 187, "pdf_page_1based": 190,
            "received_coordinates": len(source), "ciphertext": source,
            "ciphertext_sha256": hashlib.sha256(source.encode()).hexdigest(),
        },
        "key": {"id": key["id"], "ranks": ranks, "partial_square": square},
        "raw_partial_reading": raw,
        "conditional_partial_reading": text,
        "adjacent_swap": {
            "received_indices_zero_based": [128, 129],
            "received_positions_one_based": [129, 130],
            "printed_group_number_one_based": 26,
            "printed_group": source[125:130],
            "repaired_group": repaired[125:130],
            "before": "AD", "after": "DA",
            "known_coordinate_substitutions_if_counted_separately": 2,
            "unchanged_coordinates": 140,
            "coordinate_histogram_unchanged": True,
        },
        "conditional_ciphertext": repaired,
        "changed_plaintext_positions": changes,
        "fixed_plaintext_positions_before_and_after": 64,
        "total_plaintext_positions": 71,
        "unresolved_plaintext_positions": [i for i, c in enumerate(raw) if c == "?"],
        "exhaustive_adjacent_swap_check": {
            "tested": len(checks), "matches": matches,
            "checks_sha256": hashlib.sha256(json.dumps(checks, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "uniqueness_scope": "Only among the 141 single adjacent swaps under this fixed key, requiring the entire stated partial reading.",
        },
        "verification": {
            "raw_and_repaired_complete_witness_roundtrips": True,
            "arbitrary_completion_is_not_historical_evidence": True,
            "all_unknown_square_completions_leave_the_two_repairs_unchanged": True,
        },
        "limitations": [
            "The printed AD is retained as received evidence; DA is an editorial transposition hypothesis.",
            "This does not identify where the historical error arose or establish that it was a transcription error.",
            "No new plaintext priority is claimed for the words already normalized by Norbert.",
            "The seven unresolved ending positions and fourteen unassigned square cells remain unresolved.",
        ],
    }
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = compute()
    path = HERE / "result.json"
    if args.verify:
        assert json.loads(path.read_text()) == result, "Recorded certificate differs from recomputation"
    else:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print("PASS: 141 adjacent swaps checked; only 128/129 repairs both words; 64/71 positions remain fixed.")


if __name__ == "__main__":
    main()
