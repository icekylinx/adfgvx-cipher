"""Check stored six-gram calibration witnesses without models or search.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This verifies source feasibility and score arithmetic, not model lookups
or global optimality.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

SCALE = 1 << 24


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def score_arithmetic(values):
    assert isinstance(values["quad_integer_sum"], int) and isinstance(values["six_integer_sum"], int)
    assert values["quad_mean"] == values["quad_integer_sum"] / (82 * SCALE)
    assert values["six_mean"] == values["six_integer_sum"] / (80 * SCALE)
    assert values["mixed_30_70_mean"] == (240 * values["quad_integer_sum"] + 574 * values["six_integer_sum"]) / (10 * 82 * 80 * SCALE)


def main():
    data = json.loads((HERE / "results.json").read_text())
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    quad_path = ROOT / "experiments/p198_joint_exact/results.json"
    assert data["input_sha256"] == digest(input_path)
    assert data["quad_results_sha256"] == digest(quad_path)
    assert data["engine_source_sha256"] == digest(HERE / "exact_joint_six.cpp")
    assert data["integer_log_scale"] == SCALE
    assert int(data["witnesses_per_full_search"]) == math.comb(170, 5) * 6 ** 5
    cases = {c["id"]: c for c in json.loads(input_path.read_text())["cases"]}
    quad = {r["case_id"]: r for r in json.loads(quad_path.read_text())["records"]}
    assert {r["objective"] for r in data["records"]} == {"six", "mixed_30_70"}
    for record in data["records"]:
        case = cases[record["case_id"]]
        result, witness = record["exact_search"], record["verification"]
        square, ranks = case["fixed_complete_square"], case["column_rank_order"]
        assert len(square) == 36 and set(square) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        assert sorted(ranks) == list(range(1, len(ranks) + 1))
        losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
        assert losses == sorted(set(losses)) and len(losses) == len(fill) == 5
        assert all(0 <= i < 170 for i in losses) and set(fill) <= set("ADFGVX")
        full, text = witness["completed_ciphertext"], witness["plaintext"]
        assert len(full) == 170 and len(text) == 85
        assert "".join(full[i] for i in losses) == fill
        assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
        assert decrypt(full, ranks, square) == text
        assert encrypt(text, ranks, square) == full
        assert result["nominal_coordinates"] == 170 and result["observed_coordinates"] == 165
        assert result["missing_coordinates"] == 5 and result["width"] == 16
        assert result["integer_log_scale"] == SCALE and result["quad_windows"] == 82 and result["six_windows"] == 80
        assert result["all_allocations_completed"] and result["allocation_start"] == 0
        assert result["allocation_count_total"] == result["allocations_completed"] == 15504
        assert result["maximum_active_states"] <= 7 ** 5
        c4, c6, denominator = ((0, 1, 80 * SCALE) if record["objective"] == "six"
                               else (240, 574, 10 * 82 * 80 * SCALE))
        assert result["coefficient4"] == c4 and result["coefficient6"] == c6
        values, planted = witness["scores"], witness["planted_scores"]
        score_arithmetic(values)
        score_arithmetic(planted)
        assert result["best_integer_score"] == c4 * values["quad_integer_sum"] + c6 * values["six_integer_sum"]
        assert witness["planted_integer_objective"] == c4 * planted["quad_integer_sum"] + c6 * planted["six_integer_sum"]
        assert witness["display_objective"] == result["best_integer_score"] / denominator
        assert witness["integer_denominator_for_display"] == denominator
        assert witness["global_optimum_integer_advantage_over_truth"] == result["best_integer_score"] - witness["planted_integer_objective"] >= 0
        assert witness["planted_plaintext"] == case["evaluation_only"]["plaintext"]
        assert witness["plaintext_matches_truth"] == (text == witness["planted_plaintext"])
        assert witness["plaintext_hamming_distance_from_truth"] == sum(a != b for a, b in zip(text, witness["planted_plaintext"]))
        assert witness["completed_ciphertext_matches_truth"] == (full == case["evaluation_only"]["full_ciphertext"])
        assert witness["loss_mask_matches_planted_mask"] == (losses == case["evaluation_only"]["missing_full_ciphertext_positions_0based"])
        assert witness["retained_source_coordinates_preserved"] == 165
        assert witness["changed_retained_source_coordinates"] == 0 and witness["model_selected_missing_coordinates"] == 5
    for row in data["quad_winner_sensitivity"]:
        case = cases[row["case_id"]]
        previous = quad[row["case_id"]]
        assert row["quad_optimum_plaintext"] == previous["verification"]["plaintext"]
        full = encrypt(row["quad_optimum_plaintext"], case["column_rank_order"], case["fixed_complete_square"])
        losses = previous["exact_search"]["missing_full_ciphertext_positions"]
        assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
        score_arithmetic(row["planted"])
        score_arithmetic(row["quad_optimum"])
        assert all(value == row["quad_optimum"][key] - row["planted"][key]
                   for key, value in row["quad_optimum_minus_planted"].items())
    negative = next(r for r in data["quad_winner_sensitivity"] if r["case_id"] == "control_Nov13-15b")
    assert negative["quad_optimum_minus_planted"]["six_integer_sum"] > 0
    assert negative["quad_optimum_minus_planted"]["mixed_30_70_mean"] > 0
    pilot = data["pilot100"]
    assert pilot["allocations_completed"] == 100 and pilot["all_allocations_completed"] is False
    assert data["newly_accepted_historical_plaintext_characters"] == 0
    print("Verified two full six/mixed control witnesses, prior feasible competitors and exact score arithmetic.")
    print("No model lookups or searches rerun; this is not an optimality proof.")


if __name__ == "__main__":
    main()
