#!/usr/bin/env python3
"""Portable optional replay of the p215 A source-layout discovery.

Requires NumPy, a C compiler and the pinned external quad26 file. Models and
executables live only in a temporary directory. Language scores rank source
hypotheses; they neither establish historical layout nor certify word repairs.
ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = 'ADFGVX'
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_inputs(prov):
    for path, expected in prov['pinned_repository_files'].items():
        if digest(ROOT / path) != expected:
            raise ValueError('Pinned repository input changed: ' + path)
    key = next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']
               if k['id'] == 'Nov22-24')
    audit = json.loads((ROOT/'data/reviews/source_gap_audit_20261103.json').read_text())
    row = next(r for r in audit['records'] if r['id'] == 'p215_A')
    source = ''.join(''.join(row['source_rows']).split()).replace('-', '?')
    assert len(source) == 390 and source.count('?') == 18
    assert hashlib.sha256(source.encode()).hexdigest() == prov['source_analysis_sha256']
    return key, source


def build_model(np, quad26, key, prov):
    path = ROOT/'experiments/p212_medical_fragment/replay_search.py'
    spec = importlib.util.spec_from_file_location('p212_replay', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    prior = json.loads((path.parent/'search_provenance.json').read_text())
    _, dataset, _, _ = module.load_pinned_inputs(prior)
    probability, mixture_hash = module.rebuild_probabilities(np, quad26, dataset, prior)
    masks = np.zeros((49, 36))
    labels = []
    for pattern in range(49):
        row, col = divmod(pattern, 7)
        indices = [AL.index(key['square'][cell]) for cell in range(36)
                   if (row == 6 or cell//6 == row) and (col == 6 or cell%6 == col)]
        labels.append(indices)
        masks[pattern, indices] = 1.
    joint = probability.copy()
    for axis in range(4):
        joint = np.moveaxis(np.tensordot(masks, joint, axes=(1, axis)), 0, axis)
    assert np.isfinite(joint).all() and joint.min() > 0
    logs = np.log(joint)
    for pattern in [(48, 48, 48, 48), (0, 0, 0, 0), (6, 42, 47, 48)]:
        direct = np.log(probability[np.ix_(*(labels[p] for p in pattern))].sum())
        assert abs(float(direct)-float(logs[pattern])) < 1e-12
    model = logs.astype('<f4')
    assert hashlib.sha256(model.tobytes()).hexdigest() == prov['joint49_sha256']
    return model, mixture_hash


def frames(source):
    for a in range(155, 160):
        for b in range(184, 189):
            owners, chars = [], []
            for i, c in enumerate(source):
                if i in (a, b):
                    chars.append('?'); owners.append(None)
                chars.append(c); owners.append(i)
            yield [a, b], ''.join(chars), owners


def move_groups(sequence, kind, a, b):
    groups = [sequence[i:i+5] for i in range(0, 390, 5)] + [sequence[390:]]
    assert list(map(len, groups)) == [5]*78+[2]
    if kind == 1:
        groups[a], groups[b] = groups[b], groups[a]
    elif kind == 2:
        groups.insert(b, groups.pop(a))
    return sum(groups, []) if isinstance(sequence, list) else ''.join(groups)


def coordinate_model(source, a, b, destination):
    chars, owners = [], []
    for i, c in enumerate(source):
        if i in (a, b):
            chars.append('?'); owners.append(None)
        if 195 <= i < 200:
            assert c == '?'
            continue
        chars.append(c); owners.append(i)
    assert len(chars) == 387 and 0 <= destination <= 387
    return (''.join(chars[:destination])+'?'*5+''.join(chars[destination:]),
            owners[:destination]+list(range(195, 200))+owners[destination:])


def verify_owners(source, wire, owners):
    assert len(wire) == len(owners) == 392
    assert sorted(i for i in owners if i is not None) == list(range(390))
    assert sum(i is None for i in owners) == 2
    assert all(i is None or wire[j] == source[i] for j, i in enumerate(owners))


def evaluate(np, wire, key, quad, permutation):
    values = np.fromiter((CO.index(c) if c in CO else 6 for c in wire),
                         dtype=np.int8, count=392)
    interim = np.empty(392, dtype=np.int8)
    interim[permutation] = values
    pattern = interim[::2]*7+interim[1::2]
    score = float(quad[pattern[:-3], pattern[1:-2], pattern[2:-1], pattern[3:]]
                  .sum(dtype=np.float64))
    raw = ''.join('?' if x == 6 or y == 6 else key['square'][6*x+y]
                  for x, y in zip(interim[::2], interim[1::2]))
    return raw, score


def whole_scan(np, source, key, quad, permutation, work, name):
    fs = list(frames(source))
    framefile = work/(name+'.in')
    framefile.write_text('25\n'+' '.join(map(str, key['column_rank_order']))+'\n'+
                         ''.join(f'{ab[0]} {ab[1]} {wire}\n' for ab, wire, _ in fs))
    proc = subprocess.run([str(work/'order_scan'), str(work/'quad49.bin'),
                           str(framefile)], text=True, capture_output=True, check=True)
    result = json.loads(proc.stdout)
    assert result['evaluations'] == 225250
    candidates = []
    for fi, kind, a, b in result['ops']:
        ab, frame, owners = fs[fi]
        wire = move_groups(frame, kind, a, b)
        moved = move_groups(owners, kind, a, b)
        verify_owners(source, wire, moved)
        raw, score = evaluate(np, wire, key, quad, permutation)
        assert abs(score-result['best_score']) < 1e-7
        candidates.append(dict(boundaries=ab, operation=[kind, a, b], raw=raw, score=score))
    return {**result, 'candidates': candidates}


def coordinate_scan(np, source, key, quad, permutation):
    rows = []
    for a in range(155, 160):
        for b in range(184, 189):
            for destination in range(388):
                wire, owners = coordinate_model(source, a, b, destination)
                raw, score = evaluate(np, wire, key, quad, permutation)
                rows.append(dict(a=a, b=b, destination=destination, score=score, raw=raw))
    rows.sort(key=lambda row: row['score'], reverse=True)
    top = rows[0]
    wire, owners = coordinate_model(source, top['a'], top['b'], top['destination'])
    verify_owners(source, wire, owners)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad26', required=True, type=Path)
    parser.add_argument('--output', type=Path, help='Optional compact JSON report')
    parser.add_argument('--compiler', default='cc')
    parser.add_argument('--scope', choices=['all', 'whole', 'coordinate'], default='all')
    args = parser.parse_args()
    for var in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
        os.environ[var] = '1'
    import numpy as np
    prov = json.loads((HERE/'search_provenance.json').read_text())
    key, source = load_inputs(prov)
    quad, mixture_hash = build_model(np, args.quad26, key, prov)
    ranks = key['column_rank_order']
    permutation = np.array([p for col in sorted(range(22), key=lambda c:ranks[c])
                            for p in range(col, 392, 22)], dtype=np.int32)
    report = dict(schema='adfgvx-p215-discovery-replay-v1', mixture_sha256=mixture_hash,
                  joint49_sha256=prov['joint49_sha256'], controls={}, historical={})
    with tempfile.TemporaryDirectory(prefix='adfgvx-p215-') as directory:
        work = Path(directory)
        quad.tofile(work/'quad49.bin')
        if args.scope in ('all', 'whole'):
            subprocess.run([args.compiler, '-O3', '-std=c99', str(HERE/'order_scan.c'),
                            '-lm', '-o', str(work/'order_scan')], check=True)
            for item in prov['whole_controls']:
                result = whole_scan(np, item['source_masked'], key, quad, permutation,
                                    work, item['name'])
                assert len(result['candidates']) == 1
                assert result['candidates'][0]['raw'] == item['expected_raw']
                assert abs(result['best_score']-item['score']) < 1e-7
                report['controls'][item['name']] = dict(evaluations=result['evaluations'],
                    correct_fixed_positions=196-item['expected_raw'].count('?'), recovered=True)
            result = whole_scan(np, source, key, quad, permutation, work, 'historical')
            assert result['ops'] == prov['whole_historical']['ops']
            assert abs(result['best_score']-prov['whole_historical']['best_score']) < 1e-7
            report['historical']['whole'] = result
        if args.scope in ('all', 'coordinate'):
            mask_indices = {i for i, c in enumerate(source) if c == '?'}
            for item in prov['coordinate_controls']:
                text = item['plaintext']
                iv = ''.join(CO[key['square'].index(c)//6]+CO[key['square'].index(c)%6]
                             for c in text)
                full = ''.join(iv[p] for p in permutation)
                _, owners = coordinate_model(source, *item['parameters'])
                observed = ['?']*390
                for j, owner in enumerate(owners):
                    if owner is not None and owner not in mask_indices:
                        observed[owner] = full[j]
                observed = ''.join(observed)
                assert observed.count('?') == 18
                assert hashlib.sha256(observed.encode()).hexdigest() == item['source_sha256']
                rows = coordinate_scan(np, observed, key, quad, permutation)
                top = rows[0]
                assert [top['a'], top['b'], top['destination']] == item['parameters']
                assert top['raw'] == item['expected_raw']
                assert abs(top['score']-item['truth_score']) < 1e-7
                report['controls'][item['name']] = dict(models=len(rows), truth_rank=1,
                    correct_fixed_positions=196-top['raw'].count('?'), recovered=True)
            rows = coordinate_scan(np, source, key, quad, permutation)
            selected = []
            for expected in prov['coordinate_historical']['reported_models']:
                row = next(row for row in rows if [row['a'], row['b'], row['destination']]
                           == expected['parameters'])
                assert row['raw'] == expected['raw']
                assert abs(row['score']-expected['score']) < 1e-7
                selected.append({**row, 'rank': rows.index(row)+1, 'selection': expected['selection']})
            report['historical']['coordinate'] = dict(models=len(rows), best=rows[0],
                                                       reported_models=selected)
    report['limits'] = prov['limits']
    rendered = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
