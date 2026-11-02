#!/usr/bin/env python3
"""Build or verify additional source-checked corpus readings.

The local column/coordinate implementation is checked against the project's
separate cipher functions. Readable candidates remain explicit editorial
inputs; all original source coordinates and invalid glyphs are preserved.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

COORDINATES = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def layout(length, ranks):
    return [row_index for column in sorted(range(len(ranks)), key=ranks.__getitem__)
            for row_index in range(column, length, len(ranks))]


def inspect(record, key):
    literal = ''.join(''.join(record['source_rows']).split())
    cipher = ''.join(c if c in COORDINATES else '?' for c in literal)
    assert len(cipher) == record['advertised_length'] and len(cipher) % 2 == 0
    ranks, square = key['column_rank_order'], key['square']
    order = layout(len(cipher), ranks)
    inverse = [None] * len(cipher)
    intermediate = ['?'] * len(cipher)
    for source, target in enumerate(order):
        inverse[target] = source
        intermediate[target] = cipher[source]
    missing = set(ALPHABET) - set(square)
    positions = []
    raw = []
    for position in range(len(cipher) // 2):
        pair = ''.join(intermediate[2 * position:2 * position + 2])
        cells = [6 * row + column for row in range(6) for column in range(6)
                 if pair[0] in ('?', COORDINATES[row])
                 and pair[1] in ('?', COORDINATES[column])]
        domain = set()
        for cell in cells:
            domain.update(missing if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        symbol = domain if len(domain) == 1 else '?'
        raw.append(symbol)
        positions.append({'plaintext_position': position,
                          'source_coordinate_indices': inverse[2 * position:2 * position + 2],
                          'source_pair': pair, 'possible_square_cells': cells,
                          'base_domain': domain, 'base_symbol': symbol})
    raw = ''.join(raw)
    assert raw == record['expected_raw'] == decrypt(cipher, ranks, square)
    assert [row['base_domain'] for row in positions] == plaintext_domains(cipher, ranks, square)
    assert ''.join(intermediate[i] for i in order) == cipher
    result = {'id': record['id'], 'key_id': record['key_id'],
              'literal_source': literal, 'analysis_ciphertext': cipher,
              'source_slots': len(cipher),
              'valid_source_coordinates': sum(c in COORDINATES for c in literal),
              'invalid_source_slots': [{'source_index': i, 'printed': c}
                                       for i, c in enumerate(literal) if c not in COORDINATES],
              'raw_plaintext': raw, 'plaintext_positions': len(raw),
              'base_fixed_positions': sum(len(row['base_domain']) == 1 for row in positions),
              'positions': positions, 'source_coordinates_changed_in_base': 0,
              'editorial_candidate': None}
    candidate = record['candidate_plaintext']
    if candidate is not None:
        assert len(candidate) == len(raw) and all(c in square for c in candidate)
        encoded = ''.join(COORDINATES[square.index(c) // 6] + COORDINATES[square.index(c) % 6]
                          for c in candidate)
        target = ''.join(encoded[i] for i in order)
        assert target == encrypt(candidate, ranks, square)
        assert decrypt(target, ranks, square) == candidate
        substitutions = [{'source_index': i, 'source': old, 'proposed': new}
                         for i, (old, new) in enumerate(zip(cipher, target))
                         if old != '?' and old != new]
        fills = [{'source_index': i, 'printed': literal[i], 'proposed': new}
                 for i, (old, new) in enumerate(zip(cipher, target)) if old == '?']
        # Apply exactly the advertised edits to recover the proposed target.
        repaired = list(cipher)
        for edit in substitutions + fills:
            repaired[edit['source_index']] = edit['proposed']
        assert ''.join(repaired) == target
        result['editorial_candidate'] = {
            'plaintext': candidate, 'ciphertext': target,
            'known_coordinate_substitutions': substitutions,
            'source_erasure_fills': fills,
            'source_coordinates_preserved': sum(a == b and a != '?' for a, b in zip(cipher, target)),
            'plaintext_changes': [{'plaintext_position': i, 'base_symbol': a, 'proposed_symbol': b,
                                   'base_domain': positions[i]['base_domain'],
                                   'source_coordinate_indices': positions[i]['source_coordinate_indices']}
                                  for i, (a, b) in enumerate(zip(raw, candidate)) if a != b],
            'length_change': 0, 'key_change': False,
            'reason': record['editorial_reason']}
    return result


def field(record, start, length):
    return {'plaintext_start': start, 'plaintext': record['raw_plaintext'][start:start + length],
            'coordinate_pairs': [p['source_pair'] for p in record['positions'][start:start + length]],
            'source_indices': [p['source_coordinate_indices'] for p in record['positions'][start:start + length]],
            'domains': [p['base_domain'] for p in record['positions'][start:start + length]]}


def build(pdf=None):
    inputs = json.loads((HERE / 'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    keys = {key['id']: key for key in inputs['keys']}
    catalogue = {key['id']: key for key in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    for name, key in keys.items():
        assert key == catalogue[name]
    for image in inputs['source_images']:
        assert sha(HERE / image['path']) == image['sha256']
    if pdf is not None:
        import fitz
        from PIL import Image
        assert sha(pdf) == inputs['source']['pdf_sha256']
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        document = fitz.open(pdf)
        for source in inputs['source_images']:
            page = document[source['pdf_page_1based'] - 1]
            scale = source['render_scale']
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*source['crop_pdf_points']))
            image = Image.open(HERE / source['path']).convert('RGB')
            assert image.size == (pixmap.width, pixmap.height)
            assert image.tobytes() == pixmap.samples
    records = [inspect(row, keys[row['key_id']]) for row in inputs['records']]
    by_id = {row['id']: row for row in records}
    earlier, later = by_id['p203_C'], by_id['p210_C']
    earlier_start = earlier['raw_plaintext'].index('FELDPOSTX') + len('FELDPOSTX')
    later_start = later['raw_plaintext'].index('FELDPOSTX') + len('FELDPOSTX')
    earlier_field = field(earlier, earlier_start, 3)
    later_field = field(later, later_start, 3)
    assert earlier_field['coordinate_pairs'] == ['VA', 'VA', 'VV']
    assert earlier_field['plaintext'] == '???'
    assert later_field['plaintext'] == '227'
    assert all(len(d) == 1 for d in later_field['domains'])
    early_square = keys['Nov16-18']['square']
    assigned_two = early_square.index('2')
    assigned_two_pair = COORDINATES[assigned_two // 6] + COORDINATES[assigned_two % 6]
    assert assigned_two_pair == 'DV' and early_square[24] == '?'
    totals = {'records': len(records),
              'source_slots': sum(r['source_slots'] for r in records),
              'valid_source_coordinates': sum(r['valid_source_coordinates'] for r in records),
              'plaintext_positions': sum(r['plaintext_positions'] for r in records),
              'base_fixed_positions': sum(r['base_fixed_positions'] for r in records),
              'editorial_known_coordinate_substitutions': sum(len(r['editorial_candidate']['known_coordinate_substitutions'])
                                                              for r in records if r['editorial_candidate']),
              'editorial_source_erasure_fills': sum(len(r['editorial_candidate']['source_erasure_fills'])
                                                   for r in records if r['editorial_candidate'])}
    return {'schema': 'adfgvx-additional-source-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': 'All coordinate and plaintext indices are zero-based.',
            'summary': totals, 'records': records,
            'richter_postal_field_comparison': {
                'earlier_p203_C': earlier_field, 'later_p210_C': later_field,
                'already_assigned_digit_two_pair_in_Nov16_18': assigned_two_pair,
                'same_number_would_require': {'VA': '2', 'VV': '7'},
                'same_number_conflicts_with_unchanged_injective_square': True,
                'conclusion': 'Do not transfer 227 into the earlier unknown postal field. The messages are related personnel queries, but identical addresses and correct copies are not established.'},
            'limits': ['Fixed positions are consequences of the stated source and published key; a fixed garbled character is not silently counted as a correct historical reading.',
                       'All readability repairs are same-length editorial candidates, separately costed; the literal source remains unchanged.',
                       'Date-like and reference-like J strings under Nov19-21 remain literal. No global relabelling of a published square is performed.',
                       'The related Richter queries do not justify filling missing digits, and they do not independently refute or prove another conditional inference.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path, help='Optionally prove every saved image pixel against the public source PDF.')
    args = parser.parse_args()
    result = build(args.pdf)
    destination = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(destination.read_text())
    else:
        destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
