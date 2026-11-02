#!/usr/bin/env python3
"""Independent small-instance exhaustion for segment_gap.c.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026), Apache-2.0.
Checks the exact monogram-matching relaxation, not historical plaintext.
"""
from pathlib import Path
import argparse
import itertools
import json
import math
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,SYMBOLS,encrypt,untranspose


def monogram_score(ct,ranks,square,prior):
    unused=[x for x in ALPHABET if x not in square]
    mean=sum(prior[x] for x in unused)/len(unused) if unused else 0
    cell=[prior.get(ch,mean) for ch in square]
    stream=untranspose(ct,ranks);score=0
    for a,b in zip(stream[::2],stream[1::2]):
        rows=[SYMBOLS.index(a)] if a in SYMBOLS else range(6)
        cols=[SYMBOLS.index(b)] if b in SYMBOLS else range(6)
        prob=sum(cell[6*r+c] for r in rows for c in cols)/(len(rows)*len(cols))
        score+=math.log10(prob)
    return score


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,default=Path(__file__).resolve().parent/'bin/segment_gap')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    prior=dict(zip(ALPHABET,map(float,(ROOT/'experiments/joint_search/models/military_monograms.txt').read_text().split())))
    norm=sum(prior.values());prior={x:v/norm for x,v in prior.items()}
    plaintext='DIEBRUECKEWIRDHEUTEABENDGEPRUEFTXXX'
    plaintext=plaintext[:34].ljust(34,'X')
    assert len(plaintext)==34
    ranks=[4,1,6,2,5,3];square=ALPHABET
    full=encrypt(plaintext,ranks,square);cut=11;loss=5
    raw=full[:cut]+full[cut+loss:];width=6;remainder=len(full)%width
    lines=f'{width} {loss} 1 2048\n'+square+'\n'+'\n'.join(str(prior[x])for x in ALPHABET)+'\n'+raw+'\n-1\n'+'0 '*width+'\n'
    proc=subprocess.run([str(args.engine)],input=lines,text=True,capture_output=True,check=True)
    records=[json.loads(l)for l in proc.stdout.splitlines()];summary=records.pop()
    expected={};tested=0
    for gap in range(len(raw)+1):
        ct=raw[:gap]+'?'*loss+raw[gap:]
        for key in itertools.permutations(range(1,width+1)):
            mask=sum(1<<(v-1)for v in key[:remainder]);score=monogram_score(ct,key,square,prior)
            expected[(gap,mask)]=max(score,expected.get((gap,mask),-math.inf));tested+=1
    assert len(expected)==summary['enumerated_gap_segmentations']==len(records)
    for r in records:
        key=(r['gap_before_source_0based'],r['long_mask'])
        assert abs(r['monogram_score']-expected[key])<1e-9
        ct=raw[:key[0]]+'?'*loss+raw[key[0]:]
        assert abs(monogram_score(ct,r['ranks'],square,prior)-r['monogram_score'])<1e-9
    output=dict(verified=True,exhausted_keys_and_gaps=tested,geometry_classes=len(expected),
                scope='Independent enumeration of every width-six permutation and every contiguous five-coordinate gap.',
                historical_reading_claim=False)
    if args.output:args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
