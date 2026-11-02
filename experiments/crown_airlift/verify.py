#!/usr/bin/env python3
"""Verify the interrupted crown-airlift request and every declared coordinate repair.

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
        assert len(literal) == source['source_slots']
        missing = source['model']['missing_tail_coordinates']
        base = ''.join(c if c in C else '?' for c in literal) + '?'*missing
        mapping = list(range(len(literal))) + [None]*missing
        assert len(base) == source['advertised_length']
        raw = inspect(base, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], base, key, mapping, literal)
        records.append({'id': source['id'], 'literal_source': literal,
                        'source_slots': len(literal),
                        'valid_source_coordinates': sum(c in C for c in literal),
                        'ciphertext': base, 'model_to_source_indices': mapping,
                        **raw, 'readable_candidate': candidate})
    assert [len(r['raw']) for r in records] == [73, 73, 49]
    assert [r['fixed_positions'] for r in records] == [73, 72, 30]
    assert [r['readable_candidate']['fixed_positions'] for r in records] == [73, 73, 42]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [0, 1, 0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records] == [0, 1, 12]

    # The explicit interruption motivates the primary trailing gap. Ordinary
    # words alone do not distinguish all nearby geometries: retain every tie.
    third = records[2]
    literal = third['literal_source']
    prefix = inputs['a3_ordinary_word_prefix']
    assert len(prefix) == 33 and len(literal) == 79
    mask = masked_encryption(prefix + '?'*16, key)
    screen = []
    for gap in range(len(literal)+1):
        base = literal[:gap] + '?'*19 + literal[gap:]
        mapping = list(range(gap)) + [None]*19 + list(range(gap, len(literal)))
        mismatches = [i for i, (a, b) in enumerate(zip(base, mask))
                      if a != '?' and b != '?' and a != b]
        screen.append({'gap_before_source_index': gap,
                       'known_coordinate_substitutions_for_prefix': len(mismatches),
                       'mismatching_model_indices': mismatches})
    best = min(row['known_coordinate_substitutions_for_prefix'] for row in screen)
    gaps = [row['gap_before_source_index'] for row in screen
            if row['known_coordinate_substitutions_for_prefix'] == best]
    assert best == 0 and gaps == [77, 78, 79]
    alternatives = []
    for gap in gaps:
        base = literal[:gap] + '?'*19 + literal[gap:]
        mapping = list(range(gap)) + [None]*19 + list(range(gap, len(literal)))
        raw = inspect(base, key, mapping)
        candidate = repair(prefix + raw['raw'][33:], base, key, mapping, literal)
        assert not candidate['known_coordinate_substitutions']
        alternatives.append({'gap_before_source_index': gap,
                             'is_primary_source_interruption_model': gap == 79,
                             'ciphertext': base, 'model_to_source_indices': mapping,
                             **raw, 'readable_candidate': candidate})
    assert alternatives[-1]['raw'] == third['raw']
    suffix = {'record': third['id'], 'plaintext_start': 33,
              'plaintext_end_exclusive': 49,
              'raw': third['raw'][33:],
              'positions': third['positions'][33:],
              'untouched_by_candidate': True}
    assert suffix['positions'] == third['readable_candidate']['positions'][33:]
    inventory = [{'record': r['id'], 'variant': variant,
                  'raw': reading['raw'],
                  'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                    if p['raw'] in '0123456789JQY']}
                 for r in records
                 for variant, reading in [('source_model', r),
                                          ('ordinary_word_candidate', r['readable_candidate'])]]
    return {'schema': 'adfgvx-crown-airlift-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 3, 'printed_source_slots': 371,
                        'valid_source_coordinates': 370, 'modeled_coordinates': 390,
                        'plaintext_positions': 195, 'baseline_fixed_positions': 175,
                        'candidate_fixed_positions': 188,
                        'known_coordinate_substitutions': 1,
                        'printed_erasure_fills': 1, 'missing_tail_fills': 12,
                        'unfilled_missing_tail_coordinates': 7,
                        'source_deletions': 0, 'published_key_changed': False},
            'records': records,
            'a3_frame_screen': {'ordinary_word_prefix': prefix,
                                'masked_plaintext_suffix_length': 16,
                                'screened_one_gap_frames': screen,
                                'minimum_known_coordinate_substitutions': best,
                                'all_tied_minimum_gaps': gaps,
                                'primary_gap': 79,
                                'primary_selection_basis': 'Printed Did not finish annotation and advertised length 98, not suffix plausibility.',
                                'all_tied_readings': alternatives},
            'untouched_primary_suffix': suffix,
            'complete_raw_label_inventory': inventory,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The advertised 98 length and interruption define a declared source model; the original transmission is not available.',
                       'The first 33-letter candidate is compatible with every observed pair in all three tied gap frames, but is a contextual restoration rather than uniquely determined missing text.',
                       'The observed L after SENDEN is not silently changed to a separator.',
                       'The raw 1A4A1 suffix and all unknown positions remain unassigned; no key cell is filled.',
                       'The request establishes desired daily delivery, not completed flights or actual cash receipt.']}


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
