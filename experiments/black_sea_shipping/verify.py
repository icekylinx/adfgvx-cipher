#!/usr/bin/env python3
"""Verify source geometry, coded supply traffic and ship-sale instructions.

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


def model_for(record, index=None):
    literal = ''.join(''.join(record['source_rows']).split())
    cipher = ''.join(c if c in C else '?' for c in literal)
    mapping = list(range(len(literal)))
    model = record['model']
    if model['kind'] == 'delete_coordinate':
        i = model['source_index'] if index is None else index
        cipher = cipher[:i] + cipher[i+1:]
        del mapping[i]
    elif model['kind'] == 'insert_unknown_coordinate':
        i = model['source_gap'] if index is None else index
        cipher = cipher[:i] + '?' + cipher[i:]
        mapping.insert(i, None)
    else:
        assert model['kind'] == 'identity' and index is None
    return literal, cipher, mapping


def geometry(record, key):
    literal, _, _ = model_for(record)
    stencil = record['geometry_stencil']
    assert all(stencil[i] == '?' for i in record['masked_plaintext_indices'])
    target = masked_encryption(stencil, key)
    insert = record['model']['kind'] == 'insert_unknown_coordinate'
    trials = []
    for i in range(len(literal) + insert):
        _, cipher, mapping = model_for(record, i)
        mismatches = [j for j, (a, b) in enumerate(zip(cipher, target))
                      if a != '?' and b != '?' and a != b]
        trials.append({'source_gap' if insert else 'deleted_source_index': i,
                       'known_coordinate_substitutions': len(mismatches),
                       'mismatch_model_indices': mismatches})
    minimum = min(t['known_coordinate_substitutions'] for t in trials)
    best = [t for t in trials if t['known_coordinate_substitutions'] == minimum]
    key_name = 'source_gap' if insert else 'deleted_source_index'
    expected = [164, 165, 166, 167, 168] if insert else [50, 51, 52]
    assert [t[key_name] for t in best] == expected
    assert minimum == (0 if insert else 3)
    alternatives = []
    for trial in best:
        i = trial[key_name]
        _, cipher, mapping = model_for(record, i)
        result = {'model_parameter': i, 'model_ciphertext': cipher,
                  'model_to_source_indices': mapping, **inspect(cipher, key, mapping)}
        if insert:
            prefix = record['ordinary_body_prefix']
            candidate = repair(prefix + result['raw'][len(prefix):], cipher, key, mapping, literal)
            assert not candidate['known_coordinate_substitutions']
            assert candidate['raw'].startswith(prefix)
            result['body_candidate'] = candidate
            result['raw_footer'] = result['raw'][len(prefix):]
        alternatives.append(result)
    result = {'declared_model': 'One missing coordinate at any source boundary.' if insert
                               else 'One surplus observed coordinate removed at any source index.',
              'stencil': stencil, 'masked_plaintext_indices': record['masked_plaintext_indices'],
              'models_examined': len(trials), 'minimum_known_coordinate_changes': minimum,
              'all_tied_minima': best, 'all_trials': trials,
              'all_minimum_model_readings': alternatives}
    if insert:
        result['ordinary_prefix_consensus'] = record['ordinary_body_prefix']
        result['ordinary_prefix_length'] = record['body_prefix_length']
        result['unique_gap_claimed'] = False
        result['limit'] = 'The entire numeric footer is masked. Five different gap models share a zero-substitution ordinary-body fit; the footer is not used to pick one.'
    else:
        local = [t for t in trials if t[key_name] in record['malformed_group_source_indices']]
        local_min = min(t['known_coordinate_substitutions'] for t in local)
        local_best = [t for t in local if t['known_coordinate_substitutions'] == local_min]
        assert [t[key_name] for t in local_best] == [50]
        result['source_locality_constraint'] = {'six_letter_group': 'XAXADV',
                                                'source_indices': record['malformed_group_source_indices'],
                                                'all_tied_minima_with_extra_coordinate_in_this_group': local_best}
        result['limit'] = 'The reported deletion is unique only when the extra coordinate is constrained to the visibly six-letter group. The broader screen has three tied minima, all retained.'
    return result


def conditional_name_impact(records, key):
    square = key['square']
    assert square[17] == '?' and 'Y' not in square
    updated = {**key, 'square': square[:17] + 'Y' + square[18:]}
    variants = []
    for r in records:
        mapping = r['model_to_source_indices']
        inventory = [('source_model', r['model_ciphertext'], mapping)]
        inventory.extend(('candidate:' + c['id'], c['ciphertext'], mapping)
                         for c in r['editorial_candidates'])
        if 'geometry_screen' in r:
            canonical = r['model'].get('source_gap', r['model'].get('source_index'))
            for alternate in r['geometry_screen']['all_minimum_model_readings']:
                if alternate['model_parameter'] == canonical:
                    continue
                label = str(alternate['model_parameter'])
                m = alternate['model_to_source_indices']
                inventory.append(('alternative_geometry:' + label,
                                  alternate['model_ciphertext'], m))
                if 'body_candidate' in alternate:
                    inventory.append(('alternative_body_candidate:' + label,
                                      alternate['body_candidate']['ciphertext'], m))
        for label, cipher, m in inventory:
            before, after = inspect(cipher, key, m), inspect(cipher, updated, m)
            changes = [{'plaintext_index': i, 'pair': a['pair'],
                        'source_indices': a['source_indices'],
                        'before': a['domain'], 'after': b['domain']}
                       for i, (a, b) in enumerate(zip(before['positions'], after['positions']))
                       if a['domain'] != b['domain']]
            raw_changes = [{'plaintext_index': i, 'before': a, 'after': b}
                           for i, (a, b) in enumerate(zip(before['raw'], after['raw'])) if a != b]
            variants.append({'record': r['id'], 'variant': label,
                             'raw_before': before['raw'], 'raw_after': after['raw'],
                             'newly_fixed_raw_positions': raw_changes,
                             'all_changed_marginal_domains': changes})
    assert len(variants) == 21
    fixed = sum(len(r['newly_fixed_raw_positions']) for r in variants)
    assert fixed == 0
    return {'assignment': {'key_id': 'Nov13-15b', 'coordinate_pair': 'FX',
                           'square_cell_index': 17, 'symbol': 'Y'},
            'assumption': 'The separate historical courier-name identification as Tydelski is correct; this package does not independently establish that identification.',
            'physical_records': len(records), 'variants_checked': len(variants),
            'newly_fixed_raw_position_count': fixed,
            'inventory_scope': 'All five declared source models, all six explicit editorial candidates, every other tied source-geometry model, and each alternate p199 A3 body repair. Zero-change results are retained.',
            'all_variant_results': variants,
            'Nov13-15a_DG_transfer': 'Not applicable; all five records use Nov13-15b.',
            'published_key_changed': False}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    keys = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    key = inputs['key']
    assert key == keys[key['id']]
    for source in inputs['source_images']:
        assert sha(HERE/source['path']) == source['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        assert sha(pdf) == inputs['source']['pdf_sha256']
        doc = fitz.open(pdf)
        for source in inputs['source_images']:
            pixmap = doc[source['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(source['render_scale'], source['render_scale']),
                clip=fitz.Rect(*source['crop_pdf_points']))
            image = Image.open(HERE/source['path']).convert('RGB')
            assert image.size == (pixmap.width, pixmap.height) and image.tobytes() == pixmap.samples
    records = []
    for record in inputs['records']:
        literal, cipher, mapping = model_for(record)
        assert len(literal) == record['source_slots'] and len(cipher) == record['advertised_length']
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
        if 'geometry_stencil' in record:
            result['geometry_screen'] = geometry(record, key)
        records.append(result)
    first = [r['editorial_candidates'][0] for r in records]
    assert [r['fixed_positions'] for r in records] == [145, 171, 100, 195, 174]
    assert [len(r['known_coordinate_substitutions']) for r in first] == [3, 2, 0, 3, 0]
    assert [len(r['erased_coordinate_fills']) for r in first] == [0, 0, 2, 1, 2]
    return {'schema': 'adfgvx-black-sea-shipping-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based; group and row numbers are explicitly one-based.',
            'summary': {'records': len(records),
                        'printed_source_slots': sum(r['source_slots'] for r in records),
                        'valid_source_coordinates': sum(r['valid_coordinates'] for r in records),
                        'modeled_coordinates': sum(len(r['model_ciphertext']) for r in records),
                        'plaintext_positions': sum(len(r['raw']) for r in records),
                        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
                        'conservative_candidate_fixed_positions': sum(r['fixed_positions'] for r in first)},
            'records': records, 'source_relationships': inputs['source_relationships'],
            'prior_publication': inputs['prior_publication'],
            'conditional_name_layer_impact': conditional_name_impact(records, key),
            'limits': ['The coded supply report and ship-sale order are separate messages, not presumed copies.',
                       'The surplus-coordinate deletion is localized by the visibly six-letter source group; broader tied minima remain explicit.',
                       'The five p199 A3 body-compatible gap models are retained without using the numeric footer to select one.',
                       'Received omissions and unusual code-like words are not silently normalized.',
                       'No unknown published key cell or digit label is assigned.']}


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
