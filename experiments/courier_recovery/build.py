#!/usr/bin/env python3
"""Exact source accounting for the Munich courier message candidates.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The first-part candidate is editorial input. Minimum-cost source alignment is
not a proof that this plaintext or its four missing positions is historical.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import (ALPHABET, SYMBOLS, decrypt, plaintext_domains,
                          transpose, transposition_indices, untranspose)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(record):
    literal = ''.join(''.join(record['source_rows']).split())
    assert set(literal) <= set(SYMBOLS)
    uncertain = set(record['uncertain_source_indices'])
    assert all(0 <= i < len(literal) for i in uncertain)
    masked = ''.join('?' if i in uncertain else c for i, c in enumerate(literal))
    return literal, masked


def insertion_fits(observed, target):
    """All minimum-substitution fits with exactly len(target)-len(observed) losses.

    F[j,l] fits the first j-l observed slots into j target slots. A missing
    target slot extends F[j-1,l-1]; retaining a source slot extends F[j-1,l]
    and costs one precisely for a disagreement between known coordinates.
    Source erasures cost zero. No received slot can be deleted or reordered.
    """
    n, m = len(observed), len(target)
    missing = m - n
    assert missing >= 0 and '?' not in target
    infinity = m + n + 1
    costs = [[infinity] * (missing + 1) for _ in range(m + 1)]
    counts = [[0] * (missing + 1) for _ in range(m + 1)]
    costs[0][0], counts[0][0] = 0, 1
    for j in range(1, m + 1):
        for lost in range(min(j, missing) + 1):
            consumed = j - lost
            options = []
            if lost:
                options.append((costs[j-1][lost-1], counts[j-1][lost-1]))
            if 0 < consumed <= n:
                mismatch = observed[consumed-1] not in ('?', target[j-1])
                options.append((costs[j-1][lost] + mismatch,
                                counts[j-1][lost]))
            if options:
                costs[j][lost] = min(cost for cost, _ in options)
                counts[j][lost] = sum(number for cost, number in options
                                      if cost == costs[j][lost])
    # These historical instances have at most 32 optimal masks. Refuse to
    # truncate a larger set silently.
    assert counts[m][missing] <= 10000
    masks = []

    def recover(j, lost, positions):
        if j == 0:
            assert lost == 0
            masks.append(sorted(positions))
            return
        consumed = j - lost
        if lost and costs[j][lost] == costs[j-1][lost-1]:
            recover(j-1, lost-1, positions + [j-1])
        if 0 < consumed <= n:
            mismatch = observed[consumed-1] not in ('?', target[j-1])
            if costs[j][lost] == costs[j-1][lost] + mismatch:
                recover(j-1, lost, positions)

    recover(m, missing, [])
    masks.sort()
    assert len(masks) == counts[m][missing] == len({tuple(x) for x in masks})
    return costs[m][missing], masks


def fit_report(observed, target, ranks, square):
    minimum, masks = insertion_fits(observed, target)
    inverse = [0] * len(target)
    for source, intermediate in enumerate(transposition_indices(len(target), ranks)):
        inverse[intermediate] = source
    cases = []
    common_support = set(range(len(target) // 2))
    for mask in masks:
        omitted = set(mask)
        values = iter(enumerate(observed))
        frame, source_map, edits, erasures = [], [], [], []
        for j, desired in enumerate(target):
            if j in omitted:
                frame.append('?')
                source_map.append(None)
            else:
                i, actual = next(values)
                frame.append(actual)
                source_map.append(i)
                if actual == '?':
                    erasures.append({'source_index': i, 'target_index': j,
                                     'proposed': desired})
                elif actual != desired:
                    edits.append({'source_index': i, 'target_index': j,
                                  'source': actual, 'proposed': desired})
        assert next(values, None) is None and len(edits) == minimum
        frame = ''.join(frame)
        assert ''.join(c for j, c in enumerate(frame) if j not in omitted) == observed
        support = [p for p in range(len(target) // 2)
                   if all(frame[inverse[2*p + shift]] == target[inverse[2*p + shift]]
                          for shift in (0, 1))]
        common_support.intersection_update(support)
        cases.append({
            'missing_target_positions': mask,
            'missing_values_required_by_editorial_candidate': ''.join(target[i] for i in mask),
            'known_coordinate_changes': edits,
            'source_erasure_fills_required_by_candidate': erasures,
            'source_preserving_masked_frame': frame,
            'raw_plaintext_before_fills_or_changes': decrypt(frame, ranks, square),
            'candidate_positions_with_complete_unchanged_pair': support,
        })
    return {'received_slots': len(observed), 'target_slots': len(target),
            'inserted_slots': len(target) - len(observed),
            'deleted_source_slots': 0,
            'minimum_known_coordinate_changes': minimum,
            'optimal_alignment_count': len(masks),
            'candidate_positions_with_unchanged_pair_in_every_optimum': sorted(common_support),
            'optimal_alignments': cases}


def candidate_stream(text, square, unknown_cells):
    stream = []
    for position, char in enumerate(text):
        cell = unknown_cells[str(position)] if char == '?' else square.index(char)
        assert char != '?' or square[cell] == '?'
        stream.append(SYMBOLS[cell // 6] + SYMBOLS[cell % 6])
    return ''.join(stream)


def one_deletion_sensitivity(observed, target, ranks, square):
    """Exhaust the separate model allowing one received slot to be deleted.

    The six-letter group does not establish which, if any, coordinate is
    extra. Test every source slot; never fold this deletion into the literal
    transcription or the primary source-preserving alignment model.
    """
    trials = []
    best = len(target) + 1
    for deleted in range(len(observed)):
        shortened = observed[:deleted] + observed[deleted + 1:]
        minimum, masks = insertion_fits(shortened, target)
        trials.append({'deleted_source_index': deleted,
                       'deleted_source_coordinate': observed[deleted],
                       'minimum_known_coordinate_changes': minimum,
                       'optimal_alignment_count': len(masks)})
        best = min(best, minimum)
    optima = []
    common = set(range(len(target) // 2))
    for row in trials:
        if row['minimum_known_coordinate_changes'] != best:
            continue
        deleted = row['deleted_source_index']
        fit = fit_report(observed[:deleted] + observed[deleted + 1:],
                         target, ranks, square)
        common.intersection_update(
            fit['candidate_positions_with_unchanged_pair_in_every_optimum'])
        optima.append({**row,
                       'all_optimal_missing_target_positions': [
                           alignment['missing_target_positions']
                           for alignment in fit['optimal_alignments']]})
    return {'model': 'Delete exactly one received slot, then insert exactly enough slots to reach the declared length; minimize retained-coordinate substitutions.',
            'source_deletion_positions_tested': len(trials),
            'inserted_slots': len(target) - len(observed) + 1,
            'deleted_source_slots': 1,
            'minimum_known_coordinate_changes': best,
            'optimal_alignment_count': sum(x['optimal_alignment_count'] for x in optima),
            'all_optimal_deletion_choices': optima,
            'all_deletion_trials': trials,
            'candidate_positions_with_unchanged_pair_in_every_optimum': sorted(common)}


def build():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    key = inputs['key_snapshot']
    catalogue = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    assert key == catalogue[key['id']]
    ranks, square = key['column_rank_order'], key['square']
    for image in inputs['source_images']:
        assert sha(HERE / image['path']) == image['sha256']
    records = {r['id']: r for r in inputs['records']}
    raw = {name: sources(record) for name, record in records.items()}
    literal_a, masked_a = raw['p153_E1']
    literal_b, masked_b = raw['p162_A1']
    assert (len(masked_a), len(masked_b)) == (259, 264)
    relative = []
    for gap in range(len(masked_a) + 1):
        padded = masked_a[:gap] + '?' * 5 + masked_a[gap:]
        disagreements = [i for i, (a, b) in enumerate(zip(padded, masked_b))
                         if a != '?' and b != '?' and a != b]
        relative.append({'gap_before_p153_source_index': gap,
                         'known_coordinate_disagreements': disagreements,
                         'disagreement_count': len(disagreements)})
    minimum = min(row['disagreement_count'] for row in relative)
    best_relative = [row for row in relative if row['disagreement_count'] == minimum]
    assert minimum == 2
    candidate = inputs['first_part_candidate']
    text = candidate['plaintext']
    stream = candidate_stream(text, square, candidate['unresolved_cell_by_position'])
    target = transpose(stream, ranks)
    assert len(target) == 268 and decrypt(target, ranks, square) == text
    fits = {name: fit_report(raw[name][1], target, ranks, square)
            for name in ('p153_E1', 'p162_A1')}
    coordinate_support = set().union(*(set(fit['candidate_positions_with_unchanged_pair_in_every_optimum'])
                                      for fit in fits.values()))
    fixed_support = sorted(p for p in coordinate_support if text[p] != '?')
    sensitivity = {name: one_deletion_sensitivity(raw[name][1], target, ranks, square)
                   for name in fits}
    support_across_models = set().union(*(
        set(fits[name]['candidate_positions_with_unchanged_pair_in_every_optimum']) &
        set(sensitivity[name]['candidate_positions_with_unchanged_pair_in_every_optimum'])
        for name in fits))
    fixed_across_models = sorted(p for p in support_across_models if text[p] != '?')
    # Compare the other unassigned cell without assigning a numerical value.
    alternatives = []
    for cell, value in enumerate(square):
        if value != '?':
            continue
        alternative_stream = candidate_stream(text, square, {'104': cell})
        alternative_cipher = transpose(alternative_stream, ranks)
        by_source = {}
        for name in fits:
            cost, masks = insertion_fits(raw[name][1], alternative_cipher)
            by_source[name] = {'minimum_changes': cost, 'optimal_alignment_count': len(masks)}
        alternatives.append({'unassigned_cell': cell,
                             'coordinate_pair': SYMBOLS[cell // 6] + SYMBOLS[cell % 6],
                             'digit_domain': ''.join(sorted(set(ALPHABET) - set(square))),
                             'source_fits': by_source})
    continuation = []
    for name in ('p151_D2', 'p153_D2', 'p158_C2'):
        literal, masked = raw[name]
        assert len(masked) == records[name]['advertised_length'] == 136
        plain = decrypt(masked, ranks, square)
        domains = plaintext_domains(masked, ranks, square)
        interim = untranspose(masked, ranks)
        assert transpose(interim, ranks) == masked
        continuation.append({'id': name, 'literal_ciphertext': literal,
                             'analysis_ciphertext': masked, 'raw_plaintext': plain,
                             'fixed_positions': sum(len(d) == 1 for d in domains),
                             'plaintext_positions': len(plain), 'domains': domains,
                             'unknown_position': 9, 'unknown_pair': interim[18:20],
                             'source_coordinates_changed': 0})
    assert continuation[-1]['raw_plaintext'] == 'GRUKONACH?02BENACHRICHTIGENEINTREFFENHIERHERDRAHTENXNACHRCHEF4B49909'
    assert all(row['unknown_pair'] == 'VF' and row['domains'][9] == '56' for row in continuation)
    context_path = ROOT / 'experiments/p170_continuation/military_context.json'
    context = json.loads(context_path.read_text())
    assert context['base_key_id'] == key['id']
    assert context['published_partial_square'] == square
    assert context['column_rank_order'] == ranks
    assert context['contextual_cell_assignments'] == {'VF': '6', 'XA': '5'}
    contextual_square = context['contextual_square']
    assert contextual_square[26] == '6' and contextual_square[30] == '5'
    assert all(a == b or a == '?' for a, b in zip(square, contextual_square))
    contextual_views = [{
        'id': row['id'], 'base_layer': 'unchanged literal 136-coordinate source',
        'ciphertext': row['analysis_ciphertext'],
        'base_plaintext': row['raw_plaintext'],
        'conditional_plaintext': decrypt(row['analysis_ciphertext'], ranks, contextual_square),
        'newly_fixed_plaintext_position': 9,
        'base_domain': '56', 'coordinate_pair': 'VF', 'conditional_digit': '6',
        'additional_source_coordinate_changes': 0,
    } for row in continuation]
    contextual_views.append({
        'id': 'first_part_editorial_candidate',
        'base_layer': 'explicitly repaired candidate shared by p153 E1 / p162 A1; not the literal source',
        'ciphertext': target, 'base_plaintext': text,
        'conditional_plaintext': decrypt(target, ranks, contextual_square),
        'newly_fixed_plaintext_position': 104,
        'base_domain': '56', 'coordinate_pair': 'VF', 'conditional_digit': '6',
        'additional_source_coordinate_changes': 0,
    })
    return {'schema': 'adfgvx-courier-certificate-v1',
            'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
            'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': 'All positions are zero-based. Alignment counts include aliases from repeated coordinates.',
            'relative_first_part_alignment': {
                'model': 'Insert one consecutive five-slot erasure block into p153; no source deletion or reordering.',
                'positions_tested': len(relative), 'minimum_known_disagreements': minimum,
                'all_optimal_alignments': best_relative},
            'editorial_first_part': {
                'plaintext': text, 'coordinate_stream': stream, 'candidate_ciphertext': target,
                'unassigned_reference_cell': 26, 'unassigned_reference_pair': 'VF',
                'unassigned_reference_digit_domain': '56', 'source_fits': fits,
                'complete_unchanged_pair_support_under_every_minimum_fit': fixed_support,
                'supported_ordinary_or_known_digit_positions': len(fixed_support),
                'plaintext_positions': len(text),
                'one_received_deletion_sensitivity': sensitivity,
                'complete_unchanged_pair_support_across_both_alignment_models': fixed_across_models,
                'supported_positions_across_both_models': len(fixed_across_models),
                'other_unassigned_cell_comparison': alternatives,
                'status': 'Conditional editorial reconstruction. Minimum source cost does not prove the candidate or the geometry.'},
            'direct_continuation_readings': continuation,
            'conditional_context_propagation': {
                'status': 'Consequence of the separately recorded reserve-division identification, not an independent courier digit deduction.',
                'linked_context_certificate': 'experiments/p170_continuation/military_context.json',
                'linked_primary_source_id': 'franchet_1918_11_19',
                'linked_contextual_assignments': context['contextual_cell_assignments'],
                'condition': 'Accept the historical identification of the reserve division in the Nov7-9 military reports as the 6th Reserve Division, and the same correct period square for these courier records.',
                'result': 'VF=6 makes the common field GRUKONACH602 with no additional coordinate changes. Base VF remains {5,6}.',
                'views': contextual_views,
                'limits': ['The French operational source was already used for p176b; the present addition is propagation through the Nov7-9 square.',
                           'The courier records do not independently establish the military identification or validate the unit number from outside evidence.',
                           'The first-part reconstruction and its association with the direct continuation remain separately conditional.']},
            'part_association': {
                'status': 'Supported interpretation, not an explicit source cross-reference.',
                'evidence': ['The two earlier bodies are labelled first part of two; all three closing records are explicitly second parts.',
                             'p153 D and E have the same RVV v N4 header and were intercepted on the same morning.',
                             'The first-part 2120 (SY) routing is consistent with the p151 D SY v N4 closing record.',
                             'Both texts refer to GRUKONACH?02, using the same unassigned VF cell; departure followed by a request to report arrival forms a coherent instruction.']},
            'limitations': ['The parts use the existing Nov7–9 key; no new transposition key or numeral assignment is recovered.',
                            'The first-part candidate includes explicit changes to valid source coordinates and inserted missing slots.',
                            'The four additional missing first-part coordinates are not located by the relative duplicate alignment alone.',
                            'Allowing a source deletion changes the minimum substitution costs and the support count; neither alignment model is established by the source alone.',
                            'Name-like strings GERAUS and MAHRER and the abbreviation FELDGR remain unverified historical identifications.',
                            'The source-supported second part is independent of accepting the first-part reconstruction.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    output = HERE / 'certificate.json'
    if args.verify:
        assert result == json.loads(output.read_text())
    else:
        output.write_text(json.dumps(result, indent=2) + '\n')
    first = result['editorial_first_part']
    print(json.dumps({'verified': args.verify,
        'relative_optimal_alignments': len(result['relative_first_part_alignment']['all_optimal_alignments']),
        'first_part_positions': first['plaintext_positions'],
        'conditional_pair_supported_positions': first['supported_ordinary_or_known_digit_positions'],
        'pair_supported_positions_across_both_models': first['supported_positions_across_both_models'],
        'source_fits': {name: {k: fit[k] for k in ['inserted_slots', 'minimum_known_coordinate_changes', 'optimal_alignment_count']}
                        for name, fit in first['source_fits'].items()},
        'continuation_fixed_positions': result['direct_continuation_readings'][-1]['fixed_positions'],
        'continuation_total_positions': result['direct_continuation_readings'][-1]['plaintext_positions']}, indent=2))


if __name__ == '__main__':
    main()
