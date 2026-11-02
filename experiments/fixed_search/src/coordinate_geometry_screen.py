"""Enumerate coordinate relabelings and route conventions without source edits.
All 720 common permutations of ADFGVX and both pair orientations are tested.
Rank conventions: normal/inverse; optional physical-column mirror, descending
read order, and reversal within each column. p198 has an explicit five-slot gap.
N-gram scores only rank candidates; no score threshold certifies plaintext.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,time
import numpy as np
S='ADFGVX';A='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
P=np.asarray(list(itertools.permutations(range(6))),dtype=np.int16)

def routes(n,r):
 k=len(r);inv=[r.index(i+1)+1 for i in range(k)];seen=set()
 for convention,base in [('normal',r),('inverse',inv)]:
  for mirror in [False,True]:
   ranks=base[::-1] if mirror else base[:]
   for descending in [False,True]:
    order=sorted(range(k),key=ranks.__getitem__,reverse=descending)
    for revcol in [False,True]:
     ix=[]
     for col in order:
      z=list(range(col,n,k));ix.extend(z[::-1] if revcol else z)
     if tuple(ix) in seen:continue
     seen.add(tuple(ix))
     yield np.asarray(ix),dict(rank_convention=convention,mirror_columns=mirror,descending_read_order=descending,reverse_each_column=revcol)

def score(ct,sq,ix,q,swap):
 c=np.asarray([S.find(x) for x in ct],dtype=np.int16);u=np.empty(len(c),dtype=np.int16);u[ix]=c
 a,b=u[::2],u[1::2]
 if swap:a,b=b,a
 missing=(a<0)|(b<0);cells=6*P[:,np.maximum(a,0)]+P[:,np.maximum(b,0)]
 table=np.asarray([A.find(x) for x in sq],dtype=np.int16);pt=table[cells];pt[:,missing]=-1
 valid=(pt[:,:-3]>=0)&(pt[:,1:-2]>=0)&(pt[:,2:-1]>=0)&(pt[:,3:]>=0)
 safe=np.maximum(pt.astype(np.int32),0);idx=((safe[:,:-3]*36+safe[:,1:-2])*36+safe[:,2:-1])*36+safe[:,3:]
 scores=np.where(valid,q[idx],-7.4).mean(axis=1);best=int(scores.argmax())
 return dict(score=float(scores[best]),plaintext=''.join(A[x] if x>=0 else '?' for x in pt[best]),coordinate_relabeling=''.join(S[int(x)] for x in P[best]),swapped_pair_orientation=swap,known_quadgram_windows=int(valid[best].sum()),total_quadgram_windows=int(valid.shape[1]))

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repository',type=Path,required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 q=np.fromfile(args.model,dtype='<f4');assert len(q)==36**4
 keys=[k for k in json.loads((args.repository/'data/keys.json').read_text())['keys'] if k['square'].count('?')<36]
 key=next(k for k in keys if k['id']=='Nov1-3');plain='ANXDASXOBERKOMMANDOXMELDUNGXUEBERXDENXMARSCHXDERXTRUPPENXUNDXDENXZUSTANDXDERXBAHNSTRECKEX'
 stream=''.join(S[key['square'].index(c)//6]+S[key['square'].index(c)%6] for c in plain)
 ix,route=next((ix,m) for ix,m in routes(len(stream),key['column_rank_order']) if m['rank_convention']=='inverse' and m['reverse_each_column'])
 change=dict(zip(S,'FXAVDG'));ct=''.join(change[stream[int(i)]] for i in ix)
 control=dict(id='synthetic_route_relabel_control',ciphertext=ct,expected_plaintext=plain,construction_key=key['id'],construction_route=route)
 jobs=[control]
 for m in json.loads((args.repository/'data/messages.json').read_text())['messages']:
  if m['id'] not in ['p73','p153a','p153b','p170','p198']:continue
  ct=m['transcript']['analysis_ciphertext']
  if m['id']=='p198':
   jobs.extend(dict(id=m['id'],ciphertext=ct[:g]+'?????'+ct[g:],gap_position=g) for g in range(0,166,5))
  else:jobs.append(dict(id=m['id'],ciphertext=ct))
 records={};evaluations=0;start=time.time()
 for job in jobs:
  ct=job['ciphertext'];assert len(ct)%2==0;hits=[]
  for key in keys:
   for ix,route in routes(len(ct),key['column_rank_order']):
    for swapped in [False,True]:
     z=score(ct,key['square'],ix,q,swapped);evaluations+=len(P);hits.append(dict(**z,key_id=key['id'],route=route,gap_position=job.get('gap_position')))
  rows=records.setdefault(job['id'],[]);rows.extend(sorted(hits,key=lambda x:x['score'],reverse=True)[:30]);rows.sort(key=lambda x:x['score'],reverse=True);del rows[50:]
  print(json.dumps(dict(completed=job['id'],gap=job.get('gap_position'),best_score=rows[0]['score'],evaluated_hypotheses=evaluations)),flush=True)
  if job['id']==control['id']:assert rows[0]['plaintext']==plain,'Positive control failed'
 output=dict(scope=__doc__,evaluated_hypotheses=evaluations,keys=len(keys),input_variants=len(jobs),seconds=time.time()-start,model_sha256=hashlib.sha256(args.model.read_bytes()).hexdigest(),unknown_window_score=-7.4,control=control,control_recovered_at_rank_one=True,results=records,classification='Unvalidated ranked candidates; historical verification is required.')
 args.output.write_text(json.dumps(output,indent=2)+'\n')
if __name__=='__main__':main()
