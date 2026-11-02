#!/usr/bin/env python3
"""Check p170 search scope, reported candidate arithmetic and synthetic controls.

This uses only Python's standard library. It does not recompute or certify
language rankings. Use run_p170.py with the stated model for that purpose.
"""
from pathlib import Path
import argparse
import json

COORDS = 'ADFGVX'


def transposition_order(length, ranks):
    return sorted(range(length), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))


def decrypt(fragment, length, offset, ranks, square):
    ciphertext = '?' * offset + fragment + '?' * (length - offset - len(fragment))
    order = transposition_order(length, ranks)
    stream = ['?'] * length
    for c, index in zip(ciphertext, order):
        stream[index] = c
    if ''.join(stream[i] for i in order) != ciphertext:
        raise ValueError('Transposition roundtrip failed.')
    text = []
    for i in range(0, length, 2):
        a, b = stream[i:i + 2]
        text.append(square[6 * COORDS.index(a) + COORDS.index(b)]
                    if a in COORDS and b in COORDS else '?')
    return ''.join(text)


def encrypt(plaintext, ranks, square):
    stream = ''.join(COORDS[square.index(c) // 6] + COORDS[square.index(c) % 6]
                     for c in plaintext)
    return ''.join(stream[i] for i in transposition_order(len(stream), ranks))


def verify(experiment):
    source = experiment['source']
    fragment = source['analysis_ciphertext']
    assert ''.join(source['raw_source_grouped'].split()) == fragment
    assert len(fragment) == 106 and set(fragment) <= set(COORDS)
    scope = experiment['search_scope']
    assert scope['minimum_complete_length'] == 106
    assert scope['maximum_complete_length'] == 600
    assert scope['complete_length_step'] == 2
    placements = sum(n - len(fragment) + 1 for n in range(106, 601, 2))
    keys = {row['id']: row for row in experiment['keys']}
    assert len(keys) == 21
    assert placements == scope['placements_per_key'] == 61504
    assert placements * len(keys) == scope['total_placements'] == 1291584
    checked = 0
    for result in experiment['completed_key_results']:
        key = keys[result['key']]
        ranks, square = key['column_rank_order'], key['square']
        assert sorted(ranks) == list(range(1, len(ranks) + 1))
        known = square.replace('?', '')
        assert len(square) == 36 and len(set(known)) == len(known)
        assert result['trials'] == placements
        for row in result['best_candidates']:
            length, offset = row['length'], row['offset']
            assert 106 <= length <= 600 and length % 2 == 0
            assert 0 <= offset <= length - 106
            actual = decrypt(fragment, length, offset, ranks, square)
            assert actual == row['plaintext']
            assert len(actual) - actual.count('?') == row['known_letters']
            assert max(map(len, actual.split('?'))) == row['longest_known_run']
            assert row['rank'] == 1
            if row['pool'] == 'prefix':
                assert offset == 0
            elif row['pool'] == 'suffix':
                assert offset + 106 == length
            elif row['pool'] == 'known_run_at_least5':
                assert row['known_letters'] >= 12 and row['longest_known_run'] >= 5
            checked += 1
    key = keys['Nov7-9']
    for control in experiment['controls']['records']:
        length, offset = control['true_length'], control['true_offset']
        full = encrypt(control['full_plaintext'], key['column_rank_order'], key['square'])
        assert full == control['full_ciphertext'] and len(full) == length
        observed = full[offset:offset + 106]
        assert observed == control['observed_fragment']
        partial = decrypt(observed, length, offset, key['column_rank_order'], key['square'])
        assert partial == control['true_partial_plaintext']
        assert len(partial) - partial.count('?') == control['true_known_characters']
        assert all(a == '?' or a == b for a, b in zip(partial, control['full_plaintext']))
        for hit in control['retained_hits']:
            assert hit['length'] == length and hit['offset'] == offset
            assert hit['plaintext'] == partial
    return {'verified': True, 'placements_per_key': placements,
            'total_target_placements': placements * len(keys),
            'reported_best_candidate_arithmetic_checks': checked,
            'synthetic_control_roundtrips': len(experiment['controls']['records']),
            'language_ranking_recomputed': False,
            'newly_accepted_p170_plaintext': False,
            'truncation_hypothesis_excluded': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.experiment.read_text())), indent=2))


if __name__ == '__main__':
    main()
