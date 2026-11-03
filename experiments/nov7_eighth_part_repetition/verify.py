#!/usr/bin/env python3
"""Verify an eighth-part repetition request with one explicit frame exclusion.
ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt,untranspose
from experiments.romanian_pacification_consultation.verify import inspect,repair,permutation
C='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def literal(r):return ''.join(''.join(r['source_rows']).split())
def frame(r,excluded):
    src=literal(r);mp=[i for i in range(len(src))if i not in excluded]
    return ''.join(src[i]if src[i]in C else'?'for i in mp),mp

def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());key=d['key'];assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']if k['id']==key['id'])
    assert [r['id']for r in d['records']]==['p155_C1','p155_C2']
    for path,digest in d['prior_artifacts'].items():assert sha(HERE/path)==digest
    for crop in d['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf)==d['source']['pdf_sha256']and pdf.stat().st_size==d['source']['pdf_bytes'];doc=fitz.open(pdf)
        for crop in d['source_images']:
            pix=doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(crop['render_scale'],crop['render_scale']),clip=fitz.Rect(*crop['crop_pdf_points']));im=Image.open(HERE/crop['path']).convert('RGB')
            assert im.size==(pix.width,pix.height)==(crop['width'],crop['height'])and im.tobytes()==pix.samples
            assert hashlib.sha256(pix.samples).hexdigest()==crop['rgb_sha256']
    records=[]
    for r in d['records']:
        src=literal(r);assert len(src)==r['source_slots'];base,mp=frame(r,r['excluded_source_indices']);assert len(base)==r['advertised_length']
        raw=inspect(base,key,mp);assert raw['raw']==r['expected_raw'];ed=repair(r['edited_output'],base,key,mp,src)
        display=''.join(c for c in r['readable_german'].upper()if c in'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace('X','')
        assert display==ed['raw'].replace('X','')
        records.append({'id':r['id'],'literal_source':src,'source_slots':len(src),'valid_source_coordinates':sum(c in C for c in src),'frame':base,'model_to_source_indices':mp,'excluded_source_indices':r['excluded_source_indices'],**raw,'readable_candidate':ed,'readable_german':r['readable_german'],'readable_nonseparator_mapping_verified':True})
    a,b=d['records'];assert literal(a)[60:66]==d['overlong_group']['literal']=='VGVXAA';assert len(literal(a))==187 and len(literal(b))==136
    native=''.join(c if c in C else'?'for c in literal(a));middle=untranspose(native,key['column_rank_order']);order=permutation(len(native),key['column_rank_order']);assert middle==''.join(native[i]for i in order)
    native_diagnostic={'source_slots':187,'intermediate_stream':middle,'paired_output':decrypt(native,key['column_rank_order'],key['square'],allow_unpaired=True),'unpaired_intermediate_index':186,'unpaired_source_index':order[-1],'unpaired_coordinate':middle[-1],'accepted_body_reading':False}
    free=[i for i,c in enumerate(key['square'])if c=='?'];missing=sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(key['square']));assert missing==['5','6']
    alternatives=[]
    for drop in d['overlong_group']['excluded_alternatives']:
        base,mp=frame(a,[drop]);raw=inspect(base,key,mp);template=raw['raw'].replace('LEIT?TELLE','LEITSTELLE').replace('?NSEKTIOK','ANSEKTION').replace('?NSEKTION','ANSEKTION').replace('POLITIKBEALIN','POLITIKBERLIN');ed=repair(template,base,key,mp,literal(a));witnesses=[]
        for vals in itertools.permutations(missing):
            square=list(key['square'])
            for cell,v in zip(free,vals):square[cell]=v
            square=''.join(square);assert len(set(square))==36
            pair=[]
            for rid,candidate in [('p155_C1',ed),('p155_C2',records[1]['readable_candidate'])]:
                full=candidate['ciphertext'].replace('?','A');plain=decrypt(full,key['column_rank_order'],square);assert encrypt(plain,key['column_rank_order'],square)==full;assert all(x=='?'or x==y for x,y in zip(candidate['raw'],plain));pair.append({'id':rid,'ciphertext':full,'plaintext':plain})
            assert pair[0]['plaintext'][24]==pair[1]['plaintext'][57]==pair[1]['plaintext'][62]
            witnesses.append({'square':square,'XA_label':square[30],'messages':pair,'global_roundtrips_verified':True,'historical_completion_claim':False})
        alternatives.append({'excluded_source_index':drop,'excluded_coordinate':literal(a)[drop],'raw':raw,'readable_candidate':ed,'joint_global_witnesses':witnesses})
    assert [len(x['readable_candidate']['known_coordinate_substitutions'])for x in alternatives]==[0,0,0,1,2,2]
    assert [len(x['readable_candidate']['erased_coordinate_fills'])for x in alternatives]==[2]*6
    assert next(x for x in alternatives if x['excluded_source_index']==61)['readable_candidate']==records[0]['readable_candidate']
    coupled=[{'record':'p155_C1','position':records[0]['positions'][24]},{'record':'p155_C2','position':records[1]['positions'][57]},{'record':'p155_C2','position':records[1]['positions'][62]}]
    assert all(x['position']['pair']=='XA'and x['position']['domain']=='56'for x in coupled)
    return {'schema':'adfgvx-eighth-part-repetition-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'summary':{'physical_records':2,'printed_source_slots':323,'valid_source_coordinates':320,'modeled_coordinates':322,'plaintext_positions':161,'baseline_fixed_positions':sum(x['fixed_positions']for x in records),'candidate_fixed_positions':sum(x['readable_candidate']['fixed_positions']for x in records),'known_coordinate_substitutions':0,'source_or_model_erasure_fills':2,'source_deletions':1,'deleted_valid_source_coordinates':1,'inserted_slots':0,'published_key_changed':False,'counting_frame':'Primary C1 exclusion at61 plus native C2; alternative exclusions are not extra records.'},'records':records,'native_odd_C1_diagnostic':native_diagnostic,'all_six_overlong_group_exclusions':alternatives,'shared_XA_fields':coupled,'source_images':d['source_images'],'limits':d['limits'],'prior_credit':d['prior_credit']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
