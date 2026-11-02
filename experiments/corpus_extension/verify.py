#!/usr/bin/env python3
"""Verify source editions, repeated-copy alignment and two local damage models.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The independently indexed inverse is compared with the project's cipher
implementation. Human-readable proposals are separately costed, never inputs
to the raw-source decryption. Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

C = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(text):
    return ''.join(c if c in C else '?' for c in text)


def permutation(length, ranks):
    """For each untransposed coordinate, give its ciphertext position."""
    w = len(ranks)
    assert sorted(ranks) == list(range(1, w + 1))
    heights = [length // w + (i < length % w) for i in range(w)]
    starts = [sum(heights[j] for j in range(w) if ranks[j] < ranks[i]) for i in range(w)]
    result = [starts[i % w] + i // w for i in range(length)]
    assert sorted(result) == list(range(length))
    return result


def inverse(cipher, key, source_map=None):
    assert len(cipher) % 2 == 0
    square, ranks = key['square'], key['column_rank_order']
    assert len(square) == 36 and len(set(square)) == 36 and '?' not in square
    indices = permutation(len(cipher), ranks)
    middle = ''.join(cipher[i] for i in indices)
    assert middle == untranspose(cipher, ranks)
    positions = []
    for p in range(len(cipher) // 2):
        pair = middle[2*p:2*p+2]
        cells = [6*a+b for a in range(6) for b in range(6)
                 if pair[0] in ('?', C[a]) and pair[1] in ('?', C[b])]
        domain = ''.join(sorted(square[i] for i in cells))
        pair_indices = indices[2*p:2*p+2]
        positions.append({'index':p, 'model_indices':pair_indices,
                          'original_source_indices': [source_map[i] for i in pair_indices]
                          if source_map is not None else pair_indices,
                          'pair':pair, 'domain':domain,
                          'raw':domain if len(domain)==1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    restored = [None] * len(cipher)
    for ch,i in zip(middle,indices): restored[i]=ch
    assert ''.join(restored)==cipher
    return {'raw':raw, 'fixed_positions':sum(p['raw']!='?' for p in positions),
            'positions':positions}


def source_map(record, deletion=None):
    mapping = list(range(record['source_slots']))
    model = record['model']
    if model['kind']=='delete_contiguous':
        i,n=model['source_start'] if deletion is None else deletion,model['length']; del mapping[i:i+n]
    elif model['kind']=='group_restore':
        remove = model['canonical_delete_source_index'] if deletion is None else deletion
        mapping.remove(remove)
        mapping.insert(mapping.index(model['insert_before_source_index']),None)
    else:
        assert model['kind']=='identity'
    return mapping


def read_model(literal,mapping):
    return ''.join('?' if i is None else clean(literal[i]) for i in mapping)


def proposal(record, key, literal, mapping, decoded, spec):
    text=spec['plaintext']; assert len(text)==len(decoded['raw'])
    middle=list(untranspose(read_model(literal,mapping),key['column_rank_order']))
    for i,c in enumerate(text):
        if c=='?':continue
        cell=key['square'].index(c)
        middle[2*i:2*i+2]=[C[cell//6],C[cell%6]]
    perm=permutation(len(middle),key['column_rank_order'])
    target=[None]*len(middle)
    for c,i in zip(middle,perm):target[i]=c
    target=''.join(target)
    got=inverse(target,key,mapping)
    assert all(a=='?' or a==b for a,b in zip(text,got['raw']))
    if '?' not in text:
        assert target==encrypt(text,key['column_rank_order'],key['square'])
        assert got['raw']==text
    known=[];erasures=[];inserted=[];preserved=0
    base=read_model(literal,mapping)
    for i,(old,new) in enumerate(zip(base,target)):
        origin=mapping[i]
        if old==new:
            preserved+=old!='?'
            continue
        assert new in C
        event={'model_index':i,'source_index':origin,'from':old,'to':new}
        if origin is None:inserted.append(event)
        elif old=='?':
            event['literal']=literal[origin];erasures.append(event)
        else:known.append(event)
    rebuilt=list(base)
    for event in known+erasures+inserted:rebuilt[event['model_index']]=event['to']
    assert ''.join(rebuilt)==target
    return {'id':spec['id'],'plaintext':text,'reason':spec['reason'],
            'known_coordinate_substitutions':known,'source_erasure_fills':erasures,
            'model_inserted_slot_fills':inserted,'observed_coordinates_preserved':preserved,
            'full_reencryption_verified':'?' not in text,
            'source_length_unchanged_after_declared_model':True,
            'key_changed':False}


def audit_record(record,key):
    literal=''.join(''.join(record['source_rows']).split())
    assert len(literal)==record['source_slots']
    identity=decrypt(clean(literal),key['column_rank_order'],key['square'],allow_unpaired=True)
    assert identity==record['expected_identity_raw']
    mapping=source_map(record); cipher=read_model(literal,mapping)
    assert len(cipher)==record['advertised_length']
    decoded=inverse(cipher,key,mapping)
    assert decoded['raw']==record['expected_model_raw']
    aliases=[]
    if record['model']['kind']=='delete_contiguous':
        for deletion in record['model'].get('source_start_aliases',[record['model']['source_start']]):
            alias=source_map(record,deletion)
            assert read_model(literal,alias)==cipher
            aliases.append({'deleted_source_start':deletion,'deleted_symbols':literal[deletion:deletion+record['model']['length']],
                            'identical_model_ciphertext':True})
    if record['model']['kind']=='group_restore':
        for deletion in record['model']['delete_source_indices']:
            alias=source_map(record,deletion)
            assert read_model(literal,alias)==cipher
            aliases.append({'deleted_source_index':deletion,'deleted_symbol':literal[deletion],
                            'inserted_before_source_index':record['model']['insert_before_source_index'],
                            'identical_model_ciphertext':True})
    return {'id':record['id'],'key_id':record['key_id'],'literal':literal,
            'source_slots':len(literal),'valid_source_coordinates':sum(c in C for c in literal),
            'source_erasure_slots':[{'source_index':i,'literal':c} for i,c in enumerate(literal) if c not in C],
            'identity_raw':identity,'model':record['model'],'model_ciphertext':cipher,
            'source_map':mapping,'model_aliases':aliases,**decoded,
            'editorial_candidates':[proposal(record,key,literal,mapping,decoded,spec)
                                     for spec in record['editorial_candidates']]}


def parallel_audit(records,keys):
    a,b=records['p140_A1'],records['p146_A']
    assert a['key_id']==b['key_id']=='Nov4-6'
    earlier=a['model_ciphertext']; source=clean(b['literal'])
    scans=[]
    for start in range(len(source)-5+1):
        candidate=source[:start]+source[start+5:]
        disagreements=[i for i,(x,y) in enumerate(zip(candidate,earlier)) if x!='?' and x!=y]
        scans.append({'delete_source_start':start,'known_disagreements':len(disagreements)})
    minimum=min(x['known_disagreements'] for x in scans)
    best=[x for x in scans if x['known_disagreements']==minimum]
    expected=b['editorial_candidates'][0]['plaintext']
    witnessed=[];unknown=[]
    for i,c in enumerate(expected):
        witnesses=[r['id'] for r in (a,b) if r['positions'][i]['raw']==c]
        (witnessed if witnesses else unknown).append({'index':i,'symbol':c,'witnesses':witnesses})
    return {'original_p146_slots':117,'advertised_slots':112,
            'complete_contiguous_five_slot_deletion_screen':scans,
            'minimum_known_coordinate_disagreements':minimum,'minimum_models':best,
            'declared_extra_group':'VAADX','declared_source_start':55,
            'candidate_positions_witnessed':len(witnessed),'candidate_length':len(expected),
            'unwitnessed_editorial_positions':unknown,
            'limit':'A minimum-error source alignment is not a proof of the historical copy operation. The Z in OFFIZIER remains editorial.'}


def group_restoration_audit(record,key):
    literal=record['literal']; groups=INPUT_RECORDS[record['id']]['source_rows']
    groups=' '.join(groups).split();assert groups[33]=='VFFGDV' and groups[55]=='XFVA'
    starts=[];offset=0
    for g in groups:starts.append(offset);offset+=len(g)
    assert starts[33]==165 and starts[55]==276
    desired=record['editorial_candidates'][0]['plaintext']
    target=encrypt(desired,key['column_rank_order'],key['square'])
    models=[]
    for d in range(6):
        for gap in range(5):
            modified=groups[:]
            modified[33]=modified[33][:d]+modified[33][d+1:]
            modified[55]=modified[55][:gap]+'?'+modified[55][gap:]
            c=''.join(modified)
            edits=sum(a!='?' and a!=b for a,b in zip(c,target))
            models.append({'delete_within_group34':d,'insert_gap_within_group56':gap,
                           'known_coordinate_substitutions_to_candidate':edits,
                           'inserted_coordinate':target[c.index('?')]})
    minimum=min(x['known_coordinate_substitutions_to_candidate'] for x in models)
    best=[x for x in models if x['known_coordinate_substitutions_to_candidate']==minimum]
    assert [(x['delete_within_group34'],x['insert_gap_within_group56']) for x in best]==[(1,1),(2,1)]
    assert minimum==4
    return {'printed_group34':'VFFGDV','printed_group56':'XFVA','models_examined':30,
            'model_definition':'One deletion within six-letter group34, one missing slot within four-letter group56.',
            'minimum_known_substitutions_for_declared_candidate':minimum,'minimum_models':best,
            'all_models':models,'limit':'Optimality is conditional on the displayed readable candidate and this local group model; it is not a unique unconditioned decipherment.'}


INPUT_RECORDS={}


def build(pdf=None):
    global INPUT_RECORDS
    inputs=json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors']=='icekylinx and GPT-6 Astra Pro'
    catalogue={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    keys={k['id']:k for k in inputs['keys']}
    for id,k in keys.items():assert k==catalogue[id]
    for source in inputs['source_images']:assert sha(HERE/source['path'])==source['sha256']
    if pdf:
        assert pdf.stat().st_size==inputs['source']['pdf_bytes'] and sha(pdf)==inputs['source']['pdf_sha256']
    corpus={b['id']:b for b in json.loads((ROOT/'experiments/p153_corpus/inputs.json').read_text())['blocks']}
    for r in inputs['records']:
        assert all(i in corpus for i in r['ocr_blocks'])
    INPUT_RECORDS={r['id']:r for r in inputs['records']}
    records=[audit_record(r,keys[r['key_id']]) for r in inputs['records']]
    by={r['id']:r for r in records}
    ordinary=[r for r in records if r['model']['kind']=='identity']
    damaged=[r for r in records if r['model']['kind']!='identity']
    return {'schema':'adfgvx-source-extension-certificate-v1','project':inputs['project'],
            'authors':inputs['authors'],'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All indices are zero-based; printed group numbers are explicitly one-based.',
            'summary':{'ciphertext_records':len(records),'cleartext_source_records':1,
                       'printed_source_slots':sum(r['source_slots'] for r in records),
                       'valid_printed_coordinates':sum(r['valid_source_coordinates'] for r in records),
                       'identity_model_records':len(ordinary),
                       'identity_model_fixed_positions':sum(r['fixed_positions'] for r in ordinary),
                       'identity_model_plaintext_positions':sum(len(r['raw']) for r in ordinary),
                       'damaged_model_records':len(damaged),
                       'damaged_model_fixed_positions':sum(r['fixed_positions'] for r in damaged),
                       'damaged_model_plaintext_positions':sum(len(r['raw']) for r in damaged)},
            'records':records,'p140_p146_parallel':parallel_audit(by,keys),
            'p226_C3_group_restoration':group_restoration_audit(by['p226_C3'],keys['Nov28-Dec1']),
            'prior_word_length_audit':{'source_token':'SMUTIONEN','source_positions':9,
                                     'prior_publication_token':'SITUATIONEN','prior_positions':11,
                                     'extra_plaintext_positions_in_prior_normalization':2,
                                     'same_length_alternatives':['STATIONEN','INSTANZEN'],
                                     'conclusion':'The prior word is not an exact same-length decipherment; alternatives remain explicitly conditional.'},
            'limits':['Fixed positions mean consequences of the stated source, key and geometry, including readable and garbled characters.',
                      'The two local source damage models remain separate from identity decryption.',
                      'The Nov28-Dec1 published square is unchanged. Number-like X/J strings and NSL remain literal.',
                      'Prior interpretations retain their authorship; no first historical decipherment is claimed.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args=parser.parse_args(); result=build(args.pdf); path=HERE/'certificates.json'
    if args.verify:
        assert json.loads(path.read_text())==result,'Committed certificate differs from independent rebuild'
    else:path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],sort_keys=True))
    print('Source, independent inverse, proposal costs, parallel alignment and local group-model checks passed.')

if __name__=='__main__':main()
