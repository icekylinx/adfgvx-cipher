#!/usr/bin/env python3
"""Test the late-November calendar and unit assignments against native sources."""
from datetime import date
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
    rec = next(r for r in read(spec['inputs'])['records'] if r['id'] == spec['id'])
    source = literal(rec)
    old = read(spec['certificate'])
    if spec['edition'] == 'shared_J':
        cert = next(r for r in old['shared_J']['records'] if r['id'] == spec['id'])
        edited = cert['new_ciphertext']
        assert cert['literal'] == source
    else:
        cert = next(r for r in old['records'] if r['id'] == spec['id'])
        edited = cert['edition']['ciphertext']
    assert len(source) == len(edited)
    changes = [{'source_index': i, 'from': a, 'to': b}
               for i, (a, b) in enumerate(zip(source, edited)) if a in CO and a != b]
    fills = [{'source_index': i, 'literal': a, 'to': b}
             for i, (a, b) in enumerate(zip(source, edited)) if a not in CO and b in CO]
    assert len(changes) == spec['earlier_substitutions']
    assert len(fills) == spec['earlier_fills']
    return source, edited, changes, fills


def check_quote(spec, records):
    page = (ROOT / spec['case']).read_text()
    quotes = [' '.join(line[2:] for line in match[0].splitlines())
              for match in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', page, re.M)]
    assert spec['german'] in quotes
    labels = re.sub('[^A-Z0-9?]', '', spec['german'].upper())
    expected = ''.join(records[name]['interpreted_edition'] for name in spec['records'])
    assert labels == expected.replace('X', '')


def build():
    data = json.loads((HERE / 'inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    for crop in data['historical_source']['crops']:
        assert hashlib.sha256((HERE / crop['path']).read_bytes()).hexdigest() == crop['sha256']
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == data['key_id'])
    ranks = key['column_rank_order']
    prior = read('experiments/late_november_joint_completion/inputs.json')['shared_J']['new_square']
    assert prior == data['prior_square']
    sources = {s['id']: load_record(s) for s in data['records']}
    source_a1 = clean(sources['p229_A1'][0])
    prior_squares = list(completions(prior))
    assert len(prior_squares) == 24

    # The five-character field is a November day/month, not an arbitrary serial.
    calendar_witnesses = []
    proposed_days = set()
    for square in prior_squares:
        raw = decrypt(source_a1, ranks, square)
        day, month = int(raw[13:15]), int(raw[16:18])
        proposed_days.add(day)
        assert month == 11 and raw[15] == 'X'
        if 1 <= day <= 30:
            assert date(1918, month, day).isoformat() == '1918-11-30'
            calendar_witnesses.append(square)
    assert proposed_days == {30, 34, 35, 37} and len(calendar_witnesses) == 6
    ga = CO.index('G') * 6 + CO.index('A')
    vg = CO.index('V') * 6 + CO.index('G')
    assert {s[ga] for s in calendar_witnesses} == {'0'}
    calendar = list(prior)
    calendar[ga] = '0'
    calendar = ''.join(calendar)
    assert calendar == data['calendar_square']
    assert set(completions(calendar)) == set(calendar_witnesses)

    # The independently documented 217th Division and 7th Bavarian cavalry
    # brigade both use the same received VG cell in different telegrams.
    unit_witnesses = []
    for square in calendar_witnesses:
        a1 = decrypt(source_a1, ranks, square)
        a4 = decrypt(clean(sources['p230_A4'][0]), ranks, square)
        if a1[93:96] == '217' and a4[26] == '7':
            unit_witnesses.append(square)
    assert len(unit_witnesses) == 2 and {s[vg] for s in unit_witnesses} == {'7'}
    final = list(calendar)
    final[vg] = '7'
    final = ''.join(final)
    assert final == data['unit_square'] and set(completions(final)) == set(unit_witnesses)
    records = {}
    for spec in data['records']:
        source, edited, changes, fills = sources[spec['id']]
        native = clean(source)
        before, _ = positions(edited, ranks, prior)
        intermediate, _ = positions(edited, ranks, calendar)
        after, ps = positions(edited, ranks, final)
        raw_after, raw_ps = positions(native, ranks, final)
        new = []
        for p, (old, new_label) in enumerate(zip(before, after)):
            if old == '?' and new_label != '?':
                assert ps[p]['pair'] in ('GA', 'VG')
                assert raw_ps[p]['pair'] == ps[p]['pair']
                assert all(source[i] in CO for i in ps[p]['source_indices'])
                new.append({**ps[p], 'symbol': new_label})
        assert len(new) == spec['new_fixed_positions']
        witnesses = []
        for square in unit_witnesses:
            witness = {'remaining_assignment': {
                CO[i // 6] + CO[i % 6]: square[i] for i, c in enumerate(final) if c == '?'}}
            for label, cipher in [('native', native), ('edition', edited)]:
                completed_cipher = cipher.replace('?', 'A')
                text = decrypt(completed_cipher, ranks, square)
                assert encrypt(text, ranks, square) == completed_cipher
                assert all(a == '?' or a == b for a, b in zip(cipher, completed_cipher))
                _, domains = positions(cipher, ranks, final)
                assert all(ch in p['domain'] for ch, p in zip(text, domains))
                witness[label] = {'plaintext': text, 'ciphertext': completed_cipher,
                                  'arbitrary_mask_fills_are_not_readings': True}
            witnesses.append(witness)
        records[spec['id']] = {
            'id': spec['id'], 'source_slots': len(source), 'positions': len(after),
            'literal': source, 'native_interpretation': raw_after,
            'prior_interpretation': before, 'calendar_interpretation': intermediate,
            'interpreted_edition': after, 'edition_ciphertext': edited,
            'fixed_before': len(before) - before.count('?'),
            'fixed_after_calendar': len(intermediate) - intermediate.count('?'),
            'fixed_after_units': len(after) - after.count('?'),
            'new_fixed_positions': new,
            'earlier_observed_substitutions': changes, 'earlier_mask_fills': fills,
            'additional_observed_substitutions': [], 'additional_mask_fills': [],
            'remaining_domains': [p for p in ps if len(p['domain']) != 1],
            'global_witnesses': witnesses,
        }
    a2 = records['p229_A2']['interpreted_edition']
    assert a2.startswith('SEIT29X11XABENDS')
    assert records['p230_A4']['interpreted_edition'].startswith('89XUND3L3X')
    assert '7XBAYRXKAVXBRIG' in records['p230_A4']['interpreted_edition']
    for spec in data['readable_quotes']:
        check_quote(spec, records)
    for row in data['case_fields']:
        value = records[row['id']]['interpreted_edition'][row['start']:row['end']]
        assert value == row['field']
        assert row['text'] in (ROOT / row['case']).read_text()
    gains = sum(len(r['new_fixed_positions']) for r in records.values())
    assert gains == 13
    return {
        'schema': 'adfgvx-late-november-calendar-units-certificate-v1',
        'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'squares': {'prior': prior, 'calendar': calendar, 'units': final,
                    'counts': [24, 6, 2], 'remaining_symbols': '45'},
        'calendar_candidate_days': sorted(proposed_days),
        'calendar_valid_day': 30,
        'new_fixed_positions': gains,
        'records_with_new_positions': sum(bool(r['new_fixed_positions']) for r in records.values()),
        'records': list(records.values()),
        'readable_quotes_verified': data['readable_quotes'],
        'case_fields_verified': data['case_fields'],
        'limits': data['limits'],
    }


def check_pdf(path):
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
        check_pdf(args.historical_pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Late-November date + unit interpretation: 24 → 6 → 2 squares; 13 new numeral positions in 7 records; no added source edits.')


if __name__ == '__main__':
    main()
