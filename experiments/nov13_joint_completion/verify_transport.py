#!/usr/bin/env python3
"""Complete p189 E and recheck the transport-field chronology scenarios."""
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
    data = json.loads((HERE / 'transport_inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    old = read(data['source_certificate'])
    records = {r['source']['id']: r['source'] for r in old['direct_transport_context']}
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov13-15b')
    base, ranks = key['square'], key['column_rank_order']
    square = read('experiments/nov13_joint_completion/inputs.json')['joint_square']
    squares = list(completions(square))
    source = records[data['record']]['raw_literal']
    baseline, _ = positions(clean(source), ranks, base)
    shared, shared_ps = positions(clean(source), ranks, square)
    fill = data['mask_fill']
    assert source[fill['source_index']] == fill['literal'] == 'B'
    p = fill['plaintext_index']
    assert shared_ps[p]['pair'] == 'V?' and shared_ps[p]['source_indices'] == [28, 81]
    assert shared_ps[p]['domain'] == '2AKNWZ'
    edited = list(clean(source))
    edited[fill['source_index']] = fill['coordinate']
    edited = ''.join(edited)
    text, ps = positions(edited, ranks, square)
    assert text == data['expected_interpretation'] and len(text) == 47
    assert text[p-3:p+6] == fill['word']
    assert '?' not in text
    gains = [x for x in ps if baseline[x['plaintext_index']] == '?']
    assert [(x['plaintext_index'], x['pair']) for x in gains] == [(26, 'VG'), (37, 'VG'), (41, 'VV')]
    assert all(a == b for a, b in zip(source, edited) if a in CO)
    for full in squares:
        assert decrypt(edited, ranks, full) == text
        assert encrypt(text, ranks, full) == edited
    page = (ROOT / data['case']).read_text()
    assert '> ' + data['readable_german'] in page
    assert re.sub('[^A-Z0-9]', '', data['readable_german'].upper()) == text.replace('X', '')

    # Existing pair identities are recomputed from the native repeated
    # departure reports. The source time is 13.45 in both headers.
    field_data = read(data['linked_fields'])
    field_cells = field_data['square_cells']
    assert [CO[c//6] + CO[c%6] for c in field_cells] == ['FV', 'AF', 'GA', 'GD']
    departure_sources = []
    for identifier in ('p197_E', 'p198_C'):
        r = records[identifier]
        assert '13.45' in r['header_literal']
        raw, pp = positions(clean(r['raw_literal']), ranks, square)
        assert raw.startswith('LASTAUTO1?00')
        assert pp[9]['pair'] == 'AF' and pp[9]['source_indices'] == [47, 151]
        departure_sources.append({'id': identifier, 'header': r['header_literal'],
                                  'hour_position': pp[9]})
    fields, numeric_squares, same_day_squares, non_early_squares = set(), [], [], []
    numeric_same, non_early = set(), set()
    reported_only = []
    for full in squares:
        values = tuple(full[c] for c in field_cells)
        if values[1].isdigit() and 10 + int(values[1]) <= 13:
            reported_only.append(full)
        if not all(c.isdigit() for c in values):
            continue
        fields.add(values)
        numeric_squares.append(full)
        if 10 + int(values[1]) > 13:
            continue
        numeric_same.add(values)
        same_day_squares.append(full)
        if int(values[0]) <= int(values[1]):
            non_early.add(values)
            non_early_squares.append(full)
    assert [len(fields), len(numeric_same), len(non_early)] == [120, 24, 0]
    assert [len(numeric_squares), len(same_day_squares), len(non_early_squares)] == [240, 48, 0]
    assert len(reported_only) == 120
    assert {s[field_cells[1]] for s in reported_only} == {'3'}
    assert {s[field_cells[0]] for s in same_day_squares} == set('4789')
    assert field_data['scenarios'][2]['conditional_cells'] == {'FV': '2', 'AF': '3'}
    assert square[CO.index('V') * 6 + CO.index('G')] == '2'
    return {
        'schema': 'adfgvx-nov13-transport-completion-v1', 'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'transport_inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'square': square, 'completion_count': len(squares),
        'record': {'id': data['record'], 'literal_source': source,
                   'baseline': baseline, 'shared_raw': shared,
                   'edited_ciphertext': edited, 'joint_interpretation': text,
                   'positions': len(text), 'fixed_before': len(baseline) - baseline.count('?'),
                   'fixed_after': len(text), 'new_fixed_positions': gains,
                   'observed_substitutions': [], 'source_mask_fills': [fill],
                   'readable_german': data['readable_german']},
        'departure_sources': departure_sources,
        'scenarios': [
            {'assumptions': 'VG=2 and XX=Q; four distinct transport fields are decimal digits.',
             'field_assignments': len(fields), 'full_squares': len(numeric_squares)},
            {'assumptions': 'Also treat the reported departure as same-day and no later than origin 13:45.',
             'field_assignments': len(numeric_same), 'full_squares': len(same_day_squares),
             'reported_hour': '13:00', 'conditional_AF': '3', 'planned_hour_digit_domain': '4789'},
            {'assumptions': 'Also identify planned and reported movements and prohibit early departure.',
             'field_assignments': 0, 'full_squares': 0,
             'incompatibility': 'The earlier scenario assigns 2 to FV; the award-class hypothesis assigns 2 to distinct VG.'},
        ],
        'reported_time_only': {'assumptions': 'VG=2, XX=Q, and only the reported departure is a same-day clock before 13:45.',
                               'AF': '3', 'full_squares': len(reported_only)},
        'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'transport_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('p189 E: 47/47 conditional labels, 2 observed-pair digits + 1 mask fill, no observed edits; transport scenario counts 120/24/0.')


if __name__ == '__main__':
    main()
