#!/usr/bin/env python3
"""Check headquarters and award-class constraints in the Nov13–15b traffic."""
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
    CO, clean, completions, positions,
)


def read(path):
    return json.loads((ROOT / path).read_text())


def load_record(spec):
    cert = next(r for r in read(spec['certificate'])['records'] if r['id'] == spec['id'])
    source = cert[spec['literal_field']]
    edited = cert[spec['edition_field']]['ciphertext']
    mapping = cert[spec['mapping_field']]
    assert len(mapping) == len(edited) and all(i is not None for i in mapping)
    return source, edited, mapping, cert


def numeral_one_context(data, base, ranks):
    """Replay a native date-shaped field without using either new cell value.

    DD is the published label 1. Its *numerical* value is a contextual
    interpretation: if the repeated final digit is a month, only 11 is valid.
    The source geometry remains the earlier conditional obliteration model.
    """
    context = data['numeral_one_context']
    spec = next(r for r in data['records'] if r['id'] == context['record'])
    source, _, mapping, _ = load_record(spec)
    source_input = next(r for r in read(spec['inputs'])['records']
                        if r['id'] == context['record'])
    literal = ''.join(''.join(source_input['source_rows']).split())
    assert literal == source
    native = clean(''.join(source[i] for i in mapping))
    text, ps = positions(native, ranks, base)
    assert context['native_context'] in text
    start = context['plaintext_start_0based']
    assert text[start:start + len(context['literal_date'])] == context['literal_date']
    evidence = []
    for offset, expected in enumerate(context['native_source_pairs_0based']):
        p = ps[start + offset]
        indices = [mapping[i] for i in p['source_indices']]
        assert indices == expected
        assert all(source[i] in CO for i in indices)
        assert ''.join(source[i] for i in indices) == p['pair']
        evidence.append({**p, 'source_indices': indices,
                         'literal_label': text[start + offset]})
    assert [p['pair'] for p in evidence] == ['DD', 'DX', 'DV', 'DD', 'DD']
    cell = CO.index('D') * 6 + CO.index('D')
    assert base[cell] == context['published_label'] == '1'
    possible_month_digits = [d for d in range(10) if 1 <= 11 * d <= 12]
    assert possible_month_digits == [1]
    assert context['conditional_numeric_value'] == 1
    return {**context, 'positions': evidence,
            'valid_repeated_month_digits': possible_month_digits,
            'uses_published_square_only': True,
            'new_observed_substitutions': [], 'new_mask_fills': [],
            'supports_numerical_one_only_under_date_interpretation': True}


