#!/usr/bin/env python3
"""Run source-preserving, anchored-square p198 gap/order searches.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
The independent military model and its provenance are shared with joint_search.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import ALPHABET, encrypt, decrypt, plaintext_domains, untranspose
HERE = Path(__file__).resolve().parent
MODEL_SHA = 'fc450633e557d477d009fd9f682a0d6c96629d48a532c1dd2fbc42af0c73b46d'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fixtures():
    keys = {x['id']: x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    target = next(x for x in json.loads((ROOT/'data/messages.json').read_text())['messages'] if x['id']=='p198')
    selected = ['CHI-Nov13', 'Nov13-15a', 'Nov13-15b', 'Nov16-18', 'Nov10-12', 'CHI-Nov8-2026-recovery']
    cases=[]
    for keyid in selected:
        key=keys[keyid]
        for width in [14, 15, 16, 17, 18, 19, 20, 21, 22]:
            cases.append(dict(id=f'p198__{keyid}__k{width}', target='p198', key_hypothesis=keyid,
                              width=width, partial_square=key['square'], gap_size=5,
                              ranks_start=key['column_rank_order'] if key['column_count']==width else [0]*width,
                              ciphertext=target['transcript']['analysis_ciphertext']))
    # Newly written synthetic radio prose; evaluation plaintext is never passed
    # to the optimizer and is absent from the hash-pinned model's training books.
    body='DERSTABMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEWEITEREBEFEHLEUEBERMITTELN'
    assert len(body)==85
    rng=random.Random(202611021536)
    for width, gap in [(16,75),(19,109),(20,20)]:
        partial=keys['CHI-Nov13']['square']; remaining=[ch for ch in ALPHABET if ch not in partial]
        rng.shuffle(remaining); remain=iter(remaining)
        square=''.join(next(remain) if ch=='?' else ch for ch in partial)
        ranks=list(range(1,width+1));rng.shuffle(ranks)
        full=encrypt(body,ranks,square)
        ct=full[:gap]+full[gap+5:]
        cases.append(dict(id=f'control__CHI-Nov13__k{width}',target='synthetic',key_hypothesis='CHI-Nov13',width=width,
                          partial_square=partial,gap_size=5,ranks_start=[0]*width,ciphertext=ct,
                          evaluation_only=dict(plaintext=body,square=square,ranks=ranks,gap_before_source_0based=gap,
                                               full_ciphertext=full)))
    return cases


def verify_record(record, recompute_score=False, model=None):
    case=record['case'];best=record['best'];sq=best['square'];ranks=best['ranks']
    assert len(sq)==36 and set(sq)==set(ALPHABET)
    assert all(a=='?' or a==b for a,b in zip(case['partial_square'],sq))
    assert sorted(ranks)==list(range(1,case['width']+1))
    g=best['gap_before_source_0based'];n=case['gap_size'];ct=case['ciphertext']
    assert 0<=g<=len(ct) and n==best['gap_size']
    padded=ct[:g]+'?'*n+ct[g:]
    assert decrypt(padded,ranks,sq)==best['plaintext']
    domains=plaintext_domains(padded,ranks,sq)
    # One witness completes every erased coordinate and reproduces every
    # observed coordinate. This is an arithmetic check, not a reading.
    witness=''.join(d[0] for d in domains)
    encoded=encrypt(witness,ranks,sq)
    assert all(a=='?' or a==b for a,b in zip(padded,encoded))
    output=dict(source_coordinates_preserved=len(ct),plaintext_positions=len(domains),
                singleton_positions=sum(len(x)==1 for x in domains),
                plaintext_domains=domains,accepted_historical_plaintext=False)
    if 'evaluation_only' in case:
        truth=case['evaluation_only'];truep=truth['plaintext']
        output['control']=dict(correct_gap=g==truth['gap_before_source_0based'],
            correct_ranks=ranks==truth['ranks'],truth_in_all_domains=all(ch in d for ch,d in zip(truep,domains)),
            correct_singletons=sum(len(d)==1 and d==ch for d,ch in zip(domains,truep)))
    if recompute_score:
        import array
        q=array.array('f');q.frombytes(Path(model).read_bytes())
        if sys.byteorder=='big':q.byteswap()
        score=0.0
        for j in range(len(domains)-3):
            ds=domains[j:j+4];total=0.0;count=math.prod(map(len,ds))
            for letters in itertools.product(*ds):
                code=0
                for ch in letters:code=36*code+ALPHABET.index(ch)
                total+=10**q[code]
            score+=math.log10(total/count)
        score/=len(domains)-3
        assert abs(score-best['score'])<1e-7,(score,best['score'])
        output['score_recomputed']=score
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,default=HERE/'bin/gap_anchored')
    p.add_argument('--model',type=Path,default=Path('/tmp/adfgvx-models/german_military36_quad.bin'))
    p.add_argument('--output',type=Path,default=Path('/tmp/adfgvx-gap-results'))
    p.add_argument('--restarts',type=int,default=100)
    p.add_argument('--iterations',type=int,default=50000)
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--only',default='*')
    p.add_argument('--controls',action='store_true')
    p.add_argument('--list',action='store_true')
    p.add_argument('--verify',type=Path)
    args=p.parse_args()
    import fnmatch
    cases=[c for c in fixtures() if ('evaluation_only' in c)==args.controls and fnmatch.fnmatch(c['id'],args.only)]
    if args.verify:
        result=verify_record(json.loads(args.verify.read_text()),True,args.model)
        print(json.dumps(result,indent=2));return
    if args.list:
        print(json.dumps(cases,indent=2));return
    assert cases and args.restarts>0 and args.iterations>0 and args.workers>0
    assert digest(args.model)==MODEL_SHA
    args.output.mkdir(parents=True,exist_ok=True)
    modelhash=digest(args.model);enginehash=digest(args.engine);sourcehash=digest(HERE/'gap_anchored.c')
    def run(case):
        seed=int(hashlib.sha256(case['id'].encode()).hexdigest()[:15],16)
        path=args.output/(case['id']+'.json')
        recipe=dict(restarts=args.restarts,iterations=args.iterations,seed=seed,model_sha256=modelhash,engine_sha256=enginehash,
                    source_sha256=sourcehash,fixed_gap=-1,score='Mean-domain quadgram composite; every known half-coordinate retained')
        if path.exists():
            row=json.loads(path.read_text());assert row['recipe']==recipe and row['case']==case
            verify_record(row);return dict(id=case['id'],resumed=True,best=row['best'],verification=row['verification'])
        text=f'{args.model.resolve()} {case["width"]} {args.restarts} {args.iterations} {seed} {case["gap_size"]} -1\n'
        text+=case['partial_square']+'\n'+' '.join(map(str,case['ranks_start']))+'\n'+case['ciphertext']+'\n'
        start=time.monotonic();completed=subprocess.run([str(args.engine.resolve())],input=text,text=True,capture_output=True,check=True)
        rows=[json.loads(line) for line in completed.stdout.splitlines()];assert rows
        row=dict(case=case,recipe=recipe,best=rows[-1],elapsed_seconds=time.monotonic()-start,accepted_historical_plaintext=False)
        row['verification']=verify_record(row,True,args.model)
        path.write_text(json.dumps(row,indent=2)+'\n')
        path.with_suffix('.jsonl').write_text(completed.stdout)
        return dict(id=case['id'],best=row['best'],verification={k:v for k,v in row['verification'].items() if k!='plaintext_domains'})
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(run,cases):print(json.dumps(r),flush=True)

if __name__=='__main__':main()
