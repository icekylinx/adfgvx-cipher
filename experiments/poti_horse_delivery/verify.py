#!/usr/bin/env python3
"""Verify the native Poti horse-delivery continuations and retain the unresolved first part.

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


def independent_erasure_completions(record,key):
    cipher=record['ciphertext'];indices=[i for i,c in enumerate(cipher) if c=='?']
    points=[p for p in record['positions'] if p['raw']=='?']
    assert len(indices)==len(points) and all(p['pair'].count('?')==1 and len(p['domain'])==6 for p in points)
    first=cipher.replace('?','A');witnesses=[]
    for index in indices:
        for value in C:
            c=first[:index]+value+first[index+1:];plain=decrypt(c,key['column_rank_order'],key['square'])
            assert all(a=='?' or a==b for a,b in zip(record['raw'],plain))
            assert encrypt(plain,key['column_rank_order'],key['square'])==c
            witnesses.append({'changed_unfilled_model_index':index,'coordinate_value':value,'complete_ciphertext':c,'complete_plaintext':plain})
    return {'unfilled_coordinate_indices':indices,'unresolved_positions':points,'exact_distinct_complete_plaintexts':6**len(indices),
            'counting_method':'Each unresolved position uses exactly one independent coordinate erasure, and the complete square is bijective. Thus six choices per coordinate give6^k distinct full ciphertexts and plaintexts. This is a factorized count, not enumeration of all completions.',
            'finite_generating_witnesses':witnesses,'witness_convention':'All other unfilled coordinates are set to A solely as a reproducibility witness; no historical preference is asserted.'}


def contextual_frames(source,key):
    literal=''.join(source['source_rows']).replace(' ','');assert len(literal)==225
    base=literal.replace('-','?');rows=[]
    for start in range(221):
        cipher=base[:start]+base[start+5:];mapping=list(range(start))+list(range(start+5,225))
        result=inspect(cipher,key,mapping)
        rows.append({'deletion_start':start,'excluded_source_indices':list(range(start,start+5)),
                     'excluded_literal':literal[start:start+5],'excluded_known_coordinates':sum(c in C for c in literal[start:start+5]),
                     'ciphertext':cipher,'raw':result['raw'],'fixed_positions':result['fixed_positions']})
    consensus=''.join(chars[0] if len(set(chars))==1 else '?' for chars in zip(*(r['raw'] for r in rows)))
    assert rows[200]['ciphertext']==rows[201]['ciphertext']
    return {'id':source['id'],'literal_source':literal,'source_slots':225,'valid_coordinates':sum(c in C for c in literal),
            'advertised_length':220,'counted_in_summary':False,'accepted_historical_frame':None,
            'all221_consecutive_five_deletion_frames':rows,'all_frame_raw_consensus':consensus,
            'illustrative_frames':[rows[i] for i in source['illustrative_deletion_starts']],'limits':source['limits']}


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
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C+'-')
        assert len(literal)==source['source_slots']==source['advertised_length']
        base=literal.replace('-','?');mapping=list(range(len(base)));raw=inspect(base,key,mapping)
        assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b],
                        'remaining_erasure_completions':independent_erasure_completions(candidate,key)})
    assert [r['source_slots'] for r in records]==[220,230]
    assert [r['fixed_positions'] for r in records]==[103,85]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[106,107]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[11,9]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[3,23]
    assert [r['remaining_erasure_completions']['exact_distinct_complete_plaintexts'] for r in records]==[1296,1679616]
    ext=data['optional_contextual_extension'];r=records[0]
    full=repair(ext['template'],r['ciphertext'],key,r['model_to_source_indices'],r['literal_source'])
    incremental=repair(ext['template'],r['readable_candidate']['ciphertext'],key,r['model_to_source_indices'],r['literal_source'])
    assert len(full['known_coordinate_substitutions'])==25 and len(full['erased_coordinate_fills'])==7
    assert len(incremental['known_coordinate_substitutions'])==14 and len(incremental['erased_coordinate_fills'])==4
    assert full['full_plaintext_reencryption_verified'] and full['ciphertext']==incremental['ciphertext']
    optional={**ext,'complete_extension_from_literal_source':full,'additional_edits_from_main_candidate':incremental}
    context=[contextual_frames(row,key) for row in data['contextual_unread_records']]
    return {'schema':'adfgvx-poti-horse-delivery-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':2,'printed_source_slots':450,'valid_source_coordinates':412,'modeled_coordinates':450,
                       'plaintext_positions':225,'baseline_fixed_positions':188,'candidate_fixed_positions':213,
                       'known_coordinate_substitutions':20,'source_or_model_erasure_fills':26,
                       'unfilled_printed_erasure_coordinates':12,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'optional_contextual_extension':optional,
            'contextual_unread_records':context,'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
