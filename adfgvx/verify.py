"""Recompute the published source certificates with the standard library.

Run ``python -m adfgvx.verify`` from the repository root. ``--json`` emits a
machine-readable summary; no files are modified and no network is accessed.
"""
from pathlib import Path
import argparse
import hashlib
import json

from .cipher import decrypt, encrypt, self_check, SYMBOLS, plaintext_domains, transpose, untranspose
from .alignment import find_switch, table, alignment
from .projection import analyze, untranspose as project_untranspose, transpose as project_transpose
from . import prior

ROOT=Path(__file__).resolve().parent.parent


def certificate(name):
    return json.loads((ROOT/'data/certificates'/f'{name}.json').read_text())


def edited(raw, edits):
    result=raw;last=len(raw)+1
    for change in sorted(edits,key=lambda x:(x['start'],x['end']),reverse=True):
        a,b=change['start'],change['end']
        assert 0<=a<=b<=len(raw) and b<=last
        assert raw[a:b]==change['before']
        result=result[:a]+change['after']+result[b:];last=a
    return result


def p158():
    data=certificate('p158');comp=data['components'];roundtrips=[]
    for record in comp['readings']:
        ct=edited(record['raw_ciphertext'],record['edits'])
        assert ct==record['corrected_ciphertext']
        pt=decrypt(ct,comp['key'],comp['square'])
        assert pt==record['raw_plaintext']
        assert encrypt(pt,comp['key'],comp['square'])==ct
        roundtrips.append(record['id'])
    cert=data['splice'];splits=[]
    assert cert['source_B']==comp['readings'][0]['raw_ciphertext'].replace('R','?').replace('-','?')
    assert cert['source_C']==comp['readings'][2]['raw_ciphertext']
    for name,record in cert['variants'].items():
        a=record['ciphertext'];assert hashlib.sha256(a.encode()).hexdigest()==record['sha256']
        result=find_switch(a,cert['source_B'],cert['source_C'])
        assert result['minimum_cost']==record['minimum_cost']
        assert result['optimal_switches']==record['optimal_switches']
        assert len(result['optimal_switches'])==1
        assert result['optimal_switches'][0]['p158_split']==130
        splits.append({'layer':name,'cost':result['minimum_cost'],'split':130})
    count=0
    for layer in data['source_layers']['layers'].values():
        for first in 'XV':
            for second in 'XD':
                a=list(layer['ciphertext']);a[55]=first;a[126]=second
                result=find_switch(''.join(a),cert['source_B'],cert['source_C'])
                assert {r['p158_split'] for r in result['optimal_switches']}=={130}
                count+=1
    return {'status':'PASS','classification':'composite_source_identification',
            'exact_component_roundtrips':roundtrips,'splits':splits,'glyph_variants_checked':count}


def p152():
    cert=certificate('p152');key=cert['key'];ranks=key['column_rank_order'];square=key['square'];checks=[]
    for record in cert['source_decryptions']:
        raw=record['source_ciphertext'];assert hashlib.sha256(raw.encode()).hexdigest()==record['source_sha256']
        ct=raw
        for change in sorted(record['edits'],key=lambda x:x['index'],reverse=True):
            assert change['operation']=='insert';at=change['index'];ct=ct[:at]+change['value']+ct[at:]
        assert ct==record['corrected_ciphertext']
        assert decrypt(ct,ranks,square)==record['plaintext']
        assert encrypt(record['plaintext'],ranks,square)==ct
        checks.append(record['id'])
    link=cert['p152_source_link'];short=link['source_ciphertext'];chars=list(short)
    for change in link['tail_replacements']:
        assert chars[change['index']]==change['observed'];chars[change['index']]=change['replacement']
    assert link['prefix_restored_from_parallel']+''.join(chars)==link['reconstructed_ciphertext']
    long=cert['source_decryptions'][0]['source_ciphertext']
    assert link['reconstructed_ciphertext']==long
    assert len(short)==104 and short.count('?')==2 and len(link['prefix_restored_from_parallel'])==210
    row=table(short[::-1],long[::-1])[-1];cost=min(row)
    actual={'minimum_cost':cost,'optimal_offsets':[len(long)-j for j,v in enumerate(row) if v==cost],
            'alignments':[alignment(short,long[len(long)-j:]) for j,v in enumerate(row) if v==cost]}
    assert actual==cert['independent_suffix_audit']
    return {'status':'PASS','classification':'source_linked_body_recovery','exact_source_roundtrips':checks,
            'suffix_cost':cost,'tied_offsets':actual['optimal_offsets'],'restored_prefix_symbols':210}


