"""Verify recorded count witnesses, not the global optimality of the search.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
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


def check(case, square, bound):
    assert len(square) == 36 and set(square) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    result, witness = bound["exact_search"], bound["verification"]
    losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    assert losses == sorted(set(losses)) and len(losses) == len(fill) == 5
    assert all(0 <= i < 170 for i in losses) and set(fill) <= set("ADFGVX")
    full = witness["filled_ciphertext"]
    assert len(full) == 170 and len(case["observed_ciphertext"]) == 165
    assert "".join(full[i] for i in losses) == fill
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    text = decrypt(full, case["column_rank_order"], square)
    assert text == witness["representative_plaintext"]
    assert encrypt(text, case["column_rank_order"], square) == full
    count = sum(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in text)
    assert count == result["ordinary_letter_count"] == witness["ordinary_letter_count"]
    assert witness["digit_count"] == 85 - count
    assert result["best_signed_letter_count"] == (count if result["maximize_letters"] else -count)
    assert result["all_allocations_completed"] and result["allocation_start"] == 0
    assert result["allocations_completed"] == result["allocation_count_total"] == 15504
    assert result["maximum_active_states"] <= 32
    assert witness["source_coordinates_preserved"] == 165
    assert witness["changed_retained_coordinates"] == witness["model_selected_coordinates"] == 0
    assert witness["count_objective_selected_coordinates"] == 5
    assert witness["accepted_historical_plaintext"] is False
    return count


def main():
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    cases = {case["id"]: case for case in json.loads(input_path.read_text())["cases"]}
    data = json.loads((HERE / "results.json").read_text())
    assert data["input_sha256"] == digest(input_path)
    assert data["engine_source_sha256"] == digest(HERE / "exact_letter_bounds.cpp")
    case = cases[data["case_id"]]
    partial = case["partial_historical_square"]
    assert data["partial_square"] == partial
    assert data["column_rank_order"] == case["column_rank_order"]
    unknown = [i for i, c in enumerate(partial) if c == "?"]
    expected = set(itertools.combinations(unknown, 2))
    observed, minima, maxima = set(), [], []
    for row in data["membership_results"]:
        square = row["representative_complete_square"]
        assert all(a == "?" or a == b for a, b in zip(partial, square))
        letter_cells = tuple(i for i in unknown if square[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        assert list(letter_cells) == row["letter_cells_at_unknown_positions"]
        assert letter_cells not in observed
        observed.add(letter_cells)
        minimum, maximum = row["bounds"]
        assert minimum["exact_search"]["maximize_letters"] is False
        assert maximum["exact_search"]["maximize_letters"] is True
        minima.append(check(case, square, minimum))
        maxima.append(check(case, square, maximum))
        assert minima[-1] <= maxima[-1]
    assert observed == expected and len(observed) == data["unknown_cell_membership_assignments"] == 28
    assert int(data["complete_square_extensions_covered"]) == math.factorial(8)
    assert data["complete_square_extensions_per_membership"] == math.factorial(2) * math.factorial(6)
    assert len(observed) * data["complete_square_extensions_per_membership"] == math.factorial(8)
    assert int(data["loss_and_fill_witnesses_per_complete_square"]) == math.comb(170, 5) * 6 ** 5
    assert min(minima) == data["attainable_global_minimum_letters"]
    assert max(maxima) == data["attainable_global_maximum_letters"]
    assert 85 - max(maxima) == data["implied_attainable_global_minimum_digits"]
    assert 85 - min(minima) == data["implied_attainable_global_maximum_digits"]
    for control in data["positive_controls"]:
        source = cases[control["case_id"]]
        bounds = [check(source, source["fixed_complete_square"], bound) for bound in control["bounds"]]
        assert bounds[1] == len(source["evaluation_only"]["plaintext"]) == 85
    assert data["newly_accepted_historical_plaintext_characters"] == 0
    print("Verified all 28 square-membership assignments, 60 full count witnesses and declared extrema.")
    print("Recorded feasibility/arithmetic check only; no optimization rerun.")


if __name__ == "__main__":
    main()
