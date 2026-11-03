#!/usr/bin/env python3
"""Verify the separately received second part of Mackensen's withdrawal report.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,sha,permutation,verify_crops
from adfgvx.cipher import decrypt,untranspose


def inserted_frame(literal,at):
    return literal[:at]+'?'+literal[at:],list(range(at))+[None]+list(range(at,len(literal)))


def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());k=d['key'];assert k==next(x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']if x['id']==k['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/d[field]['path'])==d[field]['sha256']
    a=d['assembly_evidence'];assert sha(ROOT/a['prior_source_path'])==a['prior_source_sha256'];old=json.loads((ROOT/a['prior_source_path']).read_text())
    for part in ['part1','part3']:
        oldrow=next(s for s in old['records']if s['id']==a[part+'_id']);assert oldrow['header_literal']==a[part+'_header']and oldrow['editorial_plaintext']==a[part+'_edited_plaintext']
    for image in d['source_images']:assert sha(HERE/image['path'])==image['sha256']
    if pdf:verify_crops(pdf,d['source'],d['source_images'],HERE)
    s=d['records'][0];literal=''.join(s['source_rows']).replace(' ','');assert len(literal)==s['source_slots']==377 and set(literal)<=set(C)
    at=s['analysis_frame']['insert_at_source_boundary'];assert at==283 and literal[280:284]=='FGAD';cipher,mapping=inserted_frame(literal,at);assert len(cipher)==s['advertised_length']==378
    raw=inspect(cipher,k,mapping);assert raw['raw']==s['expected_raw'];proposal=repair(s['readable_candidate'],cipher,k,mapping,literal)
    optional=repair(s['optional_geographic_candidate'],cipher,k,mapping,literal)
    assert len(optional['known_coordinate_substitutions'])==len(proposal['known_coordinate_substitutions'])+4
    assert optional['erased_coordinate_fills']==proposal['erased_coordinate_fills']
    order=permutation(len(literal),k['column_rank_order']);middle=''.join(literal[i]for i in order);assert middle==untranspose(literal,k['column_rank_order'])
    native=''.join(k['square'][6*C.index(middle[i])+C.index(middle[i+1])]for i in range(0,len(middle)-1,2));assert native==decrypt(literal,k['column_rank_order'],k['square'],allow_unpaired=True)
    native_frame={'coordinates':len(literal),'plaintext_positions':len(native),'raw':native,'orphan_intermediate_index':len(middle)-1,'orphan_source_index':order[-1],'orphan_coordinate':middle[-1],'scope':'Unaltered odd frame. The orphan is retained explicitly; no claim of fluent reading or complete-pair re-encryption is made.'}
    prices=[]
    for j in range(len(literal)+1):
        c,mp=inserted_frame(literal,j);v=repair(s['readable_candidate'],c,k,mp,literal);prices.append({'source_boundary':j,'observed_substitutions':len(v['known_coordinate_substitutions']),'missing_coordinate_fills':len(v['erased_coordinate_fills']),'inserted_coordinate':v['erased_coordinate_fills'][0]['to']})
    minimum=min(p['observed_substitutions']for p in prices);best=[p['source_boundary']for p in prices if p['observed_substitutions']==minimum];assert minimum==13 and best==[283]
    assert re.sub('[^A-Z0-9?]','',s['readable_german'].upper()).replace('X','')==s['readable_candidate'].replace('X','')
    assert '> '+s['readable_german']in(ROOT/s['case_path']).read_text()
    summary={'physical_records':1,'printed_source_slots':377,'valid_source_coordinates':377,'modeled_coordinates':378,'plaintext_positions':189,'baseline_fixed_positions':raw['fixed_positions'],'candidate_fixed_positions':proposal['fixed_positions'],'known_coordinate_substitutions':len(proposal['known_coordinate_substitutions']),'source_mask_fills':0,'inserted_slot_fills':len(proposal['erased_coordinate_fills']),'frame_insertions':1,'frame_deletions':0,'published_key_changed':False}
    return {'schema':'adfgvx-mackensen-withdrawal-part2-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':[{'id':s['id'],'literal_source':literal,'literal_printed_rows':s['source_rows'],'native_odd_frame':native_frame,'ciphertext':cipher,'model_to_source_indices':mapping,**raw,'readable_candidate':proposal,'optional_geographic_candidate':optional,'all_single_insertion_prices':prices,'minimum_observed_substitutions':minimum,'minimum_source_boundaries':best,'complete_model_exhaustiveness_scope':'All single insertions into the transcribed source under the unchanged published key and fixed baseline template; no other damage models are excluded.'}],'headers':d['headers'],'assembly_evidence':a,'limits':d['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))

if __name__=='__main__':main()
