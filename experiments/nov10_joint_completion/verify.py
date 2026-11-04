#!/usr/bin/env python3
"""Replay the explicitly conditional Nov10–12 shared numeral completion."""
from pathlib import Path
from itertools import permutations
import hashlib
import json
import argparse
from datetime import date, timedelta

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'certificates.json'
INPUT=json.loads((HERE/'inputs.json').read_text())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verify',action='store_true')
args=parser.parse_args()
for path,digest in INPUT['dependencies'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest, path
CO='ADFGVX';AL=set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def read(path):return json.loads((ROOT/path).read_text())
def record(data,rid):return next(r for r in data['records'] if r['id']==rid)
def rows(data,field='source_rows'):return ''.join(''.join(data[field]).split())

K=next(k for k in read('data/keys.json')['keys'] if k['id']=='Nov10-12')
BASE=K['square'];RANKS=K['column_rank_order']
CELLS=[CO[i//6]+CO[i%6] for i,c in enumerate(BASE) if c=='?']
COMPLETIONS=[dict(zip(CELLS,values)) for values in permutations('56789')]
def square(assignment):
    result=list(BASE)
    for pair,c in assignment.items():result[CO.index(pair[0])*6+CO.index(pair[1])]=c
    return ''.join(result)

office=[a for a in COMPLETIONS if a['XX']=='6']
units=[a for a in office if {a['XA'],a['GF']}=={'7','9'}]
army_numbers=set(range(1,20))-{13,15,16}
army=[a for a in units if int('1'+a['XG']) in army_numbers]
decree_day=(date.fromisoformat(INPUT['historical_conditions']['first_mobilisation_gregorian_day'])-timedelta(days=1)).day
assert decree_day==9
dated=[a for a in army if a['XA']==str(decree_day)]
assert [len(COMPLETIONS),len(office),len(units),len(army),len(dated)]==[120,24,4,2,1]
SELECTED=dated[0];PRIOR=next(a for a in army if a['XA']=='7')
assert SELECTED=={'FD':'5','GF':'7','XA':'9','XG':'8','XX':'6'}
assert PRIOR=={'FD':'5','GF':'9','XA':'7','XG':'8','XX':'6'}

def order(n):
    w=len(RANKS);cols={};cur=0
    for c in sorted(range(w),key=lambda c:RANKS[c]):
        size=n//w+(c<n%w);cols[c]=list(range(cur,cur+size));cur+=size
    return [cols[c][r] for r in range((n+w-1)//w) for c in range(w) if r<len(cols[c])]

def decode(cipher,sq,mapping):
    assert len(cipher)%2==0
    indices=order(len(cipher));assert sorted(indices)==list(range(len(cipher)))
    ps=[];out=[]
    for p in range(len(cipher)//2):
        ix=indices[2*p:2*p+2];pair=''.join(cipher[i] for i in ix);domain=set()
        for a in range(6):
            for b in range(6):
                if pair[0] in (CO[a],'?') and pair[1] in (CO[b],'?'):
                    label=sq[a*6+b];domain.update(AL-set(sq) if label=='?' else label)
        out.append(next(iter(domain)) if len(domain)==1 else '?')
        ps.append({'position':p,'pair':pair,'source_indices':[mapping[i] for i in ix],'domain':''.join(sorted(domain))})
    return ''.join(out),ps

def rt(cipher,sq,mapping):
    c=cipher.replace('?','A');plain,_=decode(c,sq,mapping)
    assert '?' not in plain and set(sq)==AL
    inter=''.join(CO[sq.index(a)//6]+CO[sq.index(a)%6] for a in plain)
    encoded=''.join(inter[col::len(RANKS)] for col in sorted(range(len(RANKS)),key=lambda c:RANKS[c]))
    assert encoded==c

specs=[]
for rid in ['p172_B','p174_D']:
    file='experiments/p170_continuation/seifert_records.json';r=record(read(file),rid)
    specs.append({'id':rid,'inputs':file,'certificate':file,'literal':r['raw_source_compact'],
                  'cipher':r['analysis_ciphertext'],'raw_cipher':r['analysis_ciphertext'],
                  'mapping':list(range(len(r['analysis_ciphertext']))),'expected_previous':r['raw_plaintext'],
                  'expected_cost':[0,0,0,0],'previous_assignment':{}})

for pkg,rid,layer,cost,old in [
 ('corcovado_sale_terms','p173_A1','readable_candidate',[6,0,0,0],{'XX':'6'}),
 ('nov10_delegates_and_field_report','p175_A2','readable_candidate',[1,0,0,0],{}),
 ('romanian_ultimatum_companions','p175_C2','readable_candidate',[1,0,0,0],{}),
 ('turkish_tonnage','p177_B3','readable_candidate',[4,0,0,0],{'XX':'6'}),
 ('naval_armistice_order','p178_A5','edition',[2,0,0,0],{}),
 ('november_armistice_orders','p179_A','edition',[7,0,0,5],{}),
 ('november_armistice_orders','p179_B','edition',[1,0,0,0],{}),
 ('nov11_romanian_mobilization_report','p180_B2','readable_candidate',[4,1,4,0],{}),
 ('jaeger_accommodation_area','p183_F','readable_candidate',[1,2,0,0],{}),
]:
    ip=f'experiments/{pkg}/inputs.json';cp=f'experiments/{pkg}/certificates.json'
    i=read(ip);i=i['record'] if 'record' in i else record(i,rid)
    c=read(cp);c=record(c,rid) if 'records' in c else c
    literal=rows(i)
    mapping=c.get('model_to_source_indices',c.get('frame_to_source_indices',list(range(len(literal)))))
    raw=c.get('ciphertext',c.get('analysis_frame',c.get('framed_ciphertext')))
    if raw is None:raw=''.join('?' if j is None or literal[j] not in CO else literal[j] for j in mapping)
    specs.append({'id':rid,'inputs':ip,'certificate':cp,'literal':literal,'cipher':c[layer]['ciphertext'],
                  'raw_cipher':raw,'mapping':mapping,'expected_cost':cost,'previous_assignment':old})

records=[]
for spec in specs:
    source,cipher,mapping=spec['literal'],spec['cipher'],spec['mapping']
    assert len(cipher)==len(mapping)
    before,ps=decode(cipher,square(spec['previous_assignment']),mapping)
    if 'expected_previous' in spec:assert before==spec['expected_previous']
    after,_=decode(cipher,square(SELECTED),mapping)
    prior,_=decode(cipher,square(PRIOR),mapping)
    gains=[]
    for p,(a,b) in enumerate(zip(before,after)):
        if a==b:continue
        row=ps[p];assert a=='?' and b in '56789' and row['pair'] in CELLS
        assert all(i is not None and source[i]==v for i,v in zip(row['source_indices'],row['pair']))
        gains.append({**row,'selected':b,'prior_order':prior[p],
                      'tier':('existing_XX6_new_propagation' if row['pair']=='XX' else
                              'unit_set_and_army_number' if row['pair'] in ['FD','XG'] else 'mobilisation_date'),
                      'both_original_coordinates_observed':True})
    changes=[{'source_index':i,'from':source[i],'to':cipher[m]} for m,i in enumerate(mapping)
             if i is not None and source[i] in CO and source[i]!=cipher[m]]
    fills=[{'source_index':i,'literal':source[i],'to':cipher[m]} for m,i in enumerate(mapping)
           if i is not None and source[i] not in CO and cipher[m] in CO]
    added=[{'model_index':m,'to':cipher[m]} for m,i in enumerate(mapping) if i is None and cipher[m] in CO]
    excluded=sorted(set(range(len(source)))-set(mapping))
    assert [len(changes),len(fills),len(added),len(excluded)]==spec['expected_cost'],spec['id']
    raw_before,rp=decode(spec['raw_cipher'],BASE,mapping);raw_after,_=decode(spec['raw_cipher'],square(SELECTED),mapping)
    raw_effects=[{**rp[p],'selected':b,'before_context':raw_before[max(0,p-10):p+11],
                 'after_context':raw_after[max(0,p-10):p+11]}
                for p,(a,b) in enumerate(zip(raw_before,raw_after)) if a!=b]
    for complete in COMPLETIONS:rt(cipher,square(complete),mapping)
    records.append({'id':spec['id'],'inputs':spec['inputs'],'certificate':spec['certificate'],
                    'previous_assignment':spec['previous_assignment'],'previous_plaintext':before,
                    'selected_plaintext':after,'prior_order_plaintext':prior,'positions':len(after),
                    'fixed_before':len(before)-before.count('?'),'fixed_after':len(after)-after.count('?'),
                    'gains':gains,'old_observed_substitutions':changes,'old_printed_mask_fills':fills,
                    'old_added_coordinate_fills':added,'old_source_exclusions':excluded,
                    'raw_effects_including_adverse':raw_effects,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
                    'additional_observed_substitutions':0,'additional_source_fills':0})

prior=next(r for r in read('data/prior_readings.json')['messages'] if r['id']=='p176b')
v=prior['verified_variants'][0]['verification'];source=''.join(prior['raw_source_grouped'].split())
mapping=list(range(160))+[None]*20+list(range(160,220));cipher=v['corrected_ciphertext']
assert len(source)==220 and len(cipher)==240
assert all(i is None or cipher[m]==source[i] for m,i in enumerate(mapping))
baseline,ps=decode(cipher,BASE,mapping);assert baseline==v['raw_partial_plaintext']
anchor=[]
for p in [55,59,61]:
    row=ps[p];assert all(i is not None and source[i]==c for i,c in zip(row['source_indices'],row['pair']))
    anchor.append(row)
result={'schema':'nov10-joint-context-v1','selected_assignment':SELECTED,'selected_square':square(SELECTED),
        'prior_unit_order_assignment':PRIOR,'prior_unit_order_square':square(PRIOR),
        'completion_counts':{'all':120,'office_XX6':24,'unordered_unit_set':4,'army_number':2,'mobilisation_date':1},
        'p176b_prior_layer':{'previous_fixed':117,'positions':120,'retained_added_fills':20,'new_source_edits':0,
                           'native_anchors':anchor,'selected':decode(cipher,square(SELECTED),mapping)[0],
                           'prior_order':decode(cipher,square(PRIOR),mapping)[0],
                           'new_positions_counted':0,'credit':'Prinz and GPT-6 Astra, 2026-09-19; historical unit set remains attributed.'},
        'records':records,'new_fixed_positions':sum(len(r['gains']) for r in records),
        'new_physical_records':len(records),'additional_source_changes':0,'additional_source_fills':0,
        'conditions':['Retain the previous Marineamt XX=6 office-prefix interpretation.',
                      'The two p176b formation fields refer to 217 and 219, in an initially unspecified order, under the earlier 20-coordinate reconstruction.',
                      'The final native AOK1? in p183 F is an accurately received two-digit German army number, keeping the leading 1 numerical.',
                      'The p180 B2 mobilisation-order date refers accurately to decree 3179, signed one day before the first mobilisation day printed as 28 October / 10 November.'],
        'limits':['The layers do not prove the plaintext historically correct, nor erase old source repairs.',
                  'The former 217/219 order remains as a complete alternative when the mobilisation-date association is dropped.',
                  'Raw numeric letters inside damaged ordinary words remain visible; their existing source repairs are separately priced.',
                  'The p183 field 13711 remains literal; no separator or calendar date is substituted.']}
assert result['new_fixed_positions']==20 and result['new_physical_records']==11
result['complete_square_roundtrips']=120*len(records)
result['remaining_branches_before_date']=[{'assignment':a,'square':square(a)} for a in army]
for row in INPUT['case_displays']:
    case=(ROOT/row['path']).read_text()
    assert row['anchor'] in case, row['path']
    for literal in row['required_literals']:assert literal in case, (row['path'],literal)
if args.verify:
    assert json.loads(OUT.read_text())==result, 'certificate differs; inspect the change before regeneration'
else:
    OUT.write_text(json.dumps(result,indent=2)+'\n')
print('Assignment',SELECTED,'alternative',PRIOR)
for r in records:print(r['id'],r['fixed_before'],r['fixed_after'],r['positions'],[(g['pair'],g['selected'],g['source_indices']) for g in r['gains']])
print('Total',result['new_fixed_positions'],result['new_physical_records'])
print('PASS: 20 native labels in 11 physical sources; 1,320 full-square roundtrips; historical conditions remain explicit.')
