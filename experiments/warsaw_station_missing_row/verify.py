#!/usr/bin/env python3
"""Replay a conditional missing-row reading without changing a source coordinate.
ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt
from experiments.romanian_pacification_consultation.verify import inspect,masked_encryption
C='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());k=d['key'];source=''.join(''.join(d['source_rows']).split())
    assert d['source_record']=='p204_C2'
    assert k==next(x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']if x['id']==k['id'])
    assert len(source)==d['source_slots']==242 and set(source)<=set(C)
    assert source.endswith(d['literal_tail']) and d['advertised_length']==282
    assert len(d['source_rows'])==7 and [len(''.join(r.split()))for r in d['source_rows']]==[40]*6+[2]
    for path,digest in d['prior_artifacts'].items():assert sha(HERE/path)==digest
    for crop in d['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf)==d['source']['pdf_sha256'] and pdf.stat().st_size==d['source']['pdf_bytes']
        doc=fitz.open(pdf)
        for crop in d['source_images']:
            pix=doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(crop['render_scale'],crop['render_scale']),clip=fitz.Rect(*crop['crop_pdf_points']))
            im=Image.open(HERE/crop['path']).convert('RGB')
            assert im.size==(pix.width,pix.height)==(crop['width'],crop['height']) and im.tobytes()==pix.samples
            assert hashlib.sha256(pix.samples).hexdigest()==crop['rgb_sha256']
    native=inspect(source,k,list(range(len(source))))
    n=d['primary_model']['missing_coordinates'];assert n==40
    stencil=masked_encryption(d['editorial_template'],k);assert len(stencil)==282
    scan=[];zero=[]
    for gap in range(len(source)+1):
        frame=source[:gap]+'?'*n+source[gap:]
        mapping=list(range(gap))+[None]*n+list(range(gap,len(source)))
        target=''.join(a if b=='?'else b for a,b in zip(frame,stencil))
        changes=[{'model_index':i,'source_index':mapping[i],'from':a,'to':b}for i,(a,b)in enumerate(zip(frame,target))if a!='?'and a!=b]
        fills=[{'model_index':i,'source_index':None,'to':b}for i,(a,b)in enumerate(zip(frame,target))if a=='?'and b!='?']
        assert all(mapping[f['model_index']]is None for f in fills)
        scan.append({'gap_start':gap,'five_coordinate_group_boundary':gap%5==0,'known_coordinate_substitutions':len(changes),'inserted_slot_fills':len(fills)})
        if changes:continue
        baseline=inspect(frame,k,mapping);candidate=inspect(target,k,mapping)
        assert all(a=='?'or a==b for a,b in zip(d['editorial_template'],candidate['raw']))
        unused=iter(sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(k['square'])))
        square=''.join(next(unused)if c=='?'else c for c in k['square'])
        assert len(set(square))==36
        complete=target.replace('?','A');plain=decrypt(complete,k['column_rank_order'],square)
        assert encrypt(plain,k['column_rank_order'],square)==complete
        assert all(a=='?'or a==b for a,b in zip(candidate['raw'],plain))
        assert ''.join(complete[i]for i,j in enumerate(mapping)if j is not None)==source
        zero.append({'gap_start':gap,'frame':frame,'model_to_source_indices':mapping,'baseline':baseline,'candidate':candidate,'edited_ciphertext':target,'known_coordinate_substitutions':[],'source_mask_fills':[],'inserted_slot_fills':fills,'global_completion_witness':{'square':square,'ciphertext':complete,'plaintext':plain,'roundtrip_verified':True,'all_observed_coordinates_preserved':True,'historical_completion_claim':False}})
    assert [x['gap_start']for x in zero]==d['expected_zero_change_gap_starts']==[240,241,242]
    primary=next(x for x in zero if x['gap_start']==d['primary_model']['source_insertion_index'])
    assert primary['candidate']['raw']==d['primary_edited_output']
    assert len(primary['inserted_slot_fills'])==36
    assert primary['baseline']['fixed_positions']==101 and primary['candidate']['fixed_positions']==137
    display=''.join(c for c in d['readable_german'].upper()if c in'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace('X','')
    # The final full stop is punctuation, while all four ? tokens remain output positions.
    assert display==d['primary_edited_output'].replace('X','')
    return {'schema':'adfgvx-warsaw-station-missing-row-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'source_record':d['source_record'],'indexing':'All machine indices are zero-based.','literal_source':source,'native_242_slot_reading':native,'summary':{'physical_records':1,'printed_source_slots':242,'valid_source_coordinates':242,'modeled_coordinates':282,'plaintext_positions':141,'baseline_fixed_positions':101,'candidate_fixed_positions':137,'known_coordinate_substitutions':0,'source_or_model_erasure_fills':36,'source_mask_fills':0,'inserted_slots':40,'inserted_slot_fills':36,'remaining_inserted_masks':4,'source_deletions':0,'published_key_changed':False,'counting_frame':'One primary conditional gap-before-GX frame; alternatives are not added to totals.'},'all_contiguous_40_slot_gap_template_costs':scan,'zero_change_witnesses':zero,'primary_gap':240,'readable_nonseparator_mapping_verified':True,'context':d['context'],'limits':d['limits'],'prior_credit':d['prior_credit']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert c==json.loads(out.read_text())
    else:out.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary']},indent=2))
if __name__=='__main__':main()
