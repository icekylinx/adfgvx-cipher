#!/usr/bin/env python3
"""Independent functional-state component CSP for bounded small-width checks."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

CO = 'ADFGVX'


def extend(mapping, extra):
    if any(var in mapping and mapping[var] != value for var, value in extra.items()):
        return None
    merged = {**mapping, **extra}
    complete = [merged[(letter, 0)] * 6 + merged[(letter, 1)]
                for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if (letter, 0) in merged and (letter, 1) in merged]
    if len(complete) != len(set(complete)):
        return None
    return merged


def enumerate_keys(first, ciphertext, width):
    q, remainder = divmod(len(ciphertext), width)
    specifications = [[None if first[i // 2] == '?' else (first[i // 2], i % 2)
                       for i in range(col, 132, width)] for col in range(width)]
    solutions = []
    segmentations = nodes = 0
    for long_slots in combinations(range(width), remainder):
        segmentations += 1
        long_set = set(long_slots)
        chunks, offset = [], 0
        for slot in range(width):
            length = q + (slot in long_set)
            chunks.append(tuple(CO.index(c) for c in ciphertext[offset:offset + length]))
            offset += length
        choices = []
        for spec in specifications:
            local = []
            for chunk_id, chunk in enumerate(chunks):
                if len(chunk) != len(spec):
                    continue
                constraints = {}
                for var, value in zip(spec, chunk):
                    if var is not None:
                        if var in constraints and constraints[var] != value:
                            break
                        constraints[var] = value
                else:
                    if extend({}, constraints) is not None:
                        local.append((chunk_id, constraints))
            if not local:
                break
            choices.append(local)
        if len(choices) != width:
            continue

        def visit(mapping, selected, used):
            nonlocal nodes
            nodes += 1
            if len(selected) == width:
                square = ['?'] * 36
                for letter in set(first) - {'?'}:
                    square[6 * mapping[(letter, 0)] + mapping[(letter, 1)]] = letter
                solutions.append({'ranks': [selected[col] + 1 for col in range(width)], 'partial_square': ''.join(square)})
                return
            best = None
            for col in range(width):
                if col in selected:
                    continue
                available = []
                for chunk_id, constraints in choices[col]:
                    if chunk_id in used:
                        continue
                    merged = extend(mapping, constraints)
                    if merged is not None:
                        available.append((chunk_id, merged))
                if not available:
                    return
                if best is None or len(available) < len(best[1]):
                    best = (col, available)
            col, available = best
            for chunk_id, merged in available:
                visit(merged, {**selected, col: chunk_id}, used | {chunk_id})

        visit({}, {}, set())
    return {'width': width, 'segmentations': segmentations, 'nodes': nodes,
            'solutions': sorted(solutions, key=lambda row: row['ranks'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--widths', type=int, nargs='+', default=[15, 17, 19])
    parser.add_argument('--c-results', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    first, ciphertext, _, _ = args.input.read_text().split()
    assert len(first) == 66 and len(ciphertext) == 132
    results = []
    for width in args.widths:
        assert 14 <= width <= 26
        started = time.monotonic()
        result = enumerate_keys(first, ciphertext, width)
        rows = [json.loads(line) for line in (args.c_results / f'historical_k{width}.jsonl').read_text().splitlines()]
        expected = sorted([{'ranks': row['ranks'], 'partial_square': row['partial_square']}
                           for row in rows if row['kind'] == 'solution'], key=lambda row: row['ranks'])
        assert result['solutions'] == expected
        assert rows[-1]['complete'] and result['segmentations'] == rows[-1]['segmentations']
        result['c_results_equal'] = True
        result['elapsed_seconds'] = time.monotonic() - started
        print(json.dumps({key: value for key, value in result.items() if key != 'solutions'}), flush=True)
        results.append(result)
    args.output.write_text(json.dumps({'independent_functional_state_enumeration': results,
                                      'scope': 'Only the explicitly listed widths were exhaustively rerun in Python.'}, indent=2) + '\n')


if __name__ == '__main__':
    main()
