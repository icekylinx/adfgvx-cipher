#!/usr/bin/env python3
"""Check the shared Nov13 class digit in five further certified editions."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.late_november_joint_completion.verify import CO, clean, completions, positions


def read(path):
    return json.loads((ROOT / path).read_text())


def build():
    data = json.loads((HERE / 'traffic_inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == data['key_id'])
    base, ranks = key['square'], key['column_rank_order']
    square = read('experiments/nov13_joint_completion/inputs.json')['joint_square']
    assert square[CO.index('V') * 6 + CO.index('G')] == '2'
    squares = list(completions(square))
    assert len(squares) == 720
    records, old_records = {}, {}
    for spec in data['records']:
        old = next(r for r in read(spec['certificate'])['records'] if r['id'] == spec['id'])
        candidate = next(c for c in old['editorial_candidates'] if c['id'] == spec['candidate'])
        source, mapping = old['literal_source'], old['model_to_source_indices']
        cipher = candidate['ciphertext']
        native = clean(''.join('?' if i is None else source[i] for i in mapping))
        before, _ = positions(cipher, ranks, base)
        after, ps = positions(cipher, ranks, square)
        _, native_ps = positions(native, ranks, square)
        assert after == spec['expected_interpretation']
        gains = []
        for p, (a, b) in enumerate(zip(before, after)):
            if a == '?' and b != '?':
                assert b == '2' and ps[p]['pair'] == native_ps[p]['pair'] == 'VG'
                indices = [mapping[i] for i in ps[p]['source_indices']]
                assert None not in indices and all(source[i] in CO for i in indices)
                gains.append({**ps[p], 'source_indices': indices, 'symbol': b})
        assert len(gains) == spec['new_fixed_positions']
        changes, fills, insertions = [], [], []
        for m, i in enumerate(mapping):
            if i is None:
                insertions.append({'model_index': m, 'value': cipher[m]})
            elif source[i] in CO and source[i] != cipher[m]:
                changes.append({'source_index': i, 'from': source[i], 'to': cipher[m]})
            elif source[i] not in CO and cipher[m] in CO:
                fills.append({'source_index': i, 'literal': source[i], 'to': cipher[m]})
        witness = cipher.replace('?', 'A')
        for full_square in squares:
            full = decrypt(witness, ranks, full_square)
            assert all(a == '?' or a == b for a, b in zip(after, full))
            assert all(c in p['domain'] for c, p in zip(full, ps))
            assert encrypt(full, ranks, full_square) == witness
        records[spec['id']] = {
            'id': spec['id'], 'source_certificate': spec['certificate'],
            'candidate': spec['candidate'], 'literal_source': source,
            'model_to_source_indices': mapping, 'edition_ciphertext': cipher,
            'baseline_edition': before, 'joint_interpretation': after,
            'positions': len(after), 'fixed_before': len(before) - before.count('?'),
            'fixed_after': len(after) - after.count('?'), 'new_fixed_positions': gains,
            'earlier_observed_substitutions': changes, 'earlier_mask_fills': fills,
            'earlier_inserted_coordinates': insertions,
            'earlier_excluded_source_indices': sorted(set(range(len(source))) - set(mapping)),
            'additional_observed_substitutions': [], 'additional_mask_fills': [],
            'remaining_domains': [p for p in ps if len(p['domain']) > 1],
            'global_witness': {'square': squares[0], 'ciphertext': witness,
                               'plaintext': decrypt(witness, ranks, squares[0]),
                               'arbitrary_remaining_values_are_not_readings': True},
        }
        old_records[spec['id']] = old

    alternatives = []
    for alt in old_records['p199_A1']['geometry_screen']['all_minimum_model_readings']:
        text, _ = positions(alt['model_ciphertext'], ranks, square)
        alternatives.append({'excluded_source_index': alt['model_parameter'],
                             'native_joint_interpretation': text,
                             'quantity': text[125:128]})
    assert [(a['excluded_source_index'], a['quantity']) for a in alternatives] == [
        (50, '120'), (51, '120'), (52, '1G0')]
    assert records['p199_A1']['fixed_after'] == 146
    assert sum(len(r['new_fixed_positions']) for r in records.values()) == 6
    for quote in data['readable_quotes']:
        page = (ROOT / quote['case']).read_text()
        quotes = [' '.join(line[2:] for line in match[0].splitlines())
                  for match in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', page, re.M)]
        assert quote['german'] in quotes
        labels = re.sub('[^A-Z0-9?]', '', quote['german'].upper())
        assert labels == records[quote['record']]['joint_interpretation'].replace('X', '')
    for field in data['case_fields']:
        assert records[field['record']]['joint_interpretation'][field['start']:field['end']] == field['field']
        assert field['text'] in (ROOT / field['case']).read_text()
    return {
        'schema': 'adfgvx-nov13-shared-traffic-v1', 'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'traffic_inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'conditional_square': square, 'completion_count': len(squares),
        'records': list(records.values()), 'new_fixed_positions': 6,
        'additional_source_edits': 0, 'p199_A1_geometry_alternatives': alternatives,
        'readable_quotes_verified': data['readable_quotes'],
        'case_fields_verified': data['case_fields'], 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'traffic_certificates.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Nov13 shared traffic: 6 additional observed-pair digits in 5 records; no new edits; cargo120; all source alternatives retained.')


if __name__ == '__main__':
    main()
