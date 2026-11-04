#!/usr/bin/env python3
"""Replay the bounded, retrospective repeated-digraph-collapse retrieval.

icekylinx and GPT-6 Astra Pro. Requires NumPy. No language model is used.
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
from adfgvx.cipher import encrypt, untranspose

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
C = 'ADFGVX?'


def load(path):
    return json.loads(path.read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def native_streams(inp):
    """Exclude an entire text entry if any alias identifies this same message."""
    cache = {}; streams = []; excluded = []
    for entry in load(ROOT / inp['retrieval']['manifest'])['streams']:
        if any(ref['path'] == inp['retrieval']['excluded_same_message_input']
               for ref in entry['sources']):
            excluded.append(entry['text_sha256'])
            continue
        texts = []
        for ref in entry['sources']:
            path = ref['path']
            if path not in cache:
                cache[path] = load(ROOT / path)
            value = cache[path]
            for part in ref['json_path']:
                value = value[part]
            assert hashlib.sha256(value.encode()).hexdigest() == entry['text_sha256']
            texts.append(value)
        assert len(set(texts)) == 1
        streams.append(dict(**entry, text=texts[0]))
    assert len(streams) == 484 and sum(len(s['text']) for s in streams) == 51327
    assert len(excluded) == 4
    return streams, excluded


def collapsed_streams(streams):
    result = []
    for stream_id, stream in enumerate(streams):
        text = stream['text']
        for start in range(len(text) - 3):
            block = text[start:start + 2]
            if '?' not in block and block == text[start + 2:start + 4]:
                result.append(dict(stream_id=stream_id, source_sha256=stream['text_sha256'],
                                   source_refs=stream['sources'], start=start, block=block,
                                   text=text[:start + 2] + text[start + 4:], join=start + 2))
    assert len(result) == 110
    return result


def engine(variants, key, interval, minimum_length):
    corpus = '?'.join(x['text'] for x in variants)
    owners = np.full(len(corpus), -1, dtype=np.int32)
    joins = np.full(len(corpus), -1, dtype=np.int32)
    offset = 0
    for i, variant in enumerate(variants):
        owners[offset:offset + len(variant['text'])] = i
        joins[offset:offset + len(variant['text'])] = offset + variant['join']
        variant['corpus_offset'] = offset
        offset += len(variant['text']) + 1
    vals = np.array([A.index(c) if c in A else 36 for c in corpus], dtype=np.int16)
    ends = np.arange(len(vals))
    allowed = np.zeros((49, 37), dtype=bool)
    for pattern in range(49):
        row, col = divmod(pattern, 7)
        for cell, label in enumerate(key['square']):
            if (row == 6 or row == cell // 6) and (col == 6 or col == cell % 6):
                allowed[pattern, A.index(label)] = True

    def search(wire):
        middle = np.array([C.index(c) for c in untranspose(wire, key['column_rank_order'])], dtype=np.int8)
        patterns = 7 * middle[::2] + middle[1::2]
        support = (middle[::2] < 6).astype(int) + (middle[1::2] < 6).astype(int)
        cumulative = np.r_[0, support.cumsum()]
        run = np.zeros(len(vals), dtype=np.int16)
        rank = (0, 0); hits = []
        for target_end in range(*interval):
            run = np.r_[0, run[:-1]] + 1
            run[~allowed[patterns[target_end], vals]] = 0
            starts = ends + 1 - run
            # A hit must include the surviving digraph and a character after
            # its join. Untouched distant substrings are not collapse evidence.
            matches = np.flatnonzero((run >= minimum_length) &
                                     (starts <= joins - 2) & (ends >= joins))
            for donor_end in matches:
                length = int(run[donor_end])
                start = target_end + 1 - length
                observed = int(cumulative[target_end + 1] - cumulative[start])
                current = (observed, length)
                if current > rank:
                    rank = current; hits = []
                if current == rank:
                    owner = int(owners[donor_end]); variant = variants[owner]
                    hits.append(dict(target_start=start,
                                     text=corpus[donor_end + 1 - length:donor_end + 1],
                                     variant=owner,
                                     donor_start=int(donor_end + 1 - length - variant['corpus_offset']),
                                     collapsed_block=variant['block'], collapse_start=variant['start']))
        return dict(observed_support=rank[0], length=rank[1], hits=hits)
    return search, len(corpus)


def compute():
    inp = load(HERE / 'inputs.json'); spec = inp['retrieval']
    assert spec == dict(manifest='experiments/p164_occupation_fragment/donor_manifest.json',
                        excluded_same_message_input='experiments/black_sea_evacuation_routes/inputs.json',
                        target_plaintext_interval=[127, 144], minimum_length=10,
                        repeated_block_length=2, require_hit_to_cross_collapse=True,
                        shuffle_samples=128, shuffle_seed=20261104060289,
                        planted_seed=20261104060290, planted_variant_indices=[65, 87, 101],
                        planted_target_start=128, retrospective=True)
    streams, excluded = native_streams(inp)
    variants = collapsed_streams(streams)
    key = inp['key']; record = inp['records'][0]
    literal = ''.join(''.join(record['source_rows']).split())
    wire = literal[:200].replace('-', '?') + '?' * 100 + literal[200:].replace('-', '?')
    search, corpus_characters = engine(variants, key, spec['target_plaintext_interval'], spec['minimum_length'])
    historical = search(wire)
    assert historical == dict(observed_support=16, length=12,
                             hits=[dict(target_start=131, text='NDIENSTELLEN', variant=81,
                                        donor_start=20, collapsed_block='ST', collapse_start=25)])
    rng = random.Random(spec['shuffle_seed']); observed = [c for c in wire if c != '?']; null = []
    for _ in range(spec['shuffle_samples']):
        rng.shuffle(observed); it = iter(observed)
        shuffled = ''.join(next(it) if c != '?' else '?' for c in wire)
        null.append(search(shuffled))
    summary = dict(count=len(null), matched_at_minimum_length=sum(r['length'] >= 10 for r in null),
                   at_or_above_target=sum((r['observed_support'], r['length']) >= (16, 12) for r in null),
                   maximum_rank=list(max((r['observed_support'], r['length']) for r in null)),
                   results_sha256=digest(null))
    planted = []; rng = random.Random(spec['planted_seed'])
    for variant_id in spec['planted_variant_indices']:
        variant = variants[variant_id]; start = variant['join'] - 8
        fragment = variant['text'][start:start + 16]
        assert len(fragment) == 16 and '?' not in fragment
        truth = [rng.choice(A) for _ in range(179)]
        truth[128:144] = fragment; truth = ''.join(truth)
        full = encrypt(truth, key['column_rank_order'], key['square'])
        masked = ''.join(c if m != '?' else '?' for c, m in zip(full, wire))
        result = search(masked)
        assert any(h['target_start'] <= 128 and
                   h['text'][128 - h['target_start']:144 - h['target_start']] == fragment
                   for h in result['hits'])
        planted.append(dict(variant=variant_id, fragment=fragment, target_start=128,
                            plaintext=truth, source=masked, result=result))
    manifest = [{k: v for k, v in r.items() if k != 'corpus_offset'} for r in variants]
    donor = variants[81]
    assert donor['source_refs'] == [dict(path='experiments/premium_payment_stop/inputs.json',
                                       json_path=['records', 1, 'expected_raw'])]
    return dict(schema='adfgvx-p89-repeated-digraph-collapse-search-v1', authors=inp['authors'],
                scope=spec, donor_streams=len(streams), donor_characters=sum(len(s['text']) for s in streams),
                excluded_same_message_text_hashes=excluded, collapsed_variants=len(variants),
                collapsed_corpus_characters=corpus_characters, variant_manifest_sha256=digest(manifest),
                historical=historical,
                historical_donor={k: v for k, v in donor.items() if k not in ['text', 'corpus_offset']},
                null_summary=summary, planted=planted,
                limits=[
                    'This is a retrospective test of one proposed spelling operation, not an unconditioned decipherment search.',
                    'The wholly absent initial N of the longest donor match is not accepted. The proposed word is DIENSTELLEN at positions 132–142.',
                    'Every same-message manifest entry is excluded even when another path aliases that entry. The existing part 2 is absent from this frozen native-stream manifest.',
                    'The shuffle controls preserve all mask positions and the observed-coordinate histogram, and repeat this entire bounded retrieval.',
                    'Planted fragments test recovery in the same geometry. They are constructed controls, not additional historical witnesses.',
                    'No control frequency is interpreted as a probability that the proposed historical spelling is correct.'
                ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args(); result = compute()
    path = HERE / 'search_report.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == load(path)
    print(json.dumps(dict(verified=True, donor_streams=result['donor_streams'],
                          collapsed_variants=result['collapsed_variants'], historical=result['historical'],
                          null_summary=result['null_summary'], planted_controls=len(result['planted'])), indent=2))


if __name__ == '__main__':
    main()
