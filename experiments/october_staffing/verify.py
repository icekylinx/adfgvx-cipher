#!/usr/bin/env python3
"""Rebuild the six exact-frame October source certificates.

ADFGVX Cipher; icekylinx and GPT-6 Astra Pro. The inverse uses independent
column-height offsets and is checked against the package cipher implementation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

COORDINATES = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rebuild(inputs, pdf=None):
    key = inputs['key']
    ranks, square = key['column_rank_order'], key['square']
    assert sorted(square) == sorted(ALPHABET)
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    if pdf:
        import fitz
        assert digest(pdf) == inputs['source']['pdf_sha256']
        document = fitz.open(pdf)
    for image in inputs['source']['images']:
        assert digest(HERE / image['path']) == image['sha256']
        if pdf:
            rendered = document[image['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(image['scale'], image['scale']),
                clip=fitz.Rect(*image['clip_points']))
            assert hashlib.sha256(rendered.samples).hexdigest() == image['pixel_sha256']
    result = []
    for record in inputs['records']:
        literal = ''.join(''.join(record['rows']).split())
        received = ''.join(c if c in COORDINATES else '?' for c in literal)
        assert literal == record['literal_source']
        assert received == record['analysis_source']
        assert len(received) == record['advertised_length']
        width, length = len(ranks), len(received)
        heights = [length // width + (column < length % width) for column in range(width)]
        bases = [sum(heights[c] for c in range(width) if ranks[c] < ranks[column])
                 for column in range(width)]
        offsets = [bases[index % width] + index // width for index in range(length)]
        assert sorted(offsets) == list(range(length))
        stream = ''.join(received[index] for index in offsets)
        assert stream == untranspose(received, ranks)
        domains, origins = [], []
        for i in range(0, length, 2):
            a, b = stream[i:i + 2]
            rows = range(6) if a == '?' else [COORDINATES.index(a)]
            columns = range(6) if b == '?' else [COORDINATES.index(b)]
            domains.append(''.join(sorted(square[6 * row + column] for row in rows for column in columns)))
            origins.append(offsets[i:i + 2])
        assert domains == plaintext_domains(received, ranks, square)
        raw = ''.join(d if len(d) == 1 else '?' for d in domains)
        assert raw == record['expected_raw'] == decrypt(received, ranks, square)
        proposal = record['editorial_template']
        assert len(proposal) * 2 == length and set(proposal) <= set(ALPHABET)
        witness = encrypt(proposal, ranks, square)
        edits, fills = [], []
        for position, proposed in enumerate(proposal):
            for source_index in origins[position]:
                before, after = received[source_index], witness[source_index]
                item = {'source_index': source_index, 'printed_group_1based': source_index // 5 + 1,
                        'group_position_1based': source_index % 5 + 1,
                        'plaintext_index': position, 'before': before, 'after': after,
                        'proposed_plaintext_symbol': proposed}
                if before == '?':
                    fills.append(item)
                elif before != after:
                    edits.append(item)
        edits.sort(key=lambda r: r['source_index'])
        fills.sort(key=lambda r: r['source_index'])
        repaired = list(received)
        for change in edits + fills:
            assert repaired[change['source_index']] == change['before']
            repaired[change['source_index']] = change['after']
        assert ''.join(repaired) == witness
        assert decrypt(witness, ranks, square) == proposal
        result.append({'id': record['id'], 'source_slots': length,
                       'valid_received_coordinates': length - received.count('?'),
                       'plaintext_positions': len(domains), 'raw_plaintext': raw,
                       'raw_fixed_positions': sum(len(d) == 1 for d in domains),
                       'proposed_positions_directly_supported': sum(d == c for d, c in zip(domains, proposal)),
                       'domains': domains, 'coordinate_origins': origins,
                       'editorial_plaintext': proposal, 'known_coordinate_substitutions': edits,
                       'erasure_fills': fills, 'reencrypted_witness': witness,
                       'cost': {'substitutions': len(edits), 'fills': len(fills)},
                       'exact_roundtrip': True})
    expected_costs = {'p66_A': (0, 0), 'p66_B': (2, 0), 'p66_C1': (1, 0),
                      'p67_A2': (1, 0), 'p67_B': (0, 2), 'p67_C': (0, 0)}
    for record in result:
        assert (record['cost']['substitutions'], record['cost']['fills']) == expected_costs[record['id']]
    by_id = {r['id']: r for r in result}
    assert by_id['p67_B']['domains'][75] == '0BDFXZ'
    assert by_id['p67_B']['domains'][86] == '3CIRUW'
    return {'schema': 'adfgvx-october-staffing-certificate-v1',
            'prepared_by': inputs['prepared_by'], 'inputs_sha256': digest(HERE / 'inputs.json'),
            'records': result, 'totals': {
                'records': len(result), 'source_slots': sum(r['source_slots'] for r in result),
                'plaintext_positions': sum(r['plaintext_positions'] for r in result),
                'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in result),
                'proposed_positions_directly_supported': sum(r['proposed_positions_directly_supported'] for r in result),
                'known_coordinate_substitutions': sum(r['cost']['substitutions'] for r in result),
                'erasure_fills': sum(r['cost']['fills'] for r in result)}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / 'inputs.json').read_text())
    result = rebuild(inputs, args.pdf)
    if args.verify:
        assert json.loads((HERE / 'certificates.json').read_text()) == result
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['totals']))


if __name__ == '__main__':
    main()
