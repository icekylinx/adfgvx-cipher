#!/usr/bin/env python3
"""Verify the two native p102 C/D frames, zero-cost readings and prior OCR scope.

Prepared by icekylinx and GPT-6 Astra Pro. Standard library by default;
optional --pdf checks exact rendered pixels with PyMuPDF.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CO = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(source, key):
    ranks, square = key['column_rank_order'], key['square']
    order = sorted(range(len(source)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))
    mid, origins = [''] * len(source), [None] * len(source)
    for j, i in enumerate(order):
        mid[i], origins[i] = source[j], j
    assert len(mid) % 2 == 0
    positions = []
    for i in range(0, len(mid), 2):
        pair = ''.join(mid[i:i + 2])
        domain = ''.join(square[6 * a + b] for a in range(6) for b in range(6)
                         if (pair[0] not in CO or CO[a] == pair[0])
                         and (pair[1] not in CO or CO[b] == pair[1]))
        positions.append({'plaintext_index': i // 2, 'pair': pair, 'source_indices': origins[i:i + 2],
                          'domain': domain, 'label': domain if len(domain) == 1 else '?'})
    return ''.join(x['label'] for x in positions), positions


def encrypt(text, key):
    ranks, square = key['column_rank_order'], key['square']
    mid = ''.join(CO[square.index(x) // 6] + CO[square.index(x) % 6] for x in text)
    return ''.join(mid[i::len(ranks)] for i in sorted(range(len(ranks)), key=ranks.__getitem__))


def source_locations(rows):
    locations = []
    for row, line in enumerate(rows, 1):
        for group, text in enumerate(line.split(), 1):
            for char in range(1, len(text) + 1):
                locations.append({'row_1based': row, 'group_in_row_1based': group,
                                  'character_in_group_1based': char})
    return locations


def readable_normalized(text):
    for a, b in [('ä', 'AE'), ('ö', 'OE'), ('ü', 'UE'), ('Ä', 'AE'), ('Ö', 'OE'), ('Ü', 'UE')]:
        text = text.replace(a, b)
    return ''.join(re.findall('[A-Z0-9?]', text.upper()))


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    prior = json.loads((HERE / 'prior_evidence.json').read_text())
    assert sha(HERE / 'prior_evidence.json') == inp['prior_evidence_sha256']
    key = inp['key']
    assert key['id'] == 'Nov1-3' and key['coordinate_order'] == CO
    assert len(key['square']) == 36 and set(key['square']) == set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    assert sorted(key['column_rank_order']) == list(range(1, 20))
    doc = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        doc = fitz.open(pdf)
    for im in inp['source']['images']:
        assert sha(HERE / im['path']) == im['sha256']
        if doc is not None:
            fitz.TOOLS.store_shrink(100)
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(im['scale'], im['scale']), clip=fitz.Rect(im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    records = []
    for r in inp['records']:
        source = ''.join(''.join(r['rows']).split())
        assert source == r['literal_source'] and set(source) <= set(CO)
        assert len(source) == r['advertised_length'] and len(source) % 2 == 0
        raw, positions = decode(source, key)
        assert raw == r['expected_raw'] == r['editorial_text']
        assert encrypt(raw, key) == source
        assert not r['expected_changes'] and not r['excluded_source_indices'] and not r['inserted_coordinates']
        for field in r['preserved_literal_fields']:
            assert field in raw
        quoted = r['readable_german']
        normalized = readable_normalized(quoted)
        non_x = [(i, c) for i, c in enumerate(raw) if c != 'X']
        assert normalized == ''.join(c for _, c in non_x)
        case = ROOT / r['readable_case_path']
        assert ('> ' + quoted) in case.read_text()
        mapping = [{'readable_normalized_index': i, 'raw_plaintext_index': j, 'label': c}
                   for i, (j, c) in enumerate(non_x)]
        old = next(x for x in prior['selected_rows'] if x['block_id'] == r['prior_block_id'])
        old_raw, old_positions = decode(old['ciphertext'], key)
        assert old_raw == old['best']['plaintext']
        assert len(old['ciphertext']) == len(source)
        loc = source_locations(r['rows'])
        coord_differences = [{'source_index': i, **loc[i], 'earlier_ocr_label': a, 'source_label': b,
                              'earlier_label_was_coordinate': a in CO}
                             for i, (a, b) in enumerate(zip(old['ciphertext'], source)) if a != b]
        label_differences = [{'plaintext_index': i, 'earlier_ocr_label': a, 'native_source_label': b,
                             'source_indices': positions[i]['source_indices']}
                            for i, (a, b) in enumerate(zip(old_raw, raw)) if a != b]
        assert all(not x['earlier_label_was_coordinate'] for x in coord_differences)
        assert all(x['earlier_ocr_label'] == '?' for x in label_differences)
        digits = [{'plaintext_index': i, 'literal_label': c, 'source_indices': positions[i]['source_indices']}
                  for i, c in enumerate(raw) if c.isdigit()]
        records.append({'id': r['id'], 'literal_source_slots': len(source), 'valid_source_coordinates': len(source),
                        'working_frame_slots': len(source), 'plaintext_positions': len(raw),
                        'raw_fixed_positions': len(raw), 'edited_fixed_positions': len(raw),
                        'raw_plaintext': raw, 'editorial_plaintext': raw, 'positions': positions,
                        'reencoded_source': encrypt(raw, key), 'known_coordinate_substitutions': [],
                        'source_erasure_fills': [], 'excluded_observed_coordinates': [],
                        'inserted_coordinates': [], 'literal_digit_positions': digits,
                        'preserved_literal_fields': r['preserved_literal_fields'],
                        'readable_german': quoted, 'readable_non_x_mapping': mapping,
                        'prior_ocr_comparison': {'block_id': old['block_id'], 'earlier_plaintext': old_raw,
                                                 'coordinate_differences': coord_differences,
                                                 'plaintext_differences': label_differences}})
    assert [r['literal_source_slots'] for r in records] == [262, 258]
    assert [len(r['prior_ocr_comparison']['plaintext_differences']) for r in records] == [3, 0]
    summary = {'physical_records': len(records), 'literal_source_slots': sum(r['literal_source_slots'] for r in records),
               'valid_source_coordinates': sum(r['valid_source_coordinates'] for r in records),
               'working_frame_slots': sum(r['working_frame_slots'] for r in records),
               'plaintext_positions': sum(r['plaintext_positions'] for r in records),
               'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in records),
               'edited_fixed_positions': sum(r['edited_fixed_positions'] for r in records),
               'known_coordinate_substitutions': 0, 'source_erasure_fills': 0,
               'excluded_observed_coordinates': 0, 'added_coordinates': 0, 'published_key_changes': 0,
               'earlier_ocr_unknown_labels_resolved_by_source_transcription': 3,
               'readable_non_x_labels': sum(len(r['readable_non_x_mapping']) for r in records)}
    return {'schema': 'adfgvx-nov1-ammunition-and-leave-certificates-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'records': records,
            'summary': summary, 'limits': inp['limits']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    args = p.parse_args()
    result = build(args.pdf)
    if args.verify:
        assert result == json.loads((HERE / 'certificates.json').read_text())
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': bool(args.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
