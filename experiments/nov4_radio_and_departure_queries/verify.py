#!/usr/bin/env python3
"""Verify radio/departure queries with an explicit ambiguous-glyph frame.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,sha,verify_crops


def frame(literal,excluded=()):
    mapping=[i for i in range(len(literal))if i not in excluded]
    return ''.join(literal[i]if literal[i]in C else'?'for i in mapping),mapping


def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());k=d['key'];assert k==next(key for key in json.loads((ROOT/'data/keys.json').read_text())['keys']if key['id']==k['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/d[field]['path'])==d[field]['sha256']
    for image in d['source_images']:assert sha(HERE/image['path'])==image['sha256']
    if pdf:verify_crops(pdf,d['source'],d['source_images'],HERE)
    records=[]
    for s in d['records']:
        literal=''.join(s['source_rows']).replace(' ','');assert len(literal)==s['source_slots']
        excluded=s.get('analysis_frame',{}).get('exclude_source_indices',[]);cipher,mapping=frame(literal,excluded)
        assert len(cipher)==s['advertised_length'];raw=inspect(cipher,k,mapping);assert raw['raw']==s['expected_raw']
        proposal=repair(s['readable_candidate'],cipher,k,mapping,literal);alternatives=[]
        if excluded:
            assert s['id']=='p120_A'and literal[185:191]=='XXFTVA'and excluded==[188]
            for i in range(185,191):
                alt,mp=frame(literal,[i]);r=repair(s['readable_candidate'],alt,k,mp,literal)
                alternatives.append({'excluded_source_index':i,'excluded_literal':literal[i],'excluded_valid_coordinates':int(literal[i]in C),
                                     'known_coordinate_substitutions':r['known_coordinate_substitutions'],'erased_coordinate_fills':r['erased_coordinate_fills']})
        optional=None
        if 'optional_named_candidate'in s:
            optional=repair(s['optional_named_candidate'],cipher,k,mapping,literal)
            assert len(optional['known_coordinate_substitutions'])==len(proposal['known_coordinate_substitutions'])+2
            assert optional['fixed_positions']==proposal['fixed_positions']
        if 'readable_german'in s:
            display=s['readable_german']
            for punctuation in s.get('editorial_question_punctuation_after',[]):
                assert display.count(punctuation+'?')==1;display=display.replace(punctuation+'?',punctuation)
            assert re.sub('[^A-Z0-9?]','',display.upper()).replace('X','')==s['readable_candidate'].replace('X','')
            assert '> '+s['readable_german']in(ROOT/s['case_path']).read_text()
        records.append({'id':s['id'],'literal_source':literal,'literal_printed_rows':s['source_rows'],'source_slots':len(literal),'valid_coordinates':sum(ch in C for ch in literal),
                        'ciphertext':cipher,'analysis_frame_slots':len(cipher),'model_to_source_indices':mapping,**raw,'readable_candidate':proposal,
                        'excluded_source_slots':[{'source_index':i,'literal':literal[i],'valid_coordinate':literal[i]in C}for i in excluded],
                        'local_single_exclusion_prices':alternatives,'optional_named_candidate':optional})
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots']for r in records),'valid_source_coordinates':sum(r['valid_coordinates']for r in records),
             'modeled_coordinates':sum(len(r['ciphertext'])for r in records),'plaintext_positions':sum(len(r['raw'])for r in records),'baseline_fixed_positions':sum(r['fixed_positions']for r in records),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in records),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in records),
             'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in records),'source_mask_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in records),
             'inserted_slot_fills':0,'source_deletions':1,'excluded_valid_coordinates':0,'excluded_masked_slots':1,'published_key_changed':False}
    assert summary['printed_source_slots']==887 and summary['modeled_coordinates']==886
    assert summary['known_coordinate_substitutions']==17 and summary['source_mask_fills']==9
    return {'schema':'adfgvx-nov4-radio-and-departure-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All indices are zero-based.','summary':summary,'records':records,'headers':d['headers'],'literal_glyph_notes':d['literal_glyph_notes'],'limits':d['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
