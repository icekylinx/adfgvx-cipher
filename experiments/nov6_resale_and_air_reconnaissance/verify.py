#!/usr/bin/env python3
"""Verify p144 native records and the independently observed p152 continuation.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,sha,verify_crops

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text())
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    keys={k['id']:k for k in data['keys']}
    for k in keys.values():assert k==published[k['id']]
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
        candidate=repair(source['readable_candidate'],cipher,key,mapping,literal)
        costs=[len(candidate['known_coordinate_substitutions']),len(candidate['erased_coordinate_fills'])]
        assert costs==source['expected_costs']
        canonical=re.sub('[^A-Z0-9?]','',source['readable_german'].upper()).replace('X','')
        assert canonical==source['readable_candidate'].replace('X','')
        assert '> '+source['readable_german'] in (ROOT/source['case_path']).read_text()
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':cipher,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'plaintext_index':i,'from':a,'to':b} for i,(a,b) in enumerate(zip(raw['raw'],candidate['raw'])) if a!=b]})
    cross=data['cross_witnesses'];assert sha(ROOT/cross['certificate_path'])==cross['certificate_sha256']
    old=json.loads((ROOT/cross['certificate_path']).read_text())
    witnesses=[];key=keys['Nov4-6']
    for w in cross['records']:
        assert w==next(x for x in old['source_decryptions'] if x['id']==w['id'])
        rebuilt=w['source_ciphertext'];mapping=list(range(len(rebuilt)))
        for e in w['edits']:
            assert e['operation']=='insert';i=e['index'];rebuilt=rebuilt[:i]+e['value']+rebuilt[i:];mapping.insert(i,None)
        assert rebuilt==w['corrected_ciphertext']
        raw=inspect(rebuilt,key,mapping);assert raw['raw']==w['plaintext']
        witnesses.append({'id':w['id'],'source_ciphertext':w['source_ciphertext'],'corrected_ciphertext':rebuilt,
                          'frame_edits':w['edits'],'model_to_source_indices':mapping,**raw})
    new=records[0];native_old=next(w for w in witnesses if w['id']=='p152_E_part2')
    target=new['readable_candidate']['raw'];support=[]
    for i,ch in enumerate(target):
        observed=[]
        for witness in [new,native_old]:
            if witness['raw'][i]==ch:
                observed.append({'id':witness['id'],**witness['positions'][i]})
        assert observed
        support.append({'plaintext_index':i,'candidate':ch,'native_raw_witnesses':observed})
    assert len(target)==135
    change=new['readable_candidate']['known_coordinate_substitutions']
    assert len(change)==1 and change[0]['source_index']==146 and change[0]['from']=='D' and change[0]['to']=='A'
    assert new['ciphertext'][160:165]=='XAFFF'
    p136=next(w for w in witnesses if w['id']=='p136_B2')
    assert p136['source_ciphertext'][160:164]=='XAFF' and p136['corrected_ciphertext'][160:165]=='XAFFF'
    assert native_old['source_ciphertext'][160:165]=='XAFFF'
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots'] for r in records),
             'valid_source_coordinates':sum(r['valid_coordinates'] for r in records),'modeled_coordinates':sum(len(r['ciphertext']) for r in records),
             'plaintext_positions':sum(len(r['raw']) for r in records),'baseline_fixed_positions':sum(r['fixed_positions'] for r in records),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions'] for r in records),
             'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions']) for r in records),
             'source_mask_fills':sum(len(r['readable_candidate']['erased_coordinate_fills']) for r in records),
             'new_record_frame_changes':0,'published_key_changed':False,'older_witnesses_counted_as_new':False}
    assert [summary[k] for k in ['physical_records','printed_source_slots','valid_source_coordinates','plaintext_positions','baseline_fixed_positions','candidate_fixed_positions','known_coordinate_substitutions','source_mask_fills']]==[2,412,402,206,196,204,6,8]
    return {'schema':'adfgvx-nov6-resale-and-air-reconnaissance-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':records,
            'older_continuation_witnesses':witnesses,'p144_A2_native_raw_support_for_all_positions':support,
            'p136_short_group_support':{'source_start':160,'old_literal_group':'XAFF','new_literal_group':'XAFFF','old_supplied_coordinate':'F','old_model_boundary':164,'historical_position_among_identical_Fs_not_unique':True},
            'headers':data['headers'],'literal_glyph_notes':data['literal_glyph_notes'],'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))

if __name__=='__main__':main()
