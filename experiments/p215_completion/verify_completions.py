"""Verify p215 completion certificates without language-model files.

This independently checks source preservation, every proposed fill, exact
reencryption and the unchanged ambiguity count. It does not check model ranks.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COORDINATES = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def geometry(data):
    source = data["source_ciphertext"]
    ranks, square = data["key"]["column_rank_order"], data["key"]["square"]
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert len(source) == 248 and source.count("?") == 11
    insertions = {entry["original_index"]: entry["count"] for entry in data["geometry"]["insertions"]}
    assert insertions == {30: 5, 215: 5}
    augmented, mapping = [], []
    for i in range(len(source) + 1):
        if i in insertions:
            augmented.extend("?" * insertions[i])
            mapping.extend([None] * insertions[i])
        if i < len(source):
            augmented.append(source[i])
            mapping.append(i)
    augmented = "".join(augmented)
    assert augmented == data["augmented_ciphertext"] and mapping == data["augmented_to_original_index"]
    physical_columns = sorted(range(len(ranks)), key=lambda c: ranks[c])
    interim = [""] * len(augmented)
    offset = 0
    for column in physical_columns:
        for position in range(column, len(augmented), len(ranks)):
            interim[position] = augmented[offset]
            offset += 1
    domains = []
    for i in range(0, len(interim), 2):
        a, b = interim[i:i + 2]
        values = sorted({square[6 * row + column] for row in range(6) for column in range(6)
                         if (a == "?" or COORDINATES[row] == a) and (b == "?" or COORDINATES[column] == b)})
        domains.append("".join(values))
    assert domains == [entry["possible_characters"] for entry in data["domains"]]
    assert "".join(d if len(d) == 1 else "?" for d in domains) == data["raw_partial_plaintext"]
    assert sum(len(d) == 1 for d in domains) == 109
    assert math.prod(map(len, domains)) == 6 ** 21
    return source, augmented, mapping, ranks, square, domains


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "input.json")
    parser.add_argument("--completions", type=Path, default=ROOT / "conditional_completions.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    result = json.loads(args.completions.read_text())
    assert hashlib.sha256(args.input.read_bytes()).hexdigest() == result["input_sha256"]
    source, augmented, mapping, ranks, square, domains = geometry(data)
    checked = []
    for objective in result["objectives"]:
        assert len(objective["completions"]) == result["top_k"] == objective["top_k"]
        for rank, record in enumerate(objective["completions"], 1):
            assert record["rank"] == rank
            text = record["plaintext"]
            assert len(text) == 129 and all(c in d for c, d in zip(text, domains))
            interim = []
            for character in text:
                cell = square.index(character)
                interim.extend((COORDINATES[cell // 6], COORDINATES[cell % 6]))
            ciphertext = "".join(interim[i] for column in sorted(range(len(ranks)), key=lambda c: ranks[c])
                                 for i in range(column, len(interim), len(ranks)))
            assert ciphertext == record["reencrypted_augmented_ciphertext"]
            assert all(a == "?" or a == b for a, b in zip(augmented, ciphertext))
            fills = [{"augmented_ciphertext_index": i, "original_ciphertext_index": mapping[i],
                      "proposed_coordinate": c,
                      "kind": "source-erasure fill" if mapping[i] is not None else "inserted-gap fill"}
                     for i, c in enumerate(ciphertext) if augmented[i] == "?"]
            assert fills == record["proposed_fills"] and len(fills) == 21
            assert sum(fill["kind"] == "source-erasure fill" for fill in fills) == 11
            assert sum(fill["kind"] == "inserted-gap fill" for fill in fills) == 10
            restored_source = "".join(c for i, c in enumerate(ciphertext) if mapping[i] is not None)
            assert len(restored_source) == 248
            assert sum(a != "?" for a in source) == 237
            assert all(a == "?" or a == b for a, b in zip(source, restored_source))
            assert record["known_coordinate_changes"] == 0
            assert record["source_known_coordinates_preserved"] == 237
            assert record["accepted_as_historical_plaintext"] is False
        checked.append({"objective": objective["id"], "completions_checked": len(objective["completions"]),
                        "known_source_coordinates_preserved_per_completion": 237,
                        "fills_per_completion": {"source_erasures": 11, "inserted_gaps": 10}})
    assert result["newly_accepted_plaintext_characters"] == 0
    report = {"checks_passed": True, "objectives": checked,
              "source_fixed_plaintext_characters": 109, "source_compatible_completions": str(6 ** 21),
              "model_ranking_checked": False,
              "ranking_reproduction": "Run compute_completions.py with the hash-pinned models. This verifier checks arithmetic independently, without invoking the dynamic program."}
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
