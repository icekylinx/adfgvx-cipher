#!/usr/bin/env python3
"""Verify a two-part accounting request with one explicit missing coordinate.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Five insertion boundaries are retained; missing material is separately priced.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt
from experiments.romanian_pacification_consultation.verify import inspect,repair,permutation
C='ADFGVX'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def folded(s,separator):
    s=s.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS')
    return ''.join(c for c in s if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace(separator,'')

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());keys=data['keys']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for kid,key in keys.items():assert key==published[kid]
    for path,digest in data['prior_artifacts'].items():assert sha(HERE/path)==digest
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf)==data['source']['pdf_sha256']
        assert pdf.stat().st_size==data['source']['pdf_bytes']
        doc=fitz.open(pdf)
        for crop in data['source_images']:
            pix=doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(crop['render_scale'],crop['render_scale']),clip=fitz.Rect(*crop['crop_pdf_points']))
            im=Image.open(HERE/crop['path']).convert('RGB')
            assert im.size==(pix.width,pix.height)==(crop['width'],crop['height'])
            assert im.tobytes()==pix.samples
            assert hashlib.sha256(pix.samples).hexdigest()==crop['rgb_sha256']
    out=[]
    for r in data['records']:
        literal=''.join(''.join(r['source_rows']).split());base=''.join(c if c in C else '?'for c in literal)
        assert len(literal)==r['source_slots']
        key=keys[r['key_id']];mapping=list(range(len(base)));alternatives=[];native_diagnostic=None
        if 'insert_unknown_at_source_boundary' in r:
            assert r['id']=='p172_D1' and len(base)==197 and r['advertised_length']==198
            assert literal[25:29]=='ADAX' and r['all_insertion_boundaries']==list(range(25,30))
            order=permutation(len(base),key['column_rank_order']);orphan=order[-1]
            native_diagnostic={'ciphertext':base,'raw_diagnostic':decrypt(base,key['column_rank_order'],key['square'],allow_unpaired=True),'unpaired_coordinate':{'intermediate_index':len(base)-1,'source_index':orphan,'coordinate':base[orphan]},'source_slots':197,'diagnostic_only':True}
            for z in r['all_insertion_boundaries']:
                mm=list(range(len(base)));mm.insert(z,None);bb=base[:z]+'?'+base[z:]
                rr=inspect(bb,key,mm);cc=repair(r['edited_output'],bb,key,mm,literal)
                alternatives.append({'insertion_boundary':z,'model_to_source_indices':mm,**rr,'readable_candidate':cc,'observed_substitutions':len(cc['known_coordinate_substitutions']),'source_mask_fills':sum(x['source_index'] is not None for x in cc['erased_coordinate_fills']),'inserted_slot_fills':sum(x['source_index'] is None for x in cc['erased_coordinate_fills'])})
            costs=[x['observed_substitutions']for x in alternatives]
            assert costs==[4,3,2,2,3]
            assert alternatives[2]['readable_candidate']['ciphertext']==alternatives[3]['readable_candidate']['ciphertext']
            z=r['insert_unknown_at_source_boundary'];assert z==28
            mapping.insert(z,None);base=base[:z]+'?'+base[z:]
        else:assert len(base)==r['advertised_length']==204 and r['id']=='p172_D2'
        raw=inspect(base,key,mapping);assert raw['raw']==r['expected_raw']
        candidate=repair(r['edited_output'],base,key,mapping,literal)
        assert len(candidate['known_coordinate_substitutions'])==r['expected_substitutions']
        assert sum(x['source_index'] is not None for x in candidate['erased_coordinate_fills'])==r['expected_source_mask_fills']
        assert sum(x['source_index'] is None for x in candidate['erased_coordinate_fills'])==r['expected_inserted_slot_fills']
        # One consistent global completion, never separate assignments per occurrence.
        unused=iter(sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(key['square'])))
        full_square=''.join(next(unused) if ch=='?' else ch for ch in key['square'])
        assert len(set(full_square))==36
        full_cipher=candidate['ciphertext'].replace('?','A')
        full_plain=decrypt(full_cipher,key['column_rank_order'],full_square)
        assert encrypt(full_plain,key['column_rank_order'],full_square)==full_cipher
        assert all(a=='?'or a==b for a,b in zip(candidate['raw'],full_plain))
        candidate['global_completion_witness']={'square':full_square,'ciphertext':full_cipher,'plaintext':full_plain,'roundtrip_verified':True,'historical_completion_claim':False}
        assert folded(r['readable_german'][:-1] if r.get('question_mark_punctuation_at_end') else r['readable_german'],r['separator_label'])==folded(candidate['raw'],r['separator_label']),r['id']
        for token in r.get('protected_fields',[]):
            assert token in raw['raw'] and token in candidate['raw'] and token in r['readable_german'],(r['id'],token)
        variants=[]
        for v in r['source_variants']:
            s=''.join(v['grouped'].split());assert len(s)==len(base)and set(s)<=set(C)
            text=decrypt(s,key['column_rank_order'],key['square'])
            assert encrypt(text,key['column_rank_order'],key['square'])==s
            variants.append({'name':v['name'],'literal_source':s,'plaintext':text,'source_differences':[{'source_index':i,'first_printed':a,'second_printed':b}for i,(a,b)in enumerate(zip(literal,s))if a!=b], 'plaintext_differences':[{'plaintext_index':i,'first_printed_variant':a,'second_printed_variant':b}for i,(a,b)in enumerate(zip(raw['raw'],text))if a!=b],'roundtrip_verified':True,'source_correction_claim':False})
        out.append({'id':r['id'],'literal_source':literal,'source_slots':len(literal),'modeled_coordinates':len(base),'native_diagnostic':native_diagnostic,'all_local_insertion_candidates':alternatives,'valid_source_coordinates':sum(c in C for c in literal),'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_nonseparator_label_mapping_verified':True,'source_variants':variants})
    summary={'physical_records':len(out),'printed_source_slots':sum(r['source_slots']for r in out),'valid_source_coordinates':sum(r['valid_source_coordinates']for r in out),'modeled_coordinates':sum(r['modeled_coordinates']for r in out),'plaintext_positions':sum(len(r['raw'])for r in out),'baseline_fixed_positions':sum(r['fixed_positions']for r in out),'candidate_fixed_positions':sum(r['readable_candidate']['fixed_positions']for r in out),'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in out),'source_or_model_erasure_fills':sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_mask_fills':sum(sum(x['source_index'] is not None for x in r['readable_candidate']['erased_coordinate_fills'])for r in out),'inserted_slot_fills':sum(sum(x['source_index'] is None for x in r['readable_candidate']['erased_coordinate_fills'])for r in out),'source_deletions':0,'inserted_slots':1,'source_reorderings':0,'published_key_changed':False}
    return {'schema':'adfgvx-staatsbank-missing-coordinate-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine indices are zero-based.','summary':summary,'records':out,'prior_credit':data['prior_credit'],'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert c==json.loads(f.read_text())
    else:f.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
