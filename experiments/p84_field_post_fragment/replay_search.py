#!/usr/bin/env python3
"""Replay p84 half-coordinate phrase retrieval and optional length diagnostic.

Requires NumPy. No model binary is committed. icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import random
import sys

for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[variable] = '1'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import encrypt, decrypt, transposition_indices
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
C = 'ADFGVX?'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frames(source, totals=(244,), include_native=False):
    result = []
    for total in totals:
        for at in ([-1] if include_native else []) + list(range(75,80)):
            owners = list(range(len(source)))
            if at >= 0:
                owners.insert(at,None)
            if len(owners) > total:
                continue
            owners += [None]*(total-len(owners))
            wire = ''.join(source[i] if i is not None else '?' for i in owners)
            result.append(dict(total=total,insert_before_source=at,owners=owners,wire=wire))
    return result


def inverse(np,total,ranks):
    return np.argsort(transposition_indices(total,ranks))


def read_donors():
    manifest = load(HERE/'donor_manifest.json')
    cache = {}
    texts = []
    for entry in manifest['streams']:
        path = entry['path']
        if path not in cache:
            cache[path] = load(ROOT/path)
        value = cache[path]
        for component in entry['json_path']:
            value = value[component]
        assert isinstance(value,str)
        assert hashlib.sha256(value.encode()).hexdigest() == entry['text_sha256'], path
        texts.append(value)
    assert len(texts) == 331 and len(set(texts)) == 331
    return texts


def phrase_engine(np,texts,key):
    donor = '?'.join(texts)
    values = np.array([A.index(c) if c in A else 36 for c in donor],dtype=np.int16)
    allowed = np.zeros((49,37),dtype=bool)
    for pattern in range(49):
        r,c = divmod(pattern,7)
        for cell,ch in enumerate(key['square']):
            if (r == 6 or r == cell//6) and (c == 6 or c == cell%6):
                allowed[pattern,A.index(ch)] = True
    inv = inverse(np,244,key['column_rank_order'])
    def search(wire):
        mid = np.array([C.index(c) for c in wire],dtype=np.int8)[inv]
        patterns = 7*mid[::2]+mid[1::2]
        support = (mid[::2]<6).astype(int)+(mid[1::2]<6).astype(int)
        cumulative = np.r_[0,support.cumsum()]
        run = np.zeros(len(values),dtype=np.int16)
        best = (0,0)
        hits = []
        qualifying = set()
        for i,pattern in enumerate(patterns):
            run = np.r_[0,run[:-1]]+1
            run[~allowed[pattern,values]] = 0
            indices = np.flatnonzero(run >= 12)
            if not len(indices):
                continue
            supports = cumulative[i+1]-cumulative[i+1-run[indices]]
            for j,observations in zip(indices,supports):
                length = int(run[j]); observed = int(observations)
                if observed >= 12:
                    qualifying.add(donor[j+1-length:j+1])
                rank = (observed,length)
                row = dict(target_start=i+1-length,target_stop=i+1,
                           donor_concat_start=int(j+1-length),text=donor[j+1-length:j+1])
                if rank > best:
                    best,hits = rank,[row]
                elif rank == best:
                    hits.append(row)
        return dict(maximum_observed_support=best[0],matched_length=best[1],
                    best_hits=hits,qualifying_texts=sorted(qualifying))
    return search


def phrase_replay(np,source,key,texts):
    search = phrase_engine(np,texts,key)
    historical = [dict(insert_before_source=f['insert_before_source'],**search(f['wire'])) for f in frames(source)]
    for row in historical:
        assert row['maximum_observed_support'] == 15 and row['matched_length'] == 17
        assert row['best_hits'][0]['text'] == 'XDEUTSCLEFELDPOST'
        assert row['best_hits'][0]['target_start'] == 46
    rng = random.Random(2026110484001)
    observed = [c for c in source if c != '?']
    null = []
    for index in range(100):
        rng.shuffle(observed)
        it = iter(observed)
        shuffled = ''.join(next(it) if c != '?' else '?' for c in source)
        rows = [search(f['wire']) for f in frames(shuffled)]
        best = max(rows,key=lambda r:(r['maximum_observed_support'],r['matched_length']))
        null.append(dict(control=index,maximum_observed_support=best['maximum_observed_support'],matched_length=best['matched_length']))
    assert max(x['maximum_observed_support'] for x in null) == 11
    controls = []
    random_letters = random.Random(2026110484002)
    for index,(phrase,at) in enumerate([('VERBINDUNGMITXUKSX',76),('DIESTELLUNGENEINTE',78)]):
        assert any(phrase in t for t in texts)
        plaintext = [random_letters.choice(A) for _ in range(122)]
        plaintext[47:47+len(phrase)] = phrase
        plaintext = ''.join(plaintext)
        full = encrypt(plaintext,key['column_rank_order'],key['square'])
        frame = next(f for f in frames(source) if f['insert_before_source'] == at)
        generated = list(source)
        for i,origin in enumerate(frame['owners']):
            if origin is not None and source[origin] != '?':
                generated[origin] = full[i]
        generated = ''.join(generated)
        rows = [dict(insert_before_source=f['insert_before_source'],**search(f['wire'])) for f in frames(generated)]
        planted = next(r for r in rows if r['insert_before_source'] == at)
        assert any(phrase in h['text'] and h['target_start'] <= 47 and h['target_stop'] >= 47+len(phrase)
                   for h in planted['best_hits'])
        controls.append(dict(control=index,phrase=phrase,plaintext_start=47,
                             source=generated,plaintext=plaintext,planted_insert=at,results=rows))
    return dict(historical=historical,shuffle_controls=null,fresh_phrase_controls=controls)


def coordinate_model(np,probability,square):
    masks = np.zeros((49,36))
    for pattern in range(49):
        r,c = divmod(pattern,7)
        for cell,ch in enumerate(square):
            if (r == 6 or r == cell//6) and (c == 6 or c == cell%6):
                masks[pattern,A.index(ch)] = 1.
    joint = probability.copy()
    for axis in range(4):
        joint = np.moveaxis(np.tensordot(masks,joint,axes=(1,axis)),0,axis)
    return np.log(joint).astype('<f4')


def length_scan(np,source,key,quad):
    results = []
    for frame in frames(source,range(118,501,2),True):
        mid = np.array([C.index(c) for c in frame['wire']],dtype=np.int8)[inverse(np,frame['total'],key['column_rank_order'])]
        pat = 7*mid[::2]+mid[1::2]
        score = quad[pat[:-3],pat[1:-2],pat[2:-1],pat[3:]].sum(dtype=np.float64)
        support = (mid[::2]<6).astype(int)+(mid[1::2]<6).astype(int)
        denominator = sum(support[j:j+len(support)-3].sum() for j in range(4))
        raw = decrypt(frame['wire'],key['column_rank_order'],key['square'])
        results.append(dict(total=frame['total'],insert_before_source=frame['insert_before_source'],
                            score=float(score/denominator),raw=raw,fixed_positions=len(raw)-raw.count('?')))
    results.sort(key=lambda r:r['score'],reverse=True)
    return results


def length_replay(np,source,quad26):
    path = ROOT/'experiments/p212_medical_fragment/replay_search.py'
    spec = importlib.util.spec_from_file_location('p212_replay',path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    provenance = load(path.parent/'search_provenance.json')
    _,dataset,keys,_ = module.load_pinned_inputs(provenance)
    probability,digest = module.rebuild_probabilities(np,quad26,dataset,provenance)
    leaders,controls = [],[]
    for key in [k for k in keys if '?' not in k['square']]:
        quad = coordinate_model(np,probability,key['square'])
        rows = length_scan(np,source,key,quad)
        leaders.append(dict(key=key['id'],**rows[0]))
        if key['id'] not in ['Oct28-31','Nov1-3']:
            continue
        examples = [(244,77,'DIELEITUNGZURFUNKSTELLEISTUNTERBROCHENXALLESTATIONENWERDENGEBETENDIELETZTENMELDUNGENNOCHMALSDURCHZUGEBENXDERBETRIEBWIRDAMMORGENWIEDERAUFGENOMMENX'),
                    (202,-1,'NACHBEENDIGUNGDERARBEITENWIRDDIEVERBINDUNGWIEDERHERGESTELLTXDIEPOSTENANDERBRUECKEBLEIBENBISZURABLOESUNGAMORTX')]
        for index,(total,at,text) in enumerate(examples):
            plaintext = (text*2)[:total//2]
            full = encrypt(plaintext,key['column_rank_order'],key['square'])
            frame = next(f for f in frames(source,[total],True) if f['insert_before_source'] == at)
            generated = list(source)
            for i,origin in enumerate(frame['owners']):
                if origin is not None and source[origin] != '?':
                    generated[origin] = full[i]
            rows = length_scan(np,''.join(generated),key,quad)
            rank = next(i+1 for i,r in enumerate(rows) if (r['total'],r['insert_before_source']) == (total,at))
            best = rows[0]
            correct = sum(c != '?' and i < len(plaintext) and c == plaintext[i] for i,c in enumerate(best['raw']))
            controls.append(dict(key=key['id'],control=index,truth_length=total,truth_insert=at,
                                 truth_rank=rank,best_fixed=best['fixed_positions'],best_correct_fixed=correct))
    leaders.sort(key=lambda r:r['score'],reverse=True)
    assert (leaders[0]['key'],leaders[0]['total'],leaders[0]['insert_before_source']) == ('Oct28-31',244,76)
    expected = load(HERE/'search_provenance.json')['length_diagnostic']['controls']
    assert controls == expected
    return dict(models=12617,model_sha256=digest,key_leaders=leaders,controls=controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad26',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    import numpy as np
    inputs = load(HERE/'inputs.json')
    source = ''.join(''.join(inputs['records'][0]['source_rows']).split()).replace('-','?')
    texts = read_donors()
    result = dict(schema='adfgvx-p84-discovery-replay-v1',input_sha256=sha(HERE/'inputs.json'),
                  donor_manifest_sha256=sha(HERE/'donor_manifest.json'),
                  phrase_search=phrase_replay(np,source,inputs['key'],texts))
    if args.quad26:
        result['length_diagnostic'] = length_replay(np,source,args.quad26)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(verified=True,donor_streams=len(texts),source_frames=5,
                         shuffled_sources=100,fresh_phrase_controls=2,
                         length_diagnostic_replayed=bool(args.quad26)),indent=2))


if __name__ == '__main__':
    main()
