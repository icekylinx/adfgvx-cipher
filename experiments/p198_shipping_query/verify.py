#!/usr/bin/env python3
"""Recompute p198 A's source-directed shipping-query reconstruction.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import itertools
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import ALPHABET, decrypt, encrypt, transpose, untranspose
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, masked_encryption, permutation
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame(literal, excluded, gap):
    assert len(set(excluded)) == 4 and len(literal) == 247
    retained = [i for i in range(247) if i not in excluded]
    at = next(j for j, origin in enumerate(retained) if origin >= gap)
    mapping = retained[:at] + [None] + retained[at:]
    source = ''.join('?' if i is None or literal[i] not in C else literal[i] for i in mapping)
    assert len(mapping) == len(source) == 244
    assert len(set(i for i in mapping if i is not None)) == 243
    return source, mapping


def price(source, wanted, mapping):
    substitutions, masks, additions = [], [], []
    for i, (observed, proposed) in enumerate(zip(source, wanted)):
        if proposed not in C or observed == proposed:
            continue
        event = {'model_index': i, 'source_index': mapping[i], 'from': observed, 'to': proposed}
        (substitutions if observed in C else masks if mapping[i] is not None else additions).append(event)
    return substitutions, masks, additions


def candidate(source, mapping, literal, key, template):
    wanted = masked_encryption(template, key)
    changed, masks, additions = price(source, wanted, mapping)
    edited = ''.join(b if b in C else a for a, b in zip(source, wanted))
    result = inspect(edited, key, mapping)
    assert all(a == '?' or a == b for a, b in zip(template, result['raw']))
    for event in changed + masks + additions:
        origin = event['source_index']
        event['printed'] = literal[origin] if origin is not None else None
    rebuilt = list(source)
    for event in changed + masks + additions:
        rebuilt[event['model_index']] = event['to']
    assert ''.join(rebuilt) == edited
    return {'template': template, 'ciphertext': edited, **result,
            'known_coordinate_substitutions': changed, 'printed_mask_fills': masks,
            'inserted_slot_fills': additions}


def complete(layer, key):
    unknown_cells = [i for i, ch in enumerate(key['square']) if ch == '?']
    missing = sorted(set(ALPHABET) - set(key['square']))
    assert len(unknown_cells) == 2 and missing == ['5', '6']
    missing_coordinates = [i for i, ch in enumerate(layer['ciphertext']) if ch == '?']
    assert len(missing_coordinates) == 3
    witnesses = []
    for labels in itertools.permutations(missing):
        square = list(key['square'])
        for index, label in zip(unknown_cells, labels):
            square[index] = label
        square = ''.join(square)
        assert len(set(square)) == 36
        for values in itertools.product(C, repeat=3):
            received = list(layer['ciphertext'])
            for index, value in zip(missing_coordinates, values):
                received[index] = value
            received = ''.join(received)
            plaintext = decrypt(received, key['column_rank_order'], square)
            assert encrypt(plaintext, key['column_rank_order'], square) == received
            assert all(a == '?' or a == b for a, b in zip(layer['raw'], plaintext))
            witnesses.append({'square': square, 'ciphertext': received, 'plaintext': plaintext,
                              'first_steamer': plaintext[72:79], 'quantity': plaintext[104:110]})
    quantities = sorted({w['quantity'] for w in witnesses})
    assert len(witnesses) == len({w['plaintext'] for w in witnesses}) == 432
    assert len(quantities) == 12
    assert {w['first_steamer'][0] for w in witnesses} == set('MPRUWY')
    assert {w['first_steamer'][1] for w in witnesses} == set('DEQTUX')
    assert all(w['quantity'][:2] == '11' and w['quantity'][4:] == '0K' for w in witnesses)
    return {'globally_injective_key_completions': 2, 'unfilled_coordinate_positions': missing_coordinates,
            'complete_plaintext_count': 432, 'joint_quantity_values': quantities,
            'first_steamer_initial_domain': 'MPRUWY', 'first_steamer_second_label_domain': 'DEQTUX', 'witnesses': witnesses,
            'historical_value_claim': False}


def geometries(literal, key, template):
    wanted = masked_encryption(template, key)
    prices, records = [], []
    for first, second, tail, gap in itertools.product(
            range(6), range(6, 12), itertools.combinations(range(241, 247), 2), range(92, 97)):
        excluded = [first, second, *tail]
        base, mapping = frame(literal, excluded, gap)
        edits, masks, additions = price(base, wanted, mapping)
        prices.append([*excluded, gap, len(edits), len(masks), len(additions)])
        records.append((excluded, gap, base, mapping))
    assert len(prices) == len(records) == 2700
    minimum = min(row[5] for row in prices)
    ties = []
    for costs, (excluded, gap, base, mapping) in zip(prices, records):
        if costs[5] != minimum:
            continue
        raw = inspect(base, key, mapping)
        edited = candidate(base, mapping, literal, key, template)
        ties.append({'excluded_source_indices': excluded, 'insert_before_original_source': gap,
                     'excluded_valid_coordinates': sum(literal[i] in C for i in excluded),
                     'excluded_masks': sum(literal[i] not in C for i in excluded),
                     'raw': raw['raw'], 'fixed_raw_positions': raw['fixed_positions'],
                     'edited_raw': edited['raw'], 'known_coordinate_substitutions': len(edited['known_coordinate_substitutions']),
                     'printed_mask_fills': len(edited['printed_mask_fills']),
                     'inserted_slot_fills': len(edited['inserted_slot_fills']),
                     'first_steamer_initial_pair': raw['positions'][72]['pair'],
                     'first_steamer_initial_domain': raw['positions'][72]['domain'],
                     'edited_ciphertext_sha256': hashlib.sha256(edited['ciphertext'].encode()).hexdigest()})
    assert minimum == 5 and len(ties) == 4
    assert {tuple(row['excluded_source_indices']) for row in ties} == {
        (4, second, 245, 246) for second in [6, 7, 8, 9]}
    assert all(row['insert_before_original_source'] == 92 for row in ties)
    assert len({row['raw'] for row in ties}) == len({row['edited_raw'] for row in ties}) == 1
    return {'maps_checked': len(prices), 'price_columns': ['excluded_first', 'excluded_second', 'excluded_tail_first',
            'excluded_tail_second', 'insert_before_original_source', 'observed_substitutions', 'printed_mask_fills', 'inserted_slot_fills'],
            'all_prices_sha256': hashlib.sha256(json.dumps(prices, separators=(',', ':')).encode()).hexdigest(),
            'substitution_cost_histogram': {str(k): v for k, v in sorted(Counter(row[5] for row in prices).items())},
            'minimum_observed_substitutions': minimum, 'all_minimum_maps': ties,
            'distinct_edited_ciphertexts': len({row['edited_ciphertext_sha256'] for row in ties})}


def fold(text):
    return re.sub('[^A-Z0-9?]', '', text.upper()).replace('X', '')


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov7-9')
    prior = data['prior_ocr']
    assert sha(HERE / prior['path']) == prior['sha256']
    assert sha(ROOT / prior['source_path']) == prior['source_sha256']
    assert load(HERE / prior['path']) == next(r for r in load(ROOT / prior['source_path'])['blocks']
                                             if r['id'] == prior['source_record_id'])
    record = data['records'][0]
    literal = ''.join(''.join(record['source_rows']).split())
    assert len(literal) == record['source_slots'] == 247
    assert record['advertised_length'] == 244
    assert [(i, c) for i, c in enumerate(literal) if c not in C] == [
        (3, 'T'), (8, 'T'), (15, 'U'), (24, 'U'), (26, 'N'), (29, 'U'), (49, 'C'), (129, '-'), (130, '-'), (192, 'C')]
    assert literal[:6] == 'XADTAF' and literal[6:12] == 'AATAGV'
    assert literal[92:96] == 'XGAX' and literal[241:] == 'AXVDXX'
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    native = ''.join(c if c in C else '?' for c in literal)
    assert transpose(untranspose(native, key['column_rank_order']), key['column_rank_order']) == native
    native_order = permutation(247, key['column_rank_order'])
    native_diagnostic = {'raw': decrypt(native, key['column_rank_order'], key['square'], allow_unpaired=True),
                         'paired_plaintext_positions': 123, 'orphan_source_index': native_order[-1],
                         'orphan_coordinate': native[native_order[-1]], 'full_coordinate_roundtrip_verified': True}
    af = record['analysis_frame']
    base, mapping = frame(literal, af['excluded_source_indices'], af['insert_unknown_before_original_source'])
    raw = inspect(base, key, mapping)
    edited = candidate(base, mapping, literal, key, record['edited_output'])
    assert raw['fixed_positions'] == 111 and edited['raw'] == record['edited_output']
    assert (edited['fixed_positions'], len(edited['known_coordinate_substitutions']),
            len(edited['printed_mask_fills']), len(edited['inserted_slot_fills'])) == (118, 5, 6, 1)
    assert base.count('?') == 10 and sum(literal[i] in C for i in af['excluded_source_indices']) == 3
    assert 'TRANSPORVERSICHERUNG' in edited['raw'] and 'TRANSPORTVERSICHERUNG' not in edited['raw']
    scope = geometries(literal, key, record['edited_output'])
    completions = complete(edited, key)
    glyph_sensitivity = []
    for first, second in itertools.product('CG', repeat=2):
        variant = list(literal)
        variant[49], variant[192] = first, second
        variant = ''.join(variant)
        vbase, vmapping = frame(variant, af['excluded_source_indices'], af['insert_unknown_before_original_source'])
        vraw = inspect(vbase, key, vmapping)
        vedited = candidate(vbase, vmapping, variant, key, record['edited_output'])
        vscope = geometries(variant, key, record['edited_output'])
        assert vscope['minimum_observed_substitutions'] == 5 and len(vscope['all_minimum_maps']) == 4
        glyph_sensitivity.append({'source_49': first, 'source_192': second,
                                  'raw': vraw['raw'], 'raw_fixed_positions': vraw['fixed_positions'],
                                  'edited_raw': vedited['raw'], 'edited_fixed_positions': vedited['fixed_positions'],
                                  'observed_substitutions': len(vedited['known_coordinate_substitutions']),
                                  'printed_mask_fills': len(vedited['printed_mask_fills']),
                                  'added_slot_fills': len(vedited['inserted_slot_fills']),
                                  'minimum_map_count': len(vscope['all_minimum_maps']),
                                  'price_table_sha256': vscope['all_prices_sha256']})
    text = (ROOT / data['case']).read_text()
    assert text.count(expected_legend(ROOT / data['case'])) == 1
    fences, quotes = displays(text)
    assert [r['role_from_caption'] for r in fences] == ['raw_output', 'edited_output', 'source_transcription']
    assert [r['role_from_caption'] for r in quotes] == ['readable_german']
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    assert bodies[:2] == [raw['raw'], edited['raw']] and ''.join(bodies[2].split()) == literal
    visible = re.findall(r'^> (.*)$', text, re.M)
    assert visible == [record['readable_german']] and fold(visible[0]) == fold(edited['raw'])
    summary = {'physical_records': 1, 'printed_source_slots': 247, 'valid_source_coordinates': 237,
               'printed_mask_slots': 10, 'native_paired_positions': 123, 'native_orphan_coordinates': 1,
               'excluded_source_slots': 4, 'excluded_valid_coordinates': 3, 'excluded_invalid_glyphs': 1,
               'added_unknown_slots': 1, 'modeled_coordinates': 244, 'plaintext_positions': 122,
               'raw_fixed_positions': 111, 'edited_fixed_positions': 118,
               'observed_coordinate_substitutions': 5, 'printed_mask_fills': 6, 'inserted_slot_fills': 1}
    return {'schema': 'adfgvx-gap21-late-certificate-v1', 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': data['indexing'], 'summary': summary,
            'records': [{'id': record['id'], 'literal_source': literal, 'source_slots': 247,
                         'ciphertext': base, 'model_to_source_indices': mapping,
                         'excluded_source_indices': af['excluded_source_indices'], **raw,
                         'readable_candidate': edited, 'native_odd_frame_diagnostic': native_diagnostic}],
            'geometry_enumeration': scope, 'global_completion_frontier': completions,
            'C_G_glyph_sensitivity': glyph_sensitivity,
            'prior_credit': data['prior_credit'], 'limits': data['limits']}, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    certificate, evidence = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert certificate == load(path)
    else:
        path.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
