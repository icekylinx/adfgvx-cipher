#!/usr/bin/env python3
"""Verify the Constantinople civilian enquiry and every retained source-frame alternative.

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


def model(source, position=None):
    literal = ''.join(''.join(source['source_rows']).split())
    cipher = ''.join(c if c in C else '?' for c in literal)
    mapping = list(range(len(cipher)))
    kind = source['model']['kind']
    if kind == 'single_missing_coordinate':
        gap = source['model']['source_boundary'] if position is None else position
        cipher = cipher[:gap] + '?' + cipher[gap:]
        mapping = mapping[:gap] + [None] + mapping[gap:]
    elif kind == 'single_surplus_coordinate':
        pos = source['model']['source_index'] if position is None else position
        cipher = cipher[:pos] + cipher[pos+1:]
        mapping = mapping[:pos] + mapping[pos+1:]
    return literal, cipher, mapping


def view(source, key, position=None):
    literal, cipher, mapping = model(source, position)
    return {'source_position': position, 'ciphertext': cipher,
            'model_to_source_indices': mapping, **inspect(cipher, key, mapping),
            'readable_candidate': repair(source['readable_candidate'], cipher, key, mapping, literal)}


def geometry_screen(source, key):
    literal = ''.join(''.join(source['source_rows']).split())
    kind = source['model']['kind']
    indices = range(len(literal)+1) if kind == 'single_missing_coordinate' else range(len(literal))
    masked = masked_encryption(source['geometry_stencil'], key)
    full = masked_encryption(source['readable_candidate'], key)
    trials = []
    for pos in indices:
        _, cipher, _ = model(source, pos)
        assert len(cipher) == len(masked) == len(full)
        trials.append({'source_position': pos,
                       'masked_body_substitution_cost': sum(a != '?' and b != '?' and a != b for a, b in zip(cipher, masked)),
                       'full_candidate_substitution_cost': sum(a != '?' and b != '?' and a != b for a, b in zip(cipher, full))})
    minimum = min(t['masked_body_substitution_cost'] for t in trials)
    ties = [t['source_position'] for t in trials if t['masked_body_substitution_cost'] == minimum]
    expected = {'p221_B1': (1, [227]), 'p221_B2': (4, [134]),
                'p221_B4': (5, [181, 182, 183, 184, 185, 186])}
    assert (minimum, ties) == expected[source['id']]
    full_min = min(t['full_candidate_substitution_cost'] for t in trials)
    full_ties = [t['source_position'] for t in trials if t['full_candidate_substitution_cost'] == full_min]
    local_ranges = {'p221_B1': range(225, 230), 'p221_B2': range(130, 136), 'p221_B4': range(190, 195)}
    local = [t for t in trials if t['source_position'] in local_ranges[source['id']]]
    local_min = min(t['masked_body_substitution_cost'] for t in local)
    local_ties = [t['source_position'] for t in local if t['masked_body_substitution_cost'] == local_min]
    representative = source['model'].get('source_boundary', source['model'].get('source_index'))
    positions = sorted(set(ties+[representative]))
    views = [view(source, key, pos) for pos in positions]
    assert len({v['readable_candidate']['ciphertext'] for v in views}) == 1
    if source['id'] == 'p221_B4':
        assert (local_min, local_ties) == (8, [190])
        assert (full_min, full_ties) == (6, [184, 185, 186])
        assert all(source['geometry_stencil'][i] == '?' for i in range(116, 133))
    if source['id'] == 'p221_B1':
        assert source['geometry_stencil'][71:74] == '???'
        assert source['readable_candidate'][71:74] == '0YY'
    return {'operation': kind, 'geometry_stencil': source['geometry_stencil'],
            'all_costs': trials, 'search_size': len(trials),
            'masked_body_minimum': minimum, 'all_masked_body_minima': ties,
            'full_candidate_minimum': full_min, 'all_full_candidate_minima': full_ties,
            'source_local_trials': local, 'source_local_minimum': local_min,
            'all_source_local_minima': local_ties,
            'primary_source_position': representative,
            'all_global_masked_body_ties_and_primary_view': views,
            'corrected_ciphertext_shared_across_retained_views': True,
            'interpretive_limit': 'A minimum is conditional on its declared word stencil and frame restrictions. In B4 the source-local and broader minima differ; neither is silently discarded.'}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    current = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    assert key == current[key['id']]
    for source in inputs['source_images']:
        assert sha(HERE/source['path']) == source['sha256']
    context_path = HERE/inputs['historical_context']['path']
    assert sha(context_path) == inputs['historical_context']['sha256']
    context = json.loads(context_path.read_text())
    assert context['not_used_for_geometry_selection'] and not context['numerical_values_imported']
    if pdf:
        import fitz
        from PIL import Image
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        assert sha(pdf) == inputs['source']['pdf_sha256']
        doc = fitz.open(pdf)
        for source in inputs['source_images']:
            pix = doc[source['pdf_page_1based']-1].get_pixmap(
                matrix=fitz.Matrix(source['render_scale'], source['render_scale']),
                clip=fitz.Rect(*source['crop_pdf_points']))
            im = Image.open(HERE/source['path']).convert('RGB')
            assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples
    records, screens = [], {}
    for source in inputs['records']:
        literal, cipher, mapping = model(source)
        assert len(literal) == source['source_slots']
        assert len(cipher) == source['advertised_length']
        raw = inspect(cipher, key, mapping)
        assert raw['raw'] == source['expected_raw']
        records.append({'id': source['id'], 'literal_source': literal,
                        'source_slots': len(literal), 'valid_coordinates': sum(c in C for c in literal),
                        'model': source['model'], 'ciphertext': cipher,
                        'model_to_source_indices': mapping, **raw,
                        'readable_candidate': repair(source['readable_candidate'], cipher, key, mapping, literal)})
        if source['model']['kind'] != 'identity':
            screens[source['id']] = geometry_screen(source, key)
    assert [r['fixed_positions'] for r in records] == [148, 171, 173, 132]
    assert [r['readable_candidate']['fixed_positions'] for r in records] == [149, 172, 174, 133]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [1, 4, 3, 9]
    quantity_positions = records[0]['positions'][71:74]
    assert [(p['pair'], p['source_indices']) for p in quantity_positions] == [('AF', [123, 251]), ('DG', [6, 200]), ('DG', [226, 84])]
    assert ''.join(p['raw'] for p in quantity_positions) == '0YY'
    assert all(records[0]['ciphertext'][i] == records[0]['readable_candidate']['ciphertext'][i]
               for p in quantity_positions for i in p['model_indices'])
    return {'schema': 'adfgvx-constantinople-civilians-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'), 'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': 4,
                        'printed_source_slots': sum(r['source_slots'] for r in records),
                        'valid_source_coordinates': sum(r['valid_coordinates'] for r in records),
                        'modeled_coordinates': sum(len(r['ciphertext']) for r in records),
                        'plaintext_positions': sum(len(r['raw']) for r in records),
                        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
                        'readable_candidate_fixed_positions': sum(r['readable_candidate']['fixed_positions'] for r in records)},
            'records': records, 'geometry_screens': screens,
            'headcount_witness': {'record': 'p221_B1', 'raw_field': '0YY',
                                  'positions': quantity_positions,
                                  'headcount_excluded_from_geometry_selection': True,
                                  'requires_no_coordinate_repairs': True,
                                  'numerical_value': 'Unassigned. These are the literal labels of the published square.'},
            'historical_context': inputs['historical_context'],
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The source reports an unconfirmed departure; it does not itself verify that departure happened.',
                       'All published Nov25 labels are retained, including 0YY. No digit or letter relabelling is performed.',
                       'B4 has distinct source-local and broader geometry fits; all tied broader fits are retained.',
                       'Independent FRUS documents corroborate the civilian-residence request and diplomatic routing, not the quantity or any source-frame choice.',
                       'Fixed-position counts include received garbles and raw numerical labels, not a claim of fully settled historical wording.']}


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
