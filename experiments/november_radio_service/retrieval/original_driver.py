from pathlib import Path
import json,sys,subprocess,time,hashlib
sys.path.insert(0,'/workspace/scratch/b45c8ddf3b25/adfgvx-cipher/experiments/p198_pretransposition_loss')
from run import inverse,decode,score
from array import array
root=Path('/workspace/scratch/b45c8ddf3b25/adfgvx-cipher')
source=Path('/tmp/corpus-harvest-screen-initial.json');rows=json.loads(source.read_text())['rows'];keys={k['id']:k for k in json.loads((root/'data/keys.json').read_text())['keys']}
models={'book':Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin'),'radio':Path('/tmp/adfgvx-radio-model/radio_book37_quad_marginal.bin')};arrays={}
for name,path in models.items():
 v=array('f');v.frombytes(path.read_bytes());arrays[name]=v
engine=Path('/tmp/adfgvx-pretransposition-loss/interim_dp');out=Path('/tmp/adfgvx-pretransposition-loss/odd_block_screen.json');results=[];start=time.time()
odd=[r for r in rows if r['source_slots']%2 and 55<=r['source_slots']<=700]
for ri,r in enumerate(odd):
 cipher=r['ciphertext'];ids=list(dict.fromkeys([r['best']['key'],r['runner_up']['key']]))
 for keyid in ids:
  key=keys[keyid];stream,_=inverse(cipher,key['column_rank_order']);raw=decode(stream[:-1],key['square'])
  for name,path in models.items():
   result=json.loads(subprocess.run([str(engine),str(path),key['square'],'1',stream],text=True,capture_output=True,check=True).stdout)
   p=result['plaintext'];results.append({'block_id':r['block_id'],'printed_page':r['printed_page'],'source_slots':len(cipher),'key_id':keyid,'model':name,'ciphertext':cipher,'source_erasures':cipher.count('?'),'unmodified_raw':raw,'unpaired_coordinate':stream[-1],'baseline_mean':score(raw,arrays[name])/(len(raw)-3),'result':result,'fixed_label_fraction':1-p.count('?')/len(p)})
 if (ri+1)%25==0:print('completed blocks',ri+1,'jobs',len(results),'seconds',round(time.time()-start,2),flush=True)
output={'schema':'adfgvx-odd-OCR-one-interim-loss-screen-v1','prepared_by':['icekylinx','GPT-6 Astra Pro'],'input_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'Odd OCR blocks55..700 slots, best and runner-up keys from the frozen initial screen, both existing models, one interim insertion. All are unreviewed OCR candidates, not source recoveries.','blocks':len(odd),'completed_jobs':len(results),'elapsed_seconds':time.time()-start,'results':results}
out.write_text(json.dumps(output,indent=2)+'\n')
print('saved',out,'jobs',len(results),'seconds',time.time()-start,flush=True)
for r in sorted([r for r in results if r['fixed_label_fraction']>=0.85],key=lambda r:r['result']['score_mean']-r['baseline_mean'],reverse=True)[:35]:
 print(r['block_id'],r['key_id'],r['model'],round(r['result']['score_mean'],2),'gain',round(r['result']['score_mean']-r['baseline_mean'],2),r['result']['missing_interim_indices'],r['result']['plaintext'],flush=True)
