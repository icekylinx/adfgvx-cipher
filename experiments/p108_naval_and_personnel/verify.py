#!/usr/bin/env python3
"""Verify p108 naval and personnel messages, separating OCR loss from a printed short group.

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


def completion_witnesses(cipher,key,template):
    missing=[i for i,c in enumerate(cipher) if c=='?'];assert len(missing)==1
    out=[]
    for ch in C:
        full=cipher[:missing[0]]+ch+cipher[missing[0]+1:]
        plain=decrypt(full,key['column_rank_order'],key['square'])
        assert all(a=='?' or a==b for a,b in zip(template,plain))
        assert encrypt(plain,key['column_rank_order'],key['square'])==full
        out.append({'filled_model_index':missing[0],'coordinate':ch,'ciphertext':full,'plaintext':plain,'historical_completion_claim':False})
    return out


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert '?' not in key['square']
    for field in ['prior_attribution_check','ocr_snapshot']:assert sha(HERE/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C)
        assert len(literal)==source['source_slots'];base=literal;mapping=list(range(len(literal)))
        gap=source['missing_before_literal_index']
        if gap is not None:base=literal[:gap]+'?'+literal[gap:];mapping.insert(gap,None)
        assert len(base)==source['advertised_length']
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        assert candidate['raw']==raw['raw'] and candidate['ciphertext']==base
        assert not candidate['known_coordinate_substitutions'] and not candidate['erased_coordinate_fills']
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(literal),'valid_coordinates':len(literal),
                        'modeled_coordinates':len(base),'missing_before_literal_index':gap,
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[]})
    assert [r['source_slots'] for r in records]==[282,130,135]
    assert [len(r['ciphertext']) for r in records]==[282,130,136]
    assert [r['fixed_positions'] for r in records]==[141,65,67]
    assert all(r['readable_candidate']['full_plaintext_reencryption_verified'] for r in records[:2])
    snapshot=json.loads((HERE/'ocr_snapshot.json').read_text());old=''.join(snapshot['record_snapshot']['groups'])
    a=records[0];assert len(old)==280 and a['literal_source'][280:]=='FX'
    changes=[{'source_index':i,'ocr':u,'visible_source':v} for i,(u,v) in enumerate(zip(old,a['literal_source'][:280])) if u!=v]
    assert changes==[{'source_index':11,'ocr':'?','visible_source':'F'}]
    old_raw=inspect(old,key,list(range(280)))
    ocr={'snapshot_origin':snapshot['origin'],'earlier_ciphertext':old,'earlier_length':len(old),
         'earlier_output_under_same_key':old_raw,'source_visible_corrections':changes,
         'source_visible_tail_omitted_by_ocr':[{'source_index':280,'coordinate':'F'},{'source_index':281,'coordinate':'X'}],
         'source_coordinate_edits':0,'old_source_corpus_mutated':False}
    b=records[2];g=data['p108_B2_missing_group'];literal=b['literal_source']
    assert ' '.join(data['records'][2]['source_rows']).split()[4]=='DAGD'
    assert g['all_tested_insertion_boundaries']==list(range(20,25))
    assert b['positions'][66]['domain']=='027GQT' and b['positions'][66]['source_indices']==[35,None]
    witnesses=completion_witnesses(b['ciphertext'],key,b['raw']);variants=[]
    assert len({w['plaintext'] for w in witnesses})==6
    for gap in g['all_tested_insertion_boundaries']:
        base=literal[:gap]+'?'+literal[gap:];mapping=list(range(len(literal)));mapping.insert(gap,None)
        raw=inspect(base,key,mapping);template=g['diagnostic_word_prefix']+raw['raw'][66:]
        diagnostic=repair(template,base,key,mapping,literal)
        equivalents=[{'coordinate_in_primary_model':w['coordinate'],'same_complete_ciphertext':True} for w in witnesses if w['ciphertext']==diagnostic['ciphertext']]
        variants.append({'missing_before_literal_index':gap,'short_group_model':base[20:25],
                         'ciphertext':base,'model_to_source_indices':mapping,**raw,
                         'diagnostic_word_constraint':diagnostic,
                         'equivalent_primary_completion_witnesses':equivalents,
                         'all_six_raw_completion_witnesses':completion_witnesses(base,key,raw['raw']),
                         'counted_in_summary':False})
    assert [len(v['diagnostic_word_constraint']['known_coordinate_substitutions']) for v in variants]==[0,0,0,1,2]
    assert [len(v['diagnostic_word_constraint']['erased_coordinate_fills']) for v in variants]==[1,0,1,1,1]
    assert [v['equivalent_primary_completion_witnesses'] for v in variants]==[
        [{'coordinate_in_primary_model':'D','same_complete_ciphertext':True}],[],
        [{'coordinate_in_primary_model':'A','same_complete_ciphertext':True}],
        [{'coordinate_in_primary_model':'A','same_complete_ciphertext':True}],
        [{'coordinate_in_primary_model':'A','same_complete_ciphertext':True}]]
    union={w['ciphertext']:w['plaintext'] for v in variants for w in v['all_six_raw_completion_witnesses']}
    accepted={cipher:plain for cipher,plain in union.items() if plain[:66]==g['diagnostic_word_prefix']}
    assert len(union)==26 and len(accepted)==6
    assert set(accepted)=={w['ciphertext'] for w in witnesses}
    enumeration={'within_group_geometries':5,'coordinate_values_per_geometry':6,'geometry_labeled_completions':30,
                 'distinct_complete_ciphertexts':26,'distinct_complete_plaintexts':len(set(union.values())),
                 'distinct_completions_with_the_stated_readable_prefix':6,
                 'accepted_set_equals_primary_six_completions':True,
                 'constraint_is_lexical_not_independent_ciphertext_evidence':True}
    return {'schema':'adfgvx-p108-naval-and-personnel-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':547,'valid_source_coordinates':547,'modeled_coordinates':548,
                       'plaintext_positions':274,'baseline_fixed_positions':273,'candidate_fixed_positions':273,
                       'known_coordinate_substitutions':0,'source_or_model_erasure_fills':0,
                       'unfilled_missing_source_coordinates':1,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'p108_A_ocr_comparison':ocr,
            'p108_B2_all_five_gap_geometries':variants,'p108_B2_all_six_primary_completion_witnesses':witnesses,
            'p108_B2_complete_group_enumeration':enumeration,'p108_B2_geometry_limits':g,'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
