#!/usr/bin/env python3
"""Freeze completed search records with arithmetic and control evaluations.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Records count configured proposal slots separately from exact enumeration.
No language-ranked historical candidate is promoted to a decipherment.
"""
from pathlib import Path
import argparse,array,hashlib,itertools,json,math,sys
from run_gap import verify_record as verify_gap,MODEL_SHA,ROOT
from run_sparse import verify_record as verify_sparse
from run_transfer import verify as verify_transfer
from run_relabel import verify as verify_relabel,MODEL_SHA as MODEL37_SHA
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,decrypt,plaintext_domains
HERE=Path(__file__).resolve().parent


def domain_score(domains,model):
    total=0
    for at in range(len(domains)-3):
        ds=domains[at:at+4];mass=0
        for text in itertools.product(*ds):
            code=0
            for ch in text:code=36*code+ALPHABET.index(ch)
            mass+=10**model[code]
        total+=math.log10(mass/math.prod(map(len,ds)))
    return total/(len(domains)-3)


def evaluate(row,kind,model,model_path):
    if kind=='gap':check=verify_gap(row,True,model_path)
    elif kind=='sparse':check=verify_sparse(row,model_path)
    elif kind=='transfer':check=verify_transfer(row,model)
    elif kind=='relabel':check=verify_relabel(row,model)
    else:raise ValueError(kind)
    case=row['case']
    if 'evaluation_only'in case:
        ev=case['evaluation_only'];raw=case['ciphertext'];full=ev['full_ciphertext']
        control=check['control']
        if kind in ['gap','relabel','transfer']:
            size=case['gap_size']
            positions=[g for g in range(len(raw)+1)if full[:g]+full[g+size:]==raw] if size else [0]
            control['all_source_equivalent_true_gap_positions']=positions
        if kind=='sparse':
            losses=row['best']['missing_full_ciphertext_positions_0based']
            control['reported_losses_reproduce_source_under_true_key']=''.join(ch for i,ch in enumerate(full)if i not in losses)==raw
            missing=ev['missing_full_ciphertext_positions_0based']
            ct=''.join('?'if i in missing else ch for i,ch in enumerate(full))
            ds=plaintext_domains(ct,case['ranks'],ev['square'])
            control['planted_geometry_true_square_score']=domain_score(ds,model)
            control['reported_minus_planted_score']=row['best']['score']-control['planted_geometry_true_square_score']
        if kind=='gap':
            gap=ev['gap_before_source_0based'];ct=raw[:gap]+'?'*case['gap_size']+raw[gap:]
            control['planted_geometry_true_square_score']=domain_score(plaintext_domains(ct,ev['ranks'],ev['square']),model)
            control['reported_minus_planted_score']=row['best']['score']-control['planted_geometry_true_square_score']
    return check


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kind',required=True,choices=['gap','sparse','transfer','relabel'])
    p.add_argument('--input',type=Path,action='append',default=[])
    p.add_argument('--model',type=Path,required=True)
    p.add_argument('--output',type=Path)
    p.add_argument('--verify',type=Path)
    args=p.parse_args()
    if not args.verify and not args.output:p.error('--output is required when collecting records')
    wanted=MODEL37_SHA if args.kind=='relabel'else MODEL_SHA
    assert hashlib.sha256(args.model.read_bytes()).hexdigest()==wanted
    model=array.array('f');model.frombytes(args.model.read_bytes())
    if sys.byteorder=='big':model.byteswap()
    if args.verify:
        snapshot=json.loads(args.verify.read_text());assert snapshot['kind']==args.kind
        for row in snapshot['records']:assert evaluate(row,args.kind,model,args.model)==row['audit']
        print(json.dumps(dict(verified=True,kind=args.kind,completed_records=len(snapshot['records']),summary=snapshot['summary']),indent=2));return
    records=[];seen=set()
    for folder in args.input:
        for path in sorted(folder.glob('*.json')):
            raw=path.read_bytes();row=json.loads(raw)
            if not isinstance(row,dict)or'case'not in row or'recipe'not in row:continue
            identity=(row['case']['id'],json.dumps(row['recipe'],sort_keys=True))
            assert identity not in seen,(folder,path);seen.add(identity)
            row['input_record_sha256']=hashlib.sha256(raw).hexdigest()
            row['audit']=evaluate(row,args.kind,model,args.model);records.append(row)
    historical=[r for r in records if'evaluation_only'not in r['case']]
    controls=[r for r in records if'evaluation_only'in r['case']]
    summary=dict(completed_historical_runs=len(historical),unique_historical_cases=len({r['case']['id']for r in historical}),completed_controls=len(controls),accepted_historical_plaintexts=0,
        historical_configured_proposal_slots=sum(r['recipe'].get('restarts',0)*r['recipe'].get('iterations',0)for r in historical),
        historical_exact_evaluations=sum(r.get('summary',{}).get('evaluations',0)for r in historical),
        control_evaluations=[dict(id=r['case']['id'],evaluation=r['audit']['control'])for r in controls])
    snapshot=dict(project='ADFGVX Cipher',review_credit='icekylinx and GPT-6 Astra Pro',kind=args.kind,model_sha256=wanted,summary=summary,records=records,
        limitation='Search budgets and arithmetic are verified; stochastic completion is not exhaustion, and a ranked candidate is not a recovered historical plaintext.')
    args.output.write_text(json.dumps(snapshot,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
