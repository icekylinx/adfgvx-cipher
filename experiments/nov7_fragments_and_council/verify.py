#!/usr/bin/env python3
"""Verify p151 fragments, typed/handwritten acknowledgment layers and Soldiers Council notice.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No published substitution square or numerical label is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation(length, ranks):
    """Independent column-offset inverse: interim index -> model index."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (i < length % width) for i in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[i])
              for i in range(width)]
    order = [starts[i % width] + i // width for i in range(length)]
    assert sorted(order) == list(range(length))
    return order


def inspect(cipher, key, mapping):
    square, ranks = key['square'], key['column_rank_order']
    assert len(cipher) % 2 == 0 and len(mapping) == len(cipher)
    order = permutation(len(cipher), ranks)
    middle = ''.join(cipher[j] for j in order)
    assert middle == untranspose(cipher, ranks)
    unused = set(A) - set(square)
    positions = []
    for i in range(len(cipher) // 2):
        pair = middle[2*i:2*i+2]
        cells = [6*r+c for r in range(6) for c in range(6)
                 if pair[0] in ('?', C[r]) and pair[1] in ('?', C[c])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        indices = order[2*i:2*i+2]
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices],
                          'domain': domain,
                          'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    return {'raw': raw, 'fixed_positions': sum(p['raw'] != '?' for p in positions),
            'positions': positions}


def masked_encryption(template, key):
    square = key['square']
    middle = ''.join('??' if ch == '?' else C[square.index(ch)//6] + C[square.index(ch) % 6]
                     for ch in template)
    target = [None] * len(middle)
    for ch, i in zip(middle, permutation(len(middle), key['column_rank_order'])):
        target[i] = ch
    return ''.join(target)


def repair(template, base, key, mapping, literal):
    assert len(template)*2 == len(base)
    stencil = masked_encryption(template, key)
    target = ''.join(a if b == '?' else b for a, b in zip(base, stencil))
    result = inspect(target, key, mapping)
    assert result['raw'] == template
    substitutions, fills = [], []
    for i, (a, b) in enumerate(zip(base, target)):
        if a == b:
            continue
        source_i = mapping[i]
        event = {'model_index': i, 'source_index': source_i,
                 'printed': literal[source_i] if source_i is not None else None,
                 'from': a, 'to': b}
        (fills if a == '?' else substitutions).append(event)
    rebuilt = list(base)
    for event in substitutions + fills:
        rebuilt[event['model_index']] = event['to']
    assert ''.join(rebuilt) == target
    if '?' not in template:
        assert target == encrypt(template, key['column_rank_order'], key['square'])
    return {'template': template, 'ciphertext': target,
            'known_coordinate_substitutions': substitutions,
            'erased_coordinate_fills': fills,
            'full_plaintext_reencryption_verified': '?' not in template,
            'published_key_changed': False, **result}


def verify_crops(pdf, expected, crops, relative_to):
    import fitz
    from PIL import Image
    assert pdf.stat().st_size == expected['pdf_bytes']
    assert sha(pdf) == expected['pdf_sha256']
    doc = fitz.open(pdf)
    for crop in crops:
        rect = crop.get('crop_pdf_points', crop.get('clip_points'))
        scale = crop.get('render_scale', crop.get('scale'))
        pix = doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*rect))
        im = Image.open(relative_to/crop['path']).convert('RGB')
        assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples


