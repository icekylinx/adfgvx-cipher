#!/usr/bin/env python3
"""Optional p228 B2 discovery replay. Requires NumPy and pinned quad26 data.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = 'ADFGVX'
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mappings(source):
    n = len(source)
    for start in range(n):
        end = start
        while end < n and source[end] == '?':
            end += 1
            length = end - start
            block = list(range(start, end))
            rest = list(range(start)) + list(range(end, n))
            for destination in range(n - length + 1):
                yield [start, length, destination], rest[:destination] + block + rest[destination:]


def build_model(np, quad26, key, provenance):
    path = ROOT / 'experiments/p212_medical_fragment/replay_search.py'
    spec = importlib.util.spec_from_file_location('p212_probability', path)
    prior_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior_module)
    prior = json.loads((path.parent / 'search_provenance.json').read_text())
    _, dataset, _, _ = prior_module.load_pinned_inputs(prior)
    probability, mixture_hash = prior_module.rebuild_probabilities(np, quad26, dataset, prior)
    assert mixture_hash == provenance['mixture_sha256']
    masks = np.zeros((49, 36))
    # A bijective language-scoring shadow: late-period Y is commonly a separator.
    # This does not change any reported ciphertext, raw reading or key register.
    projection = {'X': 'Y', 'Y': 'X'}
    for pattern in range(49):
        row, col = divmod(pattern, 7)
        for cell, label in enumerate(key['square']):
            if (row == 6 or row == cell // 6) and (col == 6 or col == cell % 6):
                masks[pattern, AL.index(projection.get(label, label))] = 1.
    joint = probability
    for axis in range(4):
        joint = np.moveaxis(np.tensordot(masks, joint, axes=(1, axis)), 0, axis)
    assert np.isfinite(joint).all() and joint.min() > 0
    assert abs(float(joint[48, 48, 48, 48]) - 1.) < 1e-10
    model = np.log(joint).astype('<f4')
    assert hashlib.sha256(model.tobytes()).hexdigest() == provenance['joint49_sha256']
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad26', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
        os.environ[name] = '1'
    import numpy as np
    provenance = json.loads((HERE / 'search_provenance.json').read_text())
    for name, digest in provenance['pinned_repository_files'].items():
        assert sha(ROOT / name) == digest, name
    data = json.loads((HERE / 'inputs.json').read_text())
    key = data['key']
    source = ''.join(''.join(data['records'][0]['source_rows']).split()).replace('-', '?')
    n, width = len(source), len(key['column_rank_order'])
    assert n == 264 and source.count('?') == 43
    emit = [i for col in sorted(range(width), key=lambda c: key['column_rank_order'][c])
            for i in range(col, n, width)]
    inverse = np.empty(n, dtype=np.int16)
    for wire, middle in enumerate(emit):
        inverse[middle] = wire
    quad = build_model(np, args.quad26, key, provenance)

    def raw(wire):
        middle = ''.join(wire[int(i)] for i in inverse)
        return ''.join('?' if '?' in middle[i:i + 2] else
                       key['square'][6 * CO.index(middle[i]) + CO.index(middle[i + 1])]
                       for i in range(0, n, 2))

    def encode(plaintext):
        middle = ''.join(CO[key['square'].index(c) // 6] + CO[key['square'].index(c) % 6]
                         for c in plaintext)
        return ''.join(middle[i] for i in emit)

    def scan(observed):
        values = np.array([CO.index(c) if c in CO else 6 for c in observed], dtype=np.int16)
        best, winners, evaluated = -float('inf'), [], 0
        maps, ops = [], []

        def batch():
            nonlocal best, winners, evaluated
            middle = values[np.array(maps, dtype=np.int16)][:, inverse]
            pattern = middle[:, ::2] * 7 + middle[:, 1::2]
            scores = quad[pattern[:, :-3], pattern[:, 1:-2], pattern[:, 2:-1], pattern[:, 3:]].sum(axis=1, dtype=np.float64)
            evaluated += len(maps)
            top = float(scores.max())
            if top < best - 1e-8:
                return
            if top > best + 1e-8:
                best, winners = top, []
            for j in np.flatnonzero(abs(scores - best) < 1e-8):
                owners = maps[int(j)]
                assert sorted(owners) == list(range(n))
                assert [i for i in owners if source[i] != '?'] == [i for i, c in enumerate(source) if c != '?']
                wire = ''.join(observed[i] for i in owners)
                text = raw(wire)
                assert encode(raw(wire.replace('?', 'A'))) == wire.replace('?', 'A')
                winners.append(dict(operation=ops[int(j)], raw=text))

        for operation, owners in mappings(source):
            maps.append(owners)
            ops.append(operation)
            if len(maps) == 2000:
                batch()
                maps, ops = [], []
        if maps:
            batch()
        assert evaluated == 124628
        assert len({x['raw'] for x in winners}) == 1
        return dict(evaluations=evaluated, best_score=best, winner_raw=winners[0]['raw'],
                    winner_operations=[x['operation'] for x in winners])

    output = dict(historical=scan(source), controls=[])
    expected = provenance['historical']
    assert abs(output['historical']['best_score'] - expected['best_score']) < 1e-8
    assert output['historical']['winner_raw'] == expected['winner_raw']
    assert output['historical']['winner_operations'] == expected['winner_operations']
    for control in provenance['controls']:
        start, length, destination = control['planted_operation']
        rest = list(range(start)) + list(range(start + length, n))
        owners = rest[:destination] + list(range(start, start + length)) + rest[destination:]
        full = encode(control['plaintext'])
        observed = ['?'] * n
        for model, origin in enumerate(owners):
            if source[origin] != '?':
                observed[origin] = full[model]
        observed = ''.join(observed)
        assert observed == control['source']
        result = scan(observed)
        expected = control['result']
        assert abs(result['best_score'] - expected['best_score']) < 1e-8
        assert result['winner_raw'] == expected['winner_raw']
        assert result['winner_operations'] == expected['winner_operations']
        assert all(c == '?' or c == control['plaintext'][i] for i, c in enumerate(result['winner_raw']))
        fixed = n // 2 - result['winner_raw'].count('?')
        assert fixed == expected['fixed_correct']
        output['controls'].append(dict(id=control['id'], fixed_correct=fixed,
                                      planted_raw_recovered=result['winner_raw'] == control['planted_raw'],
                                      **result))
    output['limits'] = provenance['limits']
    text = json.dumps(output, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
