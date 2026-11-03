#!/usr/bin/env python3
"""Verify the new p180 D1 evening report and all eight tied source maps.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
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
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair
from experiments.nov11_romanian_ultimatum_report.independent import build as independent_build
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(rows):
    return ''.join(''.join(rows).split())


def mapping_for(source, duplicate, final_A, boundary):
    assert source[125:130] == source[130:135] == 'XGVXD'
    assert source[195:197] == 'AA'
    assert duplicate in (125, 130) and final_A in (195, 196)
    excluded = set(range(duplicate, duplicate + 5)) | {final_A}
    retained = [i for i in range(len(source)) if i not in excluded]
    assert len(retained) == 191 and 0 <= boundary <= len(retained)
    mapping = retained[:boundary] + [None] * 5 + retained[boundary:]
    assert len(mapping) == 196 and len(set(i for i in mapping if i is not None)) == 191
    return mapping, sorted(excluded), retained[boundary] if boundary < len(retained) else None


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov10-12')
    for field in ['prior_ocr', 'independent_source_audit']:
        spec = data[field]
        assert sha(HERE / spec['path']) == spec['sha256']
    prior = data['prior_ocr']
    assert sha(ROOT / prior['origin']) == prior['origin_sha256']
    prior_row = load(HERE / prior['path'])
    assert prior_row == next(r for r in load(ROOT / prior['origin'])['blocks'] if r['id'] == prior_row['id'])
    related = data['related_source']
    assert sha(ROOT / related['path']) == related['sha256']
    assert any(r['id'] == related['record_id'] for r in load(ROOT / related['path'])['records'])
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    independent = independent_build()
    assert independent == load(HERE / 'independent.json')
    records = []
    for r in data['records']:
        source = compact(r['source_rows'])
        audit = load(HERE / data['independent_source_audit']['path'])
        assert r['source_rows'] == audit['rows'] and source == compact(audit['rows'])
        assert len(source) == r['source_slots'] == 197
        assert sum(c in C for c in source) == 187 and source.count('-') == 9
        assert [(i, c) for i, c in enumerate(source) if c not in C + '-'] == [(108, 'O')]
        candidate = r['readable_candidate']
        assert len(candidate) * 2 == r['advertised_length'] == 196
        encoded = encrypt(candidate, key['column_rank_order'], key['square'])
        assert decrypt(encoded, key['column_rank_order'], key['square']) == candidate
        screen, minima, minimum = [], [], None
        for duplicate in [125, 130]:
            for final_A in [195, 196]:
                costs = []
                for boundary in range(192):
                    mapping, excluded, original = mapping_for(source, duplicate, final_A, boundary)
                    frame = ''.join(source[i] if i is not None and source[i] in C else '?' for i in mapping)
                    cost = sum(a != '?' and a != b for a, b in zip(frame, encoded))
                    costs.append(cost)
                    if minimum is None or cost < minimum:
                        minimum, minima = cost, []
                    if cost == minimum:
                        minima.append((duplicate, final_A, boundary))
                screen.append({'excluded_duplicate_start': duplicate, 'excluded_final_A': final_A,
                               'insertion_boundary_costs': costs})
        assert minimum == 2 and len(minima) == 8
        assert {g for _, _, g in minima} == {145, 146}
        variants = []
        for duplicate, final_A, boundary in minima:
            mapping, excluded, original = mapping_for(source, duplicate, final_A, boundary)
            frame = ''.join(source[i] if i is not None and source[i] in C else '?' for i in mapping)
            raw = inspect(frame, key, mapping)
            proposal = repair(candidate, frame, key, mapping, source)
            substitutions = proposal['known_coordinate_substitutions']
            mask_fills = [e for e in proposal['erased_coordinate_fills'] if e['source_index'] is not None]
            inserted_fills = [e for e in proposal['erased_coordinate_fills'] if e['source_index'] is None]
            assert len(substitutions) == 2 and len(mask_fills) == 10 and len(inserted_fills) == 5
            assert [(e['source_index'], e['from'], e['to']) for e in substitutions] == [(40, 'V', 'X'), (121, 'X', 'D')]
            assert raw['fixed_positions'] == (85 if boundary == 145 else 84)
            assert proposal['ciphertext'] == encoded and proposal['raw'] == candidate
            for protected in r['protected_spans']:
                a, b = protected['start'], protected['end']
                assert raw['raw'][a:b] == candidate[a:b] == protected['literal']
                for pos in raw['positions'][a:b]:
                    assert all(i is not None and source[i] in C for i in pos['source_indices'])
            digest = hashlib.sha256(json.dumps(mapping, separators=(',', ':')).encode()).hexdigest()
            other = next(x for x in independent['minimum_maps']
                         if x['duplicate_start'] == duplicate and x['excluded_final_A'] == final_A
                         and x['gap_boundary_in_retained_stream'] == boundary)
            assert digest == other['mapping_sha256'] and raw['raw'] == other['raw']
            variants.append({'excluded_duplicate_start': duplicate, 'excluded_final_A': final_A,
                             'gap_boundary_in_retained_stream': boundary,
                             'before_original_source_index': original,
                             'excluded_source_indices': excluded, 'model_to_source_indices': mapping,
                             'ciphertext': frame, 'raw': raw['raw'], 'fixed_positions': raw['fixed_positions'],
                             'observed_coordinate_substitutions': substitutions,
                             'source_mask_fills': mask_fills, 'inserted_slot_fills': inserted_fills})
        selected = next(x for x in variants if x['excluded_duplicate_start'] == 125
                        and x['excluded_final_A'] == 195 and x['gap_boundary_in_retained_stream'] == 145)
        raw = inspect(selected['ciphertext'], key, selected['model_to_source_indices'])
        assert raw['raw'] == r['expected_raw']
        proposal = repair(candidate, selected['ciphertext'], key, selected['model_to_source_indices'], source)
        proposal['source_mask_fills'] = selected['source_mask_fills']
        proposal['inserted_slot_fills'] = selected['inserted_slot_fills']
        assert re.sub('[^A-Z0-9]', '', r['readable_german'].upper()) == candidate.replace('X', '')
        records.append({'id': r['id'], 'literal_source': source, 'source_slots': len(source),
                        'valid_source_coordinates': 187, 'ciphertext': selected['ciphertext'],
                        'model_to_source_indices': selected['model_to_source_indices'], **raw,
                        'excluded_source_indices': selected['excluded_source_indices'],
                        'readable_candidate': proposal, 'readable_german': r['readable_german'],
                        'tied_minimum_maps': variants, 'complete_fixed_candidate_cost_screen': screen})
    path = ROOT / data['case']
    text = path.read_text()
    assert text.count(expected_legend(path)) == 1
    fences, quotes = displays(text)
    assert [f['role_from_caption'] for f in fences] == ['raw_output', 'edited_output', 'source_transcription']
    assert len(quotes) == 1 and quotes[0]['role_from_caption'] == 'readable_german'
    assert re.findall(r'```text\n(.*?)\n```', text, re.S) == [records[0]['raw'], records[0]['readable_candidate']['raw'], '\n'.join(data['records'][0]['source_rows'])]
    assert re.findall(r'^> (.*)$', text, re.M) == [data['records'][0]['readable_german']]
    result = {'schema': 'adfgvx-nov11-romanian-ultimatum-report-certificate-v1',
              'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
              'indexing': data['indexing'],
              'summary': {'physical_records': 1, 'printed_source_slots': 197,
                          'valid_source_coordinates': 187, 'source_mask_slots': 10,
                          'modeled_coordinates': 196, 'plaintext_positions': 98,
                          'baseline_fixed_positions': 85, 'alternative_frame_fixed_positions': 84,
                          'candidate_fixed_positions': 98, 'excluded_observed_source_slots': 6,
                          'inserted_slots': 5, 'known_coordinate_substitutions': 2,
                          'source_mask_fills': 10, 'inserted_slot_fills': 5,
                          'tied_minimum_maps': 8, 'maps_exhaustively_compared_per_implementation': 768,
                          'published_key_changed': False},
              'records': records,
              'independent_result_sha256': sha(HERE / 'independent.json'),
              'prior_credit': data['prior_credit'], 'limits': data['limits']}
    return result, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result, evidence = build(args.pdf)
    destination = HERE / 'certificates.json'
    if args.verify:
        assert result == load(destination)
    else:
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
