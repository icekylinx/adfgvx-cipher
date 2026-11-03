#!/usr/bin/env python3
"""Generate scope inputs and a matched control from the frozen transcriptions."""
import argparse
import hashlib
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def prepare(output, repo=None):
    frozen = json.loads((HERE/'frozen_inputs.json').read_text())
    if repo:
        for path, wanted in frozen['repository_input_sha256'].items():
            assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == wanted, path
    output.mkdir(parents=True, exist_ok=True)
    donor, target = frozen['donor'], frozen['target']
    literal = ''.join(''.join(donor['source_rows']).split())
    source = ''.join(''.join(target['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == target['literal_sha256']
    assert len(source) == 219 and source.count('-') == 19
    assert target['square'].count('?') == 8
    cases = []
    for model in donor['models']:
        keep = [i for i in range(len(literal)) if i not in model['excluded_source_indices']]
        assert len(literal) == 284 and len(keep) == 269
        cut = sum(i < donor['insert_before_original_source'] for i in keep)
        tx = ''.join(literal[i] for i in keep[:cut])+'?'*25+''.join(literal[i] for i in keep[cut:])
        assert len(tx) == donor['frame_slots'] == 294
        interim, cursor = ['?']*294, 0
        ranks = donor['key']['column_rank_order']
        for col in sorted(range(len(ranks)), key=lambda c:ranks[c]):
            for pos in range(col, 294, len(ranks)):
                interim[pos] = tx[cursor]
                cursor += 1
        domains = []
        for i in range(0,294,2):
            x,y = interim[i:i+2]
            domains.append(''.join(sorted(donor['key']['square'][6*r+c]
                for r in range(6) for c in range(6)
                if (x=='?' or C[r]==x) and (y=='?' or C[c]==y))))
        assert ''.join(d if len(d)==1 else '?' for d in domains) == model['expected_raw']
        for start in range(31):
            cases.append(dict(id='p219C_'+model['id']+'_window'+str(start),
                width=22,square=target['square'],domains=domains[start:start+117],
                target=source.replace('-','?')))
    assert len(cases) == 62
    expanded=[]
    ambiguity=set(target['ambiguous_baseline_labels'])
    for case in cases:
        expanded.append(dict(case,id=case['id']+'_relaxed_unproved_labels',domains=[
            ''.join(sorted(set(d)|ambiguity if set(d)&ambiguity else set(d)))
            for d in case['domains']]))
    rng=random.Random(frozen['controls']['same_shape_seed'])
    control=dict(cases[0]);control['id']='matched_shape_unhinted_control'
    unused=sorted(set(A)-set(target['square']));rng.shuffle(unused)
    complete=list(target['square'])
    for i,c in zip([i for i,c in enumerate(complete) if c=='?'],unused):complete[i]=c
    complete=''.join(complete)
    text=''.join(rng.choice(d) for d in control['domains'])
    interim=''.join(C[complete.index(c)//6]+C[complete.index(c)%6] for c in text)
    order=list(range(22));rng.shuffle(order)
    full=''.join(interim[i] for col in order for i in range(col,234,22))
    losses=sorted(rng.sample(range(234),15))
    short=''.join(c for i,c in enumerate(full) if i not in losses)
    control['target']=''.join('?' if c=='-' else short[i] for i,c in enumerate(source))
    control['control_truth']=dict(square=complete,plaintext=text,column_order=order,
        deleted_transmitted_indices=losses,full_ciphertext=full)
    for name,data in [('literal62.json',cases),('relaxed62.json',expanded),('control.json',control)]:
        (output/name).write_text(json.dumps(data,indent=2)+'\n')
    return cases,expanded,control

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--repo',type=Path,help='Optionally check the pinned repository input files.')
    args=p.parse_args();prepare(args.output,args.repo)
    print('Generated 62 literal windows, 62 relaxed windows and one unhinted matched control.')
