"""Exact source-feasible digit/QY Pareto frontier for a partial ADFGVX key.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Every membership class and column-loss allocation is exhausted. No language
model or claim about the historical numbers of digits, Q or Y is used.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, untranspose

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def allocations(remaining, lengths, prefix=()):
    if not lengths:
        if remaining == 0:
            yield prefix
        return
    for count in range(min(remaining, lengths[0]) + 1):
        yield from allocations(remaining - count, lengths[1:], prefix + (count,))


def pareto(mapping):
    """Minimize both nonnegative counts; retain one witness per frontier pair."""
    kept, best_second = {}, math.inf
    for counts in sorted(mapping):
        if counts[1] < best_second:
            kept[counts] = mapping[counts]
            best_second = counts[1]
    return kept


@lru_cache(maxsize=200000)
def combine_shapes(left, right):
    joined = {}
    for i, (ld, lq) in enumerate(left):
        for j, (rd, rq) in enumerate(right):
            joined.setdefault((ld + rd, lq + rq), (i, j))
    return tuple((d, q, *indices) for (d, q), indices in pareto(joined).items())


def optimize_membership(source, ranks, missing, square, allocation_limit=0):
    total, width = len(source) + missing, len(ranks)
    assert total % 2 == width % 2 == 0
    assert sorted(ranks) == list(range(1, width + 1))
    lengths = [total // width + (c < total % width) for c in range(width)]
    assert all(lengths[c] == lengths[c + 1] for c in range(0, width, 2))
    readout = sorted(range(width), key=ranks.__getitem__)
    starts, start = [0] * width, 0
    for column in readout:
        starts[column], start = start, start + lengths[column]
    category = [2 if c in "QY" else 1 if c in "0123456789" else 0 for c in square]
    local = {}
    for left in range(7):
        for right in range(7):
            options = {}
            for first in range(6) if left == 6 else [left]:
                for second in range(6) if right == 6 else [right]:
                    kind = category[6 * first + second]
                    options.setdefault(kind, (first, second))
            kinds = [0] if 0 in options else sorted(options)
            local[left, right] = tuple((int(kind == 1), int(kind == 2), *options[kind]) for kind in kinds)
    pair_peak = 0

    @lru_cache(maxsize=None)
    def solve_pair(left, right, height):
        nonlocal pair_peak
        losses_left, losses_right = height - len(left), height - len(right)
        states = {(0, 0): {(0, 0): ((), ())}}
        for row in range(height):
            next_states = {}
            for (used_left, used_right), frontier in states.items():
                left_options = []
                right_options = []
                if row - used_left < len(left):
                    left_options.append((used_left, left[row - used_left], False))
                if used_left < losses_left:
                    left_options.append((used_left + 1, 6, True))
                if row - used_right < len(right):
                    right_options.append((used_right, right[row - used_right], False))
                if used_right < losses_right:
                    right_options.append((used_right + 1, 6, True))
                for new_left, a, lost_left in left_options:
                    for new_right, b, lost_right in right_options:
                        target = next_states.setdefault((new_left, new_right), {})
                        for delta_d, delta_q, first, second in local[a, b]:
                            for (digits, qy), (left_events, right_events) in frontier.items():
                                counts = (digits + delta_d, qy + delta_q)
                                if counts not in target:
                                    target[counts] = (left_events + ((row, first),) if lost_left else left_events,
                                                      right_events + ((row, second),) if lost_right else right_events)
            states = {state: pareto(frontier) for state, frontier in next_states.items()}
            pair_peak = max(pair_peak, max(map(len, states.values()), default=0))
        answer = states[losses_left, losses_right]
        return tuple((d, q, witness) for (d, q), witness in answer.items())

    observed = tuple(COORDINATES.index(c) for c in source)
    global_frontier, completed = {}, 0
    for allocation in allocations(missing, lengths):
        if allocation_limit and completed >= allocation_limit:
            break
        segments, at = [None] * width, 0
        for column in readout:
            retained = lengths[column] - allocation[column]
            segments[column] = observed[at:at + retained]
            at += retained
        assert at == len(observed)
        combined = (((0, 0), ()),)
        for column in range(0, width, 2):
            pair = solve_pair(segments[column], segments[column + 1], lengths[column])
            left_shape = tuple(counts for counts, _ in combined)
            right_shape = tuple((d, q) for d, q, _ in pair)
            combined = tuple(((d, q), combined[i][1] + (pair[j][2],))
                             for d, q, i, j in combine_shapes(left_shape, right_shape))
        for counts, pair_witnesses in combined:
            if counts not in global_frontier:
                additions = []
                for pair_index, (left_events, right_events) in enumerate(pair_witnesses):
                    for side, events in enumerate([left_events, right_events]):
                        column = 2 * pair_index + side
                        additions.extend((starts[column] + row, COORDINATES[value]) for row, value in events)
                additions.sort()
                assert len(additions) == missing
                global_frontier[counts] = {"loss_positions": [p for p, _ in additions],
                                           "fill": "".join(c for _, c in additions),
                                           "losses_per_physical_column": list(allocation)}
        global_frontier = pareto(global_frontier)
        completed += 1
    return {"frontier": global_frontier, "allocations_completed": completed,
            "all_allocations_completed": not allocation_limit or completed < allocation_limit,
            "pair_subproblems": solve_pair.cache_info().misses,
            "pair_cache_hits": solve_pair.cache_info().hits,
            "maximum_pair_state_frontier_size": pair_peak}


def representatives(partial):
    unknown = [i for i, c in enumerate(partial) if c == "?"]
    letters = sorted(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - set(partial))
    digits = sorted(set("0123456789") - set(partial))
    assert letters == ["Q", "Y"] and len(unknown) == 8
    for letter_cells in itertools.combinations(unknown, 2):
        square = list(partial)
        for cell, letter in zip(letter_cells, letters):
            square[cell] = letter
        for cell, digit in zip((c for c in unknown if c not in letter_cells), digits):
            square[cell] = digit
        yield tuple(letter_cells), "".join(square)


def fill_frame(source, losses, fill):
    additions, iterator = dict(zip(losses, fill)), iter(source)
    full = "".join(additions[i] if i in additions else next(iterator)
                    for i in range(len(source) + len(losses)))
    assert next(iterator, None) is None
    return full


def witness_record(case, square, counts, witness):
    losses, fill = witness["loss_positions"], witness["fill"]
    assert len(losses) == len(fill) == case["missing_count"]
    assert losses == sorted(set(losses)) and set(fill) <= set(COORDINATES)
    full = fill_frame(case["observed_ciphertext"], losses, fill)
    text = decrypt(full, case["column_rank_order"], square)
    digits, qy = sum(c in "0123456789" for c in text), sum(c in "QY" for c in text)
    assert (digits, qy) == counts
    assert encrypt(text, case["column_rank_order"], square) == full
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    return {"digits": digits, "Q_or_Y": qy, "target24_letters": len(text) - digits - qy,
            "representative_square": square, **witness, "plaintext_witness": text,
            "filled_ciphertext": full, "source_coordinates_preserved": len(case["observed_ciphertext"]),
            "changed_retained_coordinates": 0, "reencryption_verified": True,
            "accepted_historical_plaintext": False}


def exhaustive_controls(partial):
    completions = list(representatives(partial))
    first_square = completions[0][1]
    settings = [([3, 1, 4, 2], "Q5YQ5Q", 1),
                ([4, 1, 6, 2, 5, 3], "QY2STAB", 2),
                ([3, 13, 2, 12, 1, 11, 15, 8, 9, 4, 5, 14, 6, 10, 7, 16], "DERQY3BMEL", 2)]
    reports = []
    for ranks, text, missing in settings:
        full = encrypt(text, ranks, first_square)
        planted = [1] if missing == 1 else [1, len(full) - 3]
        observed = "".join(c for i, c in enumerate(full) if i not in planted)
        case = {"column_rank_order": ranks, "observed_ciphertext": observed, "missing_count": missing}
        expected = [set() for _ in completions]
        count = 0
        for losses in itertools.combinations(range(len(full)), missing):
            for values in itertools.product(COORDINATES, repeat=missing):
                frame = fill_frame(observed, losses, "".join(values))
                stream = untranspose(frame, ranks)
                cells = [6 * COORDINATES.index(stream[i]) + COORDINATES.index(stream[i + 1]) for i in range(0, len(stream), 2)]
                histogram = [cells.count(i) for i in range(36)]
                for index, (_, square) in enumerate(completions):
                    digits = sum(histogram[i] for i, c in enumerate(square) if c in "0123456789")
                    qy = sum(histogram[i] for i, c in enumerate(square) if c in "QY")
                    expected[index].add((digits, qy))
                count += 1
        checks = []
        for index, (letter_cells, square) in enumerate(completions):
            result = optimize_membership(observed, ranks, missing, square)
            reference = set(pareto({point: None for point in expected[index]}))
            assert set(result["frontier"]) == reference
            records = [witness_record(case, square, point, witness) for point, witness in result["frontier"].items()]
            checks.append({"QY_cell_indices": list(letter_cells), "frontier": [list(p) for p in sorted(reference)],
                           "all_frontier_witnesses_verified": True, "witnesses": records})
        reports.append({"case": case, "nominal_coordinates": len(full), "loss_and_fill_witnesses_per_membership": count,
                        "memberships_exhausted": len(completions), "total_membership_loss_fill_witnesses": count * len(completions),
                        "checks": checks})
    largest_frontier = max(len(check["frontier"]) for report in reports for check in report["checks"])
    assert largest_frontier >= 2
    assert reports[0]["checks"][0]["frontier"] == [[1, 4], [2, 2]]
    return {"total_membership_loss_fill_witnesses_enumerated": sum(r["total_membership_loss_fill_witnesses"] for r in reports),
            "maximum_small_control_frontier_size": largest_frontier,
            "incomparable_frontier_control": {"source": "DFFDDAADDAA", "ranks": [3, 1, 4, 2],
                                               "square": first_square, "frontier": [[1, 4], [2, 2]],
                                               "witnesses_exhausted": 72},
            "records": reports}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pilot-allocations", type=int, default=0)
    args = parser.parse_args()
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    cases = json.loads(input_path.read_text())["cases"]
    case = next(c for c in cases if c["id"] == "p198_Nov13-15b")
    spec = importlib.util.spec_from_file_location("source_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    provenance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provenance)
    provenance.audit_provenance(cases)
    partial = case["partial_historical_square"]
    controls = exhaustive_controls(partial) if not args.pilot_allocations else None
    rows, global_frontier = [], {}
    for letter_cells, square in representatives(partial):
        result = optimize_membership(case["observed_ciphertext"], case["column_rank_order"], case["missing_count"], square,
                                     allocation_limit=args.pilot_allocations)
        if not args.pilot_allocations:
            assert result["all_allocations_completed"] and result["allocations_completed"] == 15504
        records = [witness_record(case, square, point, witness) for point, witness in result["frontier"].items()]
        for counts, witness in zip(result["frontier"], records):
            global_frontier.setdefault(counts, {"QY_cell_indices": list(letter_cells), **witness})
        global_frontier = pareto(global_frontier)
        rows.append({"QY_cell_indices": list(letter_cells), "representative_square": square,
                     "search_counts": {k: v for k, v in result.items() if k != "frontier"}, "frontier_witnesses": records})
        print(json.dumps({"membership": len(rows), "QY_cells": letter_cells, "frontier": list(result["frontier"]),
                          "allocations": result["allocations_completed"]}), flush=True)
        if args.pilot_allocations:
            break
    if args.pilot_allocations:
        print("Incomplete performance pilot; no global result is written.")
        return
    frontier = list(global_frontier)
    assert len(rows) == 28
    category_path = ROOT / "experiments/p198_letter_bounds/category_bounds.json"
    ordinary_path = ROOT / "experiments/p198_letter_bounds/results.json"
    output = {"schema": "adfgvx-exact-digit-QY-pareto-v1", "project": "ADFGVX Cipher",
              "authors": "icekylinx and GPT-6 Astra Pro", "case_id": case["id"],
              "input_sha256": digest(input_path), "algorithm_source_sha256": digest(HERE / "compute.py"),
              "category_bounds_sha256": digest(category_path), "ordinary_bounds_sha256": digest(ordinary_path),
              "partial_square": partial, "column_rank_order": case["column_rank_order"],
              "objectives": ["Minimize digit positions", "Minimize positions containing Q or Y"],
              "complete_square_extensions_covered": math.factorial(8),
              "membership_classes_completed": len(rows), "allocations_per_membership": 15504,
              "loss_and_fill_witnesses_per_complete_square": str(math.comb(170, 5) * 6 ** 5),
              "all_memberships_and_allocations_completed": True, "controls": controls,
              "membership_results": rows, "global_frontier": list(global_frontier.values()),
              "global_frontier_counts": [list(point) for point in frontier],
              "bounds_with_at_most_QY": [{"QY_budget": budget, "minimum_attainable_digits": min((d for d, q in frontier if q <= budget), default=None)} for budget in range(16)],
              "witness_tie_rule": "First encountered under sorted membership indices, physical-column loss allocations and deterministic pair choices; no global lexical-canonical claim.",
              "scope": "All 8! completions of the recorded Nov13-15b partial square, fixed transposition, every exactly-five-deletion geometry and coordinate filling, preserving all 165 observed coordinates in order.",
              "limits": ["The historical digit and Q/Y counts are unknown, so this count frontier does not reject or authenticate the key.",
                         "A Pareto frontier lists nondominated count pairs, not every attainable count pair or readable plaintext.",
                         "Representative texts are feasibility witnesses with no language-model ranking.",
                         "Other keys, transpositions and damage models are outside the declared family."],
              "newly_accepted_historical_plaintext_characters": 0}
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored Pareto frontier differs from full recomputation")
        print("Exact category frontier, exhaustive controls and all source witnesses fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"global_frontier": frontier, "small_witnesses": controls["total_membership_loss_fill_witnesses_enumerated"]}))


if __name__ == "__main__":
    main()
