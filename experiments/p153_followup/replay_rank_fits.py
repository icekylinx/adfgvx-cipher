"""Replay the bounded new-rank fits with a canonical exact-domain engine."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
SYMBOLS='ADFGVX'


def untranspose(ciphertext,ranks):
    if len(ciphertext)%2 or sorted(ranks)!=list(range(1,len(ranks)+1)):
        raise ValueError('Even ciphertext and a complete rank permutation are required')
    order=[position for col in sorted(range(len(ranks)),key=ranks.__getitem__)
           for position in range(col,len(ciphertext),len(ranks))]
    result=['']*len(ciphertext)
    for char,position in zip(ciphertext,order):result[position]=char
    return ''.join(result)


def decode(interim,square):
    return ''.join('?' if '?' in interim[i:i+2] else square[
        6*SYMBOLS.index(interim[i])+SYMBOLS.index(interim[i+1])]
        for i in range(0,len(interim),2))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--solver',type=Path,required=True)
    parser.add_argument('--quad',type=Path,required=True)
    parser.add_argument('--six',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--case',help='Optional exact case label, such as p73 or p198_gap130')
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args()
    if args.workers<1:parser.error('workers must be positive')
    metadata=json.loads((HERE/'source_metadata.json').read_text())
    for path,expected in [(args.quad,metadata['quad_model_sha256']),(args.six,metadata['sixgram_model_sha256'])]:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            parser.error('Model hash differs from the published experiment')
    cases=json.loads((HERE/'new_rank_cases.json').read_text())
    selected=[row for row in cases if args.case is None or row['label']==args.case]
    if not selected:parser.error('No matching case')
    args.output.mkdir(parents=True,exist_ok=True)
    def run(case):
        interim=untranspose(case['analysis_ciphertext'],case['ranks'])
        result=subprocess.run([str(args.solver.resolve()),str(args.quad.resolve()),str(args.six.resolve()),
            str(case['sixgram_weight']),interim,str(case['restarts']),str(case['iterations_per_restart']),
            str(case['seed']),metadata['mutable_initial_square']],capture_output=True,text=True,check=True)
        (args.output/(case['label']+'.jsonl')).write_text(result.stdout)
        best=max((json.loads(line) for line in result.stdout.splitlines()),key=lambda row:row['score'])
        assert best['plaintexts']==[decode(interim,best['square'])]
        record=dict(label=case['label'],best=best,independent_decryption_check=True,
                    scope='Unvalidated search output, not an accepted historical plaintext.')
        (args.output/(case['label']+'.json')).write_text(json.dumps(record,indent=2))
        return record
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records=list(pool.map(run,selected))
    print(json.dumps({'completed':len(records),'output':str(args.output)}))


if __name__=='__main__':main()
