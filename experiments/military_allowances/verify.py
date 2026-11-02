#!/usr/bin/env python3
"""Verify the four-part military allowance message, source assembly and exact repairs.

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
    source_records = inputs['records']
    assembly = inputs['cross_page_assembly']
    assert [r['id'] for r in source_records] == assembly['record_order']
    assert [r['message_part'] for r in source_records] == [1, 2, 3, 4]
    assert all(r['message_total_parts'] == 4 for r in source_records)
    assert all(r['common_receipt_header'] == assembly['shared_receipt'] for r in source_records)
    assert all(r['common_origin_header'] == assembly['shared_origin'] for r in source_records)
    records = []
    for source in source_records:
        literal = ''.join(''.join(source['source_rows']).split())
        assert len(literal) == source['source_slots'] == source['advertised_length']
        base = ''.join(c if c in C else '?' for c in literal)
        mapping = list(range(len(base)))
        raw = inspect(base, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], base, key, mapping, literal)
        records.append({'id': source['id'], 'message_part': source['message_part'],
                        'literal_source': literal, 'source_slots': len(literal),
                        'valid_source_coordinates': sum(c in C for c in literal),
                        'ciphertext': base, 'model_to_source_indices': mapping,
                        **raw, 'readable_candidate': candidate})
    assert [r['source_slots'] for r in records] == [398, 452, 486, 424]
    assert [len(r['raw']) for r in records] == [199, 226, 243, 212]
    assert [r['fixed_positions'] for r in records] == [197, 225, 243, 212]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [5, 4, 0, 1]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records] == [2, 1, 0, 0]
    intact = []
    for record, text in [(records[0], 'XMXRMX30NRX228'),
                          (records[3], 'PASCHEXRMX2'),
                          (records[3], 'NRX1235X18XGXBX1')]:
        start = record['raw'].index(text)
        positions = record['positions'][start:start+len(text)]
        assert positions == record['readable_candidate']['positions'][start:start+len(text)]
        intact.append({'record': record['id'], 'raw_field': text,
                       'plaintext_start': start, 'positions': positions,
                       'all_observed_pairs_unchanged': True})
    third = records[2]
    assert third['raw'] == third['readable_candidate']['raw']
    assert third['literal_source'] == third['readable_candidate']['ciphertext']
    assert third['readable_candidate']['full_plaintext_reencryption_verified']
    assert third['literal_source'].startswith('VAGAG')
    assert third['literal_source'].endswith('GXFVDA')
    direct = {'record': third['id'], 'plaintext_positions': 243,
              'raw': third['raw'], 'first_source_group': third['literal_source'][:5],
              'final_source_groups': ['GXFVD', 'A'],
              'all_source_pairs_complete': all('?' not in p['pair'] for p in third['positions']),
              'exact_unmodified_ciphertext_reencryption': True,
              'coordinate_repair_count': 0}
    inventory = [{'record': r['id'], 'variant': variant, 'raw': reading['raw'],
                  'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                    if p['raw'] in '0123456789JQY']}
                 for r in records
                 for variant, reading in [('source_model', r),
                                          ('ordinary_word_candidate', r['readable_candidate'])]]
    return {'schema': 'adfgvx-military-allowance-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 4, 'printed_source_slots': 1760,
                        'valid_source_coordinates': 1757, 'modeled_coordinates': 1760,
                        'plaintext_positions': 880, 'baseline_fixed_positions': 877,
                        'candidate_fixed_positions': 880,
                        'known_coordinate_substitutions': 10,
                        'printed_erasure_fills': 3, 'source_deletions': 0,
                        'missing_coordinate_insertions': 0, 'published_key_changed': False},
            'records': records,
            'cross_page_assembly': assembly,
            'direct_unchanged_third_part': direct,
            'unchanged_reference_fields': intact,
            'complete_raw_label_inventory': inventory,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The four parts are assembled using explicit matching headers and numbered parts, not assumed page adjacency.',
                       'No particular Swedish allowance schedule is identified or reconstructed.',
                       'PASCHE is a received reference word; no unverified title, edition or author is supplied.',
                       'The initial RM 30 and final RM 2 / NR X 1235 X 18 X G X B X 1 fields retain their raw labels.',
                       'The raw 0 punctuation candidate in A4 is a coordinate repair, not a global numerical relabeling.',
                       'The order is evidence of requested policy and a refused supplement, not proof that rates were actually reduced or communal kitchens established.']}


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
