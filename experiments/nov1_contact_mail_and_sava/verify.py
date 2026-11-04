#!/usr/bin/env python3
"""Independent p99 source-edition certificate and bounded diagnostic replay.
Prepared by icekylinx and GPT-6 Astra Pro. Standard library by default.
"""
import argparse
import array
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def inverse(source, ranks):
    quotient, remainder = divmod(len(source), len(ranks))
    columns, source_columns = {}, {}
    cursor = 0
    for column in sorted(range(len(ranks)), key=ranks.__getitem__):
        length = quotient + (column < remainder)
        columns[column] = source[cursor:cursor + length]
        source_columns[column] = list(range(cursor, cursor + length))
        cursor += length
    mid, origins = [], []
    for row in range(quotient + bool(remainder)):
        for column in range(len(ranks)):
            if row < len(columns[column]):
                mid.append(columns[column][row])
                origins.append(source_columns[column][row])
    assert cursor == len(source) and len(mid) == len(source)
    return ''.join(mid), origins


def from_mid(mid, key):
    return ''.join(key['square'][6 * CO.index(a) + CO.index(b)]
                   if a in CO and b in CO else '?'
                   for a, b in zip(mid[::2], mid[1::2]))


def decode(source, key, origin_map=None):
    mid, origins = inverse(source, key['column_rank_order'])
    if origin_map is None:
        origin_map = list(range(len(source)))
    positions = []
    for j in range(0, len(mid) - 1, 2):
        pair = mid[j:j + 2]
        domain = ''.join(key['square'][6 * row + col]
                         for row in range(6) for col in range(6)
                         if (pair[0] not in CO or pair[0] == CO[row])
                         and (pair[1] not in CO or pair[1] == CO[col]))
        indices = origins[j:j + 2]
        positions.append({'plaintext_index': j // 2, 'pair': pair, 'domain': domain,
                          'label': domain if len(domain) == 1 else '?',
                          'model_coordinate_indices': indices,
                          'source_coordinate_indices': [origin_map[i] for i in indices]})
    suffix = {'symbol': mid[-1], 'model_coordinate_index': origins[-1],
              'source_coordinate_index': origin_map[origins[-1]]} if len(mid) % 2 else None
    return ''.join(p['label'] for p in positions), positions, suffix


