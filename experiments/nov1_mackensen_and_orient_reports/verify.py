#!/usr/bin/env python3
"""Verify eight November1 Mackensen/Orient source editions and copy limits.
Prepared by icekylinx and GPT-6 Astra Pro. Standard library by default;
optional exact PDF-pixel binding requires PyMuPDF.
"""
import argparse, collections, hashlib, itertools, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def inverse(source, ranks):
    q, remainder = divmod(len(source), len(ranks))
    columns, origins, cursor = {}, {}, 0
    for c in sorted(range(len(ranks)), key=ranks.__getitem__):
        n = q + (c < remainder)
        columns[c] = source[cursor:cursor + n]
        origins[c] = list(range(cursor, cursor + n))
        cursor += n
    mid, locations = [], []
    for row in range(q + bool(remainder)):
        for c in range(len(ranks)):
            if row < len(columns[c]):
                mid.append(columns[c][row]); locations.append(origins[c][row])
    return ''.join(mid), locations


def decode(source, key, mapping=None):
    mid, origins = inverse(source, key['column_rank_order'])
    if mapping is None:
        mapping = list(range(len(source)))
    positions = []
    for i in range(0, len(mid) - 1, 2):
        pair = mid[i:i + 2]
        domain = ''.join(key['square'][6 * row + col]
                         for row in range(6) for col in range(6)
                         if (pair[0] not in CO or pair[0] == CO[row])
                         and (pair[1] not in CO or pair[1] == CO[col]))
        indices = origins[i:i + 2]
        positions.append({'plaintext_index': i // 2, 'pair': pair, 'domain': domain,
                          'label': domain if len(domain) == 1 else '?',
                          'model_indices': indices, 'source_indices': [mapping[j] for j in indices]})
    suffix = {'symbol': mid[-1], 'model_index': origins[-1], 'source_index': mapping[origins[-1]]} if len(mid) % 2 else None
    return ''.join(p['label'] for p in positions), positions, suffix


