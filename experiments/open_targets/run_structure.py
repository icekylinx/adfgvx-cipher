#!/usr/bin/env python3
"""Run or import exact gap/segmentation screens and bounded pair-order refinement.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
The initial monogram matching is exact within every enumerated geometry.
Keeping1024 seeds and refining their pair orders is a bounded approximation.
"""
from pathlib import Path
import argparse,array,hashlib,json,math,subprocess,sys,time
from run_gap import fixtures,ROOT,digest
from verify_structural import monogram_score
from source_fit import complete_square_for_plaintext
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,decrypt,plaintext_domains
HERE=Path(__file__).resolve().parent
MODEL_SHA='2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e'


def verification(record,model,prior):
    case=record['case'];ct=case['ciphertext'];width=case['width'];remainder=(len(ct)+5)%width
    assert width in [14,16,18,20] and case['gap_size']==5
    assert record['segmentation_summary']['enumerated_gap_segmentations']==(len(ct)+1)*math.comb(width,remainder)
    for row in record['segmentation_leaders']:
        gap=row['gap_before_source_0based'];padded=ct[:gap]+'?'*5+ct[gap:]
        assert sorted(row['ranks'])==list(range(1,width+1))
        assert row['long_mask']==sum(1<<(rank-1)for rank in row['ranks'][:remainder])
        assert abs(monogram_score(padded,row['ranks'],case['partial_square'],prior)-row['monogram_score'])<1e-8
    for row in record['refined_candidates']:
        gap=row['gap_before_source_0based'];padded=ct[:gap]+'?'*5+ct[gap:]
        pt=decrypt(padded,row['ranks'],case['partial_square'])
        assert pt==row['partial_plaintext']
        score=0
        for i in range(len(pt)-3):
            code=0;wild=0
            for ch in pt[i:i+4]:code=37*code+(36 if ch=='?' else ALPHABET.index(ch));wild+=ch=='?'
            score+=model[code]-wild*math.log10(36)
        score/=len(pt)-3
        assert abs(score-row['score'])<2e-6
    result=dict(source_coordinates_preserved=165,segmentation_classes_checked=record['segmentation_summary']['enumerated_gap_segmentations'],retained_seed_count=record['segmentation_summary']['retained'],retained_refinements_verified=len(record['refined_candidates']),accepted_historical_plaintext=False)
    if 'evaluation_only' in case:
        truth=case['evaluation_only'];best=record['refined_candidates'][0];g=best['gap_before_source_0based'];padded=ct[:g]+'?'*5+ct[g:]
        domains=plaintext_domains(padded,best['ranks'],case['partial_square'])
        result['control']=dict(exact_ranks=best['ranks']==truth['ranks'],recovered_gap=g,planted_gap=truth['gap_before_source_0based'],truth_in_all_positionwise_domains=all(ch in d for ch,d in zip(truth['plaintext'],domains)),correct_singletons=sum(d==ch for ch,d in zip(truth['plaintext'],domains)),singleton_positions=sum(len(d)==1 for d in domains),global_truth_feasibility=complete_square_for_plaintext(padded,best['ranks'],case['partial_square'],truth['plaintext']),better_monogram_geometries_than_truth=record['segmentation_summary']['strictly_better_geometries_than_truth'],tied_monogram_geometries_with_truth=record['segmentation_summary']['tied_geometries_with_truth'])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--segment-engine',type=Path,default=HERE/'bin/segment_gap')
    p.add_argument('--refine-engine',type=Path,default=HERE/'bin/refine_segments')
    p.add_argument('--model',type=Path,default=Path('/tmp/adfgvx-models/german_military37_quad_marginal.bin'))
    p.add_argument('--seeds',type=Path,default=Path('/tmp/adfgvx-segment-results'))
    p.add_argument('--refined',type=Path,default=Path('/tmp/adfgvx-refine-results'))
    p.add_argument('--run',action='store_true',help='Generate missing traces before importing')
    p.add_argument('--output',type=Path,default=HERE/'structure_results.json')
    p.add_argument('--only',default='*')
    p.add_argument('--verify',type=Path)
    args=p.parse_args();import fnmatch
    assert digest(args.model)==MODEL_SHA
    model=array.array('f');model.frombytes(args.model.read_bytes())
    if sys.byteorder=='big':model.byteswap()
    monopath=ROOT/'experiments/joint_search/models/military_monograms.txt';monotext=monopath.read_text()
    prior=dict(zip(ALPHABET,map(float,monotext.split())));norm=sum(prior.values());prior={ch:v/norm for ch,v in prior.items()}
    if args.verify:
        data=json.loads(args.verify.read_text())
        for row in data['records']:assert verification(row,model,prior)==row['verification']
        print(json.dumps(dict(verified=True,cases=len(data['records']),historical=sum('evaluation_only'not in r['case']for r in data['records']),controls=sum('evaluation_only'in r['case']for r in data['records'])),indent=2));return
    args.seeds.mkdir(parents=True,exist_ok=True);args.refined.mkdir(parents=True,exist_ok=True)
    records=[]
    for case in fixtures():
        if case['width']not in [14,16,18,20] or not fnmatch.fnmatch(case['id'],args.only):continue
        sp=args.seeds/(case['id']+'.jsonl');rp=args.refined/(case['id']+'.jsonl')
        truth=case.get('evaluation_only',{})
        inp=f'{case["width"]} 5 1 1024\n'+case['partial_square']+'\n'+monotext+'\n'+case['ciphertext']+'\n'+str(truth.get('gap_before_source_0based',-1))+'\n'+' '.join(map(str,truth.get('ranks',[0]*case['width'])))+'\n'
        if args.run and not sp.exists():
            with sp.open('w')as f:subprocess.run([str(args.segment_engine.resolve())],input=inp,text=True,stdout=f,check=True)
        seeds=[json.loads(line)for line in sp.read_text().splitlines()];ss=seeds.pop();assert ss['kind']=='summary'
        refine_inp=f'{args.model.resolve()} {case["width"]} 5 20 2\n'+case['partial_square']+'\n'+case['ciphertext']+'\n'+str(len(seeds))+'\n'+''.join(str(r['gap_before_source_0based'])+' '+' '.join(map(str,r['ranks']))+'\n'for r in seeds)
        if args.run and not rp.exists():
            with rp.open('w')as f:subprocess.run([str(args.refine_engine.resolve())],input=refine_inp,text=True,stdout=f,check=True)
        refined=[json.loads(line)for line in rp.read_text().splitlines()];rs=refined.pop();assert rs['kind']=='summary'
        record=dict(case=case,segmentation_summary=ss,segmentation_leaders=seeds[:10],all_segment_candidates_sha256=hashlib.sha256(json.dumps(seeds,sort_keys=True,separators=(',',':')).encode()).hexdigest(),refinement_summary=rs,refined_candidates=refined)
        record['verification']=verification(record,model,prior);records.append(record)
    result=dict(project='ADFGVX Cipher',review_credit='icekylinx and GPT-6 Astra Pro',model_sha256=MODEL_SHA,monogram_sha256=digest(monopath),segment_source_sha256=digest(HERE/'segment_gap.c'),refine_source_sha256=digest(HERE/'refine_segments.c'),records=records,accepted_historical_plaintexts=0,limitation='Exact geometric enumeration with an exact monogram-matching relaxation, followed by bounded language refinement; failed control ranks remain recorded.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(records=len(records),historical_cases=sum('evaluation_only'not in r['case']for r in records),total_historical_gap_segmentations=sum(r['segmentation_summary']['enumerated_gap_segmentations']for r in records if'evaluation_only'not in r['case']),controls=[dict(id=r['case']['id'],evaluation=r['verification']['control'])for r in records if'evaluation_only'in r['case']]),indent=2))

if __name__=='__main__':main()
