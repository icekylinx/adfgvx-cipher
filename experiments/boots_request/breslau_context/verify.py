#!/usr/bin/env python3
"""Verify a separate, historically motivated one-coordinate boots emendation.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The baseline source edition and its published key remain hash-pinned.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt, decrypt
from experiments.withdrawal_recovery.verify import reading


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(pdf=None):
    baseline = HERE.parent / 'certificate.json'
    assert sha(baseline) == 'd3d0a372c986cb567b9f8830675753043d2477fe93d56e67ece2c59ab713c569'
    data = json.loads(baseline.read_text())
    inputs = json.loads((HERE.parent / 'inputs.json').read_text())
    source = json.loads((HERE / 'source.json').read_text())
    for crop in source['crops']:
        assert sha(HERE / crop['path']) == crop['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf) == source['pdf_sha256']
        doc = fitz.open(pdf)
        for crop in source['crops']:
            pix = doc[crop['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(crop['scale'], crop['scale']),
                clip=fitz.Rect(crop['clip_points']))
            image = Image.open(HERE / crop['path']).convert('RGB')
            assert image.size == (pix.width, pix.height)
            assert image.tobytes() == pix.samples
    key = inputs['key']
    square, ranks = key['square'], key['column_rank_order']
    first, second = data['records']
    raw = first['untouched_literal_reading']
    before = first['edition']['reading']
    pair = before['source_position_pairs_0based'][14]
    assert pair == [27, 162]
    assert ''.join(first['literal_source'][p] for p in pair) == 'GD'
    assert raw['domains'][14] == before['domains'][14] == '234789QY'
    coordinates = 'ADFGVX'
    cell = lambda pair: coordinates.index(pair[0]) * 6 + coordinates.index(pair[1])
    assert square[cell('GD')] == '?' and square[cell('GG')] == '6'
    assert square.count('6') == 1
    corrected = list(first['edition']['ciphertext'])
    assert corrected[162] == 'D'
    corrected[162] = 'G'
    corrected = ''.join(corrected)
    after = reading(corrected, ranks, square)
    assert after['plaintext'][14] == '6'
    assert [(i, a, b) for i, (a, b) in enumerate(zip(before['plaintext'], after['plaintext']))
            if a != b] == [(14, '?', '6')]
    assert after['fixed_positions'] == before['fixed_positions'] + 1 == 105
    witnesses = []
    for witness in data['part2_all_domain_values_have_joint_global_witnesses']:
        full_square = witness['full_square_witness']
        plain = decrypt(corrected, ranks, full_square)
        assert plain[14] == '6' and encrypt(plain, ranks, full_square) == corrected
        assert all(c in domain for c, domain in zip(plain, after['domains']))
        witnesses.append({'connective_symbol': witness['connective_symbol'],
                          'full_square_witness': full_square,
                          'part1_plaintext_witness': plain,
                          'is_selected_reading': False})
    return {'schema': 'adfgvx-breslau-optional-emendation-v1',
            'prepared_by': 'icekylinx and GPT-6 Astra Pro',
            'baseline_certificate_sha256': sha(baseline),
            'historical_source_sha256': sha(HERE / 'source.json'),
            'assumption': 'The addressed deputy general command at Breslau is the VI Army Corps command independently attested in July1917, and its unit field has one copied coordinate wrong.',
            'plaintext_position_0based': 14, 'original_source_pair_0based': pair,
            'received_pair': 'GD', 'received_domain': before['domains'][14],
            'optional_pair': 'GG', 'optional_reading': '6',
            'additional_observed_coordinate_change': {'source_position_0based': 162,
                                                     'observed': 'D', 'proposed': 'G'},
            'published_square_changes': 0,
            'not_a_new_key_assignment': True,
            'baseline_primary_edition_fixed_positions': data['summary']['edition_fixed_positions'],
            'optional_edition_fixed_positions': after['fixed_positions'] + second['edition']['reading']['fixed_positions'],
            'total_known_coordinate_substitutions_if_adopted': 5,
            'total_erasure_fills_if_adopted': 12,
            'part1_optional_ciphertext': corrected, 'part1_optional_reading': after,
            'joint_square_witnesses': witnesses,
            'accepted_primary_edition_change': False,
            'limits': ['The source is from July1917, not November1918.',
                       'The unmodified GD cell cannot be assigned 6 under the published injective square because GG already has 6.',
                       'Quantity and connective uncertainty remain; no earlier dependency or baseline certificate is changed.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = run(args.pdf)
    path = HERE / 'certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': args.verify,
                      'baseline_fixed': result['baseline_primary_edition_fixed_positions'],
                      'optional_fixed': result['optional_edition_fixed_positions'],
                      'new_key_assignments': 0, 'additional_source_substitutions': 1}, indent=2))


if __name__ == '__main__':
    main()
