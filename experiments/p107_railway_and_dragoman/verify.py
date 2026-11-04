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
        pix = doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*rect))
        im = Image.open(relative_to/crop['path']).convert('RGB')
        assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples
        if 'rgb_sha256' in crop:
            assert im.size == (crop['width'], crop['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']


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
        literal=''.join(source['source_rows']).replace(' ','');assert set(literal)<=set(C+'-?')
        assert len(literal)==source['source_slots']==source['advertised_length']
        base=literal.replace('-','?');mapping=list(range(len(literal)))
        raw=inspect(base,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],base,key,mapping,literal)
        records.append({'id':source['id'],'literal_source':literal,'literal_printed_rows':source['source_rows'],
                        'ciphertext':base,'source_slots':len(literal),'valid_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate,
                        'all_changed_plaintext_positions':[{'before':a,'after':b} for a,b in zip(raw['positions'],candidate['positions']) if a!=b]})
    assert [r['source_slots'] for r in records]==[164,110,348]
    assert [r['valid_coordinates'] for r in records]==[164,109,347]
    assert [r['fixed_positions'] for r in records]==[82,54,173]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[82,54,174]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[5,3,3]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[0,0,1]
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
    c=records[2];source=data['records'][2];glyph=source['ambiguous_glyph']
    assert c['id']=='p107_C' and glyph['source_index']==45
    assert c['literal_printed_rows'][1].split()[1]=='?XGFF'
    assert c['literal_source'][45]=='?' and c['ciphertext'].count('?')==1
    assert c['positions'][85]['raw']=='?' and c['positions'][85]['domain']=='9FILOU'
    assert 45 in c['positions'][85]['source_indices']
    assert c['readable_candidate']['erased_coordinate_fills']==[
        {'model_index':45,'source_index':45,'printed':'?','from':'?','to':'V'}]
    assert [(e['source_index'],e['from'],e['to']) for e in c['readable_candidate']['known_coordinate_substitutions']]==[
        (182,'F','V'),(253,'X','V'),(292,'D','A')]
    glyph_branches=[]
    for coordinate in glyph['explicit_hypothesis_coordinates']:
        assert coordinate in ('X','V')
        assumed=c['ciphertext'][:45]+coordinate+c['ciphertext'][46:]
        reading=inspect(assumed,key,c['model_to_source_indices'])
        assert reading['fixed_positions']==174
        assert encrypt(reading['raw'],key['column_rank_order'],key['square'])==assumed
        assert reading['raw'][85]=={'X':'9','V':'F'}[coordinate]
        assert all(i==85 or a==b for i,(a,b) in enumerate(zip(reading['raw'],c['raw'])))
        if coordinate=='X':assert reading['raw']==glyph['previous_definite_raw']
        evaluated=repair(source['readable_candidate'],assumed,key,c['model_to_source_indices'],c['literal_source'])
        assert evaluated['ciphertext']==c['readable_candidate']['ciphertext']
        assert not evaluated['erased_coordinate_fills']
        real_changes=[e for e in evaluated['known_coordinate_substitutions'] if e['source_index']!=45]
        assumed_changes=[e for e in evaluated['known_coordinate_substitutions'] if e['source_index']==45]
        assert real_changes==c['readable_candidate']['known_coordinate_substitutions']
        assert len(assumed_changes)==(coordinate=='X')
        glyph_branches.append({
            'assumed_coordinate':coordinate,'source_index':45,
            'source_observation_claim':False,'independent_copy_claim':False,
            'assumed_ciphertext_sha256':hashlib.sha256(assumed.encode()).hexdigest(),
            'raw_reading':{'raw':reading['raw'],'fixed_positions':reading['fixed_positions'],
                           'position_85':reading['positions'][85],
                           'all_other_raw_positions_match_conservative_primary':True},
            'raw_reencryption_verified':True,
            'main_candidate_from_this_assumption':{
                'plaintext_equals_primary_candidate':evaluated['raw']==c['readable_candidate']['raw'],
                'ciphertext_equals_primary_candidate':evaluated['ciphertext']==c['readable_candidate']['ciphertext'],
                'plaintext_sha256':hashlib.sha256(evaluated['raw'].encode()).hexdigest(),
                'ciphertext_sha256':hashlib.sha256(evaluated['ciphertext'].encode()).hexdigest(),
                'observed_coordinate_substitutions':real_changes,
                'assumed_glyph_replacements':assumed_changes,
                'unassigned_glyph_fills_after_assumption':[],
                'total_coordinate_changes_from_assumed_stream':len(real_changes)+len(assumed_changes),
                'roundtrip_verified':evaluated['full_plaintext_reencryption_verified']},
            'limit':'Assigning the damaged glyph is a separate hypothesis. It is not an added observation or a lower-cost primary reading.'})
    assert [b['assumed_coordinate'] for b in glyph_branches]==['X','V']
    prior=json.loads((HERE/data['prior_attribution_check']['path']).read_text())
    old_c=[r for screen in prior['earlier_repository_screens'] for r in screen['relevant_rows']
           if r.get('block')=='p107_ocr_block4' and r.get('key')=='Nov1-3']
    assert len(old_c)==1 and old_c[0]['ciphertext']==c['ciphertext']
    assert old_c[0]['plaintext']==c['raw'] and old_c[0]['ciphertext'][45]=='?'
    proposal=json.loads((HERE/'catalog_proposal.json').read_text())
    case_path=next(r['path'] for r in proposal if r['id']=='p107_C').split('#')[0]
    page=(ROOT/case_path).read_text()
    assert page.count('\n'+c['raw']+'\n')==1
    assert page.count('\n'+c['readable_candidate']['raw']+'\n')==1
    quote=' '.join(line[2:] for line in page.splitlines() if line.startswith('> '))
    normalized=quote.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS').replace('ß','SS')
    normalized=''.join(re.findall('[A-Z0-9]',normalized))
    assert normalized==c['readable_candidate']['raw'].replace('X','')
    glyph_review={'source_index':45,'literal_marker':'?',
                  'source_position':{'row_1based':2,'group_in_row_1based':2,'character_in_group_1based':1},
                  'detail_crop':glyph['detail_crop'],'appearance':glyph['appearance'],
                  'conservative_plaintext_position':c['positions'][85],
                  'primary_candidate_coordinate_operations':4,
                  'primary_observed_substitutions':3,'primary_damaged_glyph_fills':1,
                  'explicit_assumption_branches':glyph_branches,
                  'earlier_OCR':{'path':data['prior_attribution_check']['path'],'block':'p107_ocr_block4',
                                 'same_conservative_ciphertext_verified':True,
                                 'same_raw_output_verified':True,'independent_source_claim':False},
                  'readable_mapping':{'case':case_path,'quote':quote,'normalized_display':normalized,
                                      'complete_nonseparator_mapping_verified':True},
                  'limit':glyph['hypothesis_limit']}
    return {'schema':'adfgvx-p107-railway-and-dragoman-certificate-v1','project':data['project'],'authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':3,'printed_source_slots':622,'valid_source_coordinates':620,'modeled_coordinates':622,
                       'plaintext_positions':311,'baseline_fixed_positions':309,'candidate_fixed_positions':310,
                       'known_coordinate_substitutions':11,'source_or_model_erasure_fills':1,
                       'unfilled_printed_erasure_coordinates':1,'source_deletions':0,'published_key_changed':False},
            'records':records,'headers':data['headers'],'source_notes':data['source_notes'],
            'p107_B1_ocr_comparison':ocr,'p107_B2_all_six_completion_witnesses':witnesses,
            'p107_C_damaged_glyph_review':glyph_review,
            'prior_attribution_check':data['prior_attribution_check'],'limits':data['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))


if __name__=='__main__':main()
