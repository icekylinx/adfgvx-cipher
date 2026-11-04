#!/usr/bin/env python3
"""Exact prices for the conditional p137 A5 governing clause and date marker.

icekylinx and GPT-6 Astra Pro. All indices are zero-based. This checker
reconstructs the source map independently of the earlier edition's verifier.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import plaintext_domains, encrypt, decrypt
CO='ADFGVX'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inverse_map(n,ranks):
    cols=sorted(range(len(ranks)),key=lambda i:ranks[i])
    order=[i for c in cols for i in range(c,n,len(ranks))]
    inv=[None]*n
    for j,i in enumerate(order):inv[i]=j
    assert sorted(inv)==list(range(n))
    return [inv[i:i+2] for i in range(0,n,2)]

def decode(wire,key,mapping):
    square=key['square'];pairs=inverse_map(len(wire),key['column_rank_order'])
    positions=[]
    for i,(a,b) in enumerate(pairs):
        rows=[CO.index(wire[a])]if wire[a]in CO else range(6)
        cols=[CO.index(wire[b])]if wire[b]in CO else range(6)
        domain=''.join(sorted(square[6*r+c]for r in rows for c in cols))
        positions.append(dict(plaintext_index=i,pair=wire[a]+wire[b],model_indices=[a,b],
                              source_indices=[mapping[a],mapping[b]],domain=domain))
    domains=[p['domain']for p in positions]
    raw=''.join(d if len(d)==1 else '?'for d in domains)
    assert domains==plaintext_domains(wire,key['column_rank_order'],square)
    assert raw==decrypt(wire,key['column_rank_order'],square)
    return dict(raw=raw,fixed_positions=sum(len(d)==1 for d in domains),positions=positions)

def apply(template,wire,key,mapping,literal):
    pairs=inverse_map(len(wire),key['column_rank_order']);out=list(wire)
    assert len(template)==len(pairs)
    for i,c in enumerate(template):
        if c=='?':continue
        cell=key['square'].index(c)
        for p,v in zip(pairs[i],[CO[cell//6],CO[cell%6]]):out[p]=v
    out=''.join(out);decoded=decode(out,key,mapping)
    edits=[]
    owner={p:i for i,pair in enumerate(pairs)for p in pair}
    for i,(a,b)in enumerate(zip(wire,out)):
        if a==b:continue
        kind='observed_substitution'if a in CO else ('missing_coordinate_fill'if mapping[i]is None else 'printed_mask_fill')
        edits.append(dict(kind=kind,model_index=i,source_index=mapping[i],
                          old=a,new=b,plaintext_index=owner[i]))
    counts={kind:sum(e['kind']==kind for e in edits)for kind in ['observed_substitution','printed_mask_fill','missing_coordinate_fill']}
    witness=''.join(p['domain'][0]for p in decoded['positions'])
    full=encrypt(witness,key['column_rank_order'],key['square'])
    assert all(a=='?'or a==b for a,b in zip(out,full))
    assert decrypt(full,key['column_rank_order'],key['square'])==witness
    return dict(template=template,wire=out,**decoded,edits=edits,cost=counts,
                mathematical_completion=dict(plaintext=witness,ciphertext=full,
                  historical_reading=False))

def source_frame(literal,first=0):
    last=37-first;s=literal.replace('-','?')
    return (s[:190]+'?'*first+s[190:]+'?'*last,
            list(range(190))+[None]*first+list(range(190,215))+[None]*last)

def replace_spans(text,spans):
    out=list(text)
    for r in spans:out[r['start']:r['start']+len(r['text'])]=r['text']
    return ''.join(out)

def run():
    inp=json.loads((HERE/'inputs.json').read_text())
    for p,digest in inp['dependencies'].items():assert sha(ROOT/p)==digest,p
    live=json.loads((ROOT/inp['source_input']).read_text())
    rec=next(r for r in live['records']if r['id']=='p137_A5');key=live['key']
    published=next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']if k['id']==key['id'])
    assert key['square']==published['square'] and key['column_rank_order']==published['column_rank_order']
    literal=''.join(re.sub(r'\{INTERFERENCE_[12]\}','', ''.join(rec['source_rows'])).split())
    assert len(literal)==215 and literal.count('-')==4
    prior=json.loads((ROOT/inp['staff_input']).read_text())
    assert prior['record_snapshot']==rec and prior['key_snapshot']==key
    primary=rec['readable_candidate'];staff=prior['proposal']['editorial_text']
    wire,mapping=source_frame(literal)
    raw=decode(wire,key,mapping)
    assert raw['raw']==rec['expected_raw'] and raw['fixed_positions']==85
    templates={'primary':primary,'staff':staff}
    templates['date_only']=replace_spans(primary,inp['date_marker'])
    templates['staff_and_date']=replace_spans(staff,inp['date_marker'])
    templates['governing_clause']=replace_spans(templates['staff_and_date'],inp['governing_clause'])
    layers={name:apply(txt,wire,key,mapping,literal)for name,txt in templates.items()}
    expected={'primary':(106,0,3,18),'staff':(116,3,3,28),'date_only':(108,0,3,20),
              'staff_and_date':(118,3,3,30),'governing_clause':(124,7,4,35)}
    for name,(fixed,obs,mask,missing)in expected.items():
        got=layers[name];assert got['fixed_positions']==fixed
        assert got['cost']==dict(observed_substitution=obs,printed_mask_fill=mask,missing_coordinate_fill=missing),(name,got['cost'])
    final=layers['governing_clause'];assert final['raw']==inp['expected_final_text']
    unknown=[p for p in final['positions']if len(p['domain'])>1]
    assert [p['plaintext_index']for p in unknown]==[75,125]
    old=layers['staff']['wire'];added=[]
    for i,(a,b)in enumerate(zip(old,final['wire'])):
        if a!=b:added.append(next(e for e in final['edits']if e['model_index']==i))
    assert sum(e['kind']=='observed_substitution'for e in added)==4
    assert sum(e['kind']=='missing_coordinate_fill'for e in added)==7
    assert sum(e['kind']=='printed_mask_fill'for e in added)==1
    newly_fixed=[]
    for a,b,base in zip(layers['staff']['positions'],final['positions'],raw['positions']):
        if len(a['domain'])>1 and len(b['domain'])==1:
            assert sum(c in CO for c in base['pair'])==1
            newly_fixed.append(dict(plaintext_index=b['plaintext_index'],character=b['domain'],
                                    observed_pair=base['pair'],source_indices=base['source_indices']))
    assert len(newly_fixed)==8
    # Separately retained F/V visual alternative from the earlier package.
    alt=list(literal);assert alt[68]=='F';alt[68]='V';alt=''.join(alt)
    altwire,altmap=source_frame(alt);alternate=apply(templates['governing_clause'],altwire,key,altmap,alt)
    assert alternate['cost']==dict(observed_substitution=6,printed_mask_fill=4,missing_coordinate_fill=35)
    # Full, finite allocation prices are conditional on the fixed proposed text.
    allcost=[]
    for first in range(38):
        w,mp=source_frame(literal,first);r=apply(templates['governing_clause'],w,key,mp,literal)
        allcost.append(dict(first_missing_run=first,last_missing_run=37-first,**r['cost']))
    best=min(r['observed_substitution']for r in allcost)
    assert [r['first_missing_run']for r in allcost if r['observed_substitution']==best]==[0]
    # This is a declared six-noun comparison, not an exhaustive language search.
    noun_prices=[]
    for word in inp['compared_nouns']:
        assert len(word)==10
        tmpl='?'*43+word+'?'*(126-53)
        r=apply(tmpl,wire,key,mapping,literal)
        noun_prices.append(dict(word=word,**r['cost'],edits=r['edits']))
    return dict(schema='adfgvx-p137-governing-clause-certificate-v1',authors=inp['authors'],
                input_sha256=sha(HERE/'inputs.json'),raw=raw,layers=layers,
                incremental_edits_from_staff=added,newly_fixed_positions=newly_fixed,
                unresolved_positions=unknown,visual_V_alternative=alternate,
                all_38_interference_allocation_costs=allcost,declared_noun_comparison=noun_prices,
                summary=dict(physical_bodies_added=0,old_staff_fixed=116,new_date_fixed=118,
                             new_governing_fixed=124,total_positions=126,
                             additional_observed_substitutions=4,additional_printed_mask_fills=1,additional_missing_fills=7,
                             primary_source_transcription_changed=False,key_changed=False),
                limits=inp['limits'])

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
    r=run();out=HERE/'certificates.json'
    if a.verify:assert r==json.loads(out.read_text())
    else:out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(dict(verified=a.verify,**r['summary']),indent=2))
if __name__=='__main__':main()
