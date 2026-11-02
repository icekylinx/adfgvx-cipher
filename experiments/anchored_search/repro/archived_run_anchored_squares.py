"""Search arbitrary column orders while retaining historical square cells.

This is a bounded component-reuse hypothesis. The wildcard objective discards
known half-coordinates only in language scoring; reported constraints restore
the exact domains. Controls are invented and are used only for evaluation.
"""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, random, subprocess, time

BASE=Path(__file__).resolve().parents[3]
REPO=BASE/'adfgvx-cipher'
ROOT=BASE/'adfgvx1918/root_attack'
ENGINE=REPO/'experiments/joint_search/bin/anchored_joint'
MODEL=BASE/'adfgvx1918/alternative_attack/models/german_military37_quad_marginal.bin'
import sys
sys.path.insert(0,str(REPO))
from adfgvx.cipher import encrypt, decrypt, plaintext_domains
AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def cases(controls):
    keys={k['id']:k for k in json.loads((REPO/'data/keys.json').read_text())['keys']}
    if controls:
        specifications=[('control_89','Nov7-9',20,89,'DIEKOLONNEMARSCHIERTMORGENFRUEHWEITERXBITTEVERPFLEGUNGFUERDIEMANNSCHAFTBEREITHALTENX', [1,2]),
                        ('control_53','Nov1-3',19,53,'DERZUGTRIFFTMORGENMITTAGAMBAHNHOFANXBITTEWARTENX', [])]
        out=[]
        for name,kid,width,length,body,erased in specifications:
            assert len(body)<=length
            body=body+'X'*(length-len(body))
            square=keys[kid]['square'];remaining=iter(c for c in AL if c not in square)
            fullsquare=''.join(next(remaining) if c=='?' else c for c in square)
            ranks=list(range(1,width+1));random.Random(2026110200+length).shuffle(ranks)
            complete=encrypt(body,ranks,fullsquare);received=list(complete)
            for i in erased:received[i]='?'
            out.append(dict(id=name,key_id=kid,width=width,partial_square=square,ciphertext=''.join(received),
                            evaluation_only=dict(plaintext=body,ranks=ranks,square=fullsquare,full_ciphertext=complete)))
        return out
    messages={m['id']:m for m in json.loads((REPO/'data/messages.json').read_text())['messages']}
    out=[]
    for mid in ['p73','p170']:
        for kid in ['Oct28-31','Nov1-3','Nov4-6','Nov7-9','Nov10-12']:
            for width in range(16,23):
                out.append(dict(id=mid,key_id=kid,width=width,partial_square=keys[kid]['square'],
                                ciphertext=messages[mid]['transcript']['analysis_ciphertext']))
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--controls',action='store_true');p.add_argument('--workers',type=int,default=2)
    p.add_argument('--restarts',type=int,default=100);p.add_argument('--iterations',type=int,default=50000)
    p.add_argument('--wait-for-domain',action='store_true')
    args=p.parse_args()
    if args.wait_for_domain:
        while len(list((ROOT/'results/p198_domain_refinement').glob('p198__*.json')))<136:time.sleep(15)
    out=ROOT/'results/anchored_square_search';out.mkdir(exist_ok=True)
    provenance={str(x.relative_to(BASE)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [ENGINE,MODEL,Path(__file__)]}
    def run(case):
        label=f"{case['id']}__{case['key_id']}__k{case['width']:02d}__r{args.restarts}i{args.iterations}"
        path=out/(label+'.json')
        if path.exists():return json.loads(path.read_text())
        seed=int(hashlib.sha256(label.encode()).hexdigest()[:15],16)
        lines=[f'{MODEL} {case["width"]} {args.restarts} {args.iterations} {seed} 1',case['partial_square'],
               ' '.join(['0']*case['width']),case['ciphertext']]
        start=time.time();r=subprocess.run([str(ENGINE)],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
        (out/(label+'.jsonl')).write_text(r.stdout)
        rows=[json.loads(line) for line in r.stdout.splitlines() if line.startswith('{')];best=max(rows,key=lambda r:r['score'])
        assert decrypt(case['ciphertext'],best['ranks'],best['square'])==best['plaintexts'][0]
        assert all(a=='?' or a==b for a,b in zip(case['partial_square'],best['square']))
        domains=plaintext_domains(case['ciphertext'],best['ranks'],best['square'])
        record=dict(case=case,best=best,domains=domains,requested_restarts=args.restarts,
                    iterations_per_restart=args.iterations,seed=seed,elapsed_seconds=time.time()-start,
                    model='Whole-cell wildcard marginal quadgrams; exact domains restored after ranking',
                    provenance=provenance,accepted_historical_plaintext=False)
        if 'evaluation_only' in case:
            truth=case['evaluation_only']['plaintext'];plain=best['plaintexts'][0]
            predicted=encrypt(truth,best['ranks'],best['square'])
            record['control_evaluation']={'fully_observed_plaintext_positions':sum(c!='?' for c in plain),
                 'correct_fully_observed_positions':sum(c!='?' and c==t for c,t in zip(plain,truth)),
                 'observed_coordinates':sum(c!='?' for c in case['ciphertext']),
                 'compatible_observed_coordinates':sum(c!='?' and c==p for c,p in zip(case['ciphertext'],predicted)),
                 'true_plaintext_in_every_domain':all(t in d for t,d in zip(truth,domains)),
                 'truth_was_not_supplied_to_search':True}
        path.write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps({'label':label,'score':best['score'],'elapsed_seconds':record['elapsed_seconds'],
                          'plaintext':best['plaintexts'][0],'control':record.get('control_evaluation')}),flush=True)
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:rows=list(pool.map(run,cases(args.controls)))
    print(json.dumps({'completed':len(rows),'controls':args.controls,'accepted_historical_plaintexts':0}),flush=True)

if __name__=='__main__':main()
