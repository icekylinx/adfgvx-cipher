#!/usr/bin/env python3
"""Verify the frozen p170 column-family scope, source contracts and exact controls.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt, plaintext_domains
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.verify_childs_material_coverage import quantify, read, record, literal

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
C = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(domain):
    return sum(1 << A.index(c) for c in domain)


def emitted(length, ranks):
    return [p for col in sorted(range(len(ranks)), key=lambda c: ranks[c])
            for p in range(col, length, len(ranks))]


def check_match(row, text, square, source, budget):
    ranks = row['ranks']
    assert sorted(ranks) == list(range(1, row['width'] + 1))
    order = sorted(range(len(ranks)), key=lambda c: ranks[c])
    assert order == row['full_column_order']
    used = row['used_columns']
    assert len(set(used)) == len(used) and order[:len(used)] == used
    cipher = encrypt(text, ranks, square)
    assert len(cipher) == row['full_length'] == len(text) * 2
    start = row['observed_offset']
    assert 0 <= start < len(range(used[0], len(cipher), row['width']))
    observed = cipher[start:start + len(source)]
    assert len(observed) == len(source)
    mismatches = [i for i, (a, b) in enumerate(zip(source, observed)) if a != b]
    assert len(mismatches) <= budget
    if 'cost' in row:
        assert len(mismatches) == row['cost']
        assert mismatches == row['mismatch_source_indices']
    else:
        assert not mismatches
    return emitted(len(cipher), ranks)[start:start + len(source)]


def domain_match(row, domains, source, square, support):
    text = row['joint_witness_plaintext']
    remaining = row['remaining_plaintext_domains']
    assert len(text) == len(domains) == len(remaining)
    for char, original, current in zip(text, domains, remaining):
        assert current and current & ~mask(original) == 0
        assert current & (1 << A.index(char))
    indices = check_match(row, text, square, source, 0)
    count = sum(len(domains[p // 2]) == 1 for p in indices)
    assert count == row['directly_fixed_coordinate_support'] >= support
    assert len(source) - count == row['coordinates_relying_on_partial_donor_domains']
    return text


def summaries(text):
    tokens = text.split()
    assert len(tokens) == 8
    return {tokens[i]: int(tokens[i + 1]) for i in range(0, 8, 2)}


def build(pdf=None, replay=False):
    data = json.loads((HERE / 'inputs.json').read_text())
    controls = json.loads((HERE / 'controls.json').read_text())
    registry = {k['id']: k for k in read('data/keys.json')['keys']}
    assert data['authors'] == 'icekylinx and GPT-6 Astra Pro'
    target = data['target']
    source = ''.join(''.join(target['source_rows']).split())
    assert source == target['literal_source'] and len(source) == 106
    assert hashlib.sha256(source.encode()).hexdigest() == target['literal_sha256']
    assert set(source) <= set(C) and target['mask_indices'] == []
    original = next(r for r in read('data/messages.json')['messages'] if r['id'] == 'p170')
    assert source == original['transcript']['raw_source_compact']
    assert original['source']['advertised_length'] is None
    assert original['source']['handwritten_count'] == target['handwritten_count'] == 106
    assert target['transmitted_length_established'] is False
    keys = data['target_square_hypotheses']
    assert len(keys) == 11 and len({k['id'] for k in keys}) == 11
    for key in keys:
        square = key['square']
        baseline = registry[key['registered_key_id']]['square']
        assert len(square) == len(set(square)) == 36 and set(square) == set(A)
        differences = {str(i): c for i, c in enumerate(square) if baseline[i] == '?'}
        assert differences == key['conditional_global_assignment']
        assert all(a == '?' or a == b for a, b in zip(baseline, square))
        if differences:
            assert key['registered_key_id'] == 'Nov7-9'
            assert set(differences) == {'26', '30'} and set(differences.values()) == set('56')
    full, partial = data['complete_donors'], data['partial_donors']
    assert len(full) == 293 and len(partial) == 104
    assert len({r['text'] for r in full}) == len(full)
    for donor in full:
        text = donor['text']
        assert len(text) >= 53 and set(text) <= set(A) and not set(text) <= set(C)
        assert donor['origins']
        for origin, path in donor['origins']:
            assert origin.startswith('experiments/') and '/p170_new_methods/' not in origin
            value = read(origin)
            for part in path:
                value = value[part]
            assert value == text
    partial_domains = []
    for donor in partial:
        key = registry[donor['source_key_id']]
        assert '?' not in key['square'] and len(set(key['square'])) == 36
        native = donor['source_literal']
        assert len(native) == donor['source_slots'] and len(native) % 2 == 0
        frame = ''.join(c if c in C else '?' for c in native)
        domains = plaintext_domains(frame, key['column_rank_order'], key['square'])
        assert sum(len(d) == 1 for d in domains) == donor['raw_fixed_positions']
        assert len(domains) >= 53 and 45 <= donor['raw_fixed_positions'] < len(domains)
        for origin in donor['origins']:
            inputs = read(origin['inputs'])
            assert literal(record(inputs, origin['record_id'])) == native
            assert hashlib.sha256(native.encode()).hexdigest() == origin['native_source_sha256']
            counts = quantify(origin['certificate'], origin['record_id'])
            assert counts['frame_kind'] == 'native_order_and_length'
            assert counts['native_source_slots'] == len(native)
            assert counts['fixed_raw_labels_with_all_unobserved_coordinates_unassigned'] == donor['raw_fixed_positions']
            assert counts['excluded_source_slots'] == counts['added_model_slots'] == 0
        partial_domains.append(domains)
    bounds = data['bounds']
    assert bounds == {'minimum_width': 12, 'maximum_width': 24,
                      'complete_donor_observed_error_budgets': [0, 1, 2],
                      'partial_donor_minimum_direct_coordinate_support': 90,
                      'partial_donor_error_budget': 0}
    for budget, result in data['search_summaries']['complete_donors'].items():
        assert result['projects'] == 293 * 11 * 13 == 41899
        assert result['hits'] == 0 and 0 <= result['histogram_pass'] <= result['projects']
    result = data['search_summaries']['partial_donors']
    assert result['projects'] == 104 * 11 * 13 == 14872 and result['hits'] == 0
    text = controls['synthetic_full_plaintext']
    observed = controls['synthetic_target_observations']
    square = controls['synthetic_target_square']
    assert len(text) == 64 and len(observed) == 106 and len(set(square)) == 36
    for row in controls['complete_exact']['matches']:
        check_match(row, text, square, observed, 0)
    damaged = list(observed)
    for i in controls['complete_damaged']['changed_source_indices']:
        damaged[i] = C[(C.index(damaged[i]) + 1) % 6]
    damaged = ''.join(damaged)
    for result in controls['complete_damaged']['results']:
        assert bool(result['matches']) == (result['budget'] == 2)
        for row in result['matches']:
            check_match(row, text, square, damaged, 2)
    complete_toys = controls['complete_tiny']['cases']
    assert len(complete_toys) == 12
    for toy in complete_toys:
        plain, seen = toy['plaintext'], toy['source']
        best = min(sum(a != b for a, b in zip(seen, encrypt(plain, list(ranks), square)[off:off + len(seen)]))
                   for ranks in itertools.permutations(range(1, 4))
                   for off in range(len(plain) * 2 - len(seen) + 1))
        assert best == toy['independent_bruteforce_minimum']
        assert [r['found'] for r in toy['results']] == [best <= budget for budget in range(3)]
    positive = controls['partial_positive']
    skey = registry[positive['source_key_id']]
    domains = plaintext_domains(positive['source_frame'], skey['column_rank_order'], skey['square'])
    for row in positive['matches']:
        witness = domain_match(row, domains, positive['target_source'], square, 90)
        encoded = encrypt(witness, skey['column_rank_order'], skey['square'])
        assert all(a == '?' or a == b for a, b in zip(positive['source_frame'], encoded))
        # A readable raw stream alone is insufficient: retain all target halves too.
        planted = encrypt(positive['true_plaintext'], row['ranks'], square)
        start = row['observed_offset']
        assert planted[start:start + 106] == positive['target_source']
        assert all(value & (1 << A.index(c)) for c, value in
                   zip(positive['true_plaintext'], row['remaining_plaintext_domains']))
    coupling = controls['partial_coupling']['coupling']
    allowed = coupling['allowed_plaintext']
    assert allowed == skey['square'][:6] == 'YN87PJ'
    pairs = {C[square.index(c) // 6] + C[square.index(c) % 6] for c in allowed}
    assert coupling['positive_pair'] in pairs
    false = coupling['rejected_false_marginal_pair']
    assert false not in pairs and false[0] in {p[0] for p in pairs} and false[1] in {p[1] for p in pairs}
    partial_toys = controls['partial_coupling']['tiny_bruteforce_cases']
    assert len(partial_toys) == 8
    for toy in partial_toys:
        domains = plaintext_domains(toy['source_frame'], [2, 1], skey['square'])
        assert domains == toy['domains']
        exists = False
        for ranks in itertools.permutations(range(1, 4)):
            order = emitted(6, ranks)
            for off in range(3):
                if sum(len(domains[p // 2]) == 1 for p in order[off:off + 4]) < 2:
                    continue
                for chars in itertools.product(*domains):
                    if encrypt(''.join(chars), list(ranks), square)[off:off + 4] == toy['target_source']:
                        exists = True
                        break
                if exists:
                    break
            if exists:
                break
        assert exists == toy['independent_bruteforce_exists'] == toy['found']
    replay_report = None
    if replay:
        replay_report = replay_search(data, controls, partial_domains)
    evidence = verify_source_evidence(pdf, target['original_pdf'], [target['source_image']], HERE)
    certificate = {'schema': 'adfgvx-p170-column-family-followup-certificate-v1',
                   'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
                   'controls_sha256': sha(HERE / 'controls.json'),
                   'code_sha256': {p: sha(HERE / p) for p in
                                   ['column_donor_match.cpp', 'column_domain_match.cpp', 'extract.py', 'verify.py']},
                   'summary': {'p170_observed_coordinates': 106, 'complete_donor_strings': 293,
                               'partial_source_domain_families': 104, 'target_square_hypotheses': 11,
                               'widths_per_donor_square': 13, 'complete_projects_per_budget': 41899,
                               'complete_error_budgets': [0, 1, 2], 'partial_projects': 14872,
                               'partial_minimum_direct_support': 90, 'historical_matches': 0,
                               'complete_tiny_bruteforce_comparisons': 36,
                               'partial_tiny_bruteforce_cases': 8,
                               'joint_original_source_and_target_control_verified': True,
                               'false_independent_half_combination_rejected': True,
                               'accepted_p170_plaintexts': 0},
                   'search_summaries': data['search_summaries'],
                   'limits': data['scope_limits']}
    return certificate, evidence, replay_report


def replay_search(data, controls, partial_domains):
    compiler = shutil.which('c++') or shutil.which('g++')
    if compiler is None:
        raise RuntimeError('--replay requires a C++17 compiler')
    with tempfile.TemporaryDirectory(prefix='adfgvx-p170-columns-') as td:
        tmp = Path(td)
        for name in ['column_donor_match', 'column_domain_match']:
            subprocess.run([compiler, '-O3', '-std=c++17', str(HERE / (name + '.cpp')),
                            '-o', str(tmp / name)], check=True, capture_output=True, text=True)
        def run(engine, keyrows, pool, source, lo, hi, limit):
            (tmp / 'keys').write_text('\n'.join(k['id'] + ' ' + k['square'] for k in keyrows) + '\n')
            (tmp / 'pool').write_text(pool)
            (tmp / 'source').write_text(source + '\n')
            result = subprocess.run([str(tmp / engine), str(tmp / 'keys'), str(tmp / 'pool'),
                                     str(tmp / 'source'), str(lo), str(hi), str(limit)],
                                    check=True, capture_output=True, text=True)
            return [json.loads(line) for line in result.stdout.splitlines()], summaries(result.stderr)
        keys = data['target_square_hypotheses']
        pool = ''.join(str(d['id']) + ' ' + d['text'] + '\n' for d in data['complete_donors'])
        for budget in [0, 1, 2]:
            rows, summary = run('column_donor_match', keys, pool, data['target']['literal_source'], 12, 24, budget)
            assert not rows and summary == data['search_summaries']['complete_donors'][str(budget)]
        partial_pool = ''.join(str(d['id']) + ' ' + str(len(ds)) + ' ' +
                               ' '.join(str(mask(x)) for x in ds) + '\n'
                               for d, ds in zip(data['partial_donors'], partial_domains))
        rows, summary = run('column_domain_match', keys, partial_pool, data['target']['literal_source'], 12, 24, 90)
        assert not rows and summary == data['search_summaries']['partial_donors']
        square = controls['synthetic_target_square']
        key = [{'id': 'Nov7-9-56', 'square': square}]
        plain, seen = controls['synthetic_full_plaintext'], controls['synthetic_target_observations']
        rows, _ = run('column_donor_match', key, 'positive ' + plain + '\n', seen, 20, 20, 0)
        assert rows == controls['complete_exact']['matches']
        damaged = list(seen)
        for i in controls['complete_damaged']['changed_source_indices']:
            damaged[i] = C[(C.index(damaged[i]) + 1) % 6]
        for budget in range(3):
            rows, _ = run('column_donor_match', key, 'positive ' + plain + '\n', ''.join(damaged), 20, 20, budget)
            assert rows == controls['complete_damaged']['results'][budget]['matches']
        for toy in controls['complete_tiny']['cases']:
            for budget in range(3):
                rows, _ = run('column_donor_match', key, 'toy ' + toy['plaintext'] + '\n', toy['source'], 3, 3, budget)
                assert bool(rows) == toy['results'][budget]['found']
                for row in rows:
                    check_match(row, toy['plaintext'], square, toy['source'], budget)
        def domain_pool(domains):
            return 'positive ' + str(len(domains)) + ' ' + ' '.join(str(mask(x)) for x in domains) + '\n'
        positive = controls['partial_positive']
        registry = {k['id']: k for k in read('data/keys.json')['keys']}
        source_key = registry[positive['source_key_id']]
        ds = plaintext_domains(positive['source_frame'], source_key['column_rank_order'], source_key['square'])
        rows, _ = run('column_domain_match', key, domain_pool(ds), positive['target_source'], 20, 20, 90)
        assert rows == positive['matches']
        coupling = controls['partial_coupling']['coupling']
        for pair, expected in [(coupling['positive_pair'], True), (coupling['rejected_false_marginal_pair'], False)]:
            rows, _ = run('column_domain_match', key, domain_pool([coupling['allowed_plaintext']]), pair, 1, 1, 0)
            assert bool(rows) == expected
        for toy in controls['partial_coupling']['tiny_bruteforce_cases']:
            rows, _ = run('column_domain_match', key, domain_pool(toy['domains']), toy['target_source'], 3, 3, 2)
            assert bool(rows) == toy['found']
            for row in rows:
                witness = domain_match(row, toy['domains'], toy['target_source'], square, 2)
                encoded = encrypt(witness, [2, 1], source_key['square'])
                assert all(a == '?' or a == b for a, b in zip(toy['source_frame'], encoded))
    return {'all_frozen_historical_scopes_replayed': True, 'all_controls_replayed': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='Check the frozen certificate (default).')
    parser.add_argument('--write', action='store_true', help='Freeze the recomputed certificate.')
    parser.add_argument('--replay', action='store_true', help='Compile C++17 engines and replay every scope/control.')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    assert not (args.write and args.verify)
    cert, evidence, replay = build(args.pdf, args.replay)
    output = HERE / 'certificates.json'
    if args.write:
        output.write_text(json.dumps(cert, ensure_ascii=False, indent=2) + '\n')
    else:
        assert cert == json.loads(output.read_text())
    print(json.dumps({'verified': not args.write, **cert['summary'],
                      'source_evidence': evidence['summary'], 'replay': replay}, indent=2))
