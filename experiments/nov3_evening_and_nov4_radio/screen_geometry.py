#!/usr/bin/env python3
"""Optional exhaustive p112 C language screen with fresh synthetic controls.

NumPy and the pinned external model are needed only for this optional check.
Prepared by icekylinx and GPT-6 Astra Pro.
"""
import argparse,json,runpy
from pathlib import Path
HERE=Path(__file__).resolve().parent
V=runpy.run_path(str(HERE/'verify.py'))
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?'

def equivalent(a,b):
    if isinstance(a,float)or isinstance(b,float):
        return isinstance(a,(float,int))and isinstance(b,(float,int))and abs(a-b)<=1e-12
    if isinstance(a,dict):return isinstance(b,dict)and a.keys()==b.keys()and all(equivalent(a[k],b[k])for k in a)
    if isinstance(a,list):return isinstance(b,list)and len(a)==len(b)and all(equivalent(x,y)for x,y in zip(a,b))
    return a==b

def calculate(source,key,model,truth=None):
    import numpy as np
    co='ADFGVX';lookup=np.full(256,6,dtype=np.uint8)
    for i,c in enumerate(co):lookup[ord(c)]=i
    pairs=np.full((7,7),36,dtype=np.uint8)
    for r in range(6):
        for c in range(6):pairs[r,c]=ALPHABET.index(key['square'][6*r+c])
    order=V['permutation'](122,key['column_rank_order']);gaps=[(a,b)for a in range(113)for b in range(a,113)]
    expected=lookup[np.frombuffer(V['encode'](truth,key).encode(),dtype=np.uint8)]if truth else None
    all_params=[];all_scores=[];compatible=[];top=[]
    for g1 in range(5,10):
        for g2 in range(19,24):
            base=source[:g1]+'?'+source[g1:g2]+'?'+source[g2:]
            strings=[base[:a]+'?'*5+base[a:b]+'?'*5+base[b:]for a,b in gaps]
            tx=lookup[np.frombuffer(''.join(strings).encode(),dtype=np.uint8)].reshape(len(gaps),122);middle=tx[:,order]
            p=pairs[middle[:,::2],middle[:,1::2]].astype(np.int64)
            codes=((p[:,:-3]*37+p[:,1:-2])*37+p[:,2:-1])*37+p[:,3:];q=(p==36).astype(int)
            scores=(model[codes]-(q[:,:-3]+q[:,1:-2]+q[:,2:-1]+q[:,3:])*np.log10(36)).mean(axis=1)
            for i in np.argsort(-scores,kind='stable')[:20]:
                a,b=gaps[int(i)];top.append({'parameters':[g1,g2,a,b],'normalized_marginal_mean':float(scores[i]),'raw':''.join(ALPHABET[x]for x in p[i]),'fixed_positions':int(np.sum(p[i]!=36))})
            if expected is not None:
                counts=np.sum((tx!=6)&(tx!=expected),axis=1);compatible.extend([len(all_params)+int(i)for i in np.flatnonzero(counts==0)])
            all_params.extend([[g1,g2,a,b]for a,b in gaps]);all_scores.extend(float(x)for x in scores)
    assert len(all_params)==161025
    top.sort(key=lambda r:(-r['normalized_marginal_mean'],r['parameters']))
    result={'actual_parameter_configurations':len(all_params),'top20':top[:20],'score_definition':'mean(model_quad - number_of_unknown_symbols_in_quad * log10(36)); all58 tetragrams included','known_plaintext_used_to_rank':False}
    if truth is not None:
        order=sorted(range(len(all_scores)),key=lambda i:(-all_scores[i],all_params[i]));rank={i:j+1 for j,i in enumerate(order)};assert compatible
        result['truth_compatible_layouts']=[{'parameters':all_params[i],'rank':rank[i],'score':all_scores[i]}for i in compatible]
        result['best_truth_compatible_rank']=min(rank[i]for i in compatible)
    return result

def build(model_path):
    import numpy as np
    data=json.loads((HERE/'screen_inputs.json').read_text());assert V['sha'](model_path)==data['model_sha256'];model=np.memmap(model_path,dtype='<f4',mode='r');assert model.size==37**4
    inputs=json.loads((HERE/'inputs.json').read_text());record=next(r for r in inputs['records']if r['id']=='p112_C');key=next(k for k in inputs['keys']if k['id']==record['key_id'])
    controls=[];wanted={tuple(c['parameters'])for c in data['fresh_truth_controls']};maps={}
    for params,mapping in V['local_maps']():
        if params in wanted:maps[params]=mapping
    for control in data['fresh_truth_controls']:
        text=control['newly_composed_nonhistorical_plaintext'];assert len(text)==61;full=V['encode'](text,key);mapping=maps[tuple(control['parameters'])];source=['?']*110
        for j,i in enumerate(mapping):
            if i is not None:source[i]=full[j]
        source=''.join(source);assert '?'not in source;result=calculate(source,key,model,text)
        assert any(r['parameters']==control['parameters']for r in result['truth_compatible_layouts'])
        controls.append({'id':control['id'],'plaintext':text,'complete_ciphertext':full,'source_after_declared_losses':source,'true_parameters':control['parameters'],**result})
    target=calculate(record['analysis_source'],key,model);rejected=[]
    for keyid in ['Nov4-6','Nov1-3']:
        k=next(k for k in inputs['keys']if k['id']==keyid)
        for g1 in range(5,10):
            for g2 in range(19,24):
                s=record['analysis_source'];frame=s[:g1]+'?'+s[g1:g2]+'?'+s[g2:];rejected.append({'key':keyid,'short_group_gaps':[g1,g2],'raw':V['inspect'](frame,k)['plaintext']})
    return {'schema':'adfgvx-p112-C-complete-language-screen-v1','authors':inputs['authors'],'screen_inputs_sha256':V['sha'](HERE/'screen_inputs.json'),'source_inputs_sha256':V['sha'](HERE/'inputs.json'),'model_sha256':data['model_sha256'],'target':target,'fresh_truth_controls':controls,'total_122_slot_configuration_evaluations':161025*(1+len(controls)),'short_group_only_112_slot_diagnostics':rejected,'top_rank_truth_compatible_control_count':sum(c['best_truth_compatible_rank']==1 for c in controls),'limits':['Four newly composed controls cover only this declared family and one unchanged key; they are not a historical probability.','The top-ranked layout is a screening lead. Fixed-candidate alignment minima and the broader arbitrary-loss family are verified separately.','The112-slot diagnostics do not establish impossibility; their visible outputs remain unaccepted.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--book-model',type=Path,required=True);p.add_argument('--verify',action='store_true');a=p.parse_args();result=build(a.book_model);out=HERE/'language_screen.json'
    if a.verify:assert equivalent(result,json.loads(out.read_text()))
    else:out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,'total_122_slot_configuration_evaluations':result['total_122_slot_configuration_evaluations'],'target_best':result['target']['top20'][0],'control_best_truth_ranks':[c['best_truth_compatible_rank']for c in result['fresh_truth_controls']]},indent=2))
if __name__=='__main__':main()
