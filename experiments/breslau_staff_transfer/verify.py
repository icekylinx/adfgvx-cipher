#!/usr/bin/env python3
"""Verify the Breslau staff transfer, source-level repairs and unchanged raw-label inventory.

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


def build(pdf=None, historical_pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    current = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    assert key == current[key['id']]
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path']) == crop['sha256']
    if pdf:
        verify_crops(pdf, inputs['source'], inputs['source_images'], HERE)
    ctxpath = HERE/inputs['historical_context']['path']
    assert sha(ctxpath) == inputs['historical_context']['sha256']
    context = json.loads(ctxpath.read_text())
    location = context['unit_location_witness']
    assert location['issue_date'] == '1917-07-18'
    for crop in location['crops']:
        assert sha(ROOT/crop['path']) == crop['sha256']
    if historical_pdf:
        verify_crops(historical_pdf, location, location['crops'], ROOT)
    records, inventory = [], []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        assert set(literal) <= set(C)
        assert len(literal) == source['source_slots'] == source['advertised_length']
        mapping = list(range(len(literal)))
        raw = inspect(literal, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], literal, key, mapping, literal)
        records.append({'id': source['id'], 'literal_source': literal,
                        'ciphertext': literal, 'source_slots': len(literal),
                        'valid_coordinates': len(literal), 'model_to_source_indices': mapping,
                        **raw, 'readable_candidate': candidate})
        for label, reading in [('source_model', raw), ('ordinary_word_candidate', candidate)]:
            positions = [p for p in reading['positions'] if p['raw'] in '0123456789JQY']
            inventory.append({'record': source['id'], 'variant': label,
                              'raw': reading['raw'], 'all_numeral_and_JQY_occurrences': positions})
    assert [len(r['raw']) for r in records] == [130, 149]
    assert [r['fixed_positions'] for r in records] == [130, 149]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [3, 6]
    assert all(not r['readable_candidate']['erased_coordinate_fills'] for r in records)
    rank = records[0]['positions'][9]
    name = records[0]['positions'][90]
    corps = records[1]['positions'][14]
    assert (rank['pair'], rank['raw'], rank['source_indices']) == ('VD', '9', [125, 79])
    assert (name['pair'], name['raw'], name['source_indices']) == ('AD', 'Q', [86, 210])
    assert (corps['pair'], corps['raw'], corps['source_indices']) == ('GA', '7', [247, 1])
    for rec, point in [(records[0], rank), (records[0], name), (records[1], corps)]:
        assert all(rec['ciphertext'][i] == rec['readable_candidate']['ciphertext'][i] for i in point['source_indices'])
    return {'schema': 'adfgvx-breslau-staff-transfer-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'), 'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 2, 'printed_source_slots': 558,
                        'valid_source_coordinates': 558, 'plaintext_positions': 279,
                        'baseline_fixed_positions': 279, 'candidate_fixed_positions': 279,
                        'known_coordinate_substitutions': 9, 'source_or_model_erasure_fills': 0},
            'records': records, 'complete_raw_label_inventory': inventory,
            'untouched_interpretive_fields': {'rank_MA9OR_label': rank,
                                             'surname_STRZEMIECZNQ_final_label': name,
                                             'corps_7_AK_BRESLAU_label': corps},
            'historical_context': inputs['historical_context'],
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['All 279 raw positions are fixed labels under the published square, not 279 newly solved key symbols.',
                       'No numerical or surname label is reassigned; MA9OR, STRZEMIECZNQ, AOKJJ, 7AK, 40RESK, 40AK and 04013 remain explicit.',
                       'The 1917 Breslau decree supports a unit-location hypothesis, not an identified 1918 officer or unconditional key assignment.',
                       'The 1913 surname evidence is OCR-only and has not identified the officer in this message.',
                       'The following VON LP AN CO cleartext fragment is outside the 298-coordinate second part.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--historical-pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf, args.historical_pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
