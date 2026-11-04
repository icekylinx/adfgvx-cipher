#!/usr/bin/env python3
"""Independent exact-oracle and source-witness checks for search.cpp.

icekylinx and GPT-6 Astra Pro. SPDX-License-Identifier: Apache-2.0.
The Python oracle enumerates ranks and ignored source-position subsets; it
shares neither the C++ chunk generation nor its incremental constraint state.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDINATES = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encrypt(text: str, ranks: list[int], square: str) -> str:
    """Direct definition, independent of the repository cipher implementation."""
    stream = "".join(
        COORDINATES[square.index(letter) // 6]
        + COORDINATES[square.index(letter) % 6]
        for letter in text
    )
    return "".join(
        stream[column::len(ranks)]
        for column in sorted(range(len(ranks)), key=ranks.__getitem__)
    )


def oracle_ranks(crib: str, source: str, width: int, errors: int) -> set[tuple[int, ...]]:
    """Enumerate every rank permutation and up-to-E ignored observed positions."""
    accepted: set[tuple[int, ...]] = set()
    observed = [i for i, value in enumerate(source) if value != "?"]
    letters = sorted(set(crib) - {"?"})
    for ranks in itertools.permutations(range(1, width + 1)):
        emitted = [
            index
            for column in sorted(range(width), key=ranks.__getitem__)
            for index in range(column, len(source), width)
        ]
        for count in range(errors + 1):
            for omitted in itertools.combinations(observed, count):
                ignored = set(omitted)
                bindings: dict[tuple[str, int], str] = {}
                conflict = False
                for received, original in enumerate(emitted):
                    letter = crib[original // 2]
                    if received in ignored or source[received] == "?" or letter == "?":
                        continue
                    variable = (letter, original % 2)
                    value = source[received]
                    if variable in bindings and bindings[variable] != value:
                        conflict = True
                        break
                    bindings[variable] = value
                if conflict:
                    continue
                allowed = {
                    letter: [
                        cell
                        for cell in range(36)
                        if all(
                            (letter, component) not in bindings
                            or bindings[letter, component]
                            == COORDINATES[(cell // 6, cell % 6)[component]]
                            for component in (0, 1)
                        )
                    ]
                    for letter in letters
                }
                owner: dict[int, str] = {}

                def augment(letter: str, seen: set[int]) -> bool:
                    for cell in allowed[letter]:
                        if cell in seen:
                            continue
                        seen.add(cell)
                        if cell not in owner or augment(owner[cell], seen):
                            owner[cell] = letter
                            return True
                    return False

                if all(augment(letter, set()) for letter in letters):
                    accepted.add(ranks)
                    break
            if ranks in accepted:
                break
    return accepted


def validate_witness(fixture: dict, row: dict) -> None:
    source, crib = fixture["source"], fixture["crib"]
    width = fixture["width"]
    assert sorted(row["ranks"]) == list(range(1, width + 1))
    assert sorted(row["square"]) == sorted(ALPHABET)
    assert len(row["plaintext"]) == len(crib)
    assert all(a == "?" or a == b for a, b in zip(crib, row["plaintext"]))
    filled = encrypt(row["plaintext"], row["ranks"], row["square"])
    assert filled == row["filled_source"] and len(filled) == len(source)
    edits = [
        [i, received, emitted]
        for i, (received, emitted) in enumerate(zip(source, filled))
        if received != "?" and received != emitted
    ]
    assert edits == row["edits"]
    assert len(edits) == row["actual_observed_substitutions"]
    assert len(edits) <= fixture["maximum_observed_substitutions"]
    ignored = row["ignored_source_indices"]
    assert len(ignored) == len(set(ignored)) <= fixture["maximum_observed_substitutions"]
    assert all(0 <= index < len(source) and source[index] != "?" for index in ignored)
    assert {index for index, _, _ in edits} <= set(ignored)
    assert all(a == "?" or a == b for a, b in zip(row["partial_square"], row["square"]))


def second_source_edits(fixture: dict, row: dict) -> list[list]:
    """Price only the supplied second-part prefix using the first-part square."""
    source, crib = fixture["second_source"], fixture["second_crib"]
    ranks, square = row["ranks"], row["square"]
    width = len(ranks)
    emitted = [
        index
        for column in sorted(range(width), key=ranks.__getitem__)
        for index in range(column, len(source), width)
    ]
    inverse = {original: received for received, original in enumerate(emitted)}
    edits = []
    for at, letter in enumerate(crib):
        cell = square.index(letter)
        assert row["partial_square"][cell] == letter
        for component, value in enumerate((cell // 6, cell % 6)):
            index = inverse[2 * at + component]
            if source[index] != "?" and source[index] != COORDINATES[value]:
                edits.append([index, source[index], COORDINATES[value]])
    return sorted(edits)


def run_fixture(binary: Path, directory: Path, fixture: dict, *limits: str) -> list[dict]:
    source_path = directory / (fixture["id"] + ".source")
    pool_path = directory / (fixture["id"] + ".pool")
    source_path.write_text(fixture["source"] + "\n")
    pool_path.write_text(fixture["id"] + " " + fixture["crib"] + "\n")
    command = [
        str(binary), str(source_path), str(pool_path), str(fixture["width"]),
        str(fixture["maximum_observed_substitutions"]), *(limits or ("60",)),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=True)
    return [json.loads(line) for line in completed.stdout.splitlines()]


def compute() -> dict:
    inputs = json.loads((HERE / "inputs.json").read_text())
    for dependency in inputs["source_dependencies"]:
        assert sha256(ROOT / dependency["path"]) == dependency["sha256"], dependency["path"]
    historical_fixture = next(item for item in inputs["fixtures"] if item["kind"] == "historical_consistency")
    predecessor_input = (ROOT / "experiments/p153_crib/historical_input.txt").read_text().splitlines()
    assert [historical_fixture[key] for key in ("crib", "source", "second_crib", "second_source")] == predecessor_input
    predecessor_certificate = json.loads((ROOT / "experiments/p153_crib/verification.json").read_text())
    predecessor_keys = [row for row in predecessor_certificate["historical"] if row["kind"] == "solution"]
    assert historical_fixture["expected_ranks"] == sorted(row["ranks"] for row in predecessor_keys)
    assert historical_fixture["expected_partial_squares"] == {
        ",".join(map(str, row["ranks"])): row["partial_square"] for row in predecessor_keys
    }
    assert historical_fixture["width"] == 18 and historical_fixture["maximum_observed_substitutions"] == 0
    for row in predecessor_keys:
        assert historical_fixture["expected_second_edits"] == [
            [edit["source_index"], edit["observed"], edit["proposed"]] for edit in row["edits"]
        ]
    results = []
    with tempfile.TemporaryDirectory(prefix="adfgvx_substitution_crib_") as temporary:
        directory = Path(temporary)
        binary = directory / "search"
        subprocess.run(
            ["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", str(HERE / "search.cpp"), "-o", str(binary)],
            text=True, capture_output=True, check=True,
        )
        for fixture in inputs["fixtures"]:
            rows = run_fixture(binary, directory, fixture)
            summary, witnesses = rows[-1], rows[:-1]
            assert summary["kind"] == "summary" and summary["complete"]
            assert summary["projects"] == summary["completed_projects"] == 1
            assert summary["solutions"] == len(witnesses)
            for row in witnesses:
                validate_witness(fixture, row)
            ranks = {tuple(row["ranks"]) for row in witnesses}
            result = {
                "id": fixture["id"], "kind": fixture["kind"],
                "complete": True, "source_slots": len(fixture["source"]),
                "source_masks": fixture["source"].count("?"),
                "supplied_plaintext_positions": len(fixture["crib"]) - fixture["crib"].count("?"),
                "width": fixture["width"],
                "maximum_observed_substitutions": fixture["maximum_observed_substitutions"],
                "returned_witnesses": len(witnesses), "distinct_rank_orders": len(ranks),
                "all_returned_witnesses_reencrypted": True,
            }
            if fixture["kind"] == "tiny_oracle":
                expected = oracle_ranks(fixture["crib"], fixture["source"], fixture["width"], fixture["maximum_observed_substitutions"])
                assert ranks == expected == {tuple(rank) for rank in fixture["expected_ranks"]}
                result["independent_exhaustive_rank_set_agrees"] = True
            elif fixture["kind"] == "hidden_key":
                full = encrypt(fixture["plaintext"], fixture["true_ranks"], fixture["true_square"])
                actual_planted = [i for i, (a, b) in enumerate(zip(fixture["source"], full)) if a != "?" and a != b]
                assert sorted(fixture["planted_substitutions"]) == actual_planted
                assert [i for i, c in enumerate(fixture["source"]) if c == "?"] == fixture["declared_masks"]
                assert tuple(fixture["true_ranks"]) in ranks
                compatible = [
                    row for row in witnesses
                    if row["ranks"] == fixture["true_ranks"]
                    and all(a == "?" or a == b for a, b in zip(row["partial_square"], fixture["true_square"]))
                ]
                assert compatible
                result["hidden_true_rank_retrieved"] = True
                result["planted_square_satisfies_returned_component_bindings"] = True
                result["witness"] = compatible[0]
            else:
                assert fixture["kind"] == "historical_consistency"
                assert ranks == {tuple(rank) for rank in fixture["expected_ranks"]}
                for row in witnesses:
                    expected = fixture["expected_partial_squares"][",".join(map(str, row["ranks"]))]
                    assert row["partial_square"] == expected
                    assert second_source_edits(fixture, row) == fixture["expected_second_edits"]
                result["witnesses"] = witnesses
                result["second_part_prefix_observed_edits"] = fixture["expected_second_edits"]
                result["historical_scope"] = "Post-discovery consistency of the supplied sixty-letter p153 crib; no new decipherment or digit recovery."
            results.append(result)

        # A deliberately short search must report its incomplete last project.
        fixture = next(item for item in inputs["fixtures"] if item["id"] == "positive9")
        limited = run_fixture(binary, directory, fixture, "60", "1")[-1]
        assert not limited["complete"] and limited["stop_reason"] == "node_limit"
        assert limited["projects"] == 1 and limited["completed_projects"] == 0

        # Input problems must fail rather than become a free erasure or budget.
        malformed_source = directory / "malformed.source"
        malformed_pool = directory / "malformed.pool"
        rejection_cases = [
            ("ADFC", "sample AB\n", "2", "1", "60"),
            ("ADFG extra", "sample AB\n", "2", "1", "60"),
            ("ADFG", "sample AB extra\n", "2", "1", "60"),
            ("ADFG", "sample A*\n", "2", "1", "60"),
            ("ADFG", "sample AB\n", "2", "-1", "60"),
            ("ADFG", "sample AB\n", "2", "1", "nan"),
        ]
        for source, pool, width, errors, seconds in rejection_cases:
            malformed_source.write_text(source + "\n")
            malformed_pool.write_text(pool)
            rejected = subprocess.run(
                [str(binary), str(malformed_source), str(malformed_pool), width, errors, seconds],
                text=True, capture_output=True,
            )
            assert rejected.returncode == 2 and not rejected.stdout

    return {
        "schema_version": 1,
        "credit": inputs["credit"],
        "inputs_sha256": sha256(HERE / "inputs.json"),
        "solver_sha256": sha256(HERE / "search.cpp"),
        "verifier_sha256": sha256(HERE / "verify.py"),
        "source_dependencies_verified": inputs["source_dependencies"],
        "tiny_exhaustive_oracles": 9,
        "fresh_hidden_key_controls": 10,
        "historical_consistency_fixtures": 1,
        "historical_fixture_bound_to_pinned_fields": True,
        "incomplete_project_reporting_checked": True,
        "malformed_inputs_rejected": len(rejection_cases),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write deterministic certificates.json")
    mode.add_argument("--verify", action="store_true", help="recompute and compare the committed certificate (default)")
    arguments = parser.parse_args()
    certificate = compute()
    path = HERE / "certificates.json"
    if arguments.write:
        path.write_text(json.dumps(certificate, indent=2) + "\n")
    else:
        assert certificate == json.loads(path.read_text()), "certificate mismatch"
    print("Verified 9 exhaustive tiny oracles, 10 hidden-key controls, and the existing p153 crib witness.")


if __name__ == "__main__":
    main()
