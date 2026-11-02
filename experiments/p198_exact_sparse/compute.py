"""Reproduce exact fixed-key scattered-loss alignment and its controls.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The full square is a fixed hypothesis. Missing coordinates are marginalized
within each quadgram; no missing-coordinate values are inferred here.
"""
from __future__ import annotations

import argparse
import array
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt, plaintext_domains, untranspose

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"
SCALE = 1 << 24
MODEL_SHA = "fc450633e557d477d009fd9f682a0d6c96629d48a532c1dd2fbc42af0c73b46d"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def padded_source(source, losses):
    losses = set(losses)
    observed = iter(source)
    result = "".join("?" if position in losses else next(observed)
                     for position in range(len(source) + len(losses)))
    assert next(observed, None) is None
    return result


def domain_ids(padded, ranks):
    stream = untranspose(padded, ranks)
    answer = []
    for first, second in zip(stream[::2], stream[1::2]):
        answer.append(48 if first == second == "?" else
                      36 + COORDINATES.index(second) if first == "?" else
                      42 + COORDINATES.index(first) if second == "?" else
                      6 * COORDINATES.index(first) + COORDINATES.index(second))
    return answer


class Scorer:
    def __init__(self, model, table):
        self.quad = array.array("f")
        self.quad.frombytes(Path(model).read_bytes())
        raw = Path(table).read_bytes()
        assert struct.unpack_from("<8sII", raw) == (b"M49QF32\0", 49 ** 4, SCALE)
        self.table = array.array("f")
        self.table.frombytes(raw[16:])
        assert len(self.table) == 49 ** 4

    def exact_units(self, ids):
        total = 0
        for a, b, c, d in zip(ids, ids[1:], ids[2:], ids[3:]):
            value = self.table[((a * 49 + b) * 49 + c) * 49 + d] * SCALE
            assert value.is_integer()
            total += int(value)
        return total

    @lru_cache(maxsize=None)
    def direct_gram(self, domains):
        probability = 0.0
        for letters in itertools.product(*domains):
            index = 0
            for letter in letters:
                index = 36 * index + ALPHABET.index(letter)
            probability += 10 ** self.quad[index]
        return math.log10(probability / math.prod(map(len, domains)))

    def direct_score(self, domains):
        return sum(self.direct_gram(tuple(domains[i:i + 4])) for i in range(len(domains) - 3)) / (len(domains) - 3)

    def verify_table_windows(self, ids, domains):
        worst = 0.0
        for i in range(len(ids) - 3):
            code = 0
            for value in ids[i:i + 4]:
                code = code * 49 + value
            direct = self.direct_gram(tuple(domains[i:i + 4]))
            error = abs(self.table[code] - direct)
            worst = max(worst, error)
            assert error <= 2 ** -21 + 1e-12
        return worst


def execute(binary, case, table, work, name=None, allocation_start=0, allocation_count=0):
    name = name or case["id"]
    config = work / (name + ".cfg")
    output = work / (name + ".engine.json")
    output.unlink(missing_ok=True)
    config.write_text(
        f"{len(case['column_rank_order'])} {case['missing_count']} {allocation_start} {allocation_count} 100000\n"
        + case["fixed_complete_square"] + "\n"
        + " ".join(map(str, case["column_rank_order"])) + "\n"
        + case["observed_ciphertext"] + "\n")
    subprocess.run([str(binary), "solve", str(config), str(table), str(output)],
                   check=True, stderr=subprocess.DEVNULL)
    return json.loads(output.read_text())


def build_table(binary, model, case, work):
    table = work / (case["id"] + ".marginal.bin")
    subprocess.run([str(binary), "build", str(model), case["fixed_complete_square"], str(table)], check=True)
    return table