def build():
    data = json.loads((HERE / 'inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    for crop in data['historical_source']['crops']:
        assert hashlib.sha256((HERE / crop['path']).read_bytes()).hexdigest() == crop['sha256']
    keys = {k['id']: k for k in read('data/keys.json')['keys']}
    key = keys['Nov13-15b']
    base, ranks = key['square'], key['column_rank_order']
    qcell = CO.index('X') * 6 + CO.index('X')
    classcell = CO.index('V') * 6 + CO.index('G')
    assert base[qcell] == base[classcell] == '?'

    # The source-reviewed p202 B3 has the same office and the intact GRHQU
    # abbreviation under another key. The destination identification is
    # stated as the assumption, rather than treating the messages as copies.
    donor_spec = data['headquarters_donor']
    donor = next(r for r in read(donor_spec['certificate'])['records'] if r['id'] == donor_spec['id'])
    donor_key = keys['Nov16-18']
    donor_text, donor_positions = positions(clean(donor['literal_source']),
                                             donor_key['column_rank_order'], donor_key['square'])
    span = 'GENERALINTENDANTXGRHQU'
    start = donor_text.index(span)
    donor_q = start + span.index('Q')
    assert donor_positions[donor_q]['domain'] == 'Q'
    assert '?' not in donor_positions[donor_q]['pair']
    q_square = list(base)
    q_square[qcell] = 'Q'
    q_square = ''.join(q_square)

    # The class intersection also retains DD's numerical value as 1. This
    # is not entailed merely by the published label: a separate native
    # date-shaped field corroborates it under its explicit date reading.
    one_context = numeral_one_context(data, base, ranks)
    # Conditional on both numerical DD=1 and EK + one digit denoting an
    # Iron Cross class, the official classes {1, 2} intersect only at 2.
    free_symbols = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(base)
    compatible_classes = sorted(free_symbols & set(data['award_class_symbols']))
    assert compatible_classes == ['2']
    final = list(q_square)
    final[classcell] = '2'
    final = ''.join(final)
    assert q_square == data['headquarters_square'] and final == data['joint_square']
    squares = list(completions(final))
    assert len(squares) == 720
    ycell = CO.index('F') * 6 + CO.index('X')
    assert final[ycell] == '?' and 'Y' not in final
    with_y = final[:ycell] + 'Y' + final[ycell + 1:]
    assert len(list(completions(with_y))) == 120
    records = {}
    for spec in data['records']:
        source, edited, mapping, old = load_record(spec)
        native = clean(''.join(source[i] for i in mapping))
        baseline, bp = positions(edited, ranks, base)
        headquarters, _ = positions(edited, ranks, q_square)
        text, ps = positions(edited, ranks, final)
        _, native_positions = positions(native, ranks, final)
        assert text == spec['expected_interpretation']
        new = []
        for p, (a, b) in enumerate(zip(baseline, text)):
            if a == '?' and b != '?':
                assert ps[p]['pair'] in ('XX', 'VG')
                assert ps[p]['pair'] == native_positions[p]['pair']
                indices = [mapping[i] for i in ps[p]['source_indices']]
                assert all(source[i] in CO for i in indices)
                new.append({**ps[p], 'source_indices': indices, 'symbol': b})
        assert len(new) == spec['new_fixed_positions']
        changes, fills = [], []
        for m, i in enumerate(mapping):
            a, b = source[i], edited[m]
            if a in CO and a != b:
                changes.append({'source_index': i, 'from': a, 'to': b})
            elif a not in CO and b in CO:
                fills.append({'source_index': i, 'literal': a, 'to': b})
        assert len(changes) == spec['observed_substitutions']
        assert len(fills) == spec['source_mask_fills']
        witness_cipher = edited.replace('?', 'A')
        for square in squares:
            full_text = decrypt(witness_cipher, ranks, square)
            assert all(a == '?' or a == b for a, b in zip(text, full_text))
            assert all(ch in pos['domain'] for ch, pos in zip(full_text, ps))
            assert encrypt(full_text, ranks, square) == witness_cipher
        records[spec['id']] = {
            'id': spec['id'], 'literal_source': source,
            'source_slots': len(source), 'model_to_source_indices': mapping,
            'edition_ciphertext': edited, 'baseline_edition': baseline,
            'headquarters_interpretation': headquarters, 'joint_interpretation': text,
            'native_joint_interpretation': positions(native, ranks, final)[0],
            'positions': len(text), 'fixed_before': len(baseline) - baseline.count('?'),
            'fixed_after': len(text) - text.count('?'), 'new_fixed_positions': new,
            'earlier_observed_substitutions': changes, 'earlier_mask_fills': fills,
            'additional_observed_substitutions': [], 'additional_mask_fills': [],
            'remaining_domains': [p for p in ps if len(p['domain']) != 1],
            'global_witness': {'square': squares[0], 'ciphertext': witness_cipher,
                               'plaintext': decrypt(witness_cipher, ranks, squares[0]),
                               'arbitrary_remaining_values_are_not_readings': True},
        }
    target = records['p188_C1']
    assert target['joint_interpretation'][27:35] == 'GRXHXQUX'
    assert target['joint_interpretation'][41:50] == 'ALLE2TAGE'
    assert target['new_fixed_positions'][0]['source_indices'] == [53, 171]
    award_spec = next(r for r in data['records'] if r['id'] == 'p193_F')
    _, _, _, award = load_record(award_spec)
    endpoints = []
    for variant in award['endpoint_alternatives']:
        cipher = variant['edited']['ciphertext']
        text, ps = positions(cipher, ranks, final)
        mapping = [i for i in range(len(award['literal_source']))
                   if i != variant['excluded_source_index']]
        pair = next(p for p in ps if p['pair'] == 'VG')
        assert [mapping[i] for i in pair['source_indices']] == [19, 60]
        assert pair['domain'] == '2'
        assert '2XVERLIEHENXGLUECKWUNSCH' in text
        for square in squares:
            full = decrypt(cipher, ranks, square)
            assert encrypt(full, ranks, square) == cipher
        endpoints.append({'excluded_source_index': variant['excluded_source_index'],
                          'excluded_value': variant['excluded_value'],
                          'interpretation': text, 'ciphertext': cipher,
                          'source_shape_not_selected_by_the_class_interpretation': True})
    assert [v['excluded_source_index'] for v in endpoints] == [0, 1, 73, 74]

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
    assert sum(len(r['new_fixed_positions']) for r in records.values()) == 6
    return {
        'schema': 'adfgvx-nov13-joint-completion-v1', 'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'squares': {'published': base, 'headquarters': q_square, 'joint': final,
                    'remaining_completion_counts': [40320, 5040, 720]},
        'headquarters_donor': {'id': donor_spec['id'], 'native_text': donor_text,
                              'Q_position': donor_positions[donor_q]},
        'numeral_one_context': one_context,
        'award_classes': data['award_class_symbols'], 'compatible_classes': compatible_classes,
        'records': list(records.values()), 'new_fixed_positions': 6,
        'new_source_edits': 0, 'p193_endpoint_alternatives': endpoints,
        'readable_quotes_verified': data['readable_quotes'],
        'case_fields_verified': data['case_fields'], 'limits': data['limits'],
    }


def check_historical_pdf(path):
    import fitz
    source = json.loads((HERE / 'inputs.json').read_text())['historical_source']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source['pdf_sha256']
    doc = fitz.open(path)
    for crop in source['crops']:
        pix = doc[crop['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(crop['scale'], crop['scale']),
            clip=fitz.Rect(crop['clip_pdf_points']), alpha=False)
        assert (pix.width, pix.height) == (crop['width'], crop['height'])
        assert hashlib.sha256(pix.samples).hexdigest() == crop['pixel_sha256']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--historical-pdf', type=Path)
    args = parser.parse_args()
    result = build()
    if args.historical_pdf:
        check_historical_pdf(args.historical_pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Nov13 joint constraints: XX=Q and conditional EK2/VG=2; 6 fixed positions; 720 squares; all 4 p193 endpoints retained; no source edits.')


if __name__ == '__main__':
    main()
