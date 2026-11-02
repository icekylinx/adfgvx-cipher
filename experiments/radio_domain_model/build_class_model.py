#!/usr/bin/env python3
"""A distinct 27-class objective with four further source-family holdouts.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
This is an adaptive follow-up to the 36-symbol mixture's reference-field
errors. It deliberately cannot identify individual digit labels.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    base = json.loads((HERE / 'dataset.json').read_text())
    rows = base['training_records']
    by_id = {r['id']: r for r in rows}
    specifications = [('Kiel_radio_control', ['p140_A1', 'p140_A2'], 'Nov13-15b'),
                      ('LP_forwarding', ['p192_B'], 'CHI-Nov13'),
                      ('Budapest_telephone', ['p85_B'], 'Nov13-15a'),
                      ('Naval_reports', ['p205_B1'], 'Nov7-9')]
    excluded = {by_id[rid]['family'] for _, ids, _ in specifications for rid in ids}
    validation_rows = [r for r in rows if r['family'] in excluded]
    shared = {text[i:i + 32] for r in validation_rows for text in r['plaintext_layer'].split('?')
              for i in range(len(text) - 31)}
    training, overlap = [], []
    for row in rows:
        if row['family'] in excluded:
            continue
        text = row['plaintext_layer']
        if shared & {text[i:i + 32] for i in range(len(text) - 31)}:
            overlap.append(row['id'])
        else:
            training.append(row)
    keys = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    controls = []
    rng = random.Random(202611021647)
    for i, (name, ids, key_id) in enumerate(specifications):
        joined = 'X'.join(by_id[rid]['plaintext_layer'] for rid in ids)
        start = next(j for j in range(len(joined) - 84) if '?' not in joined[j:j + 85])
        truth = joined[start:start + 85]
        key = keys[key_id]
        partial = key['square']
        if key_id == 'Nov13-15b':
            # A synthetic true square consistent with the new historical condition.
            assert partial[17] == '?' and 'Y' not in partial
            partial = partial[:17] + 'Y' + partial[18:]
        unused = sorted(set(ALPHABET) - set(partial))
        rng.shuffle(unused)
        values = iter(unused)
        square = ''.join(next(values) if c == '?' else c for c in partial)
        full = encrypt(truth, key['column_rank_order'], square)
        losses = sorted(rng.sample(range(170), 5))
        controls.append({'id': f'class_holdout_{i}_{name}', 'source_record_ids': ids,
                         'synthetic_join_separator': 'X' if len(ids) > 1 else None,
                         'source_span': [start, start + 85], 'truth': truth,
                         'truth_classes': ''.join('#' if c.isdigit() else c for c in truth),
                         'key_id': key_id, 'square': square, 'partial_square': partial,
                         'column_rank_order': key['column_rank_order'], 'full_ciphertext': full,
                         'loss_positions': losses, 'fill': ''.join(full[j] for j in losses),
                         'received_ciphertext': ''.join(c for j, c in enumerate(full) if j not in losses)})
    return {'schema': 'adfgvx-radio-27class-followup-v1',
            'authors': 'icekylinx and GPT-6 Astra Pro',
            'base_dataset_sha256': sha(HERE / 'dataset.json'),
            'key_catalog_sha256': sha(ROOT / 'data/keys.json'),
            'adaptation': 'Designed after observing that the first 36-symbol mixture could favor letters in numerical reference fields. Earlier six held-out controls are now development observations, not fresh validation for this variant.',
            'further_held_out_families': sorted(excluded),
            'training_records': training, 'validation_records': validation_rows,
            'additional_overlap_exclusions': overlap, 'controls': controls,
            'fixed_settings': {'alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#', 'radio_weight': 0.5,
                               'book_weight': 0.5, 'pseudocount_per_radio_fourgram': 0.01,
                               'specific_digit_labels_scored_identically': True,
                               'wildcards': 'Marginalize over distinct classes, counting the numerical class once.'},
            'limits': ['No score in this variant can distinguish the ten individual digit labels.',
                       'Source-edition assumptions remain inherited, and the four new families are removed from training.',
                       'This is a heuristic language objective, not a ciphertext exclusion test.']}


def models(dataset, book_path, output):
    import numpy as np
    expected = json.loads((ROOT / 'experiments/joint_search/models/provenance.json').read_text())['binary_sha256']['german_military36_quad.bin']
    assert sha(book_path) == expected
    grid = np.indices((36,) * 4, dtype=np.int16)
    folded = np.minimum(grid, 26)
    indices = (((folded[0] * 27 + folded[1]) * 27 + folded[2]).astype(np.int64) * 27 + folded[3])
    old = np.power(10., np.fromfile(book_path, dtype='<f4').astype(np.float64))
    old /= old.sum()
    book27 = np.bincount(indices.ravel(), weights=old, minlength=27 ** 4)
    radio27 = np.full(27 ** 4, 0.01, dtype=np.float64)
    grams = 0
    for row in dataset['training_records']:
        for span in row['plaintext_layer'].split('?'):
            values = [ord(c) - 65 if c.isalpha() else 26 for c in span]
            for i in range(len(values) - 3):
                code = ((values[i] * 27 + values[i + 1]) * 27 + values[i + 2]) * 27 + values[i + 3]
                radio27[code] += 1
                grams += 1
    radio27 /= radio27.sum()
    output.mkdir(parents=True, exist_ok=True)
    files = []
    for name, probabilities in [('book_class', book27), ('radio_book_class', (book27 + radio27) / 2)]:
        assert abs(probabilities.sum() - 1) < 1e-10
        np.log10(probabilities[indices]).astype('<f4').tofile(output / (name + '36_quad.bin'))
        base = probabilities.reshape((27,) * 4)
        marginal = np.empty((28,) * 4, dtype=np.float64)
        for mask in range(16):
            axes = tuple(i for i in range(4) if mask & (1 << i))
            target = tuple(27 if i in axes else slice(0, 27) for i in range(4))
            marginal[target] = base.sum(axis=axes) if axes else base
        lookup = np.array(list(range(26)) + [26] * 10 + [27])
        encoded = marginal[np.ix_(lookup, lookup, lookup, lookup)]
        assert encoded[36, 36, 36, 36] == 1 or abs(encoded[36, 36, 36, 36] - 1) < 1e-10
        np.log10(encoded).astype('<f4').tofile(output / (name + '37_quad_marginal.bin'))
        files.extend([name + '36_quad.bin', name + '37_quad_marginal.bin'])
    return {'dataset_sha256': sha(HERE / 'class_dataset.json'), 'book_quad_sha256': sha(book_path),
            'training_quadgrams': grams, 'training_records': len(dataset['training_records']),
            'model_sha256': {name: sha(output / name) for name in files},
            'numpy_version': np.__version__, 'score_space': '27 classes; 36/37-index files are lookup adapters, not normalized distributions over 36 distinct symbols.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-dataset', action='store_true')
    parser.add_argument('--book-quad', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    dataset = prepare()
    path = HERE / 'class_dataset.json'
    if args.verify_dataset:
        assert dataset == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(dataset, indent=2, ensure_ascii=False) + '\n')
    if args.book_quad:
        assert args.output
        report = models(dataset, args.book_quad, args.output)
        (HERE / 'class_model_provenance.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps({'training_records': len(dataset['training_records']), 'fresh_controls': len(dataset['controls'])}))


if __name__ == '__main__':
    main()
