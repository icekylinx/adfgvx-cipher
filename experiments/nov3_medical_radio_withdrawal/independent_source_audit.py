#!/usr/bin/env python3
"""Independent source/count audit of p117 C3/C4 by icekylinx and GPT-6 Astra Pro."""
import argparse,hashlib,json
from functools import lru_cache
from pathlib import Path

ROWS={
'p117_C3':[
'DGGAD ADVVG GDDGV AGAVF AGAVD VAGVG GXGDD AAFVV',
'GGXVG VGGDG GAXDD FADAV VGVFA DVDXG GVFDG XFVFA',
'VVFDF AXDVA GFAVV AFGGV GVFAF DAVGG DADDG GAGVG',
'VGAGG VAAGD AGFAV DGGGD ADGFX AGXGA GGDGX FAVDG'],
'p117_C4':[
'XFDVV FAGDG XDXXX ADGDX VDGDX VDXDF FAGVG VAGGX',
'VGXGD GGDVA XFXXA GXAVF GFFFG DGDXD AGVXD DXVGX',
'ADGXX FAADD XGGGD FVXAV GDGDG VDDGA VFADD VG']}
CO='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decrypt(source,key):
 width=len(key['column_rank_order']);columns={};offset=0
 for col in sorted(range(width),key=key['column_rank_order'].__getitem__):
  length=(len(source)-col+width-1)//width
  columns[col]=source[offset:offset+length];offset+=length
 middle=''.join(columns[i%width][i//width] for i in range(len(source)))
 return ''.join(key['square'][6*CO.index(middle[i])+CO.index(middle[i+1])] for i in range(0,len(middle),2))
def encrypt(text,key):
 values=[CO[key['square'].index(c)//6]+CO[key['square'].index(c)%6] for c in text]
 middle=''.join(values);width=len(key['column_rank_order'])
 ordering=sorted(range(len(middle)),key=lambda i:(key['column_rank_order'][i%width],i//width))
 return ''.join(middle[i] for i in ordering)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]);parser.add_argument('--output',type=Path,default=Path(__file__).with_name('independent_source_audit.json'));parser.add_argument('--verify',action='store_true');a=parser.parse_args()
 path=a.repo/'experiments/nov3_medical_radio_withdrawal';inp=json.loads((path/'inputs.json').read_text());cert=json.loads((path/'certificates.json').read_text());key=next(k for k in inp['keys'] if k['id']=='Nov1-3');records={r['id']:r for r in inp['records']};checks=[]
 for id,rows in ROWS.items():
  literal=''.join(''.join(rows).split());r=records[id]
  assert rows==r['rows'] and literal==r['literal_source']
  selected=''.join(c for i,c in enumerate(literal) if i not in r['excluded_source_indices'])
  raw=decrypt(selected,key);assert raw==r['expected_raw']==r['editorial_text'];assert encrypt(raw,key)==selected
  checks.append({'id':id,'independently_read_rows':rows,'row_coordinate_counts':[len(''.join(x.split())) for x in rows],'source_slots':len(literal),'advertised_length':r['advertised_length'],'selected_frame_slots':len(selected),'plaintext':raw,'coordinate_substitutions':0,'source_masks':0})
 old=next(r for r in json.loads((path/'prior_candidates.json').read_text())['rows'] if r['block_id']=='p117_ocr_block3')['ciphertext'];fresh=records['p117_C3']['literal_source']
 assert old[:35]==fresh[:35] and old[35:39]=='AAF?' and fresh[35:40]=='AAFVV' and old[39:]==fresh[40:]
 source=records['p117_C4']['literal_source'];wanted=encrypt(records['p117_C4']['editorial_text'],key)
 contiguous=[{'start':i,'omitted':source[i:i+5],'mismatch_count':sum(a!=b for a,b in zip(source[:i]+source[i+5:],wanted))} for i in range(len(source)-5+1)]
 tied=[x['start']for x in contiguous if x['mismatch_count']==0];assert tied==list(range(16,23))
 measured={'states':0,'keep_transitions':0,'delete_transitions':0}
 @lru_cache(None)
 def count(i,j):
  measured['states']+=1
  if j==len(wanted):return int(len(source)-i==5-(i-j))
  if i==len(source) or i-j>5:return 0
  result=0
  if source[i]==wanted[j]:
   measured['keep_transitions']+=1;result+=count(i+1,j+1)
  if i-j<5:
   measured['delete_transitions']+=1;result+=count(i+1,j)
  return result
 total=count(0,0);assert total==14
 def layouts(i,j,removed):
  if j==len(wanted):return [removed+list(range(i,len(source)))]
  out=[]
  if i<len(source) and source[i]==wanted[j] and count(i+1,j+1):out+=layouts(i+1,j+1,removed)
  if i<len(source) and i-j<5 and count(i+1,j):out+=layouts(i+1,j,removed+[i])
  return out
 all_layouts=layouts(0,0,[]);assert len(all_layouts)==len(set(tuple(x)for x in all_layouts))==14
 assert all(len(x)==5 and ''.join(c for i,c in enumerate(source)if i not in x)==wanted for x in all_layouts)
 out={'schema':'adfgvx-p117-independent-audit-v1','authors':['icekylinx','GPT-6 Astra Pro'],'inputs_sha256':sha(path/'inputs.json'),'certificates_sha256':sha(path/'certificates.json'),'source_images_reviewed':[{'path':str(p.relative_to(a.repo)),'sha256':sha(p)}for p in [path/'sources/p117_C_detail.png',path/'sources/p117_full.png']],'visual_findings':['All C3 rows contain eight full five-symbol groups: 4 x 40 = 160.','C4 has 40 + 40 + 37 = 117 symbols, while the clear printed heading says RICHI-112.','C4 first-row fifth group VDGDX is legible as five observed coordinates, not a printed mask or an overwritten annotation.','Both source transcriptions agree with the independently inspected crop and full page.','The C header gives source parts 3 and 4; no source evidence here supplies parts 1 and 2.'],'records':checks,'prior_C3_OCR_difference':{'old_group':'AAF?','new_source_group':'AAFVV','source_indices_zero_based':[35,36,37,38,39],'note':'This is a short OCR group plus one OCR mask, not a historical one-coordinate loss.'},'fixed_candidate_contiguous_exclusions':{'actual_evaluations':len(contiguous),'zero_mismatch_starts':tied,'all_candidates':contiguous},'fixed_candidate_arbitrary_five_deletions':{'zero_substitution_layout_count':total,'layouts':all_layouts,'measured_dynamic_program':measured},'limits':['All deletion comparisons are retrospective consistency checks against the supplied fixed reading and known key; they are not blind recovery or historical uniqueness.','Selecting the complete group at start20 is a display convention among equivalent streams.','Deleting any five observed coordinates costs five observed-symbol exclusions even when the retained stream needs no substitutions.'],'verified':True}
 if a.verify:
  assert out == json.loads(a.output.read_text())
 else:
  a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'verified':True,'source_counts':[160,117],'contiguous_evaluations':len(contiguous),'zero_starts':tied,'arbitrary_layouts':total,'measured_dp':measured},indent=2))
if __name__=='__main__':main()
