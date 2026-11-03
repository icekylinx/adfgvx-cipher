#!/usr/bin/env python3
"""Verify November 2 acknowledgment copies and personnel orders.

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


def frame(literal, boundary=None):
    native=''.join(ch if ch in C else '?' for ch in literal)
    if boundary is None:return native,list(range(len(native)))
    return native[:boundary]+'?'+native[boundary:],list(range(boundary))+[None]+list(range(boundary,len(native)))


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/data[field]['path'])==data[field]['sha256']
    for image in data['source_images']:assert sha(HERE/image['path'])==image['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','');assert len(literal)==source['source_slots']
        boundary=source.get('analysis_frame',{}).get('insert_unknown_at_source_boundary')
        cipher,mapping=frame(literal,boundary);assert len(cipher)==source['advertised_length']
        raw=inspect(cipher,key,mapping);assert raw['raw']==source['expected_raw']
        proposed=repair(source['readable_candidate'],cipher,key,mapping,literal)
        if 'readable_german' in source:
            assert re.sub('[^A-Z0-9?]','',source['readable_german'].upper()).replace('X','')==source['readable_candidate'].replace('X','')
            assert '> '+source['readable_german'] in (ROOT/source['case_path']).read_text()
        variants=[]
        if boundary is not None:
            assert source['id']=='p104_D' and len(literal)==149 and literal[100:104]=='ADAG'
            for b in range(100,105):
                base,mp=frame(literal,b);prior=inspect(base,key,mp);candidate=repair(source['readable_candidate'],base,key,mp,literal)
                variants.append({'insert_unknown_at_source_boundary':b,'raw':prior['raw'],'raw_fixed_positions':prior['fixed_positions'],
                                 'mapping':mp,'candidate':candidate})
            assert [len(v['candidate']['known_coordinate_substitutions']) for v in variants]==[2,1,0,0,1]
            zero=[v for v in variants if not v['candidate']['known_coordinate_substitutions']]
            assert [v['insert_unknown_at_source_boundary']for v in zero]==[102,103]
            assert zero[0]['candidate']['ciphertext']==zero[1]['candidate']['ciphertext']==proposed['ciphertext']
            assert zero[0]['candidate']['ciphertext'][100:105]=='ADAAG'
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],'ciphertext':cipher,
                        'source_slots':len(literal),'valid_coordinates':sum(ch in C for ch in literal),'analysis_frame_slots':len(cipher),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':proposed,'conditional_gap_alignments':variants,
                        'all_changed_plaintext_positions':[{'plaintext_index':i,'from':a,'to':b} for i,(a,b) in enumerate(zip(raw['raw'],proposed['raw'])) if a!=b]})
    byid={r['id']:r for r in records};a,b=byid['p104_A3'],byid['p106_A3']
    comparison={'source_differences':[{'source_index':i,'p104':x,'p106':y}for i,(x,y)in enumerate(zip(a['literal_source'],b['literal_source']))if x!=y],
                'plaintext_differences':[{'plaintext_index':i,'p104':x,'p106':y}for i,(x,y)in enumerate(zip(a['raw'],b['raw']))if x!=y],
                'header_dates':['1/11','2/11'],'preserved_without_repair':True}
    assert len(comparison['source_differences'])==len(comparison['plaintext_differences'])==1
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots']for r in records),
             'valid_source_coordinates':sum(r['valid_coordinates']for r in records),'modeled_coordinates':sum(len(r['ciphertext'])for r in records),
             'plaintext_positions':sum(len(r['raw'])for r in records),'baseline_fixed_positions':sum(r['fixed_positions']for r in records),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in records),
             'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in records),
             'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in records),
             'source_mask_fills':sum(sum(e['source_index']is not None for e in r['readable_candidate']['erased_coordinate_fills'])for r in records),
             'inserted_slot_fills':sum(sum(e['source_index']is None for e in r['readable_candidate']['erased_coordinate_fills'])for r in records),
             'source_deletions':0,'published_key_changed':False}
    assert summary['printed_source_slots']==1175 and summary['modeled_coordinates']==1176
    return {'schema':'adfgvx-nov2-acknowledgments-and-personnel-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':summary,'records':records,'headers':data['headers'],'near_copy_comparison':comparison,
            'literal_glyph_notes':data['literal_glyph_notes'],'source_annotations':data['source_annotations'],
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
