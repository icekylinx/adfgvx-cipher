#!/usr/bin/env python3
"""Reproduce the p111/p112 source, copy and conditional loss editions.

Prepared by icekylinx and GPT-6 Astra Pro. The optional language screen is
separate from the standard-library source/geometry certificate.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt,plaintext_domains
CO='ADFGVX'
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation(n,ranks):
    width=len(ranks)
    heights=[(n-i+width-1)//width for i in range(width)]
    offsets=[sum(heights[j]for j in range(width)if ranks[j]<ranks[i])for i in range(width)]
    result=[offsets[i%width]+i//width for i in range(n)]
    assert sorted(result)==list(range(n))
    return result


def encode(text,key):
    middle=''.join('??'if c=='?'else CO[key['square'].index(c)//6]+CO[key['square'].index(c)%6]for c in text)
    out=['?']*len(middle)
    for c,i in zip(middle,permutation(len(middle),key['column_rank_order'])):
        out[i]=c
    return ''.join(out)


def inspect(source,key):
    assert len(source)%2==0
    p=permutation(len(source),key['column_rank_order'])
    middle=''.join(source[i]for i in p)
    domains=[]
    for a,b in zip(middle[::2],middle[1::2]):
        domains.append(''.join(sorted(key['square'][6*r+c]for r in range(6)for c in range(6)
                                     if a in ('?',CO[r])and b in ('?',CO[c]))))
    raw=''.join(d if len(d)==1 else'?'for d in domains)
    assert raw==decrypt(source,key['column_rank_order'],key['square'])
    assert domains==plaintext_domains(source,key['column_rank_order'],key['square'])
    return {'plaintext':raw,'domains':domains,'fixed_positions':sum(len(d)==1 for d in domains),
            'plaintext_positions':len(domains),'interim':middle,'interim_source_indices':p}


def local_maps():
    """All declared short-group + two five-coordinate-block models."""
    for g1 in range(5,10):
        for g2 in range(19,24):
            base=list(range(g1))+[None]+list(range(g1,g2))+[None]+list(range(g2,110))
            assert len(base)==112
            for a in range(113):
                for b in range(a,113):
                    yield (g1,g2,a,b),base[:a]+[None]*5+base[a:b]+[None]*5+base[b:]


def arbitrary_loss(source,target,missing,retain_limit=100):
    assert len(target)==len(source)+missing
    @lru_cache(None)
    def dp(i,k):
        if i==len(source)and k==missing:
            return 0,1
        options=[];j=i+k
        if i<len(source):
            cost,count=dp(i+1,k)
            options.append((cost+int(source[i]!='?'and target[j]!='?'and source[i]!=target[j]),count))
        if k<missing:
            options.append(dp(i,k+1))
        best=min(cost for cost,count in options)
        return best,sum(count for cost,count in options if cost==best)
    cost,count=dp(0,0)
    layouts=[]
    def walk(i,k,inserted):
        if len(layouts)>=retain_limit:
            return
        if i==len(source)and k==missing:
            layouts.append(inserted);return
        wanted=dp(i,k)[0];j=i+k
        if i<len(source):
            charge=int(source[i]!='?'and target[j]!='?'and source[i]!=target[j])
            if dp(i+1,k)[0]+charge==wanted:
                walk(i+1,k,inserted)
        if k<missing and dp(i,k+1)[0]==wanted:
            walk(i,k+1,inserted+[j])
    walk(0,0,[])
    assert len(layouts)==min(retain_limit,count)
    assert len(set(tuple(x)for x in layouts))==len(layouts)
    for gaps in layouts:
        values=iter(source);frame=''.join('?'if j in gaps else next(values)for j in range(len(target)))
        assert sum(a!='?'and b!='?'and a!=b for a,b in zip(frame,target))==cost
    return {'minimum_observed_substitutions':cost,'optimal_layout_count':count,
            'all_optimal_inserted_model_indices':layouts,'all_optima_retained':count<=retain_limit,
            'visited_dp_states':dp.cache_info().currsize}


def loss_controls():
    examples=[('ADFG','AADFGX',2),('A?DG','AXDFGX',2),('ADAD','ADADAD',2),
              ('GVXA','GAXVXA',2),('D','AFD',2),('??','ADFG',2)]
    result=[]
    for source,target,n in examples:
        rows=[]
        for gaps in itertools.combinations(range(len(target)),n):
            observed=''.join(c for i,c in enumerate(target)if i not in gaps)
            rows.append((sum(a!='?'and a!=b for a,b in zip(source,observed)),list(gaps)))
        optimum=min(x[0]for x in rows);best=[x[1]for x in rows if x[0]==optimum]
        actual=arbitrary_loss(source,target,n)
        assert actual['minimum_observed_substitutions']==optimum
        assert sorted(actual['all_optimal_inserted_model_indices'])==sorted(best)
        result.append({'source':source,'target':target,'missing':n,'enumerated_layouts':len(rows),
                       'minimum':optimum,'all_minima':best})
    return result


def geometry_audit(record,key):
    source=record['analysis_source'];target=encode(record['editorial_text'],key)
    histogram=Counter();minimum=None;winners=[];evaluated=0;distinct_maps=set()
    for params,mapping in local_maps():
        distinct_maps.add(bytes(255 if i is None else i for i in mapping))
        cost=sum(i is not None and target[j]!='?'and source[i]!=target[j]for j,i in enumerate(mapping))
        histogram[cost]+=1;evaluated+=1
        if minimum is None or cost<minimum:
            minimum=cost;winners=[]
        if cost==minimum:
            winners.append({'parameters':list(params),'inserted_model_indices':[j for j,i in enumerate(mapping)if i is None]})
    assert evaluated==25*113*114//2==161025
    assert len(distinct_maps)==155400
    arbitrary=arbitrary_loss(source,target,12)
    assert minimum==1 and arbitrary['minimum_observed_substitutions']==1
    assert arbitrary['optimal_layout_count']==8
    return {'source_slots':110,'advertised_and_modeled_slots':122,
            'fixed_candidate_template':record['editorial_text'],
            'template_unknowns_are_wildcards':True,
            'bounded_family':{'description':'One coordinate inside each visible four-symbol group plus two arbitrary five-coordinate blocks in the112-slot temporary transmitted-coordinate frame after the two short-group insertions. The two block positions may coincide.',
                              'completed_parameter_configurations':evaluated,'distinct_source_origin_layouts':len(distinct_maps),'duplicate_parameter_configurations':evaluated-len(distinct_maps),'cost_histogram':{str(k):v for k,v in sorted(histogram.items())},
                              'minimum_observed_substitutions':minimum,'all_minimum_layouts':winners},
            'arbitrary_twelve_missing_coordinates':arbitrary,
            'independent_small_bruteforce_controls':loss_controls(),
            'limit':'Retrospective alignment to one editorial template proves compatibility and its minimum cost, not unique wording or a historical loss mechanism.'}


def copy_audit(records,inputs):
    byid={r['id']:r for r in records};src={r['id']:r for r in inputs['records']}
    a,b=src['p111_A1'],src['p112_A1'];sa,sb=a['analysis_source'],b['analysis_source']
    assert len(sa)==len(sb)==202
    differences=[];masked=[]
    for i,(x,y)in enumerate(zip(sa,sb)):
        if x!=y:
            row={'source_index':i,'p111':x,'p112':y}
            (masked if '?'in(x,y)else differences).append(row)
    assert len(differences)==2 and len(masked)==17
    key=next(k for k in inputs['keys']if k['id']=='Nov1-3')
    common=[]
    for choices in itertools.product(*[(d['p111'],d['p112'])for d in differences]):
        cipher=[y if x=='?'else x for x,y in zip(sa,sb)]
        for d,value in zip(differences,choices):cipher[d['source_index']]=value
        cipher=''.join(cipher);costs=[sum(x!='?'and x!=y for x,y in zip(source,cipher))for source in(sa,sb)]
        assert sum(costs)==2
        common.append({'conflict_choices':list(choices),'plaintext':inspect(cipher,key)['plaintext'],
                       'ciphertext':cipher,'observed_substitution_costs':costs})
    assert a['editorial_text']==b['editorial_text']
    assert any(r['plaintext']==a['editorial_text']for r in common)
    fills=[]
    for ident,donor in [('p111_A1','p112_A1'),('p112_A1','p111_A1')]:
        for item in byid[ident]['source_mask_fills']:
            i=item['source_index'];assert src[donor]['analysis_source'][i]==item['after']
            fills.append({'recipient':ident,'donor':donor,'source_index':i,'value':item['after']})
    return {'literal_records':['p111_A1','p112_A1'],'same_valid_coordinates':sum(x==y and x!='?'for x,y in zip(sa,sb)),
            'single_source_erasure_differences':masked,'observed_coordinate_conflicts':differences,
            'copy_supported_coordinate_fills':fills,'minimum_combined_observed_substitutions':2,
            'all_minimum_common_streams':common,'selected_text':a['editorial_text'],
            'limit':'The two observed conflicts do not disappear by copying. Selecting DONAU and UJVIDEK is an explicit editorial choice; the second occurrence of UJVIDEK is also unchanged within both messages.'}



def alternatives_audit(inputs):
    data=json.loads((HERE/'editorial_alternatives.json').read_text())
    record=next(r for r in inputs['records']if r['id']==data['source_id'])
    key=next(k for k in inputs['keys']if k['id']==record['key_id'])
    source=record['analysis_source'];results=[]
    for item in data['alternatives']:
        stencil=encode(item['plaintext'],key)
        witness=''.join(a if b=='?'else b for a,b in zip(source,stencil))
        assert inspect(witness,key)['plaintext']==item['plaintext']
        changes=[[i,a,b]for i,(a,b)in enumerate(zip(source,witness))if a!=b]
        cost={'known_coordinate_substitutions':sum(a!='?'for i,a,b in changes),
              'source_mask_fills':sum(a=='?'for i,a,b in changes),'missing_coordinate_fills':0}
        assert changes==item['expected_model_changes']and cost==item['expected_cost']
        results.append({'id':item['id'],'plaintext':item['plaintext'],'source_changes':changes,'cost':cost})
    assert results[0]['plaintext']==record['editorial_text']
    assert results[0]['cost']['known_coordinate_substitutions']==6
    assert results[1]['cost']['known_coordinate_substitutions']==10
    assert all(r['cost']['source_mask_fills']==18 for r in results)
    return {'inputs_sha256':sha(HERE/'editorial_alternatives.json'),'variants':results,
            'limit':'Lower source-edit cost favors one candidate within this comparison; it does not prove unique wording.'}


def display_audit(inputs):
    import re
    data=json.loads((HERE/'readable_mapping.json').read_text());records={r['id']:r for r in inputs['records']};results=[]
    for item in data['readings']:
        path=(ROOT/item['case_path']).resolve();assert path.is_relative_to(ROOT)
        text=path.read_text();section=text.split(item['section_heading']+'\n',1)[1].split('\n## ',1)[0]
        lines=section.splitlines();start=next(i for i,l in enumerate(lines)if l.startswith('> '));quote=[]
        while start<len(lines)and lines[start].startswith('>'):
            quote.append(lines[start].removeprefix('>').lstrip());start+=1
        readable=' '.join(quote);assert readable==item['readable_german']
        punctuation=item['grammatical_question_mark_offsets']
        assert len(punctuation)==len(set(punctuation))and all(readable[i]=='?'for i in punctuation)
        assert (item['id']=='p112_B'and len(punctuation)==2)or not punctuation
        preserved=''.join(c for i,c in enumerate(readable)if i not in punctuation)
        folded=preserved.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS')
        folded=''.join(c for c in folded if c in ALPHABET+'?')
        expected=records[item['id']]['editorial_text'].replace('X','')
        assert folded==expected,(item['id'],folded,expected)
        assert preserved.count('?')==records[item['id']]['editorial_text'].count('?')
        results.append({'id':item['id'],'case_path':item['case_path'],'readable_german':readable,
                        'nonseparator_labels_matched':len(expected),'unknown_positions_preserved':preserved.count('?'),'grammatical_question_marks':len(punctuation)})
    assert set(records)=={r['id']for r in results}
    return {'mapping_sha256':sha(HERE/'readable_mapping.json'),'records':results,
            'nonseparator_labels_matched':sum(r['nonseparator_labels_matched']for r in results),
            'limits':data['rules']}



def retrieval_audit(inputs):
    data=json.loads((HERE/'literal_copy_retrieval.json').read_text())
    corpus_path=ROOT/'experiments/p153_corpus/inputs.json'
    assert data['source_corpus_inputs_sha256']==sha(corpus_path)
    assert data['query_source_inputs_sha256']==sha(HERE/'inputs.json')
    corpus=json.loads(corpus_path.read_text())['blocks'];queries={};comparisons=0
    for record in inputs['records']:
        if not record['id'].startswith('p112_'):continue
        source=record['literal_source']
        grams={source[i:i+10]for i in range(len(source)-9)if set(source[i:i+10])<=set(CO)}
        matches=[]
        for block in corpus:
            text=''.join(block['groups']);other={text[i:i+10]for i in range(len(text)-9)}
            common=grams&other;comparisons+=1
            if len(common)>=8:
                matches.append({'shared_distinct_10mers':len(common),'id':block['id'],'printed_page':block['printed_page']})
        matches.sort(key=lambda x:-x['shared_distinct_10mers']);queries[record['id']]=matches
    assert queries==data['queries']and len(corpus)==data['tested_blocks']==788
    assert comparisons==data['actual_pair_comparisons']==4728
    return {'report_sha256':sha(HERE/'literal_copy_retrieval.json'),'source_corpus_sha256':sha(corpus_path),
            'actual_pair_comparisons':comparisons,'query_count':len(queries),'scope':data['scope']}


def recorded_screen_audit(inputs):
    report=json.loads((HERE/'language_screen.json').read_text())
    screen=json.loads((HERE/'screen_inputs.json').read_text())
    assert report['source_inputs_sha256']==sha(HERE/'inputs.json')
    assert report['screen_inputs_sha256']==sha(HERE/'screen_inputs.json')
    assert report['model_sha256']==screen['model_sha256']
    key=next(k for k in inputs['keys']if k['id']=='Nov4-6')
    record=next(r for r in inputs['records']if r['id']=='p112_C')
    examples=[(record['analysis_source'],report['target'])]
    controls=report['fresh_truth_controls']
    for expected,actual in zip(screen['fresh_truth_controls'],controls):
        assert expected['id']==actual['id']and expected['newly_composed_nonhistorical_plaintext']==actual['plaintext']
        assert encode(actual['plaintext'],key)==actual['complete_ciphertext']
        g1,g2,a,b=actual['true_parameters'];source=actual['source_after_declared_losses']
        base=source[:g1]+'?'+source[g1:g2]+'?'+source[g2:]
        frame=base[:a]+'?'*5+base[a:b]+'?'*5+base[b:]
        assert all(x=='?'or x==y for x,y in zip(frame,actual['complete_ciphertext']))
        assert any(x['parameters']==actual['true_parameters']for x in actual['truth_compatible_layouts'])
        examples.append((source,actual))
    checked=0
    for source,screen_result in examples:
        assert screen_result['actual_parameter_configurations']==161025
        for row in screen_result['top20']:
            g1,g2,a,b=row['parameters'];base=source[:g1]+'?'+source[g1:g2]+'?'+source[g2:]
            frame=base[:a]+'?'*5+base[a:b]+'?'*5+base[b:];raw=inspect(frame,key)
            assert raw['plaintext']==row['raw']and raw['fixed_positions']==row['fixed_positions'];checked+=1
    assert len(controls)==4 and report['total_122_slot_configuration_evaluations']==805125
    assert [c['best_truth_compatible_rank']for c in controls]==[1,5,1,27]
    for row in report['short_group_only_112_slot_diagnostics']:
        k=next(k for k in inputs['keys']if k['id']==row['key']);g1,g2=row['short_group_gaps'];source=record['analysis_source']
        frame=source[:g1]+'?'+source[g1:g2]+'?'+source[g2:]
        assert inspect(frame,k)['plaintext']==row['raw']
    assert len(report['short_group_only_112_slot_diagnostics'])==50
    return {'report_sha256':sha(HERE/'language_screen.json'),'top_candidate_frames_checked':checked,
            'control_ciphertexts_checked':len(controls),'configuration_evaluations_recorded':805125,
            'short_group_only_frames_checked':50,'model_scores_recomputed_by_default':False,
            'optional_score_check':'screen_geometry.py --verify --book-model PATH recomputes the entire frozen-model ranking, not just these retained candidates.'}


def build(pdf=None):
    inputs=json.loads((HERE/'inputs.json').read_text());keys={k['id']:k for k in inputs['keys']}
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for name,key in keys.items():
        assert key['square']==published[name]['square']and key['column_rank_order']==published[name]['column_rank_order']
        assert set(key['square'])==set(ALPHABET)and len(key['square'])==36
    doc=None
    if pdf:
        import fitz
        assert sha(pdf)==inputs['source']['pdf_sha256']
        doc=fitz.open(pdf)
    for im in inputs['source']['images']:
        assert sha(HERE/im['path'])==im['sha256']
        if doc:
            if im.get('fresh_render_cache'):fitz.TOOLS.store_shrink(100)
            pix=doc[im['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(im['scale'],im['scale']),clip=fitz.Rect(*im['clip_points']))
            assert (pix.width,pix.height)==(im['width'],im['height'])
            assert hashlib.sha256(pix.samples).hexdigest()==im['pixel_sha256']
    result=[]
    for record in inputs['records']:
        key=keys[record['key_id']];literal=''.join(''.join(record['rows']).split())
        assert literal==record['literal_source']
        source=''.join(c if c in CO else'?'for c in literal)
        assert source==record['analysis_source']
        mapping=record['model_to_source_indices']
        assert [i for i in mapping if i is not None]==list(range(len(source)))
        frame=''.join('?'if i is None else source[i]for i in mapping)
        assert len(frame)==record['advertised_length']
        raw=inspect(frame,key);assert raw['plaintext']==record['expected_raw']
        template=record['editorial_text'];assert len(template)==raw['plaintext_positions']
        stencil=encode(template,key)
        witness=''.join(x if y=='?'else y for x,y in zip(frame,stencil))
        edited=inspect(witness,key);assert edited['plaintext']==template
        substitutions=[];fills=[];missing=[]
        for j,(a,b)in enumerate(zip(frame,witness)):
            if a==b:continue
            i=mapping[j];p=raw['interim_source_indices'].index(j)//2
            item={'model_index':j,'source_index':i,'printed_glyph':literal[i]if i is not None else None,
                  'before':a,'after':b,'plaintext_index':p,'raw_label':raw['plaintext'][p],'edited_label':template[p]}
            (missing if i is None else fills if a=='?'else substitutions).append(item)
        cost={'known_coordinate_substitutions':len(substitutions),'source_mask_fills':len(fills),'missing_coordinate_fills':len(missing)}
        assert cost==record['expected_cost']
        assert sorted([[e['model_index'],e['before'],e['after']]for e in substitutions+fills+missing])==record['expected_model_changes']
        complete=''.join(d[0]for d in edited['domains']);full=encode(complete,key)
        assert full==encrypt(complete,key['column_rank_order'],key['square'])
        assert all(a=='?'or a==b for a,b in zip(witness,full))
        numeral_changes=[{'plaintext_index':i,'raw_label':a,'edited_label':b}for i,(a,b)in enumerate(zip(raw['plaintext'],template))if a.isdigit()and a!=b]
        assert numeral_changes==record['explicit_numeral_word_repairs']
        result.append({'id':record['id'],'key_id':record['key_id'],'source_slots':len(source),'valid_source_coordinates':len(source)-source.count('?'),
                       'model_slots':len(frame),'missing_model_coordinates':mapping.count(None),'raw_reading':raw,
                       'edited_reading':edited,'source_to_model_witness':mapping,'reencrypted_model_witness':witness,
                       'known_coordinate_substitutions':substitutions,'source_mask_fills':fills,'missing_coordinate_fills':missing,
                       'cost':cost,'arbitrary_complete_plaintext_witness':complete,'arbitrary_complete_ciphertext_witness':full,
                       'unknown_edited_positions':[{'plaintext_index':i,'domain':d}for i,d in enumerate(edited['domains'])if len(d)>1],
                       'explicit_numeral_word_repairs':numeral_changes})
    summary={'physical_records':len(result),'source_slots':sum(r['source_slots']for r in result),
             'valid_source_coordinates':sum(r['valid_source_coordinates']for r in result),
             'analysis_frame_slots':sum(r['model_slots']for r in result),
             'plaintext_positions':sum(r['raw_reading']['plaintext_positions']for r in result),
             'raw_fixed_positions':sum(r['raw_reading']['fixed_positions']for r in result),
             'edited_fixed_positions':sum(r['edited_reading']['fixed_positions']for r in result),
             **{k:sum(r['cost'][k]for r in result)for k in ['known_coordinate_substitutions','source_mask_fills','missing_coordinate_fills']},
             'inserted_model_coordinates':sum(r['missing_model_coordinates']for r in result),'source_exclusions':0,'published_key_changes':0}
    assert summary==inputs['expected_totals']
    c=next(r for r in inputs['records']if r['id']=='p112_C')
    return {'schema':'adfgvx-nov3-evening-nov4-radio-certificate-v1','authors':inputs['authors'],
            'inputs_sha256':sha(HERE/'inputs.json'),'summary':summary,'records':result,
            'copy_audit':copy_audit(result,inputs),'conditional_C_geometry':geometry_audit(c,keys[c['key_id']]),
            'editorial_alternatives':alternatives_audit(inputs),'readable_display_audit':display_audit(inputs),
            'literal_copy_retrieval_audit':retrieval_audit(inputs),'recorded_language_screen_audit':recorded_screen_audit(inputs),
            'limits':inputs['limits']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true');parser.add_argument('--pdf',type=Path)
    args=parser.parse_args();result=build(args.pdf);path=HERE/'certificates.json'
    if args.verify:
        assert result==json.loads(path.read_text())
    else:path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verified':args.verify,'source_pixels_checked':bool(args.pdf),**result['summary'],
                      'bounded_C_parameter_configurations':result['conditional_C_geometry']['bounded_family']['completed_parameter_configurations'],
                      'bounded_C_optima':len(result['conditional_C_geometry']['bounded_family']['all_minimum_layouts'])},indent=2))

if __name__=='__main__':main()
