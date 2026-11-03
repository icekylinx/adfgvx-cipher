#!/usr/bin/env python3
"""Verify mutually supporting Ringbahn-key source witnesses.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,sha,verify_crops


def frame(literal,boundary=None):
    native=''.join(ch if ch in C else '?' for ch in literal)
    return (native,list(range(len(native)))) if boundary is None else (native[:boundary]+'?'+native[boundary:],list(range(boundary))+[None]+list(range(boundary,len(native))))


def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());k=d['key']
    assert k==next(key for key in json.loads((ROOT/'data/keys.json').read_text())['keys']if key['id']==k['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/d[field]['path'])==d[field]['sha256']
    for image in d['source_images']:assert sha(HERE/image['path'])==image['sha256']
    w=d['independent_witness'];assert sha(ROOT/w['input_path'])==w['input_sha256']
    original=json.loads((ROOT/w['input_path']).read_text());assert w['records']==[m for m in original['messages']if m['id'].startswith('p211_B_lower')]
    assert sha(ROOT/w['source_crop']['path'])==w['source_crop']['sha256']
    if pdf:
        verify_crops(pdf,d['source'],d['source_images'],HERE)
        verify_crops(pdf,d['source'],[w['source_crop']],ROOT)
    records=[];mutual=[]
    for s,old in zip(d['records'],w['records']):
        lit=''.join(s['source_rows']).replace(' ','');assert len(lit)==s['source_slots']
        b=s.get('analysis_frame',{}).get('insert_unknown_at_source_boundary');cipher,mapping=frame(lit,b)
        assert len(cipher)==s['advertised_length'];raw=inspect(cipher,k,mapping);assert raw['raw']==s['expected_raw']
        candidate=repair(s['readable_candidate'],cipher,k,mapping,lit);assert candidate['full_plaintext_reencryption_verified']
        oldlit=''.join(old['source_rows']).replace(' ','');oldcipher,oldmap=frame(oldlit);oldraw=inspect(oldcipher,k,oldmap)
        assert oldraw['raw']==old['expected_raw'] and len(oldraw['raw'])==len(raw['raw'])
        support=[]
        for i,(a,z)in enumerate(zip(raw['raw'],candidate['raw'])):
            if a!=z:
                assert oldraw['raw'][i]==z
                support.append({'plaintext_index':i,'raw':a,'candidate':z,'independent_copy_literal':oldraw['raw'][i],
                                'new_pair_indices':raw['positions'][i]['source_indices'],'old_pair_indices':oldraw['positions'][i]['source_indices']})
        reverse=[]
        for patch in old['editorial_patches']:
            i=patch['plaintext_index'];assert raw['raw'][i]==patch['proposed_symbol']
            reverse.append({'old_plaintext_index':i,'old_raw':oldraw['raw'][i],'old_proposal':patch['proposed_symbol'],'new_literal':raw['raw'][i]})
        gap=[]
        if b is not None:
            assert s['id']=='p145_B2' and lit[30:34]=='XFVA' and len(lit)==183
            for i in range(30,35):
                alt,mp=frame(lit,i);r=repair(s['readable_candidate'],alt,k,mp,lit)
                gap.append({'boundary':i,'substitutions':r['known_coordinate_substitutions'],'fills':r['erased_coordinate_fills']})
            assert [len(x['substitutions'])for x in gap]==[6,5,4,3,4]
            assert candidate['ciphertext']==oldcipher and candidate['ciphertext'][30:35]=='XFVFA'
        if 'readable_german'in s:
            assert re.sub('[^A-Z0-9]','',s['readable_german'].upper()).replace('X','')==s['readable_candidate'].replace('X','')
            assert '> '+s['readable_german'] in (ROOT/'cases/radio/nov6_ringbahn_key_witnesses.md').read_text()
        records.append({'id':s['id'],'literal_source':lit,'literal_printed_rows':s['source_rows'],'source_slots':len(lit),'valid_coordinates':sum(ch in C for ch in lit),'ciphertext':cipher,'analysis_frame_slots':len(cipher),'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'local_gap_prices':gap})
        mutual.append({'record':s['id'],'independent_record':old['id'],'new_repairs_directly_supported_by_old_raw':support,'old_repairs_directly_supported_by_new_raw':reverse,
                       'literal_cipher_differences_in_declared_frames':[{'frame_index':i,'new':a,'old':z}for i,(a,z)in enumerate(zip(cipher,oldcipher))if a!=z],
                       'literal_plaintext_differences':[{'plaintext_index':i,'new':a,'old':z}for i,(a,z)in enumerate(zip(raw['raw'],oldraw['raw']))if a!=z]})
    summary={'physical_records':len(records),'printed_source_slots':sum(r['source_slots']for r in records),'valid_source_coordinates':sum(r['valid_coordinates']for r in records),'modeled_coordinates':sum(len(r['ciphertext'])for r in records),'plaintext_positions':sum(len(r['raw'])for r in records),'baseline_fixed_positions':sum(r['fixed_positions']for r in records),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in records),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in records),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in records),'source_mask_fills':0,'inserted_slot_fills':1,'source_deletions':0,'published_key_changed':False}
    assert summary['printed_source_slots']==531 and summary['modeled_coordinates']==532
    assert sum(len(x['old_repairs_directly_supported_by_new_raw'])for x in mutual)==4
    return {'schema':'adfgvx-nov6-ringbahn-witnesses-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':records,'mutual_source_support':mutual,'headers':d['headers'],'limits':d['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
