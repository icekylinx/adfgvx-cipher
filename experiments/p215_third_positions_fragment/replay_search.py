#!/usr/bin/env python3
"""Optional bounded p215 B3 mask-relocation replay; no binary models are saved.
Requires NumPy and the pinned external quad26 file. Uses the existing frozen
p212 probability recipe through p215 A's joint-marginal builder. Scores only
rank source frames; linguistic word repairs are verified separately.
icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os
HERE=Path(__file__).resolve().parent
CO='ADFGVX'; N=234

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def frames(kind):
    if kind=='runs':
        return [[[79,a],[95,b],[155,15-a-b]] for a in range(16) for b in range(16-a)]
    return [[[i,15]] for i in range(220) if i not in (79,95,155)]
def base_owners(insertions):
    add=dict(insertions); out=[]; uid=-1
    for i in range(220):
        for _ in range(add.get(i,0)): out.append(uid); uid-=1
        if i<219: out.append(i)
    assert len(out)==N and uid==-16
    return out
def relocate(base,move,destination):
    block=[x for x in base if move['start']<=x<move['start']+move['length']]
    rest=[x for x in base if x not in block]
    assert len(block)==move['length']
    return rest[:destination]+block+rest[destination:]
def check_owners(owners,source):
    assert sorted(x for x in owners if x>=0)==list(range(219))
    assert sorted(x for x in owners if x<0)==list(range(-15,0))
    assert [x for x in owners if x>=0 and source[x]!='?']==[i for i,c in enumerate(source) if c!='?']
def column_order(ranks):
    columns={}; offset=0
    for rank in range(1,23):
        col=ranks.index(rank); height=len(range(col,N,22))
        columns[col]=list(range(offset,offset+height)); offset+=height
    return [columns[c][row] for row in range(11) for c in range(22) if row<len(columns[c])]
def encode(pt,key):
    mid=''.join(CO[key['square'].index(c)//6]+CO[key['square'].index(c)%6] for c in pt)
    return ''.join(mid[c::22] for c in sorted(range(22),key=lambda c:key['column_rank_order'][c]))
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--quad26',required=True,type=Path)
    ap.add_argument('--repo',type=Path,default=HERE.parents[1])
    ap.add_argument('--output',type=Path)
    args=ap.parse_args(); root=args.repo.resolve()
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[name]='1'
    import numpy as np
    prov=json.loads((HERE/'search_provenance.json').read_text())
    for path,h in prov['pinned_repository_files'].items():
        assert digest(root/path)==h,('Pinned input changed',path)
    audit=json.loads((root/'data/reviews/source_gap_audit_20261103.json').read_text())
    record=next(x for x in audit['records'] if x['id']==prov['source_id'])
    source=''.join(''.join(record['source_rows']).split()).replace('-','?')
    assert hashlib.sha256(source.encode()).hexdigest()==prov['source_analysis_sha256']
    assert len(source)==219 and source.count('?')==19
    key=next(x for x in json.loads((root/'data/keys.json').read_text())['keys'] if x['id']=='Nov22-24')
    path=root/'experiments/p215_breslau_dispatch/replay_search.py'
    spec=importlib.util.spec_from_file_location('p215_a_replay',path); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    quad,mixture_hash=module.build_model(np,args.quad26,key,prov)
    order=np.array(column_order(key['column_rank_order']),dtype=np.int16)
    def decode(obs,owners):
        wire=''.join(obs[x] if x>=0 else '?' for x in owners)
        mid=''.join(wire[int(j)] for j in order)
        raw=''.join('?' if '?' in mid[i:i+2] else key['square'][CO.index(mid[i])*6+CO.index(mid[i+1])] for i in range(0,N,2))
        return raw,wire
    def scan(obs,kind):
        best=-float('inf'); winners=[]; count=0; baseline_best=-float('inf')
        lookup=np.array([CO.index(c) if c in CO else 6 for c in obs]+[6]*15,dtype=np.int16)
        for insertions in frames(kind):
            base=base_owners(insertions)
            for move in [None]+prov['moves']:
                maps=[base] if move is None else [relocate(base,move,d) for d in range(N-move['length']+1)]
                owners=np.array(maps,dtype=np.int16)
                ids=np.where(owners>=0,owners,219+(-owners-1));mid=lookup[ids][:,order]
                pattern=mid[:,::2]*7+mid[:,1::2]
                scores=quad[pattern[:,:-3],pattern[:,1:-2],pattern[:,2:-1],pattern[:,3:]].sum(axis=1,dtype=np.float64)
                count+=len(maps)
                if move is None: baseline_best=max(baseline_best,float(scores[0]))
                value=float(scores.max())
                if value<best-1e-9: continue
                if value>best+1e-9: best=value;winners=[]
                for d in np.flatnonzero(abs(scores-best)<1e-9):
                    mapping=maps[int(d)];check_owners(mapping,source);raw,wire=decode(obs,mapping)
                    # Independent rank-column decoding and a complete forward witness.
                    columns={};offset=0
                    for rank in range(1,23):
                        col=key['column_rank_order'].index(rank);length=len(range(col,N,22));columns[col]=wire[offset:offset+length];offset+=length
                    direct=''.join(columns[c][r] for r in range(11) for c in range(22) if r<len(columns[c]))
                    assert direct==''.join(wire[int(j)] for j in order)
                    full=direct.replace('?','A')
                    witness=''.join(key['square'][CO.index(full[i])*6+CO.index(full[i+1])] for i in range(0,N,2))
                    assert encode(witness,key)==wire.replace('?','A')
                    winners.append({'insertions':insertions,'move':None if move is None else move['name'],'destination':None if move is None else int(d),'raw':raw,'wire_sha256':hashlib.sha256(wire.encode()).hexdigest()})
        return {'frames':len(frames(kind)),'evaluations':count,'best_score':best,'winners':winners,'baseline_best_score':baseline_best}
    out={'schema':'adfgvx-p215-b3-discovery-replay-v1','mixture_sha256':mixture_hash,'joint49_sha256':prov['joint49_sha256'],'controls':[],'historical':{}}
    for control in prov['controls']:
        t=control['truth'];owners=relocate(base_owners(t['frame']['insertions']),t['move'],t['destination'])
        full=encode(control['plaintext'],key); observed=['?']*219
        for j,src in enumerate(owners):
            if src>=0 and source[src]!='?': observed[src]=full[j]
        observed=''.join(observed); assert observed==control['source']
        result=scan(observed,'runs')
        assert result['evaluations']==156672 and abs(result['best_score']-control['best']['score'])<1e-9
        assert any(x['raw']==control['best']['raw'] for x in result['winners'])
        for x in result['winners']:
            fixed=[(i,c) for i,c in enumerate(x['raw']) if c!='?']
            assert all(c==control['plaintext'][i] for i,c in fixed)
            assert len(fixed)==control['best_fixed_correct']
        out['controls'].append({'name':control['name'],'fixed_correct':control['best_fixed_correct'],'planted_raw_equal':control['same_raw'],'result':result})
    for kind,expected in prov['historical'].items():
        result=scan(source,kind)
        assert (result['frames'],result['evaluations'])==(expected['frames'],expected['evaluations'])
        assert abs(result['best_score']-expected['best_score'])<1e-9
        assert abs(result['baseline_best_score']-expected['baseline_best']['score'])<1e-9
        actual={(json.dumps(x['insertions']),x['move'],x['destination'],x['raw'])for x in result['winners']}
        frozen={(json.dumps(x['frame']['insertions']),None if x['move'] is None else x['move']['name'],x['destination'],x['raw'])for x in expected['best_candidates']}
        assert actual==frozen
        out['historical'][kind]=result
    out['limits']=prov['limits']; text=json.dumps(out,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    else: print(text,end='')
if __name__=='__main__': main()
