#!/usr/bin/env python3
"""Verify the three native p97 radio-service source records.

Prepared by icekylinx and GPT-6 Astra Pro. Standard library; optional PDF
verification requires PyMuPDF. Published Nov1-3 key retains prior credit.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = 'ADFGVX'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inverse(source, ranks):
    indices = sorted(range(len(source)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))
    middle, origins = [''] * len(source), [None] * len(source)
    for j, i in enumerate(indices):
        middle[i], origins[i] = source[j], j
    return ''.join(middle), origins


def encrypt(text, key):
    square, ranks = key['square'], key['column_rank_order']
    middle = ''.join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)
    return ''.join(middle[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def decode(source, key):
    middle, origins = inverse(source, key['column_rank_order'])
    assert len(middle) % 2 == 0
    labels = [key['square'][6 * CO.index(middle[i]) + CO.index(middle[i + 1])] for i in range(0, len(middle), 2)]
    return ''.join(labels), [{'plaintext_index': i // 2, 'pair': middle[i:i + 2],
                             'source_indices': origins[i:i + 2], 'label': labels[i // 2]}
                            for i in range(0, len(middle), 2)]


def locations(rows):
    result, group_number = [], 0
    for row_number, row in enumerate(rows, 1):
        for in_row, group in enumerate(row.split(), 1):
            group_number += 1
            result.extend({'row_1based': row_number, 'group_in_row_1based': in_row,
                           'group_1based': group_number, 'position_in_group_1based': j + 1}
                          for j in range(len(group)))
    return result


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    key = inp['key']
    assert len(key['square']) == 36 and set(key['square']) == set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    assert sorted(key['column_rank_order']) == list(range(1, len(key['column_rank_order']) + 1))
    assert sha(HERE / 'prior_evidence.json') == inp['prior_evidence_sha256']
    doc = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        doc = fitz.open(pdf)
    for im in inp['source']['images']:
        assert sha(HERE / im['path']) == im['sha256']
        if doc is not None:
            fitz.TOOLS.store_shrink(100)
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(matrix=fitz.Matrix(im['scale'], im['scale']), clip=fitz.Rect(*im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    records = []
    for r in inp['records']:
        literal = ''.join(''.join(r['rows']).split())
        assert literal == r['literal_source'] and set(literal) <= set(CO)
        assert len(literal) == r['advertised_length']
        raw, pairs = decode(literal, key)
        assert raw == r['expected_raw'] and encrypt(raw, key) == literal
        target = encrypt(r['editorial_text'], key)
        loc = locations(r['rows'])
        changes = []
        for j, (a, b) in enumerate(zip(literal, target)):
            if a != b:
                p = next(p for p in pairs if j in p['source_indices'])['plaintext_index']
                changes.append({'source_index': j, **loc[j], 'before': a, 'after': b,
                                'plaintext_index': p, 'raw_label': raw[p], 'proposed_label': r['editorial_text'][p]})
        assert [[c['source_index'], c['before'], c['after']] for c in changes] == r['expected_changes']
        assert decode(target, key)[0] == r['editorial_text']
        assert all(r['editorial_text'][i] == c for i, c in enumerate(raw) if c.isdigit())
        assert all(token in raw and token in r['editorial_text'] for token in r['preserved_literal_fields'])
        records.append({'id': r['id'], 'source_slots': len(literal), 'valid_source_coordinates': len(literal),
                        'raw_plaintext': raw, 'raw_fixed_positions': len(raw), 'positions': pairs,
                        'editorial_plaintext': r['editorial_text'], 'known_coordinate_substitutions': changes,
                        'repaired_ciphertext': target, 'source_mask_fills': 0, 'source_length_changes': 0,
                        'literal_digit_positions': [{'plaintext_index': i, 'label': c} for i, c in enumerate(raw) if c.isdigit()]})
    assert [r['source_slots'] for r in records] == [196, 246, 196]
    assert [len(r['known_coordinate_substitutions']) for r in records] == [0, 0, 6]
    return {'schema': 'adfgvx-p97-radio-certificate-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'records': records,
            'summary': {'physical_records': 3, 'source_slots': 638, 'valid_source_coordinates': 638,
                        'plaintext_positions': 319, 'raw_fixed_positions': 319,
                        'known_coordinate_substitutions': 6, 'source_mask_fills': 0,
                        'source_length_changes': 0, 'published_key_changes': 0},
            'limits': inp['limits']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    a = p.parse_args()
    result = build(a.pdf)
    if a.verify:
        assert result == json.loads((HERE / 'certificates.json').read_text())
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': a.verify, 'source_pixels_checked': bool(a.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
