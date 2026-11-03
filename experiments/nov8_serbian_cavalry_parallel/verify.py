#!/usr/bin/env python3
"""Verify p158 E1's one-coordinate restoration from the independent p170 source.

Research and editorial work: icekylinx and GPT-6 Astra Pro.
The complete gap comparison is source-to-source, independent of word scoring.
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
from experiments.romanian_pacification_consultation.verify import inspect,repair,permutation
C='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fold(s):return ''.join(x for x in s.upper()if x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?').replace('X','')

from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());r=d['record'];key=d['key']
    assert d['authors']=='icekylinx and GPT-6 Astra Pro'
    assert key==next(x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']if x['id']==key['id'])
    for path,digest in d['prior_artifacts'].items():assert sha(HERE/path)==digest
    reference=d['parallel_reference'];assert sha(ROOT/reference['path'])==reference['sha256']
    old=json.loads((ROOT/reference['path']).read_text());prior=next(x for x in old['records']if x['id']==reference['record_id'])
    parallel=''.join(''.join(prior['raw_source_rows']).split())
    assert parallel==prior['raw_source_compact']==prior['analysis_ciphertext']
    assert set(parallel)<=set(C)and len(parallel)==236
    assert prior['column_rank_order']==key['column_rank_order']and prior['partial_square']==key['square']
    prior_raw=inspect(parallel,key,list(range(len(parallel))))
    assert prior_raw['raw']==prior['raw_geometry_plaintext']
    source_evidence = verify_source_evidence(pdf, d['source'], d['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    parallel_evidence = verify_source_evidence(pdf, d['source'], [reference['source_image']], ROOT)
    print(json.dumps({'parallel_source_evidence': parallel_evidence['summary']}))
    source=''.join(''.join(r['source_rows']).split())
    assert len(source)==r['source_slots']==235 and set(source)<=set(C)
    assert len(source)+1==r['advertised_length']==236
    native_raw=decrypt(source,key['column_rank_order'],key['square'],allow_unpaired=True)
    orphan_index=permutation(len(source),key['column_rank_order'])[-1]
    native={'literal_source':source,'source_slots':len(source),'raw_without_added_coordinate':native_raw,'orphan':{'intermediate_index':len(source)-1,'source_index':orphan_index,'coordinate':source[orphan_index]},'meaning_claim':False}
    # Align all235 observed coordinates with all236 possible one-coordinate deletions
    # of the independent printed236-coordinate witness. No plaintext candidate enters.
    prices=[];frames={}
    for gap in range(len(source)+1):
        shortened=parallel[:gap]+parallel[gap+1:]
        assert len(shortened)==len(source)
        mismatches=[{'source_index':i,'parallel_index':i if i<gap else i+1,'current':a,'parallel':b}for i,(a,b)in enumerate(zip(source,shortened))if a!=b]
        frame=source[:gap]+parallel[gap]+source[gap:]
        independent_count=sum(a!=b for a,b in zip(frame,parallel))
        assert independent_count==len(mismatches)
        mapping=list(range(gap))+[None]+list(range(gap,len(source)))
        prices.append({'source_boundary':gap,'parallel_coordinate_supplied':parallel[gap],'observed_coordinate_disagreements':len(mismatches),'observed_coordinate_agreements':len(source)-len(mismatches)})
        frames[gap]=(frame,mapping,mismatches)
    minimum=min(x['observed_coordinate_disagreements']for x in prices)
    minima=[x['source_boundary']for x in prices if x['observed_coordinate_disagreements']==minimum]
    assert minimum==3 and minima==[82,83,84,85]
    assert len({frames[g][0]for g in minima})==1
    near=[]
    for row in prices:
        if row['observed_coordinate_disagreements']<=minimum+1:
            gap=row['source_boundary'];frame,mapping,mismatches=frames[gap]
            near.append({**row,'model_to_source_indices':mapping,'source_disagreements':mismatches,'raw_unfilled':inspect(source[:gap]+'?'+source[gap:],key,mapping),'raw_with_parallel_coordinate':inspect(frame,key,mapping)})
    model=r['analysis_frame'];gap=model['source_boundary'];frame,mapping,mismatches=frames[gap]
    assert gap==model['parallel_coordinate_index']==85 and model['inserted_coordinates']==parallel[gap]=='A'
    assert source[85:89]=='XDGV'and parallel[85:90]=='AXDGV'
    raw=inspect(frame,key,mapping);assert raw['raw']==r['expected_raw']
    raw_unfilled=inspect(source[:gap]+'?'+source[gap:],key,mapping)
    candidate=repair(r['edited_output'],frame,key,mapping,source)
    assert len(candidate['known_coordinate_substitutions'])==r['expected_substitutions']==5
    assert not candidate['erased_coordinate_fills']
    assert fold(r['readable_german'])==fold(candidate['raw'])
    for token in r['protected_fields']:assert token in raw['raw']and token in candidate['raw']and token in r['readable_german']
    copy_repair=repair(prior_raw['raw'],frame,key,mapping,source)
    assert copy_repair['ciphertext']==parallel and len(copy_repair['known_coordinate_substitutions'])==3
    assert not copy_repair['erased_coordinate_fills']
    optional=r['optional_prior_headline_candidate'];optional_repair=repair(optional['plaintext'],frame,key,mapping,source)
    assert len(optional_repair['known_coordinate_substitutions'])==optional['expected_substitutions']==7
    changes=[];supported=[];editorial=[]
    for i,(a,b)in enumerate(zip(raw['raw'],candidate['raw'])):
        if a==b:continue
        row={'plaintext_index':i,'current_raw':a,'prior_raw':prior_raw['raw'][i],'edited':b,'current_pair':raw['positions'][i]['pair'],'prior_pair':prior_raw['positions'][i]['pair']}
        changes.append(row);(supported if prior_raw['raw'][i]==b else editorial).append(row)
    assert len(changes)==5 and len(supported)==3 and len(editorial)==2
    # Consensus is a set-valued statement retaining every source disagreement.
    joint=[]
    for i,(a,b)in enumerate(zip(raw['positions'],prior_raw['positions'])):
        domain=''.join(sorted(set(a['domain'])|set(b['domain'])))
        joint.append({'plaintext_index':i,'current_pair':a['pair'],'prior_pair':b['pair'],'domain':domain,'label':domain if len(domain)==1 else'?'})
    consensus=''.join(x['label']for x in joint)
    assert len(consensus)-consensus.count('?')==114
    unknown=[p for p in raw['positions']if p['raw']=='?']
    assert len(unknown)==1 and unknown[0]['pair']=='VF'and unknown[0]['domain']=='56'
    assert [p['pair']for p in candidate['positions']if p['raw']=='?']==['VF']
    # Both globally coupled digit completions are retained, including the other cell.
    squares=[];slots=[i for i,x in enumerate(key['square'])if x=='?'];symbols=sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')-set(key['square']))
    assert symbols==['5','6']
    for labels in itertools.permutations(symbols):
        square=list(key['square'])
        for cell,label in zip(slots,labels):square[cell]=label
        square=''.join(square);assert len(set(square))==36
        outputs=[]
        for name,cipher in [('raw_source_linked',frame),('edited',candidate['ciphertext']),('prior_raw',parallel),('optional_headline',optional_repair['ciphertext'])]:
            plaintext=decrypt(cipher,key['column_rank_order'],square)
            assert encrypt(plaintext,key['column_rank_order'],square)==cipher
            outputs.append({'layer':name,'plaintext':plaintext,'ciphertext':cipher,'exact_reencryption':True})
        squares.append({'square':square,'assignments':{C[i//6]+C[i%6]:square[i]for i in slots},'outputs':outputs,'historical_selection_claim':False})
    summary={'physical_records':1,'printed_source_slots':235,'valid_source_coordinates':235,'modeled_coordinates':236,'plaintext_positions':118,'unfilled_gap_fixed_positions':raw_unfilled['fixed_positions'],'baseline_fixed_positions':raw['fixed_positions'],'candidate_fixed_positions':candidate['fixed_positions'],'source_linked_coordinate_additions':1,'known_coordinate_substitutions':5,'substitutions_supported_by_other_raw_copy':3,'shared_editorial_substitutions':2,'source_mask_fills':0,'source_or_model_erasure_fills':0,'inserted_slots':1,'source_deletions':0,'source_reorderings':0,'published_key_changed':False,'source_alignment_boundaries':236,'minimum_source_disagreements':3,'minimizing_boundaries':[82,83,84,85],'distinct_minimum_filled_ciphertexts':1,'global_digit_completions':2}
    return {'schema':'adfgvx-source-linked-one-coordinate-parallel-certificate-v1','authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All source and plaintext indices are zero-based.','summary':summary,'record':{'id':r['id'],'native':native,'analysis_frame':model,'model_to_source_indices':mapping,'ciphertext':frame,**raw,'unfilled_gap':raw_unfilled,'readable_candidate':candidate,'readable_german':r['readable_german'],'readable_label_mapping_verified':True,'optional_prior_headline_candidate':optional_repair},'parallel':{'reference':reference,'header_literal':prior['source']['header_transcription'],'literal_source':parallel,'raw':prior_raw,'repair_to_other_raw_copy':copy_repair,'new_plaintext_changes':changes,'changes_supported_by_other_raw_copy':supported,'shared_editorial_changes':editorial,'source_disagreements':mismatches,'conservative_union':{'template':consensus,'fixed_positions':114,'positions':joint},'counts_as_new_physical_record':False},'source_alignment':{'scope':'All236 one-coordinate source alignments against the independent p170 printed body. No language score or desired plaintext is used. This does not exclude other error mechanisms.','all_prices':prices,'price_histogram':{str(k):v for k,v in sorted(Counter(x['observed_coordinate_disagreements']for x in prices).items())},'minimum':minimum,'minimizing_boundaries':minima,'all_frames_within_one_disagreement_of_minimum':near},'global_completion_witnesses':squares,'prior_credit':d['prior_credit'],'limits':d['limits']}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify',action='store_true');ap.add_argument('--pdf',type=Path);a=ap.parse_args();out=build(a.pdf);path=HERE/'certificates.json'
    if a.verify:assert out==json.loads(path.read_text())
    else:path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**out['summary']},indent=2))
if __name__=='__main__':main()
