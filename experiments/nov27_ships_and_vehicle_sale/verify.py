#!/usr/bin/env python3
"""Verify native shipping and conditional surplus-group source editions.

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
        model=r.get('analysis_frame');excluded=[]
        if model:
            assert model['kind']=='single_surplus_group'
            start=model['source_start'];count=model['excluded_slots']
            excluded=[{'source_index':i,'printed':literal[i]}for i in range(start,start+count)]
            base=base[:start]+base[start+count:];mapping=mapping[:start]+mapping[start+count:]
        assert len(base)==r['advertised_length']
        raw=inspect(base,key,mapping);assert raw['raw']==r['expected_raw']
        candidate=repair(r['edited_output'],base,key,mapping,literal)
        assert len(candidate['known_coordinate_substitutions'])==r['expected_substitutions']
        assert len(candidate['erased_coordinate_fills'])==r['expected_source_mask_fills']
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
        out.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),'native_ciphertext':native_base,'native_raw_without_exclusion':native_raw,'native_orphan':native_orphan,'analysis_frame':model,'excluded_source_slots':excluded,'modeled_slots':len(base),'ciphertext':base,'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_nonseparator_label_mapping_verified':True,'source_variants':variants})
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),'valid_source_coordinates':sum(r['valid_source_coordinates']for r in out),'modeled_coordinates':sum(r['modeled_slots']for r in out),'plaintext_positions':sum(len(r['raw'])for r in out),'baseline_fixed_positions':sum(r['fixed_positions']for r in out),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_deletions':sum(len(r['excluded_source_slots'])for r in out),'deleted_valid_source_coordinates':sum(e['printed'] in C for r in out for e in r['excluded_source_slots']),'deleted_masked_source_slots':sum(e['printed'] not in C for r in out for e in r['excluded_source_slots']),'inserted_slots':0,'source_reorderings':0,'published_key_changed':False}
    window_report=check_exclusion_family(data,out)
    return {'schema':'adfgvx-nov27-shipping-source-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':out,'single_exclusion_candidate_comparison':window_report,'prior_credit':data['prior_credit'],'limits':data['limits']}


def check_exclusion_family(data,records):
    source=data['records'][1];record=records[1]
    assert source['id']=='p223_C' and record['source_slots']==235
    key=data['keys'][source['key_id']];literal=record['literal_source'];native=record['native_ciphertext']
    template=source['edited_output'];target=encrypt(template,key['column_rank_order'],key['square'])
    assert len(target)==230 and len(template)==115
    prices=[];candidates=[]
    for start in range(len(literal)-4):
        frame=native[:start]+native[start+5:]
        mapping=list(range(start))+list(range(start+5,len(native)))
        candidate=repair(template,frame,key,mapping,literal)
        price=len(candidate['known_coordinate_substitutions'])
        # Independent direct comparison with the source after excluding this window.
        retained_literal=literal[:start]+literal[start+5:]
        independent=sum(a in C and a!=b for a,b in zip(retained_literal,target))
        assert len(retained_literal)==230 and independent==price
        prices.append({'source_start':start,'excluded_literal':literal[start:start+5],
                       'excluded_valid_coordinates':sum(c in C for c in literal[start:start+5]),
                       'excluded_masked_slots':sum(c not in C for c in literal[start:start+5]),
                       'observed_coordinate_substitutions':price,'source_mask_fills':len(candidate['erased_coordinate_fills'])})
        candidates.append((start,price,frame,mapping,candidate))
    minimum=min(p['observed_coordinate_substitutions']for p in prices)
    best=[p['source_start']for p in prices if p['observed_coordinate_substitutions']==minimum]
    assert minimum==0 and best==[220,221]
    best_frames=[]
    for start,price,frame,mapping,candidate in candidates:
        if price==minimum:
            best_frames.append({'source_start':start,'excluded_literal':literal[start:start+5],
                                'retained_ciphertext':frame,'model_to_source_indices':mapping,
                                'raw_frame':inspect(frame,key,mapping),'candidate':candidate})
    assert len(best_frames)==2 and best_frames[0]['retained_ciphertext']==best_frames[1]['retained_ciphertext']
    assert best_frames[0]['candidate']['ciphertext']==best_frames[1]['candidate']['ciphertext']==target
    return {'family':'One consecutive five-slot exclusion at any of the 231 source windows; the published key and full proposed plaintext remain fixed.',
            'scope':'A candidate-conditioned comparison, not a proof of historical text, a visible cancellation or the actual damage mechanism.',
            'target_plaintext':template,'candidate_ciphertext':target,'examined_windows':len(prices),
            'minimum_observed_substitutions':minimum,'minimizing_starts':best,'prices':prices,
            'all_minimum_frames':best_frames,'minimum_frames_have_identical_retained_ciphertext':True}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
