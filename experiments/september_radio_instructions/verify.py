#!/usr/bin/env python3
"""Verify native September multipart boundaries, source annotations and key labels.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,sha,verify_crops


def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());k=d['key'];assert k==next(x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']if x['id']==k['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/d[field]['path'])==d[field]['sha256']
    for image in d['source_images']:assert sha(HERE/image['path'])==image['sha256']
    if pdf:verify_crops(pdf,d['source'],d['source_images'],HERE)
    records=[]
    for s in d['records']:
        literal=''.join(s['source_rows']).replace(' ','');assert len(literal)==s['source_slots']==s['advertised_length']
        cipher=''.join(ch if ch in C else'?'for ch in literal);mapping=list(range(len(cipher)));raw=inspect(cipher,k,mapping);assert raw['raw']==s['expected_raw']
        proposal=repair(s['readable_candidate'],cipher,k,mapping,literal);optional=None
        if 'optional_repeated_label_candidate'in s:
            assert s['id']=='p61_A'and raw['raw'][31:36]=='77?77'and raw['raw'][37:42]=='77777'
            optional=repair(s['optional_repeated_label_candidate'],cipher,k,mapping,literal)
            assert optional['known_coordinate_substitutions']==proposal['known_coordinate_substitutions']
            assert len(optional['erased_coordinate_fills'])==len(proposal['erased_coordinate_fills'])+1
            assert optional['fixed_positions']==proposal['fixed_positions']+1
        annotations=[]
        for a in d['source_annotations']:
            if a['record']!=s['id']:continue
            i=a['source_index'];assert literal[i]==a['typed'];changed=cipher[:i]+a['annotated']+cipher[i+1:];ann=inspect(changed,k,mapping)
            assert s['id']=='p57_A3'and ann['raw']==s['readable_candidate']
            annotations.append({**a,'applied_raw':ann['raw'],'observed_coordinate_substitutions':1})
        assert re.sub('[^A-Z0-9?]','',s['readable_german'].upper()).replace('X','')==s['readable_candidate'].replace('X','')
        assert '> '+s['readable_german']in(ROOT/s['case_path']).read_text()
        records.append({'id':s['id'],'literal_source':literal,'literal_printed_rows':s['source_rows'],'source_slots':len(literal),'valid_coordinates':sum(ch in C for ch in literal),'ciphertext':cipher,'model_to_source_indices':mapping,**raw,'readable_candidate':proposal,'source_annotations':annotations,'optional_repeated_label_candidate':optional})
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots']for r in records),'valid_source_coordinates':sum(r['valid_coordinates']for r in records),'plaintext_positions':sum(len(r['raw'])for r in records),'baseline_fixed_positions':sum(r['fixed_positions']for r in records),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in records),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in records),'source_mask_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in records),'frame_insertions':0,'frame_deletions':0,'published_key_changed':False}
    assert summary['printed_source_slots']==798 and summary['plaintext_positions']==399
    assert summary['known_coordinate_substitutions']==10 and summary['source_mask_fills']==9
    assert summary['candidate_fixed_positions']==398
    return {'schema':'adfgvx-september-radio-instructions-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':records,'headers':d['headers'],'literal_glyph_notes':d['literal_glyph_notes'],'limits':d['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))

if __name__=='__main__':main()
