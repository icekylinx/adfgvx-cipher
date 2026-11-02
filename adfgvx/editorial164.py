#!/usr/bin/env python3
"""Verify conditional p164 A4 edit arithmetic, without a language model.

Usage: python -m adfgvx.editorial164 [certificate.json]
Requires only Python's standard library. A successful roundtrip proves the
stated arithmetic; it does not establish the historical truth of an edit.
"""
from pathlib import Path
import itertools
import json
import sys

COORDINATES = 'ADFGVX'
PLAINTEXT = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def inverse_order(ciphertext, ranks):
    width = len(ranks)
    positions = sorted(range(len(ciphertext)), key=lambda i: (ranks[i % width], i // width))
    stream = [''] * len(ciphertext)
    mapping = [None] * len(ciphertext)
    for source_index, intermediate_index in enumerate(positions):
        stream[intermediate_index] = ciphertext[source_index]
        mapping[intermediate_index] = source_index
    return ''.join(stream), mapping


def forward_order(stream, ranks):
    return ''.join(stream[i] for i in sorted(
        range(len(stream)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks))))


def complete_squares(partial):
    missing = [c for c in PLAINTEXT if c not in partial]
    indices = [i for i, c in enumerate(partial) if c == '?']
    assert len(indices) == len(missing) == 2
    result = []
    for permutation in itertools.permutations(missing):
        square = list(partial)
        for i, value in zip(indices, permutation):
            square[i] = value
        assert set(square) == set(PLAINTEXT)
        result.append(''.join(square))
    return result


def domains(ciphertext, ranks, squares):
    stream, mapping = inverse_order(ciphertext, ranks)
    result = []
    for i in range(0, len(stream), 2):
        observed = stream[i:i + 2]
        choices = set()
        for square in squares:
            for cell, char in enumerate(square):
                pair = COORDINATES[cell // 6] + COORDINATES[cell % 6]
                if all(a == '?' or a == b for a, b in zip(observed, pair)):
                    choices.add(char)
        result.append(''.join(sorted(choices)))
    return result, stream, mapping


def encrypt(plaintext, ranks, square):
    stream = ''.join(COORDINATES[square.index(c) // 6] + COORDINATES[square.index(c) % 6]
                     for c in plaintext)
    return forward_order(stream, ranks)


def apply_edits(source, variant):
    result = list(source)
    seen = set()
    for field in ['known_symbol_substitutions', 'erasure_fills']:
        for edit in variant[field]:
            i = edit['source_index']
            assert i not in seen
            seen.add(i)
            assert result[i] == edit['observed']
            assert edit['replacement'] in COORDINATES
            if field == 'known_symbol_substitutions':
                assert result[i] in COORDINATES
            else:
                assert result[i] == '?'
            result[i] = edit['replacement']
    return ''.join(result)


def verify(record):
    source = record['raw_source_ciphertext']
    ranks = record['key']['column_rank_order']
    squares = complete_squares(record['key']['square'])
    assert ''.join(record['raw_source_grouped'].split()) == source
    assert len(source) == 198 and source.count('?') == 13
    raw_domains, raw_stream, _ = domains(source, ranks, squares)
    raw = ''.join(d if len(d) == 1 else '?' for d in raw_domains)
    assert raw == record['raw_source_plaintext']
    assert len(raw) == 99 and raw.count('?') == 12
    assert forward_order(raw_stream, ranks) == source
    output = []
    for name, known, filled in [('hypothesis', 8, 12), ('full_editorial_hypothesis', 9, 13)]:
        variant = record[name]
        assert len(variant['known_symbol_substitutions']) == known
        assert len(variant['erasure_fills']) == filled
        corrected = apply_edits(source, variant)
        expected = variant['analysis']
        assert corrected == expected['corrected_ciphertext']
        values, stream, mapping = domains(corrected, ranks, squares)
        actual = ''.join(d if len(d) == 1 else '?' for d in values)
        assert actual == expected['raw_partial_plaintext']
        assert forward_order(stream, ranks) == corrected
        for i, (choices, row) in enumerate(zip(values, expected['domains'])):
            assert choices == row['possible_characters']
            assert row['plaintext_index'] == i
            assert row['coordinate_pair'] == stream[2 * i:2 * i + 2]
            assert row['source_ciphertext_indices'] == mapping[2 * i:2 * i + 2]
        if name == 'hypothesis':
            assert values[10] == '02ACLR'
            assert sum(len(v) > 1 for v in values) == 1
            assert len(record['conditional_complete_roundtrips']) == 6
            for trial in record['conditional_complete_roundtrips']:
                assert trial['plaintext'][10] in values[10]
                assert trial['plaintext'][:10] + '?' + trial['plaintext'][11:] == actual
                for square in squares:
                    encrypted = encrypt(trial['plaintext'], ranks, square)
                    assert encrypted == trial['reencrypted_ciphertext']
                    assert all(a == '?' or a == b for a, b in zip(corrected, encrypted))
        else:
            assert actual == record['full_editorial_plaintext']
            assert '?' not in actual
            for square in squares:
                assert encrypt(actual, ranks, square) == corrected
        output.append({'id': variant['id'], 'known_coordinate_substitutions': known,
                       'guessed_erasure_values': filled, 'verified_partial_plaintext': actual,
                       'coordinate_roundtrip': True})
    return {
        'verified': True,
        'source_slots': 198,
        'source_known_coordinates': 185,
        'source_erasures': 13,
        'source_forced_plaintext_characters': 87,
        'source_plaintext_length': 99,
        'conditional_eight_repair_completions': 6,
        'full_nine_repair_roundtrip': True,
        'historical_repairs_proved': False,
        'variants': output,
    }


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'data/certificates/p164_A4_editorial.json'
    print(json.dumps(verify(json.loads(path.read_text())), indent=2))
