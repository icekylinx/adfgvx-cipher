#!/usr/bin/env python3
"""Verify the conditional two-part Tiflis Ringbahn instruction.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The fixed-text alignment searches do not assert unique historical wording.
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


def frame(literal, boundaries):
    """Insert masks before original source indices; no source slot is discarded."""
    assert sorted(boundaries) == boundaries
    assert all(0 <= b <= len(literal) for b in boundaries)
    result, mapping = [], []
    for i in range(len(literal) + 1):
        for boundary in boundaries:
            if boundary == i:
                result.append('?')
                mapping.append(None)
        if i < len(literal):
            result.append(literal[i] if literal[i] in C else '?')
            mapping.append(i)
    assert [i for i in mapping if i is not None] == list(range(len(literal)))
    return ''.join(result), mapping


def fixed_text_gap_search(literal, target, key, gap_count):
    """All ways to remove gap_count model slots from the fixed re-encryption."""
    cipher = encrypt(target, key['column_rank_order'], key['square'])
    assert len(cipher) - len(literal) == gap_count
    histogram, minimizers = Counter(), []
    best = len(literal) + 1
    single_gap_prices = []
    examined = 0
    for omitted in combinations(range(len(cipher)), gap_count):
        deleted = set(omitted)
        remaining = ''.join(ch for i, ch in enumerate(cipher) if i not in deleted)
        cost = sum(a in C and a != b for a, b in zip(literal, remaining))
        examined += 1
        histogram[cost] += 1
        if gap_count == 1:
            single_gap_prices.append(cost)
        if cost < best:
            best, minimizers = cost, []
        if cost == best:
            minimizers.append({
                'inserted_model_indices': list(omitted),
                'source_boundaries': [i - j for j, i in enumerate(omitted)],
                'inserted_values': ''.join(cipher[i] for i in omitted),
                'observed_coordinate_substitutions': cost,
            })
    return {
        'scope': 'The candidate plaintext and published key are fixed; every order-preserving alignment with exactly the stated number of added slots is tested. Printed masks have no observed-coordinate substitution cost.',
        'gap_count': gap_count,
        'alignments_examined': examined,
        'substitution_cost_histogram': {str(k): v for k, v in sorted(histogram.items())},
        'minimum_observed_substitutions': best,
        'minimum_cost_alignments': minimizers,
        'all_single_gap_costs_by_source_boundary': single_gap_prices,
    }


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
    case = (ROOT / data['case']).read_text()
    literal_fences = re.findall(r'```(?:text)?\n(.*?)\n```', case, flags=re.S)
    old_raw = {}
    for witness in data['supporting_sources']:
        assert sha(ROOT / witness['input_path']) == witness['input_sha256']
        live = json.loads((ROOT / witness['input_path']).read_text())
        pool = live.get('records', live.get('messages'))
        for source in witness['records']:
            assert source == next(r for r in pool if r['id'] == source['id'])
            literal = ''.join(source['source_rows']).replace(' ', '')
            cipher, mapping = frame(literal, [])
            decoded = inspect(cipher, key, mapping)
            assert decoded['raw'] == source['expected_raw']
            old_raw[source['id']] = decoded
    records = []
    for source in data['records']:
        literal = ''.join(source['source_rows']).replace(' ', '')
        assert len(literal) == source['source_slots']
        boundaries = source['analysis_frame']['insert_unknown_at_source_boundaries']
        cipher, mapping = frame(literal, boundaries)
        assert len(cipher) == source['advertised_length']
        decoded = inspect(cipher, key, mapping)
        assert decoded['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], cipher, key, mapping, literal)
        assert candidate['full_plaintext_reencryption_verified']
        fills = candidate['erased_coordinate_fills']
        assert len(candidate['known_coordinate_substitutions']) == source['expected_observed_substitutions']
        assert sum(e['source_index'] is not None for e in fills) == source['expected_source_mask_fills']
        assert sum(e['source_index'] is None for e in fills) == source['expected_inserted_slot_fills']
        for field in source['protected_fields']:
            assert field in decoded['raw'] and field in candidate['raw']
        assert decoded['raw'] in literal_fences and candidate['raw'] in literal_fences
        display = re.sub('[^A-Z0-9?]', '', source['readable_german'].upper()).replace('X', '')
        assert display == candidate['raw'].replace('X', '')
        assert '> ' + source['readable_german'] in case
        search = fixed_text_gap_search(literal, candidate['raw'], key, len(boundaries))
        primary = next(a for a in search['minimum_cost_alignments'] if a['source_boundaries'] == boundaries)
        assert primary['observed_coordinate_substitutions'] == len(candidate['known_coordinate_substitutions'])
        alternatives = []
        for alignment in search['minimum_cost_alignments']:
            alt_cipher, alt_map = frame(literal, alignment['source_boundaries'])
            alt_raw = inspect(alt_cipher, key, alt_map)
            alt_candidate = repair(candidate['raw'], alt_cipher, key, alt_map, literal)
            alternatives.append({**alignment, 'raw': alt_raw['raw'], 'model_to_source_indices': alt_map,
                                 'observed_substitutions': alt_candidate['known_coordinate_substitutions'],
                                 'mask_and_inserted_slot_fills': alt_candidate['erased_coordinate_fills']})
        records.append({
            'id': source['id'], 'literal_printed_rows': source['source_rows'], 'literal_source': literal,
            'source_slots': len(literal), 'valid_coordinates': sum(ch in C for ch in literal),
            'ciphertext': cipher, 'analysis_frame_slots': len(cipher), 'model_to_source_indices': mapping,
            **decoded, 'readable_candidate': candidate, 'fixed_text_alignment_search': search,
            'all_minimum_cost_alignments': alternatives,
            'all_changed_plaintext_positions': [
                {'plaintext_index': i, 'raw': a, 'candidate': b, 'source_indices': decoded['positions'][i]['source_indices']}
                for i, (a, b) in enumerate(zip(decoded['raw'], candidate['raw'])) if a != b
            ],
        })
    assert records[0]['literal_source'][65:69] == 'XAAF'
    assert records[1]['literal_source'][35:39] == 'VF--'
    first = records[0]['fixed_text_alignment_search']
    assert first['alignments_examined'] == 15400 and first['minimum_observed_substitutions'] == 0
    assert [a['source_boundaries'] for a in first['minimum_cost_alignments']] == [[66, 173]]
    second = records[1]['fixed_text_alignment_search']
    assert second['alignments_examined'] == 192 and second['minimum_observed_substitutions'] == 1
    assert [a['source_boundaries'] for a in second['minimum_cost_alignments']] == [[37], [38], [39]]
    support = []
    by_id = {r['id']: r for r in records}
    for span in data['supporting_spans']:
        new, old, text = by_id[span['new_record']], old_raw[span['old_record']], span['text']
        i, j = new['readable_candidate']['raw'].index(text), old['raw'].index(text)
        support.append({**span, 'new_start_plaintext_index': i, 'old_start_plaintext_index': j,
                        'length': len(text), 'new_changed_positions_supported': [
                            {'new_plaintext_index': i + q, 'old_plaintext_index': j + q,
                             'candidate_and_old_raw': ch, 'new_raw': new['raw'][i + q]}
                            for q, ch in enumerate(text) if new['raw'][i + q] != ch]})
    all_fills = [e for r in records for e in r['readable_candidate']['erased_coordinate_fills']]
    summary = {
        'physical_records': len(records),
        'printed_source_slots': sum(r['source_slots'] for r in records),
        'valid_source_coordinates': sum(r['valid_coordinates'] for r in records),
        'modeled_coordinates': sum(r['analysis_frame_slots'] for r in records),
        'plaintext_positions': sum(len(r['raw']) for r in records),
        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
        'candidate_fixed_positions': sum(r['readable_candidate']['fixed_positions'] for r in records),
        'known_coordinate_substitutions': sum(len(r['readable_candidate']['known_coordinate_substitutions']) for r in records),
        'source_or_model_erasure_fills': len(all_fills),
        'source_mask_fills': sum(e['source_index'] is not None for e in all_fills),
        'inserted_slot_fills': sum(e['source_index'] is None for e in all_fills),
        'inserted_slots': sum(i is None for r in records for i in r['model_to_source_indices']),
        'source_deletions': 0, 'source_reorderings': 0, 'published_key_changed': False,
    }
    assert (summary['printed_source_slots'], summary['modeled_coordinates'], summary['baseline_fixed_positions']) == (365, 368, 175)
    assert (summary['known_coordinate_substitutions'], summary['source_mask_fills'], summary['inserted_slot_fills']) == (1, 6, 3)
    return {'schema': 'adfgvx-tiflis-ringbahn-certificate-v1', 'project': data['project'], 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': 'All source, model and plaintext indices are zero-based. A source boundary is before the source index of that number, with len(source) denoting the end.',
            'summary': summary, 'records': records, 'independent_raw_span_support': support,
            'headers': data['headers'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    output = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(output.read_text())
    else:
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
