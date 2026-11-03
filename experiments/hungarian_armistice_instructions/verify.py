#!/usr/bin/env python3
"""Verify the three-part Hungarian-armistice instruction message and its OCR boundary repair.

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


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert '?' not in key['square']
    for field in ['prior_attribution_check','ocr_snapshot']:assert sha(HERE/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C)
        assert len(literal)==source['source_slots']==source['advertised_length']
        mapping=list(range(len(literal)));raw=inspect(literal,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],literal,key,mapping,literal)
        assert not candidate['erased_coordinate_fills'] and candidate['full_plaintext_reencryption_verified']
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':literal,'source_slots':len(literal),'valid_coordinates':len(literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[352,266,48]
    assert [r['fixed_positions'] for r in records]==[176,133,24]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[3,3,0]
    assert all(r['fixed_positions']==r['readable_candidate']['fixed_positions'] for r in records)
    assert 'KOOVES' in records[0]['raw'] and records[0]['readable_candidate']['raw'].endswith('VERLASSEN0')
    assert 'GENERLSTABSOFFIZIERE' in records[1]['raw'] and 'GENERLSTABSOFFIZIERE' in records[1]['readable_candidate']['raw']
    snap=json.loads((HERE/'ocr_snapshot.json').read_text());blocks={b['id']:b for b in snap['record_snapshots']}
    old1=''.join(blocks['p124_ocr_block1']['groups']+blocks['p124_ocr_block2']['groups'])
    a1=records[0];assert len(old1)==352
    differences=[{'source_index':i,'ocr':x,'visible_source':y} for i,(x,y) in enumerate(zip(old1,a1['literal_source'])) if x!=y]
    assert differences==[{'source_index':194,'ocr':'?','visible_source':'F'}]
    old23=''.join(blocks['p124_ocr_block3']['groups']+blocks['p124_ocr_block4']['groups']);assert len(old23)==308
    deletes=[67,211];replacements={114:'V',160:'V'}
    assert [old23[i] for i in deletes]==['A','?']
    assert all(old23[i]=='?' for i in replacements)
    corrected=''.join(replacements.get(i,c) for i,c in enumerate(old23) if i not in deletes)
    a2,a3=records[1:];assert corrected==a2['literal_source']+a3['literal_source'][:40]
    assert a3['literal_source'][40:]=='VDFFAFAA'
    ocr={'snapshot_origin':snap['origin'],'A1':{'earlier_ciphertext':old1,'same_key_output':inspect(old1,key,list(range(352))),
        'visible_source_mask_correction':differences},
        'A2_and_A3':{'earlier_merged_ciphertext':old23,'earlier_length':308,
        'same_key_output_of_incorrect_merged_frame':inspect(old23,key,list(range(308))),
        'deleted_OCR_only_symbols':[{'old_merged_index':i,'ocr_symbol':old23[i]} for i in deletes],
        'resolved_OCR_masks':[{'old_merged_index':i,'ocr':'?','visible_source':c} for i,c in replacements.items()],
        'corrected_prefix_length':306,'corrected_prefix':corrected,
        'source_defined_part_boundary_after_prefix_index':266,
        'visible_A3_final_row_omitted_by_OCR':'VDFFA FAA',
        'A3_tail_source_indices':list(range(40,48)),
        'final_split_source_lengths':[266,48]},
        'historical_source_insertions_or_deletions_from_OCR_repair':0,'old_shared_corpus_mutated':False}
    return {'schema':'adfgvx-hungarian-armistice-instructions-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':666,'valid_source_coordinates':666,'modeled_coordinates':666,
                       'plaintext_positions':333,'baseline_fixed_positions':333,'candidate_fixed_positions':333,
                       'known_coordinate_substitutions':6,'source_or_model_erasure_fills':0,
                       'unfilled_printed_erasure_coordinates':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'ocr_reconstruction':ocr,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
