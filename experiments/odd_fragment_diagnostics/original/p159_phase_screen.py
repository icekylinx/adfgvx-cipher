import json,sys,hashlib
from pathlib import Path
import numpy as np
R=Path('/workspace/scratch/b45c8ddf3b25/adfgvx-cipher');CO='ADFGVX';AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?'
first=json.loads(Path('/tmp/adfgvx-post-push-root/p159/one_insert_all_keys.json').read_text());source=first['literal_source'];base=np.array([CO.index(c)for c in source],dtype=np.int16);keys=json.loads((R/'data/keys.json').read_text())['keys'];model=Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin');quad=np.fromfile(model,dtype='<f4');runs=[]
def perm(n,ranks):
 w=len(ranks);hs=[(n-i+w-1)//w for i in range(w)];st=[sum(hs[j]for j in range(w)if ranks[j]<ranks[i])for i in range(w)];return np.array([st[i%w]+i//w for i in range(n)])
def rank(frames,key,kind,mult):
 sq=np.array([AL.index(c)for c in key['square']],dtype=np.int32);plain=sq[frames[:,::2]*6+frames[:,1::2]];valid=(plain[:,:-3]<36)&(plain[:,1:-2]<36)&(plain[:,2:-1]<36)&(plain[:,3:]<36);cov=valid.sum(axis=1);idx=((plain[:,:-3]*37+plain[:,1:-2])*37+plain[:,2:-1])*37+plain[:,3:];sm=np.where(valid,quad[idx],0).sum(axis=1,dtype=np.float64);scores=np.divide(sm,cov,out=np.full(len(frames),-100.),where=cov>0);scores=np.where(cov>=100,scores,-100.)
 order=np.argsort(scores)[-5:][::-1];out=[]
 for i in order:out.append({'key_id':key['id'],'kind':kind,'index':int(i)//mult,'fill':CO[int(i)%6]if mult==6 else None,'score':float(scores[i]),'known_quad_windows':int(cov[i]),'eligible':bool(cov[i]>=100),'plaintext':''.join(AL[int(c)]for c in plain[i])})
 return {'key_id':key['id'],'kind':kind,'evaluations':len(frames),'top':out}
for key in keys:
 ranks=key['column_rank_order'];mid=base[perm(len(base),ranks)]
 ins=np.stack([np.insert(mid,p,c)for p in range(272)for c in range(6)]);runs.append(rank(ins,key,'insert_fractionated',6))
 dele=np.stack([np.delete(mid,p)for p in range(271)]);runs.append(rank(dele,key,'delete_fractionated',1))
 trans=np.stack([np.delete(base,p)for p in range(271)]);trans=trans[:,perm(270,ranks)];runs.append(rank(trans,key,'delete_transmitted',1))
top=sorted([x for r in runs for x in r['top']if x['eligible']],key=lambda x:-x['score'])[:30];out={'schema':'p159-bounded-phase-diagnostic-v1','literal_source':source,'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'ranking_rule':'Mean over at least100 fully known four-grams; missing-key windows excluded and low-coverage keys unranked. Scores are diagnostics, not historical proof.','runs':runs,'total_evaluations':sum(r['evaluations']for r in runs),'top':top};Path('/tmp/adfgvx-post-push-root/p159/phase_screen.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'evaluations':out['total_evaluations'],'top':top[:12]},indent=2))
