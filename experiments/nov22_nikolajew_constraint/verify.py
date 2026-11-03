#!/usr/bin/env python3
"""Verify the optional Nov22 GD=J constraint and its complete declared source scope.

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



import itertools


def read(path):
    return json.loads((ROOT/path).read_text())


def source_variants():
    """One declared inventory, including unfavorable records and tied frames."""
    variants=[]
    def add(physical, variant, cipher, mapping, expected, provenance, primary=False):
        assert all(c in C+'?' for c in cipher)
        variants.append({'physical_record':physical,'variant':variant,'ciphertext':cipher,
                         'model_to_source_indices':mapping,'expected_baseline':expected,
                         'provenance':provenance,'is_primary_raw':primary})
    for package in ['medical_return_transports','reval_steamer_notice','hermannstadt_cash_transport','hermannstadt_radio_report']:
        path=f'experiments/{package}/certificates.json';d=read(path)
        for r in d['records']:
            add(r['id'],'primary_source_model',r['ciphertext'],r['model_to_source_indices'],r['raw'],path,True)
            e=r['readable_candidate']
            add(r['id'],'earlier_ordinary_word_candidate',e['ciphertext'],r['model_to_source_indices'],e['raw'],path)
        if package=='medical_return_transports':
            geometry=d['first_part_conditional_geometry']
            for v in geometry['all_tied_variant_certificates']:
                gap=v['gap_before_source_index']
                if gap==geometry['primary_gap']:continue
                add('p212_A1',f'tied_gap_{gap}_raw',v['ciphertext'],v['model_to_source_indices'],v['raw'],path)
                e=v['readable_candidate'];add('p212_A1',f'tied_gap_{gap}_candidate',e['ciphertext'],v['model_to_source_indices'],e['raw'],path)
        if package=='reval_steamer_notice':
            v=d['source_glyph_alternative']
            add('p213_A1','overprinted_glyph_V_alternative',v['ciphertext'],list(range(len(v['ciphertext']))),v['raw'],path)
        if package=='hermannstadt_cash_transport':
            primary=read(f'experiments/{package}/inputs.json')['records'][0]['model']['primary_gap']
            for v in d['conditional_short_group_geometry']['all_equal_minimum_variants']:
                gap=v['gap_before_source_index']
                if gap==primary:continue
                add('p216_B1',f'tied_gap_{gap}_raw',v['ciphertext'],v['model_to_source_indices'],v['raw'],path)
                e=v['readable_candidate'];add('p216_B1',f'tied_gap_{gap}_candidate',e['ciphertext'],v['model_to_source_indices'],e['raw'],path)
        if package=='hermannstadt_radio_report':
            for g in d['conditional_deletion_geometries']:
                for v in g['all_equal_minimum_variants']:
                    deleted=v['deleted_source_index']
                    if deleted==g['primary_deleted_source_index']:continue
                    add(g['record'],f'tied_deletion_{deleted}_raw',v['ciphertext'],v['model_to_source_indices'],v['raw'],path)
                    e=v['readable_candidate'];add(g['record'],f'tied_deletion_{deleted}_candidate',e['ciphertext'],v['model_to_source_indices'],e['raw'],path)
    path='experiments/open_targets_continuation/certificates.json'
    r=next(r for r in read(path)['results'] if r['id']=='p214_B');m=list(range(len(r['analysis_ciphertext'])))
    add('p214_B','primary_source_model',r['analysis_ciphertext'],m,r['direct']['plaintext'],path,True)
    add('p214_B','earlier_ordinary_word_candidate',r['editorial']['ciphertext'],m,r['editorial']['plaintext'],path)
    path='data/certificates/p215.json';r=read(path)
    add('p215','norbert_two_gap_source_model',r['constraints']['augmented_ciphertext'],
        r['constraints']['augmented_to_original_index'],r['constraints']['raw_partial_plaintext'],path,True)
    path='experiments/operational_recovery/certificates.json'
    for r in read(path)['records']:
        if r['key_id']!='Nov22-24':continue
        cipher=''.join(c if c in C else '?' for c in r['source_ciphertext']);m=list(range(len(cipher)))
        add(r['id'],'primary_source_model',cipher,m,r['raw']['plaintext'],path,True)
        add(r['id'],'earlier_ordinary_word_candidate',r['edition']['ciphertext'],m,r['edition']['reading']['plaintext'],path)
    return variants


def partial_square(base,ambiguous,assignments):
    square=['?' if c in ambiguous else c for c in base]
    for old,new in assignments.items():
        assert old in ambiguous and new not in square
        square[base.index(old)]=new
    value=''.join(square)
    assert len(value)==36 and len(set(value)-{'?'})==36-value.count('?')
    return value


def completion(square):
    unused=iter(sorted(set(A)-set(square)))
    result=''.join(next(unused) if c=='?' else c for c in square)
    assert set(result)==set(A) and len(result)==36
    return result


def witness(cipher,key,positions):
    full=completion(key['square']);filled=cipher.replace('?','A')
    plain=decrypt(filled,key['column_rank_order'],full)
    assert encrypt(plain,key['column_rank_order'],full)==filled
    assert all(a=='?' or a==b for a,b in zip(cipher,filled))
    assert all(c in p['domain'] for c,p in zip(plain,positions))
    return {'square':full,'filled_ciphertext':filled,'plaintext':plain,
            'source_preserved':True,'is_recovered_historical_plaintext':False}


def nearby(text,index,radius=17):
    a=max(0,index-radius);b=min(len(text),index+radius+1)
    return {'start':a,'text':text[a:b],'marked_index_within_context':index-a}


def earlier_place_witness():
    source_path='experiments/corcovado_sale_terms/certificates.json'
    record=next(r for r in read(source_path)['records'] if r['id']=='p173_A1')
    key=next(k for k in read('data/keys.json')['keys'] if k['id']==record['key_id'])
    fresh=inspect(record['ciphertext'],key,record['model_to_source_indices'])
    assert fresh['raw']==record['raw']
    start=fresh['raw'].index('NIKOLAJEW');positions=fresh['positions'][start:start+9]
    assert positions==record['readable_candidate']['positions'][start:start+9]
    assert all('?' not in p['pair'] and None not in p['source_indices'] for p in positions)
    return {'record':'p173_A1','key_id':key['id'],'source':source_path,'raw':fresh['raw'],
            'plaintext_start':start,'literal_place_spelling':'NIKOLAJEW','positions':positions,
            'all_name_coordinates_observed_and_unchanged':True,
            'place_identity_with_later_messages_is_an_additional_assumption':True}


def enumerate_footer(target,key,square):
    layer_key=dict(key,square=square)
    positions=inspect(target['ciphertext'],layer_key,target['model_to_source_indices'])['positions']
    last=positions[-4:]
    assert [p['pair'] for p in last]==['FD','FA','XD','AV']
    assert all('?' not in p['pair'] and None not in p['source_indices'] for p in last)
    pool=''.join(sorted(set(A)-set(square)));values=[]
    for a,b in itertools.permutations(pool,2):
        s=list(square);s[key['square'].index('3')]=a;s[key['square'].index('5')]=b
        full=completion(''.join(s));filled=target['ciphertext'].replace('?','A')
        plain=decrypt(filled,key['column_rank_order'],full)
        assert plain[-4:]==a+'1'+b+'6'
        assert encrypt(plain,key['column_rank_order'],full)==filled
        assert all(x=='?' or x==y for x,y in zip(target['ciphertext'],filled))
        values.append({'value':plain[-4:],'full_square_witness':full,'plaintext_witness':plain})
    assert len(values)==len({x['value'] for x in values})==len(pool)*(len(pool)-1)
    numeric=[x['value'] for x in values if x['value'].isdigit()]
    return {'pattern':'a1b6','a_and_b_domain':pool,'distinct_a_and_b':True,'source_positions':last,
            'count':len(values),'source_preserving_global_witness_for_each_value':values,
            'all_four_characters_are_digits_extra_assumption':{'values':numeric,'count':len(numeric),'leading_zero_allowed':True}}


def cache_screen(inputs,key):
    output=[]
    for n,r in enumerate(inputs['unreviewed_cache_candidates']):
        cipher=r['ciphertext'];order=permutation(len(cipher),key['column_rank_order'])
        middle=''.join(cipher[j] for j in order)
        raw=decrypt(cipher,key['column_rank_order'],key['square'],allow_unpaired=True)
        assert raw==r['plaintext']
        assert len(cipher)%2==r.get('orphan',0)
        occurrences=[]
        for i,c in enumerate(raw):
            if c!='9':continue
            pair=middle[2*i:2*i+2];indices=order[2*i:2*i+2]
            assert pair=='GD'
            occurrences.append({'plaintext_index':i,'pair':pair,'candidate_ciphertext_indices':indices,
                                'baseline_context':nearby(raw,i),'simple_label_substitution_context':nearby(raw.replace('9','J'),i)})
        output.append({'frozen_input_row':n,'source_cache':r['source_cache'],'block':r['block'],'score':r['score'],
                       'plaintext':raw,'raw_9_occurrences':occurrences,
                       'orphan_unpaired_coordinate':middle[-1] if len(cipher)%2 else None,
                       'is_source_reviewed':False,'is_asserted_member_of_historical_key_period':False})
    assert len(output)==123
    return {'scope':inputs['unreviewed_cache_scope'],'candidate_rows':len(output),
            'raw_9_occurrence_count':sum(len(r['raw_9_occurrences']) for r in output),'records':output,
            'assessment':'The high-coherence independently source-checked extra lexical support is p216_B2 9EWEILS. The caches also retain B9VERN and many damaged or wrong-key strings; they are not evidence for silently changing references or proper names.'}


def build():
    inputs=json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    for path,expected in inputs['dependency_sha256'].items():assert sha(ROOT/path)==expected,(path,sha(ROOT/path),expected)
    key=next(k for k in read('data/keys.json')['keys'] if k['id']==inputs['key_id'])
    assert key['square'][19]=='9' and C[19//6]+C[19%6]=='GD'
    definition=read('experiments/operational_recovery/inputs.json')['interpretation_layers'][key['id']]
    assert definition['ambiguous_baseline_labels']==inputs['ambiguous_baseline_labels']
    assert definition['layers'][0]['assignments']==inputs['prior_numeric_assignments']
    numbers=inputs['prior_numeric_assignments']
    definitions=[('lexical_J_only',{'9':'J'}),('prior_numeric_only',numbers),('prior_numeric_plus_lexical_J',{**numbers,'9':'J'})]
    layers={name:partial_square(key['square'],inputs['ambiguous_baseline_labels'],assignments) for name,assignments in definitions}
    assert ''.join(sorted(set(A)-set(layers['prior_numeric_only'])))=='0345789JQY'
    assert ''.join(sorted(set(A)-set(layers['prior_numeric_plus_lexical_J'])))=='0345789QY'
    variants=source_variants();physical=sorted({r['physical_record'] for r in variants})
    assert physical==sorted(inputs['expected_physical_records']) and len(physical)==21
    assert len(variants)==54 and len({(r['physical_record'],r['variant']) for r in variants})==54
    results=[]
    for r in variants:
        raw=inspect(r['ciphertext'],key,r['model_to_source_indices']);assert raw['raw']==r['expected_baseline']
        interpretations={}
        full_reads={}
        for name,square in layers.items():
            layer_key=dict(key,square=square);new=inspect(r['ciphertext'],layer_key,r['model_to_source_indices']);full_reads[name]=new
            interpretations[name]={'square':square,'conditional_plaintext':new['raw'],'fixed_positions':new['fixed_positions'],
                                   'all_position_domains':[p['domain'] for p in new['positions']],
                                   'global_source_preserving_witness':witness(r['ciphertext'],layer_key,new['positions'])}
        events=[];changes=[]
        for p in raw['positions']:
            i=p['plaintext_index']
            if p['raw']=='9':
                assert p['pair']=='GD'
                assert full_reads['lexical_J_only']['positions'][i]['raw']=='J'
                kind='medical shared-place-name assumption' if r['physical_record'] in ['p212_A1','p213_A6','p213_A7'] else ('independent ordinary-word JEWEILS assumption' if r['physical_record']=='p216_B2' else 'unresolved vessel-like field; no identity or correctness asserted')
                events.append({**p,'baseline_context':nearby(raw['raw'],i),
                               'conditional_context':nearby(full_reads['prior_numeric_plus_lexical_J']['raw'],i),'assessment':kind})
            before=full_reads['prior_numeric_only']['positions'][i];after=full_reads['prior_numeric_plus_lexical_J']['positions'][i]
            if before['domain']!=after['domain']:
                changes.append({'plaintext_index':i,'pair':p['pair'],'model_indices':p['model_indices'],
                                'source_indices':p['source_indices'],'baseline_label':p['raw'],
                                'prior_numeric_domain':before['domain'],'after_GD_J_domain':after['domain'],
                                'was_fixed':len(before['domain'])==1,'is_now_fixed':len(after['domain'])==1,
                                'baseline_context':nearby(raw['raw'],i)})
        results.append({**r,'baseline_plaintext':raw['raw'],'raw_9_occurrences':events,
                        'interpretations':interpretations,'complete_domain_change_inventory':changes})
    primaries=[r for r in results if r['is_primary_raw']]
    assert len(primaries)==21
    primary_events=[{'physical_record':r['physical_record'],**p} for r in primaries for p in r['raw_9_occurrences']]
    assert len(primary_events)==5 and {r['physical_record'] for r in primary_events}=={'p212_A1','p213_A6','p213_A7','p213_A2','p216_B2'}
    assert sum(len(r['raw_9_occurrences']) for r in results)==16
    target=next(r for r in variants if r['physical_record']=='p215')
    before=enumerate_footer(target,key,layers['prior_numeric_only']);after=enumerate_footer(target,key,layers['prior_numeric_plus_lexical_J'])
    assert before['count']==90 and after['count']==72
    assert before['all_four_characters_are_digits_extra_assumption']==after['all_four_characters_are_digits_extra_assumption']
    assert after['all_four_characters_are_digits_extra_assumption']['count']==42
    removed=sorted({r['value'] for r in before['source_preserving_global_witness_for_each_value']}-{r['value'] for r in after['source_preserving_global_witness_for_each_value']})
    assert len(removed)==18 and all('J' in r for r in removed)
    adverse_source=read('experiments/hermannstadt_radio_report/certificates.json')['unchanged_name_like_field']
    adverse=next(r for r in results if r['physical_record']=='p216_A2' and r['is_primary_raw'])
    pos=adverse_source['special_position']['plaintext_index']
    assert pos==52 and adverse['expected_baseline'][46:55]=='NIKOLA3EW'
    domains={name:r['all_position_domains'][pos] for name,r in adverse['interpretations'].items()}
    assert 'J' in domains['prior_numeric_only'] and 'J' not in domains['lexical_J_only'] and 'J' not in domains['prior_numeric_plus_lexical_J']
    assert adverse['ciphertext'][26]=='F'
    hypothetical=adverse['ciphertext'][:26]+'G'+adverse['ciphertext'][27:]
    hypothetical_key=dict(key,square=layers['prior_numeric_plus_lexical_J'])
    hypothetical_read=inspect(hypothetical,hypothetical_key,adverse['model_to_source_indices'])
    assert hypothetical_read['raw'][46:55]=='NIKOLAJEW'
    assert sum(a!=b for a,b in zip(adverse['ciphertext'],hypothetical))==1
    adverse_result={**adverse_source,'conditional_domains_at_name_character':domains,
        'J_excluded_by_injectivity_after_GD_J':True,'unchanged_source_same_spelling_is_compatible':False,
        'unapplied_one_coordinate_demonstration':{'source_index':26,'from':'F','to':'G',
            'ciphertext':hypothetical,'conditional_plaintext':hypothetical_read['raw'],
            'additional_source_coordinate_substitutions':1,'is_applied_to_any_inventory_variant':False}}
    p215=read('data/certificates/p215.json')
    return {'schema':'adfgvx-nov22-lexical-constraint-certificate-v1','project':inputs['project'],'authors':inputs['authors'],
      'input_sha256':sha(HERE/'inputs.json'),'indexing':inputs['indexing'],'dependency_sha256':inputs['dependency_sha256'],
      'conditional_assignment':inputs['conditional_assignment'],'independent_assumption_routes':inputs['independent_assumption_routes'],
      'conditional_squares':{name:{'square':square,'remaining_symbols':''.join(sorted(set(A)-set(square)))} for name,square in layers.items()},
      'summary':{'physical_records':21,'source_and_editorial_variants':54,'primary_raw_9_occurrences':5,
                 'all_variant_raw_9_occurrences':16,'additional_fixed_positions_across_primary_source_models':sum(sum(not p['was_fixed'] and p['is_now_fixed'] for p in r['complete_domain_change_inventory']) for r in primaries),
                 'primary_source_positions_with_any_domain_change':sum(len(r['complete_domain_change_inventory']) for r in primaries),
                 'source_coordinate_changes':0,'baseline_key_changed':False,'historical_digit_values_recovered':0},
      'earlier_literal_name_witness':earlier_place_witness(),'all_primary_raw_9_occurrences':primary_events,'adverse_name_like_occurrence':adverse_result,
      'records':results,'p215_footer':{'before_new_lexical_hypothesis':before,'after_new_lexical_hypothesis':after,
          'exactly_removed_values':removed,'depends_on_prior_numeric_assignments':numbers,
          'numeric_only_assumption_is_additional_and_unchanged':True},
      'p215_unpropagated_editorial_completion':{'source':'data/certificates/p215.json','published_readings':p215['published_readings'],
          'plaintext_length':p215['editorial_completion_comparison']['plaintext_length'],
          'model_plaintext_length':p215['editorial_completion_comparison']['model_plaintext_length'],
          'reason':'The 130-character Baertl wording has no compatible 129-position coordinate certificate. Its best single-deletion comparisons already contradict at least 27 observed coordinates; it is not another source-consistent variant in this inventory.'},
      'unreviewed_cache_screen':cache_screen(inputs,key),'scope_exclusions':inputs['scope_exclusions'],
      'limits':['GD is fixed by the ciphertext, while J is inferred from optional language assumptions.',
                'The two lexical routes are distinct from the earlier historical-formation numerical hypotheses; their conjunction is explicitly separate.',
                'B9VERN becomes BJVERN and remains unidentified. NIKOLA3EW uses FD, where J is excluded after GD=J; a same-spelling reading would require an additional source change. No inconvenient source occurrence is omitted from the declared reviewed scope.',
                'A partial-square witness demonstrates consistency, not historical correctness; unresolved labels remain one shared injective pool.',
                'No model, source transcript, original ciphertext, baseline square or earlier repair cost is changed.',
                'The inventory is complete for the stated 21 reviewed physical records and 54 certified variants; it is not a claim that the whole historical key period has been decoded.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
    result=build();target=HERE/'certificate.json'
    if a.verify:assert result==json.loads(target.read_text())
    else:target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**result['summary']},indent=2))
    print('p215 footer: 90 -> 72; all-digit subset: 42 -> 42.')


if __name__=='__main__':main()
