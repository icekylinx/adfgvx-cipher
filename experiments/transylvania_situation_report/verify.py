#!/usr/bin/env python3
"""Verify the surviving Transylvania situation report and all declared source-loss models.

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



import collections
import re


def literal_of(source):
    value=''.join(''.join(source['source_rows']).split())
    return value.replace('{INTERFERENCE_1}','').replace('{INTERFERENCE_2}','')


def frame(source,insertions=None,visual=None):
    literal=literal_of(source);base=''.join(c if c in C else '?' for c in literal)
    if visual:
        i,c=visual;base=base[:i]+c+base[i+1:]
    if insertions is None:
        model=source['model'];kind=model['kind']
        if kind=='identity':insertions=[]
        elif kind=='single_plus_five_coordinate_insertions':insertions=[(model['primary_single_gap'],1),(model['primary_five_gap'],5)]
        elif kind=='two_interference_runs':insertions=list(zip(model['literal_boundaries'],model['primary_run_lengths']))
        else:raise ValueError(kind)
    cipher=[];mapping=[]
    for i in range(len(base)+1):
        for before,count in insertions:
            if before==i:cipher.extend('?'*count);mapping.extend([None]*count)
        if i<len(base):cipher.append(base[i]);mapping.append(i)
    return literal,''.join(cipher),mapping


def p4_geometry(source,key,visual=None):
    costs=[];best=None;ties=[]
    for one in source['model']['single_gap_candidates']:
        for five in range(source['source_slots']+1):
            literal,cipher,mapping=frame(source,[(one,1),(five,5)],visual)
            candidate=repair(source['readable_candidate'],cipher,key,mapping,literal)
            cost=len(candidate['known_coordinate_substitutions'])
            costs.append({'single_gap_before_source':one,'five_gap_before_source':five,
                          'observed_coordinate_substitutions':cost,
                          'printed_glyph_fills':sum(e['source_index'] is not None for e in candidate['erased_coordinate_fills']),
                          'missing_coordinate_fills':sum(e['source_index'] is None for e in candidate['erased_coordinate_fills'])})
            if best is None or cost<best:best=cost;ties=[]
            if cost==best:ties.append((one,five))
    variants=[]
    for one,five in ties:
        literal,cipher,mapping=frame(source,[(one,1),(five,5)],visual)
        variants.append({'single_gap_before_source':one,'five_gap_before_source':five,
                         'ciphertext':cipher,'model_to_source_indices':mapping,
                         **inspect(cipher,key,mapping),
                         'readable_candidate':repair(source['readable_candidate'],cipher,key,mapping,literal)})
    return {'scope':'The one-coordinate loss is restricted to the five boundaries within or immediately beside the visibly short AAAV group; the additional five-coordinate loss is tested at every one of the 259 literal boundaries. Selection is conditional on the declared candidate.',
            'trials':len(costs),'minimum_observed_coordinate_substitutions':best,
            'all_costs':costs,'all_minimum_pairs':[list(x) for x in ties],'all_tied_variants':variants,
            'all_repaired_ciphertexts_equal':len({v['readable_candidate']['ciphertext'] for v in variants})==1}


def p5_allocations(source,key):
    model=source['model'];crib=model['conditional_selection_crib'];stencil=masked_encryption('?'*crib['plaintext_start']+crib['text']+'?'*(126-crib['plaintext_start']-len(crib['text'])),key)
    results=[]
    for first in model['all_first_run_lengths']:
        second=model['missing_coordinates_total']-first
        literal,cipher,mapping=frame(source,list(zip(model['literal_boundaries'],[first,second])))
        raw=inspect(cipher,key,mapping)
        contradictions=[{'model_index':i,'source_index':mapping[i],'observed':a,'crib_requires':b}
                        for i,(a,b) in enumerate(zip(cipher,stencil)) if a!='?' and b!='?' and a!=b]
        results.append({'first_interference_missing_coordinates':first,'final_interference_missing_coordinates':second,
                        'ciphertext':cipher,'model_to_source_indices':mapping,**raw,
                        'declared_prefix_crib_observed_coordinate_contradictions':contradictions})
    assert len(results)==38 and {r['fixed_positions'] for r in results}=={85}
    zero=[r['first_interference_missing_coordinates'] for r in results if not r['declared_prefix_crib_observed_coordinate_contradictions']]
    assert zero==[0] and model['primary_run_lengths']==[0,37]
    domains=[''.join(sorted(set().union(*(set(r['positions'][i]['domain']) for r in results)))) for i in range(126)]
    union_raw=''.join(x if len(x)==1 else '?' for x in domains)
    return {'scope':'Both printed INTERFERENCE marker locations are fixed; all 38 nonnegative allocations of 37 missing coordinates are retained. Four printed dashes remain separate occupied source slots.',
            'source_slots':215,'advertised_length':252,'printed_dashes':4,'missing_coordinate_total':37,
            'all_allocation_models':results,'lexical_crib':crib,'zero_observed_error_first_run_lengths':zero,
            'unconditioned_union_domains':domains,'unconditioned_union_raw':union_raw,
            'unconditioned_union_fixed_positions':sum(len(x)==1 for x in domains),
            'selection_is_conditional_not_a_proof_of_interference_duration':True}


def contextual_fragment(source,key):
    literal=literal_of(source);base=''.join(c if c in C else '?' for c in literal)
    assert len(literal)==74 and sum(c in C for c in literal)==71
    bounds=source['model_family']['bounded_total_coordinate_lengths'];trials=[]
    for length in range(bounds['minimum'],bounds['maximum']+1,bounds['step']):
        lost=length-len(base);cipher='?'*lost+base;mapping=[None]*lost+list(range(len(base)))
        raw=inspect(cipher,key,mapping)
        trials.append({'total_coordinates':length,'leading_loss':lost,'raw':raw['raw'],'fixed_positions':raw['fixed_positions']})
    assert len(trials)==214
    return {'id':source['id'],'literal_source':literal,'source_slots':74,'valid_source_coordinates':71,
            'source_annotation':'INTERFERENCE before the first surviving group; no RICHI length is printed.',
            'all_bounded_leading_loss_trials':trials,'selected_model':None,
            'included_in_restoration_or_catalog_counts':False,
            'limit':'The finite 74–500 diagnostic range is not an exhaustive bound on the original length. No historical length or readable body is asserted.'}


def copy_search(inputs):
    settings=inputs['copy_search'];path=ROOT/settings['corpus_path'];assert sha(path)==settings['corpus_sha256']
    blocks=json.loads(path.read_text())['blocks'];assert len(blocks)==788
    width=settings['width'];index=collections.defaultdict(list)
    for b in blocks:
        text=''.join(b['groups'])
        for i in range(len(text)-width+1):
            token=text[i:i+width]
            if set(token)<=set(C):index[token].append((b['id'],i))
    output=[]
    for source in inputs['records']+inputs['contextual_unread_records']:
        text=''.join(''.join(source['source_rows']).split());spans=re.split(r'\{INTERFERENCE_[12]\}',text)
        self_blocks=settings['self_block_exclusions'][source['id']];hits=[];votes=collections.Counter()
        for span_index,span in enumerate(spans):
            for i in range(len(span)-width+1):
                token=span[i:i+width]
                if not set(token)<=set(C):continue
                for block,j in index.get(token,[]):
                    if block in self_blocks:continue
                    hits.append({'query_span_index':span_index,'query_span_offset':i,'target_block':block,
                                 'target_block_offset':j,'exact_window':token})
                    votes[(span_index,block,j-i)]+=1
        output.append({'record':source['id'],'all_nonself_window_matches':hits,
                       'all_offset_vote_counts':[{'query_span_index':a,'target_block':b,'target_minus_query_offset':c,'matching_windows':n}
                                                for (a,b,c),n in sorted(votes.items())]})
    assert sum(len(r['all_nonself_window_matches']) for r in output)==3
    match=next(r for r in output if r['record']=='p129_A8')
    assert {x['target_block'] for x in match['all_nonself_window_matches']}=={'p146_ocr_block4'}
    return {'corpus_path':settings['corpus_path'],'corpus_sha256':settings['corpus_sha256'],'blocks_searched':788,'width':width,
            'rule':settings['rule'],'all_query_results':output,
            'assessment':'Only three overlapping windows (one 12-coordinate stretch) match p146_ocr_block4 from the part 8 query. This is retained as a short incidental lead, not a certified duplicate or recovery of any missing part. The other five queries have no nonself exact 10-coordinate window matches in this bounded OCR corpus.',
            'missing_parts_2_or_3_recovered_by_this_search':False,
            'limit':'No exact window match does not exclude a corrupted, differently keyed, resegmented or untranscribed copy. Unknown parts cannot be queried directly.'}


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());key=inputs['key']
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for crop in inputs['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,inputs['source'],inputs['source_images'],HERE)
    records=[]
    for source in inputs['records']:
        literal,cipher,mapping=frame(source);assert len(literal)==source['source_slots'] and len(cipher)==source['advertised_length']
        raw=inspect(cipher,key,mapping);assert raw['raw']==source['expected_raw']
        candidate=repair(source['readable_candidate'],cipher,key,mapping,literal)
        if '?' in candidate['raw']:
            filled=candidate['ciphertext'].replace('?','A')
            completed=decrypt(filled,key['column_rank_order'],key['square'])
            assert encrypt(completed,key['column_rank_order'],key['square'])==filled
            assert all(c in p['domain'] for c,p in zip(completed,candidate['positions']))
            assert all(a=='?' or a==b for a,b in zip(candidate['ciphertext'],filled))
            candidate['arbitrary_completion_roundtrip_witness']={'ciphertext':filled,'plaintext':completed,
                'is_proposed_historical_reading':False,'is_counted_as_an_editorial_fill':False}
        records.append({'id':source['id'],'key_id':key['id'],'literal_source':literal,'ciphertext':cipher,
                        'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
                        'model_to_source_indices':mapping,**raw,'readable_candidate':candidate})
    assert [len(r['raw']) for r in records]==[98,124,70,132,126]
    assert [r['fixed_positions'] for r in records]==[97,123,70,124,85]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records]==[0,0,3,3,0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records]==[1,1,0,8,21]
    assert [r['readable_candidate']['fixed_positions'] for r in records]==[98,124,70,132,106]
    p4=next(r for r in inputs['records'] if r['id']=='p137_A4');geometry=p4_geometry(p4,key)
    assert geometry['trials']==1295 and geometry['minimum_observed_coordinate_substitutions']==3
    assert geometry['all_minimum_pairs']==p4['model']['all_minimum_pairs']
    visual=inputs['source_visual_alternative'];assert literal_of(p4)[visual['source_index']]==visual['primary']=='A'
    alternate=p4_geometry(p4,key,(visual['source_index'],visual['alternative']))
    assert alternate['minimum_observed_coordinate_substitutions']==2 and alternate['all_minimum_pairs']==geometry['all_minimum_pairs']
    p5=next(r for r in inputs['records'] if r['id']=='p137_A5');allocations=p5_allocations(p5,key)
    # All four word completions are explicit; no observed source glyph changes.
    base=next(r for r in records if r['id']=='p137_A5');template=list(base['raw'])
    for span in p5['word_completion_spans']:
        i=span['start'];word=span['text']
        assert all(a=='?' or a==b for a,b in zip(base['raw'][i:i+len(word)],word))
        template[i:i+len(word)]=word
    assert ''.join(template)==base['readable_candidate']['raw']
    unchanged=[]
    for ident,token in [('p129_A7','VXABHAENGIG'),('p129_A8','1ANOX11226O6XGEHEIMX')]:
        r=next(r for r in records if r['id']==ident);start=r['raw'].index(token);points=r['positions'][start:start+len(token)]
        assert points==r['readable_candidate']['positions'][start:start+len(token)]
        unchanged.append({'record':ident,'field':token,'positions':points})
    inventory=[{'record':r['id'],'variant':v,'raw':reading['raw'],
                'all_numeral_and_JQY_occurrences':[p for p in reading['positions'] if p['raw'] in '0123456789JQY'],
                'all_unresolved_positions':[p for p in reading['positions'] if p['raw']=='?']}
               for r in records for v,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    return {'schema':'adfgvx-transylvania-situation-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
      'input_sha256':sha(HERE/'inputs.json'),'indexing':'All plaintext, model, span and source indices are zero-based; null source indices represent unprinted coordinates.',
      'summary':{'physical_records':5,'additional_unread_contextual_fragments':1,'printed_source_slots':1057,'valid_source_coordinates':1049,
                 'modeled_coordinates':1100,'plaintext_positions':550,'baseline_fixed_positions':499,
                 'candidate_fixed_positions':530,'known_coordinate_substitutions':6,'printed_erasure_fills':7,
                 'printed_erasure_positions_retained':1,'missing_coordinate_fills':24,'missing_coordinates_retained':19,
                 'source_deletions':0,'published_key_changed':False,'historical_message_total_parts':8,
                 'readable_surviving_parts':[1,4,5,7,8],'contextual_unread_part':6,'parts_not_located':[2,3]},
      'records':records,'p137_part4_conditional_geometry':geometry,
      'p137_part4_visual_alternative':{'definition':visual,'exact_geometry_and_repair_costs':alternate},
      'p137_part5_interference_allocations':allocations,
      'contextual_unread_records':[contextual_fragment(r,key) for r in inputs['contextual_unread_records']],
      'unchanged_reference_and_bridge_fields':unchanged,'complete_raw_label_and_domain_inventory':inventory,
      'proposed_cross_page_assembly':inputs['proposed_cross_page_assembly'],'bounded_copy_search':copy_search(inputs),
      'prior_attribution_check':inputs['prior_attribution_check'],
      'limits':['The proposed cross-page message association does not reconcile the conflicting headings or prove a single original transmission event.',
                'Parts 2 and 3 remain absent. The surviving part 6 fragment has no asserted length or plaintext and is excluded from the five restored-record counts.',
                'Part 4 geometry is conditional on the explicit candidate; every tied source mapping and the A/X glyph alternative is preserved.',
                'Part 5 allocation 0/37 is conditional on an error-free 20-character lexical crib; all 38 allocations are retained. The four selected word spans do not complete or silently correct its remaining garbled sentence.',
                'The missing-coordinate counts exclude already printed dashes and invalid glyphs; those are counted separately.',
                'No key label, historical numeral, missing part or unknown reference is supplied by normalization.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    a=p.parse_args();r=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert r==json.loads(target.read_text())
    else:target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))
    print('Part 5 unconditioned union fixed positions:',r['p137_part5_interference_allocations']['unconditioned_union_fixed_positions'])


if __name__=='__main__':main()
