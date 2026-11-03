#!/usr/bin/env python3
"""Verify a conditional surplus coordinate before transposition in p135 A.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from experiments.premium_payment_stop.verify import C,inspect,repair,permutation,sha,verify_crops
from adfgvx.cipher import decrypt,decode,encode,transpose,untranspose


def stage_reading(stream,origins,key):
    positions=[];square=key['square']
    for i in range(0,len(stream)-1,2):
        pair=stream[i:i+2];domain=''.join(sorted(square[6*r+c]for r in range(6)for c in range(6)if pair[0]in('?',C[r])and pair[1]in('?',C[c])))
        positions.append({'plaintext_index':i//2,'interim_indices':[i,i+1],'source_indices':origins[i:i+2],'pair':pair,'domain':domain,'raw':domain if len(domain)==1 else'?'})
    raw=''.join(p['raw']for p in positions);assert raw==decode(stream,square,allow_unpaired=True)
    orphan={'interim_index':len(stream)-1,'source_index':origins[-1],'coordinate':stream[-1]}if len(stream)%2 else None
    return {'raw':raw,'fixed_positions':sum(p['raw']!='?'for p in positions),'positions':positions,'unpaired_coordinate':orphan}


def stage_proposal(candidate,middle,origins,excluded,literal,key):
    stream=middle[:excluded]+middle[excluded+1:];mapping=origins[:excluded]+origins[excluded+1:];raw=stage_reading(stream,mapping,key);target=''.join(C[key['square'].index(ch)//6]+C[key['square'].index(ch)%6]for ch in candidate);assert target==encode(candidate,key['square'])and len(target)==len(stream)
    edits=[];fills=[]
    for i,(before,after)in enumerate(zip(stream,target)):
        if before==after:continue
        source=mapping[i];event={'interim_index':i,'source_index':source,'printed':literal[source],'from':before,'to':after}
        (fills if before=='?'else edits).append(event)
    edits.sort(key=lambda x:x['source_index']);fills.sort(key=lambda x:x['source_index'])
    surplus=middle[excluded];witness_middle=target[:excluded]+surplus+target[excluded:];witness=transpose(witness_middle,key['column_rank_order']);rebuilt=list(''.join(ch if ch in C else'?'for ch in literal))
    for event in edits+fills:assert rebuilt[event['source_index']]==event['from'];rebuilt[event['source_index']]=event['to']
    assert ''.join(rebuilt)==witness and len(witness)==len(literal)
    recovered=untranspose(witness,key['column_rank_order']);assert recovered[excluded]==surplus;recovered=recovered[:excluded]+recovered[excluded+1:];edited=stage_reading(recovered,mapping,key);assert edited['raw']==candidate
    return {'excluded_interim_index':excluded,'excluded_source_index':origins[excluded],'excluded_literal':literal[origins[excluded]],'excluded_valid_coordinate':surplus in C,'working_interim':stream,'working_to_source_indices':mapping,'working_raw':raw,'readable_candidate':{'template':candidate,**edited,'known_coordinate_substitutions':edits,'erased_coordinate_fills':fills,'source_shaped_reencryption_verified':True,'standard_even_frame_encryption_claimed':False,'source_shaped_ciphertext':witness,'source_shaped_interim':witness_middle,'published_key_changed':False}}


def build(pdf=None):
    d=json.loads((HERE/'inputs.json').read_text());k=d['key'];assert k==next(x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']if x['id']==k['id'])
    for field,base in [('prior_attribution_check',HERE),('verification_helper',ROOT)]:assert sha(base/d[field]['path'])==d[field]['sha256']
    for crop in d['source_images']:assert sha(HERE/crop['path'])==crop['sha256']
    if pdf:verify_crops(pdf,d['source'],d['source_images'],HERE)
    s=d['records'][0];literal=''.join(s['source_rows']).replace(' ','');base=''.join(ch if ch in C else'?'for ch in literal);assert len(literal)==s['source_slots']==s['advertised_length']==401
    order=permutation(len(base),k['column_rank_order']);middle=''.join(base[i]for i in order);assert middle==untranspose(base,k['column_rank_order'])and transpose(middle,k['column_rank_order'])==base
    native=stage_reading(middle,order,k);assert native['raw']==decrypt(base,k['column_rank_order'],k['square'],allow_unpaired=True)
    aliases=[stage_proposal(s['readable_candidate'],middle,order,j,literal,k)for j in s['frame_model']['equivalent_excluded_interim_indices']]
    assert [a['excluded_interim_index']for a in aliases]==[230,231]and [a['excluded_source_index']for a in aliases]==[296,84]
    assert aliases[0]['working_interim']==aliases[1]['working_interim']
    assert all(a['excluded_literal']=='X'and a['excluded_valid_coordinate']for a in aliases)
    assert aliases[0]['readable_candidate']['source_shaped_ciphertext']==aliases[1]['readable_candidate']['source_shaped_ciphertext']
    r=aliases[0];assert r['working_raw']['raw']==s['expected_working_raw'];candidate=r['readable_candidate']
    prices=[]
    target=encode(s['readable_candidate'],k['square'])
    for j in range(len(base)):
        sm=middle[:j]+middle[j+1:];orig=order[:j]+order[j+1:]
        edits=sum(a!=b and a in C for a,b in zip(sm,target));fills=sum(a!=b and a=='?'for a,b in zip(sm,target))
        prices.append({'stage':'interim','excluded_index':j,'source_index':order[j],'excluded_literal':literal[order[j]],'excluded_valid_coordinate':middle[j]in C,'observed_substitutions':edits,'source_mask_fills':fills})
        c=base[:j]+base[j+1:];mp=list(range(j))+list(range(j+1,len(base)));rr=repair(s['readable_candidate'],c,k,mp,literal)
        prices.append({'stage':'transmitted','excluded_index':j,'source_index':j,'excluded_literal':literal[j],'excluded_valid_coordinate':base[j]in C,'observed_substitutions':len(rr['known_coordinate_substitutions']),'source_mask_fills':len(rr['erased_coordinate_fills'])})
    minima={}
    for stage in ['interim','transmitted']:
        vals=[p for p in prices if p['stage']==stage];cost=min(p['observed_substitutions']for p in vals);minima[stage]={'observed_substitutions':cost,'excluded_indices':[p['excluded_index']for p in vals if p['observed_substitutions']==cost]}
    assert minima=={'interim':{'observed_substitutions':7,'excluded_indices':[230,231]},'transmitted':{'observed_substitutions':144,'excluded_indices':[297,298,299]}}
    w=d['already_reviewed_closing_witness'];assert w['already_catalogued']and not w['counted_as_new_record'];assert sha(ROOT/w['source_inputs_path'])==w['source_inputs_sha256'];old=next(x for x in json.loads((ROOT/w['source_inputs_path']).read_text())['records']if x['id']==w['record']);assert old==w['source_record_snapshot'];assert sha(ROOT/w['source_crop_path'])==w['source_crop_sha256'];ol=''.join(old['raw_grouped'].split());assert ol==w['literal_source'];old_raw=inspect(ol,k,list(range(len(ol))));assert old_raw['raw']==w['expected_raw']
    if pdf:verify_crops(pdf,d['source'],[{'path':w['source_crop_path'],'pdf_page_1based':old['pdf_page_1based'],'crop_pdf_points':old['crop_pdf_points'],'render_scale':old['render_scale']}],ROOT)
    closing=w['shared_closing'];assert len(closing)==58;old_start=old_raw['raw'].index(closing);new_start=candidate['raw'].index(closing);assert old_start==60 and new_start==142
    pairs=[]
    for before,after in zip(old_raw['positions'][old_start:],candidate['positions'][new_start:]):
        assert before['pair']==after['pair']and before['domain']==after['domain']and before['raw']==after['raw'];pairs.append({'letter':after['raw'],'new_plaintext_index':after['plaintext_index'],'old_plaintext_index':before['plaintext_index'],'new_source_indices':after['source_indices'],'old_source_indices':before['source_indices'],'coordinate_pair':after['pair']})
    assert re.sub('[^A-Z0-9?]','',s['readable_german'].upper()).replace('X','')==s['readable_candidate'].replace('X','')
    assert '> '+s['readable_german']in(ROOT/s['case_path']).read_text()
    summary={'physical_records':1,'printed_source_slots':401,'valid_source_coordinates':397,'received_frame_coordinates':401,'paired_interim_coordinates':400,'plaintext_positions':200,'baseline_fixed_positions':r['working_raw']['fixed_positions'],'candidate_fixed_positions':candidate['fixed_positions'],'known_coordinate_substitutions':len(candidate['known_coordinate_substitutions']),'source_mask_fills':len(candidate['erased_coordinate_fills']),'paired_model_excluded_observed_coordinates':1,'transmitted_frame_insertions_or_deletions':0,'published_key_changed':False}
    assert summary['known_coordinate_substitutions']==7 and summary['source_mask_fills']==4
    return {'schema':'adfgvx-siegfried-assignment-cancellation-certificate-v1','project':d['project'],'authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based. Interim indices are measured after inverse transposition of the received401-slot frame.','summary':summary,'records':[{'id':s['id'],'literal_source':literal,'literal_printed_rows':s['source_rows'],'native_received_frame':native,'native_interim':middle,'native_interim_to_source_indices':order,**r,'aliases':aliases,'all_single_exclusion_prices':prices,'stage_minima':minima}],'independent_closing_witness':{'record':w['record'],'counted_as_new_record':False,'closing':closing,'old_raw_start':old_start,'new_candidate_start':new_start,'complete_pairs':pairs},'headers':d['headers'],'limits':d['limits']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**r['summary']},indent=2))

if __name__=='__main__':main()
