#!/usr/bin/env python3
"""Verify the five-part evacuation routing assembly and the explicit100-coordinate loss.

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


def complete_witness_family(candidate,key):
    indices=[i for i,c in enumerate(candidate['ciphertext']) if c=='?'];assert len(indices)==31
    points=[p for p in candidate['positions'] if p['raw']=='?'];assert len(points)==28
    assert sum(len(p['domain'])==36 for p in points)==3 and sum(len(p['domain'])==6 for p in points)==25
    baseline=candidate['ciphertext'].replace('?','A');plain=decrypt(baseline,key['column_rank_order'],key['square'])
    assert encrypt(plain,key['column_rank_order'],key['square'])==baseline
    assert all(a=='?' or a==b for a,b in zip(candidate['raw'],plain))
    witnesses=[]
    for i in indices:
        for value in C[1:]:
            c=baseline[:i]+value+baseline[i+1:];p=decrypt(c,key['column_rank_order'],key['square'])
            assert encrypt(p,key['column_rank_order'],key['square'])==c
            assert all(a=='?' or a==b for a,b in zip(candidate['raw'],p))
            witnesses.append({'model_index':i,'value':value,'ciphertext':c,'plaintext':p})
    return {'unfilled_missing_coordinate_indices':indices,'unresolved_plaintext_positions':points,
            'exact_distinct_complete_plaintexts':6**31,'equivalent_domain_product':36**3*6**25,
            'counting_proof':'The complete square and fixed transposition are bijective. Each of31independent unknown coordinate slots has6choices; these give6^31different ciphertexts and therefore different plaintexts. Three plaintext positions contain two erasures and25contain one, giving the same36^3*6^25count.',
            'enumeration_scope':'One canonical witness plus155single-coordinate alternatives are materialized. The full6^31space is counted mathematically, not enumerated.',
            'canonical_witness':{'ciphertext':baseline,'plaintext':plain},'single_coordinate_alternatives':witnesses,
            'historical_completion_claim':False}


def copy_audit(data,literal):
    path=ROOT/data['corpus_path'];assert sha(path)==data['corpus_sha256']
    blocks=json.loads(path.read_text())['blocks'];assert len(blocks)==788 and data['query']==literal
    grams={literal[i:i+10] for i in range(len(literal)-9) if '-' not in literal[i:i+10] and not(i<200<i+10)}
    hits=[]
    for block in blocks:
        cipher=''.join(block['groups']);matches=[{'corpus_start':i,'literal':cipher[i:i+10]} for i in range(len(cipher)-9) if cipher[i:i+10] in grams]
        if matches:hits.append({'id':block['id'],'matches':matches})
    assert hits==data['hits'] and {r['id'] for r in hits}=={'p89_ocr_block1','p89_ocr_block2'}
    return {'corpus_block_count':788,'known_side_10mer_count':len(grams),'hits':hits,'independent_literal_copy_found':False,'limit':data['limit']}


def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key']
    assert data['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    assert '?' not in key['square']
    for field in ['prior_attribution_check','existing_part2','literal_copy_audit']:assert sha(HERE/data[field]['path'])==data[field]['sha256']
    for crop in data['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,data['source'],data['source_images'],HERE)
    records=[]
    for source in data['records']:
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C+'-') and len(literal)==source['source_slots']
        base=literal.replace('-','?');mapping=list(range(len(base)))
        loss=source.get('explicit_source_loss')
        if loss:
            assert source['id']=='p89_A3' and len(literal)==258 and loss['source_offset']==200
            assert loss['missing_groups']*loss['coordinates_per_group']==loss['missing_coordinates']==100
            base=base[:200]+'?'*100+base[200:];mapping=mapping[:200]+[None]*100+mapping[200:]
        assert len(base)==source['advertised_length'];raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        source_fills=[e for e in candidate['erased_coordinate_fills'] if e['source_index'] is not None]
        missing_fills=[e for e in candidate['erased_coordinate_fills'] if e['source_index'] is None]
        r={'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
           'ciphertext':base,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
           'modeled_coordinates':len(base),'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
           'printed_dash_fills':source_fills,'explicitly_missing_coordinate_fills':missing_fills,
           'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]}
        if loss:
            assert candidate['raw'][127:]==raw['raw'][127:] and '?' not in candidate['raw'][:127]
            assert len(source_fills)==1 and len(missing_fills)==69 and candidate['ciphertext'].count('?')==31
            assert all(mapping[i] is None for i,c in enumerate(candidate['ciphertext']) if c=='?')
            assert [(e['source_index'],e['to']) for e in candidate['known_coordinate_substitutions']]==[(243,'G')]
            r['explicit_source_loss']=loss;r['completion_count_and_witnesses']=complete_witness_family(candidate,key)
        records.append(r)
    assert [r['source_slots'] for r in records]==[298,258,360,398]
    assert [r['fixed_positions'] for r in records]==[149,81,180,199]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[149,151,180,199]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[1,1,4,2]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[0,70,0,0]
    assert all(r['readable_candidate']['full_plaintext_reencryption_verified'] for r in records if r['id']!='p89_A3')
    existing=json.loads((HERE/'existing_part2.json').read_text())
    assert existing['key']=={'column_rank_order':key['column_rank_order'],'square':key['square']}
    assert ''.join(existing['source_rows']).replace(' ','').replace('-','?')==existing['ciphertext']
    prior=inspect(existing['ciphertext'],key,list(range(290)));assert prior['raw']==existing['expected_raw'] and prior['fixed_positions']==142
    context={'id':'p89_A2','counted_as_new_record':False,'prior_credit':existing['prior_credit'],'origin':existing['origin'],**prior,'changed_source_or_reading':False}
    audit=copy_audit(json.loads((HERE/'literal_copy_audit.json').read_text()),records[1]['literal_source'])
    return {'schema':'adfgvx-black-sea-evacuation-routes-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':4,'printed_source_slots':1314,'valid_source_coordinates':1313,'modeled_coordinates':1414,
                       'plaintext_positions':707,'baseline_fixed_positions':609,'candidate_fixed_positions':679,
                       'known_coordinate_substitutions':8,'source_or_model_erasure_fills':70,
                       'printed_dash_fills':1,'source_declared_missing_coordinates':100,'missing_coordinate_fills':69,
                       'unfilled_missing_coordinates':31,'unfilled_printed_erasure_coordinates':0,'source_deletions':0,'published_key_changed':False},
            'records':records,'existing_credited_part2_context':context,'headers':data['headers'],
            'printed_cleartext_after_part5':data['printed_cleartext_after_part5'],'printed_cleartext_counted_in_ciphertext_totals':False,
            'source_annotations':data['source_annotations'],'bounded_literal_copy_audit':audit,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
