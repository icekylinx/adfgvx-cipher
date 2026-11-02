#!/usr/bin/env python3
"""Calibrate scattered-loss search with a wholly unknown substitution square.
ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Only published ranks are supplied; control plaintext and square are evaluation
metadata, never optimization inputs. A failed control prevents historical
exclusion claims from this branch.
"""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess,time
from run_sparse import verify_record
from run_gap import MODEL_SHA,digest
HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=HERE/'sparse_results.json')
    p.add_argument('--control',default='control__CHI-Nov13')
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--model',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--restarts',type=int,default=1000)
    p.add_argument('--iterations',type=int,default=100000)
    args=p.parse_args()
    assert digest(args.model)==MODEL_SHA and args.restarts>0 and args.iterations>0
    original=next(r for r in json.loads(args.input.read_text())['records']if r['case']['id']==args.control)
    case=copy.deepcopy(original['case']);case['id']='unknown_square__'+case['id'];case['partial_square']='?'*36
    seed=int(hashlib.sha256(case['id'].encode()).hexdigest()[:15],16)
    recipe=dict(restarts=args.restarts,iterations=args.iterations,seed=seed,model_sha256=MODEL_SHA,source_sha256=digest(HERE/'sparse_loss.c'),shared_scorer_sha256=digest(HERE/'gap_anchored.c'),engine_sha256=digest(args.engine),input_record_sha256=original['input_record_sha256'])
    text=f'{args.model.resolve()} {len(case["ranks"])} {args.restarts} {args.iterations} {seed} 5\n'+case['partial_square']+'\n'+' '.join(map(str,case['ranks']))+'\n'+case['ciphertext']+'\n'
    start=time.monotonic();run=subprocess.run([str(args.engine.resolve())],input=text,text=True,capture_output=True,check=True)
    row=dict(case=case,recipe=recipe,best=json.loads(run.stdout.splitlines()[-1]),elapsed_seconds=time.monotonic()-start)
    row['verification']=verify_record(row,args.model)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(row,indent=2)+'\n');args.output.with_suffix('.jsonl').write_text(run.stdout)
    print(json.dumps(dict(id=case['id'],best=row['best'],verification={k:v for k,v in row['verification'].items()if k!='plaintext_domains'}),indent=2))

if __name__=='__main__':main()
