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

def verify_live_headers(data,case_text=None):
    """Bind each displayed header to its own record, including the ambiguity."""
    if case_text is None:
        case_text=(ROOT/data['case']).read_text()
    headings=list(re.finditer(r'^## (.+)$',case_text,re.M))
    displayed=re.findall(r'^\*\*Literal header:\*\* `([^`\n]+)`$',case_text,re.M)
    assert displayed==[r['header_literal']for r in data['records']], 'Live literal headers changed'
    for record in data['records']:
        heading=record['id'].replace('_',' ')
        matches=[i for i,m in enumerate(headings)if m[1]==heading]
        assert len(matches)==1,(record['id'],'missing or repeated case section')
        i=matches[0]
        section=case_text[headings[i].end():headings[i+1].start()if i+1<len(headings)else len(case_text)]
        expected='**Literal header:** `'+record['header_literal']+'`'
        assert section.count(expected)==1,(record['id'],'header belongs in its own section')
        if record['id']=='p156_A1':
            assert '[2/3] TLE' in record['header_literal']
            note=('The faint part-count digit admits 2/3 readings. The header display uses editorial brackets '
                  'to retain both alternatives; only the first part is printed in this section. The advertised '
                  '84-coordinate body length is clear and does not depend on that header digit.')
            assert note in section,'Live p156 A1 header-ambiguity qualification changed'

from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());keys=data['keys']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    verify_live_headers(data)
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for kid,key in keys.items():assert key==published[kid]
    for path,digest in data['prior_artifacts'].items():assert sha(HERE/path)==digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    out=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split());base=''.join(c if c in C else '?'for c in literal)
        assert len(literal)==r['source_slots']==r['advertised_length']
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
            alternative_repair=repair(r['edited_output'],s,key,mapping,s)
            assert len(alternative_repair['known_coordinate_substitutions'])==v['expected_substitutions']
            assert len(alternative_repair['erased_coordinate_fills'])==v['expected_source_mask_fills']
            variants.append({'readable_candidate':alternative_repair,'name':v['name'],'literal_source':s,'plaintext':text,'source_differences':[{'source_index':i,'first_printed':a,'second_printed':b}for i,(a,b)in enumerate(zip(literal,s))if a!=b], 'plaintext_differences':[{'plaintext_index':i,'first_printed_variant':a,'second_printed_variant':b}for i,(a,b)in enumerate(zip(raw['raw'],text))if a!=b],'roundtrip_verified':True,'source_correction_claim':False})
        if r['id']=='p156_A1':
            assert r['header_transcription_variants']==[r['header_literal'].replace('[2/3]','2'),r['header_literal'].replace('[2/3]','3')]
        out.append({'id':r['id'],'header_transcription':r['header_literal'],'header_variants':r.get('header_transcription_variants',[]),'literal_source':literal,'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_nonseparator_label_mapping_verified':True,'source_variants':variants})
    reference=data['parallel_address_witness']
    assert sha(ROOT/reference['inputs_path'])==reference['inputs_sha256']
    prior=json.loads((ROOT/reference['inputs_path']).read_text())
    rr=next(r for r in prior['records']if r['id']==reference['record_id'])
    literal=''.join(''.join(rr['rows']).split())
    prior_key=keys['Nov7-9'];base=''.join(c if c in C else '?'for c in literal)
    prior_raw=inspect(base,prior_key,list(range(len(base))))
    assert prior_raw['raw']==rr['expected_raw']
    crop=reference['source_image']
    parallel_evidence = verify_source_evidence(pdf, data['source'], [crop], ROOT)
    print(json.dumps({'parallel_source_evidence': parallel_evidence['summary']}))
    comparisons=[]
    for spec in reference['comparisons']:
        new=next(r for r in out if r['id']==spec['record_id'])
        agreements=[];disagreements=[];new_support=[];prior_support=[]
        for j in range(spec['compared_positions']):
            ni=j+spec['new_plaintext_start'];pi=j+spec['prior_plaintext_start']
            a=new['raw'][ni];b=prior_raw['raw'][pi];wanted=new['readable_candidate']['raw'][ni]
            row={'new_plaintext_index':ni,'prior_plaintext_index':pi,'new_raw':a,'prior_raw':b,'new_edited':wanted,'new_pair':new['positions'][ni]['pair'],'prior_pair':prior_raw['positions'][pi]['pair']}
            if a!='?'and b!='?':
                (agreements if a==b else disagreements).append(row)
            if b=='?'and a!='?':
                row={**row,'prior_domain':prior_raw['positions'][pi]['domain']}
                assert a in row['prior_domain']
                new_support.append(row)
            if a!=wanted and b==wanted:prior_support.append(row)
        assert len(agreements)==spec['expected_known_agreements']
        assert len(disagreements)==spec['expected_known_disagreements']
        assert len(new_support)==spec['expected_new_labels_at_prior_masks']
        assert len(prior_support)==spec['expected_prior_labels_supporting_new_edits']
        comparisons.append({'record_id':spec['record_id'],'new_plaintext_start':spec['new_plaintext_start'],'prior_plaintext_start':spec['prior_plaintext_start'],'compared_positions':spec['compared_positions'],'known_agreements':agreements,'known_disagreements':disagreements,'new_raw_labels_at_prior_masks':new_support,'prior_raw_labels_supporting_new_edits':prior_support})
    parallel={'record_id':rr['id'],'header_literals':rr['headers'],'raw':prior_raw['raw'],'source_slots':len(literal),'source_image':crop,'comparisons':comparisons,'scope':reference['scope'],'counts_as_new_physical_record':False}
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),'valid_source_coordinates':sum(r['valid_source_coordinates']for r in out),'modeled_coordinates':sum(r['source_slots']for r in out),'plaintext_positions':sum(len(r['raw'])for r in out),'baseline_fixed_positions':sum(r['fixed_positions']for r in out),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_deletions':0,'inserted_slots':0,'source_reorderings':0,'published_key_changed':False}
    return {'schema':'adfgvx-native-source-edition-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':out,'parallel_address_witness':parallel,'prior_credit':data['prior_credit'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
