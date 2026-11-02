"""Check recorded source witnesses and arithmetic without model downloads.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This quick check does not rerun optimization or validate model-table lookups.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"
SCALE = 1 << 24


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def insert(source, losses, values):
    additions = dict(zip(losses, values))
    source_iter = iter(source)
    full = "".join(additions[i] if i in additions else next(source_iter)
                   for i in range(len(source) + len(losses)))
    assert next(source_iter, None) is None
    return full


def allocations(lengths, remaining, prefix=()):
    if not lengths:
        if remaining == 0:
            yield prefix
        return
    for count in range(min(lengths[0], remaining) + 1):
        yield from allocations(lengths[1:], remaining - count, prefix + (count,))


def check_case(case, record, joint):
    square, ranks = case["fixed_complete_square"], case["column_rank_order"]
    source, missing = case["observed_ciphertext"], case["missing_count"]
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    assert set(source) <= set(COORDINATES)
    result, verified = record["exact_search"], record["verification"]
    losses = result["missing_full_ciphertext_positions"]
    full_length = len(source) + missing
    assert losses == sorted(set(losses)) and len(losses) == missing
    assert all(0 <= i < full_length for i in losses)
    assert full_length == result["nominal_coordinates"] == 170
    assert result["observed_coordinates"] == len(source) == 165
    assert result["missing_coordinates"] == missing == 5
    assert result["width"] == len(ranks) == 16
    assert result["integer_log_scale"] == SCALE
    assert result["quad_windows"] == full_length // 2 - 3 == 82
    assert isinstance(result["best_integer_score"], int)
    assert result["allocation_count_total"] == result["allocations_completed"] == 15504
    assert result["allocation_start"] == 0 and result["all_allocations_completed"]
    lengths = [full_length // len(ranks) + (c < full_length % len(ranks)) for c in range(len(ranks))]
    observed_allocations, start = [0] * len(ranks), 0
    for column in sorted(range(len(ranks)), key=ranks.__getitem__):
        observed_allocations[column] = sum(start <= p < start + lengths[column] for p in losses)
        start += lengths[column]
    assert observed_allocations == result["losses_per_physical_column"]
    padded = insert(source, losses, "?" * missing)
    assert padded == verified["padded_ciphertext"]
    domains = plaintext_domains(padded, ranks, square)
    assert verified["source_coordinates_preserved"] == len(source)
    assert verified["accepted_historical_plaintext"] is False
    mean = result["best_integer_score"] / (SCALE * result["quad_windows"])
    if joint:
        fill = result["filled_missing_coordinates"]
        assert len(fill) == missing and set(fill) <= set(COORDINATES)
        full = insert(source, losses, fill)
        text = decrypt(full, ranks, square)
        assert full == verified["filled_ciphertext"]
        assert text == verified["plaintext"]
        assert encrypt(text, ranks, square) == full
        assert "".join(c for i, c in enumerate(full) if i not in losses) == source
        assert all(letter in domain for letter, domain in zip(text, domains))
        assert verified["changed_retained_source_coordinates"] == 0
        assert verified["model_selected_coordinate_fills"] == missing
        assert verified["singleton_positions_before_filling"] == sum(len(d) == 1 for d in domains)
        assert verified["positions_selected_from_non_singleton_domains"] == [i for i, d in enumerate(domains) if len(d) > 1]
        assert verified["mean_quad_score"] == mean
        previous = record["marginal_alignment_rescored_with_concrete_completion"]
        previous_full = encrypt(previous["best_plaintext"], ranks, square)
        assert "".join(c for i, c in enumerate(previous_full) if i not in previous["loss_positions"]) == source
        assert previous["mean_quad_score"] == previous["best_integer_score"] / (82 * SCALE)
        advantage = result["best_integer_score"] - previous["best_integer_score"]
        assert record["joint_integer_advantage_over_best_filling_at_marginal_mask"] == advantage >= 0
        assert result["maximum_active_states"] <= 7 ** missing
        if case["kind"] == "control":
            truth, evaluation = case["evaluation_only"], record["control_evaluation"]
            assert evaluation["plaintext_matches_truth_exactly"] == (text == truth["plaintext"])
            assert evaluation["plaintext_hamming_distance_from_truth"] == sum(a != b for a, b in zip(text, truth["plaintext"]))
            assert evaluation["global_optimum_integer_advantage_over_truth"] == result["best_integer_score"] - evaluation["true_plaintext_integer_score"]
    else:
        assert verified["plaintext_domains"] == ["".join(d) for d in domains]
        assert verified["partial_plaintext"] == "".join(d[0] if len(d) == 1 else "?" for d in domains)
        assert verified["singleton_plaintext_positions"] == sum(len(d) == 1 for d in domains)
        assert verified["quantized_mean_domain_score"] == mean
        assert verified["missing_coordinate_values_assigned"] == 0
        representative = "".join(d[0] for d in domains)
        encoded = encrypt(representative, ranks, square)
        assert all(a == "?" or a == b for a, b in zip(padded, encoded))
        assert result["maximum_active_states"] <= 3 ** missing
    return lengths


def main():
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    cases = json.loads(input_path.read_text())["cases"]
    spec = importlib.util.spec_from_file_location("sparse_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    provenance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provenance)
    provenance.audit_provenance(cases)
    by_id = {case["id"]: case for case in cases}
    checked = 0
    for directory, engine, joint in [("p198_exact_sparse", "exact_sparse.cpp", False),
                                      ("p198_joint_exact", "exact_joint.cpp", True)]:
        folder = ROOT / "experiments" / directory
        report = json.loads((folder / "results.json").read_text())
        assert report["input_sha256"] == digest(input_path)
        assert report["engine_source_sha256"] == digest(folder / engine)
        assert report["newly_accepted_historical_plaintext_characters"] == 0
        assert {r["case_id"] for r in report["records"]} == set(by_id)
        for record in report["records"]:
            lengths = check_case(by_id[record["case_id"]], record, joint)
            checked += 1
        if joint:
            assert int(report["geometry_masks_per_full_case"]) == math.comb(170, 5)
            assert report["coordinate_fillings_per_geometry"] == 6 ** 5
            assert int(report["loss_and_fill_witnesses_per_full_case"]) == math.comb(170, 5) * 6 ** 5
        else:
            assert int(report["loss_masks_covered_per_full_case"]) == math.comb(170, 5)
            assert report["full_case_column_allocations"] == math.comb(20, 5)
    count = weighted_masks = peak_joint = peak_marginal = 0
    for allocation in allocations(lengths, 5):
        count += 1
        weighted_masks += math.prod(math.comb(n, loss) for n, loss in zip(lengths, allocation))
        peak_joint = max(peak_joint, math.prod(1 + 6 * loss for loss in allocation))
        peak_marginal = max(peak_marginal, math.prod(1 + 2 * loss for loss in allocation))
    assert count == math.comb(20, 5) == 15504
    assert weighted_masks == math.comb(170, 5) == 1115034284
    assert peak_joint == 7 ** 5 and peak_marginal == 3 ** 5
    print(f"Verified {checked} recorded marginal/joint source witnesses and count/arithmetic checks.")
    print("No model lookups or searches rerun; this is not an optimality proof.")


if __name__ == "__main__":
    main()
