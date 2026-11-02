#!/usr/bin/env python3
"""Verify frozen loss-search witnesses independently of the search engine.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The default check needs only Python's standard library. Optional models
recompute the complete objective, including the independently implemented
word segmentation. No search optimality is asserted.
"""
from __future__ import annotations

import argparse
import array
import hashlib
import json
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_input(ranks, partial, received, missing=5):
    assert isinstance(ranks, list) and 1 <= len(ranks) <= 36
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    assert len(partial) == 36 and set(partial) <= set(ALPHABET + '?')
    fixed = partial.replace('?', '')
    assert len(fixed) == len(set(fixed))
    assert received and set(received) <= set(COORDINATES)
    assert 1 <= missing <= 10 and (len(received) + missing) % 2 == 0


def encrypt_independent(plaintext, ranks, square):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert set(plaintext) <= set(ALPHABET)
    positions = {letter: index for index, letter in enumerate(square)}
    row = ''.join(COORDINATES[positions[c] // 6] +
                  COORDINATES[positions[c] % 6] for c in plaintext)
    width = len(ranks)
    return ''.join(row[column::width]
                   for column in sorted(range(width), key=ranks.__getitem__))


def check_witness(candidate, ranks, partial, received, missing=5):
    validate_input(ranks, partial, received, missing)
    square = candidate['square']
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert all(a == '?' or a == b for a, b in zip(partial, square))
    losses, fills = candidate['loss'], candidate['fill']
    size = len(received) + missing
    assert len(candidate['plaintext']) * 2 == size
    assert len(losses) == missing and losses == sorted(set(losses))
    assert all(isinstance(i, int) and 0 <= i < size for i in losses)
    assert len(fills) == missing and set(fills) <= set(COORDINATES)
    full = encrypt_independent(candidate['plaintext'], ranks, square)
    omitted = set(losses)
    assert ''.join(c for i, c in enumerate(full) if i not in omitted) == received
    assert ''.join(full[i] for i in losses) == fills
    return full


def float32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


class WordModel:
    """Independent dynamic program over (text position, last word id)."""

    def __init__(self, path):
        self.trie = {}
        self.scores = []
        self.pairs = {}
        with path.open() as source:
            word_count, pair_count = map(int, source.readline().split())
            for word_id in range(word_count):
                word, score = source.readline().split()
                assert word.isascii() and word.isalpha() and word.isupper()
                node = self.trie
                for char in word:
                    node = node.setdefault(char, {})
                node[None] = word_id
                self.scores.append(float32(float(score)))
            for _ in range(pair_count):
                first, second, score = source.readline().split()
                self.pairs[int(first), int(second)] = float32(float(score))
            assert not source.read().strip()

    def score(self, text):
        states = [dict() for _ in range(len(text) + 1)]
        states[0][-1] = 0.0
        for start, char in enumerate(text):
            choices = [(start + 1, -1, -.25 if char == 'X' else -3.0)]
            if char.isdigit():
                for end in range(start + 1, min(len(text), start + 10) + 1):
                    if not text[end - 1].isdigit():
                        break
                    choices.append((end, -2, -1.0 - (end - start)))
            node = self.trie
            for end in range(start + 1, min(len(text), start + 32) + 1):
                node = node.get(text[end - 1])
                if node is None:
                    break
                if None in node:
                    word_id = node[None]
                    choices.append((end, word_id, self.scores[word_id]))
            for end, word_id, cost in choices:
                best = max(previous_score + cost +
                           (.65 * self.pairs.get((previous_id, word_id), 0.0)
                            if previous_id >= 0 and word_id >= 0 else 0.0)
                           for previous_id, previous_score in states[start].items())
                states[end][word_id] = max(states[end].get(word_id, -float('inf')), best)
        return max(states[-1].values())


def load_quad(path):
    values = array.array('f')
    values.frombytes(path.read_bytes())
    if sys.byteorder != 'little':
        values.byteswap()
    assert len(values) == 36 ** 4
    return values


def quad_score(text, values):
    symbols = [ALPHABET.index(c) for c in text]
    return sum(values[((a * 36 + b) * 36 + c) * 36 + d]
               for a, b, c, d in zip(symbols, symbols[1:], symbols[2:], symbols[3:]))


def truth_state(truth):
    return {'plaintext': truth['plaintext'], 'square': truth['square'],
            'loss': truth.get('loss', truth.get('missing_full_ciphertext_positions_0based')),
            'fill': truth.get('fill', truth.get('filled_missing_coordinates'))}


def verify(records, quad=None, lexicon=None):
    assert records['engine_source_sha256'] == sha(HERE / 'word_loss.cpp')
    assert records['lexicon_sha256'] == json.loads((HERE / 'lexicon_provenance.json').read_text())['lexicon_sha256']
    observed = next(r for r in json.loads((ROOT / 'data/messages.json').read_text())['messages']
                    if r['id'] == 'p198')['transcript']['analysis_ciphertext']
    quad_values = load_quad(quad) if quad else None
    words = WordModel(lexicon) if lexicon else None
    if quad:
        assert sha(quad) == records['quad_model_sha256']
    if lexicon:
        assert sha(lexicon) == records['lexicon_sha256']
    proposals = historical = controls = exact = objective_checks = 0
    ids = set()
    for row in records['completed']:
        job = row['input']
        assert row['case_id'] not in ids
        ids.add(row['case_id'])
        best, final = row['best_candidate'], row['final_event']
        check_witness(best, job['ranks'], job['partial_square'], job['source'])
        check_witness(final, job['ranks'], job['partial_square'], job['source'])
        assert abs(best['score'] - final['score']) < 1e-6
        assert row['completed_proposals'] == final['proposal'] >= best['proposal']
        assert row['completed_restarts'] == final['restart'] >= 0
        assert final['seconds'] >= job['seconds']
        assert row['accepted_historical_reading'] is False
        proposals += row['completed_proposals']
        if row.get('initial_state'):
            initial = row['initial_state']
            check_witness(initial, job['ranks'], job['partial_square'], job['source'])
        truth = job.get('evaluation_only')
        if truth and truth.get('plaintext'):
            controls += 1
            true_state = truth_state(truth)
            if true_state['fill'] is None:
                full = encrypt_independent(truth['plaintext'], job['ranks'], truth['square'])
                true_state['fill'] = ''.join(full[i] for i in true_state['loss'])
            check_witness(true_state, job['ranks'], job['partial_square'], job['source'])
            correct = sum(a == b for a, b in zip(truth['plaintext'], best['plaintext']))
            assert row['control']['correct_characters'] == correct
            assert row['control']['exact_plaintext'] == (correct == len(truth['plaintext']))
            exact += row['control']['exact_plaintext']
        else:
            historical += 1
            assert job['source'] == observed
        assert abs(best['score'] - best['quad_sum'] -
                   job['word_weight'] * best['word_sum']) < 1e-6
        if quad_values is not None:
            assert abs(quad_score(best['plaintext'], quad_values) - best['quad_sum']) < 1e-6
            objective_checks += 1
        if words is not None:
            assert abs(words.score(best['plaintext']) - best['word_sum']) < 1e-6
    assert len(records['declared_cases']) == len(records['completed']) + len(records['pending'])
    return {'verified': True, 'completed_cases': len(ids), 'historical_cases': historical,
            'control_runs': controls, 'exact_control_runs': exact,
            'completed_mutation_proposals': proposals, 'pending_declared_cases': len(records['pending']),
            'quad_objectives_recomputed': objective_checks,
            'word_objectives_recomputed': len(ids) if words is not None else 0,
            'historical_readings_accepted': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad', type=Path)
    parser.add_argument('--lexicon', type=Path)
    args = parser.parse_args()
    result = verify(json.loads((HERE / 'records.json').read_text()), args.quad, args.lexicon)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
