#!/usr/bin/env python3
"""Verify the lei-note exchange instructions, source geometry, repairs and every raw label.

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


def source_model(literal, gap=None):
    cipher = ''.join(ch if ch in C else '?' for ch in literal)
    mapping = list(range(len(literal)))
    if gap is not None:
        cipher = cipher[:gap] + '?' + cipher[gap:]
        mapping.insert(gap, None)
    return cipher, mapping


def numeric_inventory(record_id, variant, reading):
    return {'record': record_id, 'variant': variant, 'raw': reading['raw'],
            'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                              if p['raw'] in '0123456789JQY']}


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
        assert len(literal) == source['source_slots']
        assert sum(ch in C for ch in literal) == source['valid_source_coordinates']
        gap = source['model'].get('source_gap')
        cipher, mapping = source_model(literal, gap)
        assert len(cipher) == source['advertised_length']
        raw = inspect(cipher, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], cipher, key, mapping, literal)
        record = {'id': source['id'], 'literal_source': literal, 'ciphertext': cipher,
                  'source_slots': len(literal), 'valid_coordinates': sum(ch in C for ch in literal),
                  'model_to_source_indices': mapping, **raw, 'readable_candidate': candidate}
        if gap is not None:
            stencil = masked_encryption(source['readable_candidate'], key)
            all_gaps = []
            for g in range(len(literal)+1):
                alternative_cipher, _ = source_model(literal, g)
                cost = sum(a != '?' and a != b for a, b in zip(alternative_cipher, stencil))
                all_gaps.append({'source_gap': g, 'known_coordinate_substitutions': cost})
            minimum = min(g['known_coordinate_substitutions'] for g in all_gaps)
            winners = [g['source_gap'] for g in all_gaps if g['known_coordinate_substitutions'] == minimum]
            assert minimum == 14 and winners == [176]
            record['geometry_screen'] = {
                'method': 'Exhaust every single-loss insertion boundary against the complete ordinary-word candidate; no outside rate or numerical assignment is used.',
                'candidate_boundaries': len(all_gaps), 'ordinary_word_stencil': source['readable_candidate'],
                'all_gap_costs': all_gaps, 'minimum_known_coordinate_substitutions': minimum,
                'all_minimizing_gaps': winners, 'selected_source_gap': gap,
                'short_group_source_start': 175, 'short_group_source_end_exclusive': 179,
                'limits': 'A unique minimum is conditional on the declared language stencil, not proof that every received glyph was correctly copied.'}
            alternatives = []
            for g in source['model']['all_source_local_gap_alternatives']:
                alternate_cipher, alternate_mapping = source_model(literal, g)
                alt_raw = inspect(alternate_cipher, key, alternate_mapping)
                alt_candidate = repair(source['readable_candidate'], alternate_cipher, key,
                                       alternate_mapping, literal)
                alternatives.append({'source_gap': g, 'ciphertext': alternate_cipher,
                                     'model_to_source_indices': alternate_mapping,
                                     **alt_raw, 'readable_candidate': alt_candidate})
                inventory.extend([numeric_inventory(source['id'], f'source_gap_{g}', alt_raw),
                                  numeric_inventory(source['id'], f'candidate_gap_{g}', alt_candidate)])
            assert len({a['readable_candidate']['ciphertext'] for a in alternatives}) == 1
            record['all_source_local_gap_alternatives'] = alternatives
        else:
            inventory.extend([numeric_inventory(source['id'], 'source_model', raw),
                              numeric_inventory(source['id'], 'ordinary_word_candidate', candidate)])
        records.append(record)
    assert [r['source_slots'] for r in records] == [341, 248, 410]
    assert [r['valid_coordinates'] for r in records] == [340, 248, 406]
    assert [len(r['raw']) for r in records] == [171, 124, 205]
    assert [r['fixed_positions'] for r in records] == [169, 124, 201]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [14, 2, 5]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records] == [2, 0, 4]
    assert [(i, ch) for i, ch in enumerate(records[0]['literal_source']) if ch not in C] == [(115, 'E')]
    assert [(i, ch) for i, ch in enumerate(records[2]['literal_source']) if ch not in C] == [(114, '-'), (117, '-'), (123, '-'), (307, 'C')]
    monetary_fields = []
    for rec, label in [(records[1], 'J1YKRONENFUERJYYLEI'),
                       (records[2], '70BZW38'),
                       (records[2], '16Y8XJJXJ2B6'),
                       (records[2], 'J447XJJXJ2')]:
        start = rec['raw'].index(label)
        positions = rec['positions'][start:start+len(label)]
        assert all(p['raw'] != '?' and all(i is not None for i in p['source_indices']) for p in positions)
        assert rec['readable_candidate']['raw'][start:start+len(label)] == label
        for p in positions:
            assert rec['readable_candidate']['positions'][p['plaintext_index']] == p
            assert all(rec['ciphertext'][i] == rec['readable_candidate']['ciphertext'][i] for i in p['model_indices'])
        monetary_fields.append({'record': rec['id'], 'raw_label_field': label,
                                'plaintext_start': start, 'plaintext_end_exclusive': start+len(label),
                                'all_observed_pairs_unchanged': True, 'positions': positions})
    selected_inventory = {label: sum(p['raw'] in '0123456789JQY' for r in records
                                    for p in (r if label == 'source_model' else r['readable_candidate'])['positions'])
                          for label in ['source_model', 'ordinary_word_candidate']}
    return {'schema': 'adfgvx-lei-note-exchange-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'), 'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 3, 'printed_source_slots': 999,
                        'valid_source_coordinates': 994, 'modeled_coordinates': 1000,
                        'plaintext_positions': 500, 'baseline_fixed_positions': 494,
                        'candidate_fixed_positions': 500, 'known_coordinate_substitutions': 21,
                        'printed_erasure_fills': 5, 'missing_coordinate_fills': 1,
                        'source_deletions': 0, 'published_key_changed': False},
            'records': records, 'unchanged_monetary_and_reference_fields': monetary_fields,
            'complete_raw_label_inventory': inventory, 'selected_model_label_counts': selected_inventory,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['Fixed positions and monetary fields are raw published-square labels, not established historical numerical values.',
                       'No key assignment follows from plausible exchange rates or numerical patterns.',
                       'The candidate retains the received HEERESAZG abbreviation and apparent VORGENOMME omission.',
                       'All five source-local A1 alignments are retained, including raw 8 in the less well-fitting gaps.',
                       'The telegram describes proposed arrangements and ongoing negotiations, not proof that redemption was completed.']}


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
