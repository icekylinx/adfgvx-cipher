#!/usr/bin/env python3
"""Verify p107 railway and dragoman messages, preserving opaque references and a printed dash.

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
        out.append({'filled_source_index':missing[0],'coordinate':ch,'ciphertext':full,'plaintext':plain,'historical_completion_claim':False})
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
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C+'-')
        assert len(literal)==source['source_slots']==source['advertised_length']
        base=literal.replace('-','?');mapping=list(range(len(literal)))
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        assert not candidate['erased_coordinate_fills']
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[164,110,348]
    assert [r['fixed_positions'] for r in records]==[82,54,174]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[82,54,174]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[5,3,4]
    assert records[0]['readable_candidate']['full_plaintext_reencryption_verified']
    assert records[2]['readable_candidate']['full_plaintext_reencryption_verified']
    snapshot=json.loads((HERE/'ocr_snapshot.json').read_text());old=''.join(snapshot['record_snapshot']['groups'])
    b1=records[0];assert len(old)==160 and b1['literal_source'][160:]=='FDGD'
    changes=[{'source_index':i,'ocr':u,'visible_source':v} for i,(u,v) in enumerate(zip(old,b1['literal_source'][:160])) if u!=v]
    assert changes==[{'source_index':152,'ocr':'?','visible_source':'D'}]
    ocr={'snapshot_origin':snapshot['origin'],'earlier_ciphertext':old,'earlier_length':len(old),
         'earlier_output_under_same_key':inspect(old,key,list(range(160))),
         'source_visible_corrections':changes,
         'source_visible_tail_omitted_by_ocr':[{'source_index':160+i,'coordinate':c} for i,c in enumerate('FDGD')],
         'restoring_visible_OCR_tail_is_not_a_historical_source_insertion':True,'old_source_corpus_mutated':False}
    b2=records[1];unknown=b2['readable_candidate']['positions'][40]
    assert unknown['source_indices']==[39,67] and unknown['pair']=='?V' and unknown['domain']=='3BFKQS'
    witnesses=completion_witnesses(b2['readable_candidate']['ciphertext'],key,b2['readable_candidate']['raw'])
    return {'schema':'adfgvx-p107-railway-and-dragoman-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':622,'valid_source_coordinates':621,'modeled_coordinates':622,
                       'plaintext_positions':311,'baseline_fixed_positions':310,'candidate_fixed_positions':310,
                       'known_coordinate_substitutions':12,'source_or_model_erasure_fills':0,
                       'unfilled_printed_erasure_coordinates':1,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'source_notes':data['source_notes'],
            'p107_B1_ocr_comparison':ocr,'p107_B2_all_six_completion_witnesses':witnesses,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
