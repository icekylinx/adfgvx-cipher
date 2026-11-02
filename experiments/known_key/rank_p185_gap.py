#!/usr/bin/env python3
"""Recompute all p185 D gap-ranking scores without research-workspace imports.

Requires NumPy and the checksummed upstream quad26 table. Optional precomputed
quad49/single49 arrays must match the hashes in the published certificate.
This checks heuristic ranking reproducibility, not plaintext uniqueness.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from marginal_model import build, digest, load_quad26

COORDS = 'ADFGVX'


def partial(ciphertext, ranks, square):
    columns = [[] for _ in ranks]
    position = 0
    for column in sorted(range(len(ranks)), key=lambda i: ranks[i]):
        size = len(ciphertext) // len(ranks) + (column < len(ciphertext) % len(ranks))
        columns[column] = ciphertext[position:position + size]
        position += size
    intermediate = ''.join(columns[column][row]
                           for row in range(max(map(len, columns)))
                           for column in range(len(ranks)) if row < len(columns[column]))
    patterns, text = [], []
    for i in range(0, len(intermediate), 2):
        a, b = intermediate[i:i + 2]
        row = COORDS.index(a) if a in COORDS else 6
        column = COORDS.index(b) if b in COORDS else 6
        patterns.append(7 * row + column)
        text.append(square[6 * row + column] if row < 6 and column < 6 else '?')
    return patterns, ''.join(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', required=True, type=Path)
    parser.add_argument('--quad26', required=True, type=Path)
    parser.add_argument('--quad49', type=Path)
    parser.add_argument('--single49', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if bool(args.quad49) != bool(args.single49):
        parser.error('Provide both --quad49 and --single49, or neither.')
    certificate = json.loads(args.certificate.read_text())
    key = certificate['key']
    square, ranks = key['square'], key['column_rank_order']
    quad26 = load_quad26(args.quad26)
    if args.quad49:
        hashes = certificate['search']['ranking_model_files']
        if digest(args.quad49) != hashes['quad']['sha256']:
            raise ValueError('quad49 hash differs from the recorded model.')
        if digest(args.single49) != hashes['single']['sha256']:
            raise ValueError('single49 hash differs from the recorded model.')
        quad = np.fromfile(args.quad49, dtype='<f4').reshape((49,) * 4)
        single = np.fromfile(args.single49, dtype='<f4')
    else:
        quad, single, _ = build(square, quad26)
    source = certificate['source']['ciphertext']
    received = ''.join(c if c in COORDS else '?' for c in source)
    if len(received) != 193 or received.count('?') != 1:
        raise ValueError('Unexpected source geometry.')
    records, maximum_error = [], 0.
    for gap in range(194):
        corrected = received[:gap] + '?????' + received[gap:]
        patterns, raw = partial(corrected, ranks, square)
        score = sum(float(single[p]) for p in patterns)
        score += sum(float(quad[tuple(patterns[i:i + 4])]) / 4 for i in range(96))
        basic = sum(float(quad26[tuple(ord(c) - 65 for c in raw[i:i + 4])])
                    if all('A' <= c <= 'Z' for c in raw[i:i + 4]) else -7.
                    for i in range(96)) / 96
        recorded = certificate['all_contiguous_gap_candidates'][gap]
        if (corrected != recorded['corrected_ciphertext'] or
                raw != recorded['raw_partial_plaintext']):
            raise ValueError('A recorded candidate does not reproduce.')
        maximum_error = max(maximum_error,
                            abs(score - recorded['ranking_heuristic_score']),
                            abs(basic - recorded['legacy_plaintext_quadgram_mean']))
        records.append({'gap_before_source_index': gap,
                        'ranking_heuristic_score': score,
                        'legacy_plaintext_quadgram_mean': basic})
    composite_order = sorted(range(194), key=lambda i: (-records[i]['ranking_heuristic_score'], i))
    basic_order = sorted(range(194), key=lambda i: (-records[i]['legacy_plaintext_quadgram_mean'], i))
    if composite_order != certificate['search']['ranked_gap_positions']:
        raise ValueError('The composite ranking differs from the published ranking.')
    if basic_order != certificate['search']['legacy_quadgram_ranked_gap_positions']:
        raise ValueError('The conventional ranking differs from the published ranking.')
    if maximum_error > 1e-6:
        raise ValueError('The ranking score discrepancy exceeds 1e-6.')
    output = {'status': 'reproduced', 'placements': 194,
              'maximum_absolute_score_discrepancy': maximum_error,
              'composite_best_gap': composite_order[0],
              'legacy_best_gap': basic_order[0],
              'all_scores': records,
              'caveat': 'Ranking remains heuristic; every geometry is cryptographically compatible.'}
    text = json.dumps(output, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
