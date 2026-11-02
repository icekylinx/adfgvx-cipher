#!/usr/bin/env python3
"""Reproduce p164 source constraints and distinguish 2017 guesses from data.

All missing-coordinate completions and the two unassigned square digits remain
explicit. The two digit permutations are considered jointly, not independently
chosen at each occurrence. No language model enters this verification.
"""
from pathlib import Path
import itertools
import hashlib
import argparse
import json
import math
import sys

SYMBOLS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def untranspose(sequence, ranks):
    n, width = len(sequence), len(ranks)
    lengths = [n // width + (column < n % width) for column in range(width)]
    columns, position = {}, 0
    for column in sorted(range(width), key=ranks.__getitem__):
        columns[column] = sequence[position:position + lengths[column]]
        position += lengths[column]
    return [columns[column][row] for row in range(max(lengths, default=0))
            for column in range(width) if row < lengths[column]]


def transpose(coordinates, ranks):
    return ''.join(''.join(coordinates[column::len(ranks)])
                   for column in sorted(range(len(ranks)), key=ranks.__getitem__))


def square_completions(square):
    unknown = [i for i, char in enumerate(square) if char == '?']
    unused = [char for char in ALPHABET if char not in square]
    assert len(unknown) == len(unused) == 2
    result = []
    for permutation in itertools.permutations(unused):
        completed = list(square)
        for index, char in zip(unknown, permutation):
            completed[index] = char
        result.append(''.join(completed))
    return result


def apply_variant(source, variant):
    deleted = {edit['source_index']: edit for edit in variant.get('deletions', [])}
    replaced = {edit['source_index']: edit for edit in variant.get('known_symbol_substitutions', [])}
    filled = {edit['source_index']: edit for edit in variant.get('erasure_fills', [])}
    output, mapping = [], []
    for i in range(len(source) + 1):
        for insertion in variant.get('insertions', []):
            if insertion['source_index'] == i:
                output.extend(insertion['value'])
                mapping.extend([None] * len(insertion['value']))
        if i == len(source):
            continue
        if i in deleted:
            assert source[i] == deleted[i]['observed']
            continue
        char = source[i]
        if i in replaced:
            assert char == replaced[i]['observed'] and char in SYMBOLS
            char = replaced[i]['replacement']
        if i in filled:
            assert char == '?'
            char = filled[i]['replacement']
        output.append(char)
        mapping.append(i)
    return ''.join(output), mapping


def analyze(source, variant, ranks, square):
    ciphertext, mapping = apply_variant(source, variant)
    assert len(ciphertext) % 2 == 0
    coordinates = untranspose(ciphertext, ranks)
    indices = untranspose(list(range(len(ciphertext))), ranks)
    completions = square_completions(square)
    all_domains = []
    per_square_domains = [[] for _ in completions]
    for i in range(0, len(coordinates), 2):
        pair = ''.join(coordinates[i:i + 2])
        union = set()
        for j, complete_square in enumerate(completions):
            possible = set()
            for cell, char in enumerate(complete_square):
                code = SYMBOLS[cell // 6] + SYMBOLS[cell % 6]
                if all(a == '?' or a == b for a, b in zip(pair, code)):
                    possible.add(char)
            per_square_domains[j].append(possible)
            union.update(possible)
        ct_indices = indices[i:i + 2]
        all_domains.append({'plaintext_index': i // 2, 'coordinate_pair': pair,
                            'corrected_ciphertext_indices': ct_indices,
                            'source_ciphertext_indices': [mapping[index] for index in ct_indices],
                            'possible_characters': ''.join(sorted(union))})
    sizes = [math.prod(len(domain) for domain in domains) for domains in per_square_domains]
    intersection_size = math.prod(len(a & b) for a, b in zip(*per_square_domains))
    count = sum(sizes) - intersection_size
    assert sizes == [6 ** ciphertext.count('?')] * 2
    raw = ''.join(row['possible_characters'] if len(row['possible_characters']) == 1 else '?'
                  for row in all_domains)
    assert transpose(coordinates, ranks) == ciphertext
    return {'corrected_ciphertext': ciphertext, 'corrected_to_source_index': mapping,
            'corrected_length': len(ciphertext), 'known_coordinates': len(ciphertext) - ciphertext.count('?'),
            'erased_coordinates': ciphertext.count('?'), 'raw_partial_plaintext': raw,
            'fixed_plaintext_characters': sum(len(row['possible_characters']) == 1 for row in all_domains),
            'domains': all_domains,
            'compatible_plaintexts_for_each_fixed_digit_assignment': str(sizes[0]),
            'compatible_plaintext_intersection_across_digit_assignments': str(intersection_size),
            'distinct_compatible_plaintexts_across_both_digit_assignments': str(count)}


def verify(certificate):
    ranks, square = certificate['key']['column_rank_order'], certificate['key']['square']
    sources = {source['id']: source['ciphertext'] for source in certificate['sources']}
    summaries = []
    for variant in certificate['variants']:
        actual = analyze(sources[variant['source_id']], variant, ranks, square)
        expected = variant['expected_analysis']
        for field, value in expected.items():
            if field != 'full_analysis_sha256':
                assert actual[field] == value, (variant['id'], field)
        digest = hashlib.sha256(json.dumps(actual, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        assert digest == expected['full_analysis_sha256'], variant['id']
        summaries.append({'id': variant['id'], 'scope': variant['scope'],
                          'length': actual['corrected_length'], 'known_coordinates': actual['known_coordinates'],
                          'fixed_plaintext_characters': actual['fixed_plaintext_characters'],
                          'known_source_substitutions': len(variant.get('known_symbol_substitutions', [])),
                          'guessed_erased_coordinates': len(variant.get('erasure_fills', [])),
                          'raw_partial_plaintext': actual['raw_partial_plaintext']})
    return {'verified': True, 'unassigned_square_symbols': '56',
            'all_coordinate_roundtrips_verified': True, 'variants': summaries}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', default=str(Path(__file__).resolve().parent.parent / 'data/certificates/p164.json'))
    parser.add_argument('--details', action='store_true', help='Emit every recomputed coordinate mapping and character domain')
    args = parser.parse_args()
    certificate = json.loads(Path(args.certificate).read_text())
    result = verify(certificate)
    if args.details:
        sources = {source['id']: source['ciphertext'] for source in certificate['sources']}
        result['full_analyses'] = {variant['id']: analyze(sources[variant['source_id']], variant, certificate['key']['column_rank_order'], certificate['key']['square']) for variant in certificate['variants']}
    print(json.dumps(result, indent=2))
