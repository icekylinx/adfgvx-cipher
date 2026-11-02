#!/usr/bin/env python3
"""Independently audit the courier source/candidate certificate.

Uses only the Python standard library. Neither the builder nor the project's
cipher implementation is imported. This verifies the stated candidate and
alignment models; it does not establish an uncorrupted historical plaintext.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDINATES = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def layout(length, ranks):
    """Cipher position -> row-wise coordinate position."""
    width = len(ranks)
    return [position for column in sorted(range(width), key=ranks.__getitem__)
            for position in range(column, length, width)]


def decipher(ciphertext, ranks, square):
    stream = ['?'] * len(ciphertext)
    for value, position in zip(ciphertext, layout(len(ciphertext), ranks)):
        stream[position] = value
    domains = []
    absent = ''.join(sorted(set(ALPHABET) - set(square)))
    for offset in range(0, len(stream), 2):
        values = set()
        for row in range(6):
            for column in range(6):
                if (stream[offset] in ('?', COORDINATES[row]) and
                        stream[offset + 1] in ('?', COORDINATES[column])):
                    char = square[6 * row + column]
                    values.update(absent if char == '?' else char)
        domains.append(''.join(sorted(values)))
    return ''.join(d if len(d) == 1 else '?' for d in domains), domains, ''.join(stream)


def minimum_and_count(observed, target):
    """Forward grid DP, independent of the builder's missing-slot recurrence."""
    n, m = len(observed), len(target)
    gap = m - n
    assert gap >= 0
    # A state records consumed observed and target slots. Advancing only the
    # target inserts a missing coordinate; advancing both retains a source
    # coordinate and charges a known mismatch.
    states = {(0, 0): (0, 1)}

    def extend(state, cost, count):
        old = states.get(state)
        if old is None or cost < old[0]:
            states[state] = cost, count
        elif cost == old[0]:
            states[state] = cost, old[1] + count

    for consumed in range(n + 1):
        for filled in range(consumed, min(consumed + gap, m) + 1):
            state = states.get((consumed, filled))
            if state is None:
                continue
            cost, count = state
            if filled < m and filled - consumed < gap:
                extend((consumed, filled + 1), cost, count)
            if consumed < n and filled < m:
                extra = observed[consumed] not in ('?', target[filled])
                extend((consumed + 1, filled + 1), cost + extra, count)
    return states[n, m]


