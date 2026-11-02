"""Calibrate bounded square generators against the recorded ADFGVX keys.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.

The shared-keyword test is an exact necessary-condition test, not a wordlist
search. It relaxes digit positions and exact cell spacing. Consequently a
failure excludes the stated family; a pass is only a compatibility result.
"""

from argparse import ArgumentParser
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CONTROLS = {
    "Worked-example-VIKINGSCROWNHOTEL": ("VIKINGSCROWNHOTEL", "1234567890"),
    "TRUPPENVERSCHIEBUNG-2026-reported": ("TRUPPENVERSCHIEBUNG", "0123456789"),
}
P153 = "CHI-Nov8-2026-recovery"


def stable_ranks(word):
    ranks = [0] * len(word)
    for rank, index in enumerate(sorted(range(len(word)), key=lambda i: (word[i], i)), 1):
        ranks[index] = rank
    return tuple(ranks)


def routes():
    for axis, outer_reverse, inner_reverse, snake in product(range(2), repeat=4):
        path = []
        for step, a in enumerate(range(5, -1, -1) if outer_reverse else range(6)):
            reverse = inner_reverse ^ (snake and step % 2)
            for b in (range(5, -1, -1) if reverse else range(6)):
                path.append(6 * a + b if axis == 0 else 6 * b + a)
        name = (f"{'columns' if axis else 'rows'}:outer={outer_reverse}:"
                f"inner={inner_reverse}:snake={snake}")
        yield name, path


@lru_cache(None)
def keyword_prefix_patterns(ranks):
    """Enumerate all distinct-letter prefixes for this stable alphabetical key.

    Work in increasing-rank order. Two neighboring positions can carry equal
    letters only if their physical indices increase. Every other boundary is
    strict. Choosing equal/strict at the optional boundaries enumerates every
    possible equality pattern, without choosing the actual alphabet letters.
    """
    width = len(ranks)
    if sorted(ranks) != list(range(1, width + 1)):
        raise ValueError("The column ranks must be a permutation of 1..width")
    order = sorted(range(width), key=ranks.__getitem__)
    forced = {i for i in range(width - 1) if order[i] > order[i + 1]}
    optional = [i for i in range(width - 1) if i not in forced]
    patterns = []
    for mask in range(1 << len(optional)):
        cuts = forced | {position for bit, position in enumerate(optional) if mask >> bit & 1}
        classes = [0] * width
        current = 0
        for i, position in enumerate(order):
            classes[position] = current
            if i in cuts:
                current += 1
        prefix = tuple(dict.fromkeys(classes))
        assert len(prefix) == current + 1
        patterns.append(prefix)
    return tuple(patterns)


def relaxed_prefix_witness(known_letters, prefix):
    """Return a necessary letter-order witness, or None if impossible.

    The square's known letters must occur in their observed route order.
    Some initial portion lies in the keyword prefix; the remainder must be
    alphabetically increasing and absent from the keyword. Unknown square
    cells are ignored, as are all digit locations. The selected alphabet
    values need only leave enough room for all intervening letter classes.
    """
    known = tuple(ord(letter) - ord("A") for letter in known_letters)
    size, count = len(prefix), len(known)
    first_tail = count
    while first_tail and (first_tail == count or known[first_tail - 1] < known[first_tail]):
        first_tail -= 1

    for split in range(first_tail, min(size, count) + 1):
        excluded = set(known[split:])
        available = [i for i in range(26) if i not in excluded]
        if len(available) < size:
            continue
        value_rank = {value: i for i, value in enumerate(available)}
        target = [value_rank[value] for value in known[:split]]

        def place(index, start, assigned):
            if index == split:
                return assigned
            value = target[index]
            for position in range(start, size - split + index + 1):
                letter_class = prefix[position]
                if not letter_class <= value <= len(available) - size + letter_class:
                    continue
                conflict = any(
                    (other_value < value and other_class >= letter_class)
                    or (other_value > value and other_class <= letter_class)
                    or (abs(other_value - value) < abs(other_class - letter_class))
                    for other_class, other_value in assigned
                )
                if conflict:
                    continue
                witness = place(index + 1, position + 1, assigned + [(letter_class, value)])
                if witness is not None:
                    return witness
            return None

        witness = place(0, 0, [])
        if witness is not None:
            return {
                "known_letters_in_keyword": split,
                "keyword_distinct_letter_count": size,
                "prefix_classes": list(prefix),
                "assigned_class_and_available_alphabet_rank": [list(pair) for pair in witness],
            }
    return None


