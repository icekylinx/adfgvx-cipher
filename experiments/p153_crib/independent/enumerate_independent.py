#!/usr/bin/env python3
"""Independent exact width-18 crib enumeration, using fixed-order DFS.

This is a post-discovery conditional check. It takes a 66-character partial
crib and 132 clear source coordinates, then assesses a second crib against
108 coordinates. It never changes received coordinates during enumeration.
"""
import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time

COORDS = 'ADFGVX'


def parse(path):
    first, ciphertext, second, other = path.read_text().split()
    assert len(first) == 66 and len(ciphertext) == 132
    assert len(second) <= 54 and len(other) == 108
    assert set(first + second) <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZ?')
    assert set(ciphertext) <= set(COORDS) and set(other) <= set(COORDS + '?')
    assert set(second.replace('?', '')) <= set(first.replace('?', ''))
    return first, ciphertext, second, other


def check_second(ranks, mapping, second, ciphertext):
    # Independently construct all physical columns of the full 108-slot stream.
    # Uncribbed plaintext positions stay unknown and never score a mismatch.
    stream = []
    for position in range(54):
        ch = second[position] if position < len(second) else '?'
        cell = mapping.get(ch)
        stream.extend('??' if cell is None else COORDS[cell // 6] + COORDS[cell % 6])
    prediction = ''.join(''.join(stream[col::18]) for col in sorted(range(18), key=lambda col: ranks[col]))
    return [{'source_index': i, 'observed': old, 'proposed': new}
            for i, (old, new) in enumerate(zip(ciphertext, prediction)) if old != '?' and new != '?' and old != new]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    first, ciphertext, second, other = parse(args.input)
    ct = tuple(COORDS.index(c) for c in ciphertext)
    started = time.monotonic()
    solutions = []
    count = feasible = nodes = 0
    for long_positions in combinations(range(18), 6):
        count += 1
        long_set = set(long_positions)
        lengths = [8 if i in long_set else 7 for i in range(18)]
        chunks = []
        offset = 0
        for length in lengths:
            chunks.append(ct[offset:offset + length])
            offset += length
        assert offset == 132
        choices = []
        for pair in range(9):
            required = 8 if pair < 3 else 7
            available = [i for i, length in enumerate(lengths) if length == required]
            local = []
            for left in available:
                for right in available:
                    if left == right:
                        continue
                    mapping, inverse = {}, {}
                    valid = True
                    for row in range(required):
                        letter = first[row * 9 + pair]
                        if letter == '?':
                            continue
                        cell = 6 * chunks[left][row] + chunks[right][row]
                        if letter in mapping and mapping[letter] != cell or cell in inverse and inverse[cell] != letter:
                            valid = False
                            break
                        mapping[letter] = cell
                        inverse[cell] = letter
                    if valid:
                        local.append((left, right, mapping))
            if not local:
                break
            choices.append(local)
        if len(choices) < 9:
            continue
        feasible += 1

        def visit(pair, used, mapping, inverse, ranks):
            nonlocal nodes
            nodes += 1
            if pair == 9:
                square = ''.join(inverse.get(cell, '?') for cell in range(36))
                edits = check_second(ranks, mapping, second, other)
                solutions.append({'ranks': ranks, 'partial_square': square,
                                  'second_crib_known_coordinate_mismatches': len(edits), 'edits': edits})
                return
            for left, right, local in choices[pair]:
                if left in used or right in used:
                    continue
                if any(letter in mapping and mapping[letter] != cell or cell in inverse and inverse[cell] != letter
                       for letter, cell in local.items()):
                    continue
                visit(pair + 1, used | {left, right}, {**mapping, **local},
                      {**inverse, **{cell: letter for letter, cell in local.items()}}, ranks + [left + 1, right + 1])

        visit(0, set(), {}, {}, [])
    result = {'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'first_crib_length': len(first), 'first_crib_known_positions': len(first.replace('?', '')),
              'second_crib_length': len(second), 'segmentations': count,
              'locally_feasible_segmentations': feasible, 'fixed_order_dfs_nodes': nodes,
              'solutions': sorted(solutions, key=lambda row: row['ranks']),
              'elapsed_seconds': time.monotonic() - started,
              'scope': 'All width-18 transpositions and injective square mappings conditional on the supplied first crib, standard per-part transposition, and exact first-part source. No digit assignments or historical discovery probability are inferred.'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'solutions'}))


if __name__ == '__main__':
    main()
