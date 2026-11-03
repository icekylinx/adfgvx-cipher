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

def check_case(data):
    """Bind the evidence displays to their own live case sections."""
    case=ROOT/data['case'];text=case.read_text()
    from data.reviews.check_reading_presentation import expected_legend
    assert expected_legend(case) in text
    for r in data['records']:
        heading='## '+r['id'].replace('_',' ')+'\n'
        assert text.count(heading)==1,r['id']
        section=text.split(heading,1)[1].split('\n## ',1)[0]
        assert f"Literal header: `{r['header_literal']}`." in section,r['id']
        fences=re.findall(r'```text\n(.*?)\n```',section,re.S)
        assert fences==['\n'.join(r['source_rows']),r['expected_raw'],r['edited_output']],r['id']
        assert re.findall(r'^> (.+)$',section,re.M)==[r['readable_german']],r['id']
    assert 'only one section-A ciphertext body is printed' in text
    assert 'not a historical numeral assignment' in text

from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());keys=data['keys']
    check_case(data)
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for kid,key in keys.items():assert key==published[kid]
    for path,digest in data['prior_artifacts'].items():assert sha(HERE/path)==digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    index=data['index_omission'];assert sha(ROOT/index['index_path'])==index['index_sha256']
    old=json.loads((ROOT/index['index_path']).read_text())['blocks']
    assert len(old)==index['index_block_count'] and min(x['printed_page']for x in old)==57
    assert not any(x['printed_page']==56 for x in old)
    out=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split());base=''.join(c if c in C else '?'for c in literal)
        assert len(literal)==r['source_slots']
        if r['advertised_length'] is not None:assert len(literal)==r['advertised_length']
        else:assert r['id']=='p152_C'and r['advertised_length_text']=='----'
        key=keys[r['key_id']];mapping=list(range(len(base)))
        raw=inspect(base,key,mapping);assert raw['raw']==r['expected_raw']
        candidate=repair(r['edited_output'],base,key,mapping,literal)
        assert candidate['raw']==r['edited_output']
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
        unresolved_family=[]
        if r.get('unresolved_field'):
            field=r['unresolved_field'];assert r['id']=='p152_B2'and field=={'plaintext_index':14,'source_index':91,'domain':'4FGUYZ','display':'EB?Q'}
            assert candidate['ciphertext'].count('?')==1 and candidate['ciphertext'][91]=='?'
            for coordinate in C:
                full=candidate['ciphertext'].replace('?',coordinate)
                value=decrypt(full,key['column_rank_order'],key['square'])
                assert encrypt(value,key['column_rank_order'],key['square'])==full
                assert all(a=='?'or a==b for a,b in zip(candidate['raw'],value))
                unresolved_family.append({'source_index':91,'coordinate':coordinate,'field':value[12:16],'plaintext':value,'ciphertext':full,'exact_reencryption':True,'historical_selection_claim':False})
            assert ''.join(sorted(x['field'][2]for x in unresolved_family))==field['domain']
        out.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_nonseparator_label_mapping_verified':True,'source_variants':variants,'unresolved_source_field_family':unresolved_family})
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),'valid_source_coordinates':sum(r['valid_source_coordinates']for r in out),'modeled_coordinates':sum(r['source_slots']for r in out),'plaintext_positions':sum(len(r['raw'])for r in out),'baseline_fixed_positions':sum(r['fixed_positions']for r in out),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_deletions':0,'inserted_slots':0,'source_reorderings':0,'published_key_changed':False}
    return {'schema':'adfgvx-native-source-edition-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':out,'prior_credit':data['prior_credit'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
