#!/usr/bin/env python3
"""Recompute supplementary source and published-layer verification independently."""
import json,re
from pathlib import Path
A='ADFGVX'

def untranspose(c,r):
    # Assign each successive ciphertext column to its original grid positions.
    positions=sorted(range(len(r)),key=lambda x:r[x])
    result=['']*len(c); at=0
    for col in positions:
        for p in range(col,len(c),len(r)):
            result[p]=c[at];at+=1
    assert at==len(c)
    return ''.join(result)
def transpose(s,r):
    return ''.join(s[c::len(r)] for c in sorted(range(len(r)),key=lambda x:r[x]))
def calc(c,k):
    square=k['square'];r=k['column_rank_order'];s=untranspose(c,r)
    unused=sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(square))
    domains=[]; rows=[]
    for i in range(0,len(s)-1,2):
        pair=s[i:i+2];cells=[6*x+y for x in range(6) for y in range(6)
            if (pair[0]=='?' or A[x]==pair[0]) and (pair[1]=='?' or A[y]==pair[1])]
        chars=set()
        for cell in cells:chars.update(unused if square[cell]=='?' else square[cell])
        domains.append(''.join(sorted(chars)));rows.append(cells)
    pt=''.join(x if len(x)==1 else '?' for x in domains)
    # Re-encode the fixed plaintext cells, preserving unresolved pair coordinates.
    reenc=[]
    for i,ch in enumerate(pt):
        if ch=='?':reenc.append(s[2*i:2*i+2])
        else:
            idx=square.index(ch);pair=A[idx//6]+A[idx%6]
            assert all(a=='?' or a==b for a,b in zip(s[2*i:2*i+2],pair))
            reenc.append(pair)
    rebuilt=''.join(reenc)+s[2*len(pt):]
    recipher=transpose(rebuilt,r)
    conflicts=[i for i,(a,b) in enumerate(zip(c,recipher)) if a!='?' and a!=b]
    return {'ciphertext_length':len(c),'intermediate_stream':s,'plaintext':pt,
        'plaintext_length':len(pt),'fixed_plaintext_characters':sum(len(x)==1 for x in domains),
        'plaintext_domains':domains,'unpaired_suffix':s[2*len(pt):],
        'coordinate_roundtrip':transpose(s,r)==c,
        'fixed_plaintext_reencoding_known_coordinate_conflicts':conflicts,
        'full_plaintext_roundtrip':len(s)%2==0 and '?' not in pt and recipher==c}

def verify(path):
    data=json.loads(Path(path).read_text())
    checked=[]
    for m in data['messages']:
        literal=''.join(x for x in m['raw_source_grouped'] if x in A+'-?').replace('-','?')
        assert literal==m['source_ciphertext_literal_letters']
        assert len(literal)==m['source']['advertised_length']
        for variant,field in [('source','source_ciphertext_literal_letters'),('conservative_source','source_ciphertext_conservative'),('published','published_ciphertext')]:
            result=calc(m[field],m['key'])
            assert result==m[variant+'_verification'],(m['id'],variant)
            assert result['coordinate_roundtrip']
            assert not result['fixed_plaintext_reencoding_known_coordinate_conflicts']
        assert m['published_verification']['plaintext']==m['published_plaintext']
        differences=[{'index':i,'source':a,'published':b} for i,(a,b) in enumerate(zip(literal,m['published_ciphertext'])) if a!=b]
        assert differences==m['published_vs_literal_source_changes']
        checked.append({'id':m['id'],'source_length':len(literal),'source_fixed_plaintext':m['source_verification']['fixed_plaintext_characters'],'source_plaintext_slots':m['source_verification']['plaintext_length'],'published_reproduced':True})
    return {'passed':True,'messages':checked}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('path',nargs='?',default=str(Path(__file__).resolve().parent.parent / 'data/supplementary_readings.json'))
    p.add_argument('--output')
    args=p.parse_args();text=json.dumps(verify(args.path),indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text)
