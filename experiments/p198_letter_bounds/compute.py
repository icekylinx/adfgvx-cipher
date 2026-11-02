"""Exact letter-count bounds over a partial square and five source losses.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
These are attainable finite-source bounds, not language probabilities or
proofs that a historical message must contain a particular number of digits.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fill_frame(source, losses, fill):
    replacements, iterator = dict(zip(losses, fill)), iter(source)
    result = "".join(replacements[i] if i in replacements else next(iterator)
                     for i in range(len(source) + len(losses)))
    assert next(iterator, None) is None
    return result


def representative_completions(partial):
    unknown = [i for i, c in enumerate(partial) if c == "?"]
    letters = sorted(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - set(partial))
    digits = sorted(set("0123456789") - set(partial))
    assert len(unknown) == len(letters) + len(digits)
    for letter_cells in itertools.combinations(unknown, len(letters)):
        square = list(partial)
        for cell, letter in zip(letter_cells, letters):
            square[cell] = letter
        for cell, digit in zip((i for i in unknown if i not in letter_cells), digits):
            square[cell] = digit
        yield list(letter_cells), "".join(square)


def execute(binary, case, square, maximize, work, name):
    config, output = work / (name + ".cfg"), work / (name + ".engine.json")
    output.unlink(missing_ok=True)
    config.write_text(f"{len(case['column_rank_order'])} {case['missing_count']} 0 0 100000 {int(maximize)}\n"
                      + square + "\n" + " ".join(map(str, case["column_rank_order"])) + "\n"
                      + case["observed_ciphertext"] + "\n")
    subprocess.run([str(binary), "solve", str(config), str(output)], check=True,
                   stderr=subprocess.DEVNULL)
    return json.loads(output.read_text())


def verify_witness(case, square, result):
    losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    assert len(losses) == len(fill) == case["missing_count"]
    assert losses == sorted(set(losses)) and set(fill) <= set(COORDINATES)
    full = fill_frame(case["observed_ciphertext"], losses, fill)
    plaintext = decrypt(full, case["column_rank_order"], square)
    letters = sum(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in plaintext)
    assert letters == result["ordinary_letter_count"]
    assert result["best_signed_letter_count"] == (letters if result["maximize_letters"] else -letters)
    assert encrypt(plaintext, case["column_rank_order"], square) == full
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    assert result["all_allocations_completed"]
    return {"representative_plaintext": plaintext, "filled_ciphertext": full,
            "ordinary_letter_count": letters, "digit_count": len(plaintext) - letters,
            "source_coordinates_preserved": len(case["observed_ciphertext"]),
            "changed_retained_coordinates": 0, "model_selected_coordinates": 0,
            "count_objective_selected_coordinates": len(fill),
            "reencryption_verified": True, "accepted_historical_plaintext": False}


def exhaustive_controls(binary, work, square):
    partial = list(square)
    partial[square.index("A")] = partial[square.index("6")] = "?"
    completions = list(representative_completions("".join(partial)))
    assert len(completions) == 2
    reports = []
    settings = [([3, 1, 4, 2], "DERSTA", 1),
                ([4, 1, 6, 2, 5, 3], "DERSTAB", 2),
                ([3, 13, 2, 12, 1, 11, 15, 8, 9, 4, 5, 14, 6, 10, 7, 16], "DERSTABMEL", 2)]
    for control_index, (ranks, text, missing) in enumerate(settings):
        full = encrypt(text, ranks, square)
        planted = [1] if missing == 1 else [1, len(full) - 3]
        source = "".join(c for i, c in enumerate(full) if i not in planted)
        case = {"column_rank_order": ranks, "observed_ciphertext": source, "missing_count": missing}
        for membership_index, (letter_cells, representative) in enumerate(completions):
            best = {False: None, True: None}
            count = 0
            for losses in itertools.combinations(range(len(full)), missing):
                for values in itertools.product(COORDINATES, repeat=missing):
                    fill = "".join(values)
                    plaintext = decrypt(fill_frame(source, losses, fill), ranks, representative)
                    letters = sum(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in plaintext)
                    for maximize in best:
                        candidate = (-letters if maximize else letters, losses, fill)
                        if best[maximize] is None or candidate < best[maximize]:
                            best[maximize] = candidate
                    count += 1
            checks = []
            for maximize, expected in best.items():
                name = f"control_{control_index}_{membership_index}_{int(maximize)}"
                result = execute(binary, case, representative, maximize, work, name)
                assert result["ordinary_letter_count"] == (-expected[0] if maximize else expected[0])
                assert result["missing_full_ciphertext_positions"] == list(expected[1])
                assert result["filled_missing_coordinates"] == expected[2]
                verify_witness(case, representative, result)
                checks.append({"maximize_letters": maximize, "ordinary_letter_count": result["ordinary_letter_count"],
                               "loss_positions": list(expected[1]), "fill": expected[2], "exact_match": True})
            reports.append({"width": len(ranks), "nominal_coordinates": len(full), "losses": missing,
                            "letter_cells_at_unknown_positions": letter_cells, "representative_square": representative,
                            "witnesses_enumerated": count, "checks": checks})
    return {"partial_square_with_two_membership_assignments": "".join(partial),
            "total_witnesses_enumerated": sum(r["witnesses_enumerated"] for r in reports),
            "records": reports}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    binary = args.work_dir / "exact_letter_bounds"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                    str(HERE / "exact_letter_bounds.cpp"), "-o", str(binary)], check=True)
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    cases = json.loads(input_path.read_text())["cases"]
    spec = importlib.util.spec_from_file_location("sparse_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    provenance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provenance)
    provenance.audit_provenance(cases)
    controls = exhaustive_controls(binary, args.work_dir, cases[0]["fixed_complete_square"])
    positive = []
    for case in cases:
        if case["kind"] != "control":
            continue
        bounds = []
        for maximize in [False, True]:
            result = execute(binary, case, case["fixed_complete_square"], maximize, args.work_dir,
                             case["id"] + "_" + str(int(maximize)))
            verified = verify_witness(case, case["fixed_complete_square"], result)
            if maximize:
                assert result["ordinary_letter_count"] == len(case["evaluation_only"]["plaintext"]) == 85
            bounds.append({"exact_search": result, "verification": verified})
        positive.append({"case_id": case["id"], "true_square_supplied": True, "bounds": bounds})
    selected = next(case for case in cases if case["id"] == "p198_Nov13-15b")
    partial = selected["partial_historical_square"]
    completions = list(representative_completions(partial))
    assert len(completions) == math.comb(8, 2) == 28
    rows = []
    for index, (letter_cells, square) in enumerate(completions):
        bounds = []
        for maximize in [False, True]:
            result = execute(binary, selected, square, maximize, args.work_dir,
                             "historical_" + str(index) + "_" + str(int(maximize)))
            verified = verify_witness(selected, square, result)
            assert result["allocations_completed"] == 15504
            bounds.append({"exact_search": result, "verification": verified})
        rows.append({"letter_cells_at_unknown_positions": letter_cells, "representative_complete_square": square,
                     "bounds": bounds})
        print(json.dumps({"membership": index + 1, "letter_cells": letter_cells,
                          "minimum_letters": bounds[0]["verification"]["ordinary_letter_count"],
                          "maximum_letters": bounds[1]["verification"]["ordinary_letter_count"]}), flush=True)
    global_min = min(row["bounds"][0]["verification"]["ordinary_letter_count"] for row in rows)
    global_max = max(row["bounds"][1]["verification"]["ordinary_letter_count"] for row in rows)
    output = {"schema": "adfgvx-partial-square-letter-count-bounds-v1", "project": "ADFGVX Cipher",
              "authors": "icekylinx and GPT-6 Astra Pro", "input_sha256": digest(input_path),
              "engine_source_sha256": digest(HERE / "exact_letter_bounds.cpp"),
              "case_id": selected["id"], "partial_square": partial,
              "column_rank_order": selected["column_rank_order"], "ordinary_letters": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
              "unknown_cell_membership_assignments": len(completions),
              "complete_square_extensions_covered": str(math.factorial(8)),
              "complete_square_extensions_per_membership": math.factorial(2) * math.factorial(6),
              "loss_and_fill_witnesses_per_complete_square": str(math.comb(170, 5) * 6 ** 5),
              "controls": controls, "positive_controls": positive, "membership_results": rows,
              "attainable_global_minimum_letters": global_min, "attainable_global_maximum_letters": global_max,
              "implied_attainable_global_minimum_digits": 85 - global_max,
              "implied_attainable_global_maximum_digits": 85 - global_min,
              "scope": "All 8! complete-square extensions of the recorded partial Nov13-15b square, fixed transposition, exactly five deleted coordinates with arbitrary inserted values, and all 165 received coordinates preserved in order.",
              "limits": ["The true historical digit count is unknown, so these bounds do not exclude or authenticate this key.",
                         "A letter-count optimum need not be readable; representative completions are source-feasible witnesses, not proposed historical plaintexts.",
                         "Ordinary-letter membership is fixed per square cell across the whole message; actual remaining letter and digit permutations do not affect this objective.",
                         "Neither a language model, a frequency prior nor a p-value is used."],
              "newly_accepted_historical_plaintext_characters": 0}
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored partial-square count bounds differ from recomputation")
        print("Exact partial-square letter-count bounds, controls and witnesses fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"global_minimum_letters": global_min, "global_maximum_letters": global_max,
                      "minimum_digits": 85 - global_max, "maximum_digits": 85 - global_min}))


if __name__ == "__main__":
    main()