def inspect_alignment(observed, target, missing, ranks):
    assert missing == sorted(set(missing))
    assert len(missing) == len(target) - len(observed)
    assert all(0 <= p < len(target) for p in missing)
    gaps = set(missing)
    frame, changes, fills = [], [], []
    source_index = 0
    for target_index, desired in enumerate(target):
        if target_index in gaps:
            frame.append('?')
            continue
        actual = observed[source_index]
        frame.append(actual)
        if actual == '?':
            fills.append({'source_index': source_index, 'target_index': target_index,
                          'proposed': desired})
        elif actual != desired:
            changes.append({'source_index': source_index, 'target_index': target_index,
                            'source': actual, 'proposed': desired})
        source_index += 1
    assert source_index == len(observed)
    inverse = {plain: cipher for cipher, plain in enumerate(layout(len(target), ranks))}
    supported = {position for position in range(len(target) // 2)
                 if all(frame[inverse[2 * position + shift]] == target[inverse[2 * position + shift]]
                        for shift in (0, 1))}
    return ''.join(frame), changes, fills, supported


def main():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    proof = json.loads((HERE / 'certificate.json').read_text())
    assert proof['input_sha256'] == digest(HERE / 'inputs.json')
    assert inputs['authors'] == proof['authors'] == 'icekylinx and GPT-6 Astra Pro'
    for source in inputs['source_images']:
        assert digest(HERE / source['path']) == source['sha256']
    key = inputs['key_snapshot']
    catalogue = json.loads((ROOT / 'data/keys.json').read_text())['keys']
    assert key == next(row for row in catalogue if row['id'] == key['id'])
    ranks, square = key['column_rank_order'], key['square']
    records = {row['id']: row for row in inputs['records']}
    literal, observed = {}, {}
    for name, record in records.items():
        literal[name] = ''.join(''.join(record['source_rows']).split())
        assert set(literal[name]) <= set(COORDINATES)
        observed[name] = ''.join('?' if i in record['uncertain_source_indices'] else char
                                 for i, char in enumerate(literal[name]))
    short, long = observed['p153_E1'], observed['p162_A1']
    assert (len(short), len(long)) == (259, 264)
    trials = []
    for offset in range(len(short) + 1):
        padded = short[:offset] + '?????' + short[offset:]
        conflicts = [i for i, (a, b) in enumerate(zip(padded, long))
                     if '?' not in (a, b) and a != b]
        trials.append({'gap_before_p153_source_index': offset,
                       'known_coordinate_disagreements': conflicts,
                       'disagreement_count': len(conflicts)})
    minimum = min(row['disagreement_count'] for row in trials)
    relative = proof['relative_first_part_alignment']
    assert relative['positions_tested'] == len(trials)
    assert relative['minimum_known_disagreements'] == minimum == 2
    assert relative['all_optimal_alignments'] == [row for row in trials if row['disagreement_count'] == minimum]

    first = proof['editorial_first_part']
    plaintext = inputs['first_part_candidate']['plaintext']
    assert plaintext == first['plaintext'] and len(plaintext) == 134
    cells = [26 if char == '?' else square.index(char) for char in plaintext]
    stream = ''.join(COORDINATES[cell // 6] + COORDINATES[cell % 6] for cell in cells)
    target = ''.join(stream[i] for i in layout(len(stream), ranks))
    assert stream == first['coordinate_stream']
    assert target == first['candidate_ciphertext']
    assert decipher(target, ranks, square)[0] == plaintext
    stable = {}
    across_models = {}
    for name, fit in first['source_fits'].items():
        source = observed[name]
        cost, count = minimum_and_count(source, target)
        assert cost == fit['minimum_known_coordinate_changes']
        assert count == fit['optimal_alignment_count'] == len(fit['optimal_alignments'])
        assert fit['inserted_slots'] == len(target) - len(source)
        assert fit['deleted_source_slots'] == 0
        seen = set()
        common = set(range(len(plaintext)))
        for alignment in fit['optimal_alignments']:
            missing = alignment['missing_target_positions']
            assert tuple(missing) not in seen
            seen.add(tuple(missing))
            frame, changes, fills, supported = inspect_alignment(source, target, missing, ranks)
            assert len(changes) == cost
            assert changes == alignment['known_coordinate_changes']
            assert fills == alignment['source_erasure_fills_required_by_candidate']
            assert frame == alignment['source_preserving_masked_frame']
            assert ''.join(target[i] for i in missing) == alignment['missing_values_required_by_editorial_candidate']
            assert decipher(frame, ranks, square)[0] == alignment['raw_plaintext_before_fills_or_changes']
            assert sorted(supported) == alignment['candidate_positions_with_complete_unchanged_pair']
            common &= supported
        assert sorted(common) == fit['candidate_positions_with_unchanged_pair_in_every_optimum']
        stable[name] = common

        sensitivity = first['one_received_deletion_sensitivity'][name]
        deletion_trials = []
        for deleted in range(len(source)):
            shortened = source[:deleted] + source[deleted + 1:]
            sub_cost, sub_count = minimum_and_count(shortened, target)
            deletion_trials.append({'deleted_source_index': deleted,
                                    'deleted_source_coordinate': source[deleted],
                                    'minimum_known_coordinate_changes': sub_cost,
                                    'optimal_alignment_count': sub_count})
        assert deletion_trials == sensitivity['all_deletion_trials']
        best = min(row['minimum_known_coordinate_changes'] for row in deletion_trials)
        assert best == sensitivity['minimum_known_coordinate_changes']
        optimum_trials = [row for row in deletion_trials if row['minimum_known_coordinate_changes'] == best]
        sensitivity_common = set(range(len(plaintext)))
        assert len(optimum_trials) == len(sensitivity['all_optimal_deletion_choices'])
        for trial, alignment_set in zip(optimum_trials, sensitivity['all_optimal_deletion_choices']):
            assert all(alignment_set[k] == v for k, v in trial.items())
            deleted = trial['deleted_source_index']
            shortened = source[:deleted] + source[deleted + 1:]
            masks = alignment_set['all_optimal_missing_target_positions']
            assert len(masks) == trial['optimal_alignment_count']
            assert len({tuple(mask) for mask in masks}) == len(masks)
            for missing in masks:
                _, changes, _, supported = inspect_alignment(shortened, target, missing, ranks)
                assert len(changes) == best
                sensitivity_common &= supported
        assert sorted(sensitivity_common) == sensitivity['candidate_positions_with_unchanged_pair_in_every_optimum']
        assert sum(row['optimal_alignment_count'] for row in optimum_trials) == sensitivity['optimal_alignment_count']
        across_models[name] = common & sensitivity_common
    fixed = sorted(i for i in set.union(*stable.values()) if plaintext[i] != '?')
    both = sorted(i for i in set.union(*across_models.values()) if plaintext[i] != '?')
    assert fixed == first['complete_unchanged_pair_support_under_every_minimum_fit']
    assert both == first['complete_unchanged_pair_support_across_both_alignment_models']
    assert len(fixed) == first['supported_ordinary_or_known_digit_positions'] == 123
    assert len(both) == first['supported_positions_across_both_models'] == 118
    for completion in first['other_unassigned_cell_comparison']:
        cell = completion['unassigned_cell']
        assert square[cell] == '?'
        replaced = list(stream)
        replaced[208:210] = [COORDINATES[cell // 6], COORDINATES[cell % 6]]
        cipher = ''.join(replaced[i] for i in layout(len(replaced), ranks))
        for name, comparison in completion['source_fits'].items():
            assert minimum_and_count(observed[name], cipher) == (comparison['minimum_changes'], comparison['optimal_alignment_count'])

    for continuation in proof['direct_continuation_readings']:
        name = continuation['id']
        assert literal[name] == continuation['literal_ciphertext']
        assert observed[name] == continuation['analysis_ciphertext']
        assert len(observed[name]) == records[name]['advertised_length'] == 136
        text, domains, coordinate_stream = decipher(observed[name], ranks, square)
        assert text == continuation['raw_plaintext']
        assert domains == continuation['domains']
        assert continuation['fixed_positions'] == sum(len(x) == 1 for x in domains) == 67
        assert continuation['plaintext_positions'] == len(text) == 68
        assert coordinate_stream[18:20] == continuation['unknown_pair'] == 'VF'
        assert domains[9] == '56'
        assert continuation['source_coordinates_changed'] == 0
        assert ''.join(coordinate_stream[i] for i in layout(len(coordinate_stream), ranks)) == observed[name]
    propagation = proof['conditional_context_propagation']
    context = json.loads((ROOT / propagation['linked_context_certificate']).read_text())
    assert context['base_key_id'] == key['id']
    assert context['published_partial_square'] == square
    assert context['column_rank_order'] == ranks
    assert context['contextual_cell_assignments'] == propagation['linked_contextual_assignments'] == {'VF': '6', 'XA': '5'}
    assert any(row['id'] == propagation['linked_primary_source_id'] for row in context['sources'])
    completed = list(square)
    completed[26], completed[30] = '6', '5'
    completed = ''.join(completed)
    assert completed == context['contextual_square']
    assert len(propagation['views']) == 4
    for view in propagation['views']:
        name = view['id']
        source = target if name == 'first_part_editorial_candidate' else observed[name]
        assert source == view['ciphertext']
        assert decipher(source, ranks, square)[0] == view['base_plaintext']
        conditioned = decipher(source, ranks, completed)[0]
        assert conditioned == view['conditional_plaintext']
        changed = [i for i, (a, b) in enumerate(zip(view['base_plaintext'], conditioned)) if a != b]
        assert changed == [view['newly_fixed_plaintext_position']]
        assert conditioned[changed[0]] == view['conditional_digit'] == '6'
        assert view['base_domain'] == '56' and view['coordinate_pair'] == 'VF'
        assert view['additional_source_coordinate_changes'] == 0
        encoded = ''.join(COORDINATES[completed.index(char) // 6] + COORDINATES[completed.index(char) % 6]
                          for char in conditioned)
        assert ''.join(encoded[i] for i in layout(len(encoded), ranks)) == source
    print(json.dumps({'verified_independently': True, 'source_records': len(records),
                      'conditional_first_part_pair_support': len(fixed),
                      'conditional_support_across_both_models': len(both),
                      'first_part_positions': len(plaintext),
                      'direct_continuation': '67/68 positions fixed; VF remains 5 or 6',
                      'linked_conditional_consequence': 'VF=6 gives GRUKONACH602 in four displayed frames; zero additional coordinate edits'}, indent=2))


if __name__ == '__main__':
    main()
