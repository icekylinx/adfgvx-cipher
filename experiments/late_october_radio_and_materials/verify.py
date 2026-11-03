#!/usr/bin/env python3
"""Verify the pp74–76 source layers and explicitly priced reading candidates.

Prepared by icekylinx and GPT-6 Astra Pro. The default check uses only the
standard library. Optional source-pixel verification requires PyMuPDF.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COORDINATES = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten(rows):
    return ''.join(''.join(rows).split())


def inverse(source, ranks):
    """Map transmitted sequence to row-major intermediate slots by sorted indices."""
    order = sorted(range(len(source)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))
    middle, origins = [''] * len(source), [None] * len(source)
    for source_index, middle_index in enumerate(order):
        middle[middle_index] = source[source_index]
        origins[middle_index] = source_index
    return ''.join(middle), origins


def encrypt(plaintext, key):
    """Independent forward implementation using strided original columns."""
    square, ranks = key['square'], key['column_rank_order']
    middle = ''.join(COORDINATES[square.index(c) // 6] + COORDINATES[square.index(c) % 6]
                     for c in plaintext)
    return ''.join(middle[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def decode(source, key, source_indices=None):
    middle, origins = inverse(source, key['column_rank_order'])
    assert len(middle) % 2 == 0
    if source_indices is None:
        source_indices = list(range(len(source)))
    positions = []
    for i in range(0, len(middle), 2):
        pair = middle[i:i + 2]
        domain = ''.join(key['square'][6 * row + col] for row in range(6) for col in range(6)
                         if (pair[0] not in COORDINATES or pair[0] == COORDINATES[row])
                         and (pair[1] not in COORDINATES or pair[1] == COORDINATES[col]))
        positions.append({'plaintext_index': i // 2, 'pair': pair, 'domain': domain,
                          'working_source_indices': origins[i:i + 2],
                          'literal_source_indices': [source_indices[j] for j in origins[i:i + 2]],
                          'label': domain if len(domain) == 1 else '?'})
    return ''.join(p['label'] for p in positions), positions


def locations(rows):
    result, group_number = [], 0
    for row_number, row in enumerate(rows, 1):
        for group_in_row, group in enumerate(row.split(), 1):
            group_number += 1
            result.extend({'row_1based': row_number, 'group_in_row_1based': group_in_row,
                           'group_1based': group_number, 'position_in_group_1based': j + 1}
                          for j in range(len(group)))
    return result


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    key = inp['key']
    assert key['id'] == 'Oct28-31'
    assert len(key['square']) == 36 and set(key['square']) == set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    assert sorted(key['column_rank_order']) == list(range(1, len(key['column_rank_order']) + 1))
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
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(im['scale'], im['scale']), clip=fitz.Rect(im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    records = []
    numeral_word_repairs = []
    for record in inp['records']:
        literal = flatten(record['rows'])
        typed = flatten(record['typed_rows'])
        assert literal == record['literal_source']
        assert set(literal) <= set(COORDINATES + '-')
        assert len(typed) == record['advertised_length']
        mapping = record['working_source_indices']
        assert mapping == sorted(set(mapping))
        assert ''.join(literal[j] for j in mapping) == typed
        excluded = [i for i in range(len(literal)) if i not in mapping]
        assert excluded == record['geometry']['excluded_source_indices']
        assert record['geometry']['added_coordinates'] == 0
        if record['id'] == 'p76_A3':
            assert len(literal) == 258 and len(typed) == 238
            assert excluded == list(range(75, 95))
            assert literal[75:95] == literal[95:115] == typed[75:95]
            assert literal[75:95] == record['geometry']['excluded_literal']
            assert literal[12] == '-' and literal.count('-') == 1
            sensitivity = record['handwritten_glyph_sensitivity']
            assert sensitivity['literal_source_index'] == 87 and literal[87] == 'D'
            assert sensitivity['alternative_noncoordinate_glyph'] == 'O'
            alternate_literal = literal[:87] + 'O' + literal[88:]
            assert ''.join(alternate_literal[j] for j in mapping) == typed
            alternative_raw, alternative_positions = decode(alternate_literal, key)
            sensitivity_result = {'review': sensitivity, 'alternative_literal_source': alternate_literal,
                                  'alternative_composite_raw': alternative_raw,
                                  'alternative_composite_positions': alternative_positions,
                                  'typed_reading_unchanged': True}
            cost = record['geometry']['alternative_composite_transmission_model']
            assert cost['excluded_slots'] == 20
            assert cost['excluded_observed_coordinates_if_primary_D'] == sum(literal[j] in COORDINATES for j in excluded) == 20
            assert cost['excluded_observed_coordinates_if_alternative_O_masked'] == sum(alternate_literal[j] in COORDINATES for j in excluded) == 19
        else:
            assert literal == typed and not excluded
            sensitivity_result = None
        raw, positions = decode(typed, key, mapping)
        composite_raw, composite_positions = decode(literal, key)
        assert raw == record['expected_raw']
        assert composite_raw == record['expected_literal_composite_raw']
        target = record['editorial_text']
        ciphertext = encrypt(target, key)
        assert len(ciphertext) == len(typed)
        assert decode(ciphertext, key)[0] == target
        loc = locations(record['rows'])
        changes, substitutions, fills = [], [], []
        for index, (before, after) in enumerate(zip(typed, ciphertext)):
            if before == after:
                continue
            position = next(p for p in positions if index in p['working_source_indices'])
            literal_index = mapping[index]
            item = {'working_source_index': index, 'literal_source_index': literal_index,
                    **loc[literal_index], 'before': before, 'after': after,
                    'kind': 'printed_dash_fill' if before == '-' else 'observed_coordinate_substitution',
                    'plaintext_index': position['plaintext_index'], 'raw_domain': position['domain'],
                    'raw_label': position['label'], 'proposed_label': target[position['plaintext_index']]}
            changes.append(item)
            (fills if before == '-' else substitutions).append(item)
        assert [[c['working_source_index'], c['before'], c['after']] for c in changes] == record['expected_changes']
        assert len(fills) == typed.count('-')
        digit_positions = []
        for i, c in enumerate(raw):
            if c.isdigit():
                digit_positions.append({'plaintext_index': i, 'raw_label': c, 'edited_label': target[i],
                                        'unchanged': c == target[i]})
                if c != target[i]:
                    numeral_word_repairs.append([record['id'], i, c, target[i]])
        for field in record['preserved_literal_fields']:
            assert field in raw and field in target
        records.append({'id': record['id'], 'literal_source_slots_including_annotations': len(literal),
                        'valid_literal_coordinates_including_annotations': sum(c in COORDINATES for c in literal),
                        'typed_source_slots': len(typed),
                        'valid_typed_source_coordinates': sum(c in COORDINATES for c in typed),
                        'handwritten_slots_excluded_from_typed_frame': len(excluded),
                        'source_geometry': record['geometry'],
                        'raw_plaintext': raw, 'raw_fixed_positions': len(raw) - raw.count('?'),
                        'plaintext_positions': len(raw), 'positions': positions,
                        'literal_composite_diagnostic': {'plaintext': composite_raw,
                                                        'positions': composite_positions} if excluded else None,
                        'handwritten_glyph_sensitivity': sensitivity_result,
                        'editorial_plaintext': target, 'editorial_status': record.get('edition_status', 'coordinate_priced_reading'),
                        'coordinate_changes': changes, 'known_coordinate_substitutions': substitutions,
                        'printed_dash_fills': fills, 'repaired_typed_ciphertext': ciphertext,
                        'literal_digit_positions': digit_positions,
                        'preserved_literal_fields': record['preserved_literal_fields']})
    assert numeral_word_repairs == [['p74_C2', 29, '5', 'D'], ['p76_A3', 85, '3', 'D']]
    assert [len(r['known_coordinate_substitutions']) for r in records] == [1, 0, 0, 2, 2, 5, 0, 1]
    assert [len(r['printed_dash_fills']) for r in records] == [0, 0, 30, 0, 0, 0, 0, 1]
    summary = {'physical_records': len(records),
               'literal_source_slots_including_annotations': sum(r['literal_source_slots_including_annotations'] for r in records),
               'typed_source_slots': sum(r['typed_source_slots'] for r in records),
               'valid_typed_source_coordinates': sum(r['valid_typed_source_coordinates'] for r in records),
               'handwritten_slots_excluded_from_typed_frame': sum(r['handwritten_slots_excluded_from_typed_frame'] for r in records),
               'plaintext_positions': sum(r['plaintext_positions'] for r in records),
               'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in records),
               'known_coordinate_substitutions': sum(len(r['known_coordinate_substitutions']) for r in records),
               'printed_dash_fills': sum(len(r['printed_dash_fills']) for r in records),
               'published_key_changes': 0, 'added_working_coordinates': 0}
    assert summary['typed_source_slots'] == 1592 and summary['plaintext_positions'] == 796
    assert summary['raw_fixed_positions'] == 765
    return {'schema': 'adfgvx-late-october-radio-materials-certificate-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'records': records, 'summary': summary,
            'raw_numeral_labels_repaired_only_inside_words': numeral_word_repairs,
            'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    if args.verify:
        assert result == json.loads((HERE / 'certificates.json').read_text())
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': bool(args.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
