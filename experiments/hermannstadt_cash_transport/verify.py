#!/usr/bin/env python3
"""Verify the Hermannstadt cash transport notice and its tied short-group geometries.

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



def framed(source, gap=None):
    literal = ''.join(''.join(source['source_rows']).split())
    base = ''.join(c if c in C else '?' for c in literal)
    mapping = list(range(len(base)))
    if gap is not None:
        base = base[:gap]+'?'+base[gap:]
        mapping = mapping[:gap]+[None]+mapping[gap:]
    return literal, base, mapping


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        gap=source['model'].get('primary_gap')
        literal,base,mapping=framed(source,gap)
        assert len(base)==source['advertised_length'] and len(literal)==source['source_slots']
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'key_id':key['id'],'literal_source':literal,'ciphertext':base,
            'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
            'model_to_source_indices':mapping,**raw,'readable_candidate':candidate})
    source=inputs['records'][0];costs=[];variants=[]
    for gap in range(source['source_slots']+1):
        literal,base,mapping=framed(source,gap)
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        costs.append({'gap_before_source_index':gap,'known_coordinate_substitutions':len(candidate['known_coordinate_substitutions']),
                      'printed_erasure_fills':sum(p['source_index'] is not None for p in candidate['erased_coordinate_fills']),
                      'missing_coordinate_fills':sum(p['source_index'] is None for p in candidate['erased_coordinate_fills'])})
    minimum=min(x['known_coordinate_substitutions'] for x in costs)
    ties=[x['gap_before_source_index'] for x in costs if x['known_coordinate_substitutions']==minimum]
    assert ties==source['model']['equal_minimum_gaps']==[98,99] and minimum==5
    for gap in ties:
        literal,base,mapping=framed(source,gap)
        variants.append({'gap_before_source_index':gap,'ciphertext':base,'model_to_source_indices':mapping,
                         **inspect(base,key,mapping),'readable_candidate':repair(source['readable_candidate'],base,key,mapping,literal)})
    assert variants[0]['readable_candidate']['ciphertext']==variants[1]['readable_candidate']['ciphertext']
    assert [len(r['raw']) for r in records]==[101,95]
    assert [r['fixed_positions'] for r in records]==[99,94]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[5,0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[2,0]
    nine=[p for p in records[1]['positions'] if p['raw']=='9']
    assert len(nine)==1 and nine[0]['plaintext_index']==46 and nine[0]['pair']=='GD' and nine[0]['source_indices']==[116,185]
    assert records[1]['ciphertext'][116]=='G' and records[1]['ciphertext'][185]=='D'
    inventory=[{'record':r['id'],'variant':v,'raw':reading['raw'],
                'all_numeral_and_JQY_occurrences':[p for p in reading['positions'] if p['raw'] in '0123456789JQY'],
                'all_unresolved_positions':[p for p in reading['positions'] if p['raw']=='?']}
               for r in records for v,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    return {'schema':'adfgvx-hermannstadt-cash-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
      'input_sha256':sha(HERE/'inputs.json'),'indexing':'All plaintext, model and source indices are zero-based; null source indices are inserted gaps.',
      'summary':{'physical_records':2,'printed_source_slots':391,'valid_source_coordinates':389,
                 'modeled_coordinates':392,'plaintext_positions':196,'baseline_fixed_positions':193,
                 'candidate_fixed_positions':195,'known_coordinate_substitutions':5,'printed_erasure_fills':1,
                 'printed_erasure_positions_retained':1,'missing_coordinate_fills':1,'source_deletions':0,'published_key_changed':False},
      'records':records,'conditional_short_group_geometry':{'scope':'Every single-coordinate insertion in the 201-slot literal source, scored against the explicitly declared ordinary-word candidate; this is conditional geometry, not independently known plaintext.',
          'placements_evaluated':len(costs),'minimum_known_coordinate_substitutions':minimum,'all_costs':costs,
          'all_equal_minimum_variants':variants,'same_repaired_ciphertext':True},
      'independent_raw_9_word_observation':{'record':'p216_B2','raw_context':'OKM9EWEILSMITTEILEN',
          'coordinate_positions':nine,'proposed_separate_lexical_test':'9EWEILS may represent JEWEILS. No key assignment is made in this source edition.'},
      'complete_raw_label_and_domain_inventory':inventory,'prior_attribution_check':inputs['prior_attribution_check'],
      'limits':['Part 1 geometry and ordinary-word repairs remain conditional; both equal-minimum source ownership maps are retained.',
                'The source edition does not change raw 9, raw 8, dates, reference labels or the KRO abbreviation.',
                'The dated heading and origin are 24 November, while the received heading says 26 November; all are transcribed without resolving the discrepancy.',
                'The request does not establish that the aircraft had departed or that the cash was sent or received.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