def verify_winner(case, result, scorer):
    losses = result["missing_full_ciphertext_positions"]
    assert losses == sorted(set(losses)) and len(losses) == case["missing_count"]
    padded = padded_source(case["observed_ciphertext"], losses)
    domains = plaintext_domains(padded, case["column_rank_order"], case["fixed_complete_square"])
    ids = domain_ids(padded, case["column_rank_order"])
    assert scorer.exact_units(ids) == result["best_integer_score"]
    error = scorer.verify_table_windows(ids, domains)
    representative = "".join(domain[0] for domain in domains)
    reencrypted = encrypt(representative, case["column_rank_order"], case["fixed_complete_square"])
    assert all(a == "?" or a == b for a, b in zip(padded, reencrypted))
    assert "".join(c for i, c in enumerate(reencrypted) if i not in set(losses)) == case["observed_ciphertext"]
    return {
        "padded_ciphertext": padded,
        "partial_plaintext": "".join(domain if len(domain) == 1 else "?" for domain in domains),
        "plaintext_domains": domains,
        "singleton_plaintext_positions": sum(len(domain) == 1 for domain in domains),
        "source_coordinates_preserved": len(case["observed_ciphertext"]),
        "independent_reencryption_check": True,
        "quantized_mean_domain_score": result["best_integer_score"] / ((len(domains) - 3) * SCALE),
        "independent_unquantized_mean_domain_score": scorer.direct_score(domains),
        "maximum_checked_quad_table_rounding_error": error,
        "missing_coordinate_values_assigned": 0,
        "accepted_historical_plaintext": False,
    }


def exhaustive_controls(binary, model, table, square, work):
    controls = []
    cases = [([3, 1, 4, 2], "DERSTABMELDE"),
             ([4, 1, 6, 2, 5, 3], "DERSTABMELDET"),
             ([3, 13, 2, 12, 1, 11, 15, 8, 9, 4, 5, 14, 6, 10, 7, 16], "DERSTABMELDE")]
    scorer = Scorer(model, table)
    for key, text in cases:
        full = encrypt(text, key, square)
        removed = [1, len(full) - 3]
        source = "".join(c for i, c in enumerate(full) if i not in removed)
        case = {"id": "small_width_" + str(len(key)), "column_rank_order": key,
                "fixed_complete_square": square, "observed_ciphertext": source, "missing_count": 2}
        result = execute(binary, case, table, work)
        best = None
        worst_error = 0.0
        examined = 0
        for losses in itertools.combinations(range(len(full)), 2):
            padded = padded_source(source, losses)
            ids = domain_ids(padded, key)
            score = scorer.exact_units(ids)
            domains = plaintext_domains(padded, key, square)
            worst_error = max(worst_error, scorer.verify_table_windows(ids, domains))
            candidate = (-score, losses)
            if best is None or candidate < best:
                best = candidate
            examined += 1
        assert examined == math.comb(len(full), 2)
        assert -best[0] == result["best_integer_score"]
        assert list(best[1]) == result["missing_full_ciphertext_positions"]
        assert result["all_allocations_completed"]
        controls.append({"case": case, "nominal_coordinates": len(full),
                         "all_loss_masks_enumerated": examined,
                         "exact_dp_matches_exhaustive_score_and_canonical_mask": True,
                         "best_loss_positions": list(best[1]), "best_integer_score": -best[0],
                         "maximum_independent_table_error": worst_error})

    # The constant table makes every loss mask tie. The canonical first mask
    # must survive every DP merge, even though losses are visited row-wise.
    constant = work / "constant-tie-table.bin"
    constant.write_bytes(struct.pack("<8sII", b"M49QF32\0", 49 ** 4, SCALE)
                         + struct.pack("<f", -4.0) * (49 ** 4))
    tied = execute(binary, controls[-1]["case"], constant, work, name="constant-tie-control")
    assert tied["missing_full_ciphertext_positions"] == [0, 1]
    return {"exhaustive_small_controls": controls,
            "total_loss_masks_independently_enumerated": sum(row["all_loss_masks_enumerated"] for row in controls),
            "constant_objective_canonical_mask": [0, 1],
            "constant_objective_tie_check_passed": True}


