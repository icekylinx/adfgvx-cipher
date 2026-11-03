#!/usr/bin/env python3
"""Verify the seven source-reviewed p207/p208 military return records.

Prepared by icekylinx and GPT-6 Astra Pro. Published keys retain their
separate prior credit. Standard library; optional --pdf requires PyMuPDF.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = 'ADFGVX'
ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation(n, ranks):
    return sorted(range(n), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))


def undo(source, ranks):
    stream, origins = [''] * len(source), [None] * len(source)
    for j, i in enumerate(permutation(len(source), ranks)):
        stream[i], origins[i] = source[j], j
    assert sorted(origins) == list(range(len(source)))
    return ''.join(stream), origins


def transpose(stream, ranks):
    # Independent column-slice direction checks the sorted-index undo.
    return ''.join(stream[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def reading(stream, square):
    unused = set(ABC) - set(square)
    domains = []
    for i in range(0, len(stream) - 1, 2):
        values = set()
        a, b = stream[i:i + 2]
        for x in CO if a == '?' else a:
            for y in CO if b == '?' else b:
                c = square[CO.index(x) * 6 + CO.index(y)]
                values.update(unused if c == '?' else c)
        domains.append(''.join(sorted(values)))
    return {'plaintext': ''.join(d if len(d) == 1 else '?' for d in domains),
            'domains': domains, 'positions': len(domains),
            'fixed_positions': sum(len(d) == 1 for d in domains),
            'unpaired_coordinate': stream[-1] if len(stream) % 2 else None}


def encode(text, square):
    return ''.join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)


def places(rows):
    result, groupnum = [], 0
    for rownum, row in enumerate(rows, 1):
        for inrow, group in enumerate(row.split(), 1):
            groupnum += 1
            result.extend({'row_1based': rownum, 'group_in_row_1based': inrow,
                           'group_1based': groupnum, 'position_in_group_1based': j + 1}
                          for j in range(len(group)))
    return result


def edition(rec, key):
    source = rec['analysis_source']
    removal = rec['geometry'].get('excluded_source_index')
    source_map = [i for i in range(len(source)) if i != removal]
    working = ''.join(source[i] for i in source_map)
    stream, workorig = undo(working, key['column_rank_order'])
    origins = [source_map[j] for j in workorig]
    raw = reading(stream, key['square'])
    assert raw['unpaired_coordinate'] is None
    assert raw['plaintext'] == rec['expected_working_raw']
    text = rec['editorial_text']
    assert len(text) == len(stream) // 2
    changed = list(stream)
    untouched_unknowns = []
    for i, c in enumerate(text):
        if c == '?':
            pair = stream[2 * i:2 * i + 2]
            original_pair = pair
            if '?' in pair:
                supplied = rec['unfilled_field_pair_witnesses'][str(i)]
                pair = supplied['pair']
                assert supplied['source_record'] == 'p208_A2'
                assert supplied['source_coordinate_indices'] == origins[2 * i:2 * i + 2]
                assert all(a == '?' or a == b for a, b in zip(original_pair, pair))
                changed[2 * i:2 * i + 2] = pair
            cell = CO.index(pair[0]) * 6 + CO.index(pair[1])
            assert key['square'][cell] == '?'
            untouched_unknowns.append({'plaintext_index': i, 'original_pair': original_pair, 'pair': pair, 'cell': cell,
                                       'domain': raw['domains'][i], 'source_indices': origins[2 * i:2 * i + 2]})
        else:
            changed[2 * i:2 * i + 2] = encode(c, key['square'])
    complete = transpose(''.join(changed), key['column_rank_order'])
    final = reading(undo(complete, key['column_rank_order'])[0], key['square'])
    assert final['plaintext'] == text and '?' not in complete
    witness = list(source)
    for j, original_index in enumerate(source_map):
        witness[original_index] = complete[j]
    witness = ''.join(witness)
    loc = places(rec['rows'])
    edits = []
    for j, (a, b) in enumerate(zip(source, witness)):
        if a != b:
            i = origins.index(j) // 2
            edits.append({'source_index': j, **loc[j], 'before': a, 'after': b,
                          'literal_glyph': rec['literal_source'][j], 'plaintext_index': i,
                          'raw_label': raw['plaintext'][i], 'proposed_label': text[i]})
    substitutions = [e for e in edits if e['before'] != '?']
    fills = [e for e in edits if e['before'] == '?']
    assert [[e['source_index'], e['before'], e['after']] for e in edits] == rec['expected_changes']
    cost = {'known_coordinate_substitutions': len(substitutions), 'source_erasure_fills': len(fills),
            'excluded_transmitted_coordinates': int(removal is not None)}
    assert cost == rec['expected_cost']
    # One arbitrary global bijective numeral assignment proves a full round trip,
    # without claiming that assignment as the historical key.
    values = iter(sorted(set(ABC) - set(key['square'])))
    full_square = ''.join(next(values) if c == '?' else c for c in key['square'])
    full_text = reading(undo(complete, key['column_rank_order'])[0], full_square)['plaintext']
    assert transpose(encode(full_text, full_square), key['column_rank_order']) == complete
    numeral_ledger = []
    for i, c in enumerate(raw['plaintext']):
        if c.isdigit():
            assert text[i] == c and all(source[j] == witness[j] for j in origins[2 * i:2 * i + 2])
            numeral_ledger.append({'plaintext_index': i, 'label': c, 'source_indices': origins[2 * i:2 * i + 2]})
    for literal in rec['preserved_literal_fields']:
        assert literal in text
    return {'working_slots': len(working), 'raw': raw, 'coordinate_origins': [origins[i:i + 2] for i in range(0, len(origins), 2)],
            'edited': final, 'cost': cost, 'known_coordinate_substitutions': substitutions,
            'source_erasure_fills': fills, 'excluded_transmitted_coordinate': None if removal is None else
            {'source_index': removal, 'coordinate': source[removal], **loc[removal], 'retained_in_full_source_witness': True},
            'complete_working_witness': complete, 'repaired_full_source_witness': witness,
            'literal_known_numerals': numeral_ledger, 'unfilled_square_fields': untouched_unknowns,
            'arbitrary_bijective_roundtrip': {'square': full_square, 'plaintext': full_text, 'historical_claim': False}}


def geometry_prices(rec, key):
    source, text = rec['analysis_source'], rec['editorial_text']
    unknown_pairs = [CO[i // 6] + CO[i % 6] for i, c in enumerate(key['square']) if c == '?']
    allowed = [unknown_pairs if c == '?' else [encode(c, key['square'])] for c in text]
    result = []
    for omitted in range(len(source)):
        stream, _ = undo(source[:omitted] + source[omitted + 1:], key['column_rank_order'])
        cost = sum(min(sum(a != b for a, b in zip(stream[2 * i:2 * i + 2], pair)) for pair in choices)
                   for i, choices in enumerate(allowed))
        result.append({'excluded_source_index': omitted, 'known_coordinate_substitutions_to_retrospective_template': cost})
    assert min(r['known_coordinate_substitutions_to_retrospective_template'] for r in result) == 0
    assert [r['excluded_source_index'] for r in result if r['known_coordinate_substitutions_to_retrospective_template'] == 0] == [220]
    return result


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    key = inp['key']
    assert key['square'] == 'WG?EITNHUB2R??FDZJS???PY?VQL?1OAXMKC'
    assert set(ABC) - set(key['square']) == set('03456789')
    assert len(key['square']) == 36 and sorted(key['column_rank_order']) == list(range(1, 20))
    assert sha(HERE / 'prior_evidence.json') == inp['prior_evidence_sha256']
    doc = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        doc = fitz.open(pdf)
    for im in inp['source']['images']:
        assert sha(HERE / im['path']) == im['sha256']
        if doc is not None:
            fitz.TOOLS.store_shrink(100)
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(matrix=fitz.Matrix(im['scale'], im['scale']), clip=fitz.Rect(*im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    rows = []
    for r in inp['records']:
        literal = ''.join(''.join(r['rows']).split())
        assert literal == r['literal_source'] and literal.replace('-', '?') == r['analysis_source']
        assert set(literal) <= set(CO + '-')
        original, origins = undo(r['analysis_source'], key['column_rank_order'])
        raw = reading(original, key['square'])
        assert raw['plaintext'] == r['expected_unmodified_raw']
        if raw['unpaired_coordinate'] is not None:
            raw['unpaired_source_index'] = origins[-1]
        if r['geometry']['kind'] == 'identity':
            assert len(literal) == r['advertised_length']
            prices = []
        else:
            assert r['id'] == 'p207_A2' and len(literal) == 221 and r['advertised_length'] == 220
            assert r['geometry']['excluded_source_index'] == 220 and literal[-1] == 'X'
            prices = geometry_prices(r, key)
        selected = edition(r, key)
        rows.append({'id': r['id'], 'source_slots': len(literal), 'valid_received_coordinates': sum(c in CO for c in literal),
                     'unmodified_source_reading': raw, 'selected_edition': selected, 'retrospective_geometry_prices': prices})
    by = {r['id']: r for r in inp['records']}
    left, right = by['p207_B']['analysis_source'], by['p208_A2']['analysis_source']
    differences = [{'source_index': i, 'p207_literal': by['p207_B']['literal_source'][i], 'p208_literal': b,
                    'source_erasure': a == '?'} for i, (a, b) in enumerate(zip(left, right)) if a != b]
    assert [(r['source_index'], r['p207_literal'], r['p208_literal']) for r in differences] == [(127, 'G', 'F'), (165, '-', 'A'), (166, '-', 'D'), (167, '-', 'A'), (168, '-', 'G'), (169, '-', 'X')]
    selected = {r['id']: r['selected_edition'] for r in rows}
    assert selected['p207_B']['complete_working_witness'] == right == selected['p208_A2']['complete_working_witness']
    summary = {'physical_records': len(rows), 'source_slots': sum(r['source_slots'] for r in rows),
               'valid_received_coordinates': sum(r['valid_received_coordinates'] for r in rows),
               'working_slots': sum(r['selected_edition']['working_slots'] for r in rows),
               'working_plaintext_positions': sum(r['selected_edition']['raw']['positions'] for r in rows),
               'working_raw_fixed_positions': sum(r['selected_edition']['raw']['fixed_positions'] for r in rows),
               'edited_fixed_positions': sum(r['selected_edition']['edited']['fixed_positions'] for r in rows),
               'known_coordinate_substitutions': sum(r['selected_edition']['cost']['known_coordinate_substitutions'] for r in rows),
               'source_erasure_fills': sum(r['selected_edition']['cost']['source_erasure_fills'] for r in rows),
               'excluded_transmitted_coordinates': 1, 'retrospective_geometry_positions_priced': 221,
               'published_square_cells_changed': 0}
    return {'schema': 'adfgvx-repatriation-orders-certificate-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'summary': summary, 'records': rows,
            'duplicate_ending': {'records': ['p207_B', 'p208_A2'], 'known_coordinate_agreements': 222,
                                 'known_coordinate_disagreements': 1, 'erasures_supplied_by_copy': 5,
                                 'differences': differences, 'distinct_printed_witness_not_proven_independent_transmission': True}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    a = p.parse_args()
    result = build(a.pdf)
    dest = HERE / 'certificates.json'
    if a.verify:
        assert result == json.loads(dest.read_text())
    else:
        dest.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': a.verify, 'source_pixels_checked': bool(a.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
