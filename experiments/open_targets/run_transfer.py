#!/usr/bin/env python3
"""Test the literal neighboring XAXVV group as p198 D's missing five slots.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
No source coordinate may be changed. Partial-square anchors remain fixed.
Known-key enumeration is exhaustive only within the stated key library;
variable-rank search is bounded and evaluated with fresh planted controls.
"""
from pathlib import Path
import argparse
import array
import concurrent.futures
import copy
import fnmatch
import hashlib
import json
import subprocess
import sys
import time

from run_gap import fixtures, ROOT, MODEL_SHA, digest
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET, decrypt, encrypt, plaintext_domains

HERE=Path(__file__).resolve().parent


def cases():
    rows=copy.deepcopy(fixtures())
    for row in rows:
        row['id']=row['id'].replace('p198__','transfer__').replace('control__','transfer_control__')
        if 'evaluation_only' in row:
            ev=row['evaluation_only'];gap=ev['gap_before_source_0based']
            row['inserted_group']=ev['full_ciphertext'][gap:gap+5]
        else:row['inserted_group']='XAXVV'
    return rows


def verify(row,model):
    case,best=row['case'],row['best'];g=best['gap_before_source_0based']
    assert 0<=g<=len(case['ciphertext'])
    sq=best['square'];ranks=best['ranks'];group=case['inserted_group']
    assert sorted(ranks)==list(range(1,case['width']+1))
    assert len(sq)==36 and set(sq)==set(ALPHABET)
    assert all(a=='?' or a==b for a,b in zip(case['partial_square'],sq))
    ct=case['ciphertext'][:g]+group+case['ciphertext'][g:]
    assert len(ct)==170 and ct[:g]+ct[g+5:]==case['ciphertext']
    pt=decrypt(ct,ranks,sq)
    assert pt==best['plaintext'] and encrypt(pt,ranks,sq)==ct
    score=0
    for i in range(len(pt)-3):
        code=0
        for ch in pt[i:i+4]:code=36*code+ALPHABET.index(ch)
        score+=model[code]
    score/=len(pt)-3
    assert abs(score-best['score'])<1e-7
    result=dict(source_coordinates_preserved=165,inserted_known_group=group,
                exact_coordinate_roundtrip=True,score_recomputed=score,
                accepted_historical_plaintext=False)
    if 'evaluation_only' in case:
        ev=case['evaluation_only']
        result['control']=dict(exact_plaintext=pt==ev['plaintext'],
            correct_plaintext_positions=sum(a==b for a,b in zip(pt,ev['plaintext'])),
            exact_ranks=ranks==ev['ranks'],planted_gap=ev['gap_before_source_0based'],
            recovered_gap=g,all_source_equivalent_true_group_positions=[i for i in range(166) if ev['full_ciphertext'][i:i+5]==group and ev['full_ciphertext'][:i]+ev['full_ciphertext'][i+5:]==case['ciphertext']])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,default=HERE/'bin/group_transfer')
    p.add_argument('--model',type=Path,default=Path('/tmp/adfgvx-models/german_military36_quad.bin'))
    p.add_argument('--output',type=Path,default=Path('/tmp/adfgvx-transfer-results'))
    p.add_argument('--restarts',type=int,default=100)
    p.add_argument('--iterations',type=int,default=50000)
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--only',default='*')
    p.add_argument('--controls',action='store_true')
    p.add_argument('--verify',type=Path)
    args=p.parse_args()
    assert digest(args.model)==MODEL_SHA
    model=array.array('f');model.frombytes(args.model.read_bytes())
    if sys.byteorder=='big':model.byteswap()
    if args.verify:print(json.dumps(verify(json.loads(args.verify.read_text()),model),indent=2));return
    selected=[row for row in cases() if ('evaluation_only' in row)==args.controls and fnmatch.fnmatch(row['id'],args.only)]
    assert selected and args.restarts>0 and args.iterations>0 and args.workers>0
    args.output.mkdir(parents=True,exist_ok=True)
    def run(case):
        seed=int(hashlib.sha256(case['id'].encode()).hexdigest()[:15],16)
        recipe=dict(restarts=args.restarts,iterations=args.iterations,seed=seed,model_sha256=MODEL_SHA,
                    source_sha256=digest(HERE/'group_transfer.c'),engine_sha256=digest(args.engine),fixed_gap=-1)
        output=args.output/(case['id']+'.json')
        if output.exists():
            row=json.loads(output.read_text());assert row['recipe']==recipe and row['case']==case
            verify(row,model);return row
        inp=f'{args.model.resolve()} {case["width"]} {args.restarts} {args.iterations} {seed} 5 -1\n'
        inp+=case['partial_square']+'\n'+' '.join(map(str,case['ranks_start']))+'\n'+case['ciphertext']+'\n'+case['inserted_group']+'\n'
        start=time.monotonic();p=subprocess.run([str(args.engine.resolve())],input=inp,text=True,capture_output=True,check=True)
        best=json.loads(p.stdout.splitlines()[-1])
        row=dict(case=case,recipe=recipe,best=best,elapsed_seconds=time.monotonic()-start)
        row['verification']=verify(row,model)
        output.write_text(json.dumps(row,indent=2)+'\n');output.with_suffix('.jsonl').write_text(p.stdout)
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for row in pool.map(run,selected):print(json.dumps(dict(id=row['case']['id'],best=row['best'],verification=row['verification'])),flush=True)

if __name__=='__main__':main()
