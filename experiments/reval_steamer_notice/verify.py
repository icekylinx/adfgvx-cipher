#!/usr/bin/env python3
"""Verify the Reval steamer notice and preserve all vessel-like and numerical fields.

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



def unchanged(record,token):
    start=record['raw'].index(token);points=record['positions'][start:start+len(token)]
    assert points==record['readable_candidate']['positions'][start:start+len(token)]
    return {'record':record['id'],'raw_field':token,'plaintext_start':start,'positions':points,'all_source_coordinates_unchanged':True}


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        literal=''.join(''.join(source['source_rows']).split());cipher=''.join(c if c in C else '?' for c in literal);mapping=list(range(len(cipher)))
        assert len(cipher)==source['source_slots']==source['advertised_length']
        raw=inspect(cipher,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],cipher,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'ciphertext':cipher,
                        'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate})
    assert [len(r['raw']) for r in records]==[100,104,81]
    assert [r['fixed_positions'] for r in records]==[100,103,78]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[0,3,1]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[0,1,1]
    retained=[unchanged(records[0],'RPHAXREVAL'),unchanged(records[0],'Y5111'),
              unchanged(records[1],'PETERXBENVIT'),unchanged(records[1],'B9VERN'),
              unchanged(records[1],'BAC4LON'),unchanged(records[2],'ROHAVAL'),
              unchanged(records[2],'N?YLY1XYYXYN?ANCHX')]
    alt=inputs['visual_alternative'];assert alt['source_index']==62
    assert records[0]['literal_source'][62]==alt['primary']=='D' and alt['alternative']=='V'
    alternate=records[0]['ciphertext'][:62]+'V'+records[0]['ciphertext'][63:]
    alt_read=inspect(alternate,key,list(range(len(alternate))))
    changed=[{'plaintext_index':i,'primary':a,'alternative':b} for i,(a,b) in enumerate(zip(records[0]['raw'],alt_read['raw'])) if a!=b]
    assert len(changed)==1 and changed[0]['primary']=='5' and changed[0]['alternative']=='P'
    assert alt_read['raw']==records[0]['raw'].replace('Y5111','YP111')
    assert len([p for p in records[2]['readable_candidate']['positions'] if p['raw']=='?'])==2
    inventory=[{'record':r['id'],'variant':v,'raw':reading['raw'],
                'all_numeral_and_JQY_occurrences':[p for p in reading['positions'] if p['raw'] in '0123456789JQY'],
                'all_unresolved_positions':[p for p in reading['positions'] if p['raw']=='?']}
               for r in records for v,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    return {'schema':'adfgvx-reval-steamer-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':570,'valid_source_coordinates':566,
                       'modeled_coordinates':570,'plaintext_positions':285,'baseline_fixed_positions':281,
                       'candidate_fixed_positions':283,'known_coordinate_substitutions':4,
                       'printed_erasure_fills':2,'printed_erasure_positions_retained':2,
                       'missing_coordinate_fills':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'unchanged_amount_reference_and_vessel_like_fields':retained,
            'source_glyph_alternative':{'input':alt,'ciphertext':alternate,**alt_read,
                                        'all_changed_plaintext_positions':changed,'historical_quantity_assigned':False},
            'complete_raw_label_and_domain_inventory':inventory,
            'prior_attribution_check':inputs['prior_attribution_check'],
            'limits':['The vessel-like strings are not identified as particular ships or normalized by a late-key hypothesis.',
                      'The amount and reference labels retain their raw values; no capacity or date is inferred.',
                      'The alternative overprinted glyph changes raw 5 to raw P; neither value is a recovered historical tonnage.',
                      'The message reports expected transport provision; it does not independently prove completion or arrival.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
