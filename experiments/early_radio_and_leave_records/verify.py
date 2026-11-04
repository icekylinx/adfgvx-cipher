#!/usr/bin/env python3
"""Verify four native radio/personnel records and their displayed readings.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,sha,verify_crops

def check_place_completion(source, raw, candidate, cipher, key, mapping, literal):
    review=source['place_completion']
    donor_path=ROOT/review['donor_input_path']
    assert sha(donor_path)==review['donor_input_sha256']
    donor_data=json.loads(donor_path.read_text())
    donor=next(r for r in donor_data['records'] if r['id']==review['donor_record_id'])
    assert donor_data['key']==key
    donor_literal=''.join(donor['source_rows']).replace(' ','')
    assert len(donor_literal)==donor['source_slots']==56 and set(donor_literal)<=set(C)
    donor_raw=inspect(donor_literal,key,list(range(len(donor_literal))))
    assert donor_raw['raw']==donor['expected_raw'] and donor_raw['fixed_positions']==28
    assert donor_raw['raw'][16:28]==review['donor_native_place']=='NAGQBESCEREK'
    assert candidate['raw'][53:65]==review['target_place']=='NAGQBECSEREK'
    prior=repair(review['previous_candidate'],cipher,key,mapping,literal)
    assert prior['fixed_positions']==review['previous_fixed_positions']==96
    assert candidate['fixed_positions']==98
    assert prior['known_coordinate_substitutions']==candidate['known_coordinate_substitutions']
    old_fills={e['source_index']:e for e in prior['erased_coordinate_fills']}
    new_fills={e['source_index']:e for e in candidate['erased_coordinate_fills']}
    assert all(new_fills[i]==e for i,e in old_fills.items())
    assert sorted(new_fills.keys()-old_fills.keys())==[6,7]
    assert [(i,a,b) for i,(a,b) in enumerate(zip(prior['raw'],candidate['raw'])) if a!=b]==[(54,'?','A'),(63,'?','E')]
    for letter in review['new_letters']:
        before=raw['positions'][letter['plaintext_index']]
        after=candidate['positions'][letter['plaintext_index']]
        assert (before['pair'],before['domain'],before['source_indices'])==(letter['pair_before'],letter['domain'],letter['source_indices'])
        assert (after['pair'],after['raw'])==(letter['pair_after'],letter['after'])
        assert literal[letter['filled_source_index']]=='-' and new_fills[letter['filled_source_index']]['to']==letter['coordinate']=='F'
    matches=[]
    for span in review['matching_spans']:
        text=span['text'];a=span['donor_plaintext_start'];b=span['target_plaintext_start']
        assert donor_raw['raw'][a:a+len(text)]==candidate['raw'][b:b+len(text)]==text
        matches.append({**span,'donor_observed_pairs':[{'plaintext_index':p['plaintext_index'],'pair':p['pair'],'source_indices':p['source_indices']} for p in donor_raw['positions'][a:a+len(text)]]})
    return {'donor_record':donor['id'],'donor_input_path':review['donor_input_path'],'donor_input_sha256':review['donor_input_sha256'],
            'donor_native_raw':donor_raw['raw'],'matching_spans':matches,'new_letters':review['new_letters'],
            'previous_fixed_positions':96,'candidate_fixed_positions':98,'new_observed_substitutions':0,'new_source_mask_fills':2,
            'interpretation':review['interpretation']}

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text())
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    keys={k['id']:k for k in data['keys']}
    for key in keys.values():assert key==published[key['id']]
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:
        assert sha(base/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        key=keys[source['key_id']]
        literal=''.join(source['source_rows']).replace(' ','')
        assert len(literal)==source['source_slots']==source['advertised_length']
        cipher=''.join(c if c in C else '?' for c in literal)
        mapping=list(range(len(cipher)));raw=inspect(cipher,key,mapping)
        assert raw['raw']==source['expected_raw']
        if source['id']=='p87_A1':
            review=source['transcription_review']
            assert literal[review['source_index']]==review['source_reading']=='D'
            assert raw['positions'][review['plaintext_index']]['raw']==review['plaintext']=='X'
            assert review['source_index'] in raw['positions'][review['plaintext_index']]['source_indices']
            assert raw['fixed_positions']==83
        candidate=repair(source['readable_candidate'],cipher,key,mapping,literal)
        costs=[len(candidate['known_coordinate_substitutions']),len(candidate['erased_coordinate_fills'])]
        assert costs==source['expected_costs']
        canonical=re.sub('[^A-Z0-9?]','',source['readable_german'].upper()).replace('X','')
        assert canonical==source['readable_candidate'].replace('X','')
        assert '> '+source['readable_german'] in (ROOT/source['case_path']).read_text()
        place_review=check_place_completion(source,raw,candidate,cipher,key,mapping,literal) if 'place_completion' in source else None
        records.append({'id':source['id'],'key_id':key['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':cipher,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'transcription_review':source.get('transcription_review'),
                        **({'place_completion':place_review} if place_review else {}),
                        'all_changed_plaintext_positions':[{'plaintext_index':i,'from':a,'to':b} for i,(a,b) in enumerate(zip(raw['raw'],candidate['raw'])) if a!=b]})
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots'] for r in records),
             'valid_source_coordinates':sum(r['valid_coordinates'] for r in records),'modeled_coordinates':sum(len(r['ciphertext']) for r in records),
             'plaintext_positions':sum(len(r['raw']) for r in records),'baseline_fixed_positions':sum(r['fixed_positions'] for r in records),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions'] for r in records),
             'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions']) for r in records),
             'source_mask_fills':sum(len(r['readable_candidate']['erased_coordinate_fills']) for r in records),
             'unfilled_source_mask_coordinates':sum(r['readable_candidate']['ciphertext'].count('?') for r in records),
             'frame_changes':0,'published_key_changed':False}
    assert [summary[k] for k in ['physical_records','printed_source_slots','valid_source_coordinates','plaintext_positions','baseline_fixed_positions','candidate_fixed_positions','known_coordinate_substitutions','source_mask_fills','unfilled_source_mask_coordinates']]==[4,812,798,406,392,403,3,11,3]
    assert all(r['ciphertext']==r['readable_candidate']['ciphertext'] for r in records[:2])
    assert records[1]['readable_candidate']['full_plaintext_reencryption_verified']
    return {'schema':'adfgvx-early-radio-and-leave-records-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':records,
            'headers':data['headers'],'literal_glyph_notes':data['literal_glyph_notes'],'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))

if __name__=='__main__':main()
