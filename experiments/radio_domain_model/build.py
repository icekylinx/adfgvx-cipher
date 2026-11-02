#!/usr/bin/env python3
"""Frozen nonchallenge radio-edition model and family-held-out controls.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Editorial source editions are training text, not independently proved
transmitted plaintext. Every selected layer and its dependency hash is kept.
No open-challenge candidate or held-out family is model training material.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'
DEPENDENCIES = {}
EXCLUDED_LATE_KEYS = {'Nov19-21', 'Nov22-24', 'Nov25-28', 'Nov28-Dec1'}
HELD_OUT_IDS = ['p92_A', 'p84_A', 'p190_D', 'p192_2', 'p205_A2', 'p96_B']
CONTROL_KEYS = ['CHI-Nov13', 'Nov13-15b', 'Nov16-18', 'Nov7-9', 'Nov13-15a', 'Oct4-6']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    relative = str(path)
    if relative == 'experiments/tiflis_appointment/inputs.json':
        path = HERE / 'frozen_sources/tiflis_appointment_inputs.json'
    else:
        path = ROOT / relative
    DEPENDENCIES[relative] = sha(path)
    return json.loads(path.read_text())


def family(record_id):
    explicit = {
        'p84_A': 'oil_and_shipping', 'p84_B': 'oil_and_shipping',
        'p92_A': 'Dutch_courier',
        'p190_D': 'Mackensen_relay_request', 'p193_A': 'Mackensen_relay_request',
        'p190_B': 'backup_station_request', 'p190_E': 'backup_station_request',
        'p190_A': 'pilot_arrival', 'p194_B': 'pilot_arrival', 'p193_B': 'pilot_arrival',
        'p192_2': 'Polish_appointment', 'p192_3': 'Polish_appointment',
        'p96_B': 'Filittis_permission',
        'p131_B': 'Kremp_departure', 'p149_B': 'Kremp_departure', 'p159_D': 'Kremp_departure',
        'p146_A': 'Kiel_radio_control',
    }
    if record_id in explicit:
        return explicit[record_id]
    if record_id.startswith('p140_A'):
        return 'Kiel_radio_control'
    if record_id.startswith('p205_A'):
        return 'Crown_finance'
    if record_id.startswith('p205_B'):
        return 'Naval_report_administration'
    return record_id.split('_')[0] + '_' + re.sub(r'[0-9]+$', '', record_id.split('_', 1)[-1])


def source_records():
    records = []

    def add(record_id, key_id, text, path, field, warning=''):
        if key_id in EXCLUDED_LATE_KEYS:
            return
        assert text and set(text) <= set(ALPHABET + '?'), (record_id, field)
        records.append({'id': record_id, 'family': family(record_id), 'key_id': key_id,
                        'plaintext_layer': text, 'dependency': path, 'field': field,
                        'qualification': warning or 'An explicitly costed editorial source edition; its original assumptions and prior credits remain in the dependency.'})

    path = 'experiments/corpus_recovery/certificates.json'
    for r in read(path)['records']:
        text = r['editorial_candidate']['plaintext'] if r['editorial_candidate'] else r['raw_plaintext']
        add(r['id'], r['key_id'], text, path, 'records/editorial_candidate_or_unchanged_raw')

    path = 'experiments/corpus_extension/certificates.json'
    for r in read(path)['records']:
        if r['editorial_candidates']:
            text = r['editorial_candidates'][0]['plaintext']
        else:
            text = r['raw']
        add(r['id'], r['key_id'], text, path, 'records/first_editorial_candidate_or_raw')

    path = 'experiments/october_caucasus/inputs.json'
    for r in read(path)['records']:
        # Omit the two heavily damaged procurement records entirely.
        if r['id'] in ('p68_A1', 'p68_A2'):
            continue
        add(r['id'], 'Oct4-6', r['editorial_template'], path, 'records/editorial_template',
            'The source edition explicitly marks uncertain quantities and names. This is a language-training template, not proof of those details.')

    path = 'experiments/withdrawal_recovery/certificates.json'
    for r in read(path)['records']:
        if r['id'] not in ('p163_A14', 'p163_A17', 'p164_B'):
            continue
        add(r['id'], 'Nov7-9', r['edition']['reading']['plaintext'], path,
            'records/edition/reading/plaintext')

    path = 'experiments/nov14_retransmissions/certificates.json'
    for r in read(path)['records']:
        add(r['id'], r['key_id'], r['readable_candidate']['template'], path,
            'records/readable_candidate/template')

    path = 'experiments/tiflis_appointment/inputs.json'
    for r in read(path)['records']:
        text = r['editorial_candidates'][0]['plaintext'] if r['id'] == 'p192_2' else r['ordinary_word_template']
        add(r['id'], r['key_id'], text, path, 'ordinary_word_layer_only',
            'No TYDELSKI or conditional Y identification is used as training text; the entire appointment family is held out.')

    path = 'experiments/warsaw_service_messages/inputs.json'
    for r in read(path)['records']:
        add(r['id'], r['key_id'], r['editorial_candidates'][0]['plaintext'], path,
            'records/editorial_candidates/0/plaintext')

    path = 'experiments/corpus_joint/p205_readings.json'
    for r in read(path)['results']:
        add(r['id'], r['key_id'], r['editorial_plaintext'], path, 'results/editorial_plaintext')

    path = 'experiments/open_targets_continuation/certificates.json'
    for r in read(path)['results']:
        add(r['id'], r['key_id'], r['editorial']['plaintext'], path, 'results/editorial/plaintext')

    path = 'experiments/corpus_readings/certificates.json'
    for r in read(path)['messages']:
        # The armistice/Kress notice uses later uncertain numeral labels.
        if r['id'].startswith('p218_'):
            continue
        candidate = r.get('editorial_same_length_candidate')
        text = candidate['plaintext'] if candidate else r['direct_reading_under_stated_geometry']['plaintext']
        add(r['id'], r['key']['id'], text, path, 'messages/first_editorial_or_direct_layer')
    ids = [r['id'] for r in records]
    assert len(set(ids)) == len(ids)
    return records


def make_dataset():
    DEPENDENCIES.clear()
    records = source_records()
    by_id = {r['id']: r for r in records}
    held_families = {by_id[i]['family'] for i in HELD_OUT_IDS}
    validation = [r for r in records if r['family'] in held_families]
    held_substrings = {text[i:i + 32]
                       for r in validation for text in r['plaintext_layer'].split('?')
                       for i in range(len(text) - 31)}
    excluded_overlap = []
    training = []
    exact_seen = set()
    for r in records:
        if r['family'] in held_families:
            continue
        text = r['plaintext_layer']
        overlaps = sorted({text[i:i + 32] for i in range(len(text) - 31)} & held_substrings)
        if overlaps:
            excluded_overlap.append({'id': r['id'], 'shared_32_character_substrings': overlaps})
            continue
        if text in exact_seen:
            continue
        exact_seen.add(text)
        training.append(r)
    assert training and validation and not ({r['family'] for r in training} & held_families)
    keys = {k['id']: k for k in read('data/keys.json')['keys']}
    controls = []
    rng = random.Random(202611021631)
    for index, (record_id, key_id) in enumerate(zip(HELD_OUT_IDS, CONTROL_KEYS)):
        source = by_id[record_id]
        # First complete 85-character span is fixed by this deterministic rule.
        text = source['plaintext_layer']
        start = next(i for i in range(len(text) - 84) if '?' not in text[i:i + 85])
        truth = text[start:start + 85]
        key = keys[key_id]
        missing = list(sorted(set(ALPHABET) - set(key['square'])))
        rng.shuffle(missing)
        fill = iter(missing)
        square = ''.join(next(fill) if c == '?' else c for c in key['square'])
        assert set(square) == set(ALPHABET)
        ranks = key['column_rank_order']
        full = encrypt(truth, ranks, square)
        losses = sorted(rng.sample(range(len(full)), 5))
        observed = ''.join(c for i, c in enumerate(full) if i not in losses)
        controls.append({'id': f'radio_holdout_{index}_{record_id}', 'family': source['family'],
                         'source_record': record_id, 'source_span': [start, start + 85],
                         'truth': truth, 'key_id': key_id, 'square': square,
                         'partial_square': key['square'], 'column_rank_order': ranks,
                         'full_ciphertext': full, 'loss_positions': losses,
                         'fill': ''.join(full[i] for i in losses), 'received_ciphertext': observed,
                         'p170_rank_control_truth': truth[:53],
                         'p170_rank_control_ciphertext': encrypt(truth[:53], ranks, square)})
    return {'schema': 'adfgvx-source-radio-model-dataset-v1', 'authors': 'icekylinx and GPT-6 Astra Pro',
            'source_dependency_sha256': dict(sorted(DEPENDENCIES.items())),
            'selection_rule': 'Explicit preferred nonchallenge source-edition layers; selected heavily damaged and late uncertain-label families excluded. Entire six control families and any remaining exact 32-character overlaps are held out. Exact duplicate training strings count once.',
            'training_contains_open_challenge_candidates': False,
            'training_records': training, 'held_out_families': sorted(held_families),
            'held_out_records': validation, 'extra_overlap_exclusions': excluded_overlap,
            'training_characters_with_uncertainty_marks': sum(len(r['plaintext_layer']) for r in training),
            'controls': controls,
            'model_settings_fixed_before_control_search': {
                'collapsed_alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#',
                'digit_mapping': 'All ten digits map to # in the radio component.',
                'unknown_character_handling': 'A ? ends the current training span; no n-gram crosses it.',
                'radio_weight': 0.5, 'book_weight': 0.5,
                'radio_smoothing': 'Add 0.01 to each of 27^4 collapsed four-gram cells, then normalize.',
                'digit_expansion': 'Distribute each radio class probability uniformly over the 10^k specific digit strings.',
                'score': 'Log10 of the equal probability mixture of the book model and expanded radio model.',
            },
            'limits': ['Training uses explicitly conditional editorial texts, with their source provenance; they are not all independently proved transmitted plaintexts.',
                       'The six controls are source-derived synthetic reencryption tests, not additional historical decipherments.',
                       'Model design follows earlier book-model control failures; these held-out source families have not previously been used to tune this new mixture.',
                       'Exact source-family exclusion is not a claim of statistical independence between historical messages.']}


def write_models(dataset, book_path, output):
    import numpy as np
    expected = read('experiments/joint_search/models/provenance.json')['binary_sha256']['german_military36_quad.bin']
    assert sha(book_path) == expected
    count = np.full(27 ** 4, 0.01, dtype=np.float64)
    grams = 0
    for record in dataset['training_records']:
        for span in record['plaintext_layer'].split('?'):
            values = [ord(c) - 65 if c.isalpha() else 26 for c in span]
            for i in range(len(values) - 3):
                code = ((values[i] * 27 + values[i + 1]) * 27 + values[i + 2]) * 27 + values[i + 3]
                count[code] += 1
                grams += 1
    count /= count.sum()
    book = np.power(10.0, np.fromfile(book_path, dtype='<f4').astype(np.float64))
    assert len(book) == 36 ** 4
    book /= book.sum()
    grid = np.indices((36,) * 4, dtype=np.int16)
    numeric = (grid >= 26).sum(axis=0)
    collapsed = np.minimum(grid, 26)
    indices = ((collapsed[0] * 27 + collapsed[1]) * 27 + collapsed[2]).astype(np.int64) * 27 + collapsed[3]
    radio = count[indices] / np.power(10.0, numeric)
    assert abs(radio.sum() - 1) < 1e-10
    mixed = 0.5 * book.reshape((36,) * 4) + 0.5 * radio
    assert abs(mixed.sum() - 1) < 1e-10
    output.mkdir(parents=True, exist_ok=True)
    np.log10(mixed).astype('<f4').tofile(output / 'radio_book36_quad.bin')
    marginal = np.empty((37,) * 4, dtype=np.float64)
    for mask in range(16):
        axes = tuple(i for i in range(4) if mask & (1 << i))
        target = tuple(36 if i in axes else slice(0, 36) for i in range(4))
        marginal[target] = mixed.sum(axis=axes) if axes else mixed
    np.log10(marginal).astype('<f4').tofile(output / 'radio_book37_quad_marginal.bin')
    return {'source_dataset_sha256': sha(HERE / 'dataset.json'),
            'book_quad_sha256': sha(book_path), 'training_quadgrams': grams,
            'training_records': len(dataset['training_records']),
            'model_sha256': {p.name: sha(p) for p in sorted(output.glob('*.bin'))},
            'numpy_version': np.__version__, 'settings': dataset['model_settings_fixed_before_control_search']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-dataset', action='store_true')
    parser.add_argument('--book-quad', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    dataset = make_dataset()
    path = HERE / 'dataset.json'
    if args.verify_dataset:
        assert dataset == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(dataset, indent=2, ensure_ascii=False) + '\n')
    if args.book_quad:
        assert args.output
        report = write_models(dataset, args.book_quad, args.output)
        (HERE / 'model_provenance.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps({'training_records': len(dataset['training_records']),
                          'training_characters': dataset['training_characters_with_uncertainty_marks'],
                          'held_out_controls': len(dataset['controls'])}, indent=2))


if __name__ == '__main__':
    main()
