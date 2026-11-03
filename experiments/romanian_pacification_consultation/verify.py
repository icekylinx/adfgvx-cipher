#!/usr/bin/env python3
"""Verify four native p157 source frames and preserve a truncated contextual witness.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No published substitution square or numerical label is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import difflib
import re
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
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for field in ['prior_attribution_check','ocr_snapshot']:assert sha(HERE/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    snapshot=json.loads((HERE/'ocr_snapshot.json').read_text())
    old_by_id={r['id']:''.join(r['groups'])for r in snapshot['record_snapshots']}
    for source in data['records']:
        lit=''.join(source['source_rows']).replace(' ','');assert set(lit)<=set(C+'-')
        assert len(lit)==source['source_slots']==source['advertised_length']
        base=lit.replace('-','?');mapping=list(range(len(lit)))
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,lit)
        assert candidate['full_plaintext_reencryption_verified']
        display=re.sub(r'\[[^\]]*\]','',source['readable_german']).upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS')
        folded=''.join(ch for ch in display if ch in A)
        assert folded==candidate['raw'].replace('X','')
        old=old_by_id['p157_ocr_block'+source['source_section'][1:]]
        opcodes=[list(op) for op in difflib.SequenceMatcher(None,old,lit,autojunk=False).get_opcodes()]
        rebuilt=''.join(old[i:j] if tag=='equal' else lit[u:v] for tag,i,j,u,v in opcodes)
        assert rebuilt==lit
        comparison={'earlier_length':len(old),'literal_source_length':len(lit),'earlier_ciphertext':old,'sequence_alignment_opcodes':opcodes,'limit':'One exact reproducible text alignment, not a unique diagnosis of the OCR process and not a historical coordinate-repair cost.'}
        records.append({'id':source['id'],'readable_german':source['readable_german'],'readable_mapping_verified_after_disclosed_bracket_removal':True,'ocr_comparison':comparison,'literal_source':lit,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(lit),'valid_coordinates':sum(c in C for c in lit),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[200,218,210,128]
    assert [r['fixed_positions'] for r in records]==[100,109,105,63]
    assert [len(r['readable_candidate']['known_coordinate_substitutions'])for r in records]==[7,2,0,2]
    assert sum(len(r['readable_candidate']['erased_coordinate_fills'])for r in records)==1
    r=records[3];point=r['positions'][23]
    assert point['domain']=='02ACLR' and point['source_indices']==[99,27]
    witnesses=[]
    for ch in C:
        full=r['ciphertext'][:99]+ch+r['ciphertext'][100:]
        plain=decrypt(full,key['column_rank_order'],key['square'])
        assert encrypt(plain,key['column_rank_order'],key['square'])==full
        witnesses.append({'coordinate':ch,'ciphertext':full,'plaintext':plain,'historical_completion_claim':False})
    context=data['contextual_unread_records'][0]
    assert ''.join(context['source_rows']).replace(' ','')==context['literal_source']
    assert len(context['literal_source'])==83 and sum(c in C for c in context['literal_source'])==78
    assert context['literal_source'].count('-')==5 and not context['cataloged']
    a,b=data['copy_context']['comparison_literal_source'],context['literal_source']
    # Exact longest coordinate run, without a selected gap model.
    longest=0;hits=[]
    for i in range(len(a)):
        for j in range(len(b)):
            k=0
            while i+k<len(a) and j+k<len(b) and a[i+k]==b[j+k] and a[i+k] in C:k+=1
            if k>longest:longest=k;hits=[[i,j,k]]
            elif k==longest and k: hits.append([i,j,k])
    assert longest>=33
    c={'schema':'adfgvx-romanian-pacification-consultation-certificate-v1','project':data['project'],'authors':data['authors'],
       'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
       'summary':{'physical_records':4,'printed_source_slots':756,'valid_source_coordinates':755,'modeled_coordinates':756,
          'plaintext_positions':378,'baseline_fixed_positions':377,'candidate_fixed_positions':378,
          'known_coordinate_substitutions':sum(len(r['readable_candidate']['known_coordinate_substitutions'])for r in records),
          'source_or_model_erasure_fills':1,'source_deletions':0,'published_key_changed':False},
       'records':records,'p157_A5_all_six_raw_erasure_completions':witnesses,'headers':data['headers'],'contextual_unread_records':data['contextual_unread_records'],
       'copy_context':{**data['copy_context'],'longest_exact_valid_coordinate_run':longest,'maximal_run_starts_and_length':hits},
       'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}
    return c


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))

if __name__=='__main__':main()
