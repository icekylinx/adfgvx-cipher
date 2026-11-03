#!/usr/bin/env python3
"""Verify the p162/p166 wire-return source family without double-counting copies.

ADFGVX Cipher source restoration: icekylinx and GPT-6 Astra Pro.
Every pair retains both coordinate origins. The p162 missing prefix stays
unassigned in the primary baseline; cross-source completion is a separate layer.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, untranspose
from experiments.romanian_pacification_consultation.verify import inspect, permutation
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fold(text):
    return re.sub('[^A-Z0-9?]', '', text.upper())


def origin(record_id, index):
    return {'record_id': record_id, 'source_index': index}


def build(pdf=None):
    inp = load(HERE / 'inputs.json')
    key = inp['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    for path, digest in inp['core_sha256'].items():
        assert sha(ROOT / path) == digest
    records = {r['id']: r for r in inp['records']}
    literals = {}
    for r in records.values():
        lit = ''.join(''.join(r['source_rows']).split())
        assert lit == r['literal_source'] and len(lit) == r['source_slots']
        assert set(lit) <= set(C)
        literals[r['id']] = lit
    assert [len(literals[r]) for r in records] == [117, 311, 100]
    prior = inp['prior_snapshot']
    assert sha(HERE / prior['path']) == prior['sha256']
    snapshot = load(HERE / prior['path'])
    live = load(ROOT / prior['context_and_witness_path'])
    assert snapshot['p162_C1_previous_context'] == live['unread_context']
    witness = next(r for r in live['records'] if r['id'] == 'p162_C2')
    assert snapshot['p162_C2_previously_accepted_record'] == witness
    assert witness['literal_source'] == ''.join(''.join(witness['rows']).split())
    literals['p162_C2'] = witness['literal_source']
    old_case = (ROOT / prior['unchanged_case_path']).read_text()
    assert snapshot['old_case_display_fingerprint'] == {
        'headings': re.findall(r'^#{1,6} .*$', old_case, re.M),
        'fences': re.findall(r'```[^\n]*\n(.*?)\n```', old_case, re.S),
        'quotes': [x for x in old_case.splitlines() if x.startswith('>')]}

    def inspect_model(record_id, cipher, origins, label, support=None):
        assert len(cipher) == len(origins)
        mapping = [o['source_index'] if o and o['record_id'] == record_id else None
                   for o in origins]
        result = inspect(cipher, key, mapping)
        support = support or {}
        for position in result['positions']:
            coordinates = []
            for model_index in position['model_indices']:
                o = origins[model_index]
                coordinates.append({
                    'model_index': model_index,
                    'origin': o,
                    'printed_value': literals[o['record_id']][o['source_index']] if o else None,
                    'model_value': cipher[model_index],
                    'supporting_origin': support.get(model_index)})
            position['coordinate_origins'] = coordinates
        return {'id': record_id, 'layer': label, 'ciphertext': cipher,
                'model_to_source_indices': mapping,
                'model_to_coordinate_origins': origins,
                'literal_source': literals[record_id],
                'source_slots': len(literals[record_id]),
                'valid_source_coordinates': sum(c in C for c in literals[record_id]),
                **result}

    a, b, c = [literals[r] for r in records]
    own_a = [origin('p162_C1', i) for i in range(117)]
    own_b = [origin('p166_C1', i) for i in range(311)]
    own_c = [origin('p166_C2', i) for i in range(100)]
    primary_a = inspect_model('p162_C1', '?' * 195 + a, [None] * 195 + own_a,
                              'primary: missing prefix unassigned')
    gap_aliases = []
    for gap, donor_i in zip(inp['source_family']['p166_C1_gap_before_original_indices'],
                            inp['source_family']['p166_C1_missing_fill_witness_indices']):
        assert gap in [225, 226] and donor_i == gap - 195
        base = b[:gap] + '?' + b[gap:]
        origins = own_b[:gap] + [None] + own_b[gap:]
        before = inspect_model('p166_C1', base, origins, f'primary: unfilled gap before source {gap}')
        filled = b[:gap] + a[donor_i] + b[gap:]
        filled_origins = own_b[:gap] + [origin('p162_C1', donor_i)] + own_b[gap:]
        after = inspect_model('p166_C1', filled, filled_origins,
                              f'source-linked missing coordinate from p162 C1 source {donor_i}')
        assert a[donor_i] == 'X'
        assert before['fixed_positions'] == 155 and after['fixed_positions'] == 156
        unknown = [p for p in before['positions'] if p['raw'] == '?']
        assert len(unknown) == 1 and unknown[0]['domain'] == '178COQ'
        assert unknown[0]['plaintext_index'] == {225: 61, 226: 71}[gap]
        assert unknown[0]['pair'] == 'F?'
        gap_aliases.append({'gap_before_original_source_index': gap,
                            'donor': origin('p162_C1', donor_i),
                            'primary_unfilled': before, 'source_linked': after})
    assert gap_aliases[0]['source_linked']['ciphertext'] == gap_aliases[1]['source_linked']['ciphertext']
    primary_b = gap_aliases[0]['primary_unfilled']
    primary_c = inspect_model('p166_C2', c, own_c, 'primary: native 100 coordinates')
    primary = [primary_a, primary_b, primary_c]
    assert [r['fixed_positions'] for r in primary] == [0, 155, 50]
    assert [len(r['raw']) for r in primary] == [156, 156, 50]
    a_pair_origin_counts = {0: 0, 1: 0, 2: 0}
    for p in primary_a['positions']:
        a_pair_origin_counts[sum(o['origin'] is not None for o in p['coordinate_origins'])] += 1
    assert a_pair_origin_counts == {0: 39, 1: 117, 2: 0}

    # Source-only geometry: no expected German or target plaintext enters these costs.
    window_costs = []
    for alias in gap_aliases:
        base = alias['primary_unfilled']['ciphertext']
        costs = [sum(u != v for u, v in zip(a, base[t:t + 117]) if v != '?')
                 for t in range(196)]
        assert min(costs) == 2 and [i for i, v in enumerate(costs) if v == 2] == [195]
        window_costs.append({'gap_before_original_source_index': alias['gap_before_original_source_index'],
                             'all_196_window_costs': costs, 'minimum': 2,
                             'minimum_window_start': 195})
    suffix = b[195:]
    assert len(suffix) == 116
    insertion_costs = [sum(u != v for u, v in zip(a, suffix[:i] + '?' + suffix[i:]) if v != '?')
                       for i in range(117)]
    assert min(insertion_costs) == 2
    assert [i for i, v in enumerate(insertion_costs) if v == 2] == [30, 31]
    overlap = []
    for i, (av, bv) in enumerate(zip(a, primary_b['ciphertext'][195:])):
        model_i = 195 + i
        overlap.append({'p162_source_index': i, 'p162_value': av,
                        'p166_model_index': model_i,
                        'p166_original_source_index': primary_b['model_to_source_indices'][model_i],
                        'p166_unfilled_value': bv,
                        'status': 'gap' if bv == '?' else ('agree' if av == bv else 'disagree')})
    assert {s: sum(r['status'] == s for r in overlap) for s in ['agree', 'disagree', 'gap']} == {
        'agree': 114, 'disagree': 2, 'gap': 1}
    assert [[r['p162_source_index'], r['p166_original_source_index'], r['p166_unfilled_value'], r['p162_value']]
            for r in overlap if r['status'] == 'disagree'] == [[52, 246, 'D', 'G'], [53, 247, 'F', 'D']]

    linked_a = inspect_model('p162_C1', b[:195] + a, own_b[:195] + own_a,
                             'source-linked: 195 observed prefix coordinates copied from p166 C1')
    linked_b = gap_aliases[0]['source_linked']
    linked_c = primary_c
    linked = [linked_a, linked_b, linked_c]
    assert [r['fixed_positions'] for r in linked] == [156, 156, 50]
    linked_pair_origins = {'both_from_p166_prefix': 0, 'one_from_each_record': 0,
                          'both_from_p162': 0}
    for p in linked_a['positions']:
        ids = [o['origin']['record_id'] for o in p['coordinate_origins']]
        if ids == ['p166_C1', 'p166_C1']:
            linked_pair_origins['both_from_p166_prefix'] += 1
        elif ids == ['p162_C1', 'p162_C1']:
            linked_pair_origins['both_from_p162'] += 1
        else:
            linked_pair_origins['one_from_each_record'] += 1
    assert linked_pair_origins == {'both_from_p166_prefix': 39, 'one_from_each_record': 117, 'both_from_p162': 0}

    # The collated layer is distinct from language-based editing.
    collated_b_cipher = list(linked_b['ciphertext'])
    cross_ledger = []
    support_b = {}
    for source_i, before, after, donor_i in inp['source_family']['p166_C1_cross_copy_substitutions']:
        model_i = source_i + 1
        assert b[source_i] == before and a[donor_i] == after
        assert collated_b_cipher[model_i] == before
        collated_b_cipher[model_i] = after
        support_b[model_i] = origin('p162_C1', donor_i)
        cross_ledger.append({'record_id': 'p166_C1', 'source_index': source_i,
                             'model_index': model_i, 'from': before, 'to': after,
                             'kind': 'observed substitution supported by other source copy',
                             'support': origin('p162_C1', donor_i)})
    collated_b_cipher = ''.join(collated_b_cipher)
    assert collated_b_cipher == linked_a['ciphertext']
    collated_b = inspect_model('p166_C1', collated_b_cipher, linked_b['model_to_coordinate_origins'],
                               'source-collated: missing X and two observed-copy substitutions', support_b)
    assert collated_b['raw'] == linked_a['raw']
    source_i, before, after, donor_i = inp['source_family']['p166_C2_cross_copy_substitution']
    assert c[source_i] == before and literals['p162_C2'][donor_i] == after
    collated_c_cipher = c[:source_i] + after + c[source_i + 1:]
    support_c = {source_i: origin('p162_C2', donor_i)}
    collated_c = inspect_model('p166_C2', collated_c_cipher, own_c,
                               'source-collated: one observed-copy substitution', support_c)
    cross_ledger.append({'record_id': 'p166_C2', 'source_index': source_i, 'model_index': source_i,
                         'from': before, 'to': after,
                         'kind': 'observed substitution supported by other source copy',
                         'support': origin('p162_C2', donor_i)})
    lexical_ledger = []
    final_cipher = list(collated_b_cipher)
    for source_i, before, after in inp['source_family']['p166_C1_optional_lexical_substitutions']:
        assert source_i < 195 and b[source_i] == before and final_cipher[source_i] == before
        final_cipher[source_i] = after
        lexical_ledger.append({'record_id': 'p166_C1', 'source_index': source_i,
                               'model_index': source_i, 'from': before, 'to': after,
                               'kind': 'optional lexical substitution in shared p166 prefix',
                               'independently_observed_in_p162': False})
    final_cipher = ''.join(final_cipher)
    edited_a = inspect_model('p162_C1', final_cipher, linked_a['model_to_coordinate_origins'],
                             'optional edition: three substitutions at borrowed p166 prefix origins')
    edited_b = inspect_model('p166_C1', final_cipher, linked_b['model_to_coordinate_origins'],
                             'optional edition: two copy-supported plus three lexical substitutions', support_b)
    edited_c = collated_c
    editions = [edited_a, edited_b, edited_c]
    for r in editions:
        assert r['raw'] == records[r['id']]['edited_output']
        assert encrypt(r['raw'], key['column_rank_order'], key['square']) == r['ciphertext']
        assert fold(records[r['id']]['readable_german']) == r['raw']
    assert len({(r['record_id'], r['source_index']) for r in cross_ledger + lexical_ledger}) == 6
    changed_labels = {}
    for before, after in zip(linked, editions):
        changed_labels[before['id']] = [{'before': p, 'after': q}
                                      for p, q in zip(before['positions'], after['positions'])
                                      if p['raw'] != q['raw']]
    assert [[r['before']['plaintext_index'] for r in changed_labels[k]] for k in records] == [
        [42, 52, 62], [42, 52, 62, 123, 133], [47]]

    witness_base = inspect_model('p162_C2', literals['p162_C2'].replace('-', '?'),
                                 [origin('p162_C2', i) for i in range(100)],
                                 'existing accepted witness: native source, printed dash unfilled')
    assert witness_base['raw'] == witness['expected_raw'] and witness_base['fixed_positions'] == 49
    wfilled = literals['p162_C2'][:36] + c[36] + literals['p162_C2'][37:]
    assert c[36] == 'G'
    assert wfilled == collated_c_cipher
    assert decrypt(wfilled, key['column_rank_order'], key['square']) == witness['editorial_text']
    c2_differences = [{'source_index': i, 'p162': u, 'p166': v}
                      for i, (u, v) in enumerate(zip(literals['p162_C2'], c)) if u != v]
    assert c2_differences == [{'source_index': 36, 'p162': '-', 'p166': 'G'},
                             {'source_index': 84, 'p162': 'V', 'p166': 'F'}]
    c2_cross_pair_witnesses = []
    for i in [14, 47]:
        c2_cross_pair_witnesses.append({'plaintext_index': i,
                                       'p162_native_pair': witness_base['positions'][i],
                                       'p166_native_pair': primary_c['positions'][i],
                                       'collated_p166_pair': collated_c['positions'][i]})

    # Retain exact native odd frames as diagnostics, including their unpaired slot.
    native_odd = []
    for rid in ['p162_C1', 'p166_C1']:
        lit = literals[rid]
        order = permutation(len(lit), key['column_rank_order'])
        interim = untranspose(lit, key['column_rank_order'])
        native_odd.append({'id': rid, 'literal_source': lit,
                           'paired_plaintext_prefix': decrypt(lit, key['column_rank_order'], key['square'], allow_unpaired=True),
                           'unpaired_interim_coordinate': interim[-1],
                           'unpaired_original_source_index': order[-1],
                           'paired_labels': len(lit) // 2,
                           'counted_in_primary_fixed_positions': False})
    ocr = {r['id']: r for r in load(ROOT / prior['ocr_source_path'])['blocks']}
    ocr_comparisons = []
    for old, rid in zip(snapshot['records'], ['p166_C1', 'p166_C2']):
        assert old == ocr[old['id']]
        before, after = ''.join(old['groups']), literals[rid]
        operations = [list(op) for op in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes()]
        rebuilt = ''.join(before[i:j] if tag == 'equal' else after[u:v] for tag, i, j, u, v in operations)
        assert rebuilt == after
        ocr_comparisons.append({'id': rid, 'earlier_ocr_id': old['id'], 'earlier_ocr': before,
                                'earlier_slots': len(before), 'reviewed_source_slots': len(after),
                                'reproducible_text_alignment': operations,
                                'historical_coordinate_repair_cost': False})
    assert [r['earlier_slots'] for r in ocr_comparisons] == [307, 100]

    case = ROOT / inp['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(r['role_from_caption'] for r in fences + quotes)
    expected_fences = [primary_a['raw'], linked_a['raw'], edited_a['raw'],
                       primary_b['raw'], gap_aliases[1]['primary_unfilled']['raw'],
                       linked_b['raw'], edited_b['raw'], primary_c['raw'], edited_c['raw']]
    assert re.findall(r'```text\n(.*?)\n```', text, re.S) == expected_fences
    quote_texts = [''.join(line[2:] for line in block.splitlines())
                   for block in re.findall(r'(?:^>.*\n?)+', text, re.M)]
    assert [fold(q) for q in quote_texts] == [r['raw'] for r in editions]
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        assert pdf.stat().st_size == inp['source']['pdf_bytes']
        doc = fitz.open(pdf)
        for crop in inp['source']['reviewed_crops']:
            fitz.TOOLS.store_shrink(100)
            pix = doc[crop['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(crop['render_scale'], crop['render_scale']),
                clip=fitz.Rect(*crop['crop_pdf_points']), alpha=False)
            assert (pix.width, pix.height, pix.n) == (crop['width'], crop['height'], crop['channels'])
            assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']

    per_record = []
    for r, p, s, e in zip(records.values(), primary, linked, editions):
        per_record.append({'id': r['id'], 'source_slots': r['source_slots'],
                           'valid_source_coordinates': r['source_slots'],
                           'modeled_coordinates': len(p['ciphertext']),
                           'plaintext_positions': len(p['raw']),
                           'baseline_fixed_positions': p['fixed_positions'],
                           'source_linked_fixed_positions_added': s['fixed_positions'] - p['fixed_positions'],
                           'source_linked_fixed_positions': s['fixed_positions'],
                           'candidate_fixed_positions': e['fixed_positions'],
                           'unique_observed_substitutions_at_this_record_origins': sum(x['record_id'] == r['id'] for x in cross_ledger + lexical_ledger)})
    counts = {'physical_records': 3, 'printed_source_slots': 528,
              'valid_source_coordinates': 528, 'modeled_coordinates': 724,
              'plaintext_positions': 362, 'baseline_fixed_positions': 205,
              'source_linked_fixed_positions_added': 157,
              'source_linked_fixed_positions': 362, 'candidate_fixed_positions': 362,
              'known_coordinate_substitutions': 6,
              'cross_copy_observed_substitutions': 3, 'lexical_observed_substitutions': 3,
              'printed_mask_fills': 0, 'independently_supported_inserted_coordinate_fills': 1,
              'copied_prefix_coordinates': 195, 'inserted_missing_coordinate_slots': 1,
              'source_deletions': 0, 'key_changed': False, 'source_reordering': False,
              'supporting_previously_accepted_records_not_counted': ['p162_C2']}
    for field in ['source_slots', 'valid_source_coordinates', 'modeled_coordinates', 'plaintext_positions',
                  'baseline_fixed_positions', 'source_linked_fixed_positions_added',
                  'source_linked_fixed_positions', 'candidate_fixed_positions']:
        assert sum(r[field] for r in per_record) == counts.get(field, counts.get('printed_source_slots'))
    return {'schema': 'adfgvx-nov9-wire-return-source-family-certificate-v1',
            'authors': inp['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': 'All indices are zero-based; slices are half-open.',
            'source_records': list(records), 'source': inp['source'],
            'normalized_counts': counts, 'per_record_normalized_counts': per_record,
            'primary_unfilled_records': primary,
            'source_linked_records': linked,
            'source_collated_records': [linked_a, collated_b, collated_c],
            'optional_edited_records': editions,
            'all_p166_C1_gap_aliases': gap_aliases,
            'source_only_alignment': {'target_source_coordinates': 117,
              'p166_suffix_window_start': 195, 'overlap_positions': overlap,
              'independent_coordinate_agreements': 114, 'observed_disagreements': 2,
              'missing_comparison_coordinates': 1, 'window_comparisons': window_costs,
              'all_117_suffix_insertion_costs': insertion_costs,
              'minimum_cost_gap_local_positions': [30, 31],
              'minimum_observed_disagreements': 2,
              'scope': 'One missing p166 coordinate and an unchanged 117-coordinate p162 fragment; no plaintext target or language objective.'},
            'p162_primary_pair_observation_counts': {str(k): v for k, v in a_pair_origin_counts.items()},
            'p162_source_linked_pair_origins': linked_pair_origins,
            'deduplicated_cross_copy_substitutions': cross_ledger,
            'deduplicated_lexical_substitutions': lexical_ledger,
            'all_optional_changed_plaintext_positions': changed_labels,
            'existing_p162_C2_native_witness': witness_base,
            'C2_source_differences': c2_differences,
            'C2_complete_pair_cross_witnesses': c2_cross_pair_witnesses,
            'native_odd_frame_diagnostics': native_odd,
            'retained_OCR_comparisons': ocr_comparisons,
            'full_final_stream_roundtrips': True,
            'old_p162_C2_displays_unchanged': True,
            'core_data_unchanged': True,
            'prior_credit': inp['prior_credit'], 'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert load(path) == result, 'Recomputed certificate differs'
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify,
                      'source_pixel_check': 'passed' if args.pdf else 'skipped: provide --pdf to reproduce reviewed source pixels',
                      **result['normalized_counts']}, indent=2))


if __name__ == '__main__':
    main()
