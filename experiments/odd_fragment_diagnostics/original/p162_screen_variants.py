import json,sys,hashlib
from pathlib import Path
import numpy as np
from rows import ROWS
R=Path('/workspace/scratch/b45c8ddf3b25/adfgvx-cipher');CO='ADFGVX';AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?';keys=json.loads((R/'data/keys.json').read_text())['keys'];model=Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin');q=np.fromfile(model,dtype='<f4')
def perm(n,ranks):
 w=len(ranks);hs=[(n-i+w-1)//w for i in range(w)];st=[sum(hs[j]for j in range(w)if ranks[j]<ranks[i])for i in range(w)];return np.array([st[i%w]+i//w for i in range(n)])
def score_frames(fr,key,name,mult):
 sq=np.array([AL.index(c)for c in key['square']],dtype=np.int32);pl=sq[fr[:,::2]*6+fr[:,1::2]];known=(pl[:,:-3]<36)&(pl[:,1:-2]<36)&(pl[:,2:-1]<36)&(pl[:,3:]<36);cov=known.sum(axis=1);idx=((pl[:,:-3]*37+pl[:,1:-2])*37+pl[:,2:-1])*37+pl[:,3:];sums=np.where(known,q[idx],0).sum(axis=1,dtype=np.float64);score=np.divide(sums,cov,out=np.full(len(fr),-100.),where=cov>0);need=int((pl.shape[1]-3)*.75);score=np.where(cov>=need,score,-100.);order=np.argsort(score)[-5:][::-1]
 return {'key_id':key['id'],'kind':name,'evaluations':len(fr),'min_known_windows':need,'top':[{'key_id':key['id'],'kind':name,'boundary_or_index':int(i)//mult,'fill':CO[int(i)%6]if mult==6 else None,'score':float(score[i]),'known_windows':int(cov[i]),'eligible':bool(cov[i]>=need),'plaintext':''.join(AL[int(c)]for c in pl[i])}for i in order]}
sources={'p162_C1':''.join(ROWS['p162_C1'].split())};d=json.loads((R/'experiments/withdrawal_recovery/inputs.json').read_text());sources['p163_unlabelled']=''.join(''.join(next(x for x in d['records']if x['id']=='p163_A_unlabelled')['source_rows']).split())
for ident,s in sources.items():
 b=np.array([CO.index(c)for c in s],dtype=np.int16);n=len(b);ins=np.stack([np.insert(b,i,c)for i in range(n+1)for c in range(6)]);dele=np.stack([np.delete(b,i)for i in range(n)]);runs=[]
 for k in keys:
  p=perm(n,k['column_rank_order']);mid=b[p];mi=np.stack([np.insert(mid,i,c)for i in range(n+1)for c in range(6)]);md=np.stack([np.delete(mid,i)for i in range(n)])
  for fr,name,mult in [(ins[:,perm(n+1,k['column_rank_order'])],'insert_transmitted',6),(dele[:,perm(n-1,k['column_rank_order'])],'delete_transmitted',1),(mi,'insert_fractionated',6),(md,'delete_fractionated',1)]:runs.append(score_frames(fr,k,name,mult))
 top=sorted([x for r in runs for x in r['top']if x['eligible']],key=lambda x:-x['score'])[:40];out={'source_id':ident,'literal_source':s,'keys':len(keys),'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'ranking_rule':'Mean over fully known four-grams, at least75% windows required. Scores are diagnostics rather than acceptance or uniqueness evidence.','total_evaluations':sum(r['evaluations']for r in runs),'runs':runs,'top':top};Path('/tmp/adfgvx-post-push-root/p162/'+ident+'_four_models.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'id':ident,'evaluations':out['total_evaluations'],'top':top[:5]},indent=2))