def shared_keyword_check(square, ranks):
    patterns = keyword_prefix_patterns(tuple(ranks))
    compatible = []
    for name, path in routes():
        known = "".join(square[i] for i in path if square[i] in LETTERS)
        for prefix in patterns:
            witness = relaxed_prefix_witness(known, prefix)
            if witness is not None:
                compatible.append({"route": name, "known_letter_order": known, "witness": witness})
                break
    return {
        "equality_patterns_examined": len(patterns),
        "routes_examined": 16,
        "compatible_relaxed_routes": compatible,
    }


def digit_adjacency_check(square, path, digits, cyclic):
    """Check ten distinct letter/digit dominoes against fixed square cells."""
    successors = {path[i]: path[(i + 1) % 36] for i in range(36 if cyclic else 35)}
    known_positions = {symbol: cell for cell, symbol in enumerate(square) if symbol != "?"}
    possibilities = []
    for letter, digit in zip(LETTERS[:10], digits):
        arcs = []
        for left, right in successors.items():
            if square[left] not in ("?", letter) or square[right] not in ("?", digit):
                continue
            if letter in known_positions and known_positions[letter] != left:
                continue
            if digit in known_positions and known_positions[digit] != right:
                continue
            arcs.append((left, right))
        if not arcs:
            return False
        possibilities.append(arcs)
    possibilities.sort(key=len)

    def place(index, occupied):
        if index == len(possibilities):
            return True
        for left, right in possibilities[index]:
            mask = (1 << left) | (1 << right)
            if not occupied & mask and place(index + 1, occupied | mask):
                return True
        return False

    return place(0, 0)


def digit_checks(square):
    result = []
    for digits in ("0123456789", "1234567890"):
        compatible = []
        for name, path in routes():
            for cyclic in (False, True):
                if digit_adjacency_check(square, path, digits, cyclic):
                    compatible.append({"route": name, "cyclic": cyclic})
        result.append({"digits_after_A_through_J": digits, "variants_examined": 32,
                       "compatible_variants": compatible})
    return result


def generated_controls():
    """Independent forward constructions guard against false exclusions."""
    rng = random.Random(15320261102)
    trials = 128
    for trial in range(trials):
        width = rng.randrange(15, 24)
        word = "".join(rng.choice(LETTERS) for _ in range(width))
        letter_order = list(dict.fromkeys(word + LETTERS))
        # Arbitrary digit insertion, partial observations, and a random route.
        symbols = letter_order[:]
        for digit in "0123456789":
            symbols.insert(rng.randrange(len(symbols) + 1), digit)
        route_index = rng.randrange(16)
        path = list(routes())[route_index][1]
        square = ["?"] * 36
        for i, cell in enumerate(path):
            square[cell] = symbols[i] if rng.random() < 0.75 else "?"
        known = "".join(square[i] for i in path if square[i] in LETTERS)
        patterns = keyword_prefix_patterns(stable_ranks(word))
        actual_prefix = tuple(LETTERS.index(x) for x in dict.fromkeys(word))
        sorted_prefix = sorted(actual_prefix)
        actual_classes = tuple(sorted_prefix.index(x) for x in actual_prefix)
        assert actual_classes in patterns
        assert relaxed_prefix_witness(known, actual_classes) is not None
    return {"seed": 15320261102, "forward_generated_shared_keyword_controls": trials,
            "false_exclusions": 0}


