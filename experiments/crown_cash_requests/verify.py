#!/usr/bin/env python3
"""Verify crown-cash requests, exact coordinate repairs and all untouched amount labels.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No published substitution square or numerical label is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation(length, ranks):
    """Independent column-offset inverse: interim index -> model index."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (i < length % width) for i in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[i])
              for i in range(width)]
    order = [starts[i % width] + i // width for i in range(length)]
    assert sorted(order) == list(range(length))
    return order


def inspect(cipher, key, mapping):
    square, ranks = key['square'], key['column_rank_order']
    assert len(cipher) % 2 == 0 and len(mapping) == len(cipher)
    order = permutation(len(cipher), ranks)
    middle = ''.join(cipher[j] for j in order)
    assert middle == untranspose(cipher, ranks)
    unused = set(A) - set(square)
    positions = []
    for i in range(len(cipher) // 2):
        pair = middle[2*i:2*i+2]
        cells = [6*r+c for r in range(6) for c in range(6)
                 if pair[0] in ('?', C[r]) and pair[1] in ('?', C[c])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        indices = order[2*i:2*i+2]
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices],
                          'domain': domain,
                          'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    return {'raw': raw, 'fixed_positions': sum(p['raw'] != '?' for p in positions),
            'positions': positions}


def masked_encryption(template, key):
    square = key['square']
    middle = ''.join('??' if ch == '?' else C[square.index(ch)//6] + C[square.index(ch) % 6]
                     for ch in template)
    target = [None] * len(middle)
    for ch, i in zip(middle, permutation(len(middle), key['column_rank_order'])):
        target[i] = ch
    return ''.join(target)


def repair(template, base, key, mapping, literal):
    assert len(template)*2 == len(base)
    stencil = masked_encryption(template, key)
    target = ''.join(a if b == '?' else b for a, b in zip(base, stencil))
    result = inspect(target, key, mapping)
    assert result['raw'] == template
    substitutions, fills = [], []
    for i, (a, b) in enumerate(zip(base, target)):
        if a == b:
            continue
        source_i = mapping[i]
        event = {'model_index': i, 'source_index': source_i,
                 'printed': literal[source_i] if source_i is not None else None,
                 'from': a, 'to': b}
        (fills if a == '?' else substitutions).append(event)
    rebuilt = list(base)
    for event in substitutions + fills:
        rebuilt[event['model_index']] = event['to']
    assert ''.join(rebuilt) == target
    if '?' not in template:
        assert target == encrypt(template, key['column_rank_order'], key['square'])
    return {'template': template, 'ciphertext': target,
            'known_coordinate_substitutions': substitutions,
            'erased_coordinate_fills': fills,
            'full_plaintext_reencryption_verified': '?' not in template,
            'published_key_changed': False, **result}


def verify_crops(pdf, expected, crops, relative_to):
    import fitz
    from PIL import Image
    assert pdf.stat().st_size == expected['pdf_bytes']
    assert sha(pdf) == expected['pdf_sha256']
    doc = fitz.open(pdf)
    for crop in crops:
        rect = crop.get('crop_pdf_points', crop.get('clip_points'))
        scale = crop.get('render_scale', crop.get('scale'))
        pix = doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*rect))
        im = Image.open(relative_to/crop['path']).convert('RGB')
        assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples


def field(record, text):
    start = record['raw'].index(text)
    positions = record['positions'][start:start+len(text)]
    return {'record': record['id'], 'raw_label_field': text, 'plaintext_start': start,
            'plaintext_end_exclusive': start+len(text), 'positions': positions}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    current = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    assert key == current[key['id']]
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path']) == crop['sha256']
    if pdf:
        verify_crops(pdf, inputs['source'], inputs['source_images'], HERE)
    records, inventory = [], []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        assert set(literal) <= set(C)
        assert len(literal) == source['source_slots'] == source['advertised_length']
        mapping = list(range(len(literal)))
        raw = inspect(literal, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], literal, key, mapping, literal)
        record = {'id': source['id'], 'literal_source': literal, 'ciphertext': literal,
                  'source_slots': len(literal), 'valid_coordinates': len(literal),
                  'model_to_source_indices': mapping, **raw, 'readable_candidate': candidate}
        records.append(record)
        for label, reading in [('source_model', raw), ('ordinary_word_candidate', candidate)]:
            inventory.append({'record': source['id'], 'variant': label, 'raw': reading['raw'],
                              'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                                if p['raw'] in '0123456789JQY']})
    assert [len(r['raw']) for r in records] == [167, 115, 177]
    assert [r['fixed_positions'] for r in records] == [167, 115, 177]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [1, 3, 2]
    assert all(not r['readable_candidate']['erased_coordinate_fills'] for r in records)
    intact = []
    for record, token in [(records[0], 'JJFIALA'), (records[0], '6MIL'),
                           (records[0], '3YYYYY'), (records[0], 'OBLTXKUDEL'),
                           (records[2], 'AXOXKXJJ'), (records[2], 'J3Y20'),
                           (records[2], 'ROEM4BJ411XJYJ2')]:
        witness = field(record, token)
        for point in witness['positions']:
            i = point['plaintext_index']
            assert point == record['readable_candidate']['positions'][i]
            assert all(record['ciphertext'][j] == record['readable_candidate']['ciphertext'][j]
                       for j in point['source_indices'])
        witness['all_observed_pairs_unchanged'] = True
        intact.append(witness)
    support = {'assumption': 'The two physically consecutive parts refer to the same office and place; they are not exact retransmissions.',
               'unchanged_MGD_in_A2': field(records[1], 'MGD'),
               'unchanged_ARAD_in_A1': field(records[0], 'ARAD'),
               'candidate_MG0_to_MGD_in_A1': {'before': field(records[0], 'MG0'),
                                           'ciphertext_repair': records[0]['readable_candidate']['known_coordinate_substitutions']},
               'candidate_ARPD_to_ARAD_in_A2': {'before': field(records[1], 'ARPD'),
                                             'plaintext_after': 'ARAD'},
               'limits': 'MGD is not expanded; FIALA and KUDEL are not identified as particular people.'}
    for record, witness in [(records[1], support['unchanged_MGD_in_A2']),
                            (records[0], support['unchanged_ARAD_in_A1'])]:
        for p in witness['positions']:
            assert p == record['readable_candidate']['positions'][p['plaintext_index']]
    counts = {label: sum(p['raw'] in '0123456789JQY' for r in records
                         for p in (r if label == 'source_model' else r['readable_candidate'])['positions'])
              for label in ['source_model', 'ordinary_word_candidate']}
    return {'schema': 'adfgvx-crown-cash-request-certificate-v1', 'project': inputs['project'],
            'authors': inputs['authors'], 'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 3, 'printed_source_slots': 918,
                        'valid_source_coordinates': 918, 'modeled_coordinates': 918,
                        'plaintext_positions': 459, 'baseline_fixed_positions': 459,
                        'candidate_fixed_positions': 459, 'known_coordinate_substitutions': 6,
                        'source_or_model_erasure_fills': 0, 'source_deletions': 0,
                        'published_key_changed': False},
            'records': records, 'untouched_amount_name_army_and_reference_fields': intact,
            'within_message_office_and_place_support': support,
            'complete_raw_label_inventory': inventory, 'selected_model_label_counts': counts,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The 459 fixed positions are published-square labels, not newly solved key symbols or established numerical values.',
                       'Raw 6 MIL, 3YYYYY and all army/reference labels remain unassigned.',
                       'The ordinary-word candidates separately repair raw0 in MG0 and raw9 in MOEGLICHK9IT; both are retained in the full source inventory.',
                       'A and B concern crown liquidity, but the source does not establish that B answers this precise A request.',
                       'The reported partial transfer and requested advance are not evidence of completed full payment.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary'],
                      'selected_model_label_counts': result['selected_model_label_counts']}, indent=2))


if __name__ == '__main__':
    main()
