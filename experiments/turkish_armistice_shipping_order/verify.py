#!/usr/bin/env python3
"""Verify the cross-page Turkish armistice and shipping order with explicit related-traffic limits.

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


def occurrences(text,term):
    return [i for i in range(len(text)-len(term)+1) if text.startswith(term,i)]


def related_comparison(data,records):
    key=data['key'];source=data['record_snapshot'];base=source['analysis_source'];mapping=source['model_to_source_indices']
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert ''.join(source['rows']).replace(' ','')==source['literal_source']
    assert source['literal_source'].replace('-','?')==base
    raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
    edited=repair(source['editorial_text'],base,key,mapping,source['literal_source'])
    assert len(edited['known_coordinate_substitutions'])==6 and len(edited['erased_coordinate_fills'])==1
    comparisons=[]
    for r in records:
        assert r['raw']!=raw['raw'] and r['readable_candidate']['raw']!=edited['raw']
        comparisons.append({'record':r['id'],'same_complete_literal_raw_plaintext':False,
                            'address_occurrences_in_raw':{term:occurrences(r['raw'],term) for term in data['address_terms']},
                            'shared_edited_terms':{term:{'new_record_indices':occurrences(r['readable_candidate']['raw'],term),'p112_D_indices':occurrences(edited['raw'],term)} for term in data['shared_terms'] if term in r['readable_candidate']['raw'] and term in edited['raw']}})
    assert 'BVNXBEIBVGX7OSPOLIX?' in raw['raw']
    return {'counted_in_primary_summary':False,'snapshot_origin':data['copied_record_origin'],'p112_D_raw':raw,
            'p112_D_edited_snapshot':edited,'comparisons':comparisons,'p112_D_original_closing_fields':'BVNXBEIBVGX7OSPOLIX?',
            'changed_p112_D_source_or_key':False,'limits':data['limits']}


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert '?' not in key['square']
    assert sha(HERE/'prior_candidates.json')==data['prior_attribution_check']['sha256']
    assert sha(HERE/'related_traffic.json')==data['related_traffic']['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C)
        assert len(literal)==source['source_slots']==source['advertised_length']
        mapping=list(range(len(literal)));raw=inspect(literal,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],literal,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':literal,'source_slots':len(literal),'valid_coordinates':len(literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[338,344,236]
    assert [r['fixed_positions'] for r in records]==[169,172,118]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[169,172,118]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[6,2,3]
    assert all(not r['readable_candidate']['erased_coordinate_fills'] and r['readable_candidate']['full_plaintext_reencryption_verified'] for r in records)
    sensitivity=[]
    for source in data['faded_glyph_sensitivity']:
        r=next(r for r in records if r['id']==source['record']);i=source['source_index'];point=source['plaintext_index']
        assert r['ciphertext'][i]==source['accepted_glyph'];base=r['ciphertext'][:i]+'?'+r['ciphertext'][i+1:]
        raw=inspect(base,key,r['model_to_source_indices']);assert raw['positions'][point]['domain']==source['expected_domain']
        template=r['readable_candidate']['raw'];template=template[:point]+'?'+template[point+1:]
        candidate=repair(template,base,key,r['model_to_source_indices'],r['literal_source'])
        assert not candidate['erased_coordinate_fills'] and candidate['ciphertext'][i]=='?'
        assert len(candidate['known_coordinate_substitutions'])==len(r['readable_candidate']['known_coordinate_substitutions'])
        sensitivity.append({**source,'counted_in_summary':False,'ciphertext':base,**raw,'readable_candidate':candidate,
                            'all_six_compatibility_witnesses':complete_one_mask(candidate['ciphertext'],key,candidate['raw'])})
    related=related_comparison(json.loads((HERE/'related_traffic.json').read_text()),records)
    return {'schema':'adfgvx-turkish-armistice-shipping-order-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':918,'valid_source_coordinates':918,'modeled_coordinates':918,
                       'plaintext_positions':459,'baseline_fixed_positions':459,'candidate_fixed_positions':459,
                       'known_coordinate_substitutions':11,'source_or_model_erasure_fills':0,
                       'unfilled_printed_erasure_coordinates':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'source_annotations':data['source_annotations'],
            'faded_glyph_sensitivity_variants':sensitivity,'related_traffic_comparison':related,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
