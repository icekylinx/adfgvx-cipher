#!/usr/bin/env python3
"""Complete Nov16–18 references under the existing date and order constraints."""
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
from experiments.late_november_joint_completion.verify import (
    CO, clean, completions, literal, positions,
)


def read(path):
    return json.loads((ROOT / path).read_text())


def load_record(spec):
    original = next(r for r in read(spec['inputs'])['records'] if r['id'] == spec['id'])
    cert = next(r for r in read(spec['certificate'])['records'] if r['id'] == spec['id'])
    if spec['format'] == 'repatriation':
        source = original['literal_source']
        edition = cert['selected_edition']
        edited = edition['complete_working_witness']
        excluded = edition['excluded_transmitted_coordinate']
        mapping = [i for i in range(len(source))
                   if excluded is None or i != excluded['source_index']]
    elif spec['format'] == 'remit':
        source = literal(original)
        assert source == cert['literal_source']
        edited = cert['edition_ciphertext']
        mapping = cert['frame_to_original_source_index']
    else:
        source = literal(original)
        assert source == cert['literal_source']
        edited = cert['readable_candidate']['ciphertext']
        mapping = cert['model_to_source_indices']
    assert all(i is not None for i in mapping)
    assert len(mapping) == len(edited)
    return source, edited, mapping


def build():
    data = json.loads((HERE / 'inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    prior = read('experiments/open_targets_continuation/certificates.json')['conditional_key_layer']
    assert prior['key_id'] == 'Nov16-18'
    base, partial = prior['published_square'], prior['conditional_square']
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == prior['key_id'])
    assert key['square'] == base
    ranks = key['column_rank_order']
    squares = list(completions(partial))
    assert len(squares) == 720
    records = {}
    for spec in data['records']:
        source, earlier, mapping = load_record(spec)
        native = clean(''.join(source[i] for i in mapping))
        baseline, _ = positions(earlier, ranks, base)
        conditional, ps = positions(earlier, ranks, partial)
        _, native_positions = positions(native, ranks, partial)
        gains = []
        for p, (old, new) in enumerate(zip(baseline, conditional)):
            if old == '?' and new != '?':
                item = ps[p]
                assert item['pair'] in ('FD', 'VA')
                assert item['pair'] == native_positions[p]['pair']
                indices = [mapping[i] for i in item['source_indices']]
                assert all(source[i] in CO for i in indices)
                gains.append({**item, 'source_indices': indices, 'symbol': new})
        assert len(gains) == spec['new_numerals']
        edited = list(earlier)
        extra = spec.get('additional_mask_fill')
        if extra:
            i = mapping.index(extra['source_index'])
            assert source[extra['source_index']] not in CO and edited[i] == '?'
            assert ps[extra['plaintext_index']]['domain'] == 'ACKMOX'
            edited[i] = extra['to']
        edited = ''.join(edited)
        assert all(a == b for a, b in zip(earlier, edited) if a in CO)
        after, after_positions = positions(edited, ranks, partial)
        assert after == spec['expected_interpretation']
        changes, fills = [], []
        for model, i in enumerate(mapping):
            a, b = source[i], edited[model]
            if a in CO and a != b:
                changes.append({'source_index': i, 'from': a, 'to': b})
            elif a not in CO and b in CO:
                fills.append({'source_index': i, 'literal': a, 'to': b})
        assert len(changes) == spec['observed_substitutions']
        assert len(fills) == spec['mask_fills']
        witness_cipher = edited.replace('?', 'A')
        for square in squares:
            text = decrypt(witness_cipher, ranks, square)
            assert all(a == '?' or a == b for a, b in zip(after, text))
            assert all(ch in pos['domain'] for ch, pos in zip(text, after_positions))
            assert encrypt(text, ranks, square) == witness_cipher
        records[spec['id']] = {
            'id': spec['id'], 'source_slots': len(source), 'frame_slots': len(mapping),
            'literal_source': source, 'model_to_source_indices': mapping,
            'prior_edition_ciphertext': earlier, 'conditional_ciphertext': edited,
            'baseline_edition': baseline, 'interpreted_edition': after,
            'native_interpretation': positions(native, ranks, partial)[0],
            'fixed_before': len(baseline) - baseline.count('?'),
            'fixed_after': len(after) - after.count('?'), 'positions': len(after),
            'new_numeral_positions': gains, 'additional_mask_fill': extra,
            'observed_substitutions': changes, 'source_mask_fills': fills,
            'remaining_domains': [p for p in after_positions if len(p['domain']) != 1],
            'global_witness': {'square': squares[0], 'ciphertext': witness_cipher,
                               'plaintext': decrypt(witness_cipher, ranks, squares[0]),
                               'arbitrary_remaining_values_are_not_readings': True},
        }

    # Three fully received copies of the reference prefix support the
    # separator completion; none supplies the unknown reference digits.
    donors = []
    for donor in data['separator_donors']:
        rec = records[donor['record']]
        p = donor['start']
        native = clean(''.join(rec['literal_source'][i] for i in rec['model_to_source_indices']))
        text, ps = positions(native, ranks, base)
        assert text[p:p+3] == '1XA'
        donors.append({**donor, 'text': text[p:p+3], 'positions': ps[p:p+3]})
    target = records['p206_B1']
    assert target['interpreted_edition'][102:105] == '1XA'
    assert target['additional_mask_fill'] == {'plaintext_index': 103, 'source_index': 219, 'to': 'F'}
    for quote in data['readable_quotes']:
        page = (ROOT / quote['case']).read_text()
        quotes = [' '.join(line[2:] for line in match[0].splitlines())
                  for match in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', page, re.M)]
        assert quote['german'] in quotes
        labels = re.sub('[^A-Z0-9?]', '', quote['german'].upper())
        assert labels == records[quote['record']]['interpreted_edition'].replace('X', '')
    for field in data['case_fields']:
        value = records[field['record']]['interpreted_edition'][field['start']:field['end']]
        assert value == field['field']
        assert field['text'] in (ROOT / field['case']).read_text()
    assert sum(len(r['new_numeral_positions']) for r in records.values()) == 13
    return {
        'schema': 'adfgvx-nov16-18-reference-completion-v1',
        'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'conditional_square': partial, 'square_completions_verified': len(squares),
        'inherited_assumptions': prior['assumptions'],
        'new_numeral_positions': 13, 'new_mask_fills': 1,
        'new_observed_substitutions': 0,
        'records': list(records.values()), 'separator_donors': donors,
        'readable_quotes_verified': data['readable_quotes'],
        'case_fields_verified': data['case_fields'], 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Nov16–18 references: 13 further numeral positions in 7 records; 1 separator mask fill; no additional observed substitutions; all 720 squares checked.')


if __name__ == '__main__':
    main()
