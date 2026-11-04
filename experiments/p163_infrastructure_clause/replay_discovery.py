#!/usr/bin/env python3
"""Replay retained A16 discovery diagnostics with the hash-pinned word model.

These scores do not prove a historical reading or choose the frame length.
icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,plaintext_domains

AL='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lexicon',type=Path,required=True)
    args=parser.parse_args()
    data=json.loads((HERE/'inputs.json').read_text())
    frozen=json.loads((HERE/'discovery.json').read_text())
    assert hashlib.sha256(args.lexicon.read_bytes()).hexdigest()==frozen['lexicon']['sha256']
    assert hashlib.sha256((HERE/'domain_words.cpp').read_bytes()).hexdigest()==frozen['solver_source_sha256']
    source=''.join(''.join(data['records'][0]['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest()==frozen['received_source_sha256']
    square=frozen['complete_square_used'];ranks=frozen['ranks']
    assert len(set(square))==36 and ranks==data['key']['column_rank_order']
    assert all(a=='?' or a==b for a,b in zip(data['key']['square'],square))
    base=json.loads((ROOT/data['baseline_inputs']['path']).read_text())
    a14=next(r for r in base['records'] if r['id']=='p163_A14')
    control=''.join(''.join(a14['source_rows']).split()).replace('-','?')
    rng=random.Random(frozen['shuffle_seed'])
    cases=frozen['selected_replay_frames']
    lines=[]
    for case in cases:
        wire=case['wire']
        assert len(wire)==case['n'] and wire[:case['prefix']]=='?'*case['prefix']
        if case['kind']=='target':
            assert wire[case['prefix']:]==source
        elif case['kind']=='native_control':
            assert wire=='?'*123+control[-121:]
            assert case['full_native_raw']==decrypt(control,ranks,square)
        else:
            chars=list(source);rng.shuffle(chars)
            assert wire=='?'*163+''.join(chars)
        masks=[sum(1<<AL.index(c) for c in d) for d in plaintext_domains(wire,ranks,square)]
        lines.append(f"{case['id']} {len(masks)} "+' '.join(map(str,masks)))
    with tempfile.TemporaryDirectory(prefix='adfgvx-a16-discovery-') as temp:
        work=Path(temp);binary=work/'domain_words';frames=work/'frames.txt'
        frames.write_text('\n'.join(lines)+'\n')
        subprocess.run(['g++','-O3','-std=c++17','-o',str(binary),str(HERE/'domain_words.cpp')],check=True)
        p=frozen['parameters']
        output=subprocess.check_output([str(binary),str(args.lexicon.resolve()),str(frames),
            str(p['fallback_score']),str(p['bigram_weight']),str(p['separator_X_score'])],text=True)
    result=[json.loads(line) for line in output.splitlines()]
    assert len(result)==len(cases)==35
    for actual,expected in zip(result,cases):
        assert actual['id']==expected['id'] and actual['feasible']
        assert abs(actual['score']-expected['expected_score'])<1e-8
        assert actual['fallback_letters']==expected['expected_fallback_letters']
        if 'diagnostic_plaintext' in expected:
            assert actual['plaintext']==expected['diagnostic_plaintext']
    by_id={r['id']:r for r in result}
    truth=next(r['full_native_raw'] for r in cases if r['kind']=='native_control')
    predicted=by_id['control_A14_true244']['plaintext']
    agreement=sum(a==b for a,b in zip(truth,predicted) if a!='?')
    assert agreement==99 and sum(a!='?' for a in truth)==121
    shuffled=[r['score'] for r in result if r['id'].startswith('shuffle')]
    assert len(shuffled)==32
    print(json.dumps({'retained_diagnostic_frames_replayed':len(result),
        'target_284_score':by_id['target_284_163']['score'],
        'target_286_score':by_id['target_286_165']['score'],
        'best_matched_shuffle_284_score':max(shuffled),
        'native_A14_control_agreement_with_raw_fixed_letters':agreement,
        'native_A14_raw_fixed_letters':121,
        'accepted_full_language_model_completions':0,
        'limit':'A source-compatible language-model completion is not a historical proof. These fixed-geometry controls do not calibrate all geometry and wording choices.'},indent=2))


if __name__=='__main__':
    main()
