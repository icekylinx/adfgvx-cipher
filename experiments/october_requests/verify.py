#!/usr/bin/env python3
"""Rebuild exact, conditional and partial October source certificates.

Prepared by icekylinx and GPT-6 Astra Pro. The independent inverse retains
source glyphs and their actual printed group positions, including a six-slot
group. A complete arithmetic witness does not assert unassigned plaintext.
"""
import argparse
import hashlib
import itertools
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


def inverse_offsets(length, ranks):
    width = len(ranks)
    heights = [length // width + (c < length % width) for c in range(width)]
    bases = [sum(heights[d] for d in range(width) if ranks[d] < ranks[c])
             for c in range(width)]
    offsets = [bases[i % width] + i // width for i in range(length)]
    assert sorted(offsets) == list(range(length))
    return offsets


def apply_layout(source, model):
    assert model['insertions'] == []
    deleted = set()
    for lo, hi in model['deletions']:
        assert 0 <= lo < hi <= len(source)
        assert not deleted.intersection(range(lo, hi))
        deleted.update(range(lo, hi))
    origins = [i for i in range(len(source)) if i not in deleted]
    return ''.join(source[i] for i in origins), origins


def source_positions(record):
    positions = []
    group_index = 0
    for row_index, row in enumerate(record['rows']):
        for group in row.split():
            group_index += 1
            for character_index, glyph in enumerate(group):
                positions.append({'printed_row_1based': row_index + 1,
                                  'printed_group_1based': group_index,
                                  'group_position_1based': character_index + 1,
                                  'literal_glyph': glyph})
    return positions


def model_certificate(record, model, key, proposal=None):
    source = record['analysis_source']
    ciphertext, origins = apply_layout(source, model)
    assert len(ciphertext) % 2 == 0
    ranks, square = key['column_rank_order'], key['square']
    offsets = inverse_offsets(len(ciphertext), ranks)
    stream = ''.join(ciphertext[i] for i in offsets)
    assert stream == untranspose(ciphertext, ranks)
    domains, pairs = [], []
    for i in range(0, len(stream), 2):
        a, b = stream[i:i + 2]
        rows = range(6) if a == '?' else [COORDINATES.index(a)]
        columns = range(6) if b == '?' else [COORDINATES.index(b)]
        domains.append(''.join(sorted(square[6*r+c] for r in rows for c in columns)))
        pairs.append({'pair': a + b, 'layout_offsets': offsets[i:i + 2],
                      'source_offsets': [origins[j] for j in offsets[i:i + 2]]})
    assert domains == plaintext_domains(ciphertext, ranks, square)
    raw = ''.join(d if len(d) == 1 else '?' for d in domains)
    assert raw == decrypt(ciphertext, ranks, square)
    proposal = record['editorial_template'] if proposal is None else proposal
    assert len(proposal) == len(domains)
    assert set(proposal) <= set(ALPHABET + '?')
    group_positions = source_positions(record)
    witness = list(ciphertext.replace('?', 'A'))
    edits, fills = [], []
    for position, char in enumerate(proposal):
        if char == '?':
            continue
        cell = square.index(char)
        expected = COORDINATES[cell // 6] + COORDINATES[cell % 6]
        for half, after in enumerate(expected):
            offset = offsets[2*position + half]
            before = ciphertext[offset]
            item = {'layout_offset': offset, 'source_index': origins[offset],
                    'plaintext_index': position, 'before': before, 'after': after,
                    'proposed_plaintext_symbol': char,
                    **group_positions[origins[offset]]}
            if before == '?':
                fills.append(item)
            elif before != after:
                edits.append(item)
            witness[offset] = after
    for changes in (edits, fills):
        changes.sort(key=lambda item: item['source_index'])
    witness = ''.join(witness)
    witness_plaintext = decrypt(witness, ranks, square)
    assert encrypt(witness_plaintext, ranks, square) == witness
    assert all(a == '?' or a == b for a, b in zip(proposal, witness_plaintext))
    changed = {item['layout_offset'] for item in edits + fills}
    assert all(a == b or a == '?' or i in changed
               for i, (a, b) in enumerate(zip(ciphertext, witness)))
    return {'id': model['id'], 'layout_length': len(ciphertext),
            'layout_ciphertext': ciphertext, 'layout_source_offsets': origins,
            'raw_plaintext': raw, 'domains': domains, 'coordinate_pairs': pairs,
            'raw_fixed_positions': sum(len(d) == 1 for d in domains),
            'plaintext_positions': len(domains),
            'proposed_plaintext_positions': sum(c != '?' for c in proposal),
            'proposed_positions_directly_supported': sum(d == c for d, c in zip(domains, proposal)),
            'editorial_template': proposal,
            'known_coordinate_substitutions': edits, 'erasure_fills': fills,
            'cost': {'deleted_slots': len(source) - len(ciphertext),
                     'known_substitutions': len(edits), 'erasure_fills': len(fills)},
            'arithmetic_witness_ciphertext': witness,
            'arithmetic_witness_plaintext': witness_plaintext,
            'witness_warning': 'Question-mark plaintext positions are unasserted. '
                               'Otherwise unfilled erased coordinates use arbitrary A only for roundtrip.'}


def all_two_deletion_fits(record, key):
    """Exhaust the stated source-layout family against a fixed editorial text."""
    source = record['analysis_source']
    expected = encrypt(record['editorial_template'], key['column_rank_order'], key['square'])
    assert len(source) == 188 and len(expected) == 186
    best, minima, count = len(expected) + 1, [], 0
    for a, b in itertools.combinations(range(len(source)), 2):
        candidate = source[:a] + source[a + 1:b] + source[b + 1:]
        cost = sum(x != '?' and x != y for x, y in zip(candidate, expected))
        count += 1
        if cost < best:
            best, minima = cost, [[a, b]]
        elif cost == best:
            minima.append([a, b])
    assert count == 17578 and best == 2 and minima == [[79, 187], [80, 187]]
    return {'layouts_tested': count, 'minimum_known_substitutions': best,
            'all_minimum_deletion_indices': minima,
            'scope': 'Exactly two arbitrary source-slot deletions, fixed Oct4-6 key, '
                     'fixed full editorial template; invalid E/R are erasures. '
                     'This conditional fit does not prove historical deletions.'}


def rebuild(inputs, pdf=None):
    key = inputs['key']
    assert sorted(key['square']) == sorted(ALPHABET)
    assert sorted(key['column_rank_order']) == list(range(1, len(key['column_rank_order']) + 1))
    current = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                   if k['id'] == key['id'])
    assert current == key
    if pdf:
        import fitz
        assert digest(pdf) == inputs['source']['pdf_sha256']
        document = fitz.open(pdf)
    for image in inputs['source']['images']:
        assert digest(HERE / image['path']) == image['sha256']
        if pdf:
            pixmap = document[image['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(image['scale'], image['scale']), clip=fitz.Rect(*image['clip_points']))
            assert hashlib.sha256(pixmap.samples).hexdigest() == image['pixel_sha256']
    records = []
    for record in inputs['records']:
        literal = ''.join(''.join(record['rows']).split())
        source = ''.join(c if c in COORDINATES else '?' for c in literal)
        assert literal == record['literal_source'] and source == record['analysis_source']
        assert len(source_positions(record)) == len(source)
        assert decrypt(source, key['column_rank_order'], key['square']) == record['literal_frame_raw']
        models = [model_certificate(record, model, key) for model in record['layout_models']]
        length = models[0]['plaintext_positions']
        union = [''.join(sorted(set().union(*(set(m['domains'][i]) for m in models))))
                 for i in range(length)]
        result = {'id': record['id'], 'reading_status': record['reading_status'],
                  'literal_source_slots': len(source), 'literal_erased_slots': source.count('?'),
                  'advertised_field': record['advertised_field'],
                  'literal_frame_raw': record['literal_frame_raw'], 'models': models,
                  'all_model_union_domains': union,
                  'all_model_common_template': ''.join(d if len(d) == 1 else '?' for d in union),
                  'all_model_common_fixed_positions': sum(len(d) == 1 for d in union)}
        if record['id'] == 'p62_B':
            assert literal[7] == 'E' and literal[84] == 'R'
            assert source[79:81] == 'FF' and source[-1] == 'X'
            assert len({m['layout_ciphertext'] for m in models}) == 1
            result['conditional_two_deletion_fit'] = all_two_deletion_fits(record, key)
        if record['id'] == 'p63_A':
            assert len(' '.join(record['rows']).split()) == 54 and len(source) == 270
            assert record['advertised_field'] == 54
            assert record['editorial_template'][37:58] == '?' * 21
            assert models[0]['raw_plaintext'][37:58] == 'VASCHIWNENMECH8ISCHEN'
            result['unaccepted_full_conjecture'] = model_certificate(
                record, record['layout_models'][0], key, record['unaccepted_full_conjecture'])
            assert result['unaccepted_full_conjecture']['cost']['known_substitutions'] == 28
        if record['id'] in ('p62_A', 'p65_A'):
            assert len(source) == record['advertised_field']
        records.append(result)
    return {'schema': 'adfgvx-october-requests-certificate-v1',
            'prepared_by': inputs['prepared_by'], 'inputs_sha256': digest(HERE / 'inputs.json'),
            'records': records, 'totals': {
                'records': len(records),
                'literal_source_slots': sum(r['literal_source_slots'] for r in records),
                'plaintext_positions_after_declared_layouts': sum(r['models'][0]['plaintext_positions'] for r in records),
                'raw_fixed_positions_after_declared_layouts': sum(r['all_model_common_fixed_positions'] for r in records),
                'proposed_plaintext_positions': sum(r['models'][0]['proposed_plaintext_positions'] for r in records),
                'proposed_positions_directly_supported': sum(r['models'][0]['proposed_positions_directly_supported'] for r in records),
                'known_substitutions_one_model_per_record': sum(r['models'][0]['cost']['known_substitutions'] for r in records),
                'erasure_fills_one_model_per_record': sum(r['models'][0]['cost']['erasure_fills'] for r in records),
                'conditional_deleted_source_slots': 2}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = rebuild(json.loads((HERE / 'inputs.json').read_text()), args.pdf)
    if args.verify:
        assert json.loads((HERE / 'certificates.json').read_text()) == result
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['totals']))
    for record in result['records']:
        print(record['id'], record['models'][0]['cost'])


if __name__ == '__main__':
    main()
