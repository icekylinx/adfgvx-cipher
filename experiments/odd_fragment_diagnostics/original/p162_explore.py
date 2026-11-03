import json,sys,itertools
from pathlib import Path
import numpy as np
from rows import ROWS
R=Path('/workspace/scratch/b45c8ddf3b25/adfgvx-cipher');sys.path.insert(0,str(R));from adfgvx.cipher import decrypt,plaintext_domains
k=next(k for k in json.loads((R/'data/keys.json').read_text())['keys']if k['id']=='Nov7-9');CO='ADFGVX';AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?';q=np.fromfile('/tmp/adfgvx-models/german_military37_quad_marginal.bin',dtype='<f4')
def inspect(s):
 p=decrypt(s,k['column_rank_order'],k['square']);return {'plaintext':p,'domains':[{'position':i,'domain':d}for i,d in enumerate(plaintext_domains(s,k['column_rank_order'],k['square']))if len(d)!=1]}
def score(p):
 a=np.array([AL.index(c)for c in p]);v=(a[:-3]<36)&(a[1:-2]<36)&(a[2:-1]<36)&(a[3:]<36);idx=((a[:-3]*37+a[1:-2])*37+a[2:-1])*37+a[3:];return float(q[idx[v]].mean(dtype=np.float64))if v.sum()>=12 else-100.,int(v.sum())
for ident,rows in ROWS.items():
 literal=''.join(rows.split());s=''.join(c if c in CO else'?'for c in literal);print(ident,len(s),[(i,c)for i,c in enumerate(literal)if c not in CO])
 if len(s)%2==0:print(json.dumps(inspect(s)))
 if ident=='p162_B1':
  for pos in range(5):print(pos,json.dumps(inspect(s[:pos]+'?'+s[pos:])))
 if ident=='p162_C1':
  out=[]
  for gap in range(1,102,2):
   for end in ['prefix','suffix']:
    f='?'*gap+s if end=='prefix'else s+'?'*gap;p=inspect(f)['plaintext'];sc,n=score(p);out.append({'gap':gap,'end':end,'score':sc,'known_windows':n,**inspect(f)})
  out.sort(key=lambda r:-r['score']);Path('/tmp/adfgvx-post-push-root/p162/C1_prefix_suffix.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out[:8],indent=2))
# Same bounded prefix diagnostic for the earlier published jammed source fragment.
d=json.loads((R/'experiments/withdrawal_recovery/inputs.json').read_text());r=next(r for r in d['records']if r['id']=='p163_A_unlabelled');s=''.join(''.join(r['source_rows']).split());out=[]
for gap in range(1,102,2):
 for end in ['prefix','suffix']:
  f='?'*gap+s if end=='prefix'else s+'?'*gap;p=inspect(f)['plaintext'];sc,n=score(p);out.append({'gap':gap,'end':end,'score':sc,'known_windows':n,**inspect(f)})
out.sort(key=lambda r:-r['score']);Path('/tmp/adfgvx-post-push-root/p162/p163_prefix_suffix.json').write_text(json.dumps(out,indent=2)+'\n');print('p163 jammed',json.dumps(out[:6],indent=2))