def encrypt(template, key):
    sq, ranks = key['square'], key['column_rank_order']
    mid = ''.join('??' if c == '?' else CO[sq.index(c) // 6] + CO[sq.index(c) % 6] for c in template)
    order = sorted(range(len(mid)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))
    return ''.join(mid[i] for i in order)


def row_locations(rows):
    result = []
    for row, line in enumerate(rows, 1):
        for group, chunk in enumerate(line.split(), 1):
            for pos in range(len(chunk)):
                result.append({'row_1based': row, 'group_1based': group, 'character_1based': pos + 1})
    return result


def apply_template(source, template, key, mapping, locations):
    stencil = encrypt(template, key)
    assert len(stencil) == len(source)
    edited = ''.join(a if b == '?' else b for a, b in zip(source, stencil))
    changes = []
    for j, (a, b) in enumerate(zip(source, edited)):
        if a == b:
            continue
        origin = mapping[j]
        kind = 'missing_coordinate_fill' if origin is None else 'observed_coordinate_substitution' if a in CO else 'source_mask_fill'
        changes.append({'model_index': j, 'source_index': origin, 'source_glyph': a, 'after': b, 'kind': kind,
                        'location': locations[origin] if origin is not None else None})
    plaintext, positions, suffix = decode(edited, key, mapping)
    assert suffix is None and plaintext == template
    complete = ''.join(p['domain'][0] for p in positions)
    witness = encrypt(complete, key)
    assert all(a not in CO or a == b for a, b in zip(edited, witness))
    return {'plaintext': plaintext, 'ciphertext': edited, 'positions': positions,
            'changes': changes,
            'cost': {name: sum(c['kind'] == name for c in changes) for name in ['observed_coordinate_substitution', 'source_mask_fill', 'missing_coordinate_fill']},
            'arbitrary_complete_plaintext': complete, 'arbitrary_completion_ciphertext': witness,
            'witness_limit': 'A full re-encryption witness for any retained unknowns; its arbitrarily chosen labels are not accepted plaintext.'}


def copy_audit(pair, source_records, results, key):
    ra, rb = [source_records[x] for x in pair['records']]
    a, b = [''.join(r['literal_source'][i] for i in r['source_origin_map']) for r in [ra, rb]]
    assert len(a) == len(b)
    conflicts = [i for i, (x, y) in enumerate(zip(a, b)) if x in CO and y in CO and x != y]
    masks = [i for i, (x, y) in enumerate(zip(a, b)) if (x in CO) != (y in CO)]
    assert conflicts == pair['observed_conflict_indices']
    assert masks == pair['source_mask_model_indices_supported_by_companion']
    assert all(x in CO or y in CO for x, y in zip(a, b))
    base = [x if x in CO else y for x, y in zip(a, b)]
    witnesses = []
    for values in itertools.product(*[(a[i], b[i]) for i in conflicts]):
        cipher = base.copy()
        for i, c in zip(conflicts, values):
            cipher[i] = c
        cipher = ''.join(cipher)
        text = decode(cipher, key)[0]
        assert encrypt(text, key) == cipher
        costs = [sum(x in CO and x != y for x, y in zip(source, cipher)) for source in [a, b]]
        assert sum(costs) == len(conflicts)
        witnesses.append({'conflict_values': dict(zip(map(str, conflicts), values)), 'ciphertext': cipher,
                          'plaintext': text, 'observed_substitutions_by_record': dict(zip(pair['records'], costs))})
    chosen = encrypt(ra['editorial_template'], key)
    assert ra['editorial_template'] == rb['editorial_template'] and '?' not in chosen
    selected_costs = [sum(x in CO and x != y for x, y in zip(source, chosen)) for source in [a, b]]
    excess = [{'common_index': i, 'copy_values': [a[i], b[i]], 'chosen': chosen[i],
               'aggregate_substitution_cost': int(a[i] in CO and a[i] != chosen[i]) + int(b[i] in CO and b[i] != chosen[i])}
              for i in range(len(a)) if a[i] == b[i] and a[i] in CO and chosen[i] != a[i]]
    assert len(witnesses) == 2 ** len(conflicts)
    return {'id': pair['id'], 'records': pair['records'], 'model_slots': len(a),
            'identical_observed_positions': sum(x in CO and x == y for x, y in zip(a, b)),
            'observed_conflicts': [{'common_index': i, 'source_indices': [ra['source_origin_map'][i], rb['source_origin_map'][i]], 'values': [a[i], b[i]]} for i in conflicts],
            'complementary_source_masks': [{'common_index': i, 'source_indices': [ra['source_origin_map'][i], rb['source_origin_map'][i]], 'values': [a[i], b[i]], 'supported_coordinate': base[i]} for i in masks],
            'minimum_aggregate_observed_substitutions': len(conflicts),
            'minimum_common_witness_count': len(witnesses), 'all_minimum_common_witnesses': witnesses,
            'selected_aggregate_observed_substitutions': sum(selected_costs),
            'selected_observed_substitutions_by_record': dict(zip(pair['records'], selected_costs)),
            'selected_changes_at_shared_observed_positions': excess,
            'selected_is_minimum_common_witness': any(w['ciphertext'] == chosen for w in witnesses),
            'limit': 'These counts condition on the declared aligned frames. Source masks and geometry exclusions are priced separately. Equal joint edit cost does not identify historical plaintext or independent transmission lineage.'}


def d2_geometry(record, key):
    source, target = record['literal_source'], encrypt(record['editorial_template'], key)
    rows = []
    for start in range(len(source) - 5 + 1):
        kept = [i for i in range(len(source)) if not start <= i < start + 5]
        candidate = ''.join(source[i] for i in kept)
        substitutions = sum(a in CO and a != b for a, b in zip(candidate, target))
        exclusions = sum(c in CO for c in source[start:start + 5])
        rows.append({'start': start, 'observed_substitutions': substitutions,
                     'observed_exclusions': exclusions, 'source_mask_exclusions': 5 - exclusions,
                     'combined_observed_operations': substitutions + exclusions})
    minimum = min(r['observed_substitutions'] for r in rows)
    starts = [r['start'] for r in rows if r['observed_substitutions'] == minimum]
    assert len(rows) == 133 and minimum == 1 and starts == [8, 9, 10, 11, 12]
    loc = row_locations(record['rows']); witnesses = []
    for start in starts:
        mapping = [i for i in range(len(source)) if not start <= i < start + 5]
        model = ''.join(source[i] for i in mapping)
        edition = apply_template(model, record['editorial_template'], key, mapping, loc)
        witnesses.append({'start': start, 'excluded_source_indices': list(range(start, start + 5)),
                          'excluded_observed_glyphs': source[start:start + 5], 'source_origin_map': mapping,
                          'raw': decode(model, key, mapping)[0], 'edited_ciphertext': edition['ciphertext'], 'cost': edition['cost']})
    assert len({r['raw'] for r in witnesses}) == len({r['edited_ciphertext'] for r in witnesses}) == 1
    # Alternate optical interpretation: omit the unreadable fifth-slot remnant,
    # then represent its needed coordinate as a missing model slot instead.
    alternate_literal = source[:119] + source[120:]
    alternate_origin = [i for i in range(len(source)) if i != 119 and i not in range(10, 15)]
    alternate_origin.insert(114, None)
    alternate_model = ''.join('?' if i is None else source[i] for i in alternate_origin)
    alternate = apply_template(alternate_model, record['editorial_template'], key, alternate_origin, loc)
    assert alternate['cost'] == {'observed_coordinate_substitution': 1, 'source_mask_fill': 1, 'missing_coordinate_fill': 1}
    assert alternate['ciphertext'] == witnesses[0]['edited_ciphertext']
    combined = min(r['combined_observed_operations'] for r in rows)
    return {'completed_contiguous_five_exclusions': len(rows), 'all_costs': rows,
            'minimum_observed_substitutions': minimum, 'minimum_starts': starts,
            'minimum_combined_observed_operations': combined,
            'minimum_combined_starts': [r['start'] for r in rows if r['combined_observed_operations'] == combined],
            'all_minimum_origin_witnesses': witnesses,
            'alternate_136_slot_optical_interpretation': {'literal_source': alternate_literal, 'literal_slots': len(alternate_literal),
                'native_raw_paired_prefix': decode(alternate_literal, key)[0],
                'model_source_origin_map': alternate_origin, 'conditional_edition': alternate,
                'observed_exclusions': 5, 'omitted_source_slot_interpretation': 119,
                'limit': 'A different reading of the weak source trace, not an additional physical record. It needs one inserted model coordinate rather than a source-mask fill; the final plaintext cannot distinguish the two optical interpretations.'},
            'limit': 'A source-motivated contiguous-group model tested against the selected common text, not an exhaustive search over arbitrary five deletions or possible plaintexts.'}


def build(pdf=None):
    inp = read(HERE / 'inputs.json'); key = inp['key']
    assert key['id'] == 'Nov1-3' and set(key['square']) == set(ALPHABET)
    assert sha(HERE / 'prior_evidence.json') == inp['prior_evidence_sha256']
    doc = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']; doc = fitz.open(pdf)
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
        assert set(literal) <= set(CO + '-LCS?')
        assert ''.join(c if c in CO else '?' for c in literal) == r['analysis_source']
        mapping = r['source_origin_map']
        assert mapping == [i for i in range(len(literal)) if i not in r['excluded_source_indices']]
        assert r['excluded_source_indices'] == (list(range(10, 15)) if r['id'] == 'p101_D2' else [])
        model = ''.join(literal[i] for i in mapping)
        raw, positions, suffix = decode(model, key, mapping)
        assert suffix is None and raw == r['expected_raw']
        native, native_positions, native_suffix = decode(literal, key)
        assert native == r['expected_literal_raw_paired_prefix']
        edition = apply_template(model, r['editorial_template'], key, mapping, row_locations(r['rows']))
        assert [[c['source_index'], c['source_glyph'], c['after']] for c in edition['changes']] == r['expected_changes']
        normalized = ''.join(re.findall('[A-Z0-9?]', r['readable_german'].upper()))
        assert normalized == r['editorial_template'].replace('X', ''), r['id']
        page = (HERE.parents[1] / r['case_path']).read_text()
        section = page.split(r['heading'] + '\n', 1)[1].split('\n## ', 1)[0]
        quote = next(line[2:] for line in section.splitlines() if line.startswith('> '))
        assert quote.replace('`', '') == r['readable_german']
        records.append({'id': r['id'], 'literal_slots': len(literal), 'valid_source_coordinates': sum(c in CO for c in literal),
                        'model_slots': len(model), 'plaintext_positions': len(raw), 'source_origin_map': mapping,
                        'source_coordinate_exclusions': [{'source_index': i, 'glyph': literal[i]} for i in r['excluded_source_indices']],
                        'literal_raw_paired_prefix': native, 'literal_unpaired_coordinate': native_suffix,
                        'raw_plaintext': raw, 'raw_positions': positions, 'raw_fixed_positions': len(raw) - raw.count('?'),
                        'edited': edition, 'edited_fixed_positions': len(r['editorial_template']) - r['editorial_template'].count('?'),
                        'explicit_numeric_or_reference_repairs': [{'plaintext_index': i, 'raw': a, 'edited': b} for i, (a, b) in enumerate(zip(raw, r['editorial_template'])) if a != b and (a.isdigit() or b.isdigit())],
                        'readable_mapping': {'exact_display': quote, 'normalized_non_X_labels': normalized, 'retained_unknowns': normalized.count('?')}})
    source_records = {r['id']: r for r in inp['records']}
    copies = [copy_audit(p, source_records, {r['id']: r for r in records}, key) for p in inp['copy_pairs']]
    assert [p['minimum_common_witness_count'] for p in copies] == [4, 128]
    assert [p['selected_aggregate_observed_substitutions'] for p in copies] == [2, 9]
    summary = {'physical_records': len(records),
               **{field: sum(r[field] for r in records) for field in ['literal_slots', 'valid_source_coordinates', 'model_slots', 'plaintext_positions', 'raw_fixed_positions', 'edited_fixed_positions']},
               **{name: sum(r['edited']['cost'][name] for r in records) for name in ['observed_coordinate_substitution', 'source_mask_fill', 'missing_coordinate_fill']},
               'excluded_observed_coordinates': sum(len(r['source_coordinate_exclusions']) for r in records),
               'inserted_model_coordinates': 0, 'published_key_changes': 0}
    return {'schema': 'adfgvx-nov1-mackensen-orient-certificate-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'summary': summary,
            'records': records, 'copy_audits': copies,
            'D2_conditional_geometry': d2_geometry(source_records['p101_D2'], key), 'limits': inp['limits']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify', action='store_true'); ap.add_argument('--write', action='store_true'); ap.add_argument('--pdf', type=Path)
    args = ap.parse_args(); assert args.verify != args.write, 'Choose --verify or --write.'
    result = build(args.pdf); out = HERE / 'certificates.json'
    if args.write:
        out.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == read(out)
    print(json.dumps({'verified': args.verify, 'summary': result['summary'],
                      'minimum_copy_witnesses': [r['minimum_common_witness_count'] for r in result['copy_audits']],
                      'D2_contiguous_exclusions_evaluated': result['D2_conditional_geometry']['completed_contiguous_five_exclusions'],
                      'source_pixels_checked': bool(args.pdf)}, indent=2))


if __name__ == '__main__':
    main()
