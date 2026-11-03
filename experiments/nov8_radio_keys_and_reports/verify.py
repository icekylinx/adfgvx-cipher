#!/usr/bin/env python3
"""Check Nov8 source frames, coupled key labels and separately costed edits.

Prepared by icekylinx and GPT-6 Astra Pro. No published key is completed or
changed; both 5/6 square completions are compatibility witnesses only.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt,plaintext_domains
CO='ADFGVX';LETTERS='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def permutation(n,ranks):
    w=len(ranks);heights=[(n-i+w-1)//w for i in range(w)]
    starts=[sum(heights[j]for j in range(w)if ranks[j]<ranks[i])for i in range(w)]
    result=[starts[i%w]+i//w for i in range(n)];assert sorted(result)==list(range(n));return result

def encode(text,key):
    sq=key['square'];middle=''.join('??'if c=='?'else CO[sq.index(c)//6]+CO[sq.index(c)%6]for c in text)
    result=['?']*len(middle)
    for c,i in zip(middle,permutation(len(middle),key['column_rank_order'])):result[i]=c
    return ''.join(result)

def inspect(cipher,key):
    p=permutation(len(cipher),key['column_rank_order']);middle=''.join(cipher[i]for i in p);unused=set(LETTERS)-set(key['square']);domains=[]
    for a,b in zip(middle[::2],middle[1::2]):
        domain=set()
        for r in range(6):
            for c in range(6):
                if a in ('?',CO[r])and b in ('?',CO[c]):
                    value=key['square'][6*r+c];domain.update(unused if value=='?'else value)
        domains.append(''.join(sorted(domain)))
    raw=''.join(d if len(d)==1 else'?'for d in domains)
    if len(cipher)%2==0:
        assert raw==decrypt(cipher,key['column_rank_order'],key['square'])
        assert domains==plaintext_domains(cipher,key['column_rank_order'],key['square'])
    return {'plaintext':raw,'domains':domains,'fixed_positions':sum(len(d)==1 for d in domains),
            'plaintext_positions':len(domains),'interim':middle,'interim_source_indices':p,
            'unpaired_interim_coordinate':middle[-1:]if len(middle)%2 else''}

def completion_witnesses(witness,template,key):
    unknown=[i for i,c in enumerate(key['square'])if c=='?'];unused=sorted(set(LETTERS)-set(key['square']))
    assert len(unknown)==2 and unused==['5','6'];source_masks=[i for i,c in enumerate(witness)if c=='?'];assert len(source_masks)<=1
    result=[]
    for values in itertools.permutations(unused):
        square=list(key['square'])
        for i,c in zip(unknown,values):square[i]=c
        completed=dict(key,square=''.join(square));binding={CO[i//6]+CO[i%6]:c for i,c in zip(unknown,values)}
        for fills in itertools.product(CO,repeat=len(source_masks)):
            full=list(witness)
            for i,c in zip(source_masks,fills):full[i]=c
            full=''.join(full);plain=inspect(full,completed)['plaintext']
            assert '?'not in plain and all(a=='?'or a==b for a,b in zip(template,plain))
            assert encrypt(plain,completed['column_rank_order'],completed['square'])==full==encode(plain,completed)
            result.append({'conditional_key_binding':binding,'remaining_source_mask_values':dict(zip(map(str,source_masks),fills)),
                           'plaintext':plain,'ciphertext':full})
    assert len(result)==2*6**len(source_masks)
    marginal=inspect(witness,key)['domains']
    assert [set(d)for d in marginal]==[{r['plaintext'][i]for r in result}for i in range(len(template))]
    return {'global_key_completions':2,'remaining_coordinate_erasures':len(source_masks),
            'complete_binding_and_fill_witnesses':result,'compatible_bindings_count':len(result),
            'distinct_complete_plaintexts':len({r['plaintext']for r in result}),
            'limit':'All appearances of each missing key cell share its one chosen label; marginal question-mark positions are not independent digit choices.'}

def exclusion_audit(record,key):
    count=len(record['excluded_source_indices']);assert count in(1,2)
    source=record['analysis_source'];target=encode(record['editorial_text'],key)
    histogram=Counter();minimum=None;winners=[];combined_minimum=None;combined=[];evaluations=0;local=[]
    for excluded in itertools.combinations(range(len(source)),count):
        removed=set(excluded);kept=[i for i in range(len(source))if i not in removed]
        cost=sum(source[i]!='?'and target[j]!='?'and source[i]!=target[j]for j,i in enumerate(kept))
        observed_exclusions=sum(source[i]!='?'for i in excluded);total=cost+observed_exclusions;evaluations+=1;histogram[cost]+=1
        row={'excluded_source_indices':list(excluded),'excluded_literal_glyphs':''.join(record['literal_source'][i]for i in excluded),
             'minimum_observed_substitutions_for_template':cost,'observed_coordinate_exclusions':observed_exclusions,
             'source_mask_exclusions':count-observed_exclusions,'combined_observed_operations':total}
        if minimum is None or cost<minimum:minimum=cost;winners=[]
        if cost==minimum:winners.append(row)
        if combined_minimum is None or total<combined_minimum:combined_minimum=total;combined=[]
        if total==combined_minimum:combined.append(row)
        if record['id']=='p160_A2'and excluded[0]in range(15,21)and excluded[1]in range(26,32):local.append(row)
        if record['id']=='p160_C1'and excluded[0]in range(280,286):local.append(row)
    assert any(r['excluded_source_indices']==record['excluded_source_indices']for r in winners)
    expected=28680 if count==2 else 309;assert evaluations==expected
    return {'source_id':record['id'],'source_slots':len(source),'model_slots':len(target),'fixed_candidate':record['editorial_text'],
            'template_question_marks_are_wildcards':True,'completed_exclusion_sets':evaluations,
            'observed_substitution_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'minimum_observed_substitutions':minimum,'all_minimum_substitution_sets':winners,
            'minimum_combined_observed_operations':combined_minimum,'all_minimum_combined_sets':combined,
            'all_source_local_long_group_options':local,
            'limit':'All exclusion sets are priced against this supplied candidate, not against all possible plaintexts. Source-local overlength groups motivate a model without proving the historical error mechanism.'}

def readable_audit(inputs):
    mappings=json.loads((HERE/'readable_mapping.json').read_text());records={r['id']:r for r in inputs['records']};result=[]
    for m in mappings['readings']:
        text=(ROOT/m['path']).read_text();section=text.split(m['heading']+'\n',1)[1].split('\n## ',1)[0]
        quote=next(line[2:]for line in section.splitlines()if line.startswith('> '));assert quote==m['text']
        folded=quote.upper().replace('Ä','AE').replace('Ö','OE').replace('Ü','UE').replace('ẞ','SS')
        folded=''.join(c for c in folded if c in LETTERS+'?')
        assert folded==records[m['id']]['editorial_text'].replace('X',''),m['id']
        assert quote.count('?')==records[m['id']]['editorial_text'].count('?')
        result.append({'id':m['id'],'matched_nonseparator_labels':len(folded),'unknown_positions':quote.count('?')})
    assert set(records)=={r['id']for r in result}
    return {'mapping_sha256':sha(HERE/'readable_mapping.json'),'readings':result,'rules':mappings['rules']}

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key'];published=next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']if k['id']==key['id'])
    assert key==published
    doc=None
    if pdf:
        import fitz
        assert sha(pdf)==data['source']['pdf_sha256'];doc=fitz.open(pdf)
    for im in data['source']['images']:
        assert sha(HERE/im['path'])==im['sha256']
        if doc:
            if im.get('fresh_render_cache'):fitz.TOOLS.store_shrink(100)
            pix=doc[im['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(im['scale'],im['scale']),clip=fitz.Rect(*im['clip_points']))
            assert (pix.width,pix.height)==(im['width'],im['height'])and hashlib.sha256(pix.samples).hexdigest()==im['pixel_sha256']
    results=[];geometries=[]
    for r in data['records']:
        literal=''.join(''.join(r['rows']).split());assert literal==r['literal_source']
        source=''.join(c if c in CO else'?'for c in literal);assert source==r['analysis_source']
        excluded=r['excluded_source_indices'];mapping=[i for i in range(len(source))if i not in excluded]
        frame=''.join(source[i]for i in mapping);assert len(frame)==r['advertised_length']
        raw=inspect(frame,key);assert raw['plaintext']==r['expected_raw'];template=r['editorial_text'];assert len(template)==raw['plaintext_positions']
        stencil=encode(template,key);witness=''.join(a if b=='?'else b for a,b in zip(frame,stencil));edited=inspect(witness,key);assert edited['plaintext']==template
        substitutions=[];fills=[]
        for j,(a,b)in enumerate(zip(frame,witness)):
            if a==b:continue
            i=mapping[j];p=raw['interim_source_indices'].index(j)//2
            item={'source_index':i,'model_index':j,'printed_glyph':literal[i],'before':a,'after':b,'plaintext_index':p,'raw_label':raw['plaintext'][p],'edited_label':template[p]}
            (fills if a=='?'else substitutions).append(item)
        changes=sorted([[x['source_index'],x['before'],x['after']]for x in substitutions+fills]);assert changes==r['expected_source_changes']
        cost={'known_coordinate_substitutions':len(substitutions),'source_mask_fills':len(fills),
              'excluded_observed_coordinates':sum(source[i]!='?'for i in excluded),'excluded_source_masks':sum(source[i]=='?'for i in excluded)}
        assert cost==r['expected_cost']
        num=[{'position':i,'raw':a,'edited':b}for i,(a,b)in enumerate(zip(raw['plaintext'],template))if a.isdigit()and a!=b];assert num==r['explicit_numeral_word_repairs']
        result={'id':r['id'],'source_slots':len(source),'valid_source_coordinates':len(source)-source.count('?'),
                'model_slots':len(frame),'raw_reading':raw,'edited_reading':edited,'model_to_source_indices':mapping,
                'source_coordinate_exclusions':[{'source_index':i,'glyph':literal[i],'analysis_symbol':source[i]}for i in excluded],
                'known_coordinate_substitutions':substitutions,'source_mask_fills':fills,'cost':cost,
                'reencrypted_analysis_witness':witness,'compatible_completions':completion_witnesses(witness,template,key),
                'explicit_numeral_word_repairs':num}
        if excluded:result['unaltered_source_diagnostic']=inspect(source,key);geometries.append(exclusion_audit(r,key))
        results.append(result)
    summary={'physical_records':len(results),'source_slots':sum(r['source_slots']for r in results),
             'valid_source_coordinates':sum(r['valid_source_coordinates']for r in results),'model_slots':sum(r['model_slots']for r in results),
             'plaintext_positions':sum(r['raw_reading']['plaintext_positions']for r in results),
             'raw_fixed_positions':sum(r['raw_reading']['fixed_positions']for r in results),
             'edited_fixed_positions':sum(r['edited_reading']['fixed_positions']for r in results),
             **{k:sum(r['cost'][k]for r in results)for k in ['known_coordinate_substitutions','source_mask_fills','excluded_observed_coordinates','excluded_source_masks']},
             'inserted_model_coordinates':0,'published_key_changes':0}
    assert summary==data['expected_totals']
    return {'schema':'adfgvx-nov8-radio-key-report-certificate-v1','authors':data['authors'],'inputs_sha256':sha(HERE/'inputs.json'),
            'summary':summary,'records':results,'fixed_template_exclusion_audits':geometries,
            'readable_display_audit':readable_audit(data),'limits':data['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,'source_pixels_checked':bool(a.pdf),**r['summary'],
                     'exclusion_audits':[{'id':g['source_id'],'evaluations':g['completed_exclusion_sets'],'min_substitutions':g['minimum_observed_substitutions'],'tied_minima':len(g['all_minimum_substitution_sets'])}for g in r['fixed_template_exclusion_audits']]},indent=2))
if __name__=='__main__':main()
