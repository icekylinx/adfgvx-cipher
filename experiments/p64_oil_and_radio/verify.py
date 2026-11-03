#!/usr/bin/env python3
"""Verify p64 oil inquiry and radio report, retaining all annotated and unresolved fields.

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


def parse_rows(rows):
    literal=[];parenthesized=[]
    for group in ' '.join(rows).split():
        i=0
        while i<len(group):
            if group[i]=='(':
                assert group[i+2]==')' and group[i+1] in C
                parenthesized.append(len(literal));literal.append(group[i+1]);i+=3
            else:
                assert group[i] in C+'-'
                literal.append(group[i]);i+=1
    return ''.join(literal),parenthesized


def complete_one_mask(cipher,key,template):
    erased=[i for i,c in enumerate(cipher) if c=='?'];assert len(erased)==1
    results=[]
    for value in C:
        full=cipher[:erased[0]]+value+cipher[erased[0]+1:]
        plain=decrypt(full,key['column_rank_order'],key['square'])
        assert all(a=='?' or a==b for a,b in zip(template,plain))
        assert encrypt(plain,key['column_rank_order'],key['square'])==full
        results.append({'source_or_frame_index':erased[0],'coordinate_value':value,'plaintext':plain,
                        'complete_ciphertext':full,'historical_completion_claim':False})
    return results


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert '?' not in key['square']
    assert sha(HERE/'prior_candidates.json')==data['prior_attribution_check']['earlier_repository_candidates']['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal,parenthesized=parse_rows(source['source_rows']);assert len(literal)==source['source_slots']==source['advertised_length']
        base=literal.replace('-','?');mapping=list(range(len(base)));raw=inspect(base,key,mapping)
        assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'parenthesized_coordinate_indices':parenthesized,'model_to_source_indices':mapping,
                        **raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[346,354,176]
    assert [r['fixed_positions'] for r in records]==[172,177,87]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[173,177,87]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[4,5,1]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[1,0,0]
    assert records[1]['parenthesized_coordinate_indices']==[90,353]
    sensitivity=[]
    a1=records[0];masked=list(a1['ciphertext'])
    for i,letter in [(39,'V'),(119,'X'),(159,'F')]:
        assert masked[i]==letter;masked[i]='?'
    base=''.join(masked);raw=inspect(base,key,a1['model_to_source_indices'])
    candidate=repair(a1['readable_candidate']['raw'],base,key,a1['model_to_source_indices'],a1['literal_source'])
    assert raw['fixed_positions']==169 and len(candidate['erased_coordinate_fills'])==4
    sensitivity.append({'record':'p64_A1','variant':'three_faded_primary_glyphs_masked','hypothetically_masked_source_indices':[39,119,159],
                        'ciphertext':base,**raw,'readable_candidate':candidate,
                        'counted_in_primary_summary':False})
    a2=records[1]
    for indices in [[90],[353],[90,353]]:
        masked=list(a2['ciphertext'])
        for i in indices:masked[i]='?'
        base=''.join(masked);raw=inspect(base,key,a2['model_to_source_indices'])
        template=a2['readable_candidate']['raw']
        if 353 in indices:template=template[:175]+'?'+template[176:]
        candidate=repair(template,base,key,a2['model_to_source_indices'],a2['literal_source'])
        row={'record':'p64_A2','variant':'parenthesized_X_masked_'+('_'.join(map(str,indices))),
             'hypothetically_masked_source_indices':indices,'ciphertext':base,**raw,
             'readable_candidate':candidate,'counted_in_primary_summary':False}
        if 353 in indices:
            point=candidate['positions'][175];assert point['pair']=='?G' and point['domain']=='57DSTU'
            row['reference_domain']=point;row['decimal_only_reference_digit_choices']='57'
            row['complete_compatibility_witnesses']=complete_one_mask(candidate['ciphertext'],key,candidate['raw'])
        sensitivity.append(row)
    radio=records[2];hour=radio['readable_candidate']['positions'][30]
    assert hour['pair']=='F?' and hour['source_indices']==[82,162] and hour['domain']=='1EKLOS'
    witnesses=complete_one_mask(radio['readable_candidate']['ciphertext'],key,radio['readable_candidate']['raw'])
    digit_choices=''.join(c for c in hour['domain'] if c.isdigit());assert digit_choices=='1'
    numeric_template=radio['readable_candidate']['raw'].replace('?','1')
    conditional=repair(numeric_template,radio['readable_candidate']['ciphertext'],key,radio['model_to_source_indices'],radio['literal_source'])
    assert not conditional['known_coordinate_substitutions'] and len(conditional['erased_coordinate_fills'])==1
    return {'schema':'adfgvx-p64-oil-and-radio-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':876,'valid_source_coordinates':874,'modeled_coordinates':876,
                       'plaintext_positions':438,'baseline_fixed_positions':436,'candidate_fixed_positions':437,
                       'known_coordinate_substitutions':10,'source_or_model_erasure_fills':1,
                       'unfilled_printed_erasure_coordinates':1,'source_deletions':0,'published_key_changed':False},
            'records':records,'source_qualification_sensitivity_variants':sensitivity,
            'radio_hour_unknown':{'position':hour,'all_six_complete_compatibility_witnesses':witnesses,
                                  'conditional_decimal_field_interpretation':{'assumption':'The unknown character in the field ?600UHR is a decimal digit.','digit_choices':digit_choices,'resulting_literal_field':'1600UHR','additional_candidate':conditional,'counted_in_primary_summary':False}},
            'headers':data['headers'],'source_annotations':data['source_annotations'],
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
