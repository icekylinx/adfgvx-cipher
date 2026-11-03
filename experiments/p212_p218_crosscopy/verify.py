#!/usr/bin/env python3
"""Verify the p212/p218 truncated copy and every borrowed or repaired coordinate.

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



def corpus_search(inputs,queries):
    from collections import defaultdict,Counter
    spec=inputs['corpus_search'];path=ROOT/spec['source_path']
    assert sha(path)==spec['source_sha256']
    blocks=json.loads(path.read_text())['blocks'];width=spec['window'];index=defaultdict(list)
    for block in blocks:
        source=''.join(block['groups'])
        for at in range(len(source)-width+1):
            token=source[at:at+width]
            if set(token)<=set(C):index[token].append((block['id'],at))
    results=[]
    for query in spec['queries']:
        literal=queries[query['record']];excluded=set(query['excluded_ocr_blocks']);votes=Counter()
        for at in range(len(literal)-width+1):
            for block,offset in index.get(literal[at:at+width],[]):
                if block not in excluded:votes[(block,offset-at)]+=1
        rows=[{'block':block,'candidate_offset_minus_query_offset':offset,'matching_ten_coordinate_windows':count}
              for (block,offset),count in sorted(votes.items(),key=lambda r:(-r[1],r[0]))]
        results.append({'query':query['record'],'query_coordinates':len(literal),
                        'excluded_self_blocks':sorted(excluded),'all_nonzero_matches':rows})
    assert len(blocks)==788
    assert results[0]['all_nonzero_matches'][0]=={'block':'p218_ocr_block2','candidate_offset_minus_query_offset':0,'matching_ten_coordinate_windows':121}
    assert results[1]['all_nonzero_matches']==[]
    return {'blocks_examined':len(blocks),'window':width,'scope':spec,'results':results,
            'p212_A4_has_an_asserted_reading':False}


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for p,h in inputs['dependencies'].items():assert sha(ROOT/p)==h
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    source=inputs['records'][0];assert source['id']=='p212_A2'
    literal=''.join(''.join(source['source_rows']).split());assert len(literal)==160 and set(literal)<=set(C)
    earlier=json.loads((ROOT/'experiments/medical_return_transports/inputs.json').read_text())
    assert next(r for r in earlier['contextual_unread_records'] if r['id']=='p212_A2')['source_rows']==source['source_rows']
    witness=inputs['contextual_witness_records'][0];assert witness['already_catalogued'] and not witness['counted_as_new']
    prior=json.loads((ROOT/'experiments/corpus_readings/selected_sources.json').read_text())
    assert next(r for r in prior['messages'] if r['id']=='p218_A2')==witness['source_record_snapshot']
    wl=''.join(''.join(witness['source_record_snapshot']['source_rows']).split())
    assert wl==witness['literal_source'] and len(wl)==284
    wc=''.join(c if c in C else '?' for c in wl)
    wr=inspect(wc,key,list(range(284)));assert wr['raw']==witness['expected_raw']
    differences=[{'source_index':i,'p212':a,'p218':b} for i,(a,b) in enumerate(zip(literal,wl)) if a!=b]
    assert differences==inputs['copy_assumption']['preserved_disagreements']
    assert len(differences)==3 and sum(a==b for a,b in zip(literal,wl))==157
    scores=[]
    for gap in range(161):
        model=literal[:gap]+'?'*124+literal[gap:]
        mismatch=[i for i,(a,b) in enumerate(zip(model,wc)) if a in C and b in C and a!=b]
        scores.append({'gap_before_source_index':gap,'observed_coordinate_mismatches':len(mismatch),
                       'mismatching_model_indices':mismatch})
    best=min(r['observed_coordinate_mismatches'] for r in scores)
    winners=[r['gap_before_source_index'] for r in scores if r['observed_coordinate_mismatches']==best]
    assert best==2 and winners==[160]
    mapping=list(range(160))+[None]*124;baseline=literal+'?'*124
    raw=inspect(baseline,key,mapping);assert raw['raw']==source['expected_raw'] and raw['fixed_positions']==30
    borrowed=wl[160:];assert len(borrowed)==124 and set(borrowed)<=set(C)
    pure=literal+borrowed;pure_read=inspect(pure,key,mapping)
    assert pure_read['fixed_positions']==142
    assert encrypt(pure_read['raw'],key['column_rank_order'],key['square'])==pure
    # The conflicting source at103 uses the unchanged p218 witness. The two
    # other mismatches use observed p212 coordinates to supply the better copy.
    consensus=pure[:103]+wl[103]+pure[104:]
    consensus_read=inspect(consensus,key,mapping)
    assert consensus_read['raw']=='DIEVORDEMKRIEGZURUSZLANDGEHOERTENXHABENXSOBALDDIEALLIIERTENUNTERBERUECKSICHTIGUNGDERJNNERENLAGEDIESERGEBIETEDENAUGENBLICKFUERGEKOMMENERACHTENX'
    assert pure_read['raw'][58]=='7' and consensus_read['raw'][58]=='N'
    assert consensus_read['raw'][70]=='K' and consensus_read['raw'][109]=='E'
    assert wr['raw'][58]=='N' and wr['raw'][70]=='?' and wr['raw'][109]=='P'
    candidate=repair(source['readable_candidate'],baseline,key,mapping,literal)
    assert len(candidate['known_coordinate_substitutions'])==1
    assert candidate['known_coordinate_substitutions'][0]['source_index']==103
    assert len(candidate['erased_coordinate_fills'])==124
    assert all(e['source_index'] is None for e in candidate['erased_coordinate_fills'])
    extra=[{'model_index':i,'p218_source_index':i,'p218_literal':a,'candidate':b}
           for i,(a,b) in enumerate(zip(consensus,candidate['ciphertext'])) if a!=b]
    assert extra==[{'model_index':217,'p218_source_index':217,'p218_literal':'X','candidate':'F'}]
    assert source['readable_candidate']==consensus_read['raw'].replace('DERJNNEREN','DERINNEREN')
    assert 'RUSZLAND' in source['readable_candidate']
    origins=[]
    for i in range(284):
        origins.append({'model_index':i,'p212_source_index':i if i<160 else None,
                        'p218_source_index':i,'p212_observed':literal[i] if i<160 else None,
                        'p218_observed':wl[i],'pure_copy_coordinate':pure[i],
                        'consensus_coordinate':consensus[i],'final_candidate_coordinate':candidate['ciphertext'][i]})
    borrowed_origins=origins[160:]
    assert sum(x['final_candidate_coordinate']==x['p218_observed'] for x in borrowed_origins)==123
    assert all(x['pure_copy_coordinate']==x['p218_observed'] for x in borrowed_origins)
    contributions={'both_coordinates_observed_in_p212':0,'one_coordinate_from_each_copy':0,'both_coordinates_borrowed_from_p218':0}
    for p in raw['positions']:
        known=sum(i is not None for i in p['source_indices'])
        contributions[['both_coordinates_borrowed_from_p218','one_coordinate_from_each_copy','both_coordinates_observed_in_p212'][known]]+=1
    assert contributions=={'both_coordinates_observed_in_p212':30,'one_coordinate_from_each_copy':100,'both_coordinates_borrowed_from_p218':12}
    complementary=[{'plaintext_index':i,'p212_observed_frame':raw['positions'][i],
                    'p218_raw':wr['positions'][i],'pure_copy':pure_read['positions'][i],
                    'consensus':consensus_read['positions'][i]}
                   for i in [58,70,109]]
    context=inputs['contextual_unread_records'][0]
    assert context['id']=='p212_A4' and not context['counted_as_new'] and not context['reading_asserted']
    a4=''.join(''.join(context['source_rows']).split());assert len(a4)==197
    assert next(r for r in earlier['contextual_unread_records'] if r['id']=='p212_A4')==context['source_record_snapshot']
    search=corpus_search(inputs,{'p212_A2':literal,'p212_A4':a4})
    return {'schema':'adfgvx-p212-p218-crosscopy-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':1,'previously_catalogued_witnesses_not_counted':1,
                       'contextual_unread_records_not_counted':1,'printed_source_slots':160,
                       'valid_source_coordinates':160,'modeled_coordinates':284,'plaintext_positions':142,
                       'baseline_fixed_positions':30,'pure_crosscopy_fixed_positions':142,'candidate_fixed_positions':142,
                       'known_coordinate_substitutions':1,'printed_erasure_fills':0,'missing_coordinate_fills':124,
                       'final_missing_coordinate_fills_equal_to_literal_witness':123,
                       'additional_ordinary_word_change_to_one_borrowed_witness_coordinate':1,
                       'source_deletions':0,'published_key_changed':False},
            'records':[{'id':'p212_A2','literal_source':literal,'ciphertext':baseline,'source_slots':160,
                        'valid_source_coordinates':160,'model_to_source_indices':mapping,**raw,
                        'readable_candidate':candidate}],
            'contextual_witness_records':[{'id':'p218_A2','already_catalogued':True,'counted_as_new':False,
                                            'literal_source':wl,'ciphertext':wc,**wr}],
            'contextual_unread_records':[{'id':'p212_A4','literal_source':a4,'reading_asserted':False,'counted_as_new':False}],
            'exact_prefix_comparison':{'observed_prefix_positions':160,'identical_glyphs':157,
                                       'two_conflicting_valid_coordinate_pairs':2,'p212_supplies_one_p218_erasure':True,
                                       'all_disagreements':differences},
            'gap_placement_screen':{'model':'One contiguous 124-coordinate loss compared against the independent p218 coordinate witness.',
                                    'all161_scores':scores,'minimum_disagreements':best,'all_best_gaps':winners,
                                    'uniqueness_scope':'Unique tail placement within this single-gap comparison; it does not prove identical complete historical messages.'},
            'pure_crosscopy_layer':{'ciphertext':pure,**pure_read,'observed_p212_coordinates_changed':0,
                                    'missing_coordinates_copied_exactly_from_p218':124},
            'complementary_consensus_layer':{'ciphertext':consensus,**consensus_read,
                                             'p212_coordinate103_replaced_by_p218':True,
                                             'common_JNNEREN_garble_retained':True},
            'remaining_ordinary_word_candidate_change':extra,
            'coordinate_origin_ledger':origins,'plaintext_coordinate_contributions':contributions,
            'complementary_plaintext_witnesses':complementary,'bounded_whole_corpus_comparison':search,
            'copy_assumption_and_date_conflict':inputs['copy_assumption'],'prior_attribution':inputs['prior_attribution'],
            'limits':['The missing tail is borrowed from a separate printed witness under a same-copy assumption, not recovered from the 160 p212 coordinates alone.',
                      'The 22 November versus 25 November date/heading conflict is preserved, and the record is not joined to the surrounding medical text.',
                      'The previously catalogued p218 body is not counted again as a new unique message or a new physical record.',
                      'The fully observed p212 source supplies 30 complete plaintext pairs; 100 use one coordinate from each copy and 12 use two borrowed coordinates.',
                      'No match for p212 A4 in the bounded exact-window screen does not exclude other keys or heavier source/OCR corruption.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))


if __name__=='__main__':main()
