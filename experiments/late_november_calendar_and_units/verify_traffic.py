#!/usr/bin/env python3
"""Apply the two late-November squares to four further traffic records."""
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


def build():
    data = json.loads((HERE / 'additional_traffic.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    common = read('experiments/late_november_calendar_and_units/inputs.json')
    partial = common['unit_square']
    squares = list(completions(partial))
    assert len(squares) == 2
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == common['key_id'])
    ranks = key['column_rank_order']
    records = {}
    for spec in data['records']:
        original = next(r for r in read(spec['inputs'])['records'] if r['id'] == spec['id'])
        cert = next(r for r in read(spec['certificate'])['records'] if r['id'] == spec['id'])
        source = literal(original)
        assert source == cert[spec['literal_field']]
        edited = cert[spec['edition_field']]['ciphertext']
        assert len(source) == len(edited)
        before, before_positions = positions(edited, ranks, partial)
        older, _ = positions(edited, ranks, common['prior_square'])
        new_numerals = []
        for p, (old, new) in enumerate(zip(older, before)):
            if old == '?' and new != '?':
                pos = before_positions[p]
                assert pos['pair'] in ('GA', 'VG')
                assert all(source[i] == edited[i] and source[i] in CO
                           for i in pos['source_indices'])
                new_numerals.append({**pos, 'symbol': new})
        additional = spec.get('additional_mask_fill')
        revised = list(edited)
        support = None
        if additional:
            p, i, value = (additional[k] for k in ('plaintext_index', 'source_index', 'to'))
            support = before_positions[p]
            assert source[i] not in CO and edited[i] == '?' and i in support['source_indices']
            assert support['pair'].count('?') == 1
            revised[i] = value
        revised = ''.join(revised)
        after, ps = positions(revised, ranks, partial)
        assert after == spec['expected_interpretation']
        changes = [{'source_index': i, 'from': a, 'to': b}
                   for i, (a, b) in enumerate(zip(source, revised)) if a in CO and a != b]
        fills = [{'source_index': i, 'literal': a, 'to': b}
                 for i, (a, b) in enumerate(zip(source, revised)) if a not in CO and b in CO]
        assert len(changes) == spec['observed_substitutions']
        assert len(fills) == spec['source_mask_fills']
        assert all(a == b for a, b in zip(edited, revised) if a in CO)
        witnesses = []
        for square in squares:
            completed = revised.replace('?', 'A')
            text = decrypt(completed, ranks, square)
            assert encrypt(text, ranks, square) == completed
            assert all(ch in pos['domain'] for ch, pos in zip(text, ps))
            witnesses.append({'square': square, 'plaintext': text,
                              'ciphertext': completed,
                              'arbitrary_mask_fills_are_not_readings': True})
        variants = []
        for variant in cert.get('source_variants', []):
            variant_source = variant['literal_source']
            interpretation, domains = positions(variant_source, ranks, partial)
            for square in squares:
                text = decrypt(variant_source, ranks, square)
                assert encrypt(text, ranks, square) == variant_source
            variants.append({'name': variant['name'], 'literal_source': variant_source,
                             'interpretation': interpretation,
                             'remaining_domains': [p for p in domains if len(p['domain']) != 1]})
        records[spec['id']] = {
            'id': spec['id'], 'literal_source': source,
            'prior_edition_ciphertext': edited, 'conditional_ciphertext': revised,
            'before': before, 'interpretation': after,
            'native_interpretation': positions(clean(source), ranks, partial)[0],
            'positions': len(after), 'fixed_before': len(before) - before.count('?'),
            'fixed_after': len(after) - after.count('?'),
            'new_numeral_positions': new_numerals,
            'additional_fill_support': support, 'additional_mask_fill': additional,
            'observed_substitutions': changes, 'source_mask_fills': fills,
            'remaining_domains': [p for p in ps if len(p['domain']) != 1],
            'global_witnesses': witnesses, 'source_variants': variants,
        }

    # A digit before DEZ fixes its missing coordinate, even though the digit
    # itself depends on the still-interchangeable FX/DX values.
    radio = records['p226_A2']
    original = radio['prior_edition_ciphertext']
    date_branches = []
    for square in squares:
        choices = []
        for value in CO:
            candidate = original[:23] + value + original[24:]
            text = decrypt(candidate, ranks, square)
            if text[0].isdigit():
                assert text[1:4] == 'DEZ'
                choices.append((value, text[0], text[53:55]))
        assert len(choices) == 1 and choices[0][0] == 'X'
        hour = decrypt(records['p230_C']['conditional_ciphertext'], ranks, square)[21]
        date_branches.append({'day_in_december': int(choices[0][1]),
                              'schwere_field': choices[0][2], 'p230_C_hour': hour,
                              'square': square})
    date_branches.sort(key=lambda b: b['day_in_december'])
    assert [(b['day_in_december'], b['schwere_field'], b['p230_C_hour'])
            for b in date_branches] == [(4, '15', '5'), (5, '14', '4')]
    p229 = records['p229_C']
    assert p229['interpretation'][77:87] == 'WIRDXBITTE'
    assert p229['additional_fill_support']['domain'] == '145WXZ'
    p230 = records['p230_D']
    assert p230['interpretation'][89:94] == '98179'
    assert decrypt(clean(p230['literal_source']), ranks, common['prior_square'])[92] == '?'
    _, native_positions = positions(clean(p230['literal_source']), ranks, partial)
    assert native_positions[92]['pair'] == 'VG'
    assert native_positions[92]['source_indices'] == [187, 128]
    assert sum(len(r['new_numeral_positions']) for r in records.values()) == 3

    quote = data['readable_quote']
    page = (ROOT / quote['case']).read_text()
    quotes = [' '.join(line[2:] for line in match[0].splitlines())
              for match in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', page, re.M)]
    assert quote['german'] in quotes
    labels = re.sub('[^A-Z0-9?]', '', quote['german'].upper())
    assert labels == p229['interpretation'].replace('X', '')
    for field in data['displayed_fields']:
        assert field['text'] in (ROOT / field['case']).read_text()
    return {
        'schema': 'adfgvx-late-november-additional-traffic-v1',
        'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'additional_traffic.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'conditional_square': partial, 'square_count': len(squares),
        'records': list(records.values()), 'date_branches': date_branches,
        'additional_observed_changes': 0,
        'additional_mask_fills': 2,
        'additional_fixed_plaintext_position': {'record': 'p229_C', 'position': 81},
        'additional_VG_numerals_outside_the_original_snapshot': 3,
        'p230_D_footer_positions': native_positions[89:94],
        'readable_quote_verified': quote, 'displayed_fields_verified': data['displayed_fields'],
        'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'traffic_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Additional late-November traffic: two conditional mask fills, one new separator; date/station alternatives 4/15 and 5/14; footer 98179.')


if __name__ == '__main__':
    main()
