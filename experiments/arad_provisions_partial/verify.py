#!/usr/bin/env python3
"""Verify p159 A's conditional partial text, all tied maps and linked quantities.

Research and editorial work: icekylinx and GPT-6 Astra Pro.
The source edition remains271 slots; structural hypotheses are separately priced.
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
from adfgvx.cipher import decrypt,encrypt
from experiments.romanian_pacification_consultation.verify import inspect,permutation,masked_encryption
C='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fold(text):return ''.join(x for x in text.upper()if x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace('X','')

def stage(source,starts,one):
    excluded={i for st in starts for i in range(st,st+5)}
    assert len(excluded)==10
    kept=[(ch,i,'observed')for i,ch in enumerate(source)if i not in excluded]
    at=next((j for j,(_,i,_)in enumerate(kept)if i>=one),len(kept))
    return kept[:at]+[('?',None,'short_group_slot')]+kept[at:],sorted(excluded)

def framed(st,a,b):
    assert 0<=a<=b<=len(st)
    v=st[:a]+[('?',None,'first_five_slot_gap')]*5+st[a:b]+[('?',None,'second_five_slot_gap')]*5+st[b:]
    return ''.join(x for x,i,t in v),[i for x,i,t in v],[t for x,i,t in v]

def apply_stencil(base,stencil,mapping,tags,source,key):
    target=''.join(a if b=='?'else b for a,b in zip(base,stencil))
    substitutions=[];fills=[]
    for j,(a,b)in enumerate(zip(base,target)):
        if a==b:continue
        i=mapping[j];event={'model_index':j,'source_index':i,'printed':source[i]if i is not None else None,'from':a,'to':b,'slot_kind':tags[j]}
        (fills if a=='?'else substitutions).append(event)
    reconstructed=list(base)
    for event in substitutions+fills:reconstructed[event['model_index']]=event['to']
    assert ''.join(reconstructed)==target
    return {'ciphertext':target,'known_coordinate_substitutions':substitutions,'inserted_slot_fills':fills,**inspect(target,key,mapping)}

from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());r=d['record'];key=d['key'];family=d['search_family']
    assert d['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']if k['id']==key['id'])
    for path,digest in d['prior_artifacts'].items():assert sha(HERE/path)==digest
    source_evidence = verify_source_evidence(pdf, d['source'], d['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    source=''.join(''.join(r['source_rows']).split());assert len(source)==r['source_slots']==271 and set(source)<=set(C)
    assert source[25:30]==source[30:35]=='VDAGG'
    assert source[80:85]==source[85:90]=='FFXDF'
    assert source[115:119]=='GDDA'
    orphan=permutation(len(source),key['column_rank_order'])[-1]
    native={'literal_source':source,'source_slots':len(source),'native_raw_without_edits':decrypt(source,key['column_rank_order'],key['square'],allow_unpaired=True),'orphan':{'intermediate_index':len(source)-1,'source_index':orphan,'coordinate':source[orphan]},'observed_duplicate_groups':[{'starts':[25,30],'group':'VDAGG'},{'starts':[80,85],'group':'FFXDF'}],'short_group':{'start':115,'literal':'GDDA'},'no_source_coordinate_removed_in_this_layer':True}
    template=r['edited_output'];assert len(template)==136
    stencil=list(masked_encryption(template,key));order=permutation(272,key['column_rank_order'])
    # Bind the unresolved footer to its original VF cell, without choosing5/6.
    # Strength ?A retains its known second coordinate while its row remains free.
    assert r['quantity_plaintext_index']==96 and r['reference_plaintext_index']==131
    for p,pair in [(96,'?A'),(131,'VF')]:
        for ch,i in zip(pair,order[2*p:2*p+2]):stencil[i]=ch
    stencil=''.join(stencil);assert len(stencil)==272 and stencil.count('?')==1
    assert stencil[119]=='?'
    model=r['analysis_frame'];starts=model['primary_excluded_group_starts'];one=model['single_gap_before_source_index'];a=model['first_five_gap_stage_boundary'];b=model['second_five_gap_stage_boundary']
    st,excluded=stage(source,starts,one);assert len(st)==262
    base,mapping,tags=framed(st,a,b);assert len(base)==r['advertised_length']==272
    primary_raw=inspect(base,key,mapping);assert primary_raw['raw']==r['expected_raw']
    primary=apply_stencil(base,stencil,mapping,tags,source,key);assert primary['raw']==template
    assert primary_raw['fixed_positions']==124 and primary['fixed_positions']==134
    assert len(primary['known_coordinate_substitutions'])==r['expected_substitutions']==6
    assert len(primary['inserted_slot_fills'])==r['expected_inserted_slot_fills']==10
    assert primary['ciphertext'].count('?')==r['expected_inserted_slots_unfilled']==1
    assert sum(i is None for i in mapping)==11 and len(excluded)==10
    assert fold(r['readable_german'])==fold(primary['raw'])
    for token in r['protected_fields']:assert token in primary_raw['raw']and token in primary['raw']and token in r['readable_german']
    ledger=[(e['source_index'],e['from'],e['to'])for e in primary['known_coordinate_substitutions']]
    assert ledger==[(60,'G','X'),(65,'X','V'),(68,'V','X'),(69,'F','X'),(210,'X','G'),(235,'V','F')]
    assert [(p['plaintext_index'],p['pair'],p['domain'])for p in primary['positions']if p['raw']=='?']==[(96,'?A','34568PV'),(131,'VF','56')]
    # Canonical source-family pricing counts all 261 retained observed coordinates;
    # the one inserted short-group slot never counts as observed.
    count=0;prices_hash=hashlib.sha256();hist=Counter();minimum=10**6;best=[];stage_cache={}
    for one in family['one_coordinate_source_boundaries']:
        st,ex=stage(source,family['canonical_duplicate_starts'],one);text=''.join(c for c,i,t in st);stage_cache[one]=st;n=len(st);assert n==262
        pref={}
        for shift in (0,5,10):
            p=[0]
            for i,ch in enumerate(text):p.append(p[-1]+int(ch!='?'and stencil[i+shift]!='?'and ch!=stencil[i+shift]))
            pref[shift]=p
        for a in range(n+1):
            for b in range(a,n+1):
                price=pref[0][a]+pref[5][b]-pref[5][a]+pref[10][n]-pref[10][b]
                count+=1;hist[price]+=1;prices_hash.update(f'{one},{a},{b},{price}\n'.encode())
                if price<minimum:minimum=price;best=[]
                if price==minimum:best.append((one,a,b))
    assert count==family['canonical_evaluations']==173580
    assert prices_hash.hexdigest()==family['expected_price_sha256']
    assert minimum==family['expected_minimum_substitutions']==6
    assert best==[(118,a,b)for a in (15,16,17,18)for b in (107,108,109,110)]
    assert len(best)==family['expected_canonical_minimizing_maps']==16
    branches=list(itertools.product(*model['duplicate_group_alternatives']));assert len(branches)==4
    branch_equality=[]
    for branch in branches:
        for one in family['one_coordinate_source_boundaries']:
            st,ex=stage(source,branch,one)
            assert ''.join(c for c,i,t in st)==''.join(c for c,i,t in stage_cache[one])
        branch_equality.append({'excluded_group_starts':list(branch),'all_five_stage_strings_equal_to_canonical':True,'canonical_price_digest_applies':prices_hash.hexdigest()})
    # The identical retained strings prove that the same complete price table applies
    # to all four labeled source-instance branches; their source maps are kept below.
    assert count*len(branches)==family['source_labeled_models']==694320
    alternatives=[]
    for branch in branches:
        for one,a,b in best:
            st,ex=stage(source,branch,one);frame,mp,ts=framed(st,a,b)
            raw=inspect(frame,key,mp);edited=apply_stencil(frame,stencil,mp,ts,source,key)
            independent=sum(x!='?'and y!='?'and x!=y for x,y in zip(frame,stencil))
            assert independent==len(edited['known_coordinate_substitutions'])==6
            assert all(a=='?'or a==b for a,b in zip(template,edited['raw']))
            assert edited['positions'][131]['pair']=='VF'
            assert [(e['source_index'],e['from'],e['to'])for e in edited['known_coordinate_substitutions']]==ledger
            alternatives.append({'excluded_group_starts':list(branch),'excluded_source_indices':ex,'one_coordinate_source_boundary':one,'first_five_gap_stage_boundary':a,'second_five_gap_stage_boundary':b,'model_to_source_indices':mp,'ciphertext_with_unfilled_additions':frame,'raw':raw['raw'],'raw_fixed_positions':raw['fixed_positions'],'raw_unknown_positions':[p for p in raw['positions']if p['raw']=='?'],'edited_ciphertext':edited['ciphertext'],'edited_raw':edited['raw'],'edited_fixed_positions':edited['fixed_positions'],'known_coordinate_substitutions':edited['known_coordinate_substitutions'],'inserted_slot_fills':edited['inserted_slot_fills'],'quantity_position':edited['positions'][96],'footer_position':edited['positions'][131]})
    assert len(alternatives)==family['expected_source_labeled_minimizing_maps']==64
    quantities=Counter(x['quantity_position']['domain']for x in alternatives)
    assert quantities=={'P':48,'34568PV':16}
    # All primary completions: six choices for the remaining source-erasure row,
    # combined with both globally injective VF/XA assignments. No independent digit
    # choices are permitted for occurrences using those same square cells.
    cells=[i for i,ch in enumerate(key['square'])if ch=='?'];unused=sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(key['square']));assert unused==['5','6']
    witnesses=[]
    for labels in itertools.permutations(unused):
        sq=list(key['square'])
        for i,ch in zip(cells,labels):sq[i]=ch
        sq=''.join(sq);assert len(set(sq))==36
        for coordinate in C:
            cipher=primary['ciphertext'].replace('?',coordinate);plain=decrypt(cipher,key['column_rank_order'],sq)
            assert encrypt(plain,key['column_rank_order'],sq)==cipher
            assert all(a=='?'or a==b for a,b in zip(template,plain))
            qty,ref=plain[96],plain[131]
            if qty in '56':assert qty!=ref
            witnesses.append({'id':f'VF{sq[26]}_XA{sq[30]}_row{coordinate}','square':sq,'assignments':{'VF':sq[26],'XA':sq[30]},'quantity_pair':coordinate+'A','quantity_leading_label':qty,'quantity_field':plain[96:101],'footer_label':ref,'footer_field':plain[129:135],'plaintext':plain,'ciphertext':cipher,'exact_reencryption':True,'historical_selection_claim':False})
    assert len(witnesses)==12
    for alt in alternatives:
        compatible=[]
        for w in witnesses:
            if all(a=='?'or a==b for a,b in zip(alt['edited_ciphertext'],w['ciphertext'])):compatible.append(w['id'])
        assert len(compatible)==(2 if alt['quantity_position']['domain']=='P' else 12)
        alt['compatible_global_witness_ids']=compatible
    summary={'physical_records':1,'printed_source_slots':271,'valid_source_coordinates':271,'modeled_coordinates':272,'plaintext_positions':136,'baseline_fixed_positions':124,'candidate_fixed_positions':134,'known_coordinate_substitutions':6,'source_mask_fills':0,'source_or_model_erasure_fills':10,'inserted_slot_fills':10,'inserted_slots':11,'unfilled_inserted_slots':1,'source_deletions':10,'deleted_valid_source_coordinates':10,'source_reorderings':0,'published_key_changed':False,'canonical_gap_evaluations':173580,'equivalent_source_instance_branches':4,'source_labeled_models':694320,'canonical_minimizing_maps':16,'source_labeled_minimizing_maps':64,'minimum_observed_substitutions':6,'primary_global_completion_witnesses':12,'counting_frame':'One primary conditional 272-slot frame. Alternatives and completion witnesses are not additional physical records.'}
    return {'schema':'adfgvx-conditional-two-duplicate-partial-certificate-v1','authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All machine source, stage, model and plaintext indices are zero-based.','summary':summary,'record':{'id':r['id'],'header_literal':r['header_literal'],'native':native,'analysis_frame':model,'excluded_source_indices':excluded,'excluded_valid_coordinates':[{'source_index':i,'coordinate':source[i]}for i in excluded],'model_to_source_indices':mapping,'slot_tags':tags,'ciphertext_with_unfilled_additions':base,**primary_raw,'readable_candidate':primary,'readable_german':r['readable_german'],'readable_nonseparator_mapping_verified':True},'fixed_partial_target_comparison':{'scope':'Exhaustive within the declared source family and conditioned on this one partial text. It is not a language-independent source reconstruction or proof of unique historical wording.','plaintext_template':template,'coordinate_stencil':stencil,'quantity_constraint':'?A at plaintext96; its row is free.','footer_constraint':'VF at plaintext131; its value5/6 is not selected.','actual_canonical_price_evaluations':count,'equivalent_source_labeled_models':count*len(branches),'minimum':minimum,'canonical_price_digest':prices_hash.hexdigest(),'price_histogram':{str(k):v for k,v in sorted(hist.items())},'duplicate_branch_equality':branch_equality,'all_minimizing_source_maps':alternatives},'linked_quantity_family':{'primary_quantity_domain':'34568PV','footer_domain':'56','source_maps_with_literal_P0000':48,'source_maps_with_unresolved_leading_quantity':16,'conditional_digit_rule':'A quantity leading5 or6 uses XA, so the footer VF must use the other digit. Non-digit P/V remain allowed by the source family.','witnesses':witnesses},'prior_credit':d['prior_credit'],'limits':d['limits']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();out=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert out==json.loads(path.read_text())
    else:path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**out['summary']},indent=2))
if __name__=='__main__':main()
