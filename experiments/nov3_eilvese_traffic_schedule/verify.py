#!/usr/bin/env python3
"""Verify the Eilvese/OUI schedule and complete bounded exclusion families.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The proposed words are fixed during alignment comparisons, not independently
recovered by minimizing their own repair cost.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt
from experiments.premium_payment_stop.verify import C, inspect, repair, sha, verify_crops


def framed(literal, excluded):
    mapping = [i for i in range(len(literal)) if i not in excluded]
    return ''.join(literal[i] if literal[i] in C else '?' for i in mapping), mapping


def price(literal, target_cipher, excluded):
    cipher, _ = framed(literal, excluded)
    assert len(cipher) == len(target_cipher)
    return (sum(a in C and a != b for a, b in zip(cipher, target_cipher)),
            cipher.count('?'), sum(literal[i] in C for i in excluded))


def minimum_details(literal, key, template, candidates):
    result = []
    for label, excluded in candidates:
        base, mapping = framed(literal, excluded)
        raw = inspect(base, key, mapping)
        candidate = repair(template, base, key, mapping, literal)
        assert candidate['full_plaintext_reencryption_verified']
        result.append({
            'frame': label, 'excluded_source_indices': sorted(excluded),
            'excluded_valid_coordinates': sum(literal[i] in C for i in excluded),
            'excluded_source_masks': sum(literal[i] not in C for i in excluded),
            'ciphertext_before_word_repairs': base, 'model_to_source_indices': mapping,
            'raw': raw['raw'], 'fixed_positions': raw['fixed_positions'],
            'observed_coordinate_substitutions': candidate['known_coordinate_substitutions'],
            'source_mask_fills': candidate['erased_coordinate_fills'],
        })
    return result


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
    assert len(literal) == source['source_slots'] == 362
    assert source['advertised_length'] == 352
    assert literal[175:190] == 'FAGVDDG---FAGVD'
    assert len(literal.split()) == 1
    native, native_map = framed(literal, set())
    native_raw = inspect(native, key, native_map)
    assert native_raw['raw'] == source['native_expected_raw']
    exclusions = source['analysis_frame']['exclude_half_open_source_ranges']
    assert exclusions == [[175, 185]]
    excluded = {i for a, b in exclusions for i in range(a, b)}
    cipher, mapping = framed(literal, excluded)
    raw = inspect(cipher, key, mapping)
    assert raw['raw'] == source['expected_raw']
    candidate = repair(source['readable_candidate'], cipher, key, mapping, literal)
    assert candidate['full_plaintext_reencryption_verified']
    assert len(candidate['known_coordinate_substitutions']) == 3 and not candidate['erased_coordinate_fills']
    assert [(e['source_index'], e['from'], e['to']) for e in candidate['known_coordinate_substitutions']] == [(4, 'G', 'D'), (321, 'X', 'V'), (348, 'G', 'V')]
    assert raw['raw'].count('?') == candidate['raw'].count('?') == 0
    for token in source['protected_fields']:
        assert token in raw['raw'] and token in candidate['raw'] and token in source['readable_german']
    target_cipher = encrypt(candidate['raw'], key['column_rank_order'], key['square'])
    contiguous = []
    for start in range(len(literal) - 9):
        exc = set(range(start, start + 10))
        contiguous.append((start, price(literal, target_cipher, exc)))
    minimum = min(p[0] for _, p in contiguous)
    starts = [s for s, p in contiguous if p[0] == minimum]
    no_fill_starts = [s for s, p in contiguous if p[0] == minimum and p[1] == 0]
    assert len(contiguous) == 353 and minimum == 3
    assert starts == list(range(172, 186)) and no_fill_starts == list(range(175, 183))
    contiguous_min = minimum_details(literal, key, candidate['raw'], [
        ({'contiguous_start': s, 'contiguous_end_exclusive': s + 10}, set(range(s, s + 10))) for s in starts])
    assert {a['raw'] for a in contiguous_min if not a['source_mask_fills']} == {raw['raw']}
    assert {a['ciphertext_before_word_repairs'] for a in contiguous_min if not a['source_mask_fills']} == {cipher}
    group_prices = []
    for a, b in combinations(range(0, 360, 5), 2):
        exc = set(range(a, a + 5)) | set(range(b, b + 5))
        group_prices.append(([a, b], price(literal, target_cipher, exc)))
    group_minimum = min(p[0] for _, p in group_prices)
    group_min = [ab for ab, p in group_prices if p[0] == group_minimum]
    assert len(group_prices) == 2556 and group_minimum == 3
    assert group_min == [[175, 180], [180, 185], [185, 190]]
    group_details = minimum_details(literal, key, candidate['raw'], [
        ({'five_slot_group_starts': ab}, set(range(ab[0], ab[0] + 5)) | set(range(ab[1], ab[1] + 5)))
        for ab in group_min])
    assert [a['frame']['five_slot_group_starts'] for a in group_details if not a['source_mask_fills']] == [[175, 180], [180, 185]]
    assert {a['raw'] for a in group_details if not a['source_mask_fills']} == {raw['raw']}
    case = (ROOT / data['case']).read_text()
    fences = re.findall(r'```(?:text)?\n(.*?)\n```', case, flags=re.S)
    assert native_raw['raw'] in fences and raw['raw'] in fences and candidate['raw'] in fences
    display = re.sub('[^A-Z0-9?]', '', source['readable_german'].upper()).replace('X', '')
    assert display == candidate['raw'].replace('X', '')
    assert '> ' + source['readable_german'] in case
    histogram = Counter(p for _, p in group_prices)
    summary = {
        'physical_records': 1, 'printed_source_slots': len(literal),
        'valid_source_coordinates': sum(ch in C for ch in literal),
        'modeled_coordinates': len(cipher), 'plaintext_positions': len(raw['raw']),
        'baseline_fixed_positions': raw['fixed_positions'], 'candidate_fixed_positions': candidate['fixed_positions'],
        'known_coordinate_substitutions': len(candidate['known_coordinate_substitutions']),
        'source_or_model_erasure_fills': 0, 'source_mask_fills': 0, 'inserted_slot_fills': 0,
        'inserted_slots': 0, 'source_deletions': len(excluded),
        'excluded_valid_source_coordinates': sum(literal[i] in C for i in excluded),
        'excluded_source_mask_coordinates': sum(literal[i] not in C for i in excluded),
        'source_reorderings': 0, 'published_key_changed': False,
    }
    assert (summary['valid_source_coordinates'], summary['modeled_coordinates'], summary['baseline_fixed_positions']) == (359, 352, 176)
    record = {
        'id': source['id'], 'literal_source': literal, 'literal_printed_rows': source['source_rows'],
        'source_slots': len(literal), 'valid_source_coordinates': summary['valid_source_coordinates'],
        'native_frame': {'ciphertext': native, 'model_to_source_indices': native_map, **native_raw},
        'ciphertext': cipher, 'analysis_frame_slots': len(cipher), 'model_to_source_indices': mapping,
        'excluded_source_indices': sorted(excluded), **raw, 'readable_candidate': candidate,
        'all_changed_plaintext_positions': [
            {'plaintext_index': i, 'raw': a, 'candidate': b, 'source_indices': raw['positions'][i]['source_indices']}
            for i, (a, b) in enumerate(zip(raw['raw'], candidate['raw'])) if a != b],
        'fixed_text_frame_comparisons': {
            'scope': 'The complete edited text and published key are fixed. The families do not cover arbitrary ten-slot subsets or other plaintexts. Source-mask fills and excluded observed coordinates remain separate from the observed-substitution objective.',
            'contiguous_ten_slot_exclusions': {
                'frames_examined': len(contiguous),
                'all_prices_by_start': [{'observed_substitutions': p[0], 'retained_source_mask_fills': p[1], 'excluded_valid_coordinates': p[2]} for _, p in contiguous],
                'minimum_observed_substitutions': minimum, 'all_minimum_starts': starts,
                'minimum_starts_requiring_no_fills': no_fill_starts, 'all_minimum_frame_details': contiguous_min},
            'two_complete_five_slot_groups': {
                'frames_examined': len(group_prices), 'minimum_observed_substitutions': group_minimum,
                'price_histogram': [{'observed_substitutions': p[0], 'retained_source_mask_fills': p[1], 'excluded_valid_coordinates': p[2], 'frames': n} for p, n in sorted(histogram.items())],
                'all_minimum_group_start_pairs': group_min, 'all_minimum_frame_details': group_details},
        },
    }
    return {'schema': 'adfgvx-eilvese-traffic-schedule-certificate-v1', 'project': data['project'], 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': 'All source, model and plaintext indices are zero-based; half-open source ranges include their start and exclude their end.',
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
