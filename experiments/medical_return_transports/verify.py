#!/usr/bin/env python3
"""Verify medical return-transport readings, tied source frames and untouched labels.

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



def model_for(source, gap=None):
    literal=''.join(''.join(source['source_rows']).split())
    cipher=''.join(c if c in C else '?' for c in literal)
    mapping=list(range(len(literal)))
    if source['model']['kind']=='one_missing_group':
        if gap is None:gap=source['model']['primary_gap_before_source_index']
        cipher=cipher[:gap]+'?????'+cipher[gap:]
        mapping=mapping[:gap]+[None]*5+mapping[gap:]
    return literal,cipher,mapping


def unchanged_field(record,token):
    start=record['raw'].index(token)
    points=record['positions'][start:start+len(token)]
    assert points==record['readable_candidate']['positions'][start:start+len(token)]
    return {'record':record['id'],'raw_field':token,'plaintext_start':start,'positions':points,'all_coordinates_unchanged':True}


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        literal,cipher,mapping=model_for(source)
        assert len(literal)==source['source_slots']
        assert len(cipher)==source['advertised_length']
        raw=inspect(cipher,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],cipher,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'ciphertext':cipher,
                        'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate})
    assert [r['source_slots'] for r in records]==[339,224,280,318,276]
    assert [len(r['raw']) for r in records]==[172,112,140,159,138]
    assert [r['fixed_positions'] for r in records]==[166,112,139,158,137]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[9,5,5,5,0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[6,0,1,0,1]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[172,112,140,158,138]
    first=inputs['records'][0];template=first['readable_candidate'];stencil=masked_encryption(template,key)
    scores=[]
    for gap in range(first['source_slots']+1):
        literal,cipher,mapping=model_for(first,gap)
        differences=[{'model_index':i,'source_index':mapping[i],'from':a,'to':b}
                     for i,(a,b) in enumerate(zip(cipher,stencil)) if a!='?' and a!=b]
        scores.append({'gap_before_source_index':gap,'known_coordinate_substitutions':len(differences),
                       'differences':differences})
    best=min(s['known_coordinate_substitutions'] for s in scores)
    gaps=[s['gap_before_source_index'] for s in scores if s['known_coordinate_substitutions']==best]
    assert len(scores)==340 and best==9 and gaps==[104,105,107,108]
    assert gaps==first['model']['all_tied_minimum_gaps']
    assert [g for g in gaps if g%5==0]==[105]
    alternatives=[]
    for gap in gaps:
        literal,cipher,mapping=model_for(first,gap)
        raw=inspect(cipher,key,mapping);candidate=repair(template,cipher,key,mapping,literal)
        assert len(candidate['known_coordinate_substitutions'])==9
        assert len(candidate['erased_coordinate_fills'])==6
        assert candidate['ciphertext']==stencil
        alternatives.append({'gap_before_source_index':gap,'ciphertext':cipher,
                             'model_to_source_indices':mapping,**raw,'readable_candidate':candidate})
    prior_ranking=json.loads((HERE/'exploratory_gap_ranking.json').read_text())
    assert sha(ROOT/prior_ranking['model_path'])==prior_ranking['model_sha256']
    rank_model=json.loads((ROOT/prior_ranking['model_path']).read_text())
    ranked=[]
    for gap in range(first['source_slots']+1):
        literal,cipher,mapping=model_for(first,gap);raw=decrypt(cipher,key['column_rank_order'],key['square'])
        grams=[raw[i:i+4].lower() for i in range(len(raw)-3) if '?' not in raw[i:i+4]]
        score=sum(rank_model['weights'].get(g,rank_model['floor']) for g in grams)/len(grams) if grams else -99
        ranked.append({'hypothesis':gap,'score':score,'known_quadgrams':len(grams),
                       'known_plaintext':len(raw)-raw.count('?'),'plaintext':raw})
    ranked.sort(key=lambda r:-r['score']);assert ranked==prior_ranking['ranked_rows']

    # Preserve source-reviewed fragments without promoting them to readings.
    open_frames=[]
    for source in inputs['contextual_unread_records']:
        literal=''.join(''.join(source['source_rows']).split())
        assert len(literal)==source['source_slots'] and set(literal)<=set(C)
        assert source['source_reviewed'] and not source['readable_claim'] and not source['proposed_for_reading_catalog']
        open_frames.append({'id':source['id'],'literal_source':literal,'observed_coordinates':len(literal),
                            'advertised_length':source['advertised_length'],'readable_claim':False,
                            'proposed_for_reading_catalog':False})
    assert [(r['id'],r['observed_coordinates'],r['advertised_length']) for r in open_frames]==[
        ('p212_A2',160,284),('p212_A4',197,None)]
    by_id={r['id']:r for r in records}
    intact=[unchanged_field(by_id[i],'NIKOLA9EW') for i in ['p212_A1','p213_A6','p213_A7']]
    intact += [unchanged_field(by_id['p213_A7'],'KMXAXDXNRQJ0XXYYXY5XAYY'),
               unchanged_field(by_id['p213_A6'],'5T'),unchanged_field(by_id['p212_A5'],'2XX')]
    oil=by_id['p212_A3'];idx=oil['raw'].index('NUMM3R2')+6
    assert oil['positions'][idx]==oil['readable_candidate']['positions'][idx] and oil['raw'][idx]=='2'
    intact.append({'record':oil['id'],'raw_field':'2','plaintext_start':idx,
                   'positions':[oil['positions'][idx]],'all_coordinates_unchanged':True})
    medical6=by_id['p213_A6'];unknown=[p for p in medical6['positions'] if p['raw']=='?']
    assert len(unknown)==1 and unknown[0] in medical6['readable_candidate']['positions']
    assert medical6['readable_candidate']['raw'].count('?')==1
    assert medical6['raw'][unknown[0]['plaintext_index']+1:].startswith('DEPARTEMENT')
    inventory=[{'record':r['id'],'variant':v,'raw':reading['raw'],
                'all_numeral_and_JQY_occurrences':[p for p in reading['positions'] if p['raw'] in '0123456789JQY'],
                'all_unresolved_positions':[p for p in reading['positions'] if p['raw']=='?']}
               for r in records for v,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    alternative_inventory=[{'gap_before_source_index':r['gap_before_source_index'],'raw':r['raw'],
                            'all_numeral_and_JQY_occurrences':[p for p in r['positions'] if p['raw'] in '0123456789JQY'],
                            'all_unresolved_positions':[p for p in r['positions'] if p['raw']=='?']}
                           for r in alternatives]
    return {'schema':'adfgvx-medical-return-transports-certificate-v1','project':inputs['project'],
            'authors':inputs['authors'],'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All indices are zero-based.',
            'summary':{'physical_records':5,'additional_open_source_frames_not_counted':2,
                       'printed_source_slots':1437,'valid_source_coordinates':1433,
                       'modeled_coordinates':1442,'plaintext_positions':721,
                       'baseline_fixed_positions':712,'candidate_fixed_positions':720,
                       'known_coordinate_substitutions':24,'printed_erasure_fills':3,
                       'missing_coordinate_fills':5,'printed_erasure_positions_retained':1,
                       'source_deletions':0,'published_key_changed':False,
                       'p212_A1_exact_gap_fit_is_unique':False,'p212_A1_all_tied_minimum_gaps':gaps,
                       'semantically_unresolved_received_bridge_labels':2},
            'records':records,'first_part_conditional_geometry':{
                'assumption':'One contiguous five-coordinate gap and the recorded readable candidate; the candidate itself is not an independent witness.',
                'candidate':template,'all340_exact_gap_scores':scores,'minimum_observed_coordinate_substitutions':best,
                'all_tied_minimum_gaps':gaps,'primary_gap':105,
                'primary_selection_is_additional_source_group_boundary_assumption':True,
                'all_tied_variant_certificates':alternatives,
                'language_ranking_certifies_history':False},
            'contextual_unread_records':open_frames,
            'unchanged_name_instruction_and_reference_fields':intact,
            'unresolved_position_before_DEPARTEMENT':unknown[0],
            'complete_raw_label_and_domain_inventory':inventory,
            'complete_tied_geometry_raw_label_inventory':alternative_inventory,
            'assembly_limits':inputs['assembly_limits'],'prior_attribution_check':inputs['prior_attribution_check'],
            'limits':['The first-part reading is a costed conditional reconstruction with four equally economical gap placements, not a unique source recovery.',
                      'The oil-cartel query has no explicit part 3 label and is not merged into the medical account.',
                      'Parts 2/4 have no asserted reading and add zero records to the readable catalog.',
                      'NIKOLA9EW, the 5T bridge, the instruction label 2 and the complete final reference remain in their raw published-square labels.',
                      'The erased position before DEPARTEMENT and the meaning of 5T remain unresolved.',
                      'These medical recommendations do not establish that the requested equipment or supplies were provided.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