def audit_provenance(cases):
    source = json.loads((ROOT / "experiments/open_targets/sparse_results.json").read_text())["records"]
    by_name = {row["case"]["id"] + ".json": row for row in source}
    target = next(row for row in json.loads((ROOT / "data/messages.json").read_text())["messages"] if row["id"] == "p198")
    for case in cases:
        earlier = by_name[case["source_record_name"]]
        assert earlier["input_record_sha256"] == case["source_record_sha256"]
        assert earlier["case"]["ciphertext"] == case["observed_ciphertext"]
        assert earlier["case"]["ranks"] == case["column_rank_order"]
        expected = (earlier["case"]["evaluation_only"]["square"] if case["kind"] == "control"
                    else earlier["best"]["square"])
        assert expected == case["fixed_complete_square"]
        assert all(a == "?" or a == b for a, b in zip(case["partial_historical_square"], expected))
        if case["kind"] == "historical":
            assert case["observed_ciphertext"] == target["transcript"]["analysis_ciphertext"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--input", type=Path, default=HERE / "inputs.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if sys.byteorder != "little" or digest(args.model) != MODEL_SHA:
        parser.error("The recorded little-endian military quad model is required")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    binary = args.work_dir / "exact_sparse"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                    str(HERE / "exact_sparse.cpp"), "-o", str(binary)], check=True)
    cases = json.loads(args.input.read_text())["cases"]
    audit_provenance(cases)
    first_table = build_table(binary, args.model, cases[0], args.work_dir)
    controls = exhaustive_controls(binary, args.model, first_table, cases[0]["fixed_complete_square"], args.work_dir)
    records = []
    for index, case in enumerate(cases):
        print("Exact alignment:", case["id"], flush=True)
        table = first_table if index == 0 else build_table(binary, args.model, case, args.work_dir)
        scorer = Scorer(args.model, table)
        result = execute(binary, case, table, args.work_dir)
        assert result["all_allocations_completed"] and result["allocations_completed"] == 15504
        verified = verify_winner(case, result, scorer)
        record = {"case_id": case["id"], "marginal_table_sha256": digest(table),
                  "exact_search": result, "verification": verified}
        if case["kind"] == "control":
            truth = case["evaluation_only"]
            domains = verified["plaintext_domains"]
            true_padded = padded_source(case["observed_ciphertext"], truth["missing_full_ciphertext_positions_0based"])
            true_domains = plaintext_domains(true_padded, case["column_rank_order"], case["fixed_complete_square"])
            true_units = scorer.exact_units(domain_ids(true_padded, case["column_rank_order"]))
            record["control_evaluation"] = {
                "truth_in_all_winning_domains": all(ch in domain for ch, domain in zip(truth["plaintext"], domains)),
                "correct_singleton_positions": sum(domain == ch for ch, domain in zip(truth["plaintext"], domains)),
                "true_loss_mask_integer_score": true_units,
                "true_loss_mask_unquantized_score": scorer.direct_score(true_domains),
                "global_optimum_integer_advantage_over_true_loss_mask": result["best_integer_score"] - true_units,
                "true_plaintext_reencryption_matches_source_after_winning_losses": "".join(
                    ch for i, ch in enumerate(truth["full_ciphertext"])
                    if i not in set(result["missing_full_ciphertext_positions"])) == case["observed_ciphertext"],
            }
        else:
            previous = case["earlier_heuristic_result"]
            record["earlier_heuristic_comparison"] = {
                "same_loss_mask_as_the_global_quantized_optimum": previous["missing_full_ciphertext_positions_0based"] == result["missing_full_ciphertext_positions"],
                "earlier_unquantized_score": previous["score"],
                "scope": "Fixed at exactly the earlier heuristic's completed square. Other square completions are not bounded by this result.",
            }
        records.append(record)
        print(json.dumps({"case": case["id"], "score": verified["quantized_mean_domain_score"],
                          "losses": result["missing_full_ciphertext_positions"],
                          "partial": verified["partial_plaintext"]}), flush=True)
    output = {
        "schema": "adfgvx-exact-scattered-loss-v1", "project": "ADFGVX Cipher",
        "authors": "icekylinx and GPT-6 Astra Pro", "input_sha256": digest(args.input),
        "source_record_reference": "experiments/open_targets/sparse_results.json",
        "engine_source_sha256": digest(HERE / "exact_sparse.cpp"), "base_model_sha256": MODEL_SHA,
        "loss_masks_covered_per_full_case": str(math.comb(170, 5)),
        "full_case_column_allocations": math.comb(20, 5),
        "objective": "Sum of stored float32 log10 mean-domain quadgram frequencies, represented exactly at scale2^24. Missing coordinate alternatives are uniformly averaged separately within each quadgram.",
        "exactness_scope": "Global optimum over all five-loss masks for each fixed complete square and fixed transposition. Derived table quantization is part of the objective. No square search or hole-value assignment is included.",
        "tie_order": "Lexicographically earliest increasing list of missing full-ciphertext positions",
        "controls": controls, "records": records,
        "newly_accepted_historical_plaintext_characters": 0,
    }
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored exact sparse-loss results differ from full recomputation")
        print("Exact sparse-loss tables, controls, optima, and source witnesses fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
