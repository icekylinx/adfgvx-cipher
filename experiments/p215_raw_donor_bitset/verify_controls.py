#!/usr/bin/env python3
"""Compare 89 independent exhaustive oracles and the full-size blind control."""
import argparse
import json
from pathlib import Path
import random
import tempfile
from bitset_search import Search
import oracle
from prepare import prepare

def additional_cases():
    rng=random.Random(202611042152)
    base='QNZ72XS4C0IJY3RBEKL9FD6GMTHUVWA5O8P1'
    for number in range(52):
        width=2 if number%4==0 else 4
        length=rng.randint(4,8)
        cells=rng.sample(range(36),number%5)
        partial=''.join('?' if i in cells else c for i,c in enumerate(base))
        pool=''.join(base[i] for i in cells) or base
        plaintext=''.join(rng.choice(pool if i%3 else base) for i in range(length))
        domains=[''.join(sorted(set(c+''.join(rng.sample(base,rng.randint(0,3)))))) for c in plaintext]
        order=list(range(width));rng.shuffle(order)
        cipher,_=oracle.encode(plaintext,base,width,order)
        lost=set(rng.sample(range(2*length),number%3))
        target=''.join(c for i,c in enumerate(cipher) if i not in lost)
        if number%2:target=''.join(rng.choice(oracle.COORDS) for _ in target)
        masked=set(rng.sample(range(len(target)),number%4))
        target=''.join('?' if i in masked else c for i,c in enumerate(target))
        yield dict(id=f'extra_{number:02d}',width=width,square=partial,domains=domains,target=target)

def verify():
    cases=oracle.generate()+list(additional_cases())
    feasible=0
    for case in cases:
        expected=oracle.solve(case)
        actual=Search(case,2000000).run()
        assert actual['status']!='capped',case['id']
        assert (actual['status']=='feasible')==expected['feasible'],case['id']
        feasible+=expected['feasible']
    assert len(cases)==89 and feasible==53
    with tempfile.TemporaryDirectory() as temp:
        _,_,control=prepare(Path(temp))
        result=Search(control,1000000).run()
    assert result['status']=='feasible'
    witness,truth=result['witness'],control['control_truth']
    for field in ['square','column_order','deleted_transmitted_indices']:
        assert witness[field]==truth[field],field
    assert sum(c!='?' for c in control['target'])==200
    return dict(independent_exhaustive_cases=89,feasible=53,infeasible=36,all_agree=True,
        same_shape_unhinted=dict(source_slots=219,observations=200,printed_masks=19,
            transmitted_deletions=15,status=result['status'],nodes=result['nodes'],
            exact_square=True,exact_column_order=True,exact_deletions=True,
            arbitrary_witness_plaintext_matches=sum(a==b for a,b in zip(truth['plaintext'],witness['plaintext'])),
            plaintext_positions=117))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    args=p.parse_args();result=verify();encoded=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(encoded)
    print(encoded,end='')
