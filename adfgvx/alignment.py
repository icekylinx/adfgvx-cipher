"""Independent exhaustive single-switch comparison of Childs p158 D.

The comparison uses ciphertext alone. Its models are explicitly restricted:
the start is aligned to a prefix of p159 B and the end to a suffix of p159 C.
Every insertion/deletion/substitution of a received symbol costs one; any
explicit source erasure is compatible with one symbol, not an arbitrary block.
The result identifies source correspondence, not one underlying plaintext.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from .cipher import SYMBOLS



def mismatch(a, b):
    return int(a in SYMBOLS and b in SYMBOLS and a != b)


def table(a, b):
    dp = [list(range(len(b)+1))]
    for i, x in enumerate(a, 1):
        row = [i]
        previous = dp[-1]
        for j, y in enumerate(b, 1):
            row.append(min(previous[j]+1, row[-1]+1,
                           previous[j-1]+mismatch(x,y)))
        dp.append(row)
    return dp


def alignment(a, b):
    dp = table(a,b)
    i,j=len(a),len(b)
    aa,bb=[],[]
    while i or j:
        if i and j and dp[i][j] == dp[i-1][j-1]+mismatch(a[i-1],b[j-1]):
            aa.append(a[i-1]); bb.append(b[j-1]); i-=1; j-=1
        elif i and dp[i][j] == dp[i-1][j]+1:
            aa.append(a[i-1]); bb.append("."); i-=1
        else:
            aa.append("."); bb.append(b[j-1]); j-=1
    aa="".join(reversed(aa));bb="".join(reversed(bb))
    count=Counter()
    for x,y in zip(aa,bb):
        if x==".": count["source_only"]+=1
        elif y==".": count["p158_only"]+=1
        elif x not in SYMBOLS or y not in SYMBOLS: count["erasure_compatible"]+=1
        elif x==y: count["exact_known_matches"]+=1
        else: count["known_substitutions"]+=1
    assert aa.replace(".","")==a and bb.replace(".","")==b
    charged=count["source_only"]+count["p158_only"]+count["known_substitutions"]
    assert charged==dp[-1][-1]
    return {"p158_aligned":aa,"parallel_source_aligned":bb,"counts":dict(count),"edit_cost":charged}


def find_switch(a,b,c):
    left=table(a,b)
    right=table(a[::-1],c[::-1])
    best=10**9
    solutions=[]
    frontier=[]
    for split in range(len(a)+1):
        lcost=min(left[split]);rcost=min(right[len(a)-split])
        cost=lcost+rcost
        endpoints_b=[j for j,v in enumerate(left[split]) if v==lcost]
        starts_c=[len(c)-j for j,v in enumerate(right[len(a)-split]) if v==rcost]
        frontier.append({"p158_split":split,"cost":cost})
        if cost<best:
            best=cost;solutions=[]
        if cost==best:
            for bend in endpoints_b:
                for cstart in starts_c:
                    solutions.append({"p158_split":split,"B_prefix_end":bend,"C_suffix_start":cstart})
    for solution in solutions:
        s,i,j=solution["p158_split"],solution["B_prefix_end"],solution["C_suffix_start"]
        solution["prefix_alignment"]=alignment(a[:s],b[:i])
        solution["suffix_alignment"]=alignment(a[s:],c[j:])
    return {"minimum_cost":best,"optimal_switches":solutions,"cost_by_split":frontier}

