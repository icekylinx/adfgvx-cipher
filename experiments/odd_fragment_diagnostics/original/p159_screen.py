import ast,json,hashlib,sys
from pathlib import Path
import numpy as np
R=Path('/workspace/scratch/b45c8ddf3b25/adfgvx-cipher');sys.path.insert(0,str(R));from adfgvx.cipher import decrypt
# Read the already source-transcribed literal, without importing exploratory code.
tree=ast.parse(Path('/tmp/adfgvx-post-push-root/p160/rows.py').read_text());literal=None
for n in tree.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and ast.literal_eval(n.targets[0].slice)=='p159_A':literal=''.join(ast.literal_eval(n.value).split())
assert literal and len(literal)==271 and set(literal)<=set('ADFGVX')
CO='ADFGVX';AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?';model=Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin');quad=np.fromfile(model,dtype='<f4');keys=json.loads((R/'data/keys.json').read_text())['keys'];base=np.array([CO.index(c)for c in literal],dtype=np.int16)
frames=np.stack([np.insert(base,p,c)for p in range(272)for c in range(6)]);runs=[];N=272
for key in keys:
 ranks=key['column_rank_order'];w=len(ranks);heights=[(N-i+w-1)//w for i in range(w)];starts=[sum(heights[j]for j in range(w)if ranks[j]<ranks[i])for i in range(w)];perm=np.array([starts[i%w]+i//w for i in range(N)])
 middle=frames[:,perm];square=np.array([AL.index(c)for c in key['square']],dtype=np.int32);plain=square[middle[:,::2]*6+middle[:,1::2]]
 idx=((plain[:,:-3]*37+plain[:,1:-2])*37+plain[:,2:-1])*37+plain[:,3:];valid=(plain[:,:-3]<36)&(plain[:,1:-2]<36)&(plain[:,2:-1]<36)&(plain[:,3:]<36);coverage=valid.sum(axis=1);summed=np.where(valid,quad[idx],0).sum(axis=1,dtype=np.float64);scores=np.divide(summed,coverage,out=np.full(len(frames),-100.0),where=coverage>0);scores=np.where(coverage>=100,scores,-100.0)
 order=np.argsort(scores)[-5:][::-1];top=[]
 for i in order:
  s=''.join(AL[int(c)]for c in plain[i]);ct=''.join(CO[int(c)]for c in frames[i]);assert decrypt(ct,ranks,key['square'])==s
  top.append({'key_id':key['id'],'insert_source_boundary':int(i)//6,'insert_value':CO[int(i)%6],'score':float(scores[i]),'known_quad_windows':int(coverage[i]),'eligible_for_ranking':bool(coverage[i]>=100),'plaintext':s})
 runs.append({'key_id':key['id'],'evaluations':len(frames),'top':top})
top=sorted([x for r in runs for x in r['top'] if x['eligible_for_ranking']],key=lambda x:-x['score'])[:30]
out={'schema':'p159-bounded-all-known-key-one-insertion-diagnostic','literal_source':literal,'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'frames_per_key':len(frames),'ranking_rule':'Only at least100 fully known four-gram windows eligible; unknown windows are excluded from the mean, and low-coverage keys remain recorded but unranked.','keys':len(keys),'total_evaluations':len(keys)*len(frames),'runs':runs,'top':top,'limit':'Exploratory language scores, not accepted source repair or unique plaintext. The literal source remains unchanged; all source boundaries and all six fill values are compared under each frozen published candidate key.'}
Path('/tmp/adfgvx-post-push-root/p159/one_insert_all_keys.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'evaluations':out['total_evaluations'],'top':top[:12]},indent=2))
