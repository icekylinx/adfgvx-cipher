#!/usr/bin/env python3
"""Independent column-bucket encoder and suffix-alignment dynamic program.

No repository cipher, transposition, alignment or verifier helper is imported.
icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent


def check():
    d = json.loads((HERE / 'inputs.json').read_text())
    s = ''.join(''.join(d['records'][0]['source_rows']).split())
    k = d['key']
    coords = 'ADFGVX'
    stream = []
    for ch in d['fixed_target']['plaintext']:
        row, col = divmod(k['square'].index(ch), 6)
        stream.extend([coords[row], coords[col]])
    columns = [[] for _ in k['column_rank_order']]
    for i, ch in enumerate(stream):
        columns[i % len(columns)].append(ch)
    target = ''.join(''.join(columns[k['column_rank_order'].index(rank)])
                     for rank in range(1, len(columns) + 1))
    results = []
    for excluded in [None] + [i for i, ch in enumerate(s) if ch == '-']:
        source = ''.join(ch for i, ch in enumerate(s) if i != excluded)
        @lru_cache(None)
        def solve(i, j):
            # Consume suffixes. Extra target positions are added slots;
            # source positions may never be skipped in this branch.
            if len(target) - j < len(source) - i:
                return 10000, 0
            if i == len(source):
                return 0, 1
            options = []
            if j < len(target):
                cost, count = solve(i + 1, j + 1)
                options.append((cost + (source[i] != '-' and source[i] != target[j]), count))
                cost, count = solve(i, j + 1)
                options.append((cost, count))
            best = min(cost for cost, _ in options)
            return best, sum(count for cost, count in options if cost == best)
        cost, count = solve(0, 0)
        results.append({'excluded_printed_mask_index': excluded,
                        'minimum_observed_substitutions': cost,
                        'exact_optimal_map_count': count,
                        'added_slots': len(target) - len(source)})
    return {'method': 'Independent column-bucket encoding and recursive suffix DP with exact integer prices and path counts.',
            'encoded_target_sha256': hashlib.sha256(target.encode()).hexdigest(),
            'encoded_target': target, 'bounds': results}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
