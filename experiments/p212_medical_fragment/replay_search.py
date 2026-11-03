#!/usr/bin/env python3
"""Rebuild and optionally replay the positive p212 A4 length retrieval.

The external, checksummed upstream quadgram table is required. NumPy is needed
only by this optional search replay, never by the primary source verifier.
No model binary or full search log is written. Scores rank hypotheses; they do
not prove a missing length, a lexical completion, or an unknown square fill.

icekylinx and GPT-6 Astra Pro; upstream model credit is in search_provenance.json.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_pinned_inputs(provenance):
    for item in provenance['repository_inputs']:
        if digest(ROOT / item['path']) != item['sha256']:
            raise ValueError('Frozen repository input changed: ' + item['path'])
    inputs = json.loads((HERE / 'inputs.json').read_text())
    dataset = json.loads((ROOT / provenance['radio_dataset']['path']).read_text())
    keys = json.loads((ROOT / 'data/keys.json').read_text())['keys']
    if len(keys) != 25 or len(dataset['training_records']) != 45:
        raise ValueError('Expected the frozen 25-key registry and 45 radio records.')
    if [k['id'] for k in keys] != provenance['key_ids_in_scan_order']:
        raise ValueError('Registered search hypotheses changed.')
    source = ''.join(''.join(inputs['record']['source_rows']).split())
    if len(source) != 197 or set(source) - set(COORDINATES):
        raise ValueError('Expected all 197 original p212 A4 coordinates.')
    if any(r['id'].startswith(('p212', 'p218')) for r in dataset['training_records']):
        raise ValueError('The target family must not be radio-model training data.')
    return inputs, dataset, keys, source


def rebuild_probabilities(np, book_path, dataset, provenance):
    expected = provenance['upstream_quad26']
    if book_path.stat().st_size != expected['bytes'] or digest(book_path) != expected['sha256']:
        raise ValueError('The supplied file is not the pinned upstream data/quad.bin.')
    book_log = np.fromfile(book_path, dtype='<f4')
    if book_log.size != 26**4 or not np.isfinite(book_log).all():
        raise ValueError('Expected 26**4 finite little-endian float32 log10 values.')

    radio = np.full((27,)*4, .01, dtype=np.float64)
    quadgrams = 0
    for record in dataset['training_records']:
        for segment in record['plaintext_layer'].split('?'):
            values = [ord(c)-65 if c.isalpha() else 26 for c in segment]
            for i in range(len(values)-3):
                radio[tuple(values[i:i+4])] += 1
                quadgrams += 1
    if quadgrams != provenance['radio_dataset']['training_quadgrams']:
        raise ValueError('Radio training quadgram count changed.')
    radio /= radio.sum()
    book = np.power(10., book_log.astype(np.float64)).reshape((26,)*4)
    book /= book.sum()
    letters = sum(book.sum(axis=tuple(j for j in range(4) if j != i))
                  for i in range(4))/4
    unigrams = np.concatenate([.97*letters, np.full(10, .003)])
    extended_book = np.einsum('a,b,c,d->abcd', unigrams, unigrams, unigrams, unigrams)
    extended_book[:26, :26, :26, :26] = book*.97**4
    grid = np.indices((36,)*4, dtype=np.int16)
    extended_radio = radio[tuple(np.minimum(grid, 26))]/10.**(grid >= 26).sum(axis=0)
    mixed = .5*extended_book + .5*extended_radio
    if abs(float(mixed.sum())-1.) >= 1e-10:
        raise ValueError('Mixture is not normalized.')

    # The actual search loaded a serialized log10 float32 model. Preserve that
    # quantization before returning to normalized float64 probabilities.
    serialized = np.log10(mixed).astype('<f4')
    rebuilt_hash = hashlib.sha256(serialized.tobytes(order='C')).hexdigest()
    if rebuilt_hash != provenance['rebuilt_model']['sha256']:
        raise ValueError('Rebuilt mixture differs from the recorded quantized model: '+rebuilt_hash)
    probability = np.power(10., serialized.astype(np.float64))
    probability /= probability.sum()
    return probability, rebuilt_hash


def coordinate_model(np, probability, square):
    """Return the original half-pair likelihood-ratio objective.

    Index 6 is an unknown row or column. Partial square cells independently
    average unused labels for retrieval only; this is not a global completion.
    """
    known = {c for c in square if c in ALPHABET}
    unused = sorted(set(ALPHABET)-known)
    masks = np.zeros((49, 36))
    for row in range(7):
        for column in range(7):
            for cell, character in enumerate(square):
                if (row == 6 or row == cell//6) and (column == 6 or column == cell%6):
                    if character in ALPHABET:
                        masks[7*row+column, ALPHABET.index(character)] += 1
                    else:
                        for candidate in unused:
                            masks[7*row+column, ALPHABET.index(candidate)] += 1/len(unused)
    unigrams = sum(probability.sum(axis=tuple(j for j in range(4) if j != i))
                    for i in range(4))/4
    one = masks @ unigrams
    joint = probability.copy()
    for axis in range(4):
        joint = np.moveaxis(np.tensordot(masks, joint, axes=(1, axis)), 0, axis)
    correlation = np.log(joint)
    for axis in range(4):
        shape = [1]*4
        shape[axis] = 49
        correlation -= np.log(one).reshape(shape)
    grid = one.reshape(7, 7)
    single = .5*np.log(one/np.outer(grid[:, 6], grid[6, :]).ravel())
    return single, correlation.astype(np.float32)


def rectangle_to_stream(length, ranks, np):
    indices = np.empty(length, dtype=int)
    cursor = 0
    for column in sorted(range(len(ranks)), key=lambda c: ranks[c]):
        for position in range(column, length, len(ranks)):
            indices[position] = cursor
            cursor += 1
    return indices


def scan(np, source, key, model, layouts):
    single, quad = model
    glyphs = np.asarray([COORDINATES.index(c) for c in source])
    rows = []
    for length, permutation in layouts:
        padded = np.concatenate((np.full(length-197, 6), glyphs))
        interim = padded[permutation]
        patterns = 7*interim[::2] + interim[1::2]
        score = float(single[patterns].sum() + quad[patterns[:-3], patterns[1:-2],
                                                    patterns[2:-1], patterns[3:]].sum())
        fixed = sum(a < 6 and b < 6 and key['square'][6*a+b] in ALPHABET
                    for a, b in zip(interim[::2], interim[1::2]))
        rows.append({'length': length, 'score': score, 'fixed_labels': int(fixed)})
    return sorted(rows, key=lambda row: row['score'], reverse=True)


def check_score(actual, expected, label):
    for field in ('length', 'fixed_labels'):
        if field in expected and actual[field] != expected[field]:
            raise ValueError(label+': changed '+field)
    if abs(actual['score']-expected['score']) > 1e-6:
        raise ValueError(label+': changed score')


def replay(np, probability, inputs, keys, source, provenance):
    evidence = inputs['evidence']
    retrieval = evidence['retrieval']
    controls = evidence['length_retrieval_controls']
    leaders, control_summary = [], []
    main_rows = main_model = main_layouts = main_key = None
    for index, key in enumerate(keys):
        model = coordinate_model(np, probability, key['square'])
        layouts = [(n, rectangle_to_stream(n, key['column_rank_order'], np))
                   for n in range(198, 701, 2)]
        result = scan(np, source, key, model, layouts)
        leaders.append({'key': key['id'], **result[0]})
        for control in controls:
            if control['key'] != key['id']:
                continue
            rows = scan(np, control['source'], key, model, layouts)
            rank = next(i+1 for i, row in enumerate(rows) if row['length'] == control['total'])
            if rank != control['true_total_rank']:
                raise ValueError('Length-control rank changed for '+key['id'])
            control_summary.append({'key': key['id'], 'true_total': control['total'],
                                    'true_total_rank': rank, 'leader': rows[0]})
        if key['id'] == retrieval['actual_key']:
            main_rows, main_model, main_layouts, main_key = result, model, layouts, key
        if (index+1) % 5 == 0:
            print(f'Scanned {index+1}/{len(keys)} key hypotheses.', file=sys.stderr)
    best = max(leaders, key=lambda row: row['score'])
    if best['key'] != retrieval['actual_key']:
        raise ValueError('Global key leader changed.')
    check_score(best, {'length': retrieval['actual_length'], 'score': retrieval['actual_score']}, 'Actual leader')
    check_score(main_rows[1], retrieval['same_key_next_best'], 'Next same-key length')
    other = max((row for row in leaders if row['key'] != best['key']), key=lambda row: row['score'])
    if other['key'] != retrieval['other_key_best']['key']:
        raise ValueError('Other-key leader changed.')
    check_score(other, retrieval['other_key_best'], 'Other-key leader')
    by_length = {row['length']: row for row in main_rows}
    for expected in retrieval['nearby_lengths']:
        check_score(by_length[expected['length']], expected, 'Neighboring length')

    rng = random.Random(provenance['shuffle']['seed'])
    best_scores, at302_scores = [], []
    for i in range(100):
        glyphs = list(source)
        rng.shuffle(glyphs)
        rows = scan(np, ''.join(glyphs), main_key, main_model, main_layouts)
        best_scores.append(rows[0]['score'])
        at302_scores.append(next(row['score'] for row in rows if row['length'] == 302))
    expected = evidence['shuffled_comparison']
    for actual, wanted in zip(best_scores, expected['best_scores']):
        if abs(actual-wanted) > 1e-6:
            raise ValueError('A shuffled maximum changed.')
    for actual, wanted in zip(at302_scores, expected['at302_scores']):
        if abs(actual-wanted) > 1e-6:
            raise ValueError('A shuffled length302 score changed.')
    maximum = max(best_scores)
    greater = sum(score >= best['score'] for score in best_scores)
    if abs(maximum-expected['maximum_shuffled_best']) > 1e-6 or greater != 0:
        raise ValueError('Shuffle comparison changed.')
    if [control['true_total_rank'] for control in control_summary] != [1, 1, 2]:
        raise ValueError('Control ordering or ranks changed.')
    return {'historical_frames': 25*252, 'key_leaders': leaders, 'actual_leader': best,
            'same_key_next_best': main_rows[1], 'other_key_leader': other,
            'nearby_lengths': [by_length[n] for n in range(298, 309, 2)],
            'controls': control_summary, 'control_frames': 3*252,
            'shuffle_count': 100, 'shuffle_frames': 100*252,
            'shuffle_scope': 'Selected Nov22-24 key only; each maximum over 252 even totals.',
            'maximum_shuffled_best': maximum, 'shuffled_greater_or_equal_actual': greater,
            'all_frozen_shuffle_scores_checked': True,
            'limits': provenance['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book-quad26', required=True, type=Path,
                        help='Pinned upstream data/quad.bin; never downloaded automatically.')
    parser.add_argument('--replay', action='store_true',
                        help='Also check 6,300 frames, three controls and 100 same-key shuffles.')
    parser.add_argument('--output', type=Path, help='Optional compact JSON summary; default stdout.')
    args = parser.parse_args()
    provenance = json.loads((HERE / 'search_provenance.json').read_text())
    inputs, dataset, keys, source = load_pinned_inputs(provenance)
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    os.environ.setdefault('OMP_NUM_THREADS', '1')
    try:
        import numpy as np
    except ImportError:
        parser.error('This optional replay requires NumPy; the main verifier does not.')
    probability, model_hash = rebuild_probabilities(np, args.book_quad26, dataset, provenance)
    summary = {'schema': 'adfgvx.p212-search-replay.v1', 'rebuilt_model_sha256': model_hash,
               'model_binary_written': False, 'radio_training_records': 45,
               'numpy_version': np.__version__, 'replayed': args.replay}
    if args.replay:
        summary['search'] = replay(np, probability, inputs, keys, source, provenance)
    encoded = json.dumps(summary, indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
