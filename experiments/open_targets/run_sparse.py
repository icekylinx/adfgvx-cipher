#!/usr/bin/env python3
"""Bounded p198 searches with five separately located deletions.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026), Apache-2.0.
"""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import itertools
import json
import math
import random
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,encrypt,decrypt,plaintext_domains
from run_gap import digest, MODEL_SHA
HERE=Path(__file__).resolve().parent


def fixtures():
    keys=json.loads((ROOT/'data/keys.json').read_text())['keys']
    target=next(x for x in json.loads((ROOT/'data/messages.json').read_text())['messages'] if x['id']=='p198')
    cases=[]
    for key in keys:
        if 36-key['square'].count('?')<19:continue
        cases.append(dict(id='p198__'+key['id'],target='p198',key_hypothesis=key['id'],
            partial_square=key['square'],ranks=key['column_rank_order'],missing_count=5,
            ciphertext=target['transcript']['analysis_ciphertext']))
    body='DERSTABMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEWEITEREBEFEHLEUEBERMITTELN'
    rng=random.Random(202611021840)
    for keyid,missing in [('CHI-Nov13',[7,44,81,126,158]),('Nov13-15a',[1,38,39,111,166]),('Nov13-15b',[17,18,19,20,21])]:
        key=next(x for x in keys if x['id']==keyid);left=[ch for ch in ALPHABET if ch not in key['square']];rng.shuffle(left);it=iter(left)
        square=''.join(next(it) if ch=='?' else ch for ch in key['square'])
        full=encrypt(body,key['column_rank_order'],square)
        raw=''.join(ch for i,ch in enumerate(full) if i not in missing)
        cases.append(dict(id='control__'+keyid,target='synthetic',key_hypothesis=keyid,partial_square=key['square'],
            ranks=key['column_rank_order'],missing_count=5,ciphertext=raw,
            evaluation_only=dict(plaintext=body,square=square,full_ciphertext=full,missing_full_ciphertext_positions_0based=missing)))
    return cases


def verify_record(record,model=None):
    case=record['case'];best=record['best'];losses=best['missing_full_ciphertext_positions_0based']
    assert len(losses)==case['missing_count'] and losses==sorted(set(losses))
    n=len(case['ciphertext'])+len(losses);assert all(0<=i<n for i in losses)
    assert best['ranks']==case['ranks'] and set(best['square'])==set(ALPHABET)
    assert all(a=='?' or a==b for a,b in zip(case['partial_square'],best['square']))
    source=iter(case['ciphertext']);padded=''.join('?' if i in losses else next(source) for i in range(n))
    assert next(source,None) is None
    assert decrypt(padded,best['ranks'],best['square'])==best['plaintext']
    domains=plaintext_domains(padded,best['ranks'],best['square'])
    witness=''.join(d[0] for d in domains);encoded=encrypt(witness,best['ranks'],best['square'])
    assert all(a=='?' or a==b for a,b in zip(padded,encoded))
    result=dict(source_coordinates_preserved=len(case['ciphertext']),singleton_positions=sum(len(d)==1 for d in domains),
                plaintext_domains=domains,accepted_historical_plaintext=False)
    if 'evaluation_only' in case:
        truth=case['evaluation_only'];body=truth['plaintext']
        result['control']=dict(exact_missing_set=losses==truth['missing_full_ciphertext_positions_0based'],
            truth_in_all_domains=all(ch in d for ch,d in zip(body,domains)),
            correct_singletons=sum(len(d)==1 and d==ch for d,ch in zip(domains,body)))
    if model:
        import array
        q=array.array('f');q.frombytes(Path(model).read_bytes())
        if sys.byteorder=='big':q.byteswap()
        score=0.0
        for j in range(len(domains)-3):
            ds=domains[j:j+4];prob=0.0
            for letters in itertools.product(*ds):
                code=0
                for ch in letters:code=36*code+ALPHABET.index(ch)
                prob+=10**q[code]
            score+=math.log10(prob/math.prod(map(len,ds)))
        score/=len(domains)-3
        assert abs(score-best['score'])<1e-7
        result['recomputed_score']=score
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,default=HERE/'bin/sparse_loss')
    p.add_argument('--model',type=Path,default=Path('/tmp/adfgvx-models/german_military36_quad.bin'))
    p.add_argument('--output',type=Path,default=Path('/tmp/adfgvx-sparse-results'))
    p.add_argument('--restarts',type=int,default=100)
    p.add_argument('--iterations',type=int,default=50000)
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--only',default='*')
    p.add_argument('--controls',action='store_true')
    p.add_argument('--list',action='store_true')
    p.add_argument('--verify',type=Path)
    args=p.parse_args();import fnmatch
    if args.verify:
        assert digest(args.model)==MODEL_SHA
        print(json.dumps(verify_record(json.loads(args.verify.read_text()),args.model),indent=2));return
    cases=[c for c in fixtures() if ('evaluation_only' in c)==args.controls and fnmatch.fnmatch(c['id'],args.only)]
    if args.list:print(json.dumps(cases,indent=2));return
    assert cases and args.restarts>0 and args.iterations>0 and args.workers>0
    assert digest(args.model)==MODEL_SHA
    args.output.mkdir(parents=True,exist_ok=True)
    sourcehash=digest(Path(__file__).with_name('sparse_loss.c'));sharedhash=digest(Path(__file__).with_name('gap_anchored.c'))
    enginehash=digest(args.engine)
    def run(case):
        path=args.output/(case['id']+'.json');seed=int(hashlib.sha256(case['id'].encode()).hexdigest()[:15],16)
        recipe=dict(restarts=args.restarts,iterations=args.iterations,seed=seed,engine_sha256=enginehash,
            source_sha256=sourcehash,shared_scorer_sha256=sharedhash,model_sha256=MODEL_SHA,
            score='Mean-domain quadgram composite; known half-coordinates retained')
        if path.exists():
            row=json.loads(path.read_text());assert row['recipe']==recipe and row['case']==case;verify_record(row)
        else:
            text=f'{args.model.resolve()} {len(case["ranks"])} {args.restarts} {args.iterations} {seed} {case["missing_count"]}\n'
            text+=case['partial_square']+'\n'+' '.join(map(str,case['ranks']))+'\n'+case['ciphertext']+'\n'
            start=time.monotonic();proc=subprocess.run([str(args.engine)],input=text,text=True,capture_output=True,check=True)
            rows=[json.loads(l)for l in proc.stdout.splitlines()]
            row=dict(case=case,recipe=recipe,best=rows[-1],elapsed_seconds=time.monotonic()-start,accepted_historical_plaintext=False)
            row['verification']=verify_record(row,args.model)
            path.write_text(json.dumps(row,indent=2)+'\n');path.with_suffix('.jsonl').write_text(proc.stdout)
        return dict(id=case['id'],best=row['best'],verification={k:v for k,v in row['verification'].items() if k!='plaintext_domains'})
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for x in ex.map(run,cases):print(json.dumps(x),flush=True)

if __name__=='__main__':main()
