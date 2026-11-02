#!/usr/bin/env python3
"""Verify four literal service messages and the tied one-coordinate repair.

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


def geometry_screen(record, key, literal):
    assert len(literal) == 267 and set(literal) <= set(C)
    stencil = record['geometry_stencil']
    target = masked_encryption(stencil, key)
    assert len(target) == record['advertised_length'] == 268
    trials = []
    for gap in range(len(literal) + 1):
        cipher = literal[:gap] + '?' + literal[gap:]
        mapping = list(range(gap)) + [None] + list(range(gap, len(literal)))
        mismatches = [i for i, (a, b) in enumerate(zip(cipher, target))
                      if a != '?' and b != '?' and a != b]
        trials.append({'source_gap': gap, 'known_coordinate_substitutions': len(mismatches),
                       'mismatch_model_indices': mismatches})
    minimum = min(t['known_coordinate_substitutions'] for t in trials)
    best = [t for t in trials if t['known_coordinate_substitutions'] == minimum]
    assert minimum == 0 and [t['source_gap'] for t in best] == [109, 110]
    tied = []
    for trial in best:
        gap = trial['source_gap']
        cipher = literal[:gap] + '?' + literal[gap:]
        mapping = list(range(gap)) + [None] + list(range(gap, len(literal)))
        candidate = repair(stencil, cipher, key, mapping, literal)
        assert len(candidate['erased_coordinate_fills']) == 1
        assert candidate['erased_coordinate_fills'][0]['to'] == 'F'
        tied.append({**trial, 'unfilled_model': inspect(cipher, key, mapping),
                     'repaired': candidate})
    assert tied[0]['repaired']['ciphertext'] == tied[1]['repaired']['ciphertext']
    return {'declared_model': 'One missing coordinate at any source boundary.',
            'stencil': stencil, 'models_examined': len(trials),
            'all_tied_minima': tied, 'all_trials': trials,
            'same_repaired_ciphertext_for_both_minima': True,
            'limit': 'Exact only for the declared ordinary-word stencil and single-loss model. The numerical reference remains masked.'}


def conditional_name_layer_impact(records, key):
    """Keep all effects of the separate, conditional Tydelski name assignment."""
    square = key['square']
    assert square[17] == '?' and 'Y' not in square
    updated = {**key, 'square': square[:17] + 'Y' + square[18:]}
    variants = []
    for record in records:
        mapping = record['model_to_source_indices']
        inventory = [('source_model', record['model_ciphertext'], mapping)]
        inventory.extend(('candidate:' + c['id'], c['ciphertext'], mapping)
                         for c in record['editorial_candidates'])
        if record['id'] == 'p192_B':
            literal = record['literal_source']
            gap = 110
            inventory.append(('alternative_tied_source_gap:110',
                              literal[:gap] + '?' + literal[gap:],
                              list(range(gap)) + [None] + list(range(gap, len(literal)))))
        for name, cipher, model_mapping in inventory:
            before = inspect(cipher, key, model_mapping)
            after = inspect(cipher, updated, model_mapping)
            changes = [{'plaintext_index': i, 'pair': a['pair'],
                        'source_indices': a['source_indices'],
                        'before': a['domain'], 'after': b['domain']}
                       for i, (a, b) in enumerate(zip(before['positions'], after['positions']))
                       if a['domain'] != b['domain']]
            raw_changes = [{'plaintext_index': i, 'before': a, 'after': b}
                           for i, (a, b) in enumerate(zip(before['raw'], after['raw'])) if a != b]
            assert not raw_changes
            variants.append({'record': record['id'], 'variant': name,
                             'raw_before': before['raw'], 'raw_after': after['raw'],
                             'newly_fixed_raw_positions': raw_changes,
                             'all_changed_marginal_domains': changes})
    assert len(variants) == 10
    return {'assignment': {'key_id': 'Nov13-15b', 'coordinate_pair': 'FX',
                           'square_cell_index': 17, 'symbol': 'Y'},
            'assumption': 'The separate p192 part 3 courier identification as Tadeusz Tydelski is correct. No historical identity claim is added by this service-message package.',
            'inventory_scope': 'All four physical records: four conservative source models, all five editorial candidate variants, and the other tied p192 B gap model.',
            'physical_records': 4, 'variants_checked': 10,
            'newly_fixed_raw_position_count': 0,
            'all_variant_results': variants,
            'Nov13-15a_DG_transfer': 'Not applicable: none of these four records uses the Nov13-15a square.',
            'published_key_changed': False}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    catalogue = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    key = inputs['key']
    assert key == catalogue[key['id']]
    for source in inputs['source_images']:
        assert sha(HERE/source['path']) == source['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        assert sha(pdf) == inputs['source']['pdf_sha256']
        doc = fitz.open(pdf)
        for source in inputs['source_images']:
            page = doc[source['pdf_page_1based'] - 1]
            scale = source['render_scale']
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale),
                                     clip=fitz.Rect(*source['crop_pdf_points']))
            image = Image.open(HERE/source['path']).convert('RGB')
            assert image.size == (pixmap.width, pixmap.height)
            assert image.tobytes() == pixmap.samples
    records = []
    for record in inputs['records']:
        literal = ''.join(''.join(record['source_rows']).split())
        assert len(literal) == record['source_slots']
        cipher = ''.join(c if c in C else '?' for c in literal)
        mapping = list(range(len(literal)))
        if record['model']['kind'] == 'insert_unknown_coordinate':
            gap = record['model']['source_gap']
            cipher = cipher[:gap] + '?' + cipher[gap:]
            mapping.insert(gap, None)
        else:
            assert record['model']['kind'] == 'identity'
        assert len(cipher) == record['advertised_length']
        observed = inspect(cipher, key, mapping)
        assert observed['raw'] == record['expected_model_raw']
        result = {'id': record['id'], 'key_id': key['id'], 'literal_source': literal,
                  'source_slots': len(literal), 'valid_coordinates': sum(c in C for c in literal),
                  'literal_unpaired_coordinate_count': len(literal) % 2,
                  'model': record['model'], 'model_ciphertext': cipher,
                  'model_to_source_indices': mapping, **observed}
        result['editorial_candidates'] = [{'id': c['id'], 'reason': c['reason'],
                                            **repair(c['plaintext'], cipher, key, mapping, literal)}
                                           for c in record['editorial_candidates']]
        if record['id'] == 'p192_B':
            result['geometry_screen'] = geometry_screen(record, key, literal)
        records.append(result)
    assert [r['source_slots'] for r in records] == [350, 267, 224, 240]
    assert [r['fixed_positions'] for r in records] == [171, 131, 111, 119]
    first = [r['editorial_candidates'][0] for r in records]
    assert [len(r['known_coordinate_substitutions']) for r in first] == [0, 0, 2, 0]
    assert [len(r['erased_coordinate_fills']) for r in first] == [1, 1, 0, 1]
    assert first[3]['raw'][16:30] == 'UNKONTOLLIERTE'
    return {'schema': 'adfgvx-warsaw-service-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based; group numbers are explicitly one-based.',
            'summary': {'records': len(records),
                        'printed_source_slots': sum(r['source_slots'] for r in records),
                        'valid_source_coordinates': sum(r['valid_coordinates'] for r in records),
                        'modeled_coordinates': sum(len(r['model_ciphertext']) for r in records),
                        'plaintext_positions': sum(len(r['raw']) for r in records),
                        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
                        'conservative_candidate_fixed_positions': sum(r['fixed_positions'] for r in first)},
            'records': records,
            'conditional_name_layer_impact': conditional_name_layer_impact(records, key),
            'limits': ['No source date is silently corrected.',
                       'The p192 B gap has two tied placements; both produce the same ciphertext.',
                       'The p194 C separator interpretation is an optional editorial proposal.',
                       'The p194 E omitted R and triple separator remain literal.',
                       'Unknown key cells, digits and 0/5 labels remain unchanged.']}


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
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
