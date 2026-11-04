#!/usr/bin/env python3
"""Verify a marine-service notice with a preserved ambiguous source stroke.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The native frame and the separately priced exclusion/insertion remain distinct.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.premium_payment_stop.verify import C, inspect, masked_encryption, repair, sha, verify_crops


from adfgvx.source_evidence import verify_source_evidence

def native_witnesses(specs):
    keys = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    donors = []
    for spec in specs:
        records = json.loads((ROOT / spec['inputs']).read_text())['records']
        rec = next(r for r in records if r['id'] == spec['record'])
        donor_source = ''.join(rec[spec['source_field']].split())
        assert hashlib.sha256(donor_source.encode()).hexdigest() == spec['source_sha256']
        donor_cipher = ''.join(c if c in C else '?' for c in donor_source)
        reading = inspect(donor_cipher, keys[spec['key_id']], list(range(len(donor_cipher))))
        expected = rec
        for part in spec['raw_field'].split('.'):
            expected = expected[part]
        assert reading['raw'] == expected and spec['context'] in expected
        start = expected.index(spec['word'])
        positions = reading['positions'][start:start + len(spec['word'])]
        assert all(len(p['domain']) == 1 and set(p['pair']) <= set(C) for p in positions)
        donors.append({**spec, 'plaintext_start': start, 'positions': positions})
    return donors


def complete_labels(source, literal, candidate, key, mapping, raw):
    data = json.loads((HERE / 'label_completion.json').read_text())
    assert hashlib.sha256(literal.encode()).hexdigest() == data['source_sha256']
    completed = repair(data['proposal'], candidate['ciphertext'], key, mapping, literal)
    assert not completed['known_coordinate_substitutions']
    assert [(e['source_index'], e['to']) for e in completed['erased_coordinate_fills']] == [(44, 'F'), (146, 'X')]
    assert completed['fixed_positions'] == 143
    fields = []
    for field in data['fields']:
        i, source_index = field['plaintext_index'], field['source_index']
        assert candidate['raw'][i] == field['before'] == '?'
        assert completed['raw'][i] == field['proposed']
        assert literal[source_index] == field['printed']
        assert raw['positions'][i]['domain'] == field['native_domain']
        assert field['proposed'] in field['native_domain']
        fields.append({**field, 'pair_before': raw['positions'][i]['pair'],
                       'source_indices': raw['positions'][i]['source_indices'],
                       'pair_after': completed['positions'][i]['pair']})
    donors = native_witnesses(data['donors'])
    full = repair(data['proposal'], source, key, mapping, literal)
    assert len(full['known_coordinate_substitutions']) == 3
    assert sum(e['source_index'] is not None for e in full['erased_coordinate_fills']) == 6
    assert sum(e['source_index'] is None for e in full['erased_coordinate_fills']) == 1
    address_spec = data['optional_headquarters_address']
    assert address_spec['proposal'] == data['proposal'].replace(address_spec['before'], address_spec['after'])
    extra = repair(address_spec['proposal'], full['ciphertext'], key, mapping, literal)
    assert [[e['source_index'], e['from'], e['to']] for e in extra['known_coordinate_substitutions']] == address_spec['expected_additional_substitutions']
    assert not extra['erased_coordinate_fills']
    address = repair(address_spec['proposal'], source, key, mapping, literal)
    assert address['fixed_positions'] == full['fixed_positions'] == 143
    assert len(address['known_coordinate_substitutions']) == 5
    assert address['erased_coordinate_fills'] == full['erased_coordinate_fills']
    case = (ROOT / 'cases/radio/nov6_marine_service_notice.md').read_text()
    assert address_spec['case_summary'] in case
    optional = {
        'before': address_spec['before'], 'after': address_spec['after'],
        'readable_fragment': address_spec['readable_fragment'],
        'plaintext': address['raw'], 'ciphertext': address['ciphertext'],
        'additional_substitutions': extra['known_coordinate_substitutions'],
        'additional_source_mask_fills': 0, 'additional_fixed_positions': 0,
        'total_observed_substitutions': 5, 'total_source_mask_fills': 6, 'total_added_slot_fills': 1,
        'changed_positions': [
            {'plaintext_index': i, 'before': full['positions'][i], 'after': address['positions'][i]}
            for i in range(143) if full['raw'][i] != address['raw'][i]],
        'native_donors': native_witnesses(address_spec['donors']),
        'full_plaintext_reencryption_verified': address['full_plaintext_reencryption_verified'],
        'limits': address_spec['limits']}
    return {'input_sha256': sha(HERE / 'label_completion.json'),
            'readable_german': data['readable_german'], 'fields': fields, 'donors': donors,
            'additional_observed_substitutions': 0, 'additional_source_mask_fills': 2,
            'complete_conditional_reading': full, 'optional_headquarters_address': optional,
            'limits': data['limits']}


def build(pdf=None):
    data = json.loads((HERE / 'inputs.json').read_text())
    key = data['key']
    assert data['authors'] == 'icekylinx and GPT-6 Astra Pro'
    assert key == next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys'] if k['id'] == key['id'])
    assert '?' not in key['square']
    assert sha(ROOT / data['verification_helper']['path']) == data['verification_helper']['sha256']
    for path, digest in data['prior_artifacts'].items():
        assert sha(HERE / path) == digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))
    source = data['records'][0]
    literal = ''.join(source['source_rows']).replace(' ', '')
    assert len(literal) == source['source_slots'] == source['advertised_length'] == 286
    excluded = source['analysis_frame']['exclude_source_indices']
    assert excluded == [225] and literal[225] == source['ambiguous_source_mark']['transcription_token'] == '|'
    assert literal[220:231] == 'FADFF|VAADA'
    native = ''.join(ch if ch in C else '?' for ch in literal)
    native_result = inspect(native, key, list(range(len(native))))
    assert native_result['raw'] == source['native_expected_raw']
    retained_indices = [i for i in range(len(literal)) if i not in excluded]
    retained = ''.join(native[i] for i in retained_indices)
    assert len(retained) == 285
    assert source['analysis_frame']['insert_unknown_at_source_boundary'] == 286
    cipher, mapping = retained + '?', retained_indices + [None]
    raw = inspect(cipher, key, mapping)
    assert raw['raw'] == source['expected_raw']
    candidate = repair(source['readable_candidate'], cipher, key, mapping, literal)
    substitutions, fills = candidate['known_coordinate_substitutions'], candidate['erased_coordinate_fills']
    assert [(e['source_index'], e['from'], e['to']) for e in substitutions] == [(13, 'A', 'F'), (98, 'V', 'F'), (174, 'D', 'X')]
    assert sum(e['source_index'] is not None for e in fills) == 4
    assert sum(e['source_index'] is None for e in fills) == 1
    for token in source['protected_fields']:
        assert token in raw['raw'] and token in candidate['raw'] and token in source['readable_german']
    assert candidate['raw'].count('?') == 2 and candidate['fixed_positions'] == 141
    complete_cipher = candidate['ciphertext'].replace('?', 'A')
    complete_plain = decrypt(complete_cipher, key['column_rank_order'], key['square'])
    assert encrypt(complete_plain, key['column_rank_order'], key['square']) == complete_cipher
    assert all(a == '?' or a == b for a, b in zip(candidate['raw'], complete_plain))
    candidate['global_completion_witness'] = {
        'ciphertext': complete_cipher, 'plaintext': complete_plain,
        'roundtrip_verified': True, 'historical_completion_claim': False,
    }
    stencil = masked_encryption(candidate['raw'], key)
    prices = []
    for b in range(len(stencil)):
        reduced_target = stencil[:b] + stencil[b + 1:]
        cost = sum(a in C and z in C and a != z for a, z in zip(retained, reduced_target))
        prices.append(cost)
    minima = [i for i, cost in enumerate(prices) if cost == min(prices)]
    assert len(prices) == 286 and min(prices) == 3 and minima == [285]
    assert prices[280:] == [6, 5, 4, 4, 4, 3]
    case = (ROOT / data['case']).read_text()
    fences = re.findall(r'```(?:text)?\n(.*?)\n```', case, flags=re.S)
    assert native_result['raw'] in fences and raw['raw'] in fences and candidate['raw'] in fences
    display = re.sub('[^A-Z0-9?]', '', source['readable_german'].upper()).replace('X', '')
    assert display == candidate['raw'].replace('X', '')
    assert '> ' + source['readable_german'] in case
    summary = {
        'physical_records': 1, 'printed_source_slots': len(literal),
        'valid_source_coordinates': sum(ch in C for ch in literal),
        'modeled_coordinates': len(cipher), 'plaintext_positions': len(raw['raw']),
        'baseline_fixed_positions': raw['fixed_positions'], 'candidate_fixed_positions': candidate['fixed_positions'],
        'known_coordinate_substitutions': len(substitutions), 'source_or_model_erasure_fills': len(fills),
        'source_mask_fills': sum(e['source_index'] is not None for e in fills),
        'inserted_slot_fills': sum(e['source_index'] is None for e in fills),
        'inserted_slots': 1, 'source_deletions': 1, 'excluded_valid_source_coordinates': 0,
        'excluded_source_mask_coordinates': 1, 'unfilled_retained_source_mask_coordinates': 2,
        'source_reorderings': 0, 'published_key_changed': False,
    }
    assert (summary['valid_source_coordinates'], summary['baseline_fixed_positions'], summary['candidate_fixed_positions']) == (279, 136, 141)
    record = {
        'id': source['id'], 'literal_source': literal, 'literal_printed_rows': source['source_rows'],
        'source_slots': len(literal), 'valid_source_coordinates': summary['valid_source_coordinates'],
        'ambiguous_source_mark': source['ambiguous_source_mark'],
        'native_frame': {'ciphertext': native, 'model_to_source_indices': list(range(len(native))), **native_result},
        'ciphertext': cipher, 'analysis_frame_slots': len(cipher), 'model_to_source_indices': mapping,
        'frame_exclusions': [{'source_index': 225, 'printed': '|', 'valid_coordinate': False,
                              'visible_cancellation_claim': False, 'scope': 'Conditional treatment as a noncoordinate stroke, not a source deletion fact.'}],
        'frame_insertions': [{'source_boundary': 286, 'model_index': 285, 'initial_value': '?', 'supplied_value': candidate['ciphertext'][-1]}],
        **raw, 'readable_candidate': candidate,
        'all_changed_plaintext_positions': [
            {'plaintext_index': i, 'raw': a, 'candidate': b, 'source_indices': raw['positions'][i]['source_indices']}
            for i, (a, b) in enumerate(zip(raw['raw'], candidate['raw'])) if a != b
        ],
        'single_gap_search': {
            'scope': 'The ambiguous stroke is already excluded. All one-gap alignments of the retained 285-slot source against the fixed partial target are priced; ? in the target constrains neither coordinate. No other exclusions, insertions or historical plaintexts are searched.',
            'alignments_examined': len(prices), 'prices_by_retained_source_boundary': prices,
            'minimum_observed_substitutions': min(prices), 'minimum_retained_source_boundaries': minima,
            'corresponding_original_source_boundaries': [286],
        },
    }
    completion = complete_labels(cipher, literal, candidate, key, mapping, raw)
    assert completion['complete_conditional_reading']['raw'] in fences
    assert '> ' + completion['readable_german'] in case
    complete_display = re.sub('[^A-Z0-9?]', '', completion['readable_german'].upper()).replace('X', '')
    assert complete_display == completion['complete_conditional_reading']['raw'].replace('X', '')
    record['label_completion'] = completion
    summary['completed_conditional_fixed_positions'] = completion['complete_conditional_reading']['fixed_positions']
    summary['completion_additional_source_mask_fills'] = completion['additional_source_mask_fills']
    return {'schema': 'adfgvx-marine-service-notice-certificate-v1', 'project': data['project'], 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': 'All indices are zero-based. The literal source includes the declared narrow-stroke token. Retained-source boundaries refer to the 285-slot stream after its explicit exclusion; original-source boundaries refer to the full 286-slot transcription.',
            'summary': summary, 'records': [record], 'headers': data['headers'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
