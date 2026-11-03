#!/usr/bin/env python3
"""Verify the Turkish-mission recall, conservative readings and earlier closing witness.

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


def unchanged_field(record, text):
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
    assert [r['id'] for r in inputs['records']] == assembly['record_order']
    assert [r['message_part'] for r in inputs['records']] == [1, 2, 3, 4]
    assert all(r['message_total_parts'] == 4 for r in inputs['records'])
    assert all(r['common_receipt_header'] == assembly['shared_receipt'] for r in inputs['records'])
    assert all(r['common_origin_header'] == assembly['shared_origin'] for r in inputs['records'])
    records = []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        assert len(literal) == source['source_slots'] == source['advertised_length']
        assert set(literal) <= set(C)
        mapping = list(range(len(literal)))
        raw = inspect(literal, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], literal, key, mapping, literal)
        records.append({'id': source['id'], 'message_part': source['message_part'],
                        'literal_source': literal, 'source_slots': len(literal),
                        'valid_source_coordinates': len(literal), 'ciphertext': literal,
                        'model_to_source_indices': mapping,
                        **raw, 'readable_candidate': candidate})
    assert [r['source_slots'] for r in records] == [394, 330, 396, 170]
    assert [len(r['raw']) for r in records] == [197, 165, 198, 85]
    assert [r['fixed_positions'] for r in records] == [197, 165, 198, 85]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [0, 2, 0, 1]
    assert all(not r['readable_candidate']['erased_coordinate_fills'] for r in records)

    # Independently re-read a previously reviewed record. Its presence here
    # supplies a closing witness; it contributes zero new catalog records.
    witness = inputs['already_reviewed_closing_witness']
    assert witness['already_catalogued'] and not witness['counted_as_new_record']
    assert sha(ROOT/witness['source_inputs_path']) == witness['source_inputs_sha256']
    earlier = json.loads((ROOT/witness['source_inputs_path']).read_text())
    source = next(r for r in earlier['records'] if r['id'] == witness['record'])
    assert source == witness['source_record_snapshot']
    literal = ''.join(source['raw_grouped'].split())
    assert literal == witness['literal_source']
    old = inspect(literal, key, list(range(len(literal))))
    assert old['raw'] == witness['expected_raw']
    assert sha(ROOT/witness['source_crop_path']) == witness['source_crop_sha256']
    if pdf:
        crop = {'path': witness['source_crop_path'],
                'pdf_page_1based': source['pdf_page_1based'],
                'crop_pdf_points': source['crop_pdf_points'],
                'render_scale': source['render_scale']}
        verify_crops(pdf, inputs['source'], [crop], ROOT)
    closing = witness['shared_closing']
    assert len(closing) == 58
    old_start = old['raw'].index(closing)
    new_start = records[3]['readable_candidate']['raw'].index(closing)
    assert old_start == 60 and new_start == 27
    old_positions = old['positions'][old_start:]
    new_positions = records[3]['readable_candidate']['positions'][new_start:]
    assert len(old_positions) == len(new_positions) == 58
    assert [p['pair'] for p in old_positions] == [p['pair'] for p in new_positions]
    shared_closing = {'already_reviewed_record': witness['record'],
                      'new_record': records[3]['id'], 'text': closing,
                      'old_raw_start': old_start, 'new_candidate_start': new_start,
                      'old_raw_positions': old_positions, 'new_candidate_positions': new_positions,
                      'old_witness_requires_no_repairs': True,
                      'whole_messages_assumed_identical': False,
                      'new_record_substitutions': records[3]['readable_candidate']['known_coordinate_substitutions']}
    retained = [unchanged_field(records[0], 'ZURM2NR46873'),
                unchanged_field(records[0], 'MILITAERMISZION'),
                unchanged_field(records[0], 'EINSCHLISZLICH'),
                unchanged_field(records[1], '10'),
                unchanged_field(records[1], 'LIMANVONSANDERS'),
                unchanged_field(records[1], 'ABESCHLOSZENEN'),
                unchanged_field(records[1], 'ZURUCKBERUFEN'),
                unchanged_field(records[2], 'ZUGEGEBENENEN'),
                unchanged_field(records[2], 'MILIGRHYU'),
                unchanged_field(records[3], 'FRHRMARSCHALL')]
    unresolved = unchanged_field(records[2], 'MILIGRHYU')
    unresolved.update({'square_labels_all_fixed': True, 'editorial_expansion': None,
                       'semantic_status': 'Unresolved received office field; no forced MILIKABT reconstruction.'})
    inventory = [{'record': r['id'], 'variant': variant, 'raw': reading['raw'],
                  'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                    if p['raw'] in '0123456789JQY']}
                 for r in records
                 for variant, reading in [('source_model', r),
                                          ('ordinary_word_candidate', r['readable_candidate'])]]
    assert all([p for p in r['positions'] if p['raw'].isdigit()] ==
               [p for p in r['readable_candidate']['positions'] if p['raw'].isdigit()]
               for r in records)
    return {'schema': 'adfgvx-turkish-mission-recall-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 4, 'printed_source_slots': 1290,
                        'valid_source_coordinates': 1290, 'modeled_coordinates': 1290,
                        'plaintext_positions': 645, 'baseline_fixed_positions': 645,
                        'candidate_fixed_positions': 645,
                        'known_coordinate_substitutions': 3,
                        'printed_erasure_fills': 0, 'source_deletions': 0,
                        'missing_coordinate_insertions': 0, 'published_key_changed': False,
                        'unresolved_received_office_field_positions': 9,
                        'earlier_contextual_records_counted_as_new': 0},
            'records': records, 'cross_page_assembly': assembly,
            'independent_earlier_closing_witness': shared_closing,
            'unchanged_reference_name_and_odd_word_fields': retained,
            'unresolved_received_office_field': unresolved,
            'complete_raw_label_inventory': inventory,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['Fixed plaintext labels are not equivalent to fully resolved wording; MILIGRHYU remains unresolved.',
                       'The apparent omissions and duplicated wording are retained rather than adding unseen source letters.',
                       'The message cites article 10 of a contract; the contract itself is not independently authenticated here.',
                       'Marschall is the received signature and has an earlier same-closing witness; no independent personal identification is made.',
                       'The order requests recall and return reporting; it is not proof that every affected person returned.']}


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