def witnesses(cipher,key,template):
    missing=[i for i,c in enumerate(cipher) if c=='?'];assert len(missing)==1
    out=[]
    for ch in C:
        full=cipher[:missing[0]]+ch+cipher[missing[0]+1:]
        plain=decrypt(full,key['column_rank_order'],key['square']);assert '?' not in plain
        assert all(a=='?' or a==b for a,b in zip(template,plain))
        assert encrypt(plain,key['column_rank_order'],key['square'])==full
        out.append({'coordinate':ch,'ciphertext':full,'plaintext':plain,'historical_completion_claim':False})
    return out


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert ''.join(sorted(set(A)-set(key['square'])))=='56'
    for field in ['prior_attribution_check','ocr_snapshot']:assert sha(HERE/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        lit=''.join(source['source_rows']).replace(' ','');typed=''.join(source['typed_rows']).replace(' ','')
        assert lit==source['literal_source'] and len(lit)==source['source_slots'] and set(lit)<=set(C)
        assert len(typed)==source['typed_source_slots'];mapping=source['working_source_indices']
        base=''.join('?' if i is None else lit[i] for i in mapping);assert len(base)==source['advertised_length']
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,lit)
        assert candidate['full_plaintext_reencryption_verified']
        assert all(key['square'][C.index(p['pair'][0])*6+C.index(p['pair'][1])]!='?' for p in candidate['positions'])
        records.append({'id':source['id'],'literal_source':lit,'literal_printed_rows':source['source_rows'],
                        'typed_source':typed,'ciphertext':base,'source_slots':len(lit),'valid_coordinates':len(lit),
                        'typed_source_slots':len(typed),'modeled_coordinates':len(base),'source_geometry':source['source_geometry'],
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[189,186,161,154]
    assert [len(r['ciphertext']) for r in records]==[190,186,156,154]
    assert [r['fixed_positions'] for r in records]==[94,93,78,77]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[95,93,78,77]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[0,1,3,0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[1,0,0,0]
    a1=records[0];g=a1['source_geometry'];lit=a1['literal_source'];variants=[]
    assert ' '.join(data['records'][0]['source_rows']).split()[11]=='AVVG'
    assert g['all_insertion_boundaries']==list(range(55,60))
    for gap in g['all_insertion_boundaries']:
        base=lit[:gap]+'?'+lit[gap:];mapping=list(range(len(lit)));mapping.insert(gap,None);raw=inspect(base,key,mapping)
        variants.append({'missing_before_source_index':gap,'group_model':base[55:60],
                         'ciphertext':base,'model_to_source_indices':mapping,**raw,
                         'all_six_complete_witnesses':witnesses(base,key,raw['raw']),'counted_in_summary':False})
    union={w['ciphertext']:w['plaintext'] for v in variants for w in v['all_six_complete_witnesses']}
    accepted={c:p for c,p in union.items() if p[g['crib_start']:g['crib_end']]==g['crib_text']}
    assert len(union)==26 and len(accepted)==1
    assert accepted=={a1['readable_candidate']['ciphertext']:a1['readable_candidate']['raw']}
    assert a1['readable_candidate']['erased_coordinate_fills']==[{'model_index':55,'source_index':None,'printed':None,'from':'?','to':'D'}]
    b=records[2];bg=b['source_geometry'];assert b['literal_source'][135:140]==b['literal_source'][130:135]=='VXXDV'
    assert b['typed_source']==b['ciphertext'] and len(b['literal_source'])%2==1
    sensitivity=b['literal_source'][:138]+'O'+b['literal_source'][139:]
    assert ''.join(sensitivity[i] for i in b['model_to_source_indices'])==b['typed_source']
    snap=json.loads((HERE/'ocr_snapshot.json').read_text());old=''.join(snap['record_snapshot']['groups']);assert len(old)==155
    assert old[133]==old[149]=='?' and old[127]=='V'
    corrected=''.join('X' if i==127 else 'D' if i==133 else 'V' if i==149 else c for i,c in enumerate(old))
    assert corrected[:120]+'XXVGF'+corrected[120:]+'D'==b['literal_source']
    ocr={'snapshot_origin':snap['origin'],'earlier_ciphertext':old,'earlier_length':155,
         'resolved_old_OCR_masks':[{'old_index':133,'source_index_in_composite':138,'value':'D'},{'old_index':149,'source_index_in_composite':154,'value':'V'}],
         'corrected_typed_OCR_glyph':{'old_index':127,'source_index_in_composite':132,'old':'V','visible_source':'X'},
         'omitted_typed_group_at_composite_index120':'XXVGF','omitted_final_typed_coordinate_at_composite_index160':'D',
         'reconstructed_composite_length':161,'separate_typed_layer_length':156,'old_shared_corpus_mutated':False}
    return {'schema':'adfgvx-nov7-fragments-and-council-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based; B source indices refer to the composite with annotations.',
            'summary':{'physical_records':4,'printed_source_slots':690,'valid_source_coordinates':690,
                       'literal_source_slots_including_annotations':690,'typed_source_slots':685,'valid_typed_source_coordinates':685,
                       'handwritten_slots_excluded_from_typed_frame':5,'modeled_coordinates':686,
                       'added_missing_source_coordinates':1,'plaintext_positions':343,'baseline_fixed_positions':342,'candidate_fixed_positions':343,
                       'known_coordinate_substitutions':4,'source_or_model_erasure_fills':1,
                       'source_deletions':0,'source_deletions_in_primary_typed_layer':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'A1_all_five_gap_geometries':variants,
            'A1_bounded_crib_result':{'geometry_labeled_completions':30,'distinct_complete_ciphertexts':26,'distinct_complete_plaintexts':len(set(union.values())),
                'crib_start':g['crib_start'],'crib_end':g['crib_end'],'crib_text':g['crib_text'],'accepted_distinct_completions':1,
                'unique_only_under_stated_one_loss_and_lexical_conditions':True},
            'B_handwriting_sensitivity':{'hypothetical_composite_O_glyph':sensitivity,'source_index':138,'valid_coordinate_count':160,'typed_layer_unchanged':True,
                'composite_pair_decryption_defined':False,'primary_D_coordinate_count':161,'counted_in_summary':False},
            'B_ocr_reconstruction':ocr,'unresolved_square_cells_used_by_primary_edited_records':False,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
