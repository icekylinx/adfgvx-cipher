#!/usr/bin/env python3
"""Verify a conditional odd-length congratulation and all single-exclusion prices."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decode,untranspose
from experiments.premium_payment_stop.verify import C,A,sha,inspect,repair,permutation,masked_encryption,verify_crops

from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data=json.loads((HERE/'inputs.json').read_text());key=data['key'];r=data['records'][0]
    assert key==next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id']==key['id'])
    for f,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/data[f]['path'])==data[f]['sha256']
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    source=''.join(r['source_rows']).replace(' ','');assert len(source)==r['source_slots']==r['advertised_length']==75 and set(source)<=set(C)
    ranks=key['column_rank_order'];order75=permutation(75,ranks);middle=untranspose(source,ranks)
    assert middle==''.join(source[j] for j in order75)
    native=decode(middle[:-1],key['square']);assert native==r['native_paired_raw']
    orphan={'coordinate':middle[-1],'interim_index':74,'source_index':order75[-1]};assert orphan==r['native_orphan']
    at=r['conditional_excluded_source_index'];assert at==74 and source[at]==r['conditional_excluded_value']=='X'
    model=source[:at]+source[at+1:];mapping=list(range(at))+list(range(at+1,75));raw=inspect(model,key,mapping);assert raw['raw']==r['conditional_raw']
    candidate=repair(r['readable_candidate'],model,key,mapping,source);assert not candidate['erased_coordinate_fills']
    assert len(candidate['known_coordinate_substitutions'])==1
    change=candidate['known_coordinate_substitutions'][0];assert {k:change[k] for k in ['source_index','from','to']}==r['expected_substitution']
    unknown=[p for p in candidate['positions'] if p['raw']=='?'];assert len(unknown)==1 and unknown[0]['pair']=='VG' and unknown[0]['domain']=='234789QY' and unknown[0]['source_indices']==[19,60]
    assert unknown[0]['plaintext_index']==9
    order74=permutation(74,ranks);paired=''.join(p['pair'] for p in candidate['positions']);forward=['']*74
    for ch,i in zip(paired,order74):forward[i]=ch
    assert ''.join(forward)==candidate['ciphertext']
    received_shape=''.join(forward)+'X';assert [i for i,(a,b) in enumerate(zip(source,received_shape)) if a!=b]==[12]
    stencil=masked_encryption(r['readable_candidate'],key);paired_stencil=untranspose(stencil,ranks)
    unfilled_pairs=[C[i//6]+C[i%6] for i,ch in enumerate(key['square']) if ch=='?']
    def price(mid):
        known=sum(a!=b for a,b in zip(mid,paired_stencil) if b!='?')
        domain_extra=min(sum(a!=b for a,b in zip(mid[18:20],pair)) for pair in unfilled_pairs)
        return {'known_36_label_substitution_cost':known,'unknown_cell_domain_minimum_extra_cost':domain_extra,'all_37_positions_domain_cost':known+domain_extra}
    source_prices=[];interim_prices=[];alternatives=[]
    for i in range(75):
        c=source[:i]+source[i+1:];mp=list(range(i))+list(range(i+1,75));v=inspect(c,key,mp)
        source_prices.append({'excluded_source_index':i,'excluded_value':source[i],**price(untranspose(c,ranks)),'raw':v['raw']})
        m=middle[:i]+middle[i+1:]
        interim_prices.append({'excluded_interim_index':i,'excluded_source_index':order75[i],'excluded_value':middle[i],**price(m),'raw':decode(m,key['square'])})
        if 'VERLIEHENXGLUECKWUN5CH' in v['raw']:
            text=v['raw'].replace('GLUECKWUN5CH','GLUECKWUNSCH');ed=repair(text,c,key,mp,source)
            assert len(ed['known_coordinate_substitutions'])==1 and not ed['erased_coordinate_fills']
            assert ed['known_coordinate_substitutions'][0]['source_index']==12
            alternatives.append({'excluded_source_index':i,'excluded_value':source[i],'modeled_ciphertext':c,'raw':v,'edited':ed,'observed_exclusion_count':1})
    assert [a['excluded_source_index'] for a in alternatives]==r['endpoint_alternative_exclusions']==[0,1,73,74]
    assert alternatives[0]['modeled_ciphertext']==alternatives[1]['modeled_ciphertext']
    assert len(set(a['edited']['raw'] for a in alternatives))==3
    assert min(x['all_37_positions_domain_cost'] for x in source_prices)==1
    assert [x['excluded_source_index'] for x in source_prices if x['all_37_positions_domain_cost']==1]==[74]
    assert min(x['known_36_label_substitution_cost'] for x in interim_prices)==37
    assert min(x['all_37_positions_domain_cost'] for x in interim_prices)==38
    case=(ROOT/r['case_path']).read_text()
    assert re.sub('[^A-Z0-9?]','',r['readable_german'].upper()).replace('X','')==r['readable_candidate'].replace('X','')
    assert '> '+r['readable_german'] in case
    for a in alternatives:assert a['edited']['raw'] in case
    summary={'physical_records':1,'printed_source_slots':75,'valid_source_coordinates':75,'native_pair_positions':37,'native_orphan_coordinates':1,'modeled_coordinates':74,'plaintext_positions':37,'baseline_fixed_positions':raw['fixed_positions'],'candidate_fixed_positions':candidate['fixed_positions'],'known_coordinate_substitutions':1,'source_mask_fills':0,'conditionally_excluded_observed_source_coordinates':1,'unfilled_key_cell_plaintext_positions':1,'published_key_changed':False}
    return {'schema':'adfgvx-nov13-congratulation-conditional-frame-certificate-v1','project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.','summary':summary,'records':[{'id':r['id'],'literal_source':source,'literal_rows':r['source_rows'],'native_interim':middle,'native_paired_raw':native,'native_orphan':orphan,'conditional_model_to_source':mapping,'conditional_raw':raw,'readable_candidate':candidate,'source_shape_reconstruction':received_shape,'paired_coordinate_forward_verified':True,'ordinary_complete_plaintext_reencryption_verified':False,'endpoint_alternatives':alternatives}],'source_exclusion_prices':source_prices,'inverse_stage_exclusion_prices':interim_prices,'price_conventions':{'known_36_labels':'One unknown plaintext position is unconstrained; its two coordinates are ignored.','all_37_positions':'The unknown plaintext position must lie in one of the eight unassigned published square cells; no cell is filled.'},'headers':data['headers'],'limits':data['limits'],'prior_attribution_check':data['prior_attribution_check']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();out=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert out==json.loads(path.read_text())
    else:path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,**out['summary']},indent=2))
if __name__=='__main__':main()