def p189():
    cert=certificate('p189');key=cert['key'];ranks=key['column_rank_order'];square=key['square']
    parallel=cert['p185']['ciphertext'];pt=decrypt(parallel,ranks,square)
    assert pt==cert['p185']['plaintext'] and '?' not in pt
    assert encrypt(pt,ranks,square)==parallel
    raw=cert['p189']['raw_ciphertext'];target=''.join(c if c in SYMBOLS else '?' for c in raw)
    assert target==cert['p189']['erasure_normalized_ciphertext']
    assert len(target)==90 and target.count('?')==12
    result=analyze(parallel,target,ranks,square);expected=cert['expected_projection']
    for field in ['cost','path_count','all_path_character_domains','all_path_invariant_plaintext']:
        assert result[field]==expected[field]
    assert result['paths'][0]['raw_partial_plaintext']==expected['selected_raw_partial_plaintext']
    digest=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert digest==expected['full_analysis_sha256']
    for path in result['paths']:
        mapping=path['parallel_to_target_index']
        assert [x for x in mapping if x is not None]==list(range(90))
        ct=path['aligned_ciphertext'];coords=project_untranspose(ct,ranks)
        assert project_transpose(coords,ranks)==ct
        assert plaintext_domains(ct,ranks,square)==[x['possible_characters'] for x in path['character_domains']]
    return {'status':'PASS','classification':'conditional_source_linked_partial',
            'p185_exact_roundtrip':True,'preserved_valid_coordinates':78,'source_uncertainties':12,
            'inserted_erasures':6,'tied_alignments':result['path_count'],
            'invariant_plaintext':result['all_path_invariant_plaintext']}


def prior_readings():
    path=ROOT/'data/prior_readings.json'
    document=json.loads(path.read_text())
    result=prior.verify(path)
    catalog={x['id']:x for x in json.loads((ROOT/'data/messages.json').read_text())['messages']}
    for entry in document['messages']:
        assert entry['analysis_ciphertext']==catalog[entry['id']]['transcript']['analysis_ciphertext']
        ranks=entry['key']['column_rank_order'];square=entry['key']['square']
        for variant in entry['verified_variants']:
            verified=variant['verification']
            assert untranspose(verified['corrected_ciphertext'],ranks)==verified['intermediate_stream_before_edits']
            after=verified['intermediate_stream_after_edits']
            paired=after[:2*verified['decoded_plaintext_length']]
            assert after[len(paired):]==verified['unpaired_intermediate_suffix']
            assert plaintext_domains(transpose(paired,ranks),ranks,square)==verified['plaintext_domains']
    result['independent_domain_crosscheck']=True
    result['published_readings']=sum(len(x['published_readings']) for x in document['messages'])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json',action='store_true');args=parser.parse_args()
    assert self_check()
    # Reject silent loss of an odd trailing coordinate.
    try:decrypt('A',[1],'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    except ValueError:pass
    else:raise AssertionError('Odd-length input was silently truncated')
    results={'arithmetic':'PASS','cases':{'p152':p152(),'p158':p158(),'p189':p189()},
             'prior_readings':prior_readings()}
    if args.json:print(json.dumps(results,indent=2))
    else:
        print('PASS: independent ADFGVX arithmetic and odd-length guard')
        for name,record in results['cases'].items():print(f"PASS: {name} — {record['classification']}")
        print('Seven exact source roundtrips; exhaustive correspondence and domain checks passed.')
        previous=results['prior_readings']
        print(f"PASS: {previous['messages']} prior entries, {previous['published_readings']} attributed readings, "
              f"{previous['verified_variants']} reconstruction variants, independent domain checks")


if __name__=='__main__':main()
