#!/usr/bin/env python3
"""Verify the untouched odd source and exhaust a limited parallel-copy model."""
import argparse,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R))
from adfgvx.cipher import decrypt,encrypt,untranspose
from experiments.romanian_pacification_consultation.verify import inspect,repair
C='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def native(s,key):
 n=len(s);ranks=key['column_rank_order'];w=len(ranks);columns=[[]for _ in ranks];at=0
 for c in sorted(range(w),key=lambda x:ranks[x]):
  length=n//w+(c<n%w);columns[c]=list(range(at,at+length));at+=length
 perm=[columns[c][r]for r in range((n+w-1)//w)for c in range(w)if r<len(columns[c])]
 mid=''.join(s[i]for i in perm);assert mid==untranspose(s,ranks)
 plain=''.join(key['square'][C.index(mid[i])*6+C.index(mid[i+1])]for i in range(0,n-1,2))
 assert plain==decrypt(s,ranks,key['square'],allow_unpaired=True)
 return {'source_slots':n,'raw':plain,'fixed_positions':len(plain)-plain.count('?'),'intermediate':mid,'intermediate_to_source_indices':perm,'unpaired_coordinate':{'value':mid[-1],'source_index':perm[-1],'intermediate_index':n-1},'silently_dropped_source_coordinate':False}
def build(pdf=None):
 d=json.loads((H/'inputs.json').read_text());k=d['key'];r=d['record'];assert k==next(x for x in json.loads((R/'data/keys.json').read_text())['keys']if x['id']=='Nov10-12')
 for name,h in d['prior_artifacts'].items():assert sha(H/name)==h
 for im in d['source_images']:assert sha(H/im['path'])==im['sha256']
 if pdf:
  import fitz
  from PIL import Image
  assert sha(pdf)==d['source']['pdf_sha256'] and pdf.stat().st_size==d['source']['pdf_bytes'];doc=fitz.open(pdf)
  for im in d['source_images']:
   pix=doc[im['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(im['render_scale'],im['render_scale']),clip=fitz.Rect(*im['crop_pdf_points']));saved=Image.open(H/im['path']).convert('RGB')
   assert saved.size==(pix.width,pix.height)==(im['width'],im['height']);assert saved.tobytes()==pix.samples;assert hashlib.sha256(pix.samples).hexdigest()==im['rgb_sha256']
 literal=''.join(''.join(r['source_rows']).split());assert len(literal)==r['source_slots']==37 and set(literal)<=set(C)and r['advertised_length']==27
 witness=json.loads((H/'native_witness.json').read_text())['record'];assert witness['id']==d['witness_record']=='p183_E';wc=''.join(''.join(witness['source_rows']).split());assert len(wc)==36
 target=r['target'];assert decrypt(wc,k['column_rank_order'],k['square'])==target and encrypt(target,k['column_rank_order'],k['square'])==wc
 baseline=native(literal,k);branches=[]
 for excluded in range(len(literal)):
  mapping=[i for i in range(len(literal))if i!=excluded];model=''.join(literal[i]for i in mapping);raw=inspect(model,k,mapping);candidate=repair(target,model,k,mapping,literal)
  assert candidate['ciphertext']==wc and not candidate['erased_coordinate_fills']
  branches.append({'excluded_source_index':excluded,'excluded_observed_coordinate':literal[excluded],'observed_coordinate_exclusions':1,'masked_slot_exclusions':0,'model_to_source_indices':mapping,'raw':raw['raw'],'known_coordinate_substitutions':candidate['known_coordinate_substitutions'],'substitution_count':len(candidate['known_coordinate_substitutions']),'erasure_fills':0,'target_roundtrip_verified':True})
 best=min(b['substitution_count']for b in branches);mins=[b['excluded_source_index']for b in branches if b['substitution_count']==best];assert best==1 and mins==[36]
 primary=branches[r['primary_model_excluded_source_index']];assert primary['excluded_observed_coordinate']=='X'and primary['substitution_count']==1
 mapping=primary['model_to_source_indices'];model=''.join(literal[i]for i in mapping);raw=inspect(model,k,mapping);edited=repair(target,model,k,mapping,literal)
 assert edited['known_coordinate_substitutions']==[{'model_index':3,'source_index':3,'printed':'D','from':'D','to':'X'}]
 unused=iter(sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(k['square'])));square=''.join(next(unused)if c=='?'else c for c in k['square']);assert len(set(square))==36
 assert encrypt(target,k['column_rank_order'],square)==wc
 fold=lambda s:''.join(c for c in s.upper()if c in'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace('X','')
 assert fold(r['readable_german'])==fold(target)and 'KRAMM'in r['readable_german']
 summary={'physical_records':1,'printed_source_slots':37,'valid_source_coordinates':37,'modeled_coordinates':36,'plaintext_positions':18,'baseline_fixed_positions':18,'native_fixed_positions':baseline['fixed_positions'],'candidate_fixed_positions':18,'known_coordinate_substitutions':1,'source_or_model_erasure_fills':0,'source_deletions':1,'observed_coordinate_deletions':1,'masked_slot_deletions':0,'inserted_slots':0,'source_reorderings':0,'published_key_changed':False}
 record={'id':r['id'],'literal_source':literal,'source_slots':37,'advertised_length':27,'native_frame':baseline,'raw_is_conditional_frame':True,'model_to_source_indices':mapping,**raw,'readable_candidate':edited,'readable_german':r['readable_german'],'global_completion_witness':{'square':square,'ciphertext':wc,'plaintext':target,'roundtrip_verified':True,'historical_completion_claim':False}}
 return {'schema':'adfgvx-parallel-car-query-frame-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(H/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':[record],'native_parallel_witness':{'id':witness['id'],'source_slots':36,'ciphertext':wc,'raw':target,'new_record_counted':False},'exclusion_scan':{'positions_tested':37,'metric':'Observed substitutions after one explicitly priced observed-coordinate exclusion; fixed target supplied by native E.','minimum_substitutions':1,'all_minimizing_excluded_source_indices':mins,'branches':branches},'prior_credit':d['prior_credit'],'limits':d['limits']}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=H/'certificates.json'
 if a.verify:assert c==json.loads(f.read_text())
 else:f.write_text(json.dumps(c,indent=2)+'\n')
 print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
