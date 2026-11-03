#!/usr/bin/env python3
"""Run one frozen 62-window scope, preserving all capped statuses."""
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse
import json
from pathlib import Path
import time
from bitset_search import Search

def solve(item):
    case,cap=item
    return Search(case,cap).run()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--workers',type=int,default=3)
    p.add_argument('--cap',type=int,default=25000000)
    args=p.parse_args()
    cases=json.loads(args.input.read_text());assert len(cases)==62
    order={c['id']:i for i,c in enumerate(cases)}
    results=[];start=time.monotonic()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(solve,[(c,args.cap) for c in cases]):
            results.append(result)
            report=dict(windows=len(results),per_branch_cap=args.cap,
                statuses={s:sum(r['status']==s for r in results) for s in ['excluded','feasible','capped']},
                nodes=sum(r['nodes'] for r in results),wall_seconds=time.monotonic()-start,
                results=[dict(id=r['id'],status=r['status'],nodes=r['nodes'],seconds=r['seconds'],
                              witness=r['witness']) for r in results])
            temp=args.output.with_suffix('.tmp')
            temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(args.output)
            print(result['id'],result['status'],result['nodes'],flush=True)
    assert len(results)==62

if __name__=='__main__':main()
