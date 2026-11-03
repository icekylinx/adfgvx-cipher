#!/usr/bin/env python3
"""Verify Constanza naval-radio connections, repeated parts and source annotation.

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
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        literal=''.join(''.join(source['source_rows']).split());mapping=list(range(len(literal)))
        assert set(literal)<=set(C) and len(literal)==source['source_slots']==source['model']['coordinates']
        if source['id']=='p82_A1':assert source['advertised_length']==342 and len(literal)==242
        else:assert len(literal)==source['advertised_length']
        raw=inspect(literal,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],literal,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'ciphertext':literal,
                        'source_slots':len(literal),'advertised_length':source['advertised_length'],
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate})
    assert [len(r['raw']) for r in records]==[121,124,121,124,105,59]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[1,2,0,1,1,0]
    assert all(not r['readable_candidate']['erased_coordinate_fills'] for r in records)
    assert all(r['fixed_positions']==len(r['raw']) for r in records)
    duplicate_pairs=[]
    for li,ri,at in [(0,2,94),(1,3,55)]:
        left,right=records[li],records[ri]
        diffs=[{'source_index':i,'left':a,'right':b} for i,(a,b) in enumerate(zip(left['literal_source'],right['literal_source'])) if a!=b]
        assert len(diffs)==1 and diffs[0]['source_index']==at
        assert left['readable_candidate']['ciphertext']==right['readable_candidate']['ciphertext']
        duplicate_pairs.append({'left_record':left['id'],'right_record':right['id'],
                                'all_observed_source_differences':diffs,
                                'candidate_ciphertexts_identical':True,
                                'raw_left':left['raw'],'raw_right':right['raw'],
                                'candidate_plaintext':left['readable_candidate']['raw'],
                                'position_witnesses':[{'index':i,'left_raw':a,'right_raw':b,
                                                      'left_candidate':left['readable_candidate']['positions'][i],
                                                      'right_candidate':right['readable_candidate']['positions'][i]}
                                                     for i,(a,b) in enumerate(zip(left['positions'],right['positions']))]})
    annotation=inputs['source_annotation'];p80b2=records[1];p82a2=records[3]
    assert annotation['source_index']==55 and p80b2['literal_source'][55]=='G' and p82a2['literal_source'][55]=='F'
    annotated=p80b2['literal_source'][:55]+'F'+p80b2['literal_source'][56:]
    assert annotated==p82a2['literal_source']
    annotation_read=inspect(annotated,key,list(range(len(annotated))))
    assert annotation_read['raw']==p82a2['raw']
    assert annotation_read['raw'].startswith('FREMDLAENDISCHEN') and 'PACH' in annotation_read['raw']
    # The shared PACH spelling is not corrected merely by copying a witness:
    # both observed sources contain it, and its extra repair is priced twice.
    common_error=[]
    for record in [p80b2,p82a2]:
        start=record['raw'].index('PACH')
        assert record['readable_candidate']['raw'][start:start+4]=='NACH'
        event=next(e for e in record['readable_candidate']['known_coordinate_substitutions'] if e['source_index']==142)
        assert event['from']=='G' and event['to']=='X'
        common_error.append({'record':record['id'],'raw_positions':record['positions'][start:start+4],
                             'candidate_positions':record['readable_candidate']['positions'][start:start+4],
                             'independent_raw_NACH_witness_in_this_pair':False,'repair':event})
    inventory=[{'record':r['id'],'variant':v,'raw':reading['raw'],
                'all_numeral_and_JQY_occurrences':[p for p in reading['positions'] if p['raw'] in '0123456789JQY']}
               for r in records for v,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    refs=[]
    for r in [records[0],records[2]]:
        token='13558X13558X1XROEMX1VOM29X10XXAUFDORTXTELEGRXNRX351BRUCHSTRX18VOM25X10'
        start=r['raw'].index(token);points=r['positions'][start:start+len(token)]
        assert points==r['readable_candidate']['positions'][start:start+len(token)]
        refs.append({'record':r['id'],'raw_field':token,'plaintext_start':start,'positions':points,'all_coordinates_unchanged':True})
    return {'schema':'adfgvx-constanza-radio-certificate-v1','project':inputs['project'],
            'authors':inputs['authors'],'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All indices are zero-based.',
            'summary':{'physical_records':6,'printed_source_slots':1308,'valid_source_coordinates':1308,
                       'modeled_coordinates':1308,'plaintext_positions':654,'baseline_fixed_positions':654,
                       'candidate_fixed_positions':654,'known_coordinate_substitutions':5,
                       'source_annotation_supported_substitutions':1,'printed_erasure_fills':0,
                       'missing_coordinate_fills':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'duplicate_part_comparisons':duplicate_pairs,
            'source_annotation_layer':{'input':annotation,'ciphertext':annotated,**annotation_read,
                                       'identical_to_independent_typed_p82_A2':True,
                                       'further_common_PACH_error_remains':True},
            'common_error_separately_priced':common_error,'unchanged_reference_and_date_fields':refs,
            'complete_raw_label_inventory':inventory,'assembly':inputs['assembly'],
            'prior_attribution_check':inputs['prior_attribution_check'],
            'limits':['p82 A1 advertises 342 but prints 242; the observed-length model is supported by the independent 242-coordinate p80 copy. No 100-coordinate insertion is claimed.',
                      'The source annotation supplies F above typed G; its author and date are unknown.',
                      'Both part 2 copies have PACH. Their NACH reading is a separately priced ordinary-word candidate, not an unchanged duplicate witness.',
                      'The reference/date labels, duplicate 13558 and ROEMX1 are unchanged.',
                      'The message describes communications connections; it is not an independent operational test of those links.',
                      'Earlier unreviewed bodies and the limits of prior-attribution checks remain explicit.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
