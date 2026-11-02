#!/usr/bin/env python3
"""Verify all p185 D contiguous-gap constraints using only the standard library.

This checks source preservation, exact transposition, every reported domain,
geometry equivalences, and the direct transport-context readings. Language
scores are metadata: this verifier does not use them to certify a plaintext.
"""
from pathlib import Path
from collections import defaultdict
import json
import sys

COORDS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def reconstruct(ciphertext, ranks):
    width = len(ranks)
    columns = [[] for _ in ranks]
    source_columns = [[] for _ in ranks]
    p = 0
    for col in sorted(range(width), key=lambda i: ranks[i]):
        size = len(ciphertext) // width + (col < len(ciphertext) % width)
        columns[col] = list(ciphertext[p:p + size])
        source_columns[col] = list(range(p, p + size))
        p += size
    intermediate = []
    mapping = []
    for row in range(max(map(len, columns))):
        for col in range(width):
            if row < len(columns[col]):
                intermediate.append(columns[col][row])
                mapping.append(source_columns[col][row])
    assert len(intermediate) == len(ciphertext)
    back = ''.join(''.join(intermediate[col::width]) for col in sorted(range(width), key=lambda i: ranks[i]))
    assert back == ciphertext
    return ''.join(intermediate), mapping


def characterize(ciphertext, ranks, square, source_map):
    assert len(ciphertext) % 2 == 0
    stream, mapping = reconstruct(ciphertext, ranks)
    unused = set(ALPHABET) - set(square)
    assert len(unused) == square.count('?') == 8
    rows = []
    for j in range(len(stream) // 2):
        pair = stream[2 * j:2 * j + 2]
        cells, letters = [], set()
        for cell in range(36):
            encoded = COORDS[cell // 6] + COORDS[cell % 6]
            if all(a == '?' or a == b for a, b in zip(pair, encoded)):
                cells.append(cell)
                letters.update(unused if square[cell] == '?' else square[cell])
        rows.append({'plaintext_index': j,
                     'coordinate_pair': pair,
                     'source_indices': [source_map[mapping[2 * j]], source_map[mapping[2 * j + 1]]],
                     'corrected_ciphertext_indices': mapping[2 * j:2 * j + 2],
                     'possible_square_cells': cells,
                     'possible_characters': ''.join(sorted(letters))})
    raw = ''.join(r['possible_characters'] if len(r['possible_characters']) == 1 else '?' for r in rows)
    return {'raw_partial_plaintext': raw, 'domains': rows,
            'fixed_plaintext_characters': raw.count('?') * -1 + len(raw),
            'intermediate_stream': stream}


def common_fixed(candidates):
    return ''.join(ds[0] if len(ds[0]) == 1 and all(d == ds[0] for d in ds) else '?'
                   for ds in zip(*(c['plaintext_domains'] for c in candidates)))


def verify(record):
    raw = record['source']['ciphertext']
    assert ''.join(record['source']['ciphertext_grouped'].split()) == raw
    ct = ''.join(c if c in COORDS else '?' for c in raw)
    assert len(ct) == 193 and ct.count('?') == 1
    assert record['normalization']['analysis_ciphertext'] == ct
    assert record['normalization']['invalid_source_slots'] == [
        {'source_index': 159, 'printed': 'Y', 'analysis': '?'}]
    ranks, square = record['key']['column_rank_order'], record['key']['square']
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    candidates = record['all_contiguous_gap_candidates']
    assert len(candidates) == 194
    assert [c['insert_five_erasures_before_source_index'] for c in candidates] == list(range(194))
    ciphertext_groups, plaintext_groups = defaultdict(list), defaultdict(list)
    for gap, row in enumerate(candidates):
        corrected = ct[:gap] + '?' * 5 + ct[gap:]
        source_map = list(range(gap)) + [None] * 5 + list(range(gap, len(ct)))
        assert corrected == row['corrected_ciphertext']
        assert corrected[:gap] + corrected[gap + 5:] == ct
        actual = characterize(corrected, ranks, square, source_map)
        assert actual['raw_partial_plaintext'] == row['raw_partial_plaintext']
        assert [d['possible_characters'] for d in actual['domains']] == row['plaintext_domains']
        assert actual['fixed_plaintext_characters'] == row['fixed_plaintext_characters']
        assert row['at_printed_group_boundary'] == (gap % 5 == 0 or gap == 193)
        ciphertext_groups[corrected].append(gap)
        plaintext_groups[actual['raw_partial_plaintext']].append(gap)
    search = record['search']
    assert search['tested_placements'] == 194
    assert search['unique_masked_ciphertexts'] == len(ciphertext_groups) == 193
    assert search['unique_raw_partial_plaintext_strings'] == len(plaintext_groups)
    assert search['identical_ciphertext_geometry_classes'] == [g for g in ciphertext_groups.values() if len(g) > 1]
    assert search['identical_raw_plaintext_geometry_classes'] == [g for g in plaintext_groups.values() if len(g) > 1]
    assert search['identical_ciphertext_geometry_classes'] == [[159, 160]]
    assert search['shared_fixed_letters_over_all_placements'] == common_fixed(candidates) == '?' * 99
    rankings = sorted(candidates, key=lambda c: (-c['ranking_heuristic_score'], c['insert_five_erasures_before_source_index']))
    basic = sorted(candidates, key=lambda c: (-c['legacy_plaintext_quadgram_mean'], c['insert_five_erasures_before_source_index']))
    assert search['ranked_gap_positions'] == [r['insert_five_erasures_before_source_index'] for r in rankings]
    assert search['legacy_quadgram_ranked_gap_positions'] == [r['insert_five_erasures_before_source_index'] for r in basic]
    assert search['heuristic_best_gap'] == 55 and search['legacy_quadgram_best_gap'] == 57
    assert search['top_three_ranked_positions'] == [55, 56, 57]
    assert search['shared_fixed_letters_over_top_three_ranked_positions'] == common_fixed(rankings[:3])
    selected = record['selected_geometry']
    assert selected['insert_five_erasures_before_source_index'] == 55
    assert selected['known_source_substitutions'] == selected['erasure_fills'] == []
    source_map = list(range(55)) + [None] * 5 + list(range(55, len(ct)))
    assert selected['corrected_to_source_index'] == source_map
    corrected = candidates[55]['corrected_ciphertext']
    assert selected['corrected_ciphertext'] == corrected
    assert selected['analysis'] == characterize(corrected, ranks, square, source_map)
    assert selected['analysis']['fixed_plaintext_characters'] == 91
    assert selected['all_192_valid_source_coordinates_preserved'] is True
    assert selected['coordinate_transposition_roundtrip'] is True
    direct_context = []
    context_by_id = {}
    for row in record.get('direct_transport_context', []):
        source = row['source']
        normalized = ''.join(c if c in COORDS else '?' for c in source['raw_literal'])
        assert normalized == source['analysis_ciphertext']
        assert row['known_source_substitutions'] == row['erasure_fills'] == row['insertions'] == row['deletions'] == []
        actual = characterize(normalized, ranks, square, list(range(len(normalized))))
        assert actual == row['analysis']
        assert actual['raw_partial_plaintext'] == source['raw_plaintext']
        direct_context.append({'id': source['id'], 'raw_partial_plaintext': actual['raw_partial_plaintext'],
                               'coordinate_roundtrip': True})
        context_by_id[source['id']] = row
    for comparison in record.get('transport_parallel_comparisons', []):
        first_id, second_id = comparison['first_source_id'], comparison['second_source_id']
        first = context_by_id[first_id]['source']['raw_literal']
        second = context_by_id[second_id]['source']['raw_literal']
        assert len(first) == len(second) == comparison['length']
        differences = [{'source_index': i, 'first_printed': a, 'second_printed': b,
                        'both_valid_adfgvx': a in COORDS and b in COORDS}
                       for i, (a, b) in enumerate(zip(first, second)) if a != b]
        assert differences == comparison['differences']
        assert len(first) - len(differences) == comparison['exact_equal_coordinates']
        expected_plaintext_differences = [
            {'plaintext_index': i, 'first_raw': a, 'second_raw': b}
            for i, (a, b) in enumerate(zip(
                context_by_id[first_id]['analysis']['raw_partial_plaintext'],
                context_by_id[second_id]['analysis']['raw_partial_plaintext'])) if a != b]
        assert comparison['known_plaintext_differences'] == expected_plaintext_differences
    if 'source_supported_transport_composite' in record:
        composite = record['source_supported_transport_composite']
        first = context_by_id['p194_A']['source']['raw_literal']
        second = context_by_id['p196_B']['source']['raw_literal']
        corrected = list(''.join(c if c in COORDS else '?' for c in first))
        assert [e['source_index'] for e in composite['edits']] == [82, 167]
        for edit in composite['edits']:
            i = edit['source_index']
            assert edit['printed_in_p194_A'] == first[i]
            assert edit['chosen_value'] == second[i]
            corrected[i] = second[i]
        corrected = ''.join(corrected)
        assert corrected[173] == first[173]
        assert corrected == composite['corrected_ciphertext']
        assert composite['analysis'] == characterize(corrected, ranks, square, list(range(174)))
        assert composite['analysis']['fixed_plaintext_characters'] == 86
        alternatives = composite['all_four_observed_coordinate_choices']
        assert len(alternatives) == 4
        assert {(a['source_167'], a['source_173']) for a in alternatives} == {('V', 'D'), ('V', 'G'), ('X', 'D'), ('X', 'G')}
        for alternative in alternatives:
            trial = list(corrected)
            trial[167], trial[173] = alternative['source_167'], alternative['source_173']
            trial = ''.join(trial)
            assert trial == alternative['ciphertext']
            assert characterize(trial, ranks, square, list(range(174)))['raw_partial_plaintext'] == alternative['raw_partial_plaintext']
    return {
        'verified': True,
        'all_194_geometry_constraint_sets_verified': True,
        'all_192_valid_source_symbols_preserved': True,
        'invalid_source_slot_preserved_as_erasure': True,
        'masked_ciphertext_equivalence_class': [159, 160],
        'selected_gap_geometry_proved_unique': False,
        'selected_gap_position': 55,
        'selected_fixed_plaintext_characters': 91,
        'plaintext_length': 99,
        'ranking_metadata_sorted_consistently': True,
        'language_scores_recomputed_by_this_verifier': False,
        'source_only_new_square_cell_assignments': 0,
        'transport_parallel_comparisons_verified': len(record.get('transport_parallel_comparisons', [])),
        'conditional_transport_composite_verified': 'source_supported_transport_composite' in record,
        'direct_context': direct_context,
    }


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'data/certificates/p185_D_transport.json'
    print(json.dumps(verify(json.loads(path.read_text())), indent=2))
