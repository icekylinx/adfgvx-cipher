#!/usr/bin/env python3
"""Verify a priced partial p152 crossing report and independent place spelling.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect,repair
from data.reviews.check_reading_presentation import expected_legend
C='ADFGVX'


def load(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fold(text):return re.sub('[^A-Z0-9?]','',text.upper()).replace('X','')


def build(pdf=None,attestation_pdf=None):
    data=load(HERE/'inputs.json');key=data['key']
    assert key==next(k for k in load(ROOT/'data/keys.json')['keys']if k['id']=='Nov4-6')
    assert '?'not in key['square'] and len(set(key['square']))==36
    evidence=verify_source_evidence(pdf,data['source'],data['source_images'],HERE)
    assert sha(HERE/'place_attestation.json')==data['attestation_sha256']
    attestation=load(HERE/'place_attestation.json')
    primary=attestation['independent_primary_attestation']
    assert primary['spelling']=='Vercsiorova'and primary['printed_page']==159 and primary['pdf_page_1based']==6
    assert primary['spelling']in primary['short_quote']
    if attestation_pdf is not None:
        import fitz
        assert attestation_pdf.stat().st_size==primary['pdf_bytes']
        assert sha(attestation_pdf)==primary['pdf_sha256']
        with fitz.open(attestation_pdf)as doc:
            page=' '.join(doc[primary['pdf_page_1based']-1].get_text().split())
            assert primary['short_quote']in page
    records=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split())
        assert len(literal)==r['source_slots']==r['advertised_length']==128
        assert sum(c in C for c in literal)==r['valid_source_coordinates']==125
        assert literal[1]=='E'and literal[48:50]=='--'
        base=''.join(c if c in C else '?'for c in literal);mapping=list(range(len(base)))
        raw=inspect(base,key,mapping);assert raw['raw']==r['expected_raw']and raw['fixed_positions']==61
        variants=[]
        for v in r['source_variants']:
            assert len(v['prefix'])==37 and v['edited_output']==v['prefix']+raw['raw'][37:]
            candidate=repair(v['edited_output'],base,key,mapping,literal)
            assert len(candidate['known_coordinate_substitutions'])==v['expected_substitutions']
            assert len(candidate['erased_coordinate_fills'])==v['expected_mask_fills']
            if '?'not in candidate['raw']:
                assert encrypt(candidate['raw'],key['column_rank_order'],key['square'])==candidate['ciphertext']
            variants.append({'id':v['id'],**candidate})
        candidate=variants[0]
        assert candidate['raw']==r['edited_output']
        assert candidate['fixed_positions']==63
        assert[(e['source_index'],e['from'],e['to'])for e in candidate['known_coordinate_substitutions']]==[(15,'A','X'),(31,'A','F'),(39,'F','V'),(40,'D','G'),(47,'A','X'),(78,'X','V'),(79,'F','X')]
        assert[(e['source_index'],e['to'])for e in candidate['erased_coordinate_fills']]==[(48,'F'),(49,'X')]
        assert candidate['ciphertext'].count('?')==1 and candidate['ciphertext'][1]=='?'
        assert candidate['raw'][3:14]==raw['raw'][3:14]=='VARC8IORO?A'
        assert candidate['raw'][37:]==raw['raw'][37:]
        assert all(token in candidate['raw']and token in r['readable_german']for token in r['protected_fields'])
        assert fold(r['readable_german'])==fold(candidate['raw'])
        assert candidate['raw'][14:19]=='KEINE'and raw['raw'][14:19]=='K1ILE'
        # The two name proposals are paid alternatives, not free relabellings.
        assert [(len(v['known_coordinate_substitutions']),len(v['erased_coordinate_fills']))for v in variants]==[(7,2),(9,3),(11,3)]
        assert variants[1]['raw'][3:14]=='VARCSIOROVA'
        assert variants[2]['raw'][3:14]==primary['spelling'].upper()=='VERCSIOROVA'
        witnesses=[]
        for coordinate in C:
            cipher=candidate['ciphertext'].replace('?',coordinate)
            text=decrypt(cipher,key['column_rank_order'],key['square'])
            assert encrypt(text,key['column_rank_order'],key['square'])==cipher
            assert all(a=='?'or a==b for a,b in zip(candidate['raw'],text))
            witnesses.append({'source_mask_index':1,'coordinate':coordinate,'name':text[3:14],
                              'plaintext':text,'ciphertext':cipher,'reencryption_exact':True})
        assert ''.join(sorted(w['plaintext'][12]for w in witnesses))=='23BHSV'
        path=ROOT/data['case'];text=path.read_text();assert text.count(expected_legend(path))==1
        assert re.findall(r'```text\n(.*?)\n```',text,re.S)==['\n'.join(r['source_rows']),raw['raw']]+[v['raw']for v in variants]
        assert re.findall(r'^> (.*)$',text,re.M)==[r['readable_german']]
        records.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),
                        'ciphertext':base,'model_to_source_indices':mapping,**raw,
                        'readable_candidate':candidate,'readable_german':r['readable_german'],
                        'name_variants':variants[1:],'remaining_mask_full_witnesses':witnesses,
                        'remaining_name_domain':'23BHSV','source_frame_changed':False,
                        'actual_markdown_strings_checked':True})
    return {'schema':'adfgvx-p152-crossing-fragment-certificate-v1','authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':data['indexing'],
            'summary':{'physical_records':1,'printed_source_slots':128,'valid_source_coordinates':125,
                       'plaintext_positions':64,'baseline_fixed_positions':61,'candidate_fixed_positions':63,
                       'known_coordinate_substitutions':7,'source_mask_fills':2,
                       'inserted_or_excluded_source_slots':0,'remaining_source_masks':1},
            'records':records,'independent_place_attestation':attestation,
            'prior_credit':data['prior_credit'],'limits':data['limits']},evidence


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true');parser.add_argument('--pdf',type=Path)
    parser.add_argument('--attestation-pdf',type=Path);args=parser.parse_args()
    result,evidence=build(args.pdf,args.attestation_pdf);path=HERE/'certificates.json'
    if args.verify:assert result==load(path)
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary'],'source_evidence':evidence['summary'],
                      'attestation_pdf_checked':args.attestation_pdf is not None},indent=2))
