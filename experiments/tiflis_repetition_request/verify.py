#!/usr/bin/env python3
"""Verify the Tiflis request to repeat an encrypted telegram.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No published substitution square or numerical label is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
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
        page = doc[crop['pdf_page_1based']-1]
        if 'pdf_page_rotation_degrees' in crop:
            assert page.rotation == crop['pdf_page_rotation_degrees']
            assert crop['crop_coordinate_space'] == 'rotated_display_points'
        # Keep the PDF's native page rotation, as for the existing full crop.
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*rect))
        im = Image.open(relative_to/crop['path']).convert('RGB')
        assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples
        if 'rgb_sha256' in crop:
            assert im.size == (crop['width'], crop['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']


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
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C+'?')
        assert len(literal)==source['source_slots']==source['advertised_length']
        mapping=list(range(len(literal)));raw=inspect(literal,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],literal,key,mapping,literal)
        assert len(candidate['known_coordinate_substitutions'])==2 and len(candidate['erased_coordinate_fills'])==1
        assert candidate['full_plaintext_reencryption_verified']
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':literal,'source_slots':len(literal),'valid_coordinates':sum(ch in C for ch in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[314]
    assert [r['valid_coordinates'] for r in records]==[313]
    assert [r['fixed_positions'] for r in records]==[156]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[157]
    record=records[0];source=data['records'][0];glyph=source['ambiguous_glyph']
    assert record['id']=='p77_A' and glyph['source_index']==67
    assert record['literal_printed_rows'][1].split()[5]=='DX?XF'
    assert record['literal_source'][67]=='?' and record['literal_source'].count('?')==1
    position=record['positions'][147]
    assert position['source_indices']==[242,67] and position['pair']=='A?'
    assert position['raw']=='?' and position['domain']=='02HISX'
    candidate=record['readable_candidate']
    assert candidate['erased_coordinate_fills']==[
        {'model_index':67,'source_index':67,'printed':'?','from':'?','to':'X'}]
    assert [(e['source_index'],e['from'],e['to']) for e in candidate['known_coordinate_substitutions']]==[
        (91,'V','F'),(244,'X','G')]
    assert glyph['explicit_hypothesis_coordinates']==['X']
    assumed=record['ciphertext'][:67]+'X'+record['ciphertext'][68:]
    assumed_raw=inspect(assumed,key,record['model_to_source_indices'])
    assert assumed_raw['raw']==glyph['previous_definite_raw'] and assumed_raw['fixed_positions']==157
    assert assumed_raw['positions'][147]['raw']=='X'
    assert all(i==147 or a==b for i,(a,b) in enumerate(zip(assumed_raw['raw'],record['raw'])))
    assert encrypt(assumed_raw['raw'],key['column_rank_order'],key['square'])==assumed
    assumed_candidate=repair(source['readable_candidate'],assumed,key,record['model_to_source_indices'],record['literal_source'])
    assert assumed_candidate['ciphertext']==candidate['ciphertext']
    assert assumed_candidate['known_coordinate_substitutions']==candidate['known_coordinate_substitutions']
    assert not assumed_candidate['erased_coordinate_fills']
    assert assumed[67]==assumed_candidate['ciphertext'][67]=='X'
    prior=json.loads((HERE/data['prior_attribution_check']['path']).read_text())
    old=[r for screen in prior['earlier_repository_screens'] for r in screen['relevant_rows']
         if r.get('block')=='p77_ocr_block1' and r.get('key')=='Oct28-31']
    assert len(old)==1 and old[0]['ciphertext']==record['ciphertext']
    assert old[0]['plaintext']==record['raw'] and old[0]['ciphertext'][67]=='?'
    proposal=json.loads((HERE/'catalog_proposal.json').read_text())
    case_path=next(r['path'] for r in proposal if r['id']=='p77_A').split('#')[0]
    page=(ROOT/case_path).read_text()
    assert page.count('\n'+record['raw']+'\n')==1 and page.count('\n'+candidate['raw']+'\n')==1
    quote=' '.join(line[2:] for line in page.splitlines() if line.startswith('> '))
    normalized=quote.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS').replace('ß','SS')
    normalized=''.join(re.findall('[A-Z0-9]',normalized))
    assert normalized==candidate['raw'].replace('X','')
    glyph_review={
        'source_index':67,'literal_marker':'?',
        'source_position':{'row_1based':2,'group_in_row_1based':6,'character_in_group_1based':3},
        'detail_crop':glyph['detail_crop'],'appearance':glyph['appearance'],
        'conservative_plaintext_position':position,
        'primary_candidate_coordinate_operations':3,'primary_observed_substitutions':2,
        'primary_damaged_glyph_fills':1,'previous_definite_X_account_coordinate_operations':2,
        'additional_fill_not_reclassification':True,
        'explicit_assumption_branch':{
            'assumed_coordinate':'X','source_index':67,'source_observation_claim':False,'independent_copy_claim':False,
            'assumed_ciphertext_sha256':hashlib.sha256(assumed.encode()).hexdigest(),
            'raw_reading':{'raw':assumed_raw['raw'],'fixed_positions':assumed_raw['fixed_positions'],
                           'position_147':assumed_raw['positions'][147],
                           'all_other_raw_positions_match_conservative_primary':True},
            'raw_reencryption_verified':True,
            'main_candidate_from_this_assumption':{
                'plaintext_equals_primary_candidate':assumed_candidate['raw']==candidate['raw'],
                'ciphertext_equals_primary_candidate':True,
                'plaintext_sha256':hashlib.sha256(assumed_candidate['raw'].encode()).hexdigest(),
                'ciphertext_sha256':hashlib.sha256(assumed_candidate['ciphertext'].encode()).hexdigest(),
                'observed_coordinate_substitutions':assumed_candidate['known_coordinate_substitutions'],
                'damaged_glyph_replacements_after_assumption':[],
                'unassigned_glyph_fills_after_assumption':[],
                'total_coordinate_changes_from_assumed_stream':2,
                'roundtrip_verified':assumed_candidate['full_plaintext_reencryption_verified']},
            'limit':'The earlier X was retained unchanged by the old candidate. Assuming it again restores the former two-substitution account only conditionally; the conservative primary account additionally requires the X fill.'},
        'earlier_OCR':{'path':data['prior_attribution_check']['path'],'block':'p77_ocr_block1',
                      'same_conservative_ciphertext_verified':True,'same_raw_output_verified':True,
                      'independent_source_claim':False},
        'readable_mapping':{'case':case_path,'quote':quote,'normalized_display':normalized,
                            'complete_nonseparator_mapping_verified':True,
                            'separator_at_plaintext_147_is_conditional_fill':True},
        'limit':glyph['hypothesis_limit']}
    return {'schema':'adfgvx-tiflis-repetition-request-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':1,'printed_source_slots':314,'valid_source_coordinates':313,'modeled_coordinates':314,
                       'plaintext_positions':157,'baseline_fixed_positions':156,'candidate_fixed_positions':157,
                       'known_coordinate_substitutions':2,'source_or_model_erasure_fills':1,
                       'unfilled_printed_erasure_coordinates':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'source_notes':data['source_notes'],
            'p77_A_damaged_glyph_review':glyph_review,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
