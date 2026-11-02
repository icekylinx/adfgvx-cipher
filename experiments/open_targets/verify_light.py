#!/usr/bin/env python3
"""Check frozen open-target arithmetic, source identities and declared bounds.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Standard library only; no binary models, compiler, books, network, or search.
The cipher arithmetic below is independent of adfgvx.cipher. The check does
not rerun the optimizers or rebuild reference-corpus covariance statistics.
"""
from pathlib import Path
import argparse, hashlib, json, math, struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDS = 'ADFGVX'


def read(name):
    return json.loads((HERE / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def ranks_ok(ranks):
    assert sorted(ranks) == list(range(1, len(ranks)+1))


def square_ok(square, complete=False):
    assert len(square) == 36 and set(square) <= set(LETTERS + '?')
    filled = square.replace('?', '')
    assert len(filled) == len(set(filled))
    if complete:
        assert set(square) == set(LETTERS)


def untranspose(ciphertext, ranks):
    ranks_ok(ranks)
    width = len(ranks)
    stream = ['?'] * len(ciphertext)
    at = 0
    for col in sorted(range(width), key=lambda c: ranks[c]):
        positions = list(range(col, len(ciphertext), width))
        for pos in positions:
            stream[pos] = ciphertext[at]
            at += 1
    assert at == len(ciphertext)
    return ''.join(stream)


def transpose(stream, ranks):
    ranks_ok(ranks)
    return ''.join(stream[col::len(ranks)] for col in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def encrypt(plaintext, ranks, square):
    square_ok(square, True)
    assert set(plaintext) <= set(LETTERS)
    return transpose(''.join(COORDS[square.index(ch)//6]+COORDS[square.index(ch)%6] for ch in plaintext), ranks)


def decode(ciphertext, ranks, square):
    square_ok(square)
    stream = untranspose(ciphertext, ranks)
    assert len(stream) % 2 == 0 and transpose(stream, ranks) == ciphertext
    unused = set(LETTERS)-set(square)
    plaintext, domains = [], []
    for first, second in zip(stream[::2], stream[1::2]):
        cells = [i for i in range(36)
                 if (first not in COORDS or COORDS[i//6] == first)
                 and (second not in COORDS or COORDS[i%6] == second)]
        possible = set()
        for cell in cells:
            possible.update(unused if square[cell] == '?' else [square[cell]])
        assert possible
        domains.append(''.join(sorted(possible)))
        plaintext.append(square[cells[0]] if len(cells) == 1 else '?')
    return ''.join(plaintext), domains


def anchors(partial, square):
    square_ok(partial)
    square_ok(square)
    assert all(a == '?' or a == b for a, b in zip(partial, square))


def insert_missing(observed, positions, fill=None):
    assert positions == sorted(set(positions))
    assert len(positions) == 5 and 0 <= positions[0] <= positions[-1] < len(observed)+5
    missing = iter(fill or '?'*5)
    source = iter(observed)
    padded = ''.join(next(missing) if i in positions else next(source) for i in range(len(observed)+5))
    assert ''.join(ch for i, ch in enumerate(padded) if i not in positions) == observed
    return padded


def control_stats(truth, domains):
    assert len(truth) == len(domains)
    return dict(truth_in_all_domains=all(ch in d for ch, d in zip(truth, domains)),
                correct_singletons=sum(ch == d for ch, d in zip(truth, domains)),
                singleton_positions=sum(len(d) == 1 for d in domains))


def assert_subset(actual, recorded):
    for key, value in actual.items():
        if key in recorded:
            assert value == recorded[key], (key, value, recorded[key])


def historical_input(case, messages, keys):
    if 'evaluation_only' in case:
        return
    target = case.get('target', case['id'])
    assert case['ciphertext'] == messages[target]['transcript']['analysis_ciphertext']
    key_id = case.get('key_hypothesis', case.get('key_id'))
    anchors(case['partial_square'], keys[key_id]['square'])
    if 'ranks' in case:
        assert case['ranks'] == keys[key_id]['column_rank_order']


def true_fixture(case, kind):
    if 'evaluation_only' not in case:
        return
    ev = case['evaluation_only']
    if kind == 'relabel':
        unused = iter(sorted(set(LETTERS)-set(case['partial_square'])))
        square = ''.join(next(unused) if ch == '?' else ch for ch in case['partial_square'])
        square = effective_square(square, ev)
        ranks = case['ranks']
    else:
        square = ev['square']
        ranks = ev.get('ranks', case.get('ranks'))
    assert encrypt(ev['plaintext'], ranks, square) == ev['full_ciphertext']
    if kind == 'sparse':
        losses = ev['missing_full_ciphertext_positions_0based']
        assert ''.join(ch for i, ch in enumerate(ev['full_ciphertext']) if i not in losses) == case['ciphertext']
    elif case['gap_size']:
        gap = ev.get('gap', ev.get('gap_before_source_0based'))
        assert ev['full_ciphertext'][:gap]+ev['full_ciphertext'][gap+5:] == case['ciphertext']
    else:
        assert all(a not in COORDS or a == b for a, b in zip(case['ciphertext'], ev['full_ciphertext']))


def effective_square(square, candidate):
    rp, cp = candidate['row_relabeling'], candidate['column_relabeling']
    assert sorted(rp) == sorted(cp) == sorted(COORDS)
    swap = candidate['swapped_pair_orientation']
    return ''.join(square[6*COORDS.index(rp[b if swap else a])+COORDS.index(cp[a if swap else b])]
                   for a in range(6) for b in range(6))


def verify_record(row, kind, messages, keys):
    case = row['case']
    historical_input(case, messages, keys)
    true_fixture(case, kind)
    recipe = row['recipe']
    source_name = {'gap': 'gap_anchored.c', 'sparse': 'sparse_loss.c',
                   'transfer': 'group_transfer.c', 'relabel': 'relabel_rows_columns.c'}[kind]
    assert digest(HERE / source_name) == recipe['source_sha256']
    if 'shared_scorer_sha256' in recipe:
        assert digest(HERE / 'gap_anchored.c') == recipe['shared_scorer_sha256']
    if 'input_record_sha256' in row:
        original = {k: v for k, v in row.items() if k not in ['input_record_sha256', 'audit']}
        assert hashlib.sha256((json.dumps(original, indent=2)+'\n').encode()).hexdigest() == row['input_record_sha256']
    source = case['ciphertext']
    if kind == 'relabel':
        for candidate in row['candidates']:
            square = effective_square(case['partial_square'], candidate)
            assert square == candidate['effective_partial_square']
            gap = candidate['gap_before_source_0based']
            assert 0 <= gap <= len(source)
            padded = source[:gap]+'?'*case['gap_size']+source[gap:]
            plaintext, domains = decode(padded, case['ranks'], square)
            assert plaintext == candidate['partial_plaintext']
        gaps = len(range(0, len(source)+1, recipe['gap_step'])) if case['gap_size'] else 1
        assert row['summary']['evaluations'] == gaps*2*math.factorial(6)**2
        best = row['candidates'][0]
        gap = best['gap_before_source_0based']
        _, domains = decode(source[:gap]+'?'*case['gap_size']+source[gap:], case['ranks'], best['effective_partial_square'])
    else:
        best = row['best']
        square_ok(best['square'], True)
        anchors(case['partial_square'], best['square'])
        ranks = best['ranks']
        if kind == 'sparse':
            assert ranks == case['ranks']
            padded = insert_missing(source, best['missing_full_ciphertext_positions_0based'])
        else:
            assert len(ranks) == case['width']
            gap = best['gap_before_source_0based']
            assert 0 <= gap <= len(source)
            inserted = case['inserted_group'] if kind == 'transfer' else '?'*5
            padded = source[:gap]+inserted+source[gap:]
            assert padded[:gap]+padded[gap+5:] == source
        plaintext, domains = decode(padded, ranks, best['square'])
        assert plaintext == best['plaintext']
        if kind == 'transfer':
            assert encrypt(plaintext, ranks, best['square']) == padded
        else:
            assert domains == row['verification']['plaintext_domains']
            witness = encrypt(''.join(d[0] for d in domains), ranks, best['square'])
            assert all(a not in COORDS or a == b for a, b in zip(padded, witness))
    audit = row.get('audit', row['verification'])
    if 'plaintext_domains' in audit:
        assert domains == audit['plaintext_domains']
    if 'evaluation_only' in case:
        ev = case['evaluation_only']
        assert_subset(control_stats(ev['plaintext'], domains), audit['control'])
        if kind == 'transfer':
            assert audit['control']['exact_plaintext'] == (plaintext == ev['plaintext'])
            assert audit['control']['exact_ranks'] == (ranks == ev['ranks'])
            valid = [g for g in range(len(source)+1)
                     if ev['full_ciphertext'][g:g+5] == case['inserted_group']
                     and ev['full_ciphertext'][:g]+ev['full_ciphertext'][g+5:] == source]
            assert valid == audit['control']['all_source_equivalent_true_group_positions']
        if kind in ['gap', 'transfer', 'relabel']:
            aliases = [g for g in range(len(source)+1)
                       if ev['full_ciphertext'][:g]+ev['full_ciphertext'][g+case['gap_size']:] == source] if case['gap_size'] else [0]
            if 'all_source_equivalent_true_gap_positions' in audit['control']:
                assert aliases == audit['control']['all_source_equivalent_true_gap_positions']
        if kind == 'sparse' and 'reported_losses_reproduce_source_under_true_key' in audit['control']:
            losses = best['missing_full_ciphertext_positions_0based']
            same = ''.join(ch for i, ch in enumerate(ev['full_ciphertext']) if i not in losses) == source
            assert same == audit['control']['reported_losses_reproduce_source_under_true_key']


def snapshot(kind, messages, keys):
    data = read(kind+'_results.json')
    assert data['kind'] == kind
    for row in data['records']:
        verify_record(row, kind, messages, keys)
    historic = [r for r in data['records'] if 'evaluation_only' not in r['case']]
    summary = data['summary']
    assert summary['completed_historical_runs'] == len(historic)
    assert summary['unique_historical_cases'] == len({r['case']['id'] for r in historic})
    assert summary['completed_controls'] == len(data['records'])-len(historic)
    assert summary['historical_configured_proposal_slots'] == sum(r['recipe'].get('restarts', 0)*r['recipe'].get('iterations', 0) for r in historic)
    assert summary['historical_exact_evaluations'] == sum(r.get('summary', {}).get('evaluations', 0) for r in historic)
    expected = {'gap': (63, 54, 3, 1170000000, 0), 'sparse': (24, 24, 3, 120000000, 0),
                'transfer': (54, 54, 3, 5400000000, 0), 'relabel': (72, 72, 3, 0, 4180377600)}[kind]
    assert tuple(summary[k] for k in ['completed_historical_runs', 'unique_historical_cases', 'completed_controls',
                                     'historical_configured_proposal_slots', 'historical_exact_evaluations']) == expected
    assert summary['accepted_historical_plaintexts'] == 0
    return {k: v for k, v in summary.items() if k != 'control_evaluations'}


def verify_anchored(messages, keys):
    data = read('anchored_snapshot.json')
    assert data['completed_historical_cases'] == data['planned_historical_cases'] == len(data['historical_records']) == 70
    combinations = set()
    for item in data['historical_records']:
        row = item['record']
        case, best = row['case'], row['best']
        historical_input(case, messages, keys)
        anchors(case['partial_square'], best['square'])
        square_ok(best['square'], True)
        plaintext, domains = decode(case['ciphertext'], best['ranks'], best['square'])
        assert plaintext == best['plaintexts'][0] and domains == row['domains']
        assert row['requested_restarts'] == 1000 and row['iterations_per_restart'] == 100000
        combinations.add((case['id'], case['key_id'], case['width']))
    assert len(combinations) == 70
    targets = {c[0] for c in combinations}
    tables = {c[1] for c in combinations}
    assert targets == {'p73', 'p170'} and len(tables) == 5
    assert combinations == {(t, k, w) for t in targets for k in tables for w in range(16, 23)}
    return dict(historical_cases=70, configured_proposal_slots=7000000000)


def verify_structure(messages, keys):
    data = read('structure_results.json')
    assert digest(HERE/'segment_gap.c') == data['segment_source_sha256']
    assert digest(HERE/'refine_segments.c') == data['refine_source_sha256']
    total, history, controls = 0, 0, 0
    for row in data['records']:
        case = row['case']
        historical_input(case, messages, keys)
        true_fixture(case, 'gap')
        source, width = case['ciphertext'], case['width']
        count = (len(source)+1)*math.comb(width, (len(source)+5) % width)
        assert row['segmentation_summary']['enumerated_gap_segmentations'] == count
        if 'evaluation_only' not in case:
            total += count
            history += 1
        else:
            controls += 1
        for candidate in row['segmentation_leaders']:
            ranks_ok(candidate['ranks'])
            assert candidate['long_mask'] == sum(1 << (r-1) for r in candidate['ranks'][:170 % width])
        for candidate in row['refined_candidates']:
            gap = candidate['gap_before_source_0based']
            assert 0 <= gap <= len(source)
            plaintext, domains = decode(source[:gap]+'?'*5+source[gap:], candidate['ranks'], case['partial_square'])
            assert plaintext == candidate['partial_plaintext']
        if 'evaluation_only' in case:
            best = row['refined_candidates'][0]
            gap = best['gap_before_source_0based']
            padded = source[:gap]+'?'*5+source[gap:]
            _, domains = decode(padded, best['ranks'], case['partial_square'])
            control = row['verification']['control']
            statistics = control_stats(case['evaluation_only']['plaintext'], domains)
            assert statistics['truth_in_all_domains'] == control['truth_in_all_positionwise_domains']
            assert_subset(statistics, control)
            # A published successful global witness can be checked directly.
            fit = control['global_truth_feasibility']
            if fit['compatible']:
                anchors(case['partial_square'], fit['completion_witness'])
                encrypted = encrypt(case['evaluation_only']['plaintext'], best['ranks'], fit['completion_witness'])
                assert all(a not in COORDS or a == b for a, b in zip(padded, encrypted))
            else:
                stream = untranspose(padded, best['ranks'])
                unknown = {i for i, ch in enumerate(case['partial_square']) if ch == '?'}
                allowed = {ch: {case['partial_square'].index(ch)} if ch in case['partial_square'] else set(unknown) for ch in LETTERS}
                for ch, a, b in zip(case['evaluation_only']['plaintext'], stream[::2], stream[1::2]):
                    allowed[ch] &= {i for i in range(36) if (a not in COORDS or COORDS[i//6] == a) and (b not in COORDS or COORDS[i%6] == b)}
                assert [ch for ch in LETTERS if not allowed[ch]] == fit['empty_character_domains']
                assert fit['empty_character_domains']
    assert (history, controls, total) == (24, 2, 235666548)
    small = read('structural_small_verification.json')
    assert small['verified'] and small['exhausted_keys_and_gaps'] == 64*math.factorial(6)
    assert small['geometry_classes'] == 64*math.comb(6, 2)
    return dict(historical_cases=history, controls=controls, exact_geometry_classes=total,
                small_exhaustion_metadata_consistent=True)


def verify_direct(messages, keys):
    data = read('direct_transfer_result.json')
    inputs = data['inputs']
    assert inputs['ciphertext'] == messages['p198']['transcript']['analysis_ciphertext']
    assert inputs['inserted_group'] == 'XAXVV'
    records = []
    for key in inputs['keys']:
        anchors(key['square'], keys[key['id']]['square'])
        assert key['ranks'] == keys[key['id']]['column_rank_order']
        for gap in range(166):
            ciphertext = inputs['ciphertext'][:gap]+'XAXVV'+inputs['ciphertext'][gap:]
            plaintext, _ = decode(ciphertext, key['ranks'], key['square'])
            records.append(dict(key_id=key['id'], gap_before_source_0based=gap, partial_plaintext=plaintext))
    assert len(records) == data['evaluated_cases'] == 3984
    assert canonical(records) == data['canonical_arithmetic_records_sha256']
    return dict(exhaustive_fixed_key_insertions=len(records), arithmetic_digest_verified=True)


def verify_component():
    data = read('component_controls.json')
    fixture = data['fixture']
    assert encrypt(fixture['body'], fixture['ranks'], fixture['square']) == fixture['full_ciphertext']
    assert fixture['ciphertext'] == fixture['full_ciphertext'][:1]+'??'+fixture['full_ciphertext'][3:]
    checks = read('component_verification.json')['checks']
    for row, check in zip(data['runs'], checks):
        assert digest(ROOT / row['engine_source']) == row['source_sha256']
        n, k = len(fixture['ciphertext']), fixture['width']
        def lengths(ranks):
            return [n//k+(c < n % k) for c in sorted(range(k), key=lambda c: ranks[c])]
        assert lengths(row['initial_ranks']) == lengths(row['best']['ranks']) == lengths(fixture['ranks'])
        plaintext, domains = decode(fixture['ciphertext'], row['best']['ranks'], row['best']['square'])
        assert plaintext == row['best']['plaintexts'][0]
        assert_subset(control_stats(fixture['body'], domains), check)
        assert not check['true_plaintext_in_all_domains']
    assert [r['correct_singletons'] for r in checks] == [11, 8]
    return dict(controls=2, correct_singletons=[11, 8], singleton_positions=87,
                historical_search_launched=False)


def verify_histogram(messages, keys):
    data = read('p73_histogram_result.json')
    assert data['key_id'] == 'Nov7-9'
    anchors(data['partial_square'], keys['Nov7-9']['square'])
    sources = read('heldout_sources.json')['sources']
    assert data['heldout_sources'] == sources
    training = json.loads((ROOT/'experiments/joint_search/models/provenance.json').read_text())['sources']
    assert not {s['id'] for s in sources} & {s['id'] for s in training}
    inputs = {r['id']: r for r in data['inputs']}
    assert inputs['p73']['literal'] == messages['p73']['transcript']['raw_source_compact']
    companion = json.loads((ROOT/'data/certificates/p155.json').read_text())['sections'][0]
    assert inputs['p155_A1']['literal'] == companion['raw_literal']
    for row in inputs.values():
        assert row['known_coordinate_counts'] == [row['literal'].count(c) for c in COORDS]
        assert row['unknown_slots'] == len(row['literal'])-sum(row['known_coordinate_counts'])
        assert row['plaintext_length']*2 == len(row['literal'])
    partial = data['partial_square']
    ordinary = ''.join(sorted(ch for i, ch in enumerate(partial) if ch in LETTERS[:26] and (i//6 == 2 or i % 6 == 2)))
    assert ordinary == 'CJMOQZ'
    assert partial[14] == '7' and inputs['p73']['known_coordinate_counts'][2] == 26
    inv = data['exact_F_invariant']
    assert inv['minimum_characters_from_CJMOQZ_or_digits'] == math.ceil(26/2) == 13
    assert inv['minimum_CJMOQZ_characters_if_digit_free'] == 26
    assert all(not (i//6 == i % 6 == 2) for i, ch in enumerate(partial) if ch in LETTERS[:26])
    v_inv = data['exact_V_invariant']
    v_weights = {ch: int(i//6 == 4)+int(i % 6 == 4) for i, ch in enumerate(partial)
                 if ch in LETTERS[:26] and (i//6 == 4 or i % 6 == 4)}
    assert set(v_weights) == set('DEHKQTUX') and v_weights['X'] == 2
    assert all(weight == 1 for ch, weight in v_weights.items() if ch != 'X')
    assert v_inv['ordinary_letter_V_coefficients'] == v_weights
    assert v_inv['observed_V_count'] == inputs['p73']['known_coordinate_counts'][4] == 15
    assert v_inv['unknown_coordinate_slots'] == inputs['p73']['unknown_slots'] == 2
    v_max = v_inv['observed_V_count']+v_inv['unknown_coordinate_slots']
    assert v_inv['maximum_completed_V_count'] == v_max == 17
    assert v_inv['maximum_encoded_X_characters'] == v_max//2 == 8
    assert v_inv['maximum_DEHKQTU_characters_if_five_X'] == v_max-10 == 7
    streams = {(r['book_id'], r['convention']): r for r in data['normalized_streams']}
    assert len(data['results']) == 24
    for row in data['results']:
        target = inputs[row['target_id']]
        assert row['reference_windows'] == streams[row['book_id'], row['convention']]['normalized_characters']//target['plaintext_length']
        assert row['window_stride'] == target['plaintext_length']
        assert row['empirical_reference_fraction'] == row['reference_windows_at_least_as_distant']/row['reference_windows']
        assert set(row['unknown_digit_order']) == {'5', '6'}
        square_ok(row['square_completion_for_reference_encoding_only'], True)
        anchors(partial, row['square_completion_for_reference_encoding_only'])
        for histogram, addition in zip(row['most_favorable_completed_histograms'], row['most_favorable_erasure_additions']):
            assert all(v >= 0 and isinstance(v, int) for v in addition)
            assert sum(addition) == target['unknown_slots']
            assert histogram == [a+b for a, b in zip(target['known_coordinate_counts'], addition)]
        if row['reference_windows_at_least_as_distant'] == 0:
            assert row['squared_mahalanobis_distance'] > row['reference_distance_quantiles']['1.0']
        if row['target_id'] == 'p73' or row['convention'] == 'word_x':
            assert row['reference_windows_at_least_as_distant'] == 0
        else:
            assert row['reference_windows_at_least_as_distant'] > 0
    return dict(source_histograms_verified=2, F_category_lower_bound=13, digit_free_CJMOQZ_lower_bound=26,
                maximum_ordinary_V_weighted_count=17, maximum_encoded_X_characters=8,
                maximum_DEHKQTU_characters_if_five_X=7,
                frozen_empirical_rows_consistent=24, corpus_statistics_rebuilt=False)


def verify_heldout_scores():
    data = read('heldout_control_scores.json')
    inputs = read('joint_control_inputs.json')
    assert data['inputs_sha256'] == digest(HERE/'joint_control_inputs.json')
    texts = {}
    for case in inputs['cases']:
        ranks, square = case['column_rank_order'], case['square']
        truth = case['planted']
        assert encrypt(truth['plaintext'], ranks, square) == truth['full_ciphertext']
        assert ''.join(ch for i, ch in enumerate(truth['full_ciphertext']) if i not in truth['missing_full_ciphertext_positions_0based']) == case['observed_ciphertext']
        optimum = case['joint_quad_optimum']
        padded = insert_missing(case['observed_ciphertext'], optimum['missing_full_ciphertext_positions'], optimum['filled_missing_coordinates'])
        plaintext, _ = decode(padded, ranks, square)
        assert encrypt(plaintext, ranks, square) == padded
        texts['planted'] = truth['plaintext']
        texts[case['id']+'_wrong_joint_optimum'] = plaintext
    assert texts == data['texts']
    f32 = lambda value: struct.unpack('<f', struct.pack('<f', value))[0]
    for row in data['results']:
        for name, n in [('quad', 4), ('six', 6)]:
            table = row[name]
            counts, total = table['relevant_gram_counts'], table['weighted_gram_total']
            assert f32(math.log10(.01/total)) == table['unseen_log10_float32']
            for label, text in texts.items():
                score = sum(f32(math.log10((counts[text[i:i+n]] or .01)/total)) for i in range(len(text)-n+1))/(len(text)-n+1)
                assert abs(score-table['mean_log10_scores'][label]) < 1e-12
            for label, delta in table['wrong_minus_planted'].items():
                assert abs(table['mean_log10_scores'][label]-table['mean_log10_scores']['planted']-delta) < 1e-12
        for label in texts:
            mixed = .3*row['quad']['mean_log10_scores'][label]+.7*row['six']['mean_log10_scores'][label]
            assert abs(mixed-row['mixed_30_70_scores'][label]) < 1e-12
        for label, delta in row['mixed_wrong_minus_planted'].items():
            assert abs(row['mixed_30_70_scores'][label]-row['mixed_30_70_scores']['planted']-delta) < 1e-12
    assert len(data['results']) == 8
    return dict(heldout_models=16, compared_texts=3, selected_gram_scores_recomputed=True,
                complete_book_counts_rebuilt=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    messages = {m['id']: m for m in json.loads((ROOT/'data/messages.json').read_text())['messages']}
    keys = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    checks = {'anchored': verify_anchored(messages, keys)}
    for kind in ['gap', 'sparse', 'transfer', 'relabel']:
        checks[kind] = snapshot(kind, messages, keys)
    checks['structure'] = verify_structure(messages, keys)
    checks['direct_transfer'] = verify_direct(messages, keys)
    checks['component_controls'] = verify_component()
    unknown = read('unknown_square_control.json')
    verify_record(unknown, 'sparse', messages, keys)
    assert unknown['verification']['control']['correct_singletons'] == 49
    checks['unknown_square_control'] = dict(correct_singletons=49, singleton_positions=80, historical_search_launched=False)
    checks['p73_histogram'] = verify_histogram(messages, keys)
    checks['heldout_control_scores'] = verify_heldout_scores()
    result = dict(verified=True, project='ADFGVX Cipher', review_credit='icekylinx and GPT-6 Astra Pro',
                  checks=checks,
                  limits=['Searches and dynamic programs are not rerun by this lightweight check.',
                          'Binary-model language scores and held-out covariance statistics require the documented full replay.',
                          'Source preservation and score arithmetic do not establish a historical decipherment.'])
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
