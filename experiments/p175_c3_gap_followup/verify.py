#!/usr/bin/env python3
"""Verify the conditional p175 C3 loss geometry, model controls and source edition.

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


def equivalent(a,b):
    if isinstance(a,float) or isinstance(b,float):
        return isinstance(a,(int,float)) and isinstance(b,(int,float)) and abs(a-b)<=1e-12
    if isinstance(a,dict):
        return isinstance(b,dict) and a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
    if isinstance(a,list):
        return isinstance(b,list) and len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
    return a==b


def model_scores(text, values):
    import math
    alphabet=A+'?'
    symbols=[alphabet.index(c) for c in text]
    grams=[]
    for i in range(len(symbols)-3):
        a,b,c,d=symbols[i:i+4]
        grams.append((((a*37+b)*37+c)*37+d,sum(x==36 for x in (a,b,c,d))))
    result={}
    for name,table in values.items():
        known=[table[str(code)] for code,q in grams if not q]
        result[name]={'normalized_marginal_mean':sum(table[str(code)]-q*math.log10(36) for code,q in grams)/len(grams),
                      'marginal_mean':sum(table[str(code)] for code,q in grams)/len(grams),
                      'known_quad_mean':sum(known)/len(known) if known else None,
                      'known_quad_count':len(known)}
    return result


def one_block_screen(observed,key,values,truth=None):
    rows=[]
    for gap in range(len(observed)+1):
        cipher=observed[:gap]+'?'*5+observed[gap:]
        mapping=list(range(gap))+[None]*5+list(range(gap,len(observed)))
        raw=inspect(cipher,key,mapping)
        row={'gap_start':gap,'raw':raw['raw'],'fixed_positions':raw['fixed_positions'],
             'scores':model_scores(raw['raw'],values)}
        if truth is not None:
            expected=encrypt(truth,key['column_rank_order'],key['square'])
            row['truth_known_coordinate_conflicts']=sum(a!='?' and a!=b for a,b in zip(cipher,expected))
        rows.append(row)
    for name in values:
        for metric in ['normalized_marginal_mean','marginal_mean','known_quad_mean']:
            for rank,row in enumerate(sorted(rows,key=lambda r:(-r['scores'][name][metric],r['gap_start'])),1):
                row['scores'][name][metric+'_rank']=rank
    return rows


def verify_screen(data,values):
    controls=[]
    for control in data['fresh_truth_controls']:
        truth=control['newly_composed_nonhistorical_plaintext']
        full=encrypt(truth,data['key']['column_rank_order'],data['key']['square'])
        assert full==control['complete_ciphertext'] and len(truth)==111
        gap=control['true_gap_start'];source=list(full[:gap]+full[gap+5:])
        for mask in control['printed_mask_positions']:source[mask]='?'
        assert ''.join(source)==control['source']
        rows=one_block_screen(control['source'],data['key'],values,truth)
        fits=[r['gap_start'] for r in rows if r['truth_known_coordinate_conflicts']==0]
        assert gap in fits
        rank_report={name:{metric:min(r['scores'][name][metric+'_rank'] for r in rows if r['gap_start'] in fits)
                           for metric in ['normalized_marginal_mean','marginal_mean','known_quad_mean']} for name in values}
        controls.append({'id':control['id'],'truth_compatible_gap_starts':fits,
                         'best_truth_compatible_ranks':rank_report,'all_layouts':rows})
    target=one_block_screen(data['literal_source'].replace('-','?'),data['key'],values)
    result={'schema':'adfgvx-p175-c3-gap-screen-result-v1','authors':data['authors'],
            'inputs_sha256':sha(HERE/'screen_inputs.json'),'target_all_layouts':target,
            'fresh_control_results':controls,'accepted_historical_reading':None}
    assert equivalent(result,json.loads((HERE/'screen_results.json').read_text()))
    return result


def arbitrary_loss_dp(observed,target,missing=5):
    from functools import lru_cache
    assert len(target)==len(observed)+missing
    @lru_cache(None)
    def optimum(i,k):
        if i==len(observed) and k==missing:return 0,1
        options=[];j=i+k
        if i<len(observed):
            cost,count=optimum(i+1,k)
            options.append((cost+int(observed[i]!='?' and observed[i]!=target[j]),count))
        if k<missing:options.append(optimum(i,k+1))
        best=min(cost for cost,count in options)
        return best,sum(count for cost,count in options if cost==best)
    best,count=optimum(0,0);paths=[]
    def walk(i,k,loss):
        if i==len(observed) and k==missing:
            paths.append(loss);return
        cost,n=optimum(i,k);j=i+k
        if i<len(observed) and optimum(i+1,k)[0]+int(observed[i]!='?' and observed[i]!=target[j])==cost:
            walk(i+1,k,loss)
        if k<missing and optimum(i,k+1)[0]==cost:walk(i,k+1,loss+[j])
    assert count<=10000
    walk(0,0,[])
    assert len(paths)==count and len({tuple(p) for p in paths})==count
    table=[{'source_position':i,'insertions_used':k,'minimum_future_substitutions':optimum(i,k)[0],
            'optimal_future_paths':optimum(i,k)[1]} for i in range(len(observed)+1) for k in range(missing+1)]
    return {'minimum_observed_substitutions':best,'optimal_path_count':count,
            'all_optimal_missing_full_positions':sorted(paths),'dynamic_program_states':table}


def variant(literal,loss,template,key,label):
    loss=set(loss);cipher=[];mapping=[];i=0
    for j in range(len(literal)+len(loss)):
        if j in loss:cipher.append('?');mapping.append(None)
        else:cipher.append(literal[i] if literal[i] in C else '?');mapping.append(i);i+=1
    assert i==len(literal)
    cipher=''.join(cipher);raw=inspect(cipher,key,mapping)
    candidate=repair(template,cipher,key,mapping,literal)
    assert len(candidate['erased_coordinate_fills'])==9
    assert sum(e['source_index'] is None for e in candidate['erased_coordinate_fills'])==5
    return {'variant':label,'missing_full_ciphertext_positions':sorted(loss),
            'model_to_source_indices':mapping,'ciphertext':cipher,**raw,'readable_candidate':candidate}


def literal_copy_screen(literal):
    from collections import Counter,defaultdict
    path=ROOT/'experiments/p153_corpus/inputs.json'
    corpus=json.loads(path.read_text())['blocks'];assert len(corpus)==788
    query=literal.replace('-','?');anchors=defaultdict(list);rows=[]
    for i in range(len(query)-9):
        gram=query[i:i+10]
        if set(gram)<=set(C):anchors[gram].append(i)
    for block in corpus:
        source=''.join(block['groups']);source=''.join(c if c in C else '?' for c in source)
        pairs=[]
        for j in range(len(source)-9):
            for i in anchors.get(source[j:j+10],[]):pairs.append([i,j])
        if pairs:
            offsets=Counter(j-i for i,j in pairs)
            rows.append({'target_id':block['id'],'printed_page':block['printed_page'],
                         'exact_ten_coordinate_anchor_hits':len(pairs),
                         'all_anchor_pairs':pairs,'offset_counts':[[a,b] for a,b in sorted(offsets.items())]})
    return {'corpus_path':str(path.relative_to(ROOT)),'corpus_sha256':sha(path),
            'target_blocks':len(corpus),'minimum_anchor_length':10,'all_hits':rows,
            'accepted_cross_page_copy':None,
            'interpretation':'The same-source OCR block matches extensively. The only other block has one10-coordinate match; no independent copy is accepted.'}


def build(pdf=None,book_model=None,radio_model=None):
    from math import comb
    edition=json.loads((HERE/'edition_inputs.json').read_text())
    for dep in edition['dependencies']:assert sha(ROOT/dep['path'])==dep['sha256']
    data=json.loads((HERE/'screen_inputs.json').read_text())
    key=data['key'];literal=data['literal_source'];template=edition['candidate']
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    dep=edition['source_dependency'];source_path=ROOT/dep['path'];assert sha(source_path)==dep['sha256']
    assert sha(ROOT/dep['certificate_path'])==dep['certificate_sha256']
    old=json.loads(source_path.read_text());record=next(r for r in old['contextual_unread_records'] if r['id']=='p175_C3')
    assert literal==''.join(''.join(record['source_rows']).split())
    assert len(literal)==217 and record['advertised_length']==222 and literal.count('-')==4
    for crop in edition['extra_source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:
        verify_crops(pdf,old['source'],old['source_images'],source_path.parent)
        verify_crops(pdf,old['source'],edition['extra_source_images'],HERE)
    queried=json.loads((HERE/'queried_model_cells.json').read_text());assert queried['models']==data['models']
    values=queried['values'];assert set(values)=={'book','radio_book'}
    for name,path in [('book',book_model),('radio_book',radio_model)]:
        if path:
            import array
            model=next(m for m in data['models'] if m['id']==name);assert sha(path)==model['sha256']
            cells=array.array('f');cells.frombytes(path.read_bytes())
            if sys.byteorder!='little':cells.byteswap()
            assert len(cells)==37**4
            for index,value in values[name].items():assert cells[int(index)]==value
    screen=verify_screen(data,values)
    all_costs=[];fits=[]
    for gap in range(218):
        row=variant(literal,range(gap,gap+5),template,key,'one_block_gap'+str(gap))
        count=len(row['readable_candidate']['known_coordinate_substitutions'])
        all_costs.append({'gap_start':gap,'known_coordinate_substitutions':count,'printed_erasure_fills':4,'missing_coordinate_fills':5})
        if count==4:fits.append(row)
    best=min(r['known_coordinate_substitutions'] for r in all_costs)
    starts=[r['missing_full_ciphertext_positions'][0] for r in fits]
    assert best==4 and starts==[95,96,98,99,100,101]
    target=encrypt(template,key['column_rank_order'],key['square'])
    dp=arbitrary_loss_dp(literal.replace('-','?'),target)
    assert dp['minimum_observed_substitutions']==3 and dp['optimal_path_count']==6
    arbitrary=[variant(literal,loss,template,key,'arbitrary_five_loss_'+str(i+1)) for i,loss in enumerate(dp['all_optimal_missing_full_positions'])]
    assert all(len(r['readable_candidate']['known_coordinate_substitutions'])==3 for r in arbitrary)
    assert all(r['readable_candidate']['ciphertext']==target for r in fits+arbitrary)
    boundaries=[0];position=0
    for group in ' '.join(record['source_rows']).split():position+=len(group);boundaries.append(position)
    assert len(boundaries)==45
    group_minima=[gap for gap in starts if gap in boundaries];assert group_minima==[95,100]
    consensus=lambda rows:''.join(cs[0] if len(set(cs))==1 else '?' for cs in zip(*(r['raw'] for r in rows)))
    unconditioned=consensus(screen['target_all_layouts']);assert set(unconditioned)=={'?'}
    primary=fits[0];assert primary['missing_full_ciphertext_positions'][0]==95
    controls={name:{metric:sum(r['best_truth_compatible_ranks'][name][metric]==1 for r in screen['fresh_control_results'])
                       for metric in ['normalized_marginal_mean','marginal_mean','known_quad_mean']} for name in values}
    leaders={name:sorted(screen['target_all_layouts'],key=lambda r:r['scores'][name]['normalized_marginal_mean_rank'])[0]['gap_start'] for name in values}
    assert leaders=={'book':96,'radio_book':96}
    return {'schema':'adfgvx-p175-c3-followup-certificate-v1','project':'ADFGVX Cipher','authors':edition['authors'],
            'edition_inputs_sha256':sha(HERE/'edition_inputs.json'),'screen_results_sha256':sha(HERE/'screen_results.json'),
            'indexing':'All indices are zero-based. A gap start in one-block models is a position before that source coordinate. Arbitrary loss positions are indices in the complete222-coordinate model.',
            'summary':{'physical_records':1,'printed_source_slots':217,'valid_source_coordinates':213,'modeled_coordinates':222,
                       'plaintext_positions':111,'baseline_fixed_positions':102,'candidate_fixed_positions':111,
                       'known_coordinate_substitutions':4,'source_or_model_erasure_fills':9,
                       'printed_erasure_fills':4,'missing_coordinate_fills':5,'source_deletions':0,
                       'published_key_changed':False,'primary_frame':'one_block_gap95',
                       'alternative_arbitrary_five_insertion_minimum_substitutions':3},
            'records':[{'id':'p175_C3','literal_source':literal,'source_slots':217,'valid_coordinates':213,**primary}],
            'one_block_family':{'all218_candidate_conditioned_costs':all_costs,'minimum_known_substitutions':4,
                                'all_six_minimum_variants':fits,'whole_printed_group_boundaries':boundaries,
                                'whole_group_boundary_minimum_gaps':group_minima,
                                'all218_unrepaired_consensus':unconditioned,'all218_unrepaired_common_fixed_count':0,
                                'six_candidate_minimum_unrepaired_consensus':consensus(fits)},
            'arbitrary_five_loss_family':{'possible_full_missing_position_sets':comb(222,5),
                                        'scope':'All insertion placements for the fixed candidate ciphertext and217 observed source slots; no deletion or reorder.',
                                        'recurrence':'F(i,k)=min(F(i+1,k)+observed_mismatch(i,i+k),F(i,k+1)); sum child path counts on every tied minimum. Terminal F(217,5)=0.',
                                        **dp,'all_six_minimum_variants':arbitrary},
            'language_screen_summary':{'models':data['models'],'primary_objective_top_gap':leaders,
                                       'fresh_truth_controls':12,'number_of_top_rank_truth_compatible_controls':controls,
                                       'queried_cells_per_model':{k:len(v) for k,v in values.items()},
                                       'limits':data['ranking_rule_fixed_before_target_screen']},
            'literal_copy_retrieval':literal_copy_screen(literal),
            'prior_attribution':edition['prior_attribution'],'limits':edition['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path)
    p.add_argument('--book-model',type=Path);p.add_argument('--radio-model',type=Path);a=p.parse_args()
    result=build(a.pdf,a.book_model,a.radio_model);path=HERE/'certificates.json'
    if a.verify:assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary'],
                     'arbitrary_loss_optimal_paths':result['arbitrary_five_loss_family']['optimal_path_count'],
                     'truth_controls':result['language_screen_summary']['number_of_top_rank_truth_compatible_controls']},indent=2))


if __name__=='__main__':main()
