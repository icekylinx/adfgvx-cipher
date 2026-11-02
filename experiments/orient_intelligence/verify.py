#!/usr/bin/env python3
"""Verify the six-part Orient intelligence report and every exact source repair.

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
    points = record['positions'][start:start+len(text)]
    assert points == record['readable_candidate']['positions'][start:start+len(text)]
    return {'record': record['id'], 'raw_field': text, 'plaintext_start': start,
            'positions': points, 'all_observed_pairs_unchanged': True}


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
    assembly = inputs['cross_page_assembly']
    source_records = inputs['records']
    assert [r['id'] for r in source_records] == assembly['record_order']
    assert [r['message_part'] for r in source_records] == [1, 2, 3, 4, 5, 6]
    assert all(r['message_total_parts'] == 6 for r in source_records)
    for source_key, assembly_key in [('common_receipt_header', 'shared_receipt'),
                                     ('common_address_header', 'shared_address'),
                                     ('common_origin_header', 'shared_origin')]:
        assert all(r[source_key] == assembly[assembly_key] for r in source_records)
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
    assert [r['source_slots'] for r in records] == [328, 252, 394, 328, 368, 350]
    assert [len(r['raw']) for r in records] == [164, 126, 197, 164, 184, 175]
    assert [r['fixed_positions'] for r in records] == [164, 126, 197, 164, 183, 175]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [3, 0, 0, 0, 1, 0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records] == [0, 0, 0, 0, 1, 0]
    direct = []
    for i in [1, 2, 3, 5]:
        record = records[i]
        assert record['raw'] == record['readable_candidate']['raw']
        assert record['literal_source'] == record['readable_candidate']['ciphertext']
        assert record['readable_candidate']['full_plaintext_reencryption_verified']
        direct.append({'record': record['id'], 'plaintext_positions': len(record['raw']),
                       'raw': record['raw'], 'exact_unmodified_ciphertext_reencryption': True})
    # Every numeral is preserved except the separately priced ordinary-word
    # error 7NGLISCHER. That edit does not relabel any other occurrence of 7.
    changed_numerals = []
    for record in records:
        for raw, candidate in zip(record['positions'], record['readable_candidate']['positions']):
            if raw['raw'].isdigit() and raw['raw'] != candidate['raw']:
                changed_numerals.append({'record': record['id'], 'raw_position': raw,
                                         'candidate_position': candidate})
    assert len(changed_numerals) == 1
    assert changed_numerals[0]['record'] == 'p94_A5'
    assert changed_numerals[0]['raw_position']['raw'] == '7'
    assert changed_numerals[0]['candidate_position']['raw'] == 'E'
    retained = [field(records[0], '30X10X2'),
                field(records[0], '7XINDXDIVX60XGEMXDIV'),
                field(records[0], '54XUSW'),
                field(records[1], '31X10X1918'),
                field(records[1], 'ROEMX1'),
                field(records[1], 'FLIEGERMELUNG'),
                field(records[1], '29X10'),
                field(records[1], 'VONX2'),
                field(records[2], '1KREUZERXUX4XTORPEDOBOOTENX40XKM'),
                field(records[2], 'XARSUSX'),
                field(records[4], '29X10'),
                field(records[4], 'KALATXSHERGAT')]
    qualifications = [field(records[0], 'ANSCHEINEND'),
                      field(records[1], 'BEVORSTEHENDELANDUNG'),
                      field(records[3], 'BEVORSTEHENDENLANDUNGSVERSUCHEN'),
                      field(records[5], 'ANSCHEINEND'),
                      field(records[5], 'ANGEBLICH')]
    inventory = [{'record': r['id'], 'variant': variant, 'raw': reading['raw'],
                  'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                    if p['raw'] in '0123456789JQY']}
                 for r in records
                 for variant, reading in [('source_model', r),
                                          ('ordinary_word_candidate', r['readable_candidate'])]]
    return {'schema': 'adfgvx-orient-intelligence-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 6, 'printed_source_slots': 2020,
                        'valid_source_coordinates': 2019, 'modeled_coordinates': 2020,
                        'plaintext_positions': 1010, 'baseline_fixed_positions': 1009,
                        'candidate_fixed_positions': 1010,
                        'known_coordinate_substitutions': 4,
                        'printed_erasure_fills': 1, 'source_deletions': 0,
                        'missing_coordinate_insertions': 0, 'published_key_changed': False,
                        'p93_separated_direct_plaintext_positions': 487},
            'records': records, 'cross_page_assembly': assembly,
            'direct_unchanged_parts': direct,
            'unchanged_date_unit_count_name_and_odd_word_fields': retained,
            'unchanged_report_qualifications': qualifications,
            'all_changed_numeral_occurrences': changed_numerals,
            'complete_raw_label_inventory': inventory,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The six parts are assembled from explicit headers and part numbers.',
                       'Expected landings, reported sightings and the cavalry claim retain their source qualifications and are not independent proof of historical events.',
                       'FLIEGERMELUNG is preserved without inserting an unseen D; SZ spellings and the received ARSUS name are unchanged.',
                       'The correction to the earlier 30 October note is reproduced; that earlier document is not reconstructed by assumption.',
                       'The one repaired raw 7 belongs to 7NGLISCHER; all date, convoy, distance and military-unit labels remain untouched.',
                       'No recipient abbreviation or personal/unit identity is expanded beyond the received text.']}


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
