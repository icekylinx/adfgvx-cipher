#!/usr/bin/env python3
"""Verify and optionally replay the failed p73-shaped component controls.
ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
"""
from pathlib import Path
import argparse,array,hashlib,json,math,struct,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,decrypt,encrypt,plaintext_domains
HERE=Path(__file__).resolve().parent


def load_six(path):
    with path.open('rb')as stream:
        assert stream.read(8)==b'G6HASH2\0'
        size,count,floor=struct.unpack('<IIf',stream.read(12))
        keys=array.array('I');keys.fromfile(stream,size)
        values=array.array('f');values.fromfile(stream,size)
    if sys.byteorder=='big':keys.byteswap();values.byteswap()
    assert size>0 and size&(size-1)==0
    def lookup(code):
        key=code+1;h=key
        h=((h^(h>>16))*0x7feb352d)&0xffffffff
        h=((h^(h>>15))*0x846ca68b)&0xffffffff
        h^=h>>16;slot=h&(size-1)
        while keys[slot]:
            if keys[slot]==key:return values[slot]
            slot=(slot+1)&(size-1)
        return floor
    return lookup


def score(pt,row,quad,six):
    four=0
    for i in range(len(pt)-3):
        code=0;wild=0
        for ch in pt[i:i+4]:code=37*code+(36 if ch=='?'else ALPHABET.index(ch));wild+=ch=='?'
        value=quad[code]
        if row['id']=='mixed_component':
            # The C implementation stores this normalized value as float32.
            value=struct.unpack('<f',struct.pack('<f',value-wild*math.log10(36)))[0]
        four+=value
    if row['id']=='quad_component':return four/(len(pt)-3)
    sixsum=0;count=0
    for i in range(len(pt)-5):
        gram=pt[i:i+6]
        if'?'in gram:continue
        code=0
        for ch in gram:code=36*code+ALPHABET.index(ch)
        sixsum+=six(code);count+=1
    w=row['recipe']['six_weight']
    return (1-w)*four/(len(pt)-3)+w*(sixsum/count if count else four/(len(pt)-3))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=HERE/'component_controls.json')
    p.add_argument('--quad',type=Path,required=True)
    p.add_argument('--six',type=Path,required=True)
    p.add_argument('--output',type=Path,default=HERE/'component_verification.json')
    p.add_argument('--replay',choices=['quad_component','mixed_component'])
    p.add_argument('--engine',type=Path)
    p.add_argument('--trace-output',type=Path)
    args=p.parse_args();data=json.loads(args.input.read_text())
    assert hashlib.sha256(args.quad.read_bytes()).hexdigest()==data['model_sha256']['quad37']
    assert hashlib.sha256(args.six.read_bytes()).hexdigest()==data['model_sha256']['six36']
    quad=array.array('f');quad.frombytes(args.quad.read_bytes())
    if sys.byteorder=='big':quad.byteswap()
    six=load_six(args.six);truth=data['fixture'];ct=truth['ciphertext'];n=len(ct);k=truth['width']
    assert encrypt(truth['body'],truth['ranks'],truth['square'])==truth['full_ciphertext']
    assert ct==truth['full_ciphertext'][:1]+'??'+truth['full_ciphertext'][3:]
    def pattern(ranks):return [n//k+(col<n%k)for col in sorted(range(k),key=lambda c:ranks[c])]
    checks=[]
    for row in data['runs']:
        assert hashlib.sha256((ROOT/row['engine_source']).read_bytes()).hexdigest()==row['source_sha256']
        best=row['best'];ranks=best['ranks'];square=best['square']
        assert len(square)==36 and set(square)==set(ALPHABET)
        assert sorted(ranks)==list(range(1,k+1))
        assert pattern(row['initial_ranks'])==pattern(ranks)==pattern(truth['ranks'])
        pt=decrypt(ct,ranks,square);assert pt==best['plaintexts'][0]
        ds=plaintext_domains(ct,ranks,square)
        witness=encrypt(''.join(d[0]for d in ds),ranks,square)
        assert all(a=='?'or a==b for a,b in zip(ct,witness))
        actual=score(pt,row,quad,six);assert abs(actual-best['score'])<1e-7
        planted=decrypt(ct,truth['ranks'],truth['square']);planted_score=score(planted,row,quad,six)
        checks.append(dict(id=row['id'],configured_proposal_slots=row['recipe']['restarts']*row['recipe']['iterations'],source_coordinates_preserved=176,
            supplied_only_correct_length_segmentation=True,true_plaintext_in_all_domains=all(ch in d for ch,d in zip(truth['body'],ds)),correct_singletons=sum(d==ch for ch,d in zip(truth['body'],ds)),singleton_positions=sum(len(d)==1 for d in ds),reported_score=actual,planted_score_under_same_objective=planted_score,reported_below_planted=actual<planted_score,
            interpretation='Optimizer did not recover the planted text; historical searches were not launched with this uncalibrated method.'))
        if args.replay==row['id']:
            assert args.engine and args.trace_output
            recipe=row['recipe']
            first=f'{args.quad.resolve()} '
            if row['id']=='mixed_component':first+=f'{args.six.resolve()} {recipe["six_weight"]} '
            first+=f'{k} {recipe["restarts"]} {recipe["iterations"]} {recipe["seed"]} 1\n'
            inp=first+row['initial_square']+'\n'+' '.join(map(str,row['initial_ranks']))+'\n'+ct+'\n'
            run=subprocess.run([str(args.engine.resolve())],input=inp,text=True,capture_output=True,check=True)
            assert hashlib.sha256(run.stdout.encode()).hexdigest()==row['trace_sha256']
            args.trace_output.write_text(run.stdout)
    result=dict(verified=True,checks=checks,historical_plaintexts_claimed=0)
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
