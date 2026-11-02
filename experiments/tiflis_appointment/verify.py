#!/usr/bin/env python3
"""Separate source geometry, ordinary-word repair and historical name inference.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The published substitution squares remain unchanged.
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
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (j < length % width) for j in range(width)]
    starts = [sum(heights[k] for k in range(width) if ranks[k] < ranks[j])
              for j in range(width)]
    result = [starts[j % width] + j // width for j in range(length)]
    assert sorted(result) == list(range(length))
    return result


def inspect(cipher, key, mapping):
    square, ranks = key['square'], key['column_rank_order']
    assert len(cipher) % 2 == 0 and len(mapping) == len(cipher)
    perm = permutation(len(cipher), ranks)
    middle = ''.join(cipher[j] for j in perm)
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
        indices = perm[2*i:2*i+2]
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices],
                          'domain': domain, 'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    return {'raw': raw, 'fixed_positions': sum(p['raw'] != '?' for p in positions),
            'positions': positions}


def form_model(record):
    literal = ''.join(''.join(record['source_rows']).split())
    cipher = ''.join(c if c in C else '?' for c in literal)
    mapping = list(range(len(literal)))
    model = record.get('model', {'kind': 'identity'})
    if model['kind'] == 'insert_unknown_group':
        gap, n = model['source_gap'], model['length']
        cipher = cipher[:gap] + '?'*n + cipher[gap:]
        mapping[gap:gap] = [None]*n
    elif model['kind'] == 'prefix_erasure':
        n = model['missing_prefix_slots']
        cipher = '?'*n + cipher
        mapping = [None]*n + mapping
    elif model['kind'] == 'move_prefix_group_to_body_gap':
        n, gap = model['prefix_length'], model['body_gap']
        mapping = list(range(n, n+gap)) + list(range(n)) + list(range(n+gap, len(literal)))
        cipher = ''.join(cipher[i] for i in mapping)
    else:
        assert model['kind'] == 'identity'
    return literal, cipher, mapping


def masked_encryption(template, key):
    square = key['square']
    middle = ''.join('??' if ch == '?' else C[square.index(ch)//6] + C[square.index(ch) % 6]
                     for ch in template)
    target = [None]*len(middle)
    for ch, i in zip(middle, permutation(len(middle), key['column_rank_order'])):
        target[i] = ch
    return ''.join(target)


def repair(template, base, key, mapping):
    assert len(template)*2 == len(base)
    target = masked_encryption(template, key)
    target = ''.join(a if b == '?' else b for a, b in zip(base, target))
    result = inspect(target, key, mapping)
    assert result['raw'] == template
    substitutions, fills = [], []
    for i, (a, b) in enumerate(zip(base, target)):
        if a == b:
            continue
        event = {'model_index': i, 'source_index': mapping[i], 'from': a, 'to': b}
        (fills if a == '?' else substitutions).append(event)
    rebuilt = list(base)
    for event in substitutions + fills:
        rebuilt[event['model_index']] = event['to']
    assert ''.join(rebuilt) == target
    if '?' not in template:
        assert target == encrypt(template, key['column_rank_order'], key['square'])
    return {'template': template, 'ciphertext': target,
            'known_coordinate_substitutions': substitutions,
            'inserted_coordinate_fills': fills,
            'full_reencryption_verified': '?' not in template, **result}


def source_geometry(record, key):
    literal = ''.join(''.join(record['source_rows']).split())
    stencil = record['geometry_stencil']
    assert stencil[60:68] == '?'*8 and stencil[109:116] == '?'*7
    assert 'Y' not in stencil and key['square'][17] == '?'
    target = masked_encryption(stencil, key)
    assert len(target) == record['advertised_length'] == 232
    models = []
    for gap in range(len(literal) + 1):
        cipher = literal[:gap] + '?'*5 + literal[gap:]
        mismatches = [i for i, (a, b) in enumerate(zip(cipher, target))
                      if a != '?' and b != '?' and a != b]
        models.append({'source_gap': gap,
                       'known_coordinate_substitutions': len(mismatches),
                       'compared_observed_coordinates': sum(a != '?' and b != '?' for a, b in zip(cipher, target)),
                       'mismatch_model_indices': mismatches})
    minimum = min(m['known_coordinate_substitutions'] for m in models)
    best = [m for m in models if m['known_coordinate_substitutions'] == minimum]
    assert [(m['source_gap'], m['known_coordinate_substitutions']) for m in best] == [(150, 1)]
    return {'model_definition': 'One contiguous five-coordinate gap at any boundary of the 227-coordinate source.',
            'stencil': stencil, 'masked_name_positions': list(range(60, 68)),
            'masked_signature_positions': list(range(109, 116)),
            'models_examined': len(models), 'minimum_known_coordinate_changes': minimum,
            'all_tied_minima': best, 'all_models': models,
            'historical_name_used_in_geometry_search': False,
            'limit': 'The minimum is exact for the declared ordinary-word stencil and single-group-loss model, not a proof of the original transmission error.'}


def changed_key(key, pair, symbol):
    square = key['square']
    cell = 6*C.index(pair[0]) + C.index(pair[1])
    assert square[cell] == '?' and symbol not in square
    return {**key, 'square': square[:cell] + symbol + square[cell+1:]}


def preamble_geometry(record, key):
    literal = ''.join(''.join(record['source_rows']).split())
    spec = record['floating_group_geometry']
    group = spec['group']
    assert literal.startswith(group) and len(group) == 5
    body = literal[len(group):]
    stencil = spec['ordinary_word_stencil']
    assert all(stencil[i] == '?' for i in spec['masked_name_and_reference_plaintext_indices'])
    assert all(name not in stencil for name in ['KRESS', 'TIFLIS', 'WARSCHAU', 'OSTROWSKI'])
    target = masked_encryption(stencil, key)
    assert len(literal) == len(target) == 262 and len(body) == 257
    trials = []
    for gap in range(len(body) + 1):
        candidate = body[:gap] + group + body[gap:]
        mismatches = [i for i, (a, b) in enumerate(zip(candidate, target))
                      if b != '?' and a != b]
        trials.append({'body_gap': gap, 'known_coordinate_substitutions': len(mismatches),
                       'mismatch_model_indices': mismatches})
    minimum = min(t['known_coordinate_substitutions'] for t in trials)
    best = [t for t in trials if t['known_coordinate_substitutions'] == minimum]
    assert [(t['body_gap'], t['known_coordinate_substitutions']) for t in best] == [(10, 2)]
    return {'declared_model': 'Place the five observed floating FGFFF coordinates at every boundary of the 257-coordinate main grid; no source letters are added or removed.',
            'ordinary_word_stencil': stencil,
            'masked_name_and_reference_plaintext_indices': spec['masked_name_and_reference_plaintext_indices'],
            'models_examined': len(trials), 'minimum_known_coordinate_changes': minimum,
            'all_tied_minima': best, 'all_trials': trials,
            'literal_top_first_fit': trials[0],
            'historical_names_used_in_placement_search': False,
            'limit': 'Exact for the declared ordinary-word stencil and floating-group movement model; it does not establish the p192 date or prove message identity.'}


def layer_impact(records, keys, key_id, pair):
    updated = changed_key(keys[key_id], pair, 'Y')
    impact = []
    for record in records:
        if record['key_id'] != key_id:
            continue
        _, cipher, mapping = form_model(record)
        before = inspect(cipher, keys[key_id], mapping)
        after = inspect(cipher, updated, mapping)
        changed_domains = [{'plaintext_index': i, 'before': a['domain'], 'after': b['domain'],
                            'pair': a['pair'], 'source_indices': a['source_indices']}
                           for i, (a, b) in enumerate(zip(before['positions'], after['positions']))
                           if a['domain'] != b['domain']]
        changed_raw = [{'plaintext_index': i, 'before': a, 'after': b,
                        'pair': before['positions'][i]['pair'],
                        'source_indices': before['positions'][i]['source_indices']}
                       for i, (a, b) in enumerate(zip(before['raw'], after['raw'])) if a != b]
        if changed_domains:
            impact.append({'record': record['id'], 'raw_before': before['raw'], 'raw_after': after['raw'],
                           'newly_fixed_raw_positions': changed_raw,
                           'all_changed_marginal_domains': changed_domains})
    return impact


def check_pixels(pdf, sources, expected):
    import fitz
    from PIL import Image
    assert pdf.stat().st_size == expected['pdf_bytes'] and sha(pdf) == expected['pdf_sha256']
    doc = fitz.open(pdf)
    for source in sources:
        page = doc[source['pdf_page_1based'] - 1]
        scale = source['render_scale']
        pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*source['crop_pdf_points']))
        image = Image.open(HERE/source['path']).convert('RGB')
        assert image.size == (pixmap.width, pixmap.height) and image.tobytes() == pixmap.samples


def build(pdf=None, historical_pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    keys = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    key = inputs['key']
    assert key == keys[key['id']]
    historical = inputs['historical_reference']
    for source in inputs['source_images'] + [historical['source_crop']]:
        assert sha(HERE/source['path']) == source['sha256']
    if pdf:
        check_pixels(pdf, inputs['source_images'], inputs['source'])
    if historical_pdf:
        check_pixels(historical_pdf, [historical['source_crop']], historical)
        import fitz
        text = ' '.join(fitz.open(historical_pdf)[2].get_text().split())
        assert historical['name_evidence']['short_quote'] in text
    records = []
    for record in inputs['records']:
        literal, cipher, mapping = form_model(record)
        assert set(literal) <= set(C) and len(literal) == record['source_slots']
        assert len(cipher) == record['advertised_length']
        observed = inspect(cipher, key, mapping)
        assert observed['raw'] == record['expected_model_raw']
        r = {'id': record['id'], 'key_id': key['id'], 'literal_source': literal,
             'source_slots': len(literal), 'source_unpaired_coordinate_count': len(literal) % 2,
             'model': record['model'], 'model_ciphertext': cipher,
             'model_to_source_indices': mapping, **observed}
        if record['id'] in ('p192_2', 'p199_B1'):
            r['editorial_candidates'] = [{'id': c['id'], 'reason': c['reason'],
                                          **repair(c['plaintext'], cipher, key, mapping)}
                                         for c in record['editorial_candidates']]
            if record['id'] == 'p199_B1':
                r['literal_top_first_reading'] = inspect(literal, key, list(range(len(literal))))
                assert r['literal_top_first_reading']['raw'] == record['expected_literal_raw']
                r['floating_group_geometry'] = preamble_geometry(record, key)
                candidate = r['editorial_candidates'][0]
                assert len(candidate['known_coordinate_substitutions']) == 2
                assert not candidate['inserted_coordinate_fills'] and candidate['fixed_positions'] == 129
                assert sorted(mapping) == list(range(len(literal)))
        else:
            assert record['id'] == 'p192_3'
            r['geometry_screen'] = source_geometry(record, key)
            r['ordinary_word_repair'] = repair(record['ordinary_word_template'], cipher, key, mapping)
            assert r['ordinary_word_repair']['fixed_positions'] == 114
            assert len(r['ordinary_word_repair']['known_coordinate_substitutions']) == 1
            assert len(r['ordinary_word_repair']['inserted_coordinate_fills']) == 4
            completed_key = changed_key(key, 'FX', 'Y')
            r['historical_name_repair'] = repair(record['historical_name_candidate'], cipher, completed_key, mapping)
            assert len(r['historical_name_repair']['known_coordinate_substitutions']) == 1
            assert len(r['historical_name_repair']['inserted_coordinate_fills']) == 5
            assert r['historical_name_repair']['fixed_positions'] == 116
            occurrence = r['positions'][61]
            assert occurrence['pair'] == 'FX' and occurrence['source_indices'] == [80, 138]
            assert all(i is not None and i < 150 for i in occurrence['source_indices'])
            for i in occurrence['model_indices']:
                assert cipher[i] == r['historical_name_repair']['ciphertext'][i]
            r['name_assignment_occurrence'] = occurrence
            checks = []
            for symbol in occurrence['domain']:
                counterfactual = changed_key(key, 'FX', symbol)
                candidate = record['historical_name_candidate'].replace('TYDELSKI', 'T'+symbol+'DELSKI')
                assert encrypt(candidate, key['column_rank_order'], counterfactual['square']) == r['historical_name_repair']['ciphertext']
                checks.append({'symbol': symbol, 'name': 'T'+symbol+'DELSKI', 'same_ciphertext_reencrypts': True})
            r['reencryption_does_not_choose_the_historical_name'] = checks
        records.append(r)
    external = ROOT/'experiments/nov14_retransmissions/inputs.json'
    external_inputs = json.loads(external.read_text())
    inventory = inputs['records'] + external_inputs['records']
    direct = layer_impact(inventory, keys, 'Nov13-15b', 'FX')
    transfer = layer_impact(inventory, keys, 'Nov13-15a', 'DG')
    direct_fixed = [(r['record'], p['plaintext_index']) for r in direct for p in r['newly_fixed_raw_positions']]
    transfer_fixed = [(r['record'], p['plaintext_index']) for r in transfer for p in r['newly_fixed_raw_positions']]
    assert direct_fixed == [('p192_3', 61), ('p190_A', 37)]
    assert transfer_fixed == [('p194_B', 54), ('p193_B', 54)]
    return {'schema': 'adfgvx-tiflis-appointment-certificate-v1', 'project': inputs['project'],
            'authors': inputs['authors'], 'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based; printed group numbers are explicitly one-based.',
            'summary': {'records': 3, 'printed_source_slots': 719, 'valid_source_coordinates': 719,
                        'declared_model_coordinate_slots': 724, 'plaintext_positions': 362,
                        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
                        'preamble_fixed_positions_after_group_placement': 129,
                        'part3_ordinary_word_fixed_positions': 114,
                        'part3_conditional_name_fixed_positions': 116},
            'records': records,
            'cross_page_association': inputs['cross_page_association'],
            'conditional_key_layers': {
                'inventory_scope': 'All three Tiflis records and all seven source records in the November 14 retransmissions edition; every changed raw character and marginal domain is retained.',
                'external_inputs_path': str(external.relative_to(ROOT)), 'external_inputs_sha256': sha(external),
                'layer1': {'assumptions': ['The stated single-group gap model and ordinary-word alignment are correct.',
                                           'The courier surname identifies the independently attested Tadeusz Tydelski, with its correct spelling.'],
                           'assignment': {'key_id': 'Nov13-15b', 'coordinate_pair': 'FX', 'square_cell_index': 17, 'symbol': 'Y'},
                           'depends_on_pilot_name_identity': False, 'affected_records': direct},
                'layer2': {'additional_assumption': 'The p190 A and p194 B FR?E fields encode the same correctly copied surname.',
                           'assignment': {'key_id': 'Nov13-15a', 'coordinate_pair': 'DG', 'square_cell_index': 9, 'symbol': 'Y'},
                           'affected_records': transfer},
                'published_key_files_changed': False},
            'limits': ['The independently sourced p199 part 1 is strongly associated with the unheaded p192 parts 2 and 3 by syntax, stated multipart count and key. Their conflicting November 14/15 headings remain unresolved.',
                       'The floating-group placement masks all relevant historical names and reference symbols; no historical identity was used to select it.',
                       'The missing-group minimum is conditional on a declared ordinary-word stencil. Neither courier name nor signature is used in that screen.',
                       'Historical identity is independently supported but remains an inference; the original archival manuscript and appointment telegram have not been inspected.',
                       'Reencryption alone permits all eight unused symbols in the name cell. The historical name evidence is what selects Y.',
                       'Transferring Y from Nov13–15b FX to Nov13–15a DG additionally depends on the pilot same-name assumption.']}


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
