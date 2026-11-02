"""Fit unknown injective squares to dictionary-derived transposition candidates.

Candidates were selected without a square using independent coincidence and
frequency-profile scores. This second stage retains each observed coordinate,
including the known half of any erasure pair. No source glyph is changed.
Results are search candidates, not automatically accepted decipherments.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time

from cipher import decrypt, untranspose

ROOT=Path(__file__).resolve().parent.parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workers',type=int,default=2)
    parser.add_argument('--restarts',type=int,default=1000)
    parser.add_argument('--iterations',type=int,default=60000)
    parser.add_argument('--limit',type=int,default=0)
    parser.add_argument('--reverse',action='store_true',help='Resume unfinished cases in reverse order')
    args=parser.parse_args()
    output=ROOT/'results/dictionary_permutation_fits';output.mkdir(exist_ok=True)
    jobs=[]
    for target in ['p73','p170']:
        source=ROOT.parent/'alternative_attack/dictionary'/f'{target}_top20_per_width.json'
        data=json.loads(source.read_text())
        ciphertext=data.get('ciphertext',data.get('ciphertexts'))
        if isinstance(ciphertext,list):assert len(ciphertext)==1;ciphertext=ciphertext[0]
        if not isinstance(ciphertext,str):
            raise ValueError(f'Unrecognized ciphertext field in {source}: {list(data)}')
        unique={}
        for candidate in data['candidates']:
            key=tuple(candidate['ranks'])
            item=unique.setdefault(key,{'id':target,'ciphertext':ciphertext,'ranks':list(key),
                       'selection_records':[],'source_file':str(source.relative_to(ROOT.parent))})
            item['selection_records'].append({k:v for k,v in candidate.items() if k not in ['ranks','cells']})
        for item in unique.values():
            item['priority']=min(x['rank'] for x in item['selection_records'])
            item['interim']=untranspose(ciphertext,item['ranks'])
            item['label']=target+'__'+hashlib.sha256(json.dumps(item['ranks']).encode()).hexdigest()[:16]
            jobs.append(item)
    jobs.sort(key=lambda x:(x['priority'],len(x['ranks']),x['id']))
    if args.reverse:jobs.reverse()
    if args.limit:jobs=jobs[:args.limit]
    manifest={'cases':len(jobs),'restarts_per_case':args.restarts,'iterations_per_restart':args.iterations,
              'model':'data/military_models/german_military36_quad.bin',
              'observed_ciphertext_changes':0,'solver':'marginal_subsolve.c',
              'classification_policy':'No decipherment is accepted by an objective threshold alone.'}
    (output/'RUN.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'starting_cases':len(jobs),**manifest}),flush=True)

    def run(job):
        path=output/(job['label']+'.json')
        if path.exists():return json.loads(path.read_text())
        seed=int.from_bytes(hashlib.sha256(job['label'].encode()).digest()[:8],'little')
        cmd=[str(ROOT/'bin/marginal_subsolve'),str(ROOT/'data/military_models/german_military36_quad.bin'),
             job['interim'],str(args.restarts),str(args.iterations),str(seed)]
        start=time.time()
        result=subprocess.run(cmd,capture_output=True,text=True,check=True)
        (output/(job['label']+'.jsonl')).write_text(result.stdout)
        best=json.loads(result.stdout.splitlines()[-1])
        assert decrypt(job['ciphertext'],job['ranks'],best['square'])==best['plaintext']
        assert len(set(best['square']))==36
        record={**job,'best':best,'seconds':time.time()-start,'seed':seed,
                'restarts':args.restarts,'iterations_per_restart':args.iterations,
                'classification':'unvalidated_search_candidate'}
        path.write_text(json.dumps(record,indent=2))
        return record

    completed=[]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(run,job) for job in jobs]
        for future in as_completed(futures):
            row=future.result();completed.append(row)
            if len(completed)%20==0:
                print(json.dumps({'completed':len(completed),'total':len(jobs),'last':row['label'],
                                  'score':row['best']['score']}),flush=True)
    summary={**manifest,'results':[]}
    for target in ['p73','p170']:
        rows=sorted((r for r in completed if r['id']==target),key=lambda r:r['best']['score'],reverse=True)
        summary['results'].append({'id':target,'cases':len(rows),'top_candidates':rows[:30]})
    (output/'SUMMARY.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({'complete':True,'cases':len(completed)}),flush=True)


if __name__=='__main__':main()
