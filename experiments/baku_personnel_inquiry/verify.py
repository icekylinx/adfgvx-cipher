#!/usr/bin/env python3
"""Verify the explicitly conditional Baku inquiry and both reference-coupling alternatives.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt,untranspose
from experiments.romanian_pacification_consultation.verify import inspect,repair,permutation,masked_encryption,verify_crops
C='ADFGVX'
A='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def folded(s):
    s=s.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS')
    return ''.join(c for c in s if c in A+'?').replace('X','')
def completion(candidate,key):
    unused=iter(sorted(set(A)-set(key['square'])))
    square=''.join(next(unused)if c=='?'else c for c in key['square'])
    assert len(set(square))==36
    ct=candidate['ciphertext'].replace('?','A')
    pt=decrypt(ct,key['column_rank_order'],square)
    assert encrypt(pt,key['column_rank_order'],square)==ct
    assert all(a=='?'or a==b for a,b in zip(candidate['raw'],pt))
    return {'square':square,'ciphertext':ct,'plaintext':pt,'roundtrip_verified':True,'historical_completion_claim':False}
def unknown_cells(candidate):
    return [{'plaintext_index':p['plaintext_index'],'pair':p['pair'],'domain':p['domain']}for p in candidate['positions']if p['raw']=='?']
from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());source=data['records'][0];key=data['keys'][source['key_id']]
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']if k['id']==key['id'])
    for path,digest in data['prior_artifacts'].items():assert sha(HERE/path)==digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    literal=''.join(''.join(source['source_rows']).split());native=''.join(c if c in C else'?'for c in literal)
    assert len(literal)==source['source_slots']==279 and literal[245:255]==literal[255:265]=='XFVVFDXXVG'
    model=source['analysis_frame'];excluded=model['excluded_source_indices'];mapping=[i for i in range(len(native))if i not in excluded]
    assert excluded==list(range(245,255))+[278] and len(excluded)==11
    frame=''.join(native[i]for i in mapping);assert len(frame)==source['advertised_length']==268
    raw=inspect(frame,key,mapping);assert raw['raw']==source['expected_raw']
    candidate=repair(source['edited_output'],frame,key,mapping,literal)
    assert len(candidate['known_coordinate_substitutions'])==source['expected_substitutions']==10
    assert len(candidate['erased_coordinate_fills'])==source['expected_source_mask_fills']==1
    assert folded(source['readable_german'])==folded(candidate['raw'])
    for field in source['protected_fields']:assert field in candidate['raw']and field in source['readable_german']
    candidate['global_completion_witness']=completion(candidate,key)
    orphan_index=permutation(len(native),key['column_rank_order'])[-1]
    record={'id':source['id'],'literal_source':literal,'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
            'native_ciphertext':native,'native_raw_without_exclusions':decrypt(native,key['column_rank_order'],key['square'],allow_unpaired=True),
            'native_orphan':{'intermediate_index':len(native)-1,'source_index':orphan_index,'coordinate':native[orphan_index]},
            'analysis_frame':model,'ciphertext':frame,'modeled_slots':len(frame),'model_to_source_indices':mapping,
            'excluded_source_slots':[{'source_index':i,'printed':literal[i]}for i in excluded],**raw,
            'readable_candidate':candidate,'readable_german':source['readable_german'],'readable_nonseparator_label_mapping_verified':True}
    template=source['edited_output'];stencil=masked_encryption(template,key);prices=[];raw_jobs=[]
    for duplicate_start in [245,255]:
        retained_indices=[i for i in range(len(native))if i not in range(duplicate_start,duplicate_start+10)]
        reduced=''.join(native[i]for i in retained_indices)
        for j,additional_source_index in enumerate(retained_indices):
            test_frame=reduced[:j]+reduced[j+1:];test_mapping=retained_indices[:j]+retained_indices[j+1:]
            substitutions=sum(a in C and b!='?'and a!=b for a,b in zip(test_frame,stencil))
            # Independent calculation in the untransposed coordinate stream.
            middle=untranspose(test_frame,key['column_rank_order']);direct=0
            for i,ch in enumerate(template):
                if ch=='?':continue
                cell=key['square'].index(ch);pair=C[cell//6]+C[cell%6]
                direct+=sum(a in C and a!=b for a,b in zip(middle[2*i:2*i+2],pair))
            assert direct==substitutions
            source_masks=sum(a=='?'and b!='?'for a,b in zip(test_frame,stencil))
            row={'duplicate_exclusion_start':duplicate_start,'additional_excluded_source_index':additional_source_index,
                 'observed_coordinate_substitutions':substitutions,'source_mask_fills':source_masks,
                 'excluded_valid_coordinates':10+int(literal[additional_source_index]in C),
                 'excluded_masked_slots':int(literal[additional_source_index]not in C)}
            prices.append(row);raw_jobs.append((row,test_frame,test_mapping))
    minimum=min(p['observed_coordinate_substitutions']for p in prices)
    best=[j for j in raw_jobs if j[0]['observed_coordinate_substitutions']==minimum]
    assert len(prices)==538 and minimum==10 and len(best)==6
    assert {(x[0]['duplicate_exclusion_start'],x[0]['additional_excluded_source_index'])for x in best}=={(d,e)for d in [245,255]for e in [276,277,278]}
    distinct={};alignments=[]
    for price,test_frame,test_mapping in best:
        other=repair(template,test_frame,key,test_mapping,literal)
        assert other['raw']==candidate['raw']
        if test_frame not in distinct:
            distinct[test_frame]={'id':'frame_'+str(len(distinct)+1),'retained_ciphertext':test_frame,
                                 'raw_frame':inspect(test_frame,key,test_mapping),'edited_output':other['raw'],
                                 'candidate_ciphertext':other['ciphertext'],'unresolved_cells':unknown_cells(other),
                                 'global_completion_witness':completion(other,key)}
        alignments.append({**price,'frame_id':distinct[test_frame]['id'],'model_to_source_indices':test_mapping,
                           'known_coordinate_substitutions':other['known_coordinate_substitutions'],
                           'source_mask_fills_detail':other['erased_coordinate_fills']})
    distinct=list(distinct.values());assert len(distinct)==2
    assert {tuple((p['plaintext_index'],p['pair'])for p in f['unresolved_cells'])for f in distinct}=={
        ((113,'GG'),(114,'DX'),(115,'GX'),(116,'GG'),(124,'GD')),
        ((113,'GG'),(114,'DX'),(115,'GX'),(116,'GG'),(124,'GX'))}
    summary={'physical_records':1,'printed_source_slots':279,'valid_source_coordinates':278,'modeled_coordinates':268,
             'plaintext_positions':134,'baseline_fixed_positions':raw['fixed_positions'],'candidate_fixed_positions':candidate['fixed_positions'],
             'known_coordinate_substitutions':10,'source_or_model_erasure_fills':1,'source_mask_fills':1,
             'source_deletions':11,'deleted_valid_source_coordinates':11,'deleted_masked_source_slots':0,
             'inserted_slots':0,'source_reorderings':0,'published_key_changed':False,
             'counting_frame':'One primary 268-slot frame; alternative source mappings and reference relations are not additional physical records.'}
    comparison={'family':'Exclude one of the two identical source blocks at 245 or 255, then one additional retained source coordinate.',
                'scope':'Letter pattern fixed; its five question marks are wildcards. This does not assert unique historical text or a globally optimal damage mechanism.',
                'letter_pattern':template,'evaluated_labeled_source_maps':len(prices),'minimum_observed_substitutions':minimum,
                'prices':prices,'minimum_source_maps':alignments,'minimum_distinct_retained_frames':distinct,
                'displayed_raw_and_edited_strings_same_across_minima':True,
                'different_unknown_cell_relations_retained':True}
    return {'schema':'adfgvx-baku-personnel-inquiry-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':[record],
            'exclusion_comparison':comparison,'prior_credit':data['prior_credit'],'limits':data['limits']}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    cert=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert cert==json.loads(out.read_text())
    else:out.write_text(json.dumps(cert,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**cert['summary']},indent=2))
if __name__=='__main__':main()
