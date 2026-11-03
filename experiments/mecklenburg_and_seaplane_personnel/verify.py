#!/usr/bin/env python3
"""Verify the Mecklenburg inquiry and seaplane-personnel order in their native source frames.

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


def complete_one_mask(cipher,key,template):
    erased=[i for i,c in enumerate(cipher) if c=='?'];assert len(erased)==1
    witnesses=[]
    for value in C:
        full=cipher[:erased[0]]+value+cipher[erased[0]+1:]
        plain=decrypt(full,key['column_rank_order'],key['square'])
        assert all(a=='?' or a==b for a,b in zip(template,plain))
        assert encrypt(plain,key['column_rank_order'],key['square'])==full
        witnesses.append({'model_index':erased[0],'coordinate_value':value,'plaintext':plain,'ciphertext':full,'historical_choice':False})
    return witnesses


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert '?' not in key['square']
    assert sha(HERE/'prior_candidates.json')==data['prior_attribution_check']['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C+'-?')
        assert len(literal)==source['source_slots']==source['advertised_length']
        base=literal.replace('-','?');mapping=list(range(len(base)));raw=inspect(base,key,mapping)
        assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'printed_dash_indices':[i for i,c in enumerate(literal) if c=='-'],
                        'unreadable_visible_glyph_indices':[i for i,c in enumerate(literal) if c=='?'],
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[304,422,340]
    assert [r['fixed_positions'] for r in records]==[150,205,170]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[152,211,170]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[3,5,3]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[2,6,0]
    assert all(r['readable_candidate']['full_plaintext_reencryption_verified'] for r in records)
    assert records[0]['unreadable_visible_glyph_indices']==[68]
    assert records[0]['printed_dash_indices']==[109]
    sensitivity=[]
    for source in data['faded_glyph_sensitivity']:
        r=next(r for r in records if r['id']==source['record']);i=source['source_index'];point=source['plaintext_index']
        assert r['ciphertext'][i]==source['accepted_glyph'];base=r['ciphertext'][:i]+'?'+r['ciphertext'][i+1:]
        raw=inspect(base,key,r['model_to_source_indices']);assert raw['positions'][point]['domain']==source['expected_domain']
        template=r['readable_candidate']['raw'];template=template[:point]+'?'+template[point+1:]
        candidate=repair(template,base,key,r['model_to_source_indices'],r['literal_source'])
        assert len(candidate['known_coordinate_substitutions'])==len(r['readable_candidate']['known_coordinate_substitutions'])
        assert len(candidate['erased_coordinate_fills'])==len(r['readable_candidate']['erased_coordinate_fills'])
        assert candidate['ciphertext'][i]=='?'
        sensitivity.append({**source,'counted_in_summary':False,'ciphertext':base,**raw,'readable_candidate':candidate,
                            'all_six_compatibility_witnesses':complete_one_mask(candidate['ciphertext'],key,candidate['raw'])})
    return {'schema':'adfgvx-mecklenburg-and-seaplane-personnel-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':1066,'valid_source_coordinates':1058,'modeled_coordinates':1066,
                       'plaintext_positions':533,'baseline_fixed_positions':525,'candidate_fixed_positions':533,
                       'known_coordinate_substitutions':11,'source_or_model_erasure_fills':8,
                       'printed_dash_fills':7,'unreadable_visible_glyph_fills':1,
                       'unfilled_printed_erasure_coordinates':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'source_annotations':data['source_annotations'],
            'faded_glyph_sensitivity_variants':sensitivity,'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
