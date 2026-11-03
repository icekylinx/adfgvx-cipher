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
from experiments.romanian_pacification_consultation.verify import inspect,repair
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
    case_text=(ROOT/data['case']).read_text()
    out=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split());base=''.join(c if c in C else '?'for c in literal)
        assert len(literal)==r['source_slots']==r['advertised_length']
        assert '\n```text\n'+r['expected_raw']+'\n```' in case_text
        assert '\n> '+r['readable_german']+'\n' in case_text
        if r['edited_output'] != r['expected_raw']:
            assert '\n```text\n'+r['edited_output']+'\n```' in case_text
        key=keys[r['key_id']];mapping=list(range(len(base)))
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
        out.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_nonseparator_label_mapping_verified':True,'source_variants':variants})
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),'valid_source_coordinates':sum(r['valid_source_coordinates']for r in out),'modeled_coordinates':sum(r['source_slots']for r in out),'plaintext_positions':sum(len(r['raw'])for r in out),'baseline_fixed_positions':sum(r['fixed_positions']for r in out),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_deletions':0,'inserted_slots':0,'source_reorderings':0,'published_key_changed':False}
    support=data['independent_formula_support'];support_path=ROOT/support['input_path']
    assert sha(support_path)==support['input_sha256']
    previous=json.loads(support_path.read_text());witness=next(r for r in previous['records']if r['id']==support['record']['id'])
    assert witness==support['record']
    support_key=next(k for k in previous['keys']if k['id']==witness['key_id']);assert support_key==published[witness['key_id']]
    support_literal=''.join(''.join(witness['source_rows']).split());support_base=''.join(ch if ch in C else '?'for ch in support_literal)
    support_raw=inspect(support_base,support_key,list(range(len(support_base))))
    assert support_raw['raw']==witness['expected_raw']
    phrase=support['text'];old_start=support_raw['raw'].index(phrase);new_start=out[0]['readable_candidate']['raw'].index(phrase)
    formula_support={'source_record':witness['id'],'input_path':support['input_path'],'input_sha256':support['input_sha256'],'text':phrase,'old_start_plaintext_index':old_start,'new_start_plaintext_index':new_start,'scope':support['scope'],'old_raw':support_raw['raw'],'new_changed_positions_with_attested_formula_letters':[{'new_plaintext_index':new_start+i,'new_raw':out[0]['raw'][new_start+i],'candidate_and_old_raw':ch,'old_plaintext_index':old_start+i,'old_source_indices':support_raw['positions'][old_start+i]['source_indices']}for i,ch in enumerate(phrase)if out[0]['raw'][new_start+i]!=ch]}
    optional=data['optional_opening_proposal'];r=data['records'][0];primary=out[0]['readable_candidate']
    literal=''.join(''.join(r['source_rows']).split());base=''.join(ch if ch in C else '?'for ch in literal)
    assert optional['template']==optional['proposed_prefix']+r['edited_output'][19:]
    assert optional['primary_prefix']==r['edited_output'][:19]
    candidate=repair(optional['template'],base,keys[r['key_id']],list(range(len(base))),literal)
    primary_events={e['source_index']:e for e in primary['known_coordinate_substitutions']}
    optional_events={e['source_index']:e for e in candidate['known_coordinate_substitutions']}
    assert all(optional_events[i]==e for i,e in primary_events.items())
    extra=[optional_events[i]for i in sorted(optional_events.keys()-primary_events.keys())]
    assert len(extra)==optional['additional_observed_coordinate_substitutions']==8
    assert len(candidate['known_coordinate_substitutions'])==13
    assert candidate['erased_coordinate_fills']==primary['erased_coordinate_fills']
    assert candidate['fixed_positions']==95
    for field in ['LUHLEGKU?G','BRFIRBD9']:
        assert field in candidate['raw'] and field in optional['readable_german']
    assert folded(optional['readable_german'],'X')==folded(candidate['raw'],'X')
    assert '\n```text\n'+candidate['raw']+'\n```' in case_text
    assert '\n> '+optional['readable_german']+'\n' in case_text
    key=keys[r['key_id']];full_cipher=candidate['ciphertext'].replace('?','A')
    full_plain=decrypt(full_cipher,key['column_rank_order'],key['square'])
    assert encrypt(full_plain,key['column_rank_order'],key['square'])==full_cipher
    assert all(a=='?'or a==b for a,b in zip(candidate['raw'],full_plain))
    candidate['global_completion_witness']={'ciphertext':full_cipher,'plaintext':full_plain,'roundtrip_verified':True,'historical_completion_claim':False}
    optional_result={**optional,'candidate':candidate,'additional_observed_substitutions':extra,'changed_prefix_plaintext_positions':[{'plaintext_index':i,'raw':a,'optional':b}for i,(a,b)in enumerate(zip(optional['primary_prefix'],optional['proposed_prefix']))if a!=b]}
    return {'independent_formula_support':formula_support,'optional_opening_proposal':optional_result,'schema':'adfgvx-native-source-edition-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':out,'prior_credit':data['prior_credit'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
