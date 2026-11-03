#!/usr/bin/env python3
"""Verify Romanian-ultimatum companions and preserve the unread source parts.

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
    from itertools import permutations
    inputs=json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    key=inputs['key']
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert sha(HERE/'prior_candidates.json')==inputs['prior_attribution_check']['earlier_repository_candidates']['sha256']
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        literal=''.join(''.join(source['source_rows']).split())
        assert set(literal)<=set(C+'-')
        assert len(literal)==source['source_slots']==source['advertised_length']
        base=literal.replace('-','?');mapping=list(range(len(base)))
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'ciphertext':base,
                        'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[212,208,168]
    assert [r['fixed_positions'] for r in records]==[103,102,79]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[106,102,83]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[2,1,3]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[3,0,4]
    squares=[];cells=[i for i,c in enumerate(key['square']) if c=='?'];missing=sorted(set(A)-set(key['square']))
    for labels in permutations(missing):
        sq=list(key['square'])
        for cell,label in zip(cells,labels):sq[cell]=label
        squares.append(''.join(sq))
    assert len(squares)==120
    completion_audits=[]
    for record,unknown_positions in [(records[1],[43,45]),(records[2],[78])]:
        candidate=record['readable_candidate'];unfilled=[i for i,c in enumerate(candidate['ciphertext']) if c=='?']
        assert len(unfilled) in (0,1)
        counts={};witnesses={};digest=hashlib.sha256();tested=0
        for square in squares:
            for value in (C if unfilled else ['']):
                cipher=candidate['ciphertext']
                if unfilled:cipher=cipher[:unfilled[0]]+value+cipher[unfilled[0]+1:]
                plain=decrypt(cipher,key['column_rank_order'],square)
                assert all(a=='?' or a==b for a,b in zip(candidate['raw'],plain))
                assert encrypt(plain,key['column_rank_order'],square)==cipher
                label=''.join(plain[i] for i in unknown_positions)
                counts[label]=counts.get(label,0)+1;tested+=1
                witnesses.setdefault(label,{'full_square':square,'completed_ciphertext':cipher,'plaintext':plain,'historical_completion_claim':False})
                digest.update((square+'|'+cipher+'|'+plain+'\n').encode())
        completion_audits.append({'record':record['id'],'unknown_plaintext_positions':unknown_positions,
                                 'full_square_and_source_completion_pairs_tested':tested,
                                 'distinct_literal_plaintexts':len(counts),'completions_per_unknown_label_tuple':counts,
                                 'one_explicit_witness_per_literal_plaintext':witnesses,'ordered_enumeration_sha256':digest.hexdigest(),
                                 'interpretation':'Finite compatibility under the stated repaired candidate; no historical digit or erased coordinate is selected.'})
    assert completion_audits[0]['completions_per_unknown_label_tuple']=={d+d:24 for d in '56789'}
    assert completion_audits[1]['full_square_and_source_completion_pairs_tested']==720
    assert completion_audits[1]['distinct_literal_plaintexts']==10
    context=[]
    for source in inputs['contextual_unread_records']:
        lit=''.join(''.join(source['source_rows']).split());assert set(lit)<=set(C+'-')
        assert len(lit)==source['source_slots']
        assert sum(c in C for c in lit)==source['valid_coordinates']
        assert lit.count('-')==source['printed_erasure_slots']
        row={**source,'literal_source':lit}
        if source['id']=='p175_C3':
            assert len(lit)==217 and source['advertised_length']==222
            row['unlocated_length_shortfall']=5
        else:
            assert len(lit)==160 and lit.count('-')==86
            row['unfilled_native_frame_diagnostic']=inspect(lit.replace('-','?'),key,list(range(len(lit))))
        context.append(row)
    return {'schema':'adfgvx-romanian-ultimatum-companions-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':588,'valid_source_coordinates':580,
                       'modeled_coordinates':588,'plaintext_positions':294,'baseline_fixed_positions':284,
                       'candidate_fixed_positions':291,'known_coordinate_substitutions':6,
                       'source_or_model_erasure_fills':7,'unfilled_printed_erasure_coordinates':1,
                       'source_deletions':0,'published_key_changed':False},
            'records':records,'conditional_completion_audits':completion_audits,
            'contextual_unread_records_excluded_from_summary':context,
            'assembly':inputs['assembly'],'prior_attribution_check':inputs['prior_attribution_check'],'limits':inputs['limits']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true');parser.add_argument('--pdf',type=Path);args=parser.parse_args()
    result=build(args.pdf);path=HERE/'certificates.json'
    if args.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
