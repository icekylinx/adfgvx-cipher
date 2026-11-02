#!/usr/bin/env python3
"""Audit p215's 2017 partial reading and a later editorial completion.

This reproduces coordinate constraints; it never chooses an erased symbol.
The correction geometry is Norbert's published two-missing-group hypothesis.
"""
from pathlib import Path
import json
import math
import sys

SYMBOLS = 'ADFGVX'


def untranspose(sequence, ranks):
    n, width = len(sequence), len(ranks)
    lengths = [n // width + (i < n % width) for i in range(width)]
    columns, position = {}, 0
    for column in sorted(range(width), key=ranks.__getitem__):
        columns[column] = sequence[position:position + lengths[column]]
        position += lengths[column]
    return [columns[column][row] for row in range(max(lengths, default=0))
            for column in range(width) if row < lengths[column]]


def transpose(coordinates, ranks):
    return ''.join(''.join(coordinates[column::len(ranks)])
                   for column in sorted(range(len(ranks)), key=ranks.__getitem__))


def encode(plaintext, ranks, square):
    coordinates = ''.join(SYMBOLS[square.index(char) // 6] + SYMBOLS[square.index(char) % 6]
                          for char in plaintext)
    return transpose(coordinates, ranks)


def analyze(source, ranks, square, insertions):
    assert len(square) == len(set(square)) == 36
    augmented, original_indices = [], []
    for i in range(len(source) + 1):
        for insertion in insertions:
            if insertion['original_index'] == i:
                augmented.extend('?' * insertion['count'])
                original_indices.extend([None] * insertion['count'])
        if i < len(source):
            augmented.append(source[i])
            original_indices.append(i)
    augmented = ''.join(augmented)
    pairs = untranspose(augmented, ranks)
    indices = untranspose(list(range(len(augmented))), ranks)
    domains = []
    for i in range(0, len(pairs), 2):
        pair = ''.join(pairs[i:i + 2])
        possible = []
        for cell, char in enumerate(square):
            code = SYMBOLS[cell // 6] + SYMBOLS[cell % 6]
            if all(a == '?' or a == b for a, b in zip(pair, code)):
                possible.append(char)
        ct_indices = indices[i:i + 2]
        domains.append({'plaintext_index': i // 2, 'coordinate_pair': pair,
                        'possible_characters': ''.join(sorted(possible)),
                        'augmented_ciphertext_indices': ct_indices,
                        'original_ciphertext_indices': [original_indices[j] for j in ct_indices]})
    raw = ''.join(row['possible_characters'] if len(row['possible_characters']) == 1 else '?' for row in domains)
    return {'augmented_ciphertext': augmented, 'augmented_to_original_index': original_indices,
            'raw_partial_plaintext': raw, 'domains': domains,
            'fully_determined_plaintext_characters': sum(len(row['possible_characters']) == 1 for row in domains),
            'compatible_plaintext_count': str(math.prod(len(row['possible_characters']) for row in domains))}


def compare_completion(completion, analysis, ranks, square):
    target_length = len(analysis['domains'])
    result = {'plaintext_length': len(completion), 'model_plaintext_length': target_length,
              'length_compatible': len(completion) == target_length}
    if len(completion) == target_length + 1:
        deletion_trials = []
        for i in range(len(completion)):
            candidate = completion[:i] + completion[i + 1:]
            encoded = encode(candidate, ranks, square)
            mismatches = [{'augmented_ciphertext_index': j,
                           'original_ciphertext_index': analysis['augmented_to_original_index'][j],
                           'observed': a, 'proposed': b}
                          for j, (a, b) in enumerate(zip(analysis['augmented_ciphertext'], encoded))
                          if a != '?' and a != b]
            deletion_trials.append({'removed_plaintext_index': i, 'removed_character': completion[i],
                                    'candidate': candidate, 'known_ciphertext_contradictions': mismatches})
        minimum = min(len(row['known_ciphertext_contradictions']) for row in deletion_trials)
        best = [row for row in deletion_trials if len(row['known_ciphertext_contradictions']) == minimum]
        for row in best:
            row['incompatible_plaintext_positions'] = [
                {'plaintext_index': i, 'proposed_character': char,
                 'allowed_characters': analysis['domains'][i]['possible_characters']}
                for i, char in enumerate(row['candidate'])
                if char not in analysis['domains'][i]['possible_characters']]
        result.update({'single_deletion_trials': len(deletion_trials),
                       'minimum_known_ciphertext_contradictions_after_one_plaintext_deletion': minimum,
                       'best_single_deletion_comparisons': best})
    return result


def verify(certificate):
    ranks, square = certificate['key']['column_rank_order'], certificate['key']['square']
    source = certificate['source']['ciphertext']
    actual = analyze(source, ranks, square, certificate['correction_geometry']['insertions'])
    assert actual == certificate['constraints']
    assert transpose(untranspose(actual['augmented_ciphertext'], ranks), ranks) == actual['augmented_ciphertext']
    assert actual['raw_partial_plaintext'] == certificate['published_readings']['norbert_comment32']['raw_plaintext']
    comparison = compare_completion(certificate['published_readings']['baertl_comment39']['plaintext'], actual, ranks, square)
    assert comparison == certificate['editorial_completion_comparison']
    return {'verified': True, 'received_slots': len(source),
            'known_received_coordinates': sum(char != '?' for char in source),
            'augmented_slots': len(actual['augmented_ciphertext']),
            'fully_determined_plaintext_characters': actual['fully_determined_plaintext_characters'],
            'raw_partial_plaintext': actual['raw_partial_plaintext'],
            'compatible_plaintext_count': actual['compatible_plaintext_count'],
            'norbert_2017_partial_reproduced_exactly': True,
            'baertl_2017_length_compatible': comparison['length_compatible'],
            'best_single_deletion_known_ciphertext_contradictions': comparison['minimum_known_ciphertext_contradictions_after_one_plaintext_deletion'],
            'best_single_deletion_incompatible_plaintext_positions': len(comparison['best_single_deletion_comparisons'][0]['incompatible_plaintext_positions'])}


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'data/certificates/p215.json'
    print(json.dumps(verify(json.loads(path.read_text())), indent=2))
