#!/usr/bin/env python3
"""Replay p137 exact-domain lexical diagnostics with the hash-pinned model.

The full replay optimizes 13 families of 264 lengths. --best-only replays
one retained winner per family and is not a substitute for that full scan.
icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import plaintext_domains
from experiments.p137_publicity_fragment.verify import build, checked

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lexicon', type=Path, required=True)
    parser.add_argument('--best-only', action='store_true')
    parser.add_argument('--family', help='Replay one exact family ID from discovery.json.')
    args = parser.parse_args()
    # Check source identity, shuffle generation, keys and frozen snapshot structure first.
    build()
    frozen = json.loads((HERE/'discovery.json').read_text())
    assert hashlib.sha256(args.lexicon.read_bytes()).hexdigest() == frozen['lexicon']['sha256']
    solver = checked(frozen['solver'])
    families = frozen['families']
    if args.family:
        families = [f for f in families if f['id'] == args.family]
        if not families:
            parser.error('Unknown family: '+args.family)
    replayed = 0
    reports = []
    with tempfile.TemporaryDirectory(prefix='adfgvx-p137-discovery-') as temp:
        work = Path(temp); binary = work/'domain_words'
        subprocess.run(['g++','-O3','-std=c++17','-o',str(binary),str(solver)],check=True)
        for family in families:
            chosen = family['scores_by_length']
            if args.best_only:
                chosen = [row for row in chosen if row[0] == family['best_length']]
            lines = []
            for n, _ in chosen:
                wire = '?'*(n-74)+family['source_literal'].replace('-', '?')
                domains = plaintext_domains(wire, family['ranks'], family['square'])
                masks = [sum(1 << A.index(c) for c in d) for d in domains]
                lines.append(f'{n} {len(masks)} '+' '.join(map(str,masks)))
            frames = work/'frames.txt'; output = work/'results.jsonl'
            frames.write_text('\n'.join(lines)+'\n')
            p = frozen['parameters']
            with output.open('w') as stream:
                subprocess.run([str(binary),str(args.lexicon.resolve()),str(frames),
                    str(p['fallback_score']),str(p['bigram_weight']),str(p['separator_X_score'])],
                    stdout=stream,check=True)
            actual = [json.loads(line) for line in output.read_text().splitlines()]
            assert len(actual) == len(chosen)
            assert [int(r['id']) for r in actual] == [n for n, _ in chosen]
            for row, (n, score) in zip(actual, chosen):
                assert row['feasible'] and row['length'] == n//2
                assert abs(row['score']-score) < 1e-8, (family['id'],n,row['score'],score)
                if n == family['best_length']:
                    assert row['plaintext'] == family['diagnostic_best_plaintext']
                    assert row['segmented'] == family['diagnostic_best_segmentation']
            winner = max(actual,key=lambda r:r['score'])
            assert int(winner['id']) == family['best_length']
            replayed += len(actual)
            report = {'family':family['id'],'frames_replayed':len(actual),
                      'best_length':int(winner['id']),'best_score':winner['score']}
            reports.append(report)
            print(json.dumps(report),flush=True)
    print(json.dumps({'families_replayed':len(reports),'frames_replayed':replayed,
        'full_family_optimization_replayed':not args.best_only,
        'accepted_full_language_model_completions':0,
        'limit':'Exact within the pinned model; no historical uniqueness probability. The fresh authored positive recovers only 54 of 127 labels.'},indent=2))


if __name__ == '__main__':
    main()
