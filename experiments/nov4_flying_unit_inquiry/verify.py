#!/usr/bin/env python3
"""Verify the partial flying-unit inquiry and both locally tied gap mappings.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.premium_payment_stop.verify import C, inspect, repair, sha, verify_crops


def frame(literal, boundary):
    native = ''.join(ch if ch in C else '?' for ch in literal)
    cipher = native[:boundary] + '?' + native[boundary:]
    mapping = list(range(boundary)) + [None] + list(range(boundary, len(native)))
    return cipher, mapping


from adfgvx.source_evidence import verify_source_evidence

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
    assert len(literal) == source['source_slots'] == 183
    assert literal[15:19] == 'XFVV'
    boundary = source['analysis_frame']['insert_unknown_at_source_boundary']
    cipher, mapping = frame(literal, boundary)
    assert len(cipher) == source['advertised_length'] == 184
    assert [i for i in mapping if i is not None] == list(range(len(literal)))
    raw = inspect(cipher, key, mapping)
    assert raw['raw'] == source['expected_raw']
    candidate = repair(source['readable_candidate'], cipher, key, mapping, literal)
    assert raw['raw'][:17] == candidate['raw'][:17] == source['protected_prefix']
    assert candidate['raw'].count('?') == 9
    assert len(candidate['known_coordinate_substitutions']) == 2
    fills = candidate['erased_coordinate_fills']
    assert sum(e['source_index'] is not None for e in fills) == 16
    assert sum(e['source_index'] is None for e in fills) == 1
    assert [(e['source_index'], e['from'], e['to']) for e in candidate['known_coordinate_substitutions']] == [(14, 'G', 'D'), (171, 'A', 'G')]
    # One arbitrary completion proves that the residual masks can be completed
    # consistently. It does not supply the historical opening reference.
    complete_cipher = candidate['ciphertext'].replace('?', 'A')
    complete_plain = decrypt(complete_cipher, key['column_rank_order'], key['square'])
    assert encrypt(complete_plain, key['column_rank_order'], key['square']) == complete_cipher
    assert all(a == '?' or a == b for a, b in zip(candidate['raw'], complete_plain))
    candidate['global_completion_witness'] = {
        'ciphertext': complete_cipher, 'plaintext': complete_plain,
        'roundtrip_verified': True, 'historical_completion_claim': False,
    }
    alternatives = []
    for b in source['analysis_frame']['all_local_boundaries']:
        base, mp = frame(literal, b)
        decoded = inspect(base, key, mp)
        repaired = repair(source['readable_candidate'], base, key, mp, literal)
        alternatives.append({
            'source_boundary': b, 'inserted_model_index': b,
            'raw': decoded['raw'], 'fixed_positions': decoded['fixed_positions'],
            'model_to_source_indices': mp,
            'observed_coordinate_substitutions': repaired['known_coordinate_substitutions'],
            'source_mask_and_inserted_slot_fills': repaired['erased_coordinate_fills'],
            'candidate_ciphertext': repaired['ciphertext'],
            'added_value': repaired['ciphertext'][b],
        })
    costs = [len(a['observed_coordinate_substitutions']) for a in alternatives]
    assert costs == [3, 2, 2, 3, 3]
    minima = [a for a in alternatives if len(a['observed_coordinate_substitutions']) == min(costs)]
    assert [a['source_boundary'] for a in minima] == source['analysis_frame']['tied_minimum_boundaries'] == [16, 17]
    assert minima[0]['candidate_ciphertext'] == minima[1]['candidate_ciphertext'] == candidate['ciphertext']
    assert minima[0]['raw'] != minima[1]['raw']
    assert candidate['ciphertext'][15:20] == 'XFFVV'
    case = (ROOT / data['case']).read_text()
    fences = re.findall(r'```(?:text)?\n(.*?)\n```', case, flags=re.S)
    assert raw['raw'] in fences and candidate['raw'] in fences and minima[0]['raw'] in fences
    display = re.sub('[^A-Z0-9?]', '', source['readable_german'].upper()).replace('X', '')
    assert display == candidate['raw'].replace('X', '')
    assert '> ' + source['readable_german'] in case
    record = {
        'id': source['id'], 'literal_source': literal, 'literal_printed_rows': source['source_rows'],
        'source_slots': len(literal), 'valid_source_coordinates': sum(ch in C for ch in literal),
        'ciphertext': cipher, 'analysis_frame_slots': len(cipher), 'model_to_source_indices': mapping,
        **raw, 'readable_candidate': candidate,
        'all_changed_plaintext_positions': [
            {'plaintext_index': i, 'raw': a, 'candidate': b, 'source_indices': raw['positions'][i]['source_indices']}
            for i, (a, b) in enumerate(zip(raw['raw'], candidate['raw'])) if a != b
        ],
        'local_gap_comparison': {
            'scope': 'Exactly one gap within or at an edge of the visibly short XFVV group; the proposed body and unresolved opening template remain fixed. This is not a search over all historical plaintexts.',
            'alternatives': alternatives,
            'minimum_observed_substitutions': min(costs),
            'all_minimum_source_boundaries': [a['source_boundary'] for a in minima],
        },
    }
    summary = {
        'physical_records': 1, 'printed_source_slots': len(literal),
        'valid_source_coordinates': sum(ch in C for ch in literal),
        'modeled_coordinates': len(cipher), 'plaintext_positions': len(raw['raw']),
        'baseline_fixed_positions': raw['fixed_positions'],
        'candidate_fixed_positions': candidate['fixed_positions'],
        'known_coordinate_substitutions': len(candidate['known_coordinate_substitutions']),
        'source_or_model_erasure_fills': len(fills),
        'source_mask_fills': sum(e['source_index'] is not None for e in fills),
        'inserted_slot_fills': sum(e['source_index'] is None for e in fills),
        'unfilled_source_mask_coordinates': sum(ch not in C for ch in literal) - sum(e['source_index'] is not None for e in fills),
        'inserted_slots': 1, 'source_deletions': 0, 'source_reorderings': 0, 'published_key_changed': False,
    }
    assert (summary['valid_source_coordinates'], summary['baseline_fixed_positions'], summary['candidate_fixed_positions']) == (158, 67, 83)
    return {'schema': 'adfgvx-flying-unit-inquiry-certificate-v1', 'project': data['project'], 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': 'All source, model and plaintext indices are zero-based. A source boundary is before the original source index of that number.',
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
