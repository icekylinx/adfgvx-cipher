#!/usr/bin/env python3
"""Verify p228 A's native source and every tied bounded deletion model.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import (
    inspect, masked_encryption, permutation, repair,
)

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(rows):
    return ''.join(''.join(rows).split())


def masked(literal):
    return ''.join(c if c in C else '?' for c in literal)


def score(mapping, source, stencil):
    observed, fills = 0, 0
    for j, i in enumerate(mapping):
        if stencil[j] == '?':
            continue
        if source[i] not in C:
            fills += 1
        elif source[i] != stencil[j]:
            observed += 1
    excluded = sorted(set(range(len(source))) - set(mapping))
    return {'substitutions': observed, 'stencil_mask_fills': fills,
            'excluded_valid_coordinates': sum(source[i] in C for i in excluded),
            'excluded_masked_slots': sum(source[i] not in C for i in excluded)}


def model_branch(mapping, source, key, stencil, start):
    base = ''.join(masked(source)[i] for i in mapping)
    raw = inspect(base, key, mapping)
    proposed = ''.join(a if b == '?' else b for a, b in zip(base, stencil))
    proposed_reading = inspect(proposed, key, mapping)
    # Recover only the explicit word stencil; all other raw labels and masks stay.
    edited = repair(proposed_reading['raw'], base, key, mapping, source)
    assert edited['ciphertext'] == proposed
    p = score(mapping, source, stencil)
    assert len(edited['known_coordinate_substitutions']) == p['substitutions']
    assert len(edited['erased_coordinate_fills']) == p['stencil_mask_fills']
    unknown_slots = [i for i, c in enumerate(proposed) if c == '?']
    witnesses = []
    for values in itertools.product(C, repeat=len(unknown_slots)):
        completed = list(proposed)
        for i, value in zip(unknown_slots, values):
            completed[i] = value
        completed = ''.join(completed)
        plain = decrypt(completed, key['column_rank_order'], key['square'])
        assert encrypt(plain, key['column_rank_order'], key['square']) == completed
        assert all(a == '?' or a == b for a, b in zip(edited['raw'], plain))
        witnesses.append({'remaining_model_slots': unknown_slots,
                          'remaining_source_slots': [mapping[i] for i in unknown_slots],
                          'coordinate_values': ''.join(values), 'ciphertext': completed,
                          'plaintext': plain, 'historical_completion_claim': False})
    return {'excluded_start': start, 'excluded_source_indices': list(range(start, start+10)),
            **p, 'model_to_source_indices': mapping, 'ciphertext': base,
            'raw': raw, 'word_stencil_candidate': edited,
            'all_remaining_mask_completions': witnesses}


def build(pdf=None):
    data = json.loads((HERE/'inputs.json').read_text())
    record, key = data['record'], data['key']
    assert data['authors'] == 'icekylinx and GPT-6 Astra Pro'
    assert key == next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id'] == key['id'])
    assert '?' not in key['square'] and set(key['square']) == set(A)
    for name, digest in data['prior_artifacts'].items():
        assert sha(HERE/name) == digest
    report = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': report['summary']}))
    source = compact(record['source_rows'])
    assert len(source) == record['source_slots'] == 384
    assert sum(c in C for c in source) == record['valid_source_coordinates'] == 379
    assert [(i,c) for i,c in enumerate(source) if c not in C] == [(10,'-'),(25,'-'),(52,'M'),(57,'M'),(117,'-')]
    assert record['advertised_length_literal'] == '374?' and record['separator'] == 'Y'
    native = inspect(masked(source), key, list(range(384)))
    spans = data['retrospective_word_spans']
    plain_stencil = ['?']*187
    for span in spans:
        start, text = span['start'], span['text']
        assert record['primary_edited_output'][start:start+len(text)] == text
        assert all(c == '?' for c in plain_stencil[start:start+len(text)])
        plain_stencil[start:start+len(text)] = text
    plain_stencil = ''.join(plain_stencil)
    stencil = masked_encryption(plain_stencil, key)
    assert len(stencil) == 374

    contiguous = []
    for start in range(375):
        mapping = list(range(start)) + list(range(start+10,384))
        contiguous.append({'start': start, **score(mapping,source,stencil)})
    minimum = min(r['substitutions'] for r in contiguous)
    tied = [r for r in contiguous if r['substitutions'] == minimum]
    assert minimum == 7 and [r['start'] for r in tied] == list(range(4,14))
    branches = [model_branch(list(range(r['start'])) + list(range(r['start']+10,384)),
                source,key,stencil,r['start']) for r in tied]
    primary = next(r for r in branches if r['excluded_start'] == 5)
    assert primary['raw']['raw'] == record['primary_expected_raw']
    assert primary['word_stencil_candidate']['raw'] == record['primary_edited_output']
    assert primary['raw']['fixed_positions'] == 183
    assert primary['word_stencil_candidate']['fixed_positions'] == 187
    assert primary['excluded_valid_coordinates'] == 9 and primary['excluded_masked_slots'] == 1
    edits = primary['word_stencil_candidate']['known_coordinate_substitutions']
    fills = primary['word_stencil_candidate']['erased_coordinate_fills']
    assert [(e['source_index'],e['from'],e['to']) for e in edits] == [(98,'F','V'),(133,'X','V'),(165,'F','V'),(186,'F','V'),(225,'G','D'),(233,'G','D'),(234,'F','V')]
    assert [(e['source_index'],e['printed'],e['to']) for e in fills] == [(25,'-','D'),(52,'M','D'),(57,'M','D'),(117,'-','X')]
    primary_aliases = [r['excluded_start'] for r in branches if r['ciphertext'] == primary['ciphertext']]
    assert primary_aliases == list(range(5,11))

    groups = []
    for first, second in itertools.combinations(range(76),2):
        removed = set(range(5*first,5*first+5)) | set(range(5*second,5*second+5))
        mapping = [i for i in range(384) if i not in removed]
        groups.append({'excluded_group_indices':[first,second],**score(mapping,source,stencil)})
    group_minimum = min(r['substitutions'] for r in groups)
    group_ties = [r for r in groups if r['substitutions'] == group_minimum]
    assert len(groups) == 2850 and group_minimum == 7
    assert [r['excluded_group_indices'] for r in group_ties] == [[1,2],[2,3]]
    assert all(source[5*i:5*i+5] == 'VGXXV' for i in [1,3])
    assert source[10:15] == '-XVVG'

    word_costs = []
    order = permutation(374,key['column_rank_order'])
    for span in spans:
        positions = range(span['start'],span['start']+len(span['text']))
        slots = {j for p in positions for j in order[2*p:2*p+2]}
        word_costs.append({**span,
            'raw': primary['raw']['raw'][span['start']:span['start']+len(span['text'])],
            'known_coordinate_substitutions':[e for e in edits if e['model_index'] in slots],
            'printed_mask_fills':[e for e in fills if e['model_index'] in slots]})
    assert sum(len(w['known_coordinate_substitutions']) for w in word_costs) == 7
    assert sum(len(w['printed_mask_fills']) for w in word_costs) == 4
    differences = []
    for branch in branches:
        diffs = [{'plaintext_index':i,'primary':a,'alternative':b}
                 for i,(a,b) in enumerate(zip(record['primary_edited_output'],branch['word_stencil_candidate']['raw'])) if a != b]
        assert all(plain_stencil[e['plaintext_index']] == '?' for e in diffs)
        differences.append({'excluded_start':branch['excluded_start'],
                            'candidate_fixed_positions':branch['word_stencil_candidate']['fixed_positions'],
                            'differences_outside_word_stencil':diffs})
    folded = ''.join(c for c in record['readable_german'].upper() if c in A+'?')
    assert folded == record['primary_edited_output'].replace('Y','')
    ocr = json.loads((HERE/'ocr_snapshot.json').read_text())
    assert len(ocr['records']) == 1 and ocr['records'][0]['id'] == 'p228_ocr_block1'
    old = ''.join(ocr['records'][0]['groups'])
    old_comparison = {'earlier_slots':len(old),'native_slots':len(source),
                      'earlier_source':old,'current_source':source,
                      'same_length_character_differences':[{'source_index':i,'old':a,'reviewed':b} for i,(a,b) in enumerate(zip(old,source)) if a != b],
                      'historical_repair_cost':False}
    case = (ROOT/data['case']).read_text()
    assert 'Literal header: `' + record['literal_header'] + '`.' in case
    assert '\n'.join(record['source_rows']) in case
    for plain in [native['raw'],primary['raw']['raw'],record['primary_edited_output']]:
        assert '\n```text\n'+plain+'\n```\n' in case
    assert '> '+record['readable_german']+'\n' in case
    assert 'starts **4–13**' in case and 'Y is the separator' in case
    assert 'GEDRATET' in case and 'BUCKAREST' in case and 'MARSCHZ' in case
    return {'schema':'adfgvx-nov30-aviation-march-destination-certificate-v1',
        'project':data['project'],'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),
        'indexing':'All source, model, plaintext and group indices are zero-based; intervals are half-open.',
        'summary':{'physical_records':1,'printed_source_slots':384,'valid_source_coordinates':379,
            'modeled_coordinates':374,'plaintext_positions':187,
            'native_fixed_positions':native['fixed_positions'],'native_plaintext_positions':192,
            'baseline_fixed_positions':183,'candidate_fixed_positions':187,
            'known_coordinate_substitutions':7,'printed_mask_fills':4,
            'observed_coordinate_exclusions':9,'masked_slot_exclusions':1,'source_exclusions':10,
            'added_model_slots':0,'added_slot_fills':0,'published_key_changed':False,
            'scope':'Primary ten-slot exclusion [5,15). All ten tied contiguous placements are retained separately.'},
        'record_id':record['id'],'literal_header':record['literal_header'],'literal_source':source,
        'literal_source_rows':record['source_rows'],'native':native,'primary':primary,
        'plaintext_word_stencil':plain_stencil,'ciphertext_word_stencil':stencil,
        'selection_scope':data['selection_scope'],'primary_word_costs':word_costs,
        'all_contiguous_ten_slot_exclusion_prices':contiguous,
        'all_two_whole_group_exclusion_prices':groups,
        'all_contiguous_minimum_branches':branches,
        'all_two_whole_group_minima':group_ties,
        'primary_equivalent_contiguous_source_maps':primary_aliases,
        'unconstrained_label_sensitivity':differences,
        'ocr_comparison':old_comparison,'readable_german':record['readable_german'],
        'prior_credit':data['prior_credit'],'limits':data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary']},indent=2))


if __name__ == '__main__':
    main()
