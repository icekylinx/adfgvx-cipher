#!/usr/bin/env python3
"""Propagate conditional November Y assignments without changing source keys.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The finite p198 frontier is inherited by exact membership restriction;
--recompute independently recomputes every retained membership as well.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains
from adfgvx.projection import analyze

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
DEPENDENCIES = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(relative):
    path = ROOT / relative
    DEPENDENCIES[relative] = digest(path)
    return json.loads(path.read_text())


def load_module(relative, name):
    path = ROOT / relative
    DEPENDENCIES[relative] = digest(path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inverse_indices(length, ranks):
    """Independent physical-column offset inverse, to source-frame indices."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (col < length % width) for col in range(width)]
    starts, at = [None] * width, 0
    for col in sorted(range(width), key=ranks.__getitem__):
        starts[col] = at
        at += heights[col]
    assert at == length
    return [starts[p % width] + p // width for p in range(length)]


def inspect(cipher, ranks, square):
    assert len(cipher) % 2 == 0 and set(cipher) <= set(C + '?')
    known = square.replace('?', '')
    assert len(square) == 36 and len(set(known)) == len(known)
    unknown = sorted(set(A) - set(known))
    order = inverse_indices(len(cipher), ranks)
    domains, pairs, cells = [], [], []
    for position in range(0, len(cipher), 2):
        left, right = cipher[order[position]], cipher[order[position + 1]]
        candidates = [6 * r + c
                      for r in ([C.index(left)] if left in C else range(6))
                      for c in ([C.index(right)] if right in C else range(6))]
        domain = set()
        for cell in candidates:
            domain.update(unknown if square[cell] == '?' else square[cell])
        domains.append(''.join(sorted(domain)))
        pairs.append(left + right)
        cells.append(candidates)
    assert domains == plaintext_domains(cipher, ranks, square)
    raw = ''.join(d if len(d) == 1 else '?' for d in domains)
    assert raw == decrypt(cipher, ranks, square)
    return {'raw': raw, 'domains': domains, 'pairs': pairs, 'cells': cells,
            'inverse_indices': order}


def assign(square, cell, symbol):
    assert square[cell] == '?' and symbol not in square
    return square[:cell] + symbol + square[cell + 1:]


def frontier_report(recompute):
    historical = read('experiments/p198_category_frontier/results.json')
    reviewed = read('data/reviews/p198_pareto_independent.json')
    inputs = read('experiments/p198_exact_sparse/inputs.json')
    case = next(c for c in inputs['cases'] if c['id'] == 'p198_Nov13-15b')
    assert historical['all_memberships_and_allocations_completed'] is True
    assert reviewed['membership_classes_recomputed'] == 28
    assert historical['global_frontier_counts'] == reviewed['global_frontier']
    independent = load_module('experiments/p198_category_frontier/verify_independent.py',
                              'independent_category_frontier')
    # Counts ignore whether a particular rare-letter cell is Q or Y.
    # Fixing FX=Y keeps precisely the seven classes containing square cell 17.
    selected = [m for m in historical['membership_results'] if 17 in m['QY_cell_indices']]
    unknown = [i for i, c in enumerate(historical['partial_square']) if c == '?']
    assert len(selected) == 7
    assert {tuple(m['QY_cell_indices']) for m in selected} == {
        tuple(sorted((17, cell))) for cell in unknown if cell != 17}
    pool = independent.geometry_pool(case) if recompute else None
    membership_rows, all_witnesses = [], []
    for member in selected:
        square = member['representative_square']
        swap = square[17] == 'Q'
        assert square[17] in 'QY'
        translate = str.maketrans('QY', 'YQ') if swap else {}
        square = square.translate(translate)
        assert square[17] == 'Y'
        assert all(a == '?' or a == b for a, b in zip(historical['partial_square'], square))
        witnesses = []
        for original in member['frontier_witnesses']:
            row = dict(original)
            row['representative_square'] = square
            row['plaintext_witness'] = original['plaintext_witness'].translate(translate)
            independent.check_witness(case, row)
            assert encrypt(row['plaintext_witness'], case['column_rank_order'], square) == row['filled_ciphertext']
            row['QY_cell_indices'] = member['QY_cell_indices']
            row['QY_label_swap_applied'] = swap
            witnesses.append(row)
        counts = [(r['digits'], r['Q_or_Y']) for r in witnesses]
        assert counts == list(independent.undominated(counts))
        if recompute:
            assert list(independent.membership_frontier(pool, square)) == counts
        membership_rows.append({'QY_cell_indices': member['QY_cell_indices'],
                                'square_with_FX_Y': square,
                                'complete_square_extensions_covered': math.factorial(6),
                                'loss_allocations_completed_in_parent': member['search_counts']['allocations_completed'],
                                'frontier': [list(c) for c in counts],
                                'witnesses': witnesses})
        all_witnesses.extend(witnesses)
    counts = independent.undominated((r['digits'], r['Q_or_Y']) for r in all_witnesses)
    expected = ((4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (10, 1), (13, 0))
    assert counts == expected
    witnesses = [next(r for r in all_witnesses if (r['digits'], r['Q_or_Y']) == count)
                 for count in counts]
    return {'key_id': 'Nov13-15b', 'condition': 'FX=Y', 'square_cell_index': 17,
            'partial_square_before': historical['partial_square'],
            'partial_square_after': assign(historical['partial_square'], 17, 'Y'),
            'column_rank_order': case['column_rank_order'],
            'received_coordinates': len(case['observed_ciphertext']),
            'all_received_coordinates_preserved': True,
            'missing_coordinates': case['missing_count'],
            'complete_square_extensions_before': math.factorial(8),
            'complete_square_extensions_after': math.factorial(7),
            'membership_classes_after': 7, 'loss_allocations_per_membership': 15504,
            'loss_position_choices_per_square': math.comb(170, 5),
            'loss_and_fill_witnesses_per_square': math.comb(170, 5) * 6 ** 5,
            'membership_results': membership_rows,
            'global_frontier': [list(c) for c in counts], 'global_witnesses': witnesses,
            'minimum_digits': 4, 'minimum_digits_if_no_Q_or_Y': 13,
            'weaker_condition_with_same_category_frontier': 'FX is either Q or Y; this covers 10,080 square completions.',
            'newly_accepted_historical_plaintext_characters': 0}


def inventory():
    records = []

    def add(record_id, variant, cipher, key, source, mapping=None):
        assert len(cipher) % 2 == 0, (record_id, variant)
        assert set(cipher) <= set(C + '?'), (record_id, variant)
        records.append({'id': record_id, 'variant': variant, 'key_id': key,
                        'ciphertext': cipher, 'dependency': source,
                        'frame_to_source_indices': mapping})

    for source in ('experiments/tiflis_appointment/certificates.json',
                   'experiments/nov14_retransmissions/certificates.json'):
        for record in read(source)['records']:
            cipher = record.get('model_ciphertext', record.get('ciphertext'))
            add(record['id'], 'source model', cipher, record['key_id'], source,
                record['model_to_source_indices'])

    source = 'experiments/warsaw_service_messages/certificates.json'
    for record in read(source)['records']:
        add(record['id'], 'source model', record['model_ciphertext'], record['key_id'], source,
            record['model_to_source_indices'])
        for candidate in record['editorial_candidates']:
            add(record['id'], 'explicit editorial candidate: ' + candidate['id'],
                candidate['ciphertext'], record['key_id'], source,
                record['model_to_source_indices'])
        if record['id'] == 'p192_B':
            assert record['model']['source_gap'] == 109
            assert record['model']['all_tied_source_gaps'] == [109, 110]
            literal, gap = record['literal_source'], 110
            cipher = literal[:gap] + '?' + literal[gap:]
            mapping = list(range(gap)) + [None] + list(range(gap, len(literal)))
            add(record['id'], 'alternative source gap 110', cipher, record['key_id'], source, mapping)

    source = 'data/certificates/p189.json'
    d = read(source)
    add('p185_C', 'literal', d['p185']['ciphertext'], d['key']['id'], source)
    projection = analyze(d['p185']['ciphertext'], d['p189']['erasure_normalized_ciphertext'],
                         d['key']['column_rank_order'], d['key']['square'])
    assert projection['path_count'] == 10
    for i, row in enumerate(projection['paths']):
        add('p189', f'conditional source alignment {i}', row['aligned_ciphertext'],
            d['key']['id'], source, row['parallel_to_target_index'])

    source = 'data/certificates/p185_D_transport.json'
    d = read(source)
    row = d['selected_geometry']
    add('p185_D', 'previously selected conditional geometry', row['corrected_ciphertext'],
        d['key']['id'], source, row['corrected_to_source_index'])
    for row in d['direct_transport_context']:
        original = row['source']
        add(original['id'], 'literal conservative source', original['analysis_ciphertext'],
            original['key_id'], source)

    source = 'data/certificates/p197_p198_transport.json'
    d = read(source)
    for row in d['records']:
        if len(row['analysis_ciphertext']) % 2 == 0:
            add(row['id'], 'literal conservative source', row['analysis_ciphertext'],
                d['key']['id'], source)
    for kind in ('duplicate_group_repair', 'erasure_relocation', 'missing_group_alignment'):
        reconstruction = d[kind]
        for i, row in enumerate(reconstruction.get('candidates', reconstruction.get('best_alignments', []))):
            add(reconstruction['source_id'], f'{kind} alias {i}', row['corrected_ciphertext'],
                d['key']['id'], source, row.get('corrected_to_source_index'))

    source = 'data/supplementary_readings.json'
    for row in read(source)['messages']:
        if row['key_id'] in ('Nov13-15a', 'Nov13-15b'):
            add(row['id'], 'literal conservative source', row['source_ciphertext_conservative'],
                row['key_id'], source)

    source = 'experiments/aviation_connection/certificate.json'
    d = read(source)
    for row in d['candidates']:
        gap = row['gap_boundary_0based']
        for name, cipher in [('source model', row['framed_ciphertext']),
                             ('explicit previous editorial repairs', row['edition']['ciphertext'])]:
            add('p187_D', f'gap {gap}: {name}', cipher, 'Nov13-15a', source)
    assert len({(r['id'], r['variant']) for r in records}) == len(records)
    return records


def inventory_report(keys):
    effects, direct, reference = [], [], []
    for record in inventory():
        key = keys[record['key_id']]
        cell = 17 if key['id'] == 'Nov13-15b' else 9
        changed = assign(key['square'], cell, 'Y')
        before = inspect(record['ciphertext'], key['column_rank_order'], key['square'])
        after = inspect(record['ciphertext'], key['column_rank_order'], changed)
        changes = []
        for i, (old, new) in enumerate(zip(before['domains'], after['domains'])):
            assert set(new) <= set(old)
            if old != new:
                frame_indices = before['inverse_indices'][2 * i:2 * i + 2]
                mapping = record['frame_to_source_indices']
                changes.append({'plaintext_index': i, 'domain_before': old, 'domain_after': new,
                                'coordinate_pair': before['pairs'][i],
                                'possible_square_cells': before['cells'][i],
                                'frame_indices': frame_indices,
                                'source_indices': [mapping[j] for j in frame_indices] if mapping else None})
        newly_fixed = [p for p in changes if len(p['domain_before']) > 1 and len(p['domain_after']) == 1]
        direct.extend({'id': record['id'], 'variant': record['variant'], **p} for p in newly_fixed)
        effects.append({**record, 'raw_before': before['raw'], 'raw_after': after['raw'],
                        'fixed_before': sum(len(d) == 1 for d in before['domains']),
                        'fixed_after': sum(len(d) == 1 for d in after['domains']),
                        'newly_fixed_positions': newly_fixed, 'all_changed_domains': changes})
        if record['id'] == 'p187_D' and 'editorial' in record['variant']:
            unknown_positions = [i for i, domain in enumerate(after['domains']) if len(domain) > 1]
            unknown_cells = sorted({before['cells'][i][0] for i in unknown_positions})
            assert len(unknown_positions) == 12 and len(unknown_cells) == 5
            assert all(len(before['cells'][i]) == 1 for i in unknown_positions)
            assert 9 not in unknown_cells
            assert all(after['domains'][i] == '0123456789Q' for i in unknown_positions)
            reference.append({'variant': record['variant'], 'unresolved_positions': unknown_positions,
                              'distinct_square_cells': unknown_cells,
                              'allowed_symbols_before': '0123456789QY',
                              'allowed_symbols_after': '0123456789Q',
                              'coupled_field_assignments_before': math.perm(12, 5),
                              'coupled_field_assignments_after': math.perm(11, 5),
                              'newly_fixed_positions': 0})
    assert {(p['id'], p['plaintext_index']) for p in direct} == {
        ('p192_3', 61), ('p190_A', 37), ('p194_B', 54), ('p193_B', 54)}
    return {'scope': 'Explicitly enumerated previously reviewed source frames and editorial variants; not every ciphertext in Childs.',
            'unique_physical_records': len({r['id'] for r in effects}),
            'source_and_editorial_variants': len(effects),
            'newly_fixed_positions_in_all_variants': direct,
            'effects': effects, 'p187_D_reference_constraints': reference}


def build(recompute=False):
    DEPENDENCIES.clear()
    keys = {k['id']: k for k in read('data/keys.json')['keys']}
    name = read('experiments/tiflis_appointment/certificates.json')
    layers = name['conditional_key_layers']
    assert layers['layer1']['assignment'] == {
        'key_id': 'Nov13-15b', 'coordinate_pair': 'FX', 'square_cell_index': 17, 'symbol': 'Y'}
    assert layers['layer2']['assignment'] == {
        'key_id': 'Nov13-15a', 'coordinate_pair': 'DG', 'square_cell_index': 9, 'symbol': 'Y'}
    frontier = frontier_report(recompute)
    propagated = inventory_report(keys)
    return {'schema': 'adfgvx-contextual-Nov13-Y-constraints-v1',
            'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
            'dependency_sha256': dict(sorted(DEPENDENCIES.items())),
            'assumptions': {'Nov13-15b': layers['layer1']['assumptions'],
                            'Nov13-15a_additional': layers['layer2']['additional_assumption'],
                            'p198_additional': 'p198 uses the recorded Nov13-15b transposition and square, with exactly five lost coordinates and no received-coordinate substitutions.'},
            'p198_conditional_frontier': frontier,
            'reviewed_frame_inventory': propagated,
            'published_key_files_changed': False,
            'new_historical_digits_recovered': 0,
            'limits': ['Historical name identification remains conditional; cipher arithmetic does not establish it.',
                       'The p198 key and loss model remain unproved, and its actual digit/Q/Y counts remain unknown.',
                       'The inventory retains previously declared source geometry and editorial assumptions; the new assignment does not authenticate those models.',
                       'Marginal character domains are coupled by one injective square. Different frontier witnesses may use different complete squares.',
                       'The four newly fixed letters already occur in the Tiflis/local retransmission edition; this propagation does not claim four additional discoveries.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--recompute', action='store_true',
                        help='Independently recompute all seven retained exact p198 category frontiers')
    args = parser.parse_args()
    report = build(args.recompute)
    output = HERE / 'certificate.json'
    if args.verify:
        assert report == json.loads(output.read_text())
    else:
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, 'independent_memberships_recomputed': 7 if args.recompute else 0,
                      'p198_frontier': report['p198_conditional_frontier']['global_frontier'],
                      'inventory_records': report['reviewed_frame_inventory']['unique_physical_records'],
                      'inventory_variants': report['reviewed_frame_inventory']['source_and_editorial_variants'],
                      'p187_reference_assignments_after': math.perm(11, 5)}, indent=2))


if __name__ == '__main__':
    main()
