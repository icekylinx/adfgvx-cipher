"""Refine the five-symbol p198 loss model with full coordinate-domain scores.

Every observed symbol is preserved. Four independently published permutation
families are tested; the substitution square is unknown and bijective. Only
five-symbol-group boundary gaps are covered in this run.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import time
import argparse

from cipher import decrypt, untranspose, load_data

ROOT=Path(__file__).resolve().parent.parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--reverse',action='store_true',help='Resume unfinished cases in reverse order')
    args=parser.parse_args()
    messages,_=load_data();ct=messages['p198']['ciphertext'];assert len(ct)==165
    keys={x['id']:x for x in json.loads((ROOT.parent/'source_audit/audited_keys.json').read_text())['keys']}
    output=ROOT/'results/p198_domain_refinement';output.mkdir(exist_ok=True)
    model=ROOT/'data/military_models'
    records=[]
    names=['CHI-Nov13','Nov13-15b','Nov13-15a','Nov28-Dec1']
    gaps=list(range(0,166,5))
    if args.reverse:names.reverse();gaps.reverse()
    for name in names:
        ranks=keys[name]['column_rank_order']
        for gap in gaps:
            label=f'p198__{name}__gap{gap:03d}';dest=output/(label+'.json')
            if dest.exists():records.append(json.loads(dest.read_text()));continue
            restored=ct[:gap]+'?????'+ct[gap:];interim=untranspose(restored,ranks)
            seed=int.from_bytes(hashlib.sha256(label.encode()).digest()[:8],'little')
            cmd=[str(ROOT/'bin/marginal_subsolve6'),str(model/'german_military36_quad.bin'),
                 str(model/'german_military36_sixgram.bin'),'0.7',interim,'120','100000',str(seed)]
            prior=ROOT/'results/p198_unknown_square_missing_group'/(label+'.json')
            if prior.exists():cmd.append(json.loads(prior.read_text())['best']['square'])
            start=time.time();result=subprocess.run(cmd,capture_output=True,text=True,check=True)
            (output/(label+'.jsonl')).write_text(result.stdout)
            best=json.loads(result.stdout.splitlines()[-1])
            assert decrypt(restored,ranks,best['square'])==best['plaintext']
            record={'id':'p198','key_id':name,'ranks':ranks,'gap_position':gap,'gap_length':5,
                    'received_ciphertext':ct,'ciphertext_with_gap':restored,'best':best,
                    'restarts':120,'iterations_per_restart':100000,'seed':seed,
                    'sixgram_weight':.7,'models':'data/military_models','seconds':time.time()-start,
                    'known_coordinate_changes':0,'classification':'unvalidated_search_candidate'}
            dest.write_text(json.dumps(record,indent=2));records.append(record)
            print(json.dumps({'completed':len(records),'total':136,'key':name,'gap':gap,
                              'score':best['score'],'seconds':record['seconds']}),flush=True)
    (output/'SUMMARY.json').write_text(json.dumps({'cases':len(records),
        'scope':'Four fixed rank families, unknown square, one five-symbol gap at every group boundary.',
        'top_candidates':sorted(records,key=lambda x:x['best']['score'],reverse=True)[:30]},indent=2))


if __name__=='__main__':main()
