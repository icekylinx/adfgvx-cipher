#!/usr/bin/env python3
"""Exhaust every insertion boundary for p198 D + neighboring literal XAXVV.
ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
"""
from pathlib import Path
import argparse,array,hashlib,json,math,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,decrypt,plaintext_domains,untranspose
HERE=Path(__file__).resolve().parent
MODEL_SHA='2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e'


def evaluate(inputs,model):
    ct=inputs['ciphertext'];group=inputs['inserted_group'];records=[]
    assert len(ct)==165 and set(ct)<=set('ADFGVX') and group=='XAXVV'
    for key in inputs['keys']:
        assert sorted(key['ranks'])==list(range(1,len(key['ranks'])+1))
        for gap in range(len(ct)+1):
            trial=ct[:gap]+group+ct[gap:]
            assert trial[:gap]+trial[gap+5:]==ct
            pt=decrypt(trial,key['ranks'],key['square']);domains=plaintext_domains(trial,key['ranks'],key['square'])
            assert len(pt)==85 and all(p=='?' or p==d for p,d in zip(pt,domains))
            stream=untranspose(trial,key['ranks'])
            roundtrip=''.join(stream[col::len(key['ranks'])] for col in sorted(range(len(key['ranks'])),key=lambda c:key['ranks'][c]))
            assert roundtrip==trial
            score=0
            for i in range(len(pt)-3):
                code=0;wild=0
                for ch in pt[i:i+4]:code=37*code+(36 if ch=='?' else ALPHABET.index(ch));wild+=ch=='?'
                score+=model[code]-wild*math.log10(36)
            records.append(dict(key_id=key['id'],gap_before_source_0based=gap,score=score/(len(pt)-3),partial_plaintext=pt))
    return records


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',type=Path,default=Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin'))
    p.add_argument('--output',type=Path,default=HERE/'direct_transfer_result.json')
    p.add_argument('--replay',type=Path)
    p.add_argument('--all-records',type=Path)
    args=p.parse_args()
    assert hashlib.sha256(args.model.read_bytes()).hexdigest()==MODEL_SHA
    model=array.array('f');model.frombytes(args.model.read_bytes())
    if sys.byteorder=='big':model.byteswap()
    if args.replay:original=json.loads(args.replay.read_text());inputs=original['inputs']
    else:
        keys=json.loads((ROOT/'data/keys.json').read_text())['keys'];message=next(m for m in json.loads((ROOT/'data/messages.json').read_text())['messages']if m['id']=='p198')
        inputs=dict(target='p198 section D / CHI-170',ciphertext=message['transcript']['analysis_ciphertext'],inserted_group='XAXVV',group_source='p198 section E, either identical adjacent copy at source15..19 or20..24',keys=[dict(id=k['id'],square=k['square'],ranks=k['column_rank_order'])for k in keys if k['square'].count('?')<36])
    records=evaluate(inputs,model)
    ranked=sorted(records,key=lambda r:(-r['score'],r['key_id'],r['gap_before_source_0based']))
    result=dict(project='ADFGVX Cipher',review_credit='icekylinx and GPT-6 Astra Pro',inputs=inputs,
        model_sha256=MODEL_SHA,score_definition='Mean quadgram log probability; each whole-letter wildcard is normalized by36. Known half-coordinate domains remain available for exact arithmetic but are not used in ranking.',
        evaluated_cases=len(records),known_key_hypotheses=len(inputs['keys']),tested_insertion_boundaries=166,
        all_165_source_coordinates_preserved=True,exact_coordinate_roundtrips_verified=len(records),
        canonical_all_records_sha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        canonical_arithmetic_records_sha256=hashlib.sha256(json.dumps([{k:v for k,v in r.items() if k!='score'} for r in records],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        top_twenty=ranked[:20],best_by_key=[next(r for r in ranked if r['key_id']==k['id'])for k in inputs['keys']],
        accepted_historical_plaintexts=0,
        limitation='Exhaustive only for these fixed ranks and partial squares. The five extra E coordinates may be independent dittography rather than a displaced D group; this test does not establish transfer.')
    if args.replay:assert result==original
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if args.all_records:args.all_records.write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','top_twenty','best_by_key']},indent=2))

if __name__=='__main__':main()
