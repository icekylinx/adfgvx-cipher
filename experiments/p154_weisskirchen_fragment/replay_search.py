#!/usr/bin/env python3
"""Replay the bounded p154 A2 surplus-glyph and missing-prefix search.

Requires NumPy and the pinned external quad26 file; writes no binary model.
icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = 'ADFGVX'
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad26',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
        os.environ[name] = '1'
    import numpy as np
    prov = json.loads((HERE/'search_provenance.json').read_text())
    for path,value in prov['pinned_repository_files'].items():
        assert digest(ROOT/path) == value, path
    path = ROOT/'experiments/p212_medical_fragment/replay_search.py'
    spec = importlib.util.spec_from_file_location('p212_probability_recipe',path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    recipe = json.loads(path.with_name('search_provenance.json').read_text())
    _,dataset,_,_ = old.load_pinned_inputs(recipe)
    probability,probability_sha = old.rebuild_probabilities(np,args.quad26,dataset,recipe)
    assert probability_sha == prov['probability_sha256']
    data = json.loads((HERE/'inputs.json').read_text())
    key = data['key']
    source = ''.join(''.join(data['records'][0]['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == prov['literal_source_sha256']
    masks = np.zeros((49,36))
    for pattern in range(49):
        a,b = divmod(pattern,7)
        for cell in range(36):
            if (a == 6 or cell//6 == a) and (b == 6 or cell%6 == b):
                masks[pattern,AL.index(key['square'][cell])] = 1.
    joint = probability.copy()
    for axis in range(4):
        joint = np.moveaxis(np.tensordot(masks,joint,axes=(1,axis)),0,axis)
    quad = np.log(joint).astype('<f4')
    assert hashlib.sha256(quad.tobytes()).hexdigest() == prov['joint49_sha256']
    ranks = key['column_rank_order']
    def inverse(n):
        return np.argsort([i for c in sorted(range(len(ranks)),key=lambda c:ranks[c]) for i in range(c,n,len(ranks))])
    def encode(text):
        mid = ''.join(CO[key['square'].index(c)//6]+CO[key['square'].index(c)%6] for c in text)
        return ''.join(mid[c::len(ranks)] for c in sorted(range(len(ranks)),key=lambda c:ranks[c]))
    def evaluate(wires):
        vals = np.array([[CO.index(c) if c in CO else 6 for c in s] for s in wires],dtype=np.int16)
        mid = vals[:,inverse(len(wires[0]))]
        patterns = mid[:,::2]*7+mid[:,1::2]
        scores = quad[patterns[:,:-3],patterns[:,1:-2],patterns[:,2:-1],patterns[:,3:]].sum(1,dtype=np.float64)
        return scores,mid
    def raw(mid):
        return ''.join('?' if a == 6 or b == 6 else key['square'][6*a+b] for a,b in zip(mid[::2],mid[1::2]))
    def primary_scan(s):
        wires,metadata = [],[]
        for excluded in range(25,31):
            shortened = s[:excluded]+s[excluded+1:]
            for boundary in range(118):
                wires.append(shortened[:boundary]+'?'*45+shortened[boundary:])
                metadata.append((excluded,boundary))
        scores,mid = evaluate(wires)
        best = float(scores.max())
        winners = []
        for i in np.flatnonzero(abs(scores-best) < 1e-8):
            excluded,boundary = metadata[int(i)]
            origins = [j for j in range(118) if j != excluded]
            origins[boundary:boundary] = [None]*45
            assert len(origins) == 162
            assert ''.join('?' if j is None else s[j] for j in origins) == wires[i]
            full_mid = ['A' if x == 6 else CO[int(x)] for x in mid[i]]
            plaintext = ''.join(key['square'][6*CO.index(a)+CO.index(b)] for a,b in zip(full_mid[::2],full_mid[1::2]))
            assert encode(plaintext) == wires[i].replace('?','A')
            text = raw(mid[i])
            winners.append(dict(excluded_source=excluded,gap_before_shortened_boundary=boundary,
                                raw=text,fixed=len(text)-text.count('?'),score=float(scores[i])))
        return scores,winners
    scores,winners = primary_scan(source)
    assert abs(float(scores.max())-prov['primary_scope']['best'][0]['score']) < 1e-6
    assert {(r['excluded_source'],r['gap_before_shortened_boundary'],r['raw']) for r in winners} == {
        (r['excluded_source'],r['gap_before_shortened_boundary'],r['raw']) for r in prov['primary_scope']['best']}
    controls = []
    for control in prov['controls']:
        full = encode(control['plaintext'])
        a = control['true_gap_at']
        shortened = full[:a]+full[a+45:]
        synthetic = shortened[:28]+'D'+shortened[28:]
        assert synthetic == control['source']
        sc,ws = primary_scan(synthetic)
        index = 3*118+a
        rank = 1+int(np.sum(sc > sc[index]+1e-8))
        assert rank == control['true_rank']
        correct = all(all(c == '?' or c == control['plaintext'][i] for i,c in enumerate(w['raw'])) for w in ws)
        assert correct == control['all_best_fixed_correct']
        controls.append(dict(id=control['id'],true_rank=rank,all_best_fixed_correct=correct))
    rng = random.Random(prov['frequency_preserving_null']['seed'])
    null = []
    for _ in range(40):
        shuffled = list(source)
        rng.shuffle(shuffled)
        ns,_ = primary_scan(''.join(shuffled))
        null.append(float(ns.max()))
    assert all(abs(x-y) < 1e-6 for x,y in zip(null,prov['frequency_preserving_null']['scores']))
    lengths = []
    for n in range(118,301,2):
        for excluded in range(25,31):
            shortened = source[:excluded]+source[excluded+1:]
            sc,_ = evaluate(['?'*(n-117)+shortened])
            lengths.append((float(sc[0]),n,excluded))
    lengths.sort(reverse=True)
    assert len(lengths) == 552 and all(n == 162 for _,n,_ in lengths[:6])
    split_best = -float('inf')
    count = 0
    for excluded in range(25,31):
        shortened = source[:excluded]+source[excluded+1:]
        for prefix in range(46):
            wires = ['?'*prefix+shortened[:a]+'?'*(45-prefix)+shortened[a:] for a in range(118)]
            sc,_ = evaluate(wires)
            count += len(wires)
            split_best = max(split_best,float(sc.max()))
    assert count == 32568
    assert abs(split_best-prov['prefix_plus_second_gap_diagnostic']['best']['score']) < 1e-6
    result = dict(verified=True,primary_models=708,primary_best=winners,controls=controls,
                  shuffle_maximum=max(null),shuffles_at_least_historical=int(sum(x >= scores.max() for x in null)),
                  length_models=552,top_lengths=lengths[:6],prefix_split_models=count,
                  prefix_split_best=split_best,limits=prov['limits'])
    text = json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')


if __name__ == '__main__':
    main()
