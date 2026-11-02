#!/usr/bin/env python3
"""Enumerate distinct row/column relabelings beyond the prior common-label screen.
ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
"""
from pathlib import Path
import argparse,array,concurrent.futures,hashlib,json,math,random,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,encrypt,decrypt,plaintext_domains
COORDS='ADFGVX';HERE=Path(__file__).resolve().parent
MODEL_SHA='2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e'


def inputs():
    keys=json.loads((ROOT/'data/keys.json').read_text())['keys']
    messages={m['id']:m for m in json.loads((ROOT/'data/messages.json').read_text())['messages']}
    rows=[]
    for message in ['p73','p170','p198']:
        for key in keys:
            if 36-key['square'].count('?')<19:continue
            rows.append(dict(id=f'{message}__{key["id"]}',target=message,key_id=key['id'],partial_square=key['square'],ranks=key['column_rank_order'],ciphertext=messages[message]['transcript']['analysis_ciphertext'],gap_size=5 if message=='p198' else 0))
    key=next(k for k in keys if k['id']=='Nov13-15b')
    body='DERSTABMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEWEITEREBEFEHLEUEBERMITTELNXABX'
    rng=random.Random(20261102)
    for target,length,swap in [('p73',89,False),('p170',53,True),('p198',85,True)]:
        rp=list(COORDS);cp=list(COORDS);rng.shuffle(rp);rng.shuffle(cp)
        remaining=iter(sorted(set(ALPHABET)-set(key['square'])))
        full=''.join(next(remaining) if c=='?' else c for c in key['square'])
        effective=''.join(full[6*COORDS.index(rp[b if swap else a])+COORDS.index(cp[a if swap else b])] for a in range(6) for b in range(6))
        truebody=body[:length];ct=encrypt(truebody,key['column_rank_order'],effective);fullct=ct
        if target=='p73':ct=ct[:1]+'??'+ct[3:]
        gap=71 if target=='p198' else 0
        if target=='p198':ct=ct[:gap]+ct[gap+5:]
        rows.append(dict(id=f'control__{target}',target='synthetic',key_id=key['id'],partial_square=key['square'],ranks=key['column_rank_order'],ciphertext=ct,gap_size=5 if target=='p198' else 0,
                         evaluation_only=dict(plaintext=truebody,row_relabeling=''.join(rp),column_relabeling=''.join(cp),swapped_pair_orientation=swap,gap=gap,full_ciphertext=fullct)))
    return rows


def verify(row,model):
    case=row['case'];best=row['candidates'][0]
    for candidate in row['candidates']:
        rp,cp=candidate['row_relabeling'],candidate['column_relabeling'];swap=candidate['swapped_pair_orientation']
        assert sorted(rp)==sorted(cp)==sorted(COORDS)
        square=''.join(case['partial_square'][6*COORDS.index(rp[b if swap else a])+COORDS.index(cp[a if swap else b])] for a in range(6) for b in range(6))
        assert square==candidate['effective_partial_square']
        gap=candidate['gap_before_source_0based'];ct=case['ciphertext'][:gap]+'?'*case['gap_size']+case['ciphertext'][gap:]
        pt=decrypt(ct,case['ranks'],square)
        assert pt==candidate['partial_plaintext']
        domains=plaintext_domains(ct,case['ranks'],square)
        assert all(ch=='?' or d==ch for ch,d in zip(pt,domains))
        score=0
        for i in range(len(pt)-3):
            code=0;wild=0
            for ch in pt[i:i+4]:code=37*code+(36 if ch=='?' else ALPHABET.index(ch));wild+=ch=='?'
            score+=model[code]-wild*math.log10(36)
        score/=len(pt)-3
        assert abs(score-candidate['score'])<2e-6,(score,candidate['score'])
    gaps=list(range(0,len(case['ciphertext'])+1,row['recipe']['gap_step'])) if case['gap_size'] else [0]
    assert row['summary']['evaluations']==len(gaps)*2*720*720
    result=dict(all_retained_candidates_arithmetic_verified=True,evaluations=row['summary']['evaluations'],source_coordinates_unchanged=True,accepted_historical_plaintext=False)
    if 'evaluation_only' in case:
        ev=case['evaluation_only'];gap=best['gap_before_source_0based'];ct=case['ciphertext'][:gap]+'?'*case['gap_size']+case['ciphertext'][gap:]
        ds=plaintext_domains(ct,case['ranks'],best['effective_partial_square'])
        result['control']=dict(truth_in_all_domains=all(ch in d for ch,d in zip(ev['plaintext'],ds)),correct_singletons=sum(d==ch for ch,d in zip(ev['plaintext'],ds)),singleton_positions=sum(len(d)==1 for d in ds),exact_relabelings=all(best[k]==ev[k] for k in ['row_relabeling','column_relabeling','swapped_pair_orientation']),recovered_gap=gap,planted_gap=ev['gap'])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--engine',type=Path,default=HERE/'bin/relabel_rows_columns');p.add_argument('--model',type=Path,default=Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin'));p.add_argument('--output',type=Path,default=Path('/tmp/adfgvx-relabel-results'));p.add_argument('--controls',action='store_true');p.add_argument('--only',default='*');p.add_argument('--workers',type=int,default=1);p.add_argument('--gap-step',type=int,default=1);p.add_argument('--keep',type=int,default=20);p.add_argument('--verify',type=Path)
    args=p.parse_args();import fnmatch
    assert hashlib.sha256(args.model.read_bytes()).hexdigest()==MODEL_SHA
    model=array.array('f');model.frombytes(args.model.read_bytes())
    if sys.byteorder=='big':model.byteswap()
    if args.verify:print(json.dumps(verify(json.loads(args.verify.read_text()),model),indent=2));return
    cases=[c for c in inputs() if ('evaluation_only'in c)==args.controls and fnmatch.fnmatch(c['id'],args.only)]
    assert cases and args.workers>0 and args.gap_step>0 and 1<=args.keep<=100
    args.output.mkdir(parents=True,exist_ok=True)
    def run(case):
        path=args.output/(case['id']+'.json');recipe=dict(gap_step=args.gap_step,keep=args.keep,model_sha256=MODEL_SHA,source_sha256=hashlib.sha256((HERE/'relabel_rows_columns.c').read_bytes()).hexdigest(),engine_sha256=hashlib.sha256(args.engine.read_bytes()).hexdigest())
        if path.exists():
            row=json.loads(path.read_text());assert row['recipe']==recipe and row['case']==case;verify(row,model);return row
        inp=f'{args.model.resolve()} {len(case["ranks"])} {case["gap_size"]} {args.gap_step} {args.keep}\n'+case['partial_square']+'\n'+' '.join(map(str,case['ranks']))+'\n'+case['ciphertext']+'\n'
        start=time.monotonic();p=subprocess.run([str(args.engine.resolve())],input=inp,text=True,capture_output=True,check=True)
        records=[json.loads(line)for line in p.stdout.splitlines()]
        row=dict(case=case,recipe=recipe,candidates=records[:-1],summary=records[-1],elapsed_seconds=time.monotonic()-start);row['verification']=verify(row,model)
        path.write_text(json.dumps(row,indent=2)+'\n');return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers)as pool:
        for row in pool.map(run,cases):print(json.dumps(dict(id=row['case']['id'],best=row['candidates'][0],verification=row['verification'])),flush=True)

if __name__=='__main__':main()
