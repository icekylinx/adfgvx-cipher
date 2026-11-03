#!/usr/bin/env python3
"""Verify the two p95 Dunst-assignment records and the explicit prefix-dash model.

Prepared by icekylinx and GPT-6 Astra Pro. Standard library by default;
optional exact source-pixel verification requires PyMuPDF.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(source, key, mapping=None):
    order = sorted(range(len(source)), key=lambda i: (key['column_rank_order'][i % len(key['column_rank_order'])], i // len(key['column_rank_order'])))
    mid, origins = [''] * len(source), [None] * len(source)
    if mapping is None:
        mapping = list(range(len(source)))
    for j, i in enumerate(order):
        mid[i], origins[i] = source[j], mapping[j]
    positions = []
    for i in range(0, len(source) - 1, 2):
        pair = ''.join(mid[i:i + 2])
        domain = ''.join(key['square'][6 * row + col] for row in range(6) for col in range(6)
                         if (pair[0] not in CO or pair[0] == CO[row])
                         and (pair[1] not in CO or pair[1] == CO[col]))
        positions.append({'plaintext_index': i // 2, 'pair': pair, 'domain': domain,
                          'label': domain if len(domain) == 1 else '?',
                          'literal_source_indices': origins[i:i + 2]})
    trailing = {'symbol': mid[-1], 'literal_source_index': origins[-1]} if len(source) % 2 else None
    return ''.join(x['label'] for x in positions), positions, trailing


def encrypt(text, key):
    square, ranks = key['square'], key['column_rank_order']
    mid = ''.join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)
    return ''.join(mid[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def locations(rows):
    result, group_number = [], 0
    for row_number, row in enumerate(rows, 1):
        for group_in_row, group in enumerate(row.split(), 1):
            group_number += 1
            for j in range(len(group)):
                result.append({'row_1based': row_number, 'printed_group_in_row_1based': group_in_row,
                               'printed_group_1based': group_number, 'character_in_printed_group_1based': j + 1})
    return result


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    key = inp['key']
    assert key['id'] == 'Nov1-3'
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
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(matrix=fitz.Matrix(im['scale'], im['scale']), clip=fitz.Rect(im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    records, numeral_word_repairs = [], []
    for r in inp['records']:
        literal = ''.join(''.join(r['rows']).split())
        assert literal == r['literal_source'] and set(literal) <= set(CO + '-')
        excluded = r['excluded_source_indices']
        mapping = [i for i in range(len(literal)) if i not in excluded]
        assert mapping == r['working_source_indices']
        working = ''.join(literal[i] for i in mapping)
        assert len(working) == r['advertised_length'] and set(working) <= set(CO)
        if r['id'] == 'p95_A1':
            assert literal.startswith('-DGDGX') and excluded == [0]
            assert len(literal) == 283 and len(working) == 282
        else:
            assert r['id'] == 'p95_A2' and not excluded and len(literal) == 464
        raw, positions, trailing = decode(working, key, mapping)
        assert trailing is None and raw == r['expected_raw']
        assert encrypt(raw, key) == working
        composite_raw, composite_positions, composite_trailing = decode(literal, key)
        assert composite_raw == r['expected_literal_raw_paired_prefix']
        target = r['editorial_text']
        repaired = encrypt(target, key)
        assert len(repaired) == len(working) and decode(repaired, key)[0] == target
        loc, changes = locations(r['rows']), []
        for j, (before, after) in enumerate(zip(working, repaired)):
            if before == after:
                continue
            source_index = mapping[j]
            p = next(p for p in positions if source_index in p['literal_source_indices'])
            changes.append({'working_source_index': j, 'literal_source_index': source_index,
                            **loc[source_index], 'before': before, 'after': after,
                            'plaintext_index': p['plaintext_index'], 'raw_label': p['label'],
                            'proposed_label': target[p['plaintext_index']]})
        assert [[c['working_source_index'], c['before'], c['after']] for c in changes] == r['expected_changes']
        digits = []
        for i, c in enumerate(raw):
            if c.isdigit():
                digits.append({'plaintext_index': i, 'raw_label': c, 'edited_label': target[i], 'unchanged': c == target[i]})
                if target[i] != c:
                    numeral_word_repairs.append([r['id'], i, c, target[i]])
        for field in r['preserved_literal_fields']:
            assert field in raw and field in target
        records.append({'id': r['id'], 'literal_source_slots': len(literal),
                        'valid_source_coordinates': sum(x in CO for x in literal),
                        'working_frame_slots': len(working), 'raw_plaintext': raw,
                        'raw_fixed_positions': len(raw), 'plaintext_positions': len(raw), 'positions': positions,
                        'literal_composite_diagnostic': {'paired_prefix': composite_raw,
                                                        'positions': composite_positions,
                                                        'unpaired_coordinate': composite_trailing},
                        'excluded_source_indices': excluded,
                        'excluded_observed_coordinates': sum(literal[i] in CO for i in excluded),
                        'excluded_noncoordinate_marks': sum(literal[i] not in CO for i in excluded),
                        'editorial_plaintext': target, 'known_coordinate_substitutions': changes,
                        'repaired_working_ciphertext': repaired, 'literal_digit_positions': digits,
                        'preserved_literal_fields': r['preserved_literal_fields']})
    assert numeral_word_repairs == [['p95_A1', 37, '1', 'A'], ['p95_A1', 114, '7', 'E']]
    first = inp['records'][0]
    source, wanted = first['literal_source'], encrypt(first['expected_raw'], key)
    placements = []
    for i in range(len(source)):
        kept = source[:i] + source[i + 1:]
        mismatches = [{'working_index': j, 'source_label': a, 'target_label': b}
                      for j, (a, b) in enumerate(zip(kept, wanted)) if a in CO and a != b]
        retained_masks = [{'working_index': j, 'source_glyph': a, 'target_coordinate': b}
                          for j, (a, b) in enumerate(zip(kept, wanted)) if a not in CO]
        placements.append({'excluded_index': i, 'excluded_glyph': source[i],
                           'excluded_observed_coordinates': int(source[i] in CO),
                           'excluded_noncoordinate_marks': int(source[i] not in CO),
                           'retained_noncoordinate_fills': retained_masks,
                           'known_coordinate_mismatches': len(mismatches)})
    zero_mismatch = [p['excluded_index'] for p in placements if p['known_coordinate_mismatches'] == 0]
    assert zero_mismatch == [0, 1]
    assert placements[0]['retained_noncoordinate_fills'] == []
    assert placements[1]['retained_noncoordinate_fills'] == [{'working_index': 0, 'source_glyph': '-', 'target_coordinate': 'D'}]
    assert [len(r['known_coordinate_substitutions']) for r in records] == [3, 1]
    summary = {'physical_records': 2, 'literal_source_slots_including_prefixed_dash': 747,
               'valid_source_coordinates': 746, 'working_frame_slots': 746,
               'plaintext_positions': 373, 'raw_fixed_positions': 373,
               'known_coordinate_substitutions': 4, 'source_erasure_fills': 0,
               'excluded_observed_coordinates': 0, 'excluded_noncoordinate_source_marks': 1,
               'added_coordinates': 0, 'published_key_changes': 0}
    return {'schema': 'adfgvx-dunst-assignment-certificates-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'records': records, 'summary': summary,
            'raw_numeral_labels_repaired_only_inside_words': numeral_word_repairs,
            'prefix_dash_model': inp['prefix_dash_model'],
            'retrospective_single_exclusion_check': {'actual_evaluated_placements': len(placements),
                                                    'fixed_target': 'First-part raw reading before word repairs',
                                                    'zero_known_mismatch_indices': zero_mismatch,
                                                    'placements': placements,
                                                    'scope': 'Fixed-text source consistency only; no historical or unrestricted uniqueness claim.'},
            'limits': inp['limits']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    a = p.parse_args()
    result = build(a.pdf)
    if a.verify:
        assert result == json.loads((HERE / 'certificates.json').read_text())
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': a.verify, 'source_pixels_checked': bool(a.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
