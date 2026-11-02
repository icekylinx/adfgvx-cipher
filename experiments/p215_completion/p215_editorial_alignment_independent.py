"""Independent banded dynamic program for the p215 editorial-alignment audit.

Run with explicit paths to the repository's prior_readings and alignment JSON.
No code from that repository is imported. Source positions are never deleted.
"""
import argparse
from functools import lru_cache
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json


def encipher(plaintext, square, ranks):
    """Build physical columns explicitly, then emit in transmission order."""
    abc = 'ADFGVX'
    assert len(square) == len(set(square)) == 36
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    coordinate = {symbol: abc[i // 6] + abc[i % 6]
                  for i, symbol in enumerate(square)}
    columns = [[] for _ in ranks]
    position = 0
    for symbol in plaintext:
        for value in coordinate[symbol]:
            columns[position % len(ranks)].append(value)
            position += 1
    return ''.join(''.join(columns[ranks.index(rank)])
                   for rank in range(1, len(ranks) + 1))


def banded_alignment(source, target):
    """State (i,g): i source slots consumed, g target insertions consumed.

    The next target index is i+g. Alignment and insertion transitions are
    disjoint, so tied path counts add. Completion has one all-insertion suffix.
    """
    n = len(source)
    gaps = len(target) - n
    if gaps < 0:
        raise ValueError('Target shorter than the preserved source')

    @lru_cache(None)
    def suffix(i, g):
        if i == n:
            return 0, 1
        j = i + g
        cost, count = suffix(i + 1, g)
        cost += int(source[i] != '?' and source[i] != target[j])
        if g < gaps:
            other_cost, other_count = suffix(i, g + 1)
            if other_cost < cost:
                return other_cost, other_count
            if other_cost == cost:
                count += other_count
        return cost, count

    return suffix(0, 0)


def brute_force(source, target):
    counts = {}
    for retained in combinations(range(len(target)), len(source)):
        cost = sum(a != '?' and a != target[j]
                   for a, j in zip(source, retained))
        counts[cost] = counts.get(cost, 0) + 1
    return min(counts), counts[min(counts)]


def controls():
    tested = 0
    for n in range(4):
        for m in range(n, 6):
            for a in product('AD?', repeat=n):
                source = ''.join(a)
                for b in product('AD', repeat=m):
                    target = ''.join(b)
                    assert banded_alignment(source, target) == brute_force(source, target)
                    tested += 1
    assert banded_alignment('????', 'ADADADA') == (0, comb(7, 4))
    assert banded_alignment('AAAAA', 'DDDDDDD') == (5, comb(7, 5))
    return tested + 2


def verify(prior_path, expected_path):
    record = next(r for r in json.loads(prior_path.read_text())['messages']
                  if r['id'] == 'p215')
    published = next(r for r in record['published_readings']
                     if r['id'] == 'baertl_comment39')
    source = record['analysis_ciphertext']
    text = published['compact_plaintext']
    square = record['key']['square']
    ranks = record['key']['column_rank_order']
    expected = json.loads(expected_path.read_text())
    assert hashlib.sha256(source.encode()).hexdigest() == expected['source_sha256']
    assert hashlib.sha256(text.encode()).hexdigest() == expected['editorial_plaintext_sha256']
    rows = []
    for removed in [None] + list(range(len(text))):
        candidate = text if removed is None else text[:removed] + text[removed + 1:]
        target = encipher(candidate, square, ranks)
        cost, count = banded_alignment(source, target)
        rows.append({
            'removed_plaintext_index': removed,
            'plaintext_length': len(candidate),
            'required_insertions': len(target) - len(source),
            'minimum_known_coordinate_substitutions': cost,
            'optimal_source_preserving_injections': count,
        })
    assert rows == expected['records']
    best_cost = min(r['minimum_known_coordinate_substitutions'] for r in rows[1:])
    best = [r for r in rows[1:] if r['minimum_known_coordinate_substitutions'] == best_cost]
    return {
        'schema': 'p215-editorial-alignment-independent-review-v1',
        'passed': True,
        'review_date': '2026-11-02',
        'independent_method': 'Banded suffix dynamic program over source index and insertion count; independent explicit-column ADFGVX encryption; no repository code imported.',
        'root_records_compared_exactly': len(rows),
        'exhaustive_small_control_cases': controls(),
        'source_slots': len(source),
        'source_known_coordinates': sum(c != '?' for c in source),
        'source_sha256': expected['source_sha256'],
        'editorial_plaintext_sha256': expected['editorial_plaintext_sha256'],
        'root_alignment_artifact_sha256': hashlib.sha256(expected_path.read_bytes()).hexdigest(),
        'full_editorial_result': rows[0],
        'best_one_letter_deletions': best,
        'recurrence_review': 'The two choices either align the next original slot to the next target coordinate, charging one for a known-symbol contradiction, or consume one extra target coordinate. They partition the strictly increasing injections, so tied counts add without double counting. A source erasure contributes zero cost but remains a distinct preserved source slot.',
        'interpretation': 'Under the stated fixed key and a model retaining every source slot in order, the full 130-letter editorial text requires 12 inserted coordinates plus at least 166 known-coordinate substitutions. Among all 130 one-letter deletions, deleting V at zero-based plaintext index 8 is the sole minimum: 10 insertions and at least 27 substitutions, attained by 6355 increasing source-to-target injections.',
        'scope_limit': 'This rules out the tested editorial wording as a missing-coordinate-only explanation under the fixed key. It does not rule out a different key, received-coordinate deletion or rearrangement, other plaintext edits, or more extensive historical corruption. The injection counts describe positional alignments to a fixed target ciphertext, not different recovered plaintexts, independent historical witnesses, or probabilities.',
        'new_historical_letters_accepted': 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prior-readings', type=Path, required=True)
    parser.add_argument('--expected', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.prior_readings, args.expected)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
