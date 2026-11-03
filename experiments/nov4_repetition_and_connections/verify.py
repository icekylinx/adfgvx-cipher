#!/usr/bin/env python3
"""Verify the native November 4 repetition and communications records.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C, inspect, repair, sha, verify_crops


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:
        assert sha(base/data[field]['path'])==data[field]['sha256']
    for image in data['source_images']:assert sha(HERE/image['path'])==image['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','')
        assert len(literal)==source['source_slots']==source['advertised_length']
        cipher=''.join(ch if ch in C else '?' for ch in literal)
        mapping=list(range(len(cipher)));raw=inspect(cipher,key,mapping)
        assert raw['raw']==source['expected_raw']
        proposed=repair(source['readable_candidate'],cipher,key,mapping,literal)
        assert proposed['full_plaintext_reencryption_verified']
        assert re.sub('[^A-Z0-9]', '', source['readable_german'].upper()).replace('X','')==source['readable_candidate'].replace('X','')
        case='cases/finance/cash_arrival_acknowledgment.md' if source['id']=='p122_C' else 'cases/radio/nov4_repetition_and_connections.md'
        assert '> '+source['readable_german'] in (ROOT/case).read_text()
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':cipher,'source_slots':len(literal),'valid_coordinates':sum(ch in C for ch in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':proposed,
                        'all_changed_plaintext_positions':[{'plaintext_index':i,'from':a,'to':b} for i,(a,b) in enumerate(zip(raw['raw'],proposed['raw'])) if a!=b]})
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots'] for r in records),
             'valid_source_coordinates':sum(r['valid_coordinates'] for r in records),
             'modeled_coordinates':sum(len(r['ciphertext']) for r in records),
             'plaintext_positions':sum(len(r['raw']) for r in records),
             'baseline_fixed_positions':sum(r['fixed_positions'] for r in records),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions'] for r in records),
             'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions']) for r in records),
             'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills']) for r in records),
             'source_deletions':0,'published_key_changed':False}
    assert [r['source_slots'] for r in records]==[236,236,262,182,114]
    assert summary['printed_source_slots']==1030 and summary['plaintext_positions']==515
    assert summary['baseline_fixed_positions']==514 and summary['candidate_fixed_positions']==515
    return {'schema':'adfgvx-nov4-repetition-and-connections-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':summary,'records':records,'headers':data['headers'],
            'literal_glyph_notes':data['literal_glyph_notes'],'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
