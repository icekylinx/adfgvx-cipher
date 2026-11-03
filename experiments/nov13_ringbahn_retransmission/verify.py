#!/usr/bin/env python3
"""Verify the truncated p187 Ringbahn instruction and every copied coordinate.

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
from experiments.romanian_pacification_consultation.verify import inspect
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(rows):
    return ''.join(''.join(rows).split())


def source_map(source, first, second):
    assert first in (50, 55) and second in (80, 85)
    assert source[50:55] == source[55:60] == 'AVXVD'
    assert source[80:85] == source[85:90] == 'DXDGA'
    excluded = set(range(first, first + 5)) | set(range(second, second + 5))
    mapping = [None] * 5
    for i in range(len(source)):
        if i == 40:
            mapping += [None] * 5
        if i not in excluded:
            mapping.append(i)
    mapping += [None] * 74
    assert len(mapping) == 214
    assert len(set(i for i in mapping if i is not None)) == 130
    return mapping, sorted(excluded)


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov4-6')
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    donors = {}
    for ref in data['donors']:
        path = ROOT / ref['path']
        assert sha(path) == ref['sha256']
        donor = next(r for r in load(path)[ref['container']] if r['id'] == ref['id'])
        donors[ref['id']] = compact(donor['source_rows'])
        assert len(donors[ref['id']]) == 214 and set(donors[ref['id']]) <= set(C)
        assert decrypt(donors[ref['id']], key['column_rank_order'], key['square']) == donor['expected_raw']
    previous = data['prior_ocr']
    assert sha(HERE / previous['path']) == previous['sha256']
    assert sha(ROOT / previous['origin']) == previous['origin_sha256']
    old = load(HERE / previous['path'])
    assert old == next(r for r in load(ROOT / previous['origin'])['blocks'] if r['id'] == old['id'])
    records = []
    for r in data['records']:
        source = compact(r['source_rows'])
        assert len(source) == r['source_slots'] == 140
        assert source.count('-') == 1 and source[79] == '-'
        assert r['advertised_length'] == 214
        aliases = []
        for first, second in r['group_aliases']:
            mapping, excluded = source_map(source, first, second)
            frame = ''.join('?' if i is None or source[i] == '-' else source[i] for i in mapping)
            primary = inspect(frame, key, mapping)
            assert primary['fixed_positions'] == 33
            aliases.append({'excluded_group_starts': [first, second],
                            'excluded_source_indices': excluded,
                            'model_to_source_indices': mapping, 'ciphertext': frame,
                            'raw': primary['raw'], 'fixed_positions': 33})
        assert len(aliases) == 4 and len({a['ciphertext'] for a in aliases}) == 1
        selected = aliases[0]
        mapping, frame = selected['model_to_source_indices'], selected['ciphertext']
        primary = inspect(frame, key, mapping)
        linked = list(frame)
        copied = []
        for model_index, original in enumerate(mapping):
            if original is not None:
                continue
            donor = 'p211_B_lower1' if model_index == 46 else 'p145_B1'
            linked[model_index] = donors[donor][model_index]
            copied.append({'model_index': model_index, 'donor_record': donor,
                           'donor_source_index': model_index, 'coordinate': linked[model_index]})
        assert len(copied) == 84
        assert sum(c['donor_record'] == 'p145_B1' for c in copied) == 83
        assert sum(c['donor_record'] == 'p211_B_lower1' for c in copied) == 1
        linked = ''.join(linked)
        before_repairs = inspect(linked, key, mapping)
        assert before_repairs['fixed_positions'] == 106 and linked.count('?') == 1
        fixed_gain = [i for i, (a, b) in enumerate(zip(primary['positions'], before_repairs['positions']))
                      if len(a['domain']) > 1 and len(b['domain']) == 1]
        assert len(fixed_gain) == 73
        target = encrypt(r['readable_candidate'], key['column_rank_order'], key['square'])
        assert len(target) == 214 and decrypt(target, key['column_rank_order'], key['square']) == r['readable_candidate']
        assert all(target[c['model_index']] == c['coordinate'] for c in copied)
        changes, masks = [], []
        rebuilt = list(linked)
        for j, (a, b) in enumerate(zip(linked, target)):
            if a == b:
                continue
            original = mapping[j]
            assert original is not None
            donor_support = [{'record': rid, 'source_index': j, 'coordinate': s[j]}
                             for rid, s in donors.items() if s[j] == b]
            assert donor_support
            event = {'model_index': j, 'source_index': original, 'printed': source[original],
                     'from': a, 'to': b, 'observed_donor_support': donor_support}
            (masks if a == '?' else changes).append(event)
            rebuilt[j] = b
        assert len(changes) == 5 and len(masks) == 1
        assert ''.join(rebuilt) == target
        assert [c['source_index'] for c in changes] == [26, 75, 76, 77, 78]
        assert masks[0]['source_index'] == 79
        assert all(token in r['readable_candidate'] for token in r['protected_fields'])
        german = re.sub('[^A-Z0-9]', '', r['readable_german'].upper())
        assert german == r['readable_candidate'].replace('X', '')
        records.append({'id': r['id'], 'literal_source': source, 'source_slots': len(source),
                        'valid_source_coordinates': 139, 'ciphertext': frame,
                        'model_to_source_indices': mapping, **primary,
                        'excluded_source_indices': selected['excluded_source_indices'],
                        'source_map_aliases': aliases,
                        'source_linked': {'ciphertext': linked, 'raw': before_repairs['raw'],
                                          'fixed_positions': 106, 'copied_coordinate_origins': copied,
                                          'additional_fixed_positions': fixed_gain},
                        'readable_candidate': {'raw': r['readable_candidate'], 'ciphertext': target,
                                               'known_coordinate_substitutions': changes,
                                               'source_mask_fills': masks,
                                               'source_linked_slot_fills': copied,
                                               'reencryption_verified': True},
                        'readable_german': r['readable_german']})
    case_path = ROOT / data['case']
    text = case_path.read_text()
    assert text.count(expected_legend(case_path)) == 1
    fences, quotes = displays(text)
    assert [f['role_from_caption'] for f in fences] == ['raw_output', 'edited_output', 'source_transcription']
    assert len(quotes) == 1 and quotes[0]['role_from_caption'] == 'readable_german'
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    assert bodies == [records[0]['raw'], records[0]['readable_candidate']['raw'],
                      '\n'.join(data['records'][0]['source_rows'])]
    assert re.findall(r'^> (.*)$', text, re.M) == [data['records'][0]['readable_german']]
    result = {'schema': 'adfgvx-armistice-remaining-sources-certificate-v1',
              'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
              'indexing': data['indexing'],
              'summary': {'physical_records': 1, 'printed_source_slots': 140,
                          'valid_source_coordinates': 139, 'modeled_coordinates': 214,
                          'plaintext_positions': 107, 'baseline_fixed_positions': 33,
                          'source_linked_fixed_positions_before_repairs': 106,
                          'additional_fixed_positions_from_copy': 73,
                          'candidate_fixed_positions': 107, 'excluded_observed_source_slots': 10,
                          'inserted_source_linked_slots': 84, 'known_coordinate_substitutions': 5,
                          'source_mask_fills': 1, 'published_key_changed': False},
              'records': records, 'prior_credit': data['prior_credit'], 'limits': data['limits']}
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
