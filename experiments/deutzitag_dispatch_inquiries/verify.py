#!/usr/bin/env python3
"""Verify repeated DEUTZITAG inquiries and the separate Tiflis pioneer order.

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
    inputs = json.loads((HERE/'inputs.json').read_text())
    key = inputs['key']
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    assert key == next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path']) == crop['sha256']
    if pdf:
        verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        literal=''.join(''.join(source['source_rows']).split())
        assert set(literal)<=set(C) and len(literal)==source['source_slots']==source['advertised_length']
        mapping=list(range(len(literal)))
        raw=inspect(literal,key,mapping)
        assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],literal,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'ciphertext':literal,
                        'source_slots':len(literal),'model_to_source_indices':mapping,
                        **raw,'readable_candidate':candidate})
    assert [len(r['raw']) for r in records]==[137,169,66,137]
    assert all(r['fixed_positions']==len(r['raw']) for r in records)
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[0,1,0,0]
    assert all(not r['readable_candidate']['erased_coordinate_fills'] for r in records)
    a,long,pioneer,c=records
    assert a['literal_source']==c['literal_source']
    assert a['raw']==c['raw']==long['readable_candidate']['raw'][32:]
    assert long['raw'][:32]=='FUERXSAULXWEINREICHXDOPPELPUNKTX'
    pairs=[]
    for i in range(137):
        assert a['positions'][i]['pair']==c['positions'][i]['pair']==long['readable_candidate']['positions'][32+i]['pair']
        pairs.append({'short_index':i,'long_index':32+i,'p80_A_raw':a['positions'][i],
                      'p81_C_raw':c['positions'][i],'p81_A_before':long['positions'][32+i],
                      'p81_A_after':long['readable_candidate']['positions'][32+i]})
    mismatch=[p for p in pairs if p['p81_A_before']['raw']!=p['p80_A_raw']['raw']]
    assert len(mismatch)==1 and mismatch[0]['short_index']==7
    assert long['readable_candidate']['known_coordinate_substitutions']==[{'model_index':248,'source_index':248,'printed':'G','from':'G','to':'F'}]
    assert pioneer['raw']==pioneer['readable_candidate']['raw']
    label_inventory=[{'record':r['id'],'variant':v,'raw':read['raw'],
                      'all_numeral_and_JQY_occurrences':[p for p in read['positions'] if p['raw'] in '0123456789JQY']}
                     for r in records for v,read in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    reference=[]
    for token in ['4452','BX103830XO9']:
        start=pioneer['raw'].index(token)
        reference.append({'token':token,'plaintext_start':start,'positions':pioneer['positions'][start:start+len(token)],'all_coordinates_unchanged':True})
    return {'schema':'adfgvx-deutzitag-dispatch-certificate-v1','project':inputs['project'],
            'authors':inputs['authors'],'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All indices are zero-based.',
            'summary':{'physical_records':4,'printed_source_slots':1018,'valid_source_coordinates':1018,
                       'modeled_coordinates':1018,'plaintext_positions':509,'baseline_fixed_positions':509,
                       'candidate_fixed_positions':509,'known_coordinate_substitutions':1,
                       'printed_erasure_fills':0,'missing_coordinate_fills':0,'source_deletions':0,
                       'published_key_changed':False},
            'records':records,'identical_short_source_records':['p80_A','p81_C'],
            'shared_137_character_body':{'text':a['raw'],'long_prefix':long['raw'][:32],
                                       'position_witnesses':pairs,'all_raw_disagreements':mismatch},
            'separate_pioneer_order_unchanged_references':reference,
            'complete_raw_label_inventory':label_inventory,
            'prior_attribution_check':inputs['prior_attribution_check'],
            'limits':['The dispatch inquiries ask for shipment information; they do not establish that a particular shipment took place.',
                      'Saul Weinreich is the received addressee, not an independently identified individual.',
                      'The pioneer order is a separate message. Its reference fields and received O9 are unchanged.',
                      'The local J-to-O repair changes one observed ciphertext coordinate; it is not a global square relabeling.',
                      'All bodies had earlier unreviewed OCR candidates; this package makes no first historical decipherment claim.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