def analyze():
    catalogue = json.loads((ROOT / "data/keys.json").read_text())["keys"]
    projection = [{"id": key["id"], "square": key["square"],
                   "column_rank_order": key["column_rank_order"]} for key in catalogue]
    records = []
    positive_controls = []
    for key in catalogue:
        if key["square"] == "?" * 36:
            continue
        records.append({"id": key["id"], "known_cells": 36 - key["square"].count("?"),
                        "digit_adjacency": digit_checks(key["square"]),
                        "shared_keyword": shared_keyword_check(key["square"], key["column_rank_order"])})
        if key["id"] in CONTROLS:
            word, digits = CONTROLS[key["id"]]
            letter_order = "".join(dict.fromkeys(word + LETTERS))
            digit_map = dict(zip(LETTERS[:10], digits))
            expected = "".join(letter + digit_map.get(letter, "") for letter in letter_order)
            observed = key.get("reported_full_square", key["square"])
            assert stable_ranks(word) == tuple(key["column_rank_order"])
            assert expected == observed
            positive_controls.append({"id": key["id"], "keyword": word,
                                      "keyword_length": len(word), "digit_sequence": digits,
                                      "forward_square_and_transposition_match": True})

    target = next(key for key in catalogue if key["id"] == P153)
    transposed = "".join(target["square"][6 * col + row] for row in range(6) for col in range(6))
    swapped = [target["column_rank_order"][i ^ 1] for i in range(18)]
    alternative = shared_keyword_check(transposed, swapped)
    assert not alternative["compatible_relaxed_routes"]
    historical = [row for row in records if row["id"] not in CONTROLS and row["id"] != P153]
    assert len(historical) == 21
    assert all(not row["shared_keyword"]["compatible_relaxed_routes"] for row in historical)
    assert all(not c["compatible_variants"] for row in historical for c in row["digit_adjacency"])
    p153 = next(row for row in records if row["id"] == P153)
    assert not p153["shared_keyword"]["compatible_relaxed_routes"]
    assert all(not c["compatible_variants"] for c in p153["digit_adjacency"])
    return {
        "schema": "adfgvx-p153-key-structure-v1",
        "project": "ADFGVX Cipher", "authors": "icekylinx and GPT-6 Astra Pro",
        "source_projection_sha256": sha256(json.dumps(projection, sort_keys=True).encode()).hexdigest(),
        "scope": {
            "letter_alphabet": LETTERS,
            "stable_rank_ties": "Equal keyword letters are ranked from left to right.",
            "routes": "Row or column major, either outer/inner direction, optionally serpentine:16 routes.",
            "shared_keyword_family": "One A-Z keyword supplies the transposition ranks and the square's deduplicated letter prefix, followed by unused letters in alphabetical order.",
            "shared_keyword_relaxation": "Digit positions and exact cell spacing are ignored. Failure excludes the family; success alone does not prove a realizable square.",
            "excluded_from_claim": "Independent square/transposition keywords, arbitrary row/column relabeling, different alphabet orderings, other generators, and extra source errors.",
        },
        "historical_comparison_key_count": len(historical),
        "historical_comparison_shared_keyword_survivors": 0,
        "historical_comparison_digit_adjacency_survivors": 0,
        "p153_equivalent_pair_swapped_representation": alternative,
        "new_historical_digit_assignments": 0,
        "positive_controls": positive_controls,
        "generated_control_check": generated_controls(),
        "all_key_results": records,
        "skipped_unknown_square": "NSA-June1-CHI-21",
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "result.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = analyze()
    if args.verify:
        if json.loads(args.output.read_text()) != result:
            raise SystemExit("Stored key-structure results differ from fresh computation")
        print("Key-structure results and128 independently generated controls verified")
    else:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
