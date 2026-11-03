#!/usr/bin/env python3
"""Verify one native divisional-position fragment and optional geography and their displayed readings.

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
    for key in keys.values():assert key==published[key['id']]
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:
        assert sha(base/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    reference=data['contextual_geographical_reference']
    assert sha(ROOT/reference['input_path'])==reference['input_sha256']
    assert sha(ROOT/reference['source_image_path'])==reference['source_image_sha256']
    earlier=json.loads((ROOT/reference['input_path']).read_text())
    contextual_source=next(r for r in earlier['records'] if r['id']==reference['id'])
    contextual_literal=''.join(contextual_source['source_rows']).replace(' ','')
    assert len(contextual_literal)==240 and all(c in C for c in contextual_literal)
    contextual=inspect(contextual_literal,keys['Nov22-24'],list(range(240)))
    assert contextual['raw']==contextual_source['editorial_recipe']['text']
    a,b=reference['plaintext_start_index'],reference['plaintext_end_index_exclusive']
    assert contextual['raw'][a:b]==reference['word']=='OROSHAZA'
    context_proof={**reference,'raw':contextual['raw'],'word_pairs':contextual['positions'][a:b],
                   'known_coordinate_substitutions':0,'source_mask_fills':0,'counted_as_new_record':False}
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
        if source.get('editorial_terminal_question_mark'):
            assert canonical.endswith('?') and '?' not in source['readable_candidate']
            canonical=canonical[:-1]
        assert canonical==source['readable_candidate'].replace('X','')
        assert '> '+source['readable_german'] in (ROOT/source['case_path']).read_text()
        alternative=source['geographical_alternative']
        optional=repair(alternative['candidate'],cipher,key,mapping,literal)
        assert [len(optional['known_coordinate_substitutions']),len(optional['erased_coordinate_fills'])]==alternative['expected_costs']==[18,14]
        assert optional['fixed_positions']==143 and optional['raw'].count('?')==7
        assert re.sub('[^A-Z0-9?]','',alternative['readable_german'].upper()).replace('X','')==optional['raw'].replace('X','')
        assert '> '+alternative['readable_german'] in (ROOT/source['case_path']).read_text()
        primary_fills={e['source_index']:e['to'] for e in candidate['erased_coordinate_fills']}
        extras=[e for e in optional['erased_coordinate_fills'] if e['source_index'] not in primary_fills]
        assert len(extras)==1 and extras[0]['source_index']==144 and extras[0]['to']=='X'
        for e in optional['erased_coordinate_fills']:
            if e['source_index'] in primary_fills:assert e['to']==primary_fills[e['source_index']]
        records.append({'id':source['id'],'key_id':key['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':cipher,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'geographical_alternative':optional,'geography_extra_mask_fills':extras,
                        'all_changed_plaintext_positions':[{'plaintext_index':i,'from':a,'to':b} for i,(a,b) in enumerate(zip(raw['raw'],candidate['raw'])) if a!=b]})
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots'] for r in records),
             'valid_source_coordinates':sum(r['valid_coordinates'] for r in records),'modeled_coordinates':sum(len(r['ciphertext']) for r in records),
             'plaintext_positions':sum(len(r['raw']) for r in records),'baseline_fixed_positions':sum(r['fixed_positions'] for r in records),
             'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions'] for r in records),
             'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions']) for r in records),
             'source_mask_fills':sum(len(r['readable_candidate']['erased_coordinate_fills']) for r in records),
             'unfilled_source_mask_coordinates':sum(r['readable_candidate']['ciphertext'].count('?') for r in records),
             'frame_changes':0,'published_key_changed':False}
    assert [summary[k] for k in ['physical_records','printed_source_slots','valid_source_coordinates','plaintext_positions','baseline_fixed_positions','candidate_fixed_positions','known_coordinate_substitutions','source_mask_fills','unfilled_source_mask_coordinates']]==[1,300,279,150,129,142,0,13,8]
    return {'schema':'adfgvx-southern-hungary-positions-part2-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':records,
            'contextual_geographical_reference':context_proof,'headers':data['headers'],'literal_glyph_notes':data['literal_glyph_notes'],'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))

if __name__=='__main__':main()
