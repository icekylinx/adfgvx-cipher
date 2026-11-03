#!/usr/bin/env python3
"""Verify the central-gap partial source editions and live Markdown displays.

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


def build(pdf=None):
    data=load(HERE/'inputs.json');key=data['key']
    assert key==next(k for k in load(ROOT/'data/keys.json')['keys']if k['id']=='Nov7-9')
    evidence=verify_source_evidence(pdf,data['source'],data['source_images'],HERE)
    assert sha(HERE/'prior_snapshot.json')==data['prior_snapshot_sha256']
    prior=load(HERE/'prior_snapshot.json')
    case=ROOT/data['case'];text=case.read_text();assert text.count(expected_legend(case))==1
    out=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split())
        assert len(literal)==r['source_slots']==r['advertised_length']
        assert set(literal)<=set(C)
        mapping=list(range(len(literal)));raw=inspect(literal,key,mapping)
        assert raw['raw']==r['expected_raw']
        assert decrypt(literal,key['column_rank_order'],key['square'])==raw['raw']
        assert encrypt(raw['raw'],key['column_rank_order'],key['square'])==literal
        candidate=repair(r['edited_output'],literal,key,mapping,literal)
        assert len(candidate['known_coordinate_substitutions'])==r['expected_substitutions']
        assert len(candidate['erased_coordinate_fills'])==r['expected_mask_fills']
        assert encrypt(candidate['raw'],key['column_rank_order'],key['square'])==candidate['ciphertext']
        assert fold(r['readable_german'])==fold(candidate['raw'])
        assert all(field in raw['raw']and field in candidate['raw']and field in r['readable_german']for field in r['protected_fields'])
        heading='## '+r['id'].replace('_',' ')+'\n';assert text.count(heading)==1
        section=text.split(heading,1)[1].split('\n## ',1)[0]
        assert re.findall(r'```text\n(.*?)\n```',section,re.S)==['\n'.join(r['source_rows']),raw['raw'],candidate['raw']]
        assert re.findall(r'^> (.*)$',section,re.M)==[r['readable_german']]
        if r['id']=='p164_D':
            old=prior['earlier_p164_D_context']
            assert literal==old['raw_ciphertext']and raw['raw']==old['plaintext']
            assert [(e['source_index'],e['from'],e['to'])for e in candidate['known_coordinate_substitutions']]==[(50,'G','D'),(73,'G','D')]
        out.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),
                    'ciphertext':literal,'model_to_source_indices':mapping,**raw,
                    'readable_candidate':candidate,'readable_german':r['readable_german'],
                    'actual_markdown_mapping_checked':True,'ordinary_reencryption_exact':True})
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),
             'plaintext_positions':sum(len(r['raw'])for r in out),
             'baseline_fixed_positions':sum(r['fixed_positions']for r in out),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),
             'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),
             'source_mask_fills':0,'inserted_or_excluded_source_slots':0}
    return {'schema':'adfgvx-gap21-central-certificate-v1','authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':data['indexing'],
            'summary':summary,'records':out,'prior_credit':data['prior_credit']},evidence


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');parser.add_argument('--pdf',type=Path);args=parser.parse_args()
    result,evidence=build(args.pdf);path=HERE/'certificates.json'
    if args.verify:assert result==load(path)
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary'],'source_evidence':evidence['summary']},indent=2))
