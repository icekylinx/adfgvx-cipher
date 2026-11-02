#!/usr/bin/env python3
"""Exact shared-cell and semantic-domain follow-up for the p153 recovery.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Only the received strings, recovered ranks and conservative square are input
evidence. Decimal dates, chronology and the footer separator remain separate
assumptions. No optimizer labels are accepted as historical numerals.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
_MAP_CACHE = {}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def source_map(length, ranks):
    """Map each row-written coordinate to its received coordinate index."""
    cache_key = length, tuple(ranks)
    if cache_key in _MAP_CACHE:
        return _MAP_CACHE[cache_key]
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    columns = [list(range(col, length, width)) for col in range(width)]
    received_order = []
    for column in sorted(range(width), key=ranks.__getitem__):
        received_order.extend(columns[column])
    inverse = [None] * length
    for received, written in enumerate(received_order):
        inverse[written] = received
    assert sorted(inverse) == list(range(length))
    _MAP_CACHE[cache_key] = inverse
    return inverse


def decipher(ciphertext, ranks, square):
    assert len(ciphertext) % 2 == 0
    mapping = source_map(len(ciphertext), ranks)
    stream = "".join(ciphertext[index] for index in mapping)
    return "".join(
        "?" if "?" in stream[i:i+2] else square[6 * COORDS.index(stream[i]) + COORDS.index(stream[i+1])]
        for i in range(0, len(stream), 2)
    )


def encipher(plaintext, ranks, square):
    assert len(square) == len(set(square)) == 36 and set(square) == set(ALPHABET)
    inverse = {letter: COORDS[i // 6] + COORDS[i % 6] for i, letter in enumerate(square)}
    stream = "".join(inverse[letter] for letter in plaintext)
    result = [None] * len(stream)
    for written, received in enumerate(source_map(len(stream), ranks)):
        result[received] = stream[written]
    return "".join(result)


def complete(square):
    remaining = iter(letter for letter in ALPHABET if letter not in square)
    return "".join(next(remaining) if letter == "?" else letter for letter in square)


def date_assignments(*, nonfuture, no_leading_zero):
    """Enumerate declared decimal interpretations; leading zero is optional."""
    values = []
    for alpha, beta, gamma, delta in itertools.permutations("0123456789", 4):
        day, month = int(alpha), int(beta + beta)
        if not (1 <= day <= 9 and 1 <= month <= 12):
            continue
        if nonfuture and (month, day) > (11, 8):
            continue
        if no_leading_zero and gamma == "0":
            continue
        values.append({"day": day, "month": month, "serial": gamma + delta + gamma})
    return values


def reuse_obstruction(core, other, transpose):
    """A two-letter invariant disproves row/column relabeling compatibility."""
    target = {ch: divmod(i, 6) for i, ch in enumerate(core) if ch != "?"}
    source = {ch: divmod(i, 6) for i, ch in enumerate(other) if ch != "?"}
    for left, right in itertools.combinations(sorted(target.keys() & source.keys()), 2):
        for axis in (0, 1):
            target_equal = target[left][axis] == target[right][axis]
            source_equal = source[left][axis ^ transpose] == source[right][axis ^ transpose]
            if target_equal != source_equal:
                return {
                    "letters": [left, right],
                    "target_axis": ["row", "column"][axis],
                    "compared_source_axis": ["row", "column"][axis ^ transpose],
                    "target_cells": [list(target[left]), list(target[right])],
                    "source_cells": [list(source[left]), list(source[right])],
                    "equal_in_target": target_equal,
                    "equal_in_source": source_equal,
                }
    return None


def footer_triples(square):
    """Union over all bijective completions, preserving shared unknown cells."""
    unused = [letter for letter in ALPHABET if letter not in square]
    assert len(unused) == 12 and square[0] == square[28] == "?"
    triples = set()
    for first, middle in itertools.permutations(unused, 2):
        local = list(square)
        local[0], local[28] = first, middle
        row = local[:6]
        column = [local[6*r+4] for r in range(6)]
        assert "?" not in row and "?" not in column
        triples.update("".join(t) for t in itertools.product(row, column, row))
    return triples


def analyze():
    cert = json.loads((ROOT / "data/certificates/p153.json").read_text())
    keys = json.loads((ROOT / "data/keys.json").read_text())["keys"]
    ranks, core = cert["ranks"], cert["core_partial_square"]
    ciphertexts = cert["ciphertexts"]
    assert [decipher(ct, ranks, core) for ct in ciphertexts] == cert["core_decodes"]

    maps = [source_map(len(ct), ranks) for ct in ciphertexts]
    for m, records in enumerate(cert["source_coordinate_maps"]):
        for record in records:
            p = record["plaintext_position"]
            assert maps[m][2*p:2*p+2] == record["received_coordinate_positions"]

    tail = []
    for p in range(42, 54):
        source_indices = maps[1][2*p:2*p+2]
        pair = "".join(ciphertexts[1][i] for i in source_indices)
        tail.append({"plaintext_position": p, "received_coordinate_positions": source_indices,
                     "received_digraph": pair})
    assert " ".join(t["received_digraph"] for t in tail) == "AF DV AF AV AF XX A? ?V A? GA AF XD"
    assert all(cert["source_coordinate_maps"][0][p]["received_digraph"] == "DV" for p in (25, 27))

    repaired = list(ciphertexts[1])
    hypothesis = cert["part6_body_hypothesis"]
    for row in hypothesis["inferred_erased_coordinates"]:
        assert repaired[row["received_position"]] == "?"
        repaired[row["received_position"]] = row["proposed_coordinate"]
    for row in hypothesis["printed_coordinate_disagreements"]:
        assert repaired[row["received_position"]] == row["printed"]
        repaired[row["received_position"]] = row["body_requires"]
    repaired = "".join(repaired)
    separator_square = cert["optional_separator_partial_square"]
    conditional_decode = decipher(repaired, ranks, separator_square)
    assert conditional_decode == hypothesis["text"] + "X?XGXR???BXA"
    assert sum(ch != "?" for ch in conditional_decode) == 50
    assert [i for i, ch in enumerate(repaired) if ch == "?"] == [5, 11, 17]

    # Re-encoding tests use arbitrary complete squares strictly as witnesses.
    # They are not candidate historical digit assignments.
    models = []
    checked_assignments = set()
    for nonfuture, nozero in ((False, False), (True, False), (False, True), (True, True)):
        values = date_assignments(nonfuture=nonfuture, no_leading_zero=nozero)
        models.append({"nonfuture_date": nonfuture, "serial_has_no_leading_zero": nozero,
                       "count": len(values), "days": sorted({v["day"] for v in values}),
                       "months": sorted({v["month"] for v in values}),
                       "assignments_sha256": digest(values)})
        for value in values:
            assignment_key = value["day"], value["month"], value["serial"]
            if assignment_key in checked_assignments:
                continue
            checked_assignments.add(assignment_key)
            partial = list(separator_square)
            partial[12], partial[19] = str(value["day"]), str(value["month"])[0]
            partial[10], partial[24] = value["serial"][0], value["serial"][1]
            square = complete(partial)
            first = decipher(ciphertexts[0], ranks, square)
            assert encipher(first, ranks, square) == ciphertexts[0]
            for fills in itertools.product(COORDS, repeat=3):
                full_ct = list(repaired)
                for index, ch in zip((5, 11, 17), fills):
                    full_ct[index] = ch
                full_ct = "".join(full_ct)
                second = decipher(full_ct, ranks, square)
                assert second[:42] == hypothesis["text"]
                assert second[43] == value["serial"][0]
                assert encipher(second, ranks, square) == full_ct
    assert [r["count"] for r in models] == [448, 392, 392, 343]
    assert len(checked_assignments) == 448

    sample = date_assignments(nonfuture=True, no_leading_zero=False)[0]
    partial = list(separator_square)
    partial[12], partial[19], partial[10], partial[24] = str(sample["day"]), "1", sample["serial"][0], sample["serial"][1]
    triples = footer_triples(partial)
    # Independent count: no free row cell is used, or at least one is used.
    formula = 5**2 * (5 + 12) + (6**2 - 5**2) * 12 * (5 + 11)
    assert formula == len(triples) == 2537
    assert all(t[0] != t[1] or t[0] == "G" for t in triples)
    assert all(t[1] != t[2] or t[1] == "G" for t in triples)

    reuse = []
    skipped = []
    for key in keys:
        if key["id"] == "CHI-Nov8-2026-recovery":
            continue
        if set(key["square"]) == {"?"}:
            skipped.append({"key_id": key["id"], "reason": "No attested square cells; no reuse exclusion possible."})
            continue
        witnesses = []
        for transpose in (0, 1):
            witness = reuse_obstruction(core, key["square"], transpose)
            assert witness is not None, key["id"]
            witnesses.append({"transpose_square": bool(transpose), **witness})
        reuse.append({"key_id": key["id"], "obstructions": witnesses})
    assert len(reuse) == 23
    # Relabel a complete extension, then check the invariant does not reject it.
    full = complete(core)
    rp, cp = (2, 5, 0, 4, 1, 3), (4, 1, 5, 0, 3, 2)
    permuted = "".join(full[6*rp[r]+cp[c]] for r in range(6) for c in range(6))
    assert reuse_obstruction(core, permuted, 0) is None
    transposed = "".join(permuted[6*c+r] for r in range(6) for c in range(6))
    assert reuse_obstruction(core, transposed, 1) is None

    return {
        "schema": "adfgvx-p153-shared-cell-extension-v1",
        "title": "ADFGVX Cipher: p153 shared-cell and conditional-date constraints",
        "authors": ["icekylinx", "GPT-6 Astra Pro"],
        "date": "2026-11-02",
        "status": "Exact follow-up of the accepted partial recovery; no new unconditional digit or source repair.",
        "evidence_sha256": digest({"ciphertexts": ciphertexts, "ranks": ranks, "core": core,
                                   "other_squares": [{"id": k["id"], "square": k["square"]} for k in keys]}),
        "tail_source_map": tail,
        "shared_cell": {"digraph": "DV", "square_cell": 10, "part5_positions": [25, 27], "part6_position": 43,
                        "conclusion": "The first and last serial character and the footer character are identical under every shared-square completion."},
        "conditional_part6": {
            "plain_template": "MUNITIONSBESTAND DER NACHHUTARTILLERIE MELDEN X <gamma> X G X R <u><v><w> B X A",
            "position_string": conditional_decode,
            "fixed_positions": 50, "total_positions": 54,
            "conditions": ["The previously certified 42-letter body with twelve erased-coordinate fills and two A-to-X emendations.",
                           "The separately stated AF=X footer-separator interpretation."],
            "unconditional_core_fixed_positions": 33,
            "unresolved_footer_digraphs": {"u": "A?", "v": "?V", "w": "A?"},
            "coupling": ["u=v implies u=v=G.", "v=w implies v=w=G.", "u=w is otherwise allowed."],
            "interpretation": "No expansion of the G, R, B or A initials, military unit, signature or padding is asserted."
        },
        "date_models": {
            "common_conditions": ["FA is a one-character ordinary decimal day.", "GD GD is a two-character ordinary decimal month between 1 and 12.",
                                  "DV VA DV is a three-character decimal serial.", "Distinct square cells have distinct plaintext symbols."],
            "forced_within_these_conditions": {"month": 11, "GD": "1", "FA_not": "1", "DV_not": "1", "VA_not": "1"},
            "extra_condition_nonfuture": "The referenced order is dated in 1918 no later than the received 8 November message; this is not ciphertext evidence.",
            "models": models,
            "historical_digit_claim": "No day or serial is selected. GD=1 is conditional on decimal-calendar interpretation, not an independently recovered square cell."
        },
        "remaining_ambiguity": {
            "per_fixed_decimal_assignment": {"square_completions": math.factorial(12), "remaining_erasure_fills_per_square": 216,
                                             "distinct_footer_triples": len(triples), "count_formula": "25*(5+12) + 11*12*(5+11) = 2537"},
            "nonfuture_allowing_leading_zero": {"date_serial_assignments": 392, "distinct_joint_plaintext_pairs": 392 * len(triples)},
            "nonfuture_no_leading_zero": {"date_serial_assignments": 343, "distinct_joint_plaintext_pairs": 343 * len(triples)},
            "scope": "Conditions include AF=X and the existing body emendation/fill hypothesis. All unassigned square letters/digits and three residual source erasures are free; no language or historical ranking is added."
        },
        "other_square_reuse": {
            "model": "Any independent permutations of six rows and six columns, optionally transposing the square; all established letter identities preserved.",
            "excluded_key_count": len(reuse), "proof": "Bijections preserve equality of row and column coordinates for every pair of known letters. Each recorded witness violates one such equality.",
            "witnesses": reuse, "skipped": skipped,
            "limits": "This rejects only the recorded squares under the stated relabeling model. It does not exclude a related keyword, arbitrary cell permutation, different square or additional source errors.",
            "positive_controls": ["Known full extension with independent row/column relabeling passes.", "Its transposed version passes the transposed invariant."]
        },
        "verification": {"independent_coordinate_map": True, "raw_core_decodes_reproduced": True,
                         "every_date_assignment_roundtripped": True, "all_216_residual_erasure_fills_per_assignment_roundtripped": True,
                         "footer_union_matches_independent_count": True, "input_sources_changed": False}
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "result.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = analyze()
    if args.verify:
        assert result == json.loads(args.output.read_text()), "Stored result does not reproduce."
    else:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"conditional_part6_fixed_positions": 50,
                      "date_model_counts": [r["count"] for r in result["date_models"]["models"]],
                      "footer_triples_per_fixed_assignment": 2537,
                      "other_squares_excluded_by_exact_invariants": 23,
                      "verified": args.verify}))


if __name__ == "__main__":
    main()
