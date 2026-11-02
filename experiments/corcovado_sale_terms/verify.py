#!/usr/bin/env python3
"""Verify Corcovado traffic and conditional cross-key office-prefix digits.

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


def assign(key, assignments):
    square = list(key['square'])
    for pair, symbol in assignments.items():
        cell = C.index(pair[0])*6 + C.index(pair[1])
        assert square[cell] == '?' and symbol not in square
        square[cell] = symbol
    return {**key, 'square': ''.join(square)}


def layer_impact(records, key, assignments):
    changed = assign(key, assignments)
    variants = []
    for record in records:
        if record['key_id'] != key['id']:
            continue
        mapping = list(range(len(record['ciphertext'])))
        for label, cipher in [('source_model', record['ciphertext']),
                              ('readable_candidate', record['readable_candidate']['ciphertext'])]:
            before, after = inspect(cipher, key, mapping), inspect(cipher, changed, mapping)
            domains = [{'plaintext_index': i, 'pair': a['pair'],
                        'source_indices': a['source_indices'],
                        'before': a['domain'], 'after': b['domain']}
                       for i, (a, b) in enumerate(zip(before['positions'], after['positions']))
                       if a['domain'] != b['domain']]
            raw_changes = [{'plaintext_index': i, 'before': a, 'after': b,
                            'pair': before['positions'][i]['pair'],
                            'source_indices': before['positions'][i]['source_indices'],
                            'assignment_used': assignments[before['positions'][i]['pair']]}
                           for i, (a, b) in enumerate(zip(before['raw'], after['raw'])) if a != b]
            variants.append({'record': record['id'], 'variant': label,
                             'raw_before': before['raw'], 'raw_after': after['raw'],
                             'newly_fixed_raw_positions': raw_changes,
                             'all_changed_marginal_domains': domains,
                             'all_remaining_uncertain_positions': [p for p in after['positions'] if len(p['domain']) > 1]})
    return {'key_id': key['id'], 'assignments': assignments,
            'square_after_conditional_assignments': changed['square'],
            'physical_records_checked': len(variants)//2, 'variants_checked': len(variants),
            'all_variant_results': variants,
            'previously_published_completion': key.get('previously_published_completion'),
            'published_key_changed': False}


def office_layers(inputs, records, keys):
    witness = inputs['office_prefix_witness']
    path = ROOT/witness['path']
    assert sha(path) == witness['sha256']
    external = json.loads(path.read_text())
    source = next(r for r in external['records'] if r['id'] == witness['record'])
    literal = ''.join(''.join(source['source_rows']).split())
    cipher = ''.join(c if c in C else '?' for c in literal)
    external_key = keys[witness['key_id']]
    reading = inspect(cipher, external_key, list(range(len(cipher))))
    assert reading['raw'] == source['expected_model_raw']
    start = witness['plaintext_start']
    assert reading['raw'][start:start+5] == witness['word'] == 'SECHS'
    assert reading['raw'].endswith(witness['context_raw'])
    word_positions = reading['positions'][start:start+5]
    assert all('?' not in p['pair'] and p['raw'] in 'SECHS' for p in word_positions)
    assert all(literal[i] in C for p in word_positions for i in p['source_indices'])
    by = {r['id']: r for r in records}
    earlier = by['p165_A5']['positions'][239]
    reply = by['p173_A1']['positions'][8]
    assert earlier['pair'] == 'VF' and earlier['source_indices'] == [473, 98]
    assert earlier['domain'] == '56'
    assert reply['pair'] == 'XX' and reply['source_indices'] == [121, 167]
    assert reply['domain'] == '56789'
    for record, position in [(by['p165_A5'], earlier), (by['p173_A1'], reply)]:
        for i in position['source_indices']:
            assert record['ciphertext'][i] in C
            assert record['ciphertext'][i] == record['readable_candidate']['ciphertext'][i]
    nov7 = layer_impact(records, keys['Nov7-9'], {'VF': '6', 'XA': '5'})
    nov10 = layer_impact(records, keys['Nov10-12'], {'XX': '6'})
    fixed7 = [(r['record'], r['variant'], p['plaintext_index'], p['pair'])
              for r in nov7['all_variant_results'] for p in r['newly_fixed_raw_positions']]
    fixed10 = [(r['record'], r['variant'], p['plaintext_index'], p['pair'])
               for r in nov10['all_variant_results'] for p in r['newly_fixed_raw_positions']]
    assert fixed7 == [('p165_A5', 'source_model', 239, 'VF'),
                      ('p165_A5', 'readable_candidate', 239, 'VF')]
    assert fixed10 == [('p173_A1', 'source_model', 8, 'XX'),
                       ('p173_A1', 'readable_candidate', 8, 'XX')]
    counterfactuals = []
    for digit in '56':
        k = assign(keys['Nov7-9'], {'VF': digit, 'XA': '5' if digit == '6' else '6'})
        text = inspect(by['p165_A5']['ciphertext'], k, list(range(500)))['raw']
        counterfactuals.append({'key_id': k['id'], 'VF': digit,
                               'unchanged_source_pair': earlier,
                               'raw_office_and_reference_ending': text[text.index('MARINEAMT'):]})
    for digit in '56789':
        k = assign(keys['Nov10-12'], {'XX': digit})
        text = inspect(by['p173_A1']['ciphertext'], k, list(range(242)))['raw']
        counterfactuals.append({'key_id': k['id'], 'XX': digit,
                               'unchanged_source_pair': reply,
                               'raw_reference_prefix': text[:18]})
    return {'assumptions': inputs['conditional_office_prefix_assumptions'],
            'independent_spelled_out_witness': {'record': witness['record'],
                                               'external_inputs_path': witness['path'],
                                               'external_inputs_sha256': witness['sha256'],
                                               'key_id': witness['key_id'],
                                               'raw_context': witness['context_raw'],
                                               'word': witness['word'],
                                               'word_positions': word_positions,
                                               'word_uses_only_complete_observed_pairs': True,
                                               'word_requires_no_coordinate_repairs': True,
                                               'office_name_limit': 'MARIN?AMT itself has a separate source erasure; every letter of SECHS is directly observed.'},
            'Nov7-9_layer': {**nov7,
                            'direct_witness': earlier,
                            'direct_assignment': 'VF=6 under the same-office-prefix assumption.',
                            'injective_complement': 'XA=5 because these are the only two unfilled cells and 5/6 are the only unused symbols.',
                            'local_occurrences_fixed_by_VF': [{'record': 'p165_A5', 'plaintext_index': 239}],
                            'local_occurrences_fixed_by_XA': []},
            'Nov10-12_layer': {**nov10, 'direct_witness': reply,
                              'direct_assignment': 'XX=6 under the same-office-prefix assumption.',
                              'remaining_unfilled_cell_symbols': '5789'},
            'all_counterfactual_source_compatible_digit_labels': counterfactuals,
            'reference_tails_compared_for_equality': False,
            'reference_tail_warning': 'p165 ends A?S8?3GG, whereas p173 cites A?S?24GG. They are not exact matching references. Consecutive numbering is not assumed.',
            'baseline_completion_warning': 'These conditional assignments disagree with the earlier completed-square hypotheses (Nov7 VF5/XA6 and Nov10 XX9). The audited partial keys remain unchanged.'}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    keys = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for key in inputs['keys']:
        assert key == keys[key['id']]
    earlier_context = inputs['existing_independent_Nov7_context']
    earlier_path = ROOT/earlier_context['path']
    assert sha(earlier_path) == earlier_context['sha256']
    assert json.loads(earlier_path.read_text())['contextual_cell_assignments'] == earlier_context['assignments']
    assert earlier_context['used_to_select_office_prefix_labels'] is False
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
            im = Image.open(HERE/source['path']).convert('RGB')
            assert im.size == (pixmap.width, pixmap.height) and im.tobytes() == pixmap.samples
    records = []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        cipher = ''.join(c if c in C else '?' for c in literal)
        assert len(literal) == source['source_slots'] == source['advertised_length']
        mapping = list(range(len(cipher)))
        key = keys[source['key_id']]
        observed = inspect(cipher, key, mapping)
        assert observed['raw'] == source['expected_raw']
        result = {'id': source['id'], 'key_id': source['key_id'], 'literal_source': literal,
                  'ciphertext': cipher, 'source_slots': len(literal),
                  'valid_coordinates': sum(c in C for c in literal),
                  'model_to_source_indices': mapping, **observed}
        result['readable_candidate'] = repair(source['readable_candidate'], cipher, key, mapping, literal)
        records.append(result)
    by = {r['id']: r for r in records}
    first, reply = by['p165_A1'], by['p173_A1']
    name_start = reply['raw'].index('CORCOVADO')
    name_positions = reply['positions'][name_start:name_start+9]
    assert all('?' not in p['pair'] for p in name_positions)
    earlier_name_start = first['raw'].index('CORCOVAUO')
    changed_name_position = earlier_name_start + 7
    assert first['raw'][changed_name_position] == 'U'
    assert first['readable_candidate']['raw'][changed_name_position] == 'D'
    assert reply['raw'][name_start+7] == 'D'
    price_start = first['raw'].index('10XMILL')
    price_positions = first['positions'][price_start:price_start+7]
    assert all('?' not in p['pair'] for p in price_positions)
    assert all(first['ciphertext'][i] == first['readable_candidate']['ciphertext'][i]
               for p in price_positions for i in p['source_indices'])
    assert [r['fixed_positions'] for r in records] == [190, 227, 190, 246, 119, 79]
    return {'schema': 'adfgvx-corcovado-sale-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based; printed part labels are preserved literally.',
            'summary': {'records': len(records),
                        'printed_source_slots': sum(r['source_slots'] for r in records),
                        'valid_source_coordinates': sum(r['valid_coordinates'] for r in records),
                        'plaintext_positions': sum(len(r['raw']) for r in records),
                        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
                        'readable_candidate_fixed_positions': sum(r['readable_candidate']['fixed_positions'] for r in records)},
            'records': records,
            'direct_purchase_price_witness': {'record': first['id'],
                                               'observed_field': '10XMILL',
                                               'positions': price_positions,
                                               'requires_no_key_assignments_or_coordinate_repairs': True,
                                               'currency': 'Not specified in this field.'},
            'cross_key_ship_name_witness': {'assumption': 'The sale terms and following report concern the same vessel.',
                                           'earlier_record': first['id'],
                                           'earlier_received_name': 'CORCOVAUO',
                                           'earlier_changed_plaintext_position': changed_name_position,
                                           'proposed_name': 'CORCOVADO',
                                           'independent_record': reply['id'],
                                           'independently_observed_name_positions': name_positions,
                                           'whole_messages_are_duplicates': False},
            'conditional_office_prefix_layers': office_layers(inputs, records, keys),
            'existing_independent_Nov7_context': earlier_context,
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The six records are new source editions under published keys; universal historical priority is not claimed.',
                       'The 4 TEILE header and printed 1, 2, 3, 5 part labels are retained without inventing another block.',
                       'The p165 price is literally 10 million; the currency is not stated in the recovered field.',
                       'The office-prefix digit assignments are conditional; the nonmatching reference tails are not equated.',
                       'Every remaining uncertain position and all locally changed raw/domain positions are retained under each conditional layer.']}


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
