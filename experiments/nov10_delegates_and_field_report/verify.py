#!/usr/bin/env python3
"""Verify two Nov10 message families and exact native-frame coordinate repairs.

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
    from itertools import permutations
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    current = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    assert key == current[key['id']]
    assert sha(HERE/'prior_candidates.json') == inputs['prior_attribution_check']['earlier_repository_candidates']['sha256']
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path']) == crop['sha256']
    if pdf:
        verify_crops(pdf, inputs['source'], inputs['source_images'], HERE)
    records, inventory = [], []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        assert set(literal) <= set(C)
        assert len(literal) == source['source_slots'] == source['advertised_length']
        mapping = list(range(len(literal)))
        raw = inspect(literal, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], literal, key, mapping, literal)
        assert not candidate['erased_coordinate_fills']
        changes = []
        for a, b in zip(raw['positions'], candidate['positions']):
            if a != b:
                changes.append({'plaintext_index': a['plaintext_index'], 'before': a, 'after': b})
        records.append({'id': source['id'], 'literal_source': literal, 'ciphertext': literal,
                        'source_slots': len(literal), 'valid_coordinates': len(literal),
                        'model_to_source_indices': mapping, **raw,
                        'readable_candidate': candidate, 'all_changed_plaintext_positions': changes})
        for label, reading in [('literal_source', raw), ('ordinary_word_candidate', candidate)]:
            inventory.append({'record': source['id'], 'variant': label,
                              'all_raw_numeral_or_unknown_positions': [p for p in reading['positions'] if p['raw'] in '0123456789?']})
    assert [r['source_slots'] for r in records] == [192,104,252,272]
    assert [r['fixed_positions'] for r in records] == [96,51,125,136]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [4,1,1,4]
    assert records[3]['literal_source'][150:155] == 'VDVAV'
    time = records[1]
    unknowns = [p for p in time['positions'] if p['raw'] == '?']
    assert len(unknowns) == 1
    unknown = unknowns[0]
    assert unknown['plaintext_index'] == 33 and unknown['pair'] == 'FD'
    assert unknown['source_indices'] == [42,69] and unknown['domain'] == '56789'
    assert unknown == time['readable_candidate']['positions'][33]
    # Enumerate all five-factorial injective completions. This is a finite
    # compatibility audit, not a claim that any digit is historically true.
    missing = sorted(set(A)-set(key['square']))
    cells = [i for i,c in enumerate(key['square']) if c == '?']
    assert len(missing) == len(cells) == 5
    counts, witnesses = {}, {}
    for labels in permutations(missing):
        square = list(key['square'])
        for cell, label in zip(cells, labels):
            square[cell] = label
        square = ''.join(square)
        plain = decrypt(time['readable_candidate']['ciphertext'], key['column_rank_order'], square)
        digit = plain[33]
        assert plain[:33] == time['readable_candidate']['raw'][:33]
        assert plain[34:] == time['readable_candidate']['raw'][34:]
        assert encrypt(plain, key['column_rank_order'], square) == time['readable_candidate']['ciphertext']
        counts[digit] = counts.get(digit,0)+1
        witnesses.setdefault(digit, {'full_square':square, 'plaintext':plain,
                                    'roundtrip_ciphertext':time['readable_candidate']['ciphertext'],
                                    'historical_digit_claim':False})
    assert counts == {d:24 for d in '56789'}
    return {'schema':'adfgvx-nov10-companions-certificate-v1', 'project':inputs['project'],
            'authors':inputs['authors'], 'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All indices are zero-based.',
            'summary':{'physical_records':4, 'printed_source_slots':820,
                       'valid_source_coordinates':820, 'modeled_coordinates':820,
                       'plaintext_positions':410, 'baseline_fixed_positions':408,
                       'candidate_fixed_positions':409, 'known_coordinate_substitutions':10,
                       'source_or_model_erasure_fills':0, 'source_deletions':0,
                       'published_key_changed':False},
            'records':records, 'complete_raw_label_inventory':inventory,
            'unassigned_time_cell':{'record':'p175_A2', 'position':unknown,
                                    'all_full_square_completions_tested':120,
                                    'number_of_distinct_literal_candidate_plaintexts':5,
                                    'completions_per_digit':counts, 'one_witness_per_digit':witnesses,
                                    'interpretation':'All five digit possibilities preserve the exact candidate ciphertext. No timetable, date plausibility or earlier paraphrase selects one.'},
            'message_headers':inputs['message_headers'],
            'context_records_excluded_from_new_counts':inputs['context_records_excluded_from_new_counts'],
            'prior_attribution_check':inputs['prior_attribution_check'],
            'limits':inputs['literal_limits']}


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
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify, **result['summary'],
                      'time_digit_completions':result['unassigned_time_cell']['completions_per_digit']},indent=2))


if __name__ == '__main__':
    main()
