"""Exact top-K model-ranked completions of the fixed p215 letter domains.

Every received valid coordinate remains unchanged. The result is conditional
on the prior published geometry and is not a recovered historical plaintext.
"""
from __future__ import annotations
import argparse
import array
from collections import defaultdict
from functools import lru_cache
import hashlib
import heapq
import itertools
import json
import math
from pathlib import Path
import random
import struct
import sys
import time

ROOT = Path(__file__).resolve().parent
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"
SCALE = 2 ** 24
EXPECTED = {
    "general_quad": "cbc02525fbf50d231054dd6ab642882d385a0ab31f96dcd4139b85cceaeece59",
    "military_quad": "fc450633e557d477d009fd9f682a0d6c96629d48a532c1dd2fbc42af0c73b46d",
    "military_six": "79e1474e78afa0d208ffe4306b31ed3531786c2fc6a0c7efb4d2f3a7fd5e4b5a",
}


def transpose(stream, ranks):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    return "".join(stream[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def encrypt(plaintext, ranks, square):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    stream = "".join(COORDINATES[square.index(c) // 6] + COORDINATES[square.index(c) % 6]
                     for c in plaintext)
    return transpose(stream, ranks)


def top_k(domains, k, order, contribution):
    """K best prefixes per Markov suffix; integer scores and lexical tie order."""
    states = {"": [(0, "")]}
    counters = {"maximum_retained_suffix_states": 1, "transitions_considered": 0,
                "retained_prefixes_per_suffix": k}
    for position, domain in enumerate(domains):
        candidates = defaultdict(list)
        for suffix, prefixes in states.items():
            for letter in domain:
                combined = suffix + letter
                delta = contribution(combined, position)
                target = combined[-order:]
                for score, text in prefixes:
                    candidates[target].append((score + delta, text + letter))
                    counters["transitions_considered"] += 1
        states = {suffix: heapq.nsmallest(k, rows, key=lambda row: (-row[0], row[1]))
                  for suffix, rows in candidates.items()}
        counters["maximum_retained_suffix_states"] = max(counters["maximum_retained_suffix_states"], len(states))
    result = heapq.nsmallest(k, itertools.chain.from_iterable(states.values()), key=lambda row: (-row[0], row[1]))
    assert len({text for _, text in result}) == len(result)
    return result, counters


def check_dp():
    """Independent exhaustive comparison on small finite-domain problems."""
    rng = random.Random(1918215)
    reports = []
    for order in [3, 5]:
        domains = ["AB", "C", "BD", "AC", "D", "AB", "BC", "A", "CD"]
        tables = {}
        for span in [4, 6]:
            tables[span] = {"".join(gram): rng.randrange(-1000, 1)
                            for gram in itertools.product("ABCD", repeat=span)}
        def term(suffix, position):
            total = 3 * tables[4][suffix[-4:]] if position >= 3 else 0
            if order == 5 and position >= 5:
                total += 7 * tables[6][suffix[-6:]]
            return total
        dynamic, _ = top_k(domains, 12, order, term)
        brute = []
        for letters in itertools.product(*domains):
            text = "".join(letters)
            score = sum(3 * tables[4][text[i:i + 4]] for i in range(len(text) - 3))
            if order == 5:
                score += sum(7 * tables[6][text[i:i + 6]] for i in range(len(text) - 5))
            brute.append((score, text))
        brute.sort(key=lambda row: (-row[0], row[1]))
        assert dynamic == brute[:12]
        reports.append({"markov_order": order, "exhaustive_completions": len(brute), "top_k": 12, "exact_match": True})
    tied, _ = top_k(["AB"] * 8, 12, 5, lambda suffix, position: 0)
    assert [text for _, text in tied] == ["".join(x) for x in list(itertools.product("AB", repeat=8))[:12]]
    return {"exhaustive_controls": reports, "lexical_tie_control_passed": True}


def load_bytes(path, kind):
    data = Path(path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED[kind], (kind, "model hash mismatch")
    return data


def integer_log(value):
    numerator, denominator = float(value).as_integer_ratio()
    assert SCALE % denominator == 0, (value, denominator)
    return numerator * (SCALE // denominator)


class Tables:
    def __init__(self, quad_path, quad_kind, six_path=None):
        quad_bytes = load_bytes(quad_path, quad_kind)
        assert len(quad_bytes) == 4 * 36 ** 4
        self.quad = array.array("f")
        self.quad.frombytes(quad_bytes)
        if six_path:
            self.six_bytes = load_bytes(six_path, "military_six")
            magic, size, count, floor = struct.unpack_from("<8sIIf", self.six_bytes)
            assert magic == b"G6HASH2\0" and size & (size - 1) == 0
            assert len(self.six_bytes) == 20 + 8 * size
            self.keys = memoryview(self.six_bytes)[20:20 + 4 * size].cast("I")
            self.values = memoryview(self.six_bytes)[20 + 4 * size:].cast("f")
            self.mask, self.floor = size - 1, floor

    @lru_cache(maxsize=None)
    def units(self, gram):
        code = 0
        for letter in gram:
            code = code * 36 + ALPHABET.index(letter)
        if len(gram) == 4:
            return integer_log(self.quad[code])
        assert len(gram) == 6
        key = code + 1
        h = ((key ^ (key >> 16)) * 0x7FEB352D) & 0xFFFFFFFF
        h = ((h ^ (h >> 15)) * 0x846CA68B) & 0xFFFFFFFF
        h ^= h >> 16
        slot = h & self.mask
        while self.keys[slot]:
            if self.keys[slot] == key:
                return integer_log(self.values[slot])
            slot = (slot + 1) & self.mask
        return integer_log(self.floor)


def completion_record(data, text, score, denominator, rank):
    domains = [d["possible_characters"] for d in data["domains"]]
    assert len(text) == len(domains) and all(c in d for c, d in zip(text, domains))
    ciphertext = encrypt(text, data["key"]["column_rank_order"], data["key"]["square"])
    observed = data["augmented_ciphertext"]
    assert len(ciphertext) == len(observed) == 258
    assert all(a == "?" or a == b for a, b in zip(observed, ciphertext))
    fills = [{"augmented_ciphertext_index": i, "original_ciphertext_index": data["augmented_to_original_index"][i],
              "proposed_coordinate": c,
              "kind": "source-erasure fill" if data["augmented_to_original_index"][i] is not None else "inserted-gap fill"}
             for i, c in enumerate(ciphertext) if observed[i] == "?"]
    assert len(fills) == 21
    return {"rank": rank, "integer_objective": score, "display_score": score / denominator,
            "plaintext": text, "reencrypted_augmented_ciphertext": ciphertext,
            "known_coordinate_changes": 0, "source_known_coordinates_preserved": 237,
            "proposed_fills": fills, "accepted_as_historical_plaintext": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "input.json")
    parser.add_argument("--general-quad", type=Path, required=True)
    parser.add_argument("--military-quad", type=Path, required=True)
    parser.add_argument("--military-six", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--output", type=Path, default=ROOT / "conditional_completions.json")
    args = parser.parse_args()
    if sys.byteorder != "little":
        parser.error("This binary table reader requires little-endian input arrays")
    if args.top_k < 1 or args.top_k > 100:
        parser.error("top-k must be between 1 and 100")
    data = json.loads(args.input.read_text())
    domains = [d["possible_characters"] for d in data["domains"]]
    assert math.prod(map(len, domains)) == int(data["compatible_plaintext_count"]) == 6 ** 21
    assert sum(len(d) == 1 for d in domains) == 109
    controls = check_dp()
    general = Tables(args.general_quad, "general_quad")
    military = Tables(args.military_quad, "military_quad", args.military_six)
    n = len(domains)
    objectives = []
    for name, tables, mixed in [("general_quad", general, False), ("military_quad", military, False),
                                ("military_mixed_30_70", military, True)]:
        # All float32 log-table entries are represented exactly at scale 2^24.
        # Integer coefficients remove averaging/mixture denominators from the
        # optimization, so floating-point tie drift cannot affect the DP order.
        coefficient4 = 3 * (n - 5) if mixed else 1
        coefficient6 = 7 * (n - 3) if mixed else 0
        denominator = 10 * (n - 3) * (n - 5) * SCALE if mixed else (n - 3) * SCALE
        def contribution(suffix, position):
            score = coefficient4 * tables.units(suffix[-4:]) if position >= 3 else 0
            if mixed and position >= 5:
                score += coefficient6 * tables.units(suffix[-6:])
            return score
        started = time.monotonic()
        rows, counters = top_k(domains, args.top_k, 5 if mixed else 3, contribution)
        records = []
        for rank, (score, text) in enumerate(rows, 1):
            check = coefficient4 * sum(tables.units(text[i:i + 4]) for i in range(n - 3))
            if mixed:
                check += coefficient6 * sum(tables.units(text[i:i + 6]) for i in range(n - 5))
            assert score == check
            records.append(completion_record(data, text, score, denominator, rank))
        objectives.append({"id": name, "order": 5 if mixed else 3,
                           "integer_denominator_for_display": denominator,
                           "coefficient4": coefficient4, "coefficient6": coefficient6,
                           "integer_log_scale": SCALE, "top_k": args.top_k,
                           "dp_counts": counters, "seconds": time.monotonic() - started,
                           "completions": records})
    best_texts = [objective["completions"][0]["plaintext"] for objective in objectives]
    differences = [{"plaintext_index": i, "source_domain": domains[i],
                    "model_top_one_letters": {o["id"]: o["completions"][0]["plaintext"][i] for o in objectives}}
                   for i in range(n) if len({text[i] for text in best_texts}) > 1]
    output = {"format_version": 1, "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
              "model_sha256": EXPECTED, "top_k": args.top_k,
              "optimization_scope": "Exact top K in the recorded finite letter domains for each specified additive log-table objective, with lexical tie breaking. This is a model ranking, not a recovery claim or posterior probability.",
              "geometry_status": "Conditional on Norbert's previously published two missing-group hypothesis; the primary header itself says 248 coordinates.",
              "source_known_coordinates": 237, "source_fixed_plaintext_characters": 109,
              "model_selected_coordinates_per_completion": 21, "newly_accepted_plaintext_characters": 0,
              "compatible_plaintext_count": str(6 ** 21), "controls": controls,
              "objectives": objectives, "top_one_model_disagreements": differences,
              "earlier_Baertl_completion": {"plaintext_length": 130,
                  "review": "Outside these domains. Its best one-letter deletion still contradicts 27 received coordinates at 20 plaintext positions, as independently verified in the parent p215 certificate."}}
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"objectives": [{"id": o["id"], "seconds": o["seconds"],
                     "best": o["completions"][0]["plaintext"], "score": o["completions"][0]["display_score"],
                     "dp_counts": o["dp_counts"]} for o in objectives],
                     "top_one_disagreements": differences}, indent=2))


if __name__ == "__main__":
    main()
