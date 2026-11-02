"""Exact, language-ranked common-plaintext decoding of two damaged witnesses.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The historical reading remains conditional on the common-plaintext model,
the already published repair of witness D, the fixed key, and the language
objective. Source transcriptions are never modified by this experiment.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"
SCALE = 1 << 24
EXPECTED = {
    "military_quad": "fc450633e557d477d009fd9f682a0d6c96629d48a532c1dd2fbc42af0c73b46d",
    "military_six": "79e1474e78afa0d208ffe4306b31ed3531786c2fc6a0c7efb4d2f3a7fd5e4b5a",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def untranspose(ciphertext, ranks):
    width = len(ranks)
    columns = [""] * width
    offset = 0
    for column in sorted(range(width), key=ranks.__getitem__):
        length = len(range(column, len(ciphertext), width))
        columns[column] = ciphertext[offset:offset + length]
        offset += length
    assert offset == len(ciphertext)
    return "".join(columns[column][row]
                   for row in range((len(ciphertext) + width - 1) // width)
                   for column in range(width) if row < len(columns[column]))


def transpose(stream, ranks):
    return "".join(stream[column::len(ranks)]
                   for column in sorted(range(len(ranks)), key=ranks.__getitem__))


def square_pairs(square):
    assert len(square) == len(set(square)) == 36 and set(square) == set(ALPHABET)
    return {symbol: COORDINATES[i // 6] + COORDINATES[i % 6]
            for i, symbol in enumerate(square)}


def symbol_cost(pair, observations):
    return sum(a != b for observed in observations
               for a, b in zip(pair, observed) if b != "?")


def prepare_input():
    certificate = json.loads((ROOT / "data/certificates/p109_parallel.json").read_text())
    previous = next(row for row in json.loads((ROOT / "data/prior_readings.json").read_text())["messages"]
                    if row["id"] == "p109")
    variant = next(row for row in previous["verified_variants"] if row["id"] == "norbert18")
    ciphertexts = {
        "B": certificate["source_B"]["ciphertext"],
        "D_after_Norbert18": variant["verification"]["corrected_ciphertext"],
    }
    ranks = previous["key"]["column_rank_order"]
    square = previous["key"]["square"]
    pairs = square_pairs(square)
    streams = {name: untranspose(text, ranks) for name, text in ciphertexts.items()}
    assert {len(text) for text in ciphertexts.values()} == {248}
    assert all(transpose(streams[name], ranks) == text for name, text in ciphertexts.items())
    domains = certificate["analysis"]["common_plaintext_model"]["domains"]
    candidate = "".join(row["readable_candidate_character"] for row in domains)
    costs, minima, observations = [], [], []
    for position, domain in enumerate(domains):
        observed = [streams[name][2 * position:2 * position + 2] for name in ciphertexts]
        assert observed == [domain["pair_B"], domain["pair_D"]]
        row = [symbol_cost(pairs[letter], observed) for letter in ALPHABET]
        minimum = min(row)
        assert minimum == domain["minimum_cost"]
        assert "".join(sorted(ALPHABET[i] for i, cost in enumerate(row) if cost == minimum)) == domain["minimum_cost_characters"]
        assert row[ALPHABET.index(candidate[position])] == domain["readable_candidate_cost"]
        costs.append(row)
        minima.append(minimum)
        observations.append(observed)
    assert sum(minima) == 42
    assert sum(row[ALPHABET.index(letter)] for row, letter in zip(costs, candidate)) == 46
    return {
        "case": "p109", "alphabet": ALPHABET, "ranks": ranks, "square": square,
        "ciphertexts": ciphertexts, "intermediate_observations": observations,
        "position_costs": costs, "position_minima": minima,
        "earlier_editorial_candidate": candidate,
        "D_repair": variant["ciphertext_edits"],
        "source_reference": "data/certificates/p109_parallel.json",
    }


def load_tables(quad, six):
    # Reuse the independently written Python table reader for cross-checking
    # the C++ objective, including the hashed sixgram lookup.
    spec = importlib.util.spec_from_file_location("completion_tables", ROOT / "experiments/p215_completion/compute_completions.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Tables(quad, "military_quad", six)


def objective_score(text, tables, coefficient4, coefficient6):
    return (coefficient4 * sum(tables.units(text[i:i + 4]) for i in range(len(text) - 3))
            + coefficient6 * sum(tables.units(text[i:i + 6]) for i in range(len(text) - 5)))


def execute(binary, costs, budget, top_k, order, coefficient4, coefficient6,
            quad, six, work, name, max_states, quiet=False):
    input_path = work / f"{name}.costs"
    output_path = work / f"{name}.json"
    output_path.unlink(missing_ok=True)
    lines = [f"{len(costs)} {budget} {top_k} {order} {coefficient4} {coefficient6} {max_states}"]
    lines.extend(" ".join(map(str, row)) for row in costs)
    input_path.write_text("\n".join(lines) + "\n")
    subprocess.run([str(binary), str(input_path), str(quad), str(six), str(output_path)],
                   check=True, stderr=subprocess.DEVNULL if quiet else None)
    return json.loads(output_path.read_text())


def exhaustive_controls(binary, tables, quad, six, work):
    rng = random.Random(1918109)
    reports = []
    for order in (3, 5):
        domains = ["AB", "AC", "BC", "AD", "BD", "AC", "CD", "AB", "BC"]
        budget, top_k = 3, 8
        costs = []
        for domain in domains:
            row = [budget + 1] * 36
            for symbol in domain:
                row[ALPHABET.index(symbol)] = rng.randrange(3)
            row[ALPHABET.index(domain[0])] = 0
            costs.append(row)
        coefficient4, coefficient6 = (3, 7) if order == 5 else (1, 0)
        result = execute(binary, costs, budget, top_k, order, coefficient4, coefficient6,
                         quad, six, work, f"control-order{order}", 100000, quiet=True)
        brute = [[] for _ in range(budget + 1)]
        for symbols in itertools.product(*domains):
            text = "".join(symbols)
            cost = sum(row[ALPHABET.index(letter)] for row, letter in zip(costs, text))
            if cost <= budget:
                brute[cost].append((objective_score(text, tables, coefficient4, coefficient6), text))
        for row in result["by_exact_excess_budget"]:
            expected = sorted(brute[row["budget"]], key=lambda item: (-item[0], item[1]))[:top_k]
            actual = [(candidate["score"], candidate["plaintext"]) for candidate in row["candidates"]]
            assert actual == expected
        reports.append({"order": order, "finite_completions_enumerated": 512,
                        "budgets": list(range(budget + 1)), "top_k": top_k,
                        "all_rankings_match_exhaustive_enumeration": True})

    # A zero objective exposes tie behavior and permits independently deriving
    # the expected answer by sorting all finite-domain strings.
    tie_domains = ["A0"] * 8
    tie_costs = [[0 if symbol == "A" else 1 if symbol == "0" else 5
                  for symbol in ALPHABET] for _ in tie_domains]
    tied = execute(binary, tie_costs, 4, 10, 3, 0, 0, quad, six, work,
                   "control-lexical-ties", 100000, quiet=True)
    for row in tied["by_exact_excess_budget"]:
        expected = sorted("".join(symbols) for symbols in itertools.product(*tie_domains)
                          if symbols.count("0") == row["budget"])[:10]
        assert [candidate["plaintext"] for candidate in row["candidates"]] == expected

    # Verify that coordinate costs commute with two independently permuted
    # observation streams, including erasures and contradictory observations.
    pairs = square_pairs(ALPHABET)
    source_plain = "ABACBDAC"
    encoded = "".join(pairs[symbol] for symbol in source_plain)
    ranks = ([3, 1, 4, 2], [2, 5, 1, 4, 3])
    witnesses = [list(transpose(encoded, key)) for key in ranks]
    witnesses[0][3] = "?"
    witnesses[1][7] = "X" if witnesses[1][7] != "X" else "D"
    witnesses = ["".join(row) for row in witnesses]
    streams = [untranspose(text, key) for text, key in zip(witnesses, ranks)]
    minimum_sum = 0
    for position in range(len(source_plain)):
        observed = [stream[2 * position:2 * position + 2] for stream in streams]
        minimum_sum += min(symbol_cost(pair, observed) for pair in pairs.values())
    assert minimum_sum == 1
    checked = 0
    for symbols in itertools.product("AB", repeat=8):
        text = "".join(symbols)
        encoded_candidate = "".join(pairs[symbol] for symbol in text)
        direct = sum(a != b for witness, key in zip(witnesses, ranks)
                     for a, b in zip(transpose(encoded_candidate, key), witness) if b != "?")
        local = sum(symbol_cost(pairs[symbol], [stream[2 * position:2 * position + 2]
                                              for stream in streams])
                    for position, symbol in enumerate(text))
        assert direct == local
        checked += 1
    return {"random_seed": 1918109, "exhaustive_markov_controls": reports,
            "lexical_tie_control_completions": 256, "lexical_ties_verified": True,
            "independent_transposition_cost_control_completions": checked,
            "irreducible_coordinate_disagreement_control": minimum_sum}


def candidate_record(data, text, global_start, score, denominator, excess, rank):
    pairs = square_pairs(data["square"])
    stream = ["?"] * (2 * len(data["position_costs"]))
    for position, letter in enumerate(text, global_start):
        stream[2 * position:2 * position + 2] = pairs[letter]
    encrypted_subset = transpose("".join(stream), data["ranks"])
    changed = {}
    fills = {}
    for name, source in data["ciphertexts"].items():
        changed[name] = [i for i, (expected, actual) in enumerate(zip(encrypted_subset, source))
                         if expected != "?" and actual != "?" and expected != actual]
        fills[name] = [{"received_index": i, "coordinate": expected}
                       for i, (expected, actual) in enumerate(zip(encrypted_subset, source))
                       if expected != "?" and actual == "?"]
    stop = global_start + len(text)
    minimum = sum(data["position_minima"][global_start:stop])
    local_cost = sum(data["position_costs"][position][ALPHABET.index(letter)]
                     for position, letter in enumerate(text, global_start))
    assert sum(map(len, changed.values())) == local_cost == minimum + excess
    outside = [{"plaintext_index": position, "symbol": letter,
                "extra_coordinate_substitutions": data["position_costs"][position][ALPHABET.index(letter)] - data["position_minima"][position]}
               for position, letter in enumerate(text, global_start)
               if data["position_costs"][position][ALPHABET.index(letter)] > data["position_minima"][position]]
    return {"rank": rank, "integer_objective": score, "display_score": score / denominator,
            "plaintext": text, "global_plaintext_span": [global_start, stop],
            "excess_coordinate_substitutions": excess, "total_coordinate_substitutions": local_cost,
            "changed_received_indices": changed, "source_erasure_fills": fills,
            "positions_above_their_minimum_cost": outside,
            "reencrypted_coordinate_subset": encrypted_subset,
            "independent_reencryption_cost_check": True,
            "accepted_as_historical_plaintext": False}


def solve(data, args, binary, tables, scope, objective):
    start, stop = (0, 124) if scope == "full" else (6, 114)
    rows = data["position_costs"][start:stop]
    minima = data["position_minima"][start:stop]
    costs = [[value - minimum for value in row] for row, minimum in zip(rows, minima)]
    length = stop - start
    mixed = objective == "military_mixed_30_70"
    coefficient4, coefficient6 = (3 * (length - 5), 7 * (length - 3)) if mixed else (1, 0)
    denominator = 10 * (length - 3) * (length - 5) * SCALE if mixed else (length - 3) * SCALE
    raw = execute(binary, costs, args.max_budget, args.top_k, 5 if mixed else 3,
                  coefficient4, coefficient6, args.military_quad, args.military_six,
                  args.work_dir, f"{scope}-{objective}", args.max_states)
    candidates_by_budget = []
    for row in raw["by_exact_excess_budget"]:
        candidates = []
        for candidate in row["candidates"]:
            assert candidate["score"] == objective_score(candidate["plaintext"], tables, coefficient4, coefficient6)
            candidates.append(candidate_record(data, candidate["plaintext"], start, candidate["score"],
                                               denominator, row["budget"], candidate["rank"]))
        candidates_by_budget.append({"excess_budget": row["budget"],
                                     "total_coordinate_cost": sum(minima) + row["budget"],
                                     "candidates": candidates})
    earlier = data["earlier_editorial_candidate"][start:stop]
    earlier_cost = sum(row[ALPHABET.index(letter)] for row, letter in zip(rows, earlier))
    earlier_score = objective_score(earlier, tables, coefficient4, coefficient6)
    earlier_rank = next((candidate["rank"] for row in candidates_by_budget for candidate in row["candidates"]
                         if candidate["plaintext"] == earlier), None)
    return {
        "scope": scope, "global_plaintext_span": [start, stop], "objective": objective,
        "markov_order": 5 if mixed else 3, "integer_log_scale": SCALE,
        "coefficient4": coefficient4, "coefficient6": coefficient6,
        "integer_denominator_for_display": denominator,
        "minimum_coordinate_substitutions": sum(minima),
        "top_k_per_exact_budget": args.top_k, "maximum_excess_budget": args.max_budget,
        "dp_counts": {key: raw[key] for key in ("peak_suffix_budget_states", "candidate_path_extensions", "layer_states")},
        "by_exact_excess_budget": candidates_by_budget,
        "earlier_editorial_candidate_comparison": {
            "plaintext": earlier, "total_coordinate_cost": earlier_cost,
            "excess_coordinate_cost": earlier_cost - sum(minima),
            "integer_objective": earlier_score, "display_score": earlier_score / denominator,
            "rank_within_reported_top_k_at_its_exact_budget": earlier_rank,
            "not_used_as_a_search_constraint": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--military-quad", type=Path, required=True)
    parser.add_argument("--military-six", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--max-budget", type=int, default=6)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-states", type=int, default=3000000)
    parser.add_argument("--scopes", nargs="+", choices=("full", "body"), default=["full", "body"])
    parser.add_argument("--objectives", nargs="+", choices=("military_quad", "military_mixed_30_70"),
                        default=["military_quad", "military_mixed_30_70"])
    parser.add_argument("--output", type=Path, default=HERE / "p109_results.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.max_budget <= 10 or not 1 <= args.top_k <= 20:
        parser.error("Use a budget between0 and10 and top-k between1 and20")
    for path, kind in ((args.military_quad, "military_quad"), (args.military_six, "military_six")):
        if digest(path) != EXPECTED[kind]:
            parser.error(f"Hash mismatch for {kind}")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    binary = args.work_dir / "decode"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                    str(HERE / "decode.cpp"), "-o", str(binary)], check=True)
    data = prepare_input()
    tables = load_tables(args.military_quad, args.military_six)
    controls = exhaustive_controls(binary, tables, args.military_quad, args.military_six, args.work_dir)
    runs = []
    for scope in args.scopes:
        for objective in args.objectives:
            print(f"Solving {scope}, {objective}, exact excess budgets0..{args.max_budget}", flush=True)
            run = solve(data, args, binary, tables, scope, objective)
            runs.append(run)
            for row in run["by_exact_excess_budget"]:
                best = row["candidates"][0]
                print(json.dumps({"scope": scope, "objective": objective, "cost": row["total_coordinate_cost"],
                                  "score": best["display_score"], "best": best["plaintext"]}), flush=True)
    result = {
        "schema": "adfgvx-exact-parallel-decoder-v1", "project": "ADFGVX Cipher",
        "authors": "icekylinx and GPT-6 Astra Pro", "case": "p109",
        "input_projection_sha256": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
        "engine_source_sha256": digest(HERE / "decode.cpp"), "model_sha256": EXPECTED,
        "assumptions": [
            "B and the explicitly repaired D are compared as one plaintext in the selected span.",
            "The November1-3 key and Norbert's earlier D repair are fixed inputs.",
            "Each mismatch against a known coordinate costs1; an erased coordinate costs0. Witnesses have equal weight.",
            "The full run uses positions0..123. The body sensitivity run uses positions6..113 and excludes both the leading fields and differing endings.",
            "All36 symbols are allowed at every position, subject only to the exact coordinate-cost budget.",
        ],
        "optimization": "Exact top K for each excess budget using additive integer4/6gram scores; ties use ASCII lexical order. No beam pruning, crib constraint, or editorial-candidate training is used.",
        "interpretation": "Model-ranked editorial hypotheses, not new source-fixed letters or posterior probabilities. Separate witness wording, unmodelled source errors, and other D repairs remain possible.",
        "controls": controls, "input": data, "runs": runs,
        "newly_accepted_historical_plaintext_characters": 0,
    }
    if args.verify:
        if json.loads(args.output.read_text()) != result:
            raise SystemExit("Stored parallel-decoder result differs from full recomputation")
        print("Exact multi-witness result fully reproduced")
    else:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
