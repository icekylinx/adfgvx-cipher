"""Check stored Pareto witnesses and report arithmetic without optimization.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The separate independent verifier recomputes the global frontier.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def nondominated(points):
    points = set(points)
    return sorted(p for p in points if not any(q != p and q[0] <= p[0] and q[1] <= p[1] for q in points))


def witness(case, row):
    square = row["representative_square"]
    assert len(square) == 36 and set(square) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    losses, fill = row["loss_positions"], row["fill"]
    total = len(case["observed_ciphertext"]) + case["missing_count"]
    assert losses == sorted(set(losses)) and len(losses) == len(fill) == case["missing_count"]
    assert all(0 <= i < total for i in losses) and set(fill) <= set("ADFGVX")
    full, text = row["filled_ciphertext"], row["plaintext_witness"]
    assert len(full) == total and len(text) == total // 2
    assert "".join(full[i] for i in losses) == fill
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    assert decrypt(full, case["column_rank_order"], square) == text
    assert encrypt(text, case["column_rank_order"], square) == full
    counts = sum(c in "0123456789" for c in text), sum(c in "QY" for c in text)
    assert counts == (row["digits"], row["Q_or_Y"])
    assert row["target24_letters"] == len(text) - sum(counts)
    assert row["source_coordinates_preserved"] == len(case["observed_ciphertext"])
    assert row["changed_retained_coordinates"] == 0 and row["accepted_historical_plaintext"] is False
    ranks = case["column_rank_order"]
    lengths = [total // len(ranks) + (c < total % len(ranks)) for c in range(len(ranks))]
    allocation, start = [0] * len(ranks), 0
    for column in sorted(range(len(ranks)), key=ranks.__getitem__):
        allocation[column] = sum(start <= p < start + lengths[column] for p in losses)
        start += lengths[column]
    assert allocation == row["losses_per_physical_column"]
    return counts


def main():
    data = json.loads((HERE / "results.json").read_text())
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    assert data["input_sha256"] == digest(input_path)
    assert data["algorithm_source_sha256"] == digest(HERE / "compute.py")
    assert data["category_bounds_sha256"] == digest(ROOT / "experiments/p198_letter_bounds/category_bounds.json")
    assert data["ordinary_bounds_sha256"] == digest(ROOT / "experiments/p198_letter_bounds/results.json")
    case = next(c for c in json.loads(input_path.read_text())["cases"] if c["id"] == data["case_id"])
    partial = case["partial_historical_square"]
    assert data["partial_square"] == partial and data["column_rank_order"] == case["column_rank_order"]
    unknown = [i for i, c in enumerate(partial) if c == "?"]
    expected_memberships = set(itertools.combinations(unknown, 2))
    seen, all_points, count_full = set(), set(), 0
    by_membership = {}
    for member in data["membership_results"]:
        cells = tuple(member["QY_cell_indices"])
        assert cells not in seen
        seen.add(cells)
        square = member["representative_square"]
        assert all(a == "?" or a == b for a, b in zip(partial, square))
        assert tuple(i for i in unknown if square[i] in "QY") == cells
        search = member["search_counts"]
        assert search["all_allocations_completed"] and search["allocations_completed"] == 15504
        points = []
        for row in member["frontier_witnesses"]:
            assert row["representative_square"] == square
            points.append(witness(case, row))
            count_full += 1
        assert points == nondominated(points)
        all_points.update(points)
        by_membership[cells] = {point: row for point, row in zip(points, member["frontier_witnesses"])}
    assert seen == expected_memberships and len(seen) == data["membership_classes_completed"] == 28
    expected_global = nondominated(all_points)
    observed_global = []
    for row in data["global_frontier"]:
        point = witness(case, row)
        observed_global.append(point)
        member_row = by_membership[tuple(row["QY_cell_indices"])][point]
        assert all(row[key] == value for key, value in member_row.items())
    assert observed_global == expected_global == [tuple(p) for p in data["global_frontier_counts"]]
    for row in data["bounds_with_at_most_QY"]:
        assert row["minimum_attainable_digits"] == min((d for d, q in expected_global if q <= row["QY_budget"]), default=None)
    assert data["complete_square_extensions_covered"] == math.factorial(8)
    assert int(data["loss_and_fill_witnesses_per_complete_square"]) == math.comb(170, 5) * 6 ** 5
    assert data["all_memberships_and_allocations_completed"] and data["allocations_per_membership"] == 15504
    controls = data["controls"]
    total_small, largest = 0, 0
    for control in controls["records"]:
        assert control["memberships_exhausted"] == len(control["checks"]) == 28
        count = math.comb(control["nominal_coordinates"], control["case"]["missing_count"]) * 6 ** control["case"]["missing_count"]
        assert control["loss_and_fill_witnesses_per_membership"] == count
        assert control["total_membership_loss_fill_witnesses"] == 28 * count
        total_small += 28 * count
        for check in control["checks"]:
            points = [witness(control["case"], row) for row in check["witnesses"]]
            assert points == nondominated(points) == [tuple(p) for p in check["frontier"]]
            largest = max(largest, len(points))
    assert total_small == controls["total_membership_loss_fill_witnesses_enumerated"] == 285264
    assert largest == controls["maximum_small_control_frontier_size"] >= 2
    assert controls["records"][0]["checks"][0]["frontier"] == [[1, 4], [2, 2]]
    assert data["newly_accepted_historical_plaintext_characters"] == 0
    print(f"Verified {count_full} membership and {len(observed_global)} global source witnesses, all memberships and frontier arithmetic.")
    print("Recorded-witness check only; use verify_independent.py for a full separate optimum recomputation.")


if __name__ == "__main__":
    main()
