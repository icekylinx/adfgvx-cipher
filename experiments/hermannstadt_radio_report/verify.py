#!/usr/bin/env python3
"""Verify the Hermannstadt radio report and all conditional excess-coordinate geometries.

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



def framed(source, deleted=None):
    literal=''.join(''.join(source['source_rows']).split())
    cipher=''.join(c if c in C else '?' for c in literal);mapping=list(range(len(cipher)))
    if deleted is not None:
        cipher=cipher[:deleted]+cipher[deleted+1:];mapping.pop(deleted)
    return literal,cipher,mapping


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[];geometries=[]
    for source in inputs['records']:
        deletion=source['model'].get('primary_deleted_source_index')
        literal,base,mapping=framed(source,deletion)
        assert len(base)==source['advertised_length'] and len(literal)==source['source_slots']
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'key_id':key['id'],'literal_source':literal,'ciphertext':base,
            'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
            'model_to_source_indices':mapping,'deleted_source_coordinate':None if deletion is None else {'source_index':deletion,'printed':literal[deletion]},
            **raw,'readable_candidate':candidate})
        if deletion is None:continue
        costs=[];variants=[]
        for j in range(len(literal)):
            _,cipher,m=framed(source,j);edition=repair(source['readable_candidate'],cipher,key,m,literal)
            costs.append({'deleted_source_index':j,'deleted_literal_glyph':literal[j],
                          'known_coordinate_substitutions':len(edition['known_coordinate_substitutions']),
                          'printed_erasure_fills':len(edition['erased_coordinate_fills'])})
        minimum=min(x['known_coordinate_substitutions'] for x in costs)
        ties=[x['deleted_source_index'] for x in costs if x['known_coordinate_substitutions']==minimum]
        assert ties==source['model']['all_minimum_deleted_source_indices']
        for j in ties:
            _,cipher,m=framed(source,j)
            variants.append({'deleted_source_index':j,'deleted_literal_glyph':literal[j],
                'ciphertext':cipher,'model_to_source_indices':m,**inspect(cipher,key,m),
                'readable_candidate':repair(source['readable_candidate'],cipher,key,m,literal)})
        geometries.append({'record':source['id'],'scope':'Every deletion of one literal source slot, compared with the explicitly declared ordinary-word candidate. This is a conditional fit, not an independent original-text witness.',
            'trials':len(costs),'minimum_known_coordinate_substitutions':minimum,'all_costs':costs,
            'all_minimum_deleted_source_indices':ties,'primary_deleted_source_index':deletion,
            'all_equal_minimum_variants':variants,
            'all_repaired_ciphertexts_equal':len({v['readable_candidate']['ciphertext'] for v in variants})==1})
    assert [len(r['raw']) for r in records]==[123,121,122,99]
    assert [r['fixed_positions'] for r in records]==[123,121,122,98]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[1,6,5,0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[0,0,0,1]
    r=records[1];start=r['raw'].index('NIKOLA3EW');positions=r['positions'][start:start+9]
    assert positions==r['readable_candidate']['positions'][start:start+9]
    special=positions[6];assert special['raw']=='3' and special['pair']=='FD'
    assert all(None not in p['source_indices'] and '?' not in p['pair'] for p in positions)
    inventory=[{'record':r['id'],'variant':v,'raw':reading['raw'],
                'all_numeral_and_JQY_occurrences':[p for p in reading['positions'] if p['raw'] in '0123456789JQY'],
                'all_unresolved_positions':[p for p in reading['positions'] if p['raw']=='?']}
               for r in records for v,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    return {'schema':'adfgvx-hermannstadt-radio-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
      'input_sha256':sha(HERE/'inputs.json'),'indexing':'All plaintext, model and source indices are zero-based.',
      'summary':{'physical_records':4,'printed_source_slots':932,'valid_source_coordinates':931,
                 'modeled_coordinates':930,'plaintext_positions':465,'baseline_fixed_positions':464,
                 'candidate_fixed_positions':465,'known_coordinate_substitutions':12,'printed_erasure_fills':1,
                 'printed_erasure_positions_retained':0,'missing_coordinate_fills':0,'source_deletions':2,'published_key_changed':False},
      'records':records,'conditional_deletion_geometries':geometries,
      'unchanged_name_like_field':{'record':'p216_A2','field':'NIKOLA3EW','plaintext_start':start,'positions':positions,
         'all_name_coordinates_observed_and_unchanged':True,'special_position':special,
         'consequence_for_optional_GD_J':'This occurrence uses FD, not GD. Assigning J to GD leaves this position unresolved after clearing arbitrary labels; it does not turn NIKOLA3EW into NIKOLAJEW. Reading the same spelling would require an additional source/copying assumption.',
         'unapplied_one_coordinate_comparison':{'observed_pair':'FD','pair_if_this_position_were_GD':'GD','source_index':special['source_indices'][0],'printed':'F','hypothetical_replacement':'G','is_applied':False}},
      'complete_raw_label_and_domain_inventory':inventory,'prior_attribution_check':inputs['prior_attribution_check'],
      'limits':['The source explicitly defines four parts. No adjacent section-B financial request is merged into this report.',
                'The two single-deletion models remain conditional; every tied source mapping is retained.',
                'Raw NIKOLA3EW, dates and references remain unchanged. No global key labels are inferred from them.',
                'The message reports the sender’s communication experience and requests information; it does not independently establish the situation or official interpretation of the armistice.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
