#!/usr/bin/env python3
"""Verify the source-annotation reconstruction of the Kiev unrest report.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, masked_encryption
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_annotations(rows):
    literal, parenthetical, jammed = '', [], []
    for row in rows:
        tokens = row.split()
        for token in tokens:
            if token == '{JAMMED}':
                jammed.append(len(literal))
            elif token.startswith('('):
                assert token.endswith(')') and len(token) == 7
                letters = token[1:-1]
                assert set(letters) <= set(C)
                parenthetical.append({'preceding': [len(literal) - 5, len(literal)],
                                      'parenthesized': [len(literal), len(literal) + 5],
                                      'literal': letters})
                literal += letters
            else:
                assert token and set(token) <= set(C)
                literal += token
    return literal, parenthetical, jammed


def frame(literal, choices, duplicate):
    excluded = set()
    for choice, first, second in zip(choices, [20, 200, 255], [25, 205, 260]):
        assert choice in [0, 1, 2]
        if choice:
            start = first if choice == 2 else second
            excluded.update(range(start, start + 5))
    if duplicate is not None:
        assert duplicate in [0, 5] and literal[duplicate:duplicate + 5] == 'XFXDD'
        excluded.update(range(duplicate, duplicate + 5))
    retained = [i for i in range(len(literal)) if i not in excluded]
    before_jam = next(j for j, i in enumerate(retained) if i >= 85)
    added = 294 - len(retained)
    assert added == 10 + len(excluded)
    mapping = retained[:before_jam] + [None] * added + retained[before_jam:]
    received = ''.join('?' if origin is None else literal[origin] for origin in mapping)
    assert len(received) == len(mapping) == 294
    assert len(set(i for i in mapping if i is not None)) == len(retained)
    return received, mapping, sorted(excluded)


def layer(template, base, mapping, literal, key):
    wanted = masked_encryption(template, key)
    received = ''.join(b if b in C else a for a, b in zip(base, wanted))
    result = inspect(received, key, mapping)
    assert all(a == '?' or a == b for a, b in zip(template, result['raw']))
    substitutions, inserted_fills = [], []
    for i, (a, b) in enumerate(zip(base, received)):
        if a == b:
            continue
        origin = mapping[i]
        event = {'model_index': i, 'source_index': origin,
                 'printed': literal[origin] if origin is not None else None, 'from': a, 'to': b}
        if a in C:
            assert origin is not None
            substitutions.append(event)
        else:
            assert origin is None
            inserted_fills.append(event)
    reconstructed = list(base)
    for event in substitutions + inserted_fills:
        reconstructed[event['model_index']] = event['to']
    assert ''.join(reconstructed) == received
    witness = received.replace('?', 'A')
    plaintext = decrypt(witness, key['column_rank_order'], key['square'])
    assert encrypt(plaintext, key['column_rank_order'], key['square']) == witness
    assert all(a == '?' or a == b for a, b in zip(result['raw'], plaintext))
    return {'template': template, 'ciphertext': received, **result,
            'known_coordinate_substitutions': substitutions, 'printed_mask_fills': [],
            'inserted_slot_fills': inserted_fills,
            'full_completion_witness': {'ciphertext': witness, 'plaintext': plaintext,
                                        'roundtrip_verified': True, 'historical_fill_claim': False}}


def enumerate_models(literal, key, template):
    wanted = masked_encryption(template, key)
    prices, details = [], []
    for choices, duplicate in itertools.product(itertools.product([0, 1, 2], repeat=3), [None, 0, 5]):
        base, mapping, excluded = frame(literal, choices, duplicate)
        cost = sum(a in C and b in C and a != b for a, b in zip(base, wanted))
        fills = sum(a == '?' and b in C for a, b in zip(base, wanted))
        prices.append({'parenthetical_choices': list(choices), 'duplicate_excluded_start': duplicate,
                       'excluded_source_slots': len(excluded), 'added_unknown_slots': base.count('?'),
                       'observed_substitutions': cost, 'inserted_slot_fills': fills})
        details.append((base, mapping, excluded))
    assert len(prices) == len(details) == 81
    minimum = min(row['observed_substitutions'] for row in prices)
    minima = []
    for row, (base, mapping, excluded) in zip(prices, details):
        if row['observed_substitutions'] != minimum:
            continue
        edited = layer(template, base, mapping, literal, key)
        minima.append(dict(row, excluded_source_indices=excluded,
                           raw=decrypt(base, key['column_rank_order'], key['square']),
                           edited_raw=edited['raw'],
                           edited_ciphertext_sha256=hashlib.sha256(edited['ciphertext'].encode()).hexdigest()))
    assert len(minima) == 4
    assert {tuple(r['parenthetical_choices']) for r in minima} == {(1, 2, 0), (2, 2, 0)}
    assert {r['duplicate_excluded_start'] for r in minima} == {0, 5}
    assert len({r['edited_raw'] for r in minima}) == 2
    return {'maps_checked': len(prices), 'all_prices': prices,
            'minimum_observed_substitutions': minimum, 'all_minimum_maps': minima,
            'distinct_edited_streams_at_minimum': len({r['edited_ciphertext_sha256'] for r in minima})}


def fold(text):
    return re.sub('[^A-Z0-9?]', '', text.upper()).replace('X', '')


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov25-28')
    assert len(set(key['square'])) == 36
    prior = data['prior_ocr']
    assert sha(HERE / prior['path']) == prior['sha256']
    assert sha(ROOT / prior['source_path']) == prior['source_sha256']
    assert load(HERE / prior['path']) == next(r for r in load(ROOT / prior['source_path'])['blocks']
                                             if r['id'] == prior['source_record_id'])
    record = data['records'][0]
    literal, parentheses, jammed = parse_annotations(record['source_rows_annotated'])
    assert literal == ''.join(''.join(record['source_rows']).split())
    assert len(literal) == record['source_slots'] == 284 and set(literal) <= set(C)
    assert parentheses == data['annotations']['parenthesized_groups'] and jammed == [85]
    assert literal[:5] == literal[5:10] == 'XFXDD'
    native = inspect(literal, key, list(range(len(literal))))
    assert native['fixed_positions'] == 142
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    af = record['analysis_frame']
    base, mapping, excluded = frame(literal, af['parenthesized_choices'], af['duplicate_prefix_excluded_start'])
    assert excluded == af['excluded_source_indices'] and len(excluded) == 15
    assert base.count('?') == af['unknown_inserted_slots'] == 25
    raw = inspect(base, key, mapping)
    assert raw['fixed_positions'] == 122
    primary = layer(data['primary_template'], base, mapping, literal, key)
    optional = {name: layer(template, base, mapping, literal, key)
                for name, template in data['optional_templates'].items()}
    assert (primary['fixed_positions'], len(primary['known_coordinate_substitutions']),
            len(primary['inserted_slot_fills'])) == (139, 0, 17)
    expected_prices = {'leader': (140, 4, 18), 'odessa': (139, 1, 17),
                       'signature': (141, 2, 19), 'combined': (142, 7, 20)}
    for name, candidate in optional.items():
        assert (candidate['fixed_positions'], len(candidate['known_coordinate_substitutions']),
                len(candidate['inserted_slot_fills'])) == expected_prices[name]
    scopes = {'primary': enumerate_models(literal, key, data['primary_template']),
              'optional_combined': enumerate_models(literal, key, data['optional_templates']['combined'])}
    assert scopes['primary']['minimum_observed_substitutions'] == 0
    assert scopes['optional_combined']['minimum_observed_substitutions'] == 7
    for i in [66, 67, 78, 115, 117, 119, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136]:
        assert primary['raw'][i] == raw['raw'][i]
    assert primary['raw'][78] == '?'  # Do not invent the incomplete modifier's ending.
    text = (ROOT / data['case']).read_text()
    assert text.count(expected_legend(ROOT / data['case'])) == 1
    fences, quotes = displays(text)
    assert [r['role_from_caption'] for r in fences] == ['raw_output', 'edited_output', 'edited_output', 'source_transcription']
    assert [r['role_from_caption'] for r in quotes] == ['readable_german', 'readable_german']
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    assert bodies[:3] == [raw['raw'], primary['raw'], optional['combined']['raw']]
    assert bodies[3].splitlines() == record['source_rows_annotated']
    displayed_quotes = re.findall(r'^> (.*)$', text, re.M)
    assert displayed_quotes == [data['readable_quotes']['primary'], data['readable_quotes']['optional']]
    for displayed, candidate in zip(displayed_quotes, [primary, optional['combined']]):
        excerpt = ''.join(candidate['raw'][start:end] for start, end in data['quote_spans'])
        assert fold(displayed) == fold(excerpt)
    summary = {'physical_records': 1, 'printed_source_slots': 284, 'valid_source_coordinates': 284,
               'printed_masks': 0, 'excluded_observed_coordinates': 15, 'added_unknown_slots': 25,
               'modeled_coordinates': 294, 'plaintext_positions': 147, 'raw_fixed_positions': 122,
               'zero_substitution_lexical_fixed_positions': 139, 'zero_substitution_added_slot_fills': 17,
               'optional_combined_fixed_positions': 142, 'optional_combined_observed_substitutions': 7,
               'optional_combined_added_slot_fills': 20}
    return {'schema': 'adfgvx-p219-kiev-unrest-certificate-v1', 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': data['indexing'], 'summary': summary,
            'records': [{'id': record['id'], 'literal_source': literal, 'source_slots': 284,
                         'ciphertext': base, 'model_to_source_indices': mapping,
                         'excluded_source_indices': excluded, **raw, 'native_baseline': native,
                         'readable_candidate': primary, 'optional_name_candidates': optional}],
            'geometry_enumerations': scopes, 'prior_credit': data['prior_credit'], 'limits': data['limits']}, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    certificate, evidence = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert certificate == load(path)
    else:
        path.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
