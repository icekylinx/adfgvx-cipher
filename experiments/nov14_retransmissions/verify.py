#!/usr/bin/env python3
"""Verify source readings, cross-key relationships and an interrupted copy.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No published key is completed or relabelled by this experiment.
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
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation(length, ranks):
    """Independent column-offset inverse: interim index -> source index."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (i < length % width) for i in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[i])
              for i in range(width)]
    indices = [starts[i % width] + i // width for i in range(length)]
    assert sorted(indices) == list(range(length))
    return indices


def inspect(record, key):
    literal = ''.join(''.join(record['source_rows']).split())
    assert len(literal) == record['source_slots']
    source_cipher = ''.join(c if c in C else '?' for c in literal)
    model = record.get('model', {'kind': 'identity'})
    if model['kind'] == 'prefix_erasure':
        mapping = [None] * model['missing_prefix_slots'] + list(range(len(literal)))
        cipher = '?' * model['missing_prefix_slots'] + source_cipher
        assert len(cipher) == model['full_length']
    else:
        assert model['kind'] == 'identity'
        mapping = list(range(len(literal)))
        cipher = source_cipher
    assert len(cipher) % 2 == 0
    square, ranks = key['square'], key['column_rank_order']
    order = permutation(len(cipher), ranks)
    middle = ''.join(cipher[i] for i in order)
    assert middle == untranspose(cipher, ranks)
    unused = set(ALPHABET) - set(square)
    positions = []
    for i in range(len(cipher) // 2):
        pair = middle[2*i:2*i+2]
        cells = [6*r+c for r in range(6) for c in range(6)
                 if pair[0] in ('?', C[r]) and pair[1] in ('?', C[c])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': order[2*i:2*i+2],
                          'source_indices': [mapping[j] for j in order[2*i:2*i+2]],
                          'domain': domain, 'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == record['expected_raw'] == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    restored = [None] * len(cipher)
    for ch, i in zip(middle, order):
        restored[i] = ch
    assert ''.join(restored) == cipher

    template = record['readable_template']
    assert len(template) == len(raw)
    proposed_middle = list(middle)
    for i, ch in enumerate(template):
        if ch == '?':
            assert raw[i] == '?'
            continue
        cell = square.index(ch)
        proposed_middle[2*i:2*i+2] = [C[cell//6], C[cell % 6]]
    target = [None] * len(cipher)
    for ch, i in zip(proposed_middle, order):
        target[i] = ch
    target = ''.join(target)
    assert decrypt(target, ranks, square) == template
    if '?' not in template:
        assert target == encrypt(template, ranks, square)
    substitutions = [{'source_index': mapping[i], 'model_index': i, 'from': a, 'to': b}
                     for i, (a, b) in enumerate(zip(cipher, target)) if a != '?' and a != b]
    fills = [{'source_index': mapping[i], 'model_index': i,
              'printed': literal[mapping[i]] if mapping[i] is not None else None, 'to': b}
             for i, (a, b) in enumerate(zip(cipher, target)) if a == '?' and a != b]
    repaired = list(cipher)
    for edit in substitutions + fills:
        repaired[edit['model_index']] = edit['to']
    assert ''.join(repaired) == target

    alternatives = []
    for spec in record['source_glyph_alternatives']:
        i = spec['source_index']
        assert literal[i] == '?' and set(spec['allowed_coordinates']) <= set(C)
        variants = []
        for ch in spec['allowed_coordinates']:
            model_i = mapping.index(i)
            variant = cipher[:model_i] + ch + cipher[model_i+1:]
            variants.append({'coordinate': ch, 'raw': decrypt(variant, ranks, square),
                             'agrees_with_readable_template_coordinate': ch == target[model_i]})
        alternatives.append({**spec, 'variants': variants})
    return {'id': record['id'], 'key_id': record['key_id'],
            'literal_source': literal, 'literal_source_ciphertext': source_cipher,
            'literal_source_unpaired_coordinate_count': len(literal) % 2,
            'model': model, 'model_to_source_indices': mapping,
            'ciphertext': cipher, 'raw': raw,
            'source_slots': len(literal), 'valid_coordinates': sum(c in C for c in literal),
            'fixed_positions': sum(len(p['domain']) == 1 for p in positions),
            'positions': positions, 'source_glyph_alternatives': alternatives,
            'readable_candidate': {'template': template, 'ciphertext': target,
                                   'known_coordinate_substitutions': substitutions,
                                   'source_erasure_fills': fills,
                                   'unknown_pairs_preserved': [p for p in positions if template[p['plaintext_index']] == '?'],
                                   'full_plaintext_reencryption_verified': '?' not in template,
                                   'key_changed': False, 'length_changed': False}}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    catalogue = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    keys = {k['id']: k for k in inputs['keys']}
    for name, key in keys.items():
        assert key == catalogue[name]
    for image in inputs['source_images']:
        assert sha(HERE/image['path']) == image['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        assert sha(pdf) == inputs['source']['pdf_sha256']
        document = fitz.open(pdf)
        for source in inputs['source_images']:
            page = document[source['pdf_page_1based'] - 1]
            pixmap = page.get_pixmap(matrix=fitz.Matrix(source['render_scale'], source['render_scale']),
                                    clip=fitz.Rect(*source['crop_pdf_points']))
            image = Image.open(HERE/source['path']).convert('RGB')
            assert image.size == (pixmap.width, pixmap.height)
            assert image.tobytes() == pixmap.samples
    records = [inspect(r, keys[r['key_id']]) for r in inputs['records']]
    by = {r['id']: r for r in records}

    a, b = by['p190_B'], by['p190_E']
    template = a['readable_candidate']['template']
    assert template == b['readable_candidate']['template'] and len(template) == 88
    witness_positions = []
    for i, ch in enumerate(template):
        witnesses = [r['id'] for r in (a, b) if r['raw'][i] == ch]
        witness_positions.append({'plaintext_index': i, 'proposed_symbol': ch,
                                  'observed_complete_pair_witnesses': witnesses,
                                  'raw_symbols': {r['id']: r['raw'][i] for r in (a, b)}})
    unwitnessed = [p for p in witness_positions if not p['observed_complete_pair_witnesses']]
    assert [(p['plaintext_index'], p['proposed_symbol']) for p in unwitnessed] == [(64, 'S')]

    shorter, longer = by['p190_D'], by['p193_A']
    short_template = shorter['readable_candidate']['template']
    long_template = longer['readable_candidate']['template']
    extra_e = long_template.index('FUER') + 2
    assert long_template[:extra_e] + long_template[extra_e+1:] == short_template
    relay_witnesses = []
    for i, ch in enumerate(long_template):
        short_i = None if i == extra_e else i if i < extra_e else i - 1
        witnesses = []
        if longer['raw'][i] == ch:
            witnesses.append({'record': longer['id'], 'plaintext_index': i})
        if short_i is not None and shorter['raw'][short_i] == ch:
            witnesses.append({'record': shorter['id'], 'plaintext_index': short_i})
        relay_witnesses.append({'longer_plaintext_index': i, 'shorter_plaintext_index': short_i,
                                'proposed_symbol': ch, 'observed_complete_pair_witnesses': witnesses})
    assert all(p['observed_complete_pair_witnesses'] for p in relay_witnesses)

    fragment, complete = by['p193_B'], by['p194_B']
    assert len(fragment['literal_source']) == 195 and len(complete['literal_source']) == 280
    assert fragment['literal_source'] == complete['literal_source'][85:]
    restored_cipher = complete['literal_source'][:85] + fragment['literal_source']
    assert restored_cipher == complete['literal_source']
    key = keys[fragment['key_id']]
    restored_raw = decrypt(restored_cipher, key['column_rank_order'], key['square'])
    assert restored_raw == complete['raw']
    prefix_restoration = [{'model_index': i, 'coordinate': complete['literal_source'][i],
                           'witness_record': complete['id'], 'witness_source_index': i}
                          for i in range(85)]
    fragment_restoration = {
        'fragment_record': fragment['id'], 'complete_record': complete['id'],
        'fragment_source_slots': 195, 'reference_source_slots': 280,
        'exact_suffix_start': 85, 'all_original_suffix_coordinates_match': True,
        'original_fragment_coordinates_changed': 0,
        'new_prefix_slots_supplied_by_observed_witness': 85,
        'prefix_restoration': prefix_restoration,
        'restored_ciphertext': restored_cipher, 'restored_raw': restored_raw,
        'fixed_positions_before_witness': fragment['fixed_positions'],
        'fixed_positions_after_witness': complete['fixed_positions'],
        'additional_fixed_raw_positions': complete['fixed_positions'] - fragment['fixed_positions'],
        'limit': 'The complete witness restores the interrupted source frame; its own SOLDLTENRATS garble and unknown name cell remain unchanged.'}

    a, b = by['p190_A'], by['p194_B']
    pa, pb = a['positions'][37], b['positions'][54]
    assert pa['pair'] == 'FX' and pb['pair'] == 'DG'
    assert a['raw'][35:39] == b['raw'][52:56] == 'FR?E'
    intersection = ''.join(sorted(set(pa['domain']) & set(pb['domain'])))
    assert intersection == '234789QY'
    reencryption_checks = []
    for ch in intersection:
        for record, pair in [(a, 'FX'), (b, 'DG')]:
            key = keys[record['key_id']]
            cell = 6*C.index(pair[0]) + C.index(pair[1])
            assert key['square'][cell] == '?' and ch not in key['square']
            square = key['square'][:cell] + ch + key['square'][cell+1:]
            candidate = record['readable_candidate']['template'].replace('?', ch)
            assert encrypt(candidate, key['column_rank_order'], square) == record['readable_candidate']['ciphertext']
            assert decrypt(record['readable_candidate']['ciphertext'], key['column_rank_order'], square) == candidate
        reencryption_checks.append({'shared_symbol': ch, 'displayed_name': 'FR'+ch+'E',
                                    'both_corrected_ciphertexts_reencrypt_exactly': True})
    return {'schema': 'adfgvx-nov14-cross-key-certificate-v1', 'project': inputs['project'],
            'authors': inputs['authors'], 'input_sha256': sha(HERE/'inputs.json'),
            'indexing': 'All indices are zero-based; printed group numbers are explicitly one-based.',
            'summary': {'records': len(records), 'source_slots': sum(r['source_slots'] for r in records),
                        'valid_coordinates': sum(r['valid_coordinates'] for r in records),
                        'model_coordinate_slots': sum(len(r['ciphertext']) for r in records),
                        'plaintext_positions': sum(len(r['raw']) for r in records),
                        'fixed_positions': sum(r['fixed_positions'] for r in records),
                        'witness_restored_coordinates': 85,
                        'witness_restored_raw_positions': fragment_restoration['additional_fixed_raw_positions'],
                        'fixed_positions_after_witness_restoration': sum(r['fixed_positions'] for r in records) + fragment_restoration['additional_fixed_raw_positions']},
            'records': records,
            'backup_station_pair': {'relationship': 'Aligned retransmissions under two distinct published keys.',
                                    'records': ['p190_B', 'p190_E'], 'template': template,
                                    'positions_with_complete_pair_witness': 87,
                                    'positions_without_complete_pair_witness': unwitnessed,
                                    'position_witnesses': witness_positions,
                                    'limit': 'The S in SEWASTOPOL remains editorial; the two damaged copies do not directly attest it.'},
            'relay_station_pair': {'relationship': 'Near-parallel retransmissions differing by FUR versus FUER.',
                                   'records': ['p190_D', 'p193_A'],
                                   'shorter_template': short_template, 'longer_template': long_template,
                                   'extra_e_in_longer_plaintext_index': extra_e,
                                   'positions_with_complete_pair_witness': len(relay_witnesses),
                                   'position_witnesses': relay_witnesses,
                                   'limit': 'The 186- and 188-coordinate frames remain separate; no source ciphertext insertion is claimed.'},
            'interrupted_arrival_copy': fragment_restoration,
            'arrival_name_relation': {'relationship': 'Near-parallel arrival notices with differing wording.',
                                      'earlier': {'record': a['id'], **pa},
                                      'later': {'record': b['id'], **pb},
                                      'conditional_assumption': 'Both four-slot name fields encode the same correctly copied name.',
                                      'shared_domain': intersection,
                                      'additional_letter_only_domain': 'QY',
                                      'conditional_reencryption_checks': reencryption_checks,
                                      'surname_proposal': 'FRYE',
                                      'proposal_status': 'Lexically plausible only; not uniquely implied by the shared-domain constraint. No independent historical identification is established.',
                                      'global_square_assignment_made': False},
            'limits': ['Readable candidates are editorial templates, separately costed against literal source coordinates.',
                       'A fixed raw character can itself be garbled; fixed-position totals do not count historically correct letters.',
                       'Shared-name equality alone leaves eight possible symbols, and a letter-only assumption leaves Q or Y.',
                       'The source contains one visible A/X overstrike; both alternatives are retained and decrypted.',
                       'The p193 B literal source is an odd-length interrupted record. Its declared 280-coordinate frame and 85 missing prefix coordinates are explicit; only the independent p194 B source supplies them.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    output = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(output.read_text())
    else:
        output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
