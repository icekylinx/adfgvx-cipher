#!/usr/bin/env python3
"""Verify a source-reviewed native-frame edition and every declared word repair.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The source-preserving frame is independent of any language score.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt
from experiments.romanian_pacification_consultation.verify import inspect,repair,permutation
C='ADFGVX'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def folded(s,separator):
    s=s.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS')
    return ''.join(c for c in s if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace(separator,'')

from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());keys=data['keys']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for kid,key in keys.items():assert key==published[kid]
    for path,digest in data['prior_artifacts'].items():assert sha(HERE/path)==digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    out=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split());base=''.join(c if c in C else '?'for c in literal)
        assert len(literal)==r['source_slots']
        key=keys[r['key_id']];mapping=list(range(len(base)));native_base=base
        native_raw=decrypt(native_base,key['column_rank_order'],key['square'],allow_unpaired=bool(len(native_base)%2))
        native_orphan=None
        if len(native_base)%2:
            last=permutation(len(native_base),key['column_rank_order'])[-1]
            native_orphan={'intermediate_index':len(native_base)-1,'source_index':last,'coordinate':native_base[last]}
        model=r.get('analysis_frame')
        if model:
            assert model['kind']=='single_missing_group'
            gap=model['source_boundary'];count=model['inserted_slots']
            base=base[:gap]+'?'*count+base[gap:];mapping=mapping[:gap]+[None]*count+mapping[gap:]
        assert len(base)==r['advertised_length']
        raw=inspect(base,key,mapping);assert raw['raw']==r['expected_raw']
        candidate=repair(r['edited_output'],base,key,mapping,literal)
        assert len(candidate['known_coordinate_substitutions'])==r['expected_substitutions']
        assert sum(e['source_index'] is not None for e in candidate['erased_coordinate_fills'])==r['expected_source_mask_fills']
        assert sum(e['source_index'] is None for e in candidate['erased_coordinate_fills'])==r.get('expected_inserted_slot_fills',0)
        # One consistent global completion, never separate assignments per occurrence.
        unused=iter(sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(key['square'])))
        full_square=''.join(next(unused) if ch=='?' else ch for ch in key['square'])
        assert len(set(full_square))==36
        full_cipher=candidate['ciphertext'].replace('?','A')
        full_plain=decrypt(full_cipher,key['column_rank_order'],full_square)
        assert encrypt(full_plain,key['column_rank_order'],full_square)==full_cipher
        assert all(a=='?'or a==b for a,b in zip(candidate['raw'],full_plain))
        candidate['global_completion_witness']={'square':full_square,'ciphertext':full_cipher,'plaintext':full_plain,'roundtrip_verified':True,'historical_completion_claim':False}
        assert folded(r['readable_german'][:-1] if r.get('question_mark_punctuation_at_end') else r['readable_german'],r['separator_label'])==folded(candidate['raw'],r['separator_label']),r['id']
        for token in r.get('protected_fields',[]):
            assert token in raw['raw'] and token in candidate['raw'] and token in r['readable_german'],(r['id'],token)
        variants=[]
        for v in r['source_variants']:
            s=''.join(v['grouped'].split());assert len(s)==len(base)and set(s)<=set(C)
            text=decrypt(s,key['column_rank_order'],key['square'])
            assert encrypt(text,key['column_rank_order'],key['square'])==s
            variants.append({'name':v['name'],'literal_source':s,'plaintext':text,'source_differences':[{'source_index':i,'first_printed':a,'second_printed':b}for i,(a,b)in enumerate(zip(literal,s))if a!=b], 'plaintext_differences':[{'plaintext_index':i,'first_printed_variant':a,'second_printed_variant':b}for i,(a,b)in enumerate(zip(raw['raw'],text))if a!=b],'roundtrip_verified':True,'source_correction_claim':False})
        out.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),'native_ciphertext':native_base,'native_raw_without_gap':native_raw,'native_orphan':native_orphan,'analysis_frame':model,'modeled_slots':len(base),'ciphertext':base,'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_nonseparator_label_mapping_verified':True,'source_variants':variants})
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),'valid_source_coordinates':sum(r['valid_source_coordinates']for r in out),'modeled_coordinates':sum(r['modeled_slots']for r in out),'plaintext_positions':sum(len(r['raw'])for r in out),'baseline_fixed_positions':sum(r['fixed_positions']for r in out),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_mask_fills':sum(e['source_index'] is not None for r in out for e in r['readable_candidate']['erased_coordinate_fills']),'inserted_slot_fills':sum(e['source_index'] is None for r in out for e in r['readable_candidate']['erased_coordinate_fills']),'source_deletions':0,'inserted_slots':sum(r['modeled_slots']-r['source_slots']for r in out),'source_reorderings':0,'published_key_changed':False}
    gap_report=check_gap_family(data,out)
    copy_report=check_key_notice_copy(data,out)
    return {'schema':'adfgvx-nov15-radio-source-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':out,'single_gap_candidate_comparison':gap_report,'december_notice_copy_comparison':copy_report,'prior_credit':data['prior_credit'],'limits':data['limits']}


def check_gap_family(data,records):
    source=data['records'][0];record=records[0]
    assert source['id']=='p197_A1' and record['source_slots']==193
    key=data['keys'][source['key_id']];literal=record['literal_source'];native=record['native_ciphertext']
    template=source['edited_output'];target=encrypt(template,key['column_rank_order'],key['square'])
    assert len(target)==198 and len(template)==99
    all_prices=[];candidates=[]
    for boundary in range(len(literal)+1):
        frame=native[:boundary]+'?'*5+native[boundary:]
        mapping=list(range(boundary))+[None]*5+list(range(boundary,len(native)))
        candidate=repair(template,frame,key,mapping,literal)
        price=len(candidate['known_coordinate_substitutions'])
        # Separate edit-distance count on the full known candidate; no use of repair's positions.
        reduced_target=target[:boundary]+target[boundary+5:]
        independent=sum(a in C and a!=b for a,b in zip(literal,reduced_target))
        assert len(reduced_target)==len(literal) and independent==price
        all_prices.append({'source_boundary':boundary,'observed_coordinate_substitutions':price,
                           'source_mask_fills':sum(e['source_index'] is not None for e in candidate['erased_coordinate_fills']),
                           'inserted_slot_fills':sum(e['source_index'] is None for e in candidate['erased_coordinate_fills'])})
        candidates.append((boundary,price,frame,mapping,candidate))
    minimum=min(p['observed_coordinate_substitutions']for p in all_prices)
    best=[p['source_boundary']for p in all_prices if p['observed_coordinate_substitutions']==minimum]
    assert minimum==1 and best==[165]
    nearby=[]
    for boundary,price,frame,mapping,candidate in candidates:
        if price<=minimum+1:
            nearby.append({'source_boundary':boundary,'raw_frame':inspect(frame,key,mapping),
                           'known_coordinate_substitutions':candidate['known_coordinate_substitutions'],
                           'erased_coordinate_fills':candidate['erased_coordinate_fills']})
    return {'family':'Exactly one consecutive gap of five coordinates, at any of the 194 source boundaries, with the published key fixed.',
            'scope':'All prices are conditioned on the one stated candidate; this does not prove unique historical text or a globally minimal error mechanism.',
            'target_plaintext':template,'candidate_ciphertext':target,'examined_boundaries':len(all_prices),
            'minimum_observed_substitutions':minimum,'minimizing_boundaries':best,'prices':all_prices,
            'all_frames_within_one_substitution_of_minimum':nearby}

def check_key_notice_copy(data,records):
    ref=data['cross_copy_reference'];path=HERE/ref['path'];assert sha(path)==ref['sha256']
    old=json.loads(path.read_text());literal=''.join(''.join(old['source']['source_rows']).split())
    key=data['keys']['Nov13-15b'];previous=inspect(literal,key,list(range(len(literal))))
    current=next(r for r in records if r['id']=='p197_B')
    assert len(literal)==len(current['literal_source'])==124
    diffs=[{'source_index':i,'p189_C':a,'p197_B':b}for i,(a,b)in enumerate(zip(literal,current['literal_source']))if a!=b]
    assert diffs==[{'source_index':93,'p189_C':'G','p197_B':'F'}]
    changed=[i for i,(a,b)in enumerate(zip(current['raw'],current['readable_candidate']['raw']))if a!=b]
    supported=[i for i in changed if previous['raw'][i]==current['readable_candidate']['raw'][i]]
    unsupported=[i for i in changed if i not in supported]
    assert changed==[6,8,10] and supported==[6] and unsupported==[8,10]
    return {'reference':ref,'literal_p189_C':literal,'raw_p189_C':previous,'source_differences':diffs,
            'changed_p197_B_plaintext_indices':changed,'indices_supported_by_other_raw_copy':supported,
            'indices_still_editorial_in_both_copies':unsupported,
            'limit':'The repeated text supports the literal body and p197 B letter B at index 6. It supplies no independent raw support for the shared R/F repairs or a meaning for IRRTUM.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
