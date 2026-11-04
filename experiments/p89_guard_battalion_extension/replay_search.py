#!/usr/bin/env python3
"""Replay the frozen raw-word search over p89 A3's previously unread tail.

Requires NumPy. The null controls preserve every erasure location and the
observed-coordinate histogram. They do not estimate historical correctness.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import random
import sys
for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt
from verify import inverse, load, record

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
C = 'ADFGVX?'
MANIFEST = 'experiments/p164_occupation_fragment/donor_manifest.json'
EXCLUDED = 'experiments/black_sea_evacuation_routes/inputs.json'


def donors():
    cache = {}; texts = []
    for entry in load(ROOT/MANIFEST)['streams']:
        refs = [r for r in entry['sources'] if r['path'] != EXCLUDED]
        if not refs:
            continue
        matches = []
        for ref in refs:
            path = ref['path']
            if path not in cache:
                cache[path] = load(ROOT/path)
            value = cache[path]
            for part in ref['json_path']:
                value = value[part]
            assert hashlib.sha256(value.encode()).hexdigest() == entry['text_sha256']
            matches.append(value)
        assert len(set(matches)) == 1
        texts.append(matches[0])
    assert len(texts) == len(set(texts)) == 485
    assert sum(map(len, texts)) == 51526
    return texts


def engine(texts, key, n):
    corpus = '?'.join(texts)
    vals = np.array([A.index(c) if c in A else 36 for c in corpus], dtype=np.int16)
    iv = np.array(inverse(n, key['column_rank_order']))
    allowed = np.zeros((49, 37), dtype=bool)
    for pat in range(49):
        row, col = divmod(pat, 7)
        for cell, ch in enumerate(key['square']):
            if (row == 6 or row == cell//6) and (col == 6 or col == cell % 6):
                allowed[pat, A.index(ch)] = True
    def best(wire):
        middle = np.array([C.index(c) for c in wire], dtype=np.int8)[iv]
        patterns = 7*middle[::2] + middle[1::2]
        support = (middle[::2] < 6).astype(int) + (middle[1::2] < 6).astype(int)
        cumulative = np.r_[0, support.cumsum()]
        run = np.zeros(len(vals), dtype=np.int16)
        rank = (0, 0); hits = []
        for i in range(127, len(patterns)):
            run = np.r_[0, run[:-1]] + 1
            run[~allowed[patterns[i], vals]] = 0
            for j in np.flatnonzero(run >= 12):
                length = int(run[j]); start = i+1-length
                observed = int(cumulative[i+1]-cumulative[start])
                if observed < 12:
                    continue
                current = (observed, length)
                if current > rank:
                    rank = current; hits = []
                if current == rank:
                    hits.append([start, corpus[j+1-length:j+1]])
        return dict(observed_support=rank[0], length=rank[1], hits=sorted(set(tuple(x) for x in hits)))
    return best


def compute():
    inp = load(HERE/'inputs.json')
    data = load(ROOT/inp['target']['input_path'])
    cert = load(ROOT/inp['target']['certificate_path'])
    source = record(cert, 'p89_A3')['ciphertext']; key = data['key']
    texts = donors(); search = engine(texts, key, len(source))
    historical = search(source)
    assert historical['observed_support'] == 27 and historical['length'] == 20
    assert historical['hits'] == [(144, 'ERSXBATLX2XGARDEREGT')]
    seed = 20261104030689
    rng = random.Random(seed); observed = [c for c in source if c != '?']; null = []
    for i in range(500):
        rng.shuffle(observed); it = iter(observed)
        shuffled = ''.join(next(it) if c != '?' else '?' for c in source)
        null.append(dict(id=i, **search(shuffled)))
    null_summary = dict(count=500, minimum_matched_length=12,
                        hits_at_minimum_length=sum(x['length'] >= 12 for x in null),
                        maximum_observed_support=max(x['observed_support'] for x in null),
                        at_or_above_historical_support=sum(x['observed_support'] >= 27 for x in null),
                        result_sha256=hashlib.sha256(json.dumps(null, sort_keys=True, separators=(',', ':')).encode()).hexdigest())
    rng = random.Random(seed+1); controls = []
    for word in ['OBERKOMMANDO', 'MITTELMEERDIVISION', 'WAFFENSTILLSTAND', 'KONSTANTINOPEL']:
        assert any(word in text for text in texts)
        truth = [rng.choice(A) for _ in range(179)]
        truth[144:144+len(word)] = word; truth = ''.join(truth)
        full = encrypt(truth, key['column_rank_order'], key['square'])
        masked = ''.join(a if b != '?' else '?' for a, b in zip(full, source))
        result = search(masked)
        assert any(start <= 144 and text[144-start:144-start+len(word)] == word
                   for start, text in result['hits'])
        controls.append(dict(word=word, offset=144, plaintext=truth, source=masked, result=result))
    return dict(schema='adfgvx-p89-guard-battalion-search-v1', manifest=MANIFEST,
                excluded_same_message_inputs=EXCLUDED, donor_streams=len(texts), donor_characters=sum(map(len, texts)),
                target_plaintext_interval=[127, 179], minimum_length=12, seed=seed,
                historical=historical, null_summary=null_summary, planted=controls,
                limits=['The twenty-character phrase is the frozen zero-substitution retrieval result.',
                        'The shorter BERLIN proposal is subsequent contextual work, outside this twelve-character retrieval threshold.',
                        'Coordinate shuffles calibrate this declared retrieval only; they do not prove unique wording or a null probability.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = json.loads(json.dumps(compute()))
    path = HERE/'search_report.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == load(path)
    print(json.dumps(dict(verified=True, historical=result['historical'],
                          null_summary=result['null_summary'],
                          planted=[dict(word=c['word'], result=c['result']) for c in result['planted']]), indent=2))


if __name__ == '__main__':
    main()
