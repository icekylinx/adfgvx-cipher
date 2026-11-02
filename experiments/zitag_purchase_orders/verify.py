#!/usr/bin/env python3
"""Verify the ZITAG source copies, exact witnessed repairs and contract-cancellation message.

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


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    keys = json.loads((ROOT/'data/keys.json').read_text())['keys']
    assert key == next(k for k in keys if k['id'] == key['id'])
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path']) == crop['sha256']
    if pdf:
        verify_crops(pdf, inputs['source'], inputs['source_images'], HERE)
    records = []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        assert len(literal) == source['source_slots'] == source['advertised_length']
        base = ''.join(c if c in C else '?' for c in literal)
        mapping = list(range(len(base)))
        raw = inspect(base, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], base, key, mapping, literal)
        records.append({'id': source['id'], 'literal_source': literal,
                        'source_slots': len(literal),
                        'valid_source_coordinates': sum(c in C for c in literal),
                        'ciphertext': base, 'model_to_source_indices': mapping,
                        **raw, 'readable_candidate': candidate})
    assert [len(r['raw']) for r in records] == [90, 90, 90, 137, 127]
    assert [r['fixed_positions'] for r in records] == [90, 90, 90, 137, 124]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [2, 1, 1, 10, 0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records] == [0, 0, 0, 0, 3]
    by_id = {r['id']: r for r in records}
    copies = [by_id[ident] for ident in inputs['cross_copy_records']]
    target = copies[0]['readable_candidate']['ciphertext']
    assert all(r['readable_candidate']['ciphertext'] == target for r in copies)
    assert all(r['readable_candidate']['raw'] == inputs['cross_copy_candidate'] for r in copies)
    varying = [i for i in range(180) if len({r['literal_source'][i] for r in copies}) > 1]
    assert varying == [29, 55, 162]
    witnesses = []
    for i, coordinate in enumerate(target):
        support = [r['id'] for r in copies if r['literal_source'][i] == coordinate]
        assert support
        witnesses.append({'source_index': i, 'candidate_coordinate': coordinate,
                          'supporting_source_records': support,
                          'all_observed_readings': {r['id']: r['literal_source'][i] for r in copies}})
    pairwise = []
    for i, left in enumerate(copies):
        for right in copies[i+1:]:
            differences = [j for j in range(180) if left['literal_source'][j] != right['literal_source'][j]]
            pairwise.append({'left': left['id'], 'right': right['id'],
                             'same_length': 180, 'differing_source_indices': differences,
                             'matching_source_coordinates': 180-len(differences)})
    altered_plaintext = []
    for record in copies:
        for raw, candidate in zip(record['positions'], record['readable_candidate']['positions']):
            if raw['raw'] != candidate['raw']:
                altered_plaintext.append({'record': record['id'], 'raw_position': raw,
                                          'candidate_position': candidate,
                                          'candidate_pair_witnesses': [witnesses[i] for i in candidate['source_indices']]})
    b1 = by_id['p103_B1']
    numeric_fields = []
    for text in ['NRX5', '6MILLIONEN', 'NRX3']:
        begin = b1['raw'].index(text)
        positions = b1['positions'][begin:begin+len(text)]
        assert positions == b1['readable_candidate']['positions'][begin:begin+len(text)]
        numeric_fields.append({'record': b1['id'], 'raw_field': text,
                               'plaintext_start': begin, 'positions': positions,
                               'all_observed_pairs_unchanged': True})
    b2 = by_id['p103_B2']
    begin = b2['raw'].index('WESTERNHAGEN')
    name = {'record': b2['id'], 'raw_field': 'WESTERNHAGEN',
            'plaintext_start': begin, 'positions': b2['positions'][begin:begin+12],
            'identity_assigned': False}
    assert name['positions'] == b2['readable_candidate']['positions'][begin:begin+12]
    inventory = [{'record': r['id'], 'variant': variant, 'raw': reading['raw'],
                  'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                    if p['raw'] in '0123456789JQY']}
                 for r in records
                 for variant, reading in [('source_model', r),
                                          ('ordinary_word_candidate', r['readable_candidate'])]]
    return {'schema': 'adfgvx-zitag-purchase-order-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 5, 'printed_source_slots': 1068,
                        'valid_source_coordinates': 1065, 'modeled_coordinates': 1068,
                        'plaintext_positions': 534, 'baseline_fixed_positions': 531,
                        'candidate_fixed_positions': 534,
                        'known_coordinate_substitutions': 14,
                        'printed_erasure_fills': 3, 'source_deletions': 0,
                        'missing_coordinate_insertions': 0, 'published_key_changed': False},
            'records': records,
            'cross_copy_certificate': {'assumption': inputs['cross_copy_assumption'],
                                       'shared_candidate_plaintext': inputs['cross_copy_candidate'],
                                       'shared_candidate_ciphertext': target,
                                       'all_varying_source_indices': varying,
                                       'pairwise_comparisons': pairwise,
                                       'all_180_coordinate_witnesses': witnesses,
                                       'all_changed_plaintext_positions': altered_plaintext,
                                       'every_candidate_coordinate_has_a_literal_source_witness': True,
                                       'majority_vote_claimed': False},
            'unchanged_numeric_fields': numeric_fields,
            'unchanged_name_field': name,
            'complete_raw_label_inventory': inventory,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['A common-original assumption and ordinary wording motivate the cross-copy candidate; the three copies do not prove which version was originally transmitted.',
                       'The neighboring contract-cancellation message is not treated as an exact repeat of the stop-order.',
                       'Raw amount 6 and references 5/3 are preserved as published-square labels; no numerical relabeling is inferred.',
                       'Raw 4, 1, 5 inside damaged ordinary words are explicitly retained before their candidate repairs.',
                       'WESTERNHAGEN is a received name, not an independently identified individual.',
                       'The orders do not establish completed cancellation, shipment, return or receipt of rubles.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    target = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
