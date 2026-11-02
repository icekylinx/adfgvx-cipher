"""Exact bound for the 24 recorded ordinary letters other than Q and Y.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Only new category-audit files are written; the reviewed base engine and
its original report stay unchanged. No language model is used.
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
TARGET = "ABCDEFGHIJKLMNOPRSTUVWXZ"
BASE_SHA = "0f7e8ef517e24f774678cc113c94a8b91dc3fbb4362673f0474a178eeae80244"
CHANGES = [
    ("const int letter = cell_letters[6 * first + second] < 26;",
     "const int symbol = cell_letters[6 * first + second];\n"
     "                        const int letter = symbol < 26 && symbol != 16 && symbol != 24;"),
    ("ordinary_letter_count", "target_category_count"),
    ("best_signed_letter_count", "best_signed_category_count"),
    (r'\"maximize_letters\"', r'\"maximize_target_category\"'),
]


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    return digest_bytes(Path(path).read_bytes())


def generated_source():
    source = (HERE / "exact_letter_bounds.cpp").read_bytes()
    if digest_bytes(source) != BASE_SHA:
        raise ValueError("The pinned reviewed base engine has changed; category adaptation requires review")
    text = source.decode()
    for original, replacement in CHANGES:
        if text.count(original) != 1:
            raise ValueError("A declared category adaptation is not a unique exact replacement")
        text = text.replace(original, replacement)
    return text


def fill_frame(source, losses, fill):
    additions, iterator = dict(zip(losses, fill)), iter(source)
    full = "".join(additions[i] if i in additions else next(iterator)
                    for i in range(len(source) + len(losses)))
    assert next(iterator, None) is None
    return full


def execute(binary, source_case, square, maximize, work, name):
    config, output = work / (name + ".cfg"), work / (name + ".json")
    output.unlink(missing_ok=True)
    config.write_text(f"{len(source_case['column_rank_order'])} {source_case['missing_count']} 0 0 100000 {int(maximize)}\n"
                      + square + "\n" + " ".join(map(str, source_case["column_rank_order"])) + "\n"
                      + source_case["observed_ciphertext"] + "\n")
    subprocess.run([str(binary), "solve", str(config), str(output)], check=True, stderr=subprocess.DEVNULL)
    return json.loads(output.read_text())


def verify_witness(case, square, result):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    losses, fill = result["missing_full_ciphertext_positions"], result["filled_missing_coordinates"]
    assert losses == sorted(set(losses)) and len(losses) == len(fill) == case["missing_count"]
    assert set(fill) <= set(COORDINATES)
    full = fill_frame(case["observed_ciphertext"], losses, fill)
    text = decrypt(full, case["column_rank_order"], square)
    counts = {"target24": sum(c in TARGET for c in text), "Q": text.count("Q"),
              "Y": text.count("Y"), "digits": sum(c in "0123456789" for c in text)}
    assert sum(counts.values()) == len(text)
    assert counts["target24"] == result["target_category_count"]
    assert result["best_signed_category_count"] == (counts["target24"] if result["maximize_target_category"] else -counts["target24"])
    assert encrypt(text, case["column_rank_order"], square) == full
    assert "".join(c for i, c in enumerate(full) if i not in losses) == case["observed_ciphertext"]
    assert result["all_allocations_completed"]
    return {"representative_plaintext": text, "filled_ciphertext": full, "category_counts": counts,
            "source_coordinates_preserved": len(case["observed_ciphertext"]), "changed_retained_coordinates": 0,
            "count_selected_coordinate_fills": len(fill), "reencryption_verified": True,
            "accepted_historical_plaintext": False}


def exhaustive_controls(binary, work, square):
    reports = []
    settings = [([3, 1, 4, 2], "QY12ER", 1),
                ([4, 1, 6, 2, 5, 3], "QY2STAB", 2),
                ([3, 13, 2, 12, 1, 11, 15, 8, 9, 4, 5, 14, 6, 10, 7, 16], "DERQY3BMEL", 2)]
    for index, (ranks, text, missing) in enumerate(settings):
        full = encrypt(text, ranks, square)
        planted = [1] if missing == 1 else [1, len(full) - 3]
        source = "".join(c for i, c in enumerate(full) if i not in planted)
        case = {"column_rank_order": ranks, "observed_ciphertext": source, "missing_count": missing}
        best = {False: None, True: None}
        count = 0
        for losses in itertools.combinations(range(len(full)), missing):
            for values in itertools.product(COORDINATES, repeat=missing):
                fill = "".join(values)
                plaintext = decrypt(fill_frame(source, losses, fill), ranks, square)
                target_count = sum(c in TARGET for c in plaintext)
                for maximize in best:
                    candidate = (-target_count if maximize else target_count, losses, fill)
                    if best[maximize] is None or candidate < best[maximize]:
                        best[maximize] = candidate
                count += 1
        checks = []
        for maximize, expected in best.items():
            result = execute(binary, case, square, maximize, work, f"small_{index}_{int(maximize)}")
            assert result["target_category_count"] == (-expected[0] if maximize else expected[0])
            assert result["missing_full_ciphertext_positions"] == list(expected[1])
            assert result["filled_missing_coordinates"] == expected[2]
            witness = verify_witness(case, square, result)
            checks.append({"exact_search": result, "verification": witness, "matches_exhaustive_optimum": True})
        reports.append({"case": case, "square": square, "source_control_plaintext": text,
                        "nominal_coordinates": len(full), "witnesses_enumerated": count, "checks": checks})
    return {"total_witnesses_enumerated": sum(r["witnesses_enumerated"] for r in reports), "records": reports}


def load_context():
    input_path = ROOT / "experiments/p198_exact_sparse/inputs.json"
    cases = json.loads(input_path.read_text())["cases"]
    case = next(c for c in cases if c["id"] == "p198_Nov13-15b")
    partial = case["partial_historical_square"]
    remaining = set(ALPHABET) - set(partial)
    assert len(TARGET) == 24 and set(TARGET) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - set("QY")
    assert not remaining.intersection(TARGET) and set(TARGET) <= set(partial)
    base = json.loads((HERE / "results.json").read_text())
    representative = base["membership_results"][0]["representative_complete_square"]
    assert all(a == "?" or a == b for a, b in zip(partial, representative))
    return input_path, cases, case, representative, base


def verify_recorded(path):
    data = json.loads(path.read_text())
    input_path, cases, case, representative, base = load_context()
    assert data["input_sha256"] == digest(input_path)
    assert data["base_letter_bounds_sha256"] == digest(HERE / "results.json")
    assert data["base_engine_sha256"] == BASE_SHA
    assert data["generated_engine_sha256"] == digest_bytes(generated_source().encode())
    assert data["target_category"] == TARGET
    assert data["representative_complete_square"] == representative
    witness = verify_witness(case, representative, data["exact_search"])
    assert witness == data["verification"]
    assert witness["category_counts"] == {"target24": 75, "Q": 0, "Y": 0, "digits": 10}
    assert data["maximum_target24_positions"] == 75
    assert data["necessary_minimum_digits_plus_Q_plus_Y"] == 10
    assert data["separate_necessary_minimum_digits"] == base["implied_attainable_global_minimum_digits"] == 3
    assert data["attainable_minimum_digits_conditional_on_no_Q_or_Y"] == 10
    assert data["complete_square_extensions_covered"] == math.factorial(8)
    assert data["exact_search"]["allocations_completed"] == 15504
    assert data["exact_search"]["maximum_active_states"] <= 32
    control = data["positive_control"]
    control_case = next(c for c in cases if c["id"] == control["case_id"])
    control_witness = verify_witness(control_case, control_case["fixed_complete_square"], control["exact_search"])
    assert control_witness == control["verification"] and control_witness["category_counts"]["target24"] == 85
    assert data["newly_accepted_historical_plaintext_characters"] == 0
    print("Verified category invariance, stored source witnesses and combined count inequalities; optimization not rerun.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "category_bounds.json")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--verify-recorded", action="store_true")
    args = parser.parse_args()
    if args.verify_recorded:
        verify_recorded(args.output)
        return
    if args.work_dir is None:
        parser.error("--work-dir is required for an exact search")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    source = generated_source()
    generated = args.work_dir / "category_generated.cpp"
    generated.write_text(source)
    binary = args.work_dir / "category_exact"
    subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror", str(generated), "-o", str(binary)], check=True)
    input_path, cases, case, representative, base = load_context()
    spec = importlib.util.spec_from_file_location("source_provenance", ROOT / "experiments/p198_exact_sparse/compute.py")
    provenance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provenance)
    provenance.audit_provenance(cases)
    controls = exhaustive_controls(binary, args.work_dir, representative)
    result = execute(binary, case, representative, True, args.work_dir, "historical_common24")
    witness = verify_witness(case, representative, result)
    assert result["target_category_count"] == 75
    assert witness["category_counts"]["Q"] == witness["category_counts"]["Y"] == 0
    positive = next(c for c in cases if c["id"] == "control_Nov13-15b")
    positive_result = execute(binary, positive, positive["fixed_complete_square"], True, args.work_dir, "positive_common24")
    positive_witness = verify_witness(positive, positive["fixed_complete_square"], positive_result)
    assert positive_witness["category_counts"]["target24"] == 85
    output = {"schema": "adfgvx-common24-category-bound-v1", "project": "ADFGVX Cipher",
              "authors": "icekylinx and GPT-6 Astra Pro", "case_id": case["id"],
              "input_sha256": digest(input_path), "base_letter_bounds_sha256": digest(HERE / "results.json"),
              "base_engine_sha256": BASE_SHA, "generated_engine_sha256": digest_bytes(source.encode()),
              "declared_source_adaptations": [{"exact_original": a, "replacement": b, "required_occurrences": 1} for a, b in CHANGES],
              "target_category": TARGET, "partial_square": case["partial_historical_square"],
              "representative_complete_square": representative,
              "invariance_reason": "All 24 target letters are already assigned in the partial square. Every remaining cell is Q, Y or a digit, outside this target category, so all 8! square completions have identical category scores for every coordinate frame.",
              "complete_square_extensions_covered": math.factorial(8),
              "loss_and_fill_witnesses_per_complete_square": str(math.comb(170, 5) * 6 ** 5),
              "controls": controls, "exact_search": result, "verification": witness,
              "positive_control": {"case_id": positive["id"], "exact_search": positive_result, "verification": positive_witness},
              "maximum_target24_positions": 75, "necessary_minimum_digits_plus_Q_plus_Y": 10,
              "separate_necessary_minimum_digits": base["implied_attainable_global_minimum_digits"],
              "attainable_minimum_digits_conditional_on_no_Q_or_Y": 10,
              "limits": ["The historical number of digits, Q and Y is unknown; these conditions do not reject or authenticate the key.",
                         "The two inequalities are necessary conditions, not a complete digit/Q/Y trade-off frontier.",
                         "The representative maximum-count text is a source-feasible witness, not a plausible plaintext proposal.",
                         "The all-square claim concerns the fixed Nov13-15b partial square, fixed ranks and exactly five source deletions."],
              "newly_accepted_historical_plaintext_characters": 0}
    if args.verify:
        if json.loads(args.output.read_text()) != output:
            raise SystemExit("Stored category bounds differ from recomputation")
        print("Exact category bound, exhaustive controls and witnesses fully reproduced")
    else:
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"maximum_common24": 75, "minimum_digits_plus_Q_plus_Y": 10,
                      "minimum_digits": base["implied_attainable_global_minimum_digits"],
                      "QY_free_attainable_minimum_digits": 10, "counts_of_attaining_witness": witness["category_counts"]}))


if __name__ == "__main__":
    main()
