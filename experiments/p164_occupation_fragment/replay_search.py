#!/usr/bin/env python3
"""Replay the frozen p164 half-coordinate phrase retrieval and controls.

Requires NumPy. No language-model binary or generated search dump is stored.
"""
from pathlib import Path
import hashlib
import json
import os
import random
import sys
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import encrypt
from verify import inverse, load, complete_squares
A='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
C='ADFGVX?'


def donors():
    cache={};texts=[]
    for entry in load(HERE/'donor_manifest.json')['streams']:
        matches=[]
        for ref in entry['sources']:
            path=ref['path']
            if path not in cache:cache[path]=load(ROOT/path)
            value=cache[path]
            for part in ref['json_path']:value=value[part]
            assert isinstance(value,str)
            assert hashlib.sha256(value.encode()).hexdigest()==entry['text_sha256']
            matches.append(value)
        assert len(set(matches))==1
        texts.append(matches[0])
    assert len(texts)==len(set(texts))==488
    return texts


def engine(texts,key,n):
    donor='?'.join(texts)
    vals=np.array([A.index(c) if c in A else 36 for c in donor],dtype=np.int16)
    iv=np.array(inverse(n,key['column_rank_order']))
    allowed=np.zeros((49,37),dtype=bool)
    missing=set(A)-set(key['square'])
    for pattern in range(49):
        a,b=divmod(pattern,7)
        for cell,ch in enumerate(key['square']):
            if(a==6 or a==cell//6)and(b==6 or b==cell%6):
                for label in (missing if ch=='?'else[ch]):allowed[pattern,A.index(label)]=True
    def best(source):
        mid=np.array([C.index(c)for c in source],dtype=np.int8)[iv]
        patterns=7*mid[::2]+mid[1::2]
        support=(mid[::2]<6).astype(int)+(mid[1::2]<6).astype(int)
        cs=np.r_[0,support.cumsum()];run=np.zeros(len(vals),dtype=np.int16)
        rank=(0,0);where=[]
        for i,pattern in enumerate(patterns):
            run=np.r_[0,run[:-1]]+1;run[~allowed[pattern,vals]]=0
            for j in np.flatnonzero(run>=12):
                length=int(run[j]);observed=int(cs[i+1]-cs[i+1-length]);current=(observed,length)
                if current>rank:rank=current;where=[]
                if current==rank:where.append((i+1-length,donor[j+1-length:j+1]))
        return dict(observed_support=rank[0],length=rank[1],hits=[list(x)for x in sorted(set(where))])
    return best


def main():
    inp=load(HERE/'inputs.json');data=load(ROOT/inp['source_certificate'])
    key=data['key'];source=next(s['ciphertext']for s in data['sources']if s['id']=='p164_A3')
    texts=donors();expected=load(HERE/'search_report.json');search=engine(texts,key,len(source))
    assert search(source)==expected['historical']
    rng=random.Random(expected['seed']);observed=[c for c in source if c!='?'];null=[]
    for i in range(500):
        rng.shuffle(observed);it=iter(observed)
        shuffled=''.join(next(it)if c!='?'else'?'for c in source)
        null.append(dict(id=i,**search(shuffled)))
    summary=dict(count=len(null),minimum_matched_length=12,
                 hits_at_minimum_length=sum(x['length']>=12 for x in null),
                 maximum_observed_support=max(x['observed_support']for x in null),
                 result_sha256=hashlib.sha256(json.dumps(null,sort_keys=True,separators=(',',':')).encode()).hexdigest())
    assert summary==expected['null_summary']
    rng=random.Random(202611040238165);controls=[];square=complete_squares(key['square'])[0]
    for word in ['VERBINDUNGEN','MITTELMEERDIVISION','KONSTANTINOPEL','EREIGNISSE']:
        assert any(word in text for text in texts)
        truth=[rng.choice(A)for _ in range(121)];truth[18:18+len(word)]=word;truth=''.join(truth)
        full=encrypt(truth,key['column_rank_order'],square)
        masked=''.join(a if b!='?'else'?'for a,b in zip(full,source))
        controls.append(dict(word=word,offset=18,source=masked,plaintext=truth,result=search(masked)))
    assert controls==expected['planted']
    print(json.dumps(dict(verified=True,donor_streams=len(texts),shuffle_controls=500,
                          long_planted_words_retrieved=3,short_below_threshold_control=1),indent=2))


if __name__=='__main__':main()
