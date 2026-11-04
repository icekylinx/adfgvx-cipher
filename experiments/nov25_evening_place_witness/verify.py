#!/usr/bin/env python3
"""Check the native cross-key TISZAFOELDVAR witness and its exact repair price.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = 'ADFGVX'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inverse(cipher, ranks, square):
    """Independent rectangular-column inverse with original source positions."""
    width = len(ranks)
    height, remainder = divmod(len(cipher), width)
    columns, origins, offset = {}, {}, 0
    for column in sorted(range(width), key=lambda c: ranks[c]):
        size = height + (column < remainder)
        columns[column] = cipher[offset:offset + size]
        origins[column] = list(range(offset, offset + size))
        offset += size
    assert offset == len(cipher)
    fractionated, source_positions = [], []
    for row in range(height + bool(remainder)):
        for column in range(width):
            if row < len(columns[column]):
                fractionated.append(columns[column][row])
                source_positions.append(origins[column][row])
    positions = []
    for start in range(0, len(fractionated), 2):
        pair = ''.join(fractionated[start:start + 2])
        cell = CO.index(pair[0]) * 6 + CO.index(pair[1])
        positions.append({'plaintext_index': start // 2, 'pair': pair,
                          'source_indices': source_positions[start:start + 2],
                          'cell': cell, 'value': square[cell]})
    return ''.join(p['value'] for p in positions), positions


def encode_word(word, square):
    return [CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in word]


def build(pdf=None, check_displays=True):
    data = json.loads((HERE / 'inputs.json').read_text())
    for path, sha in data['dependencies'].items():
        assert digest(ROOT / path) == sha, path
    recipient_dir = ROOT / data['recipient']['package']
    donor_dir = ROOT / data['donor']['package']
    recipient_module = load(recipient_dir / 'verify.py', 'evening_place_recipient')
    donor_module = load(donor_dir / 'verify.py', 'evening_place_donor')
    recipient_certificate = recipient_module.build(pdf)
    donor_certificate = donor_module.run()
    assert recipient_certificate == json.loads((recipient_dir / 'certificates.json').read_text())
    assert donor_certificate == json.loads((donor_dir / 'certificates.json').read_text())
    if pdf:
        donor_module.check_pdf(pdf)
    recipient_manifest = json.loads((recipient_dir / 'inputs.json').read_text())
    donor_manifest = json.loads((donor_dir / 'inputs.json').read_text())
    reader = load(ROOT / 'experiments/nov25_letter_constraint/verify.py', 'evening_place_reader')
    names_module = load(ROOT / 'experiments/nov25_treaty_digits/verify_names.py', 'evening_place_names')
    names = names_module.build()
    assert names == json.loads((ROOT / data['shared_square_certificate']).read_text())
    partial = names['conditional_partial_square']
    records = {}
    for role, manifest, cert in [('recipient', recipient_manifest, recipient_certificate),
                                  ('donor', donor_manifest, donor_certificate)]:
        request = data[role]
        record = next(r for r in manifest['records'] if r['id'] == request['id'])
        checked = next(r for r in cert['records'] if r['id'] == request['id'])
        key = (manifest['keys'][record['key_id']] if role == 'recipient' else manifest['key'])
        native = ''.join(''.join(record['source_rows']).split())
        assert set(native) <= set(CO)
        assert len(native) == request['source_length'] == 2 * request['plaintext_length']
        raw, positions = inverse(native, key['column_rank_order'], key['square'])
        assert raw == record['expected_raw']
        compared = reader.read(native, key['column_rank_order'], key['square'])
        assert raw == compared['plaintext']
        assert [p['source_indices'] for p in positions] == [p['frame_indices'] for p in compared['positions']]
        first, end = request['range']
        assert raw[first:end] == request['native_place']
        edition = (checked['readable_candidate']['ciphertext'] if role == 'recipient'
                   else checked['edition']['ciphertext'])
        # Every coordinate in both place spans predates this proposal.
        assert all(native[i] == edition[i] for p in positions[first:end] for i in p['source_indices'])
        records[role] = {'id': request['id'], 'key': key, 'native_ciphertext': native,
                         'prior_edition_ciphertext': edition, 'native_plaintext': raw,
                         'place_range': request['range'], 'place_positions': positions[first:end],
                         'positions': positions}
    target, donor = records['recipient'], records['donor']
    proposal = data['recipient']['proposed_place']
    assert donor['native_plaintext'][slice(*data['donor']['range'])] == proposal
    assert len(proposal) == 13 and len({i for p in donor['place_positions'] for i in p['source_indices']}) == 26
    assert target['key']['id'] != donor['key']['id']
    assert target['key']['column_rank_order'] != donor['key']['column_rank_order']
    anchor = data['donor']['supporting_Z']
    pos = donor['positions'][anchor['plaintext_index']]
    assert pos['pair'] == anchor['pair'] and pos['source_indices'] == anchor['source_indices'] and pos['value'] == 'Z'
    wanted = encode_word(proposal, target['key']['square'])
    assert wanted == encode_word(proposal, partial)
    prices = []
    for start in range(len(target['positions']) - len(proposal) + 1):
        cost = sum(a != b for p, pair in zip(target['positions'][start:start + len(proposal)], wanted)
                   for a, b in zip(p['pair'], pair))
        prices.append({'plaintext_start': start, 'observed_substitutions': cost})
    minimum = min(p['observed_substitutions'] for p in prices)
    minima = [p for p in prices if p['observed_substitutions'] == minimum]
    assert len(prices) == 98 and minima == [{'plaintext_start': 69, 'observed_substitutions': 1}]
    change = data['recipient']['mismatch']
    pos = target['positions'][change['plaintext_index']]
    assert pos['pair'] == change['pair'] and pos['source_indices'] == change['source_indices']
    prior_changes = [{'source_index': i, 'from': a, 'to': b}
                     for i, (a, b) in enumerate(zip(target['native_ciphertext'], target['prior_edition_ciphertext'])) if a != b]
    assert prior_changes == data['prior_recipient_changes']
    edition = list(target['prior_edition_ciphertext'])
    correction = change['source_change']
    assert edition[correction['source_index']] == correction['from']
    edition[correction['source_index']] = correction['to']
    edition = ''.join(edition)
    baseline, _ = inverse(edition, target['key']['column_rank_order'], target['key']['square'])
    shared, _ = inverse(edition, target['key']['column_rank_order'], partial)
    assert shared == data['expected_conditional_plaintext']
    assert re.sub('[^A-Z0-9?]', '', data['recipient']['german'].upper()) == shared[slice(*data['recipient']['display_range'])].replace('X', '')
    assert baseline[slice(*data['recipient']['range'])] == proposal
    all_changes = [{'source_index': i, 'from': a, 'to': b}
                   for i, (a, b) in enumerate(zip(target['native_ciphertext'], edition)) if a != b]
    assert all_changes == [correction] + prior_changes
    # The known pair's H becomes Z. Fixed-position counts remain unchanged.
    before = reader.read(target['prior_edition_ciphertext'], target['key']['column_rank_order'], partial)
    after = reader.read(edition, target['key']['column_rank_order'], partial)
    assert [i for i, (a, b) in enumerate(zip(before['plaintext'], after['plaintext'])) if a != b] == [72]
    assert sum(len(p['domain']) == 1 for p in before['positions']) == 103
    assert sum(len(p['domain']) == 1 for p in after['positions']) == 103
    witnesses = {
        'recipient_native': reader.witness(target['native_ciphertext'], target['key']['column_rank_order'], partial),
        'recipient_edition': reader.witness(edition, target['key']['column_rank_order'], partial),
        'donor_native': reader.witness(donor['native_ciphertext'], donor['key']['column_rank_order'], donor['key']['square']),
    }
    context = data['provisioning_context']
    context_record = next(r for r in recipient_manifest['records'] if r['id'] == context['id'])
    context_checked = next(r for r in recipient_certificate['records'] if r['id'] == context['id'])
    context_native = ''.join(''.join(context_record['source_rows']).split())
    context_key = recipient_manifest['keys'][context_record['key_id']]
    context_raw, context_positions = inverse(context_native, context_key['column_rank_order'], context_key['square'])
    context_edition = context_checked['readable_candidate']['ciphertext']
    context_shared, context_shared_positions = inverse(context_edition, context_key['column_rank_order'], partial)
    assert context_raw == context_record['expected_raw']
    assert context_raw[slice(*context['range'])] == context['baseline_labels']
    assert context_shared[slice(*context['range'])] == context['conditional_labels']
    for anchor in context['pairs']:
        p = context_positions[anchor['plaintext_index']]
        assert p['pair'] == anchor['pair'] and p['source_indices'] == anchor['source_indices']
        assert all(context_native[i] == context_edition[i] for i in p['source_indices'])
        assert context_shared_positions[anchor['plaintext_index']]['value'] == '1'
    assert sum(a != b for a, b in zip(context_native, context_edition)) == context['unchanged_observed_substitutions']
    assert context_shared == next(r for r in names['records'] if r['id'] == context['id'])['conditional_edition']
    assert re.sub('[^A-Z0-9?]', '', context['german'].upper()) == context_shared.replace('X', '')
    witnesses['provisioning_context_edition'] = reader.witness(context_edition, context_key['column_rank_order'], partial)
    if check_displays:
        for display in data['displays']:
            text = (ROOT / display['path']).read_text()
            assert all(field in text for field in display['required']), display['path']
    for item in records.values():
        del item['positions']
    return {'schema': 'adfgvx-nov25-evening-place-witness-certificate-v1',
            'authors': data['authors'], 'input_sha256': digest(HERE / 'inputs.json'),
            'indexing': 'Zero-based positions; ranges end-exclusive.',
            'summary': {'physical_sources_reused': 3, 'recipient_observed_coordinates': 220,
                        'donor_place_observed_coordinates': 26, 'donor_place_repairs': 0,
                        'new_recipient_substitutions': 1, 'total_recipient_substitutions': 2,
                        'source_mask_fills': 0, 'source_geometry_changes': 0,
                        'recipient_partial_fixed_positions_before': 103,
                        'recipient_partial_fixed_positions_after': 103,
                        'provisioning_army_positions_interpreted': 2,
                        'provisioning_context_new_substitutions': 0,
                        'provisioning_context_retained_substitutions': 3,
                        'all_word_starts_checked': 98, 'minimum_cost': minimum,
                        'minimum_word_starts': [p['plaintext_start'] for p in minima]},
            'records': records, 'all_word_start_prices': prices,
            'new_source_change': correction, 'prior_source_changes': prior_changes,
            'total_recipient_source_changes': all_changes,
            'recipient_edition_ciphertext': edition, 'recipient_baseline_edition': baseline,
            'conditional_partial_square': partial, 'recipient_conditional_edition': shared,
            'verified_recipient_display': {'range': data['recipient']['display_range'],
                                          'german': data['recipient']['german']},
            'provisioning_context': {**context, 'native_ciphertext': context_native,
                                     'native_plaintext': context_raw,
                                     'conditional_edition': context_shared},
            'full_roundtrip_witnesses': witnesses, 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    certificate = build(args.pdf)
    path = HERE / 'certificate.json'
    if args.verify:
        assert certificate == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **certificate['summary']}, indent=2))


if __name__ == '__main__':
    main()
