"""Check the stored conditional historical witness without model files.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This does not rerun optimization or validate individual model lookups.
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
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

SCALE = 1 << 24


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    calibration_path = ROOT / "experiments/p198_joint_six/results.json"
    quad_path = ROOT / "experiments/p198_joint_exact/results.json"
    engine = ROOT / "experiments/p198_joint_six/exact_joint_six.cpp"
    data = json.loads((HERE / "results.json").read_text())
    for key, path in [("input_sha256", input_path), ("calibration_results_sha256", calibration_path),
                      ("quad_results_sha256", quad_path), ("engine_source_sha256", engine)]:
        assert data[key] == digest(path)
    case = next(c for c in json.loads(input_path.read_text())["cases"] if c["id"] == data["case_id"])
    ranks, square = case["column_rank_order"], case["fixed_complete_square"]
    assert sorted(ranks) == list(range(1, 17))
    assert len(square) == 36 and set(square) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    result, witness = data["exact_search"], data["verification"]
    losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    assert losses == sorted(set(losses)) and len(losses) == len(fill) == 5
    assert all(0 <= i < 170 for i in losses) and set(fill) <= set("ADFGVX")
    full, text = witness["completed_ciphertext"], witness["plaintext"]
    assert len(full) == 170 and len(text) == 85
    assert "".join(full[i] for i in losses) == fill
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    assert decrypt(full, ranks, square) == text and encrypt(text, ranks, square) == full
    padded = "".join("?" if i in losses else c for i, c in enumerate(full))
    assert padded == witness["padded_ciphertext"]
    full_domains = plaintext_domains(padded, ranks, square)
    partial_domains = plaintext_domains(padded, ranks, case["partial_historical_square"])
    assert partial_domains == witness["partial_square_domains_at_selected_geometry"]
    assert all(c in d for c, d in zip(text, partial_domains))
    assert witness["singleton_positions_under_frozen_complete_square_before_gap_fills"] == sum(len(d) == 1 for d in full_domains)
    assert witness["singleton_positions_under_recorded_partial_square_before_gap_fills"] == sum(len(d) == 1 for d in partial_domains)
    assert witness["model_selected_square_labels_in_frozen_completion"] == case["partial_historical_square"].count("?")
    assert witness["source_coordinates_preserved"] == 165
    assert witness["changed_retained_coordinates"] == 0 and witness["model_selected_coordinate_fills"] == 5
    assert result["all_allocations_completed"] and result["allocation_start"] == 0
    assert result["allocation_count_total"] == result["allocations_completed"] == 15504
    assert result["maximum_active_states"] <= 7 ** 5
    assert result["integer_log_scale"] == SCALE and result["coefficient4"] == 0 and result["coefficient6"] == 1
    values = witness["scores"]
    assert values["six_integer_sum"] == result["best_integer_score"]
    assert values["quad_mean"] == values["quad_integer_sum"] / (82 * SCALE)
    assert values["six_mean"] == values["six_integer_sum"] / (80 * SCALE)
    assert values["mixed_30_70_mean"] == (240 * values["quad_integer_sum"] + 574 * values["six_integer_sum"]) / (10 * 82 * 80 * SCALE)
    previous = next(r for r in json.loads(quad_path.read_text())["records"] if r["case_id"] == case["id"])
    comparison = data["earlier_quad_optimum_rescored"]
    assert comparison["plaintext"] == previous["verification"]["plaintext"]
    assert comparison["loss_positions"] == previous["exact_search"]["missing_full_ciphertext_positions"]
    assert comparison["six_integer_advantage_of_new_optimum"] == result["best_integer_score"] - comparison["scores"]["six_integer_sum"] >= 0
    fixed = data["best_six_completion_at_earlier_quad_mask"]
    assert fixed["loss_positions"] == comparison["loss_positions"]
    fixed_full = encrypt(fixed["plaintext"], ranks, square)
    assert "".join(c for i, c in enumerate(fixed_full) if i not in fixed["loss_positions"]) == case["observed_ciphertext"]
    assert fixed["mean_six_score"] == fixed["integer_six_score"] / (80 * SCALE)
    assert fixed["new_geometry_integer_advantage"] == result["best_integer_score"] - fixed["integer_six_score"] >= 0
    assert int(data["loss_and_fill_witnesses_covered"]) == math.comb(170, 5) * 6 ** 5
    assert witness["accepted_historical_plaintext"] is False
    assert data["newly_accepted_historical_plaintext_characters"] == 0
    print("Verified the conditional p198 sixgram source witness, key-domain counts and score arithmetic.")
    print("No model lookups or searches rerun; historical plaintext remains unaccepted.")


if __name__ == "__main__":
    main()
