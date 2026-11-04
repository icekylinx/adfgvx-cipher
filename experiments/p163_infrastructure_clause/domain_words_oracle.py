#!/usr/bin/env python3
"""Small exhaustive concrete-plaintext oracle for the optimized domain DP."""
from itertools import product
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

SCRIPT=Path(__file__).resolve().parent
temporary=tempfile.TemporaryDirectory(prefix='adfgvx-domain-oracle-')
HERE=Path(temporary.name)
executable=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE/'domain_words'
if len(sys.argv)==1:
    subprocess.run(['g++','-O2','-std=c++17','-o',str(executable),str(SCRIPT/'domain_words.cpp')],check=True)
AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
rng=random.Random(1632026)
words=['A','B','AB','BA','ABA','BAB','CD','ACD','DBA','AX','XAB','ABCD']
score={w:round(rng.uniform(-5,-1),8) for w in words}
bonus={(a,b):round(rng.uniform(0,2),8) for a in words for b in words if rng.random()<.28}
lex=HERE/'domain_oracle.lex'
lex.write_text(f'{len(words)} {len(bonus)}\n'+''.join(f'{w} {score[w]}\n' for w in words)+''.join(f'{words.index(a)} {words.index(b)} {s}\n' for (a,b),s in bonus.items()))
domains=[]
for z in range(160):
    domains.append([sorted(rng.sample('ABCDX01',rng.choice([1,1,2]))) for _ in range(rng.randint(1,7))])
domains += [[list(s)] for s in ['CX','01','C','X','A']]
frames=HERE/'domain_oracle.frames'
frames.write_text(''.join(f'{i} {len(ds)} '+' '.join(str(sum(1<<AL.index(c) for c in d)) for d in ds)+'\n' for i,ds in enumerate(domains)))

def exact_plain(text,fallback,weight,xscore):
    # No trie or domain traversal: brute-force every token and predecessor
    # on an already completed plaintext, then maximize over every completion.
    dp=[{} for _ in range(len(text)+1)];dp[0][None]=0.
    for i in range(len(text)):
        edges=[]
        if text[i]=='X': edges.append((i+1,None,xscore))
        elif fallback>-1e90: edges.append((i+1,None,fallback))
        for j in range(i,min(i+10,len(text))):
            if not text[j].isdigit():break
            edges.append((j+1,'#',-1-(j-i+1)))
        for w in words:
            if text.startswith(w,i):edges.append((i+len(w),w,score[w]))
        for end,w,s in edges:
            for prev,p in dp[i].items():
                val=p+s+weight*bonus.get((prev,w),0)
                dp[end][w]=max(dp[end].get(w,-1e100),val)
    return max(dp[-1].values(),default=-1e100)

count=0
for fallback,weight,xscore in [(-3,.65,-.25),(-1e100,.65,-.25),(-3,0,-2),(-.1,.65,-.25)]:
    output=subprocess.check_output([str(executable),str(lex),str(frames),str(fallback),str(weight),str(xscore)],text=True)
    result=[json.loads(s) for s in output.splitlines()]
    assert len(result)==len(domains)
    for i,(ds,got) in enumerate(zip(domains,result)):
        want=max(exact_plain(''.join(p),fallback,weight,xscore) for p in product(*ds))
        if want<-1e90:assert not got['feasible'],(i,ds,got,want)
        else:assert got['feasible'] and abs(got['score']-want)<1e-7,(i,ds,got,want)
        count+=1
missing=subprocess.run([str(executable),str(lex),str(HERE/'missing.frames')],text=True,capture_output=True)
assert missing.returncode!=0 and 'frames' in missing.stderr
print(json.dumps({'verified_domain_frames_and_parameter_settings':count,'unreadable_frame_file_rejected':True,'oracle':'Every concrete plaintext completion, every lexical token, and every predecessor state; no trie or positive-bigram optimization.'},indent=2))
