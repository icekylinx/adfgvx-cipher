"""Independent checks and deterministic controls for the conditional enumeration.

This is a post-discovery crib test, not a blind cryptanalytic search.
"""
from pathlib import Path
import argparse
import hashlib
import json
import random
import subprocess

ROOT=Path(__file__).resolve().parent
COORDS='ADFGVX'
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def encode(text,ranks,square):
    stream=''.join('??' if c=='?' else COORDS[square.index(c)//6]+COORDS[square.index(c)%6] for c in text)
    return ''.join(stream[i] for col in sorted(range(18),key=ranks.__getitem__) for i in range(col,len(stream),18))


def run_case(engine,path):
    proc=subprocess.run([str(engine),str(path)],capture_output=True,text=True,check=True)
    rows=[json.loads(line) for line in proc.stdout.splitlines()]
    pt1,ct1,pt2,ct2=path.read_text().split()
    solutions=[r for r in rows if r['kind']=='solution'];summary=rows[-1]
    assert summary['kind']=='summary' and summary['segmentations']==18564
    assert summary['solutions']==len(solutions)
    for row in solutions:
        ranks=row['ranks'];square=row['partial_square']
        assert sorted(ranks)==list(range(1,19)) and len(square)==36
        assert len(set(square.replace('?','')))==len(square.replace('?',''))
        first=encode(pt1,ranks,square)
        assert all(a=='?' or a==b for a,b in zip(first,ct1))
        second=encode(pt2+'?'*(54-len(pt2)),ranks,square)
        changes=[{'source_index':i,'observed':a,'proposed':b} for i,(a,b) in enumerate(zip(ct2,second)) if a!='?' and b!='?' and a!=b]
        assert sorted(changes,key=lambda d:d['source_index'])==sorted(row['edits'],key=lambda d:d['source_index'])
        assert len(changes)==row['second_crib_known_coordinate_mismatches']
    return rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,default=ROOT/'enumerate')
    p.add_argument('--output',type=Path)
    args=p.parse_args();engine=args.engine.resolve()
    historical=run_case(engine,ROOT/'historical_input.txt')
    saved=[json.loads(line) for line in (ROOT/'historical_result.jsonl').read_text().splitlines()]
    for actual,old in zip(historical,saved):
        a=dict(actual);b=dict(old);a.pop('cpu_seconds',None);b.pop('cpu_seconds',None);assert a==b
    assert len(historical)==len(saved)
    assert historical[-1]['solutions']==2 and historical[-1]['minimum_second_crib_known_coordinate_mismatches']==2
    a,b=historical[:2]
    assert a['ranks']==[b['ranks'][i^1] for i in range(18)]
    assert a['partial_square']==''.join(b['partial_square'][6*c+r] for r in range(6) for c in range(6))
    assert all(sorted(d['source_index'] for d in r['edits'])==[3,4] for r in historical[:2])
    control_dir=ROOT/'controls';control_dir.mkdir(exist_ok=True)
    reports=[]
    for k in range(2):
        rng=random.Random(202611025300+k)
        letters='ABCDEGHILMNORSTUVWZ'
        hidden={14,18,19,25,26,27}
        first=[rng.choice(letters) for _ in range(66)]
        positions=[i for i in range(66) if i not in hidden];rng.shuffle(positions)
        for i,c in zip(positions,letters):first[i]=c
        first=''.join(first);crib=''.join('?' if i in hidden else c for i,c in enumerate(first))
        second=''.join(rng.choice(letters) for _ in range(54))
        square=list(ALPHABET);rng.shuffle(square);square=''.join(square)
        ranks=list(range(1,19));rng.shuffle(ranks)
        ct1=encode(first,ranks,square);ct2=list(encode(second,ranks,square))
        ct2[5:20]='?'*15
        changes=[]
        if k:
            for i in [0,1]:
                expected=ct2[i];ct2[i]=COORDS[(COORDS.index(expected)+1)%6]
                changes.append({'source_index':i,'observed':ct2[i],'proposed':expected})
        inputs='\n'.join([crib,ct1,second[:42],''.join(ct2)])+'\n'
        path=control_dir/f'control_{k}.txt';path.write_text(inputs)
        rows=run_case(engine,path)
        truth=next(r for r in rows[:-1] if r['ranks']==ranks)
        assert sorted(truth['edits'],key=lambda d:d['source_index'])==changes
        assert rows[-1]['solutions']==2
        assert rows[-1]['minimum_second_crib_known_coordinate_mismatches']==2*k
        reports.append({'name':f'control_{k}','seed':202611025300+k,'expected_ranks':ranks,
                        'true_square':square,'expected_known_coordinate_changes':changes,
                        'source_sha256':hashlib.sha256(inputs.encode()).hexdigest(),'results':rows})
    # An all-A crib would require every physical column to be constant. The
    # mixed-symbol source above cannot be transformed into that pattern.
    path=control_dir/'impossible_constant_crib.txt'
    path.write_text('\n'.join(['A'*66,ct1,'A'*42,''.join(ct2)])+'\n')
    negative=run_case(engine,path);assert negative[-1]['solutions']==0
    report={'passed':True,'classification':'Exact post-discovery conditional validation',
            'historical':historical,'controls':reports,'negative_control':negative,
            'engine_source_sha256':hashlib.sha256((ROOT/'enumerate.c').read_bytes()).hexdigest(),
            'scope':'Only width 18, separately reset rectangles, the supplied 60-letter first-part crib, and an injective 36-cell square. Unknown square cells and the six masked positions are not assigned. No blind-recovery or historical-uniqueness claim.'}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':True,'historical_partial_keys':2,'equivalent_representations':True,
                      'minimum_part6_crib_emendations':2,'positive_controls':2,'negative_controls':1}))


if __name__=='__main__':main()
