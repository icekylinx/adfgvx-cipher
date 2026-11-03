import json,importlib.util,itertools,hashlib
from array import array
from pathlib import Path
base=Path('/workspace/scratch/b45c8ddf3b25/adfgvx-cipher')
spec=importlib.util.spec_from_file_location('source_verify',base/'experiments/november_radio_service/verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
j=json.load(open('/tmp/adfgvx-radio-followup/p138_B_transcription.json'));k=j['key'];ranks=k['column_rank_order'];sq=k['square'];CO='ADFGVX';ABC='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?';models={};model_hashes={}
for name,path in [('book','/tmp/adfgvx-models/german_military37_quad_marginal.bin'),('radio','/tmp/adfgvx-radio-model/radio_book37_quad_marginal.bin')]:
 b=Path(path).read_bytes();a=array('f');a.frombytes(b);models[name]=a;model_hashes[name]=hashlib.sha256(b).hexdigest()
def labels(s):return ''.join(sq[6*CO.index(a)+CO.index(b)] for a,b in zip(s[::2],s[1::2]))
def score(s,m):
 ids=[ABC.index(c) for c in s];return sum(m[((a*37+b)*37+c)*37+d] for a,b,c,d in zip(ids,ids[1:],ids[2:],ids[3:]))/(len(s)-3)
rows=[]
for fill in CO:
 src=j['analysis_source'].replace('?',fill);interim,_=v.inverse(src,ranks)
 for stage,frame in [('transmitted',src),('interim',interim)]:
  for mode in ['insert','remove']:
   for pos in range(len(frame)+(mode=='insert')):
    for value in (CO if mode=='insert' else [frame[pos]]):
     changed=frame[:pos]+(value+frame[pos:] if mode=='insert' else frame[pos+1:])
     paired=v.inverse(changed,ranks)[0] if stage=='transmitted' else changed
     txt=labels(paired)
     rows.append({'stage':stage,'mode':mode,'position':pos,'value':value,'source_R_fill':fill,'plaintext':txt,'scores':{n:score(txt,m) for n,m in models.items()}})
for model in models:
 seen=set();print('\nMODEL',model)
 for r in sorted(rows,key=lambda r:-r['scores'][model]):
  if r['plaintext'] in seen:continue
  seen.add(r['plaintext']);print(r)
  if len(seen)==10:break
out={'source_sha256':hashlib.sha256(Path('/tmp/adfgvx-radio-followup/p138_B_transcription.json').read_bytes()).hexdigest(),'model_sha256':model_hashes,'candidates_completed':len(rows),'rows':rows};Path('/tmp/adfgvx-radio-followup/p138_B_one_coordinate_screen.json').write_text(json.dumps(out,indent=2)+'\n')