def encrypt_constraints(template, key):
    square, ranks = key['square'], key['column_rank_order']
    mid = ''.join('??' if c == '?' else CO[square.index(c) // 6] + CO[square.index(c) % 6]
                  for c in template)
    order = sorted(range(len(mid)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))
    return ''.join(mid[i] for i in order)


def source_locations(rows):
    result = []
    for row, line in enumerate(rows, 1):
        for group, chunk in enumerate(line.split(), 1):
            for character in range(1, len(chunk) + 1):
                result.append({'row_1based': row, 'group_in_row_1based': group,
                               'character_in_group_1based': character})
    return result


def readable_labels(record, template):
    """Remove only explicitly declared bracketed display letters."""
    display = record['readable_german']
    expansions = record.get('readable_expansions', [])
    for item in expansions:
        fragment = item['display']
        supplied = ''.join(re.findall(r'\[([A-Za-z]+)\]', fragment)).upper()
        literal = re.sub(r'\[[A-Za-z]+\]', '', fragment).upper()
        assert supplied == item['supplied_display_letters']
        assert literal == item['literal']
        start = item['plaintext_start']
        assert template[start:start + len(literal)] == literal
        assert display.count(fragment) == 1
        display = display.replace(fragment, literal)
    assert '[' not in display and ']' not in display
    normalized = ''.join(re.findall('[A-Z0-9?]', display.upper()))
    assert normalized == template.replace('X', '')
    return normalized, expansions


def apply_template(source, key, template, origin_map, locations):
    constraints = encrypt_constraints(template, key)
    assert len(constraints) == len(source)
    edited = ''.join(before if after == '?' else after for before, after in zip(source, constraints))
    changes = []
    for i, (before, after) in enumerate(zip(source, edited)):
        if before == after:
            continue
        origin = origin_map[i]
        kind = ('missing_coordinate_fill' if origin is None else
                'known_coordinate_substitution' if before in CO else 'source_mask_fill')
        changes.append({'model_index': i, 'source_index': origin, 'before': before,
                        'after': after, 'kind': kind,
                        'source_location': locations[origin] if origin is not None else None})
    text, positions, suffix = decode(edited, key, origin_map)
    assert suffix is None and text == template
    witness = ''.join(p['domain'][0] for p in positions)
    ciphertext = encrypt_constraints(witness, key)
    assert all(a not in CO or a == b for a, b in zip(edited, ciphertext))
    return {'plaintext': text, 'ciphertext': edited, 'positions': positions,
            'changes': changes, 'costs': {name: sum(c['kind'] == name for c in changes)
                                       for name in ['known_coordinate_substitution', 'source_mask_fill', 'missing_coordinate_fill']},
            'arbitrary_complete_plaintext_witness': witness,
            'arbitrary_witness_ciphertext': ciphertext,
            'witness_limit': 'The arbitrary completion verifies partial-stream consistency; unknown labels are not accepted as plaintext.'}


def score(text, cells):
    values = []
    for j in range(len(text) - 3):
        if '?' not in text[j:j + 4]:
            index = 0
            for c in text[j:j + 4]:
                index = 36 * index + ALPHABET.index(c)
            values.append(cells[str(index)])
    return {'known_quad_mean': sum(values) / len(values) if values else None,
            'known_quad_windows': len(values), 'fixed_positions': len(text) - text.count('?')}


def replay_screen(inp, quad=None):
    archived = read(HERE / 'search/one_coordinate_screen.json')
    sampled = read(HERE / 'search/queried_model_cells.json')
    cells = sampled['values']
    assert sampled['alphabet'] == ALPHABET
    assert sampled['model_sha256'] == archived['model_sha256']
    if quad:
        assert sha(quad) == sampled['model_sha256']
        table = array.array('f')
        table.frombytes(quad.read_bytes())
        if sys.byteorder != 'little':
            table.byteswap()
        assert len(table) == 36 ** 4
        assert all(table[int(i)] == value for i, value in cells.items())
    source = ''.join(c if c in CO else '?' for c in inp['records'][0]['literal_source'])
    assert source == archived['source']
    rows = []
    for mode in ['insert_transmitted', 'delete_transmitted', 'insert_fractionated', 'delete_fractionated']:
        stream = inverse(source, inp['key']['column_rank_order'])[0] if 'fractionated' in mode else source
        for i in range(len(stream) + ('insert' in mode)):
            candidate = stream[:i] + '?' + stream[i:] if 'insert' in mode else stream[:i] + stream[i + 1:]
            mid = candidate if 'fractionated' in mode else inverse(candidate, inp['key']['column_rank_order'])[0]
            text = from_mid(mid, inp['key'])
            rows.append({'model': mode, 'boundary_or_index': i, 'plaintext': text, **score(text, cells)})
    rows.sort(key=lambda r: r['known_quad_mean'] or -100, reverse=True)
    assert len(rows) == archived['completed_configurations'] == 534
    assert rows == archived['records']
    return {'completed_configurations': len(rows),
            'mode_counts': dict(collections.Counter(r['model'] for r in rows)),
            'queried_model_cells': len(cells), 'best': rows[0],
            'limits': 'Known-quad means omit windows containing unknowns; this short, damaged text has only nine known windows at the top result. A retrospective diagnostic, not an independently calibrated ranking guarantee.'}


def build(pdf=None, quad=None):
    inp = read(HERE / 'inputs.json')
    key = inp['key']
    assert key['id'] == 'Nov1-3' and set(key['square']) == set(ALPHABET)
    assert sorted(key['column_rank_order']) == list(range(1, 20))
    for field, path in [('prior_evidence_sha256', 'prior_evidence.json'),
                        ('screen_sha256', 'search/one_coordinate_screen.json'),
                        ('queried_model_cells_sha256', 'search/queried_model_cells.json')]:
        assert sha(HERE / path) == inp[field]
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
    records = []
    for r in inp['records']:
        literal = ''.join(''.join(r['rows']).split())
        assert literal == r['literal_source'] and len(literal) == r['advertised_length']
        assert set(literal) <= set(CO + '-E')
        mapping = r['geometry']['source_origin_map']
        model = ''.join('?' if index is None else literal[index] for index in mapping)
        assert [i for i in mapping if i is not None] == list(range(len(literal)))
        assert [i for i, origin in enumerate(mapping) if origin is None] == r['geometry']['inserted_model_indices']
        if r['id'] == 'p99_A':
            assert len(literal) == 133 and mapping == list(range(133)) + [None]
            assert literal.count('-') == 22 and [i for i, c in enumerate(literal) if c == 'E'] == [38, 40]
        else:
            assert mapping == list(range(len(literal)))
        native_raw, native_positions, native_suffix = decode(literal, key)
        assert native_raw == r['expected_literal_raw_paired_prefix']
        raw, raw_positions, suffix = decode(model, key, mapping)
        assert suffix is None and raw == r['expected_raw']
        loc = source_locations(r['rows'])
        edited = apply_template(model, key, r['editorial_template'], mapping, loc)
        assert [[c['model_index'], c['before'], c['after']] for c in edited['changes']] == r['expected_changes']
        normalized, expansions = readable_labels(r, edited['plaintext'])
        case = HERE.parents[1] / r['case_path']
        quotes = [line[2:].replace('`', '') for line in case.read_text().splitlines() if line.startswith('> ')]
        assert quotes.count(r['readable_german']) == 1, (r['id'], 'Exact readable display missing or duplicated')
        numeral_fields = re.findall('[0-9]+', edited['plaintext'])
        rec = {'id': r['id'], 'literal_slots': len(literal),
               'valid_source_coordinates': sum(c in CO for c in literal),
               'model_slots': len(model), 'plaintext_positions': len(raw),
               'source_origin_map': mapping, 'literal_raw_paired_prefix': native_raw,
               'literal_unpaired_coordinate': native_suffix, 'literal_raw_positions': native_positions,
               'raw_plaintext': raw, 'raw_fixed_positions': len(raw) - raw.count('?'),
               'raw_positions': raw_positions, 'edited': edited,
               'edited_fixed_positions': len(edited['plaintext']) - edited['plaintext'].count('?'),
               'literal_numeral_fields_after_explicit_repairs': numeral_fields,
               'readable_german': r['readable_german'],
               'readable_mapping': {'normalized_display': normalized,
                                    'retained_non_X_labels': len(normalized),
                                    'unknown_positions': [i for i, c in enumerate(normalized) if c == '?'],
                                    'display_only_expansions': expansions,
                                    'method': 'Remove only the explicitly declared bracketed display letters, then uppercase and retain A-Z, digits and question marks. The result must equal every non-X label in the cited stream.'}}
        if r['id'] == 'p99_A':
            assert len(edited['plaintext']) == 67 and '?' not in edited['plaintext']
            assert r['retained_unknowns'] == []
            assert expansions == [{'display': 'zwisc[h]en', 'literal': 'ZWISCEN',
                                   'plaintext_start': 35, 'supplied_display_letters': 'H',
                                   'reason': 'Explicit prose spelling completion only. The cipher candidate retains the seven labels ZWISCEN and contains no extra H at this position.'}]
            prior = r['earlier_partial_edition']
            earlier = apply_template(model, key, prior['editorial_template'], mapping, loc)
            assert [[c['model_index'], c['before'], c['after']] for c in earlier['changes']] == prior['expected_changes']
            assert earlier['costs'] == {'known_coordinate_substitution': 0, 'source_mask_fill': 21, 'missing_coordinate_fill': 1}
            assert [i for i, c in enumerate(earlier['plaintext']) if c == '?'] == prior['retained_unknowns'] == [38, 39, 41]
            prior_normalized, prior_expansions = readable_labels(prior, earlier['plaintext'])
            assert not prior_expansions
            rec['earlier_partial_edition'] = {'inputs_sha256': prior['inputs_sha256'],
                                            'disposition': prior['disposition'],
                                            'readable_german': prior['readable_german'],
                                            'normalized_display': prior_normalized,
                                            'edited': earlier}
            rec['optional_WIEDER_candidate'] = apply_template(model, key, r['full_optional_candidate'], mapping, loc)
            rec['optional_WIEDER_candidate']['disposition'] = r['full_optional_candidate_disposition']
            assert edited['costs'] == {'known_coordinate_substitution': 0, 'source_mask_fill': 24, 'missing_coordinate_fill': 1}
            assert rec['optional_WIEDER_candidate']['costs'] == {'known_coordinate_substitution': 3, 'source_mask_fill': 24, 'missing_coordinate_fill': 1}
            assert raw[35:42] == '?WI??E?'
            assert earlier['plaintext'][35:42] == 'XWI??E?'
            assert edited['plaintext'][35:42] == 'ZWISCEN'
            assert all(literal[i] not in CO or literal[i] == edited['ciphertext'][i]
                       for i in range(len(literal)))
            revised = []
            for i, (before, after) in enumerate(zip(earlier['ciphertext'], edited['ciphertext'])):
                if before != after:
                    assert mapping[i] is not None and literal[mapping[i]] not in CO
                    revised.append({'source_index': mapping[i], 'printed': literal[mapping[i]],
                                    'earlier_completion': before, 'current_completion': after,
                                    'source_location': loc[mapping[i]]})
            assert [(x['source_index'], x['earlier_completion'], x['current_completion']) for x in revised] == [
                (10, 'X', 'F'), (18, '-', 'D'), (26, '-', 'D'), (40, 'E', 'G')]
            local_positions = []
            local_completions = 1
            for i in range(35, 42):
                raw_position = raw_positions[i]
                local_completions *= len(raw_position['domain'])
                local_positions.append({'plaintext_index': i, 'raw': raw_position,
                                        'earlier_label': earlier['plaintext'][i],
                                        'current_label': edited['plaintext'][i],
                                        'completed_pair': edited['positions'][i]['pair']})
            assert local_completions == 1296
            rec['conditional_between_phrase'] = {
                'plaintext_span_half_open': [35, 42], 'raw_span': raw[35:42],
                'earlier_span': earlier['plaintext'][35:42],
                'current_literal_span': edited['plaintext'][35:42],
                'positions': local_positions, 'mask_completion_changes_from_earlier_edition': revised,
                'compatible_local_completions_before_language_choice': local_completions,
                'all_valid_source_coordinates_retained_unchanged': sum(c in CO for c in literal),
                'note': r['conditional_phrase_note'],
                'limits': 'The earlier X separator was a mask completion, not an observation. ZWISCEN is one contextual completion of four half-observed positions. The bracketed display h is not encrypted; no independently matching phrase or unique historical wording is asserted.'}
            constraints = encrypt_constraints(r['editorial_template'], key)
            layouts = []
            for i in range(len(literal) + 1):
                candidate = literal[:i] + '?' + literal[i:]
                mismatch = [j for j, (a, b) in enumerate(zip(candidate, constraints)) if a in CO and b in CO and a != b]
                layouts.append({'insertion_boundary': i, 'observed_mismatch_count': len(mismatch)})
            minimum = min(x['observed_mismatch_count'] for x in layouts)
            minima = [x['insertion_boundary'] for x in layouts if x['observed_mismatch_count'] == minimum]
            assert minimum == 0 and minima == [132, 133]
            witnesses = []
            for boundary in minima:
                candidate = literal[:boundary] + '?' + literal[boundary:]
                origin = list(range(boundary)) + [None] + list(range(boundary, len(literal)))
                witness = apply_template(candidate, key, r['editorial_template'], origin, loc)
                assert witness['ciphertext'] == edited['ciphertext']
                witnesses.append({'insertion_boundary': boundary, 'source_origin_map': origin,
                                  'raw_plaintext': decode(candidate, key, origin)[0],
                                  'costs': witness['costs'], 'ciphertext': witness['ciphertext'],
                                  'changes': witness['changes']})
            rec['fixed_template_geometry'] = {'completed_configurations': len(layouts),
                                             'minimum_observed_substitutions': minimum,
                                             'minimum_boundaries': minima, 'all_layout_costs': layouts,
                                             'witnesses': witnesses,
                                             'limits': 'The target was assembled after the diagnostic. Equal minima differ in source origins but give the same edited stream; neither identifies where a historical coordinate was lost.'}
        records.append(rec)
    summary = {'physical_records': len(records),
               'source_slots': sum(r['literal_slots'] for r in records),
               'valid_source_coordinates': sum(r['valid_source_coordinates'] for r in records),
               'model_slots': sum(r['model_slots'] for r in records),
               'plaintext_positions': sum(r['plaintext_positions'] for r in records),
               'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in records),
               'edited_fixed_positions': sum(r['edited_fixed_positions'] for r in records),
               'known_coordinate_substitutions': sum(r['edited']['costs']['known_coordinate_substitution'] for r in records),
               'source_mask_fills': sum(r['edited']['costs']['source_mask_fill'] for r in records),
               'missing_coordinate_fills': sum(r['edited']['costs']['missing_coordinate_fill'] for r in records),
               'source_coordinate_exclusions': 0,
               'inserted_model_coordinates': 1}
    return {'schema': 'adfgvx-nov1-contact-mail-sava-certificate-v1',
            'authors': inp['authors'], 'inputs_sha256': sha(HERE / 'inputs.json'),
            'summary': summary, 'records': records,
            'bounded_A_diagnostic': replay_screen(inp, quad),
            'limits': inp['limits']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--pdf', type=Path)
    ap.add_argument('--quad', type=Path)
    args = ap.parse_args()
    assert args.verify != args.write, 'Choose --verify or --write.'
    result = build(args.pdf, args.quad)
    destination = HERE / 'certificates.json'
    if args.write:
        destination.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == read(destination), 'Certificate differs from independently recomputed result.'
    print(json.dumps({'verified': args.verify, 'written': args.write, 'summary': result['summary'],
                      'A_diagnostic_configurations': result['bounded_A_diagnostic']['completed_configurations'],
                      'A_fixed_template_configurations': result['records'][0]['fixed_template_geometry']['completed_configurations'],
                      'source_images': len(read(HERE / 'inputs.json')['source']['images']),
                      'source_pixels_verified': bool(args.pdf), 'full_quad_binding_verified': bool(args.quad)}, indent=2))


if __name__ == '__main__':
    main()
