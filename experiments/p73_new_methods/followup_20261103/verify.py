#!/usr/bin/env python3
"""Check the compact p73 followup without its unavailable language model.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The default checks are independent integer/cipher arithmetic. They do not
replay annealing or authenticate any historical plaintext.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'


def read(path):
    return json.loads(path.read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inverse_slots(ciphertext, ranks):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    result = [''] * len(ciphertext)
    at = 0
    for column in sorted(range(len(ranks)), key=ranks.__getitem__):
        for position in range(column, len(ciphertext), len(ranks)):
            result[position] = ciphertext[at]
            at += 1
    assert at == len(ciphertext)
    return ''.join(result)


def encode(plaintext, ranks, square):
    assert sorted(square) == sorted(ALPHABET)
    pairs = {c: COORDINATES[i // 6] + COORDINATES[i % 6]
             for i, c in enumerate(square)}
    middle = ''.join(pairs[c] for c in plaintext)
    return ''.join(middle[c::len(ranks)]
                   for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def cells(ciphertext, ranks):
    middle = inverse_slots(ciphertext, ranks)
    assert len(middle) % 2 == 0
    return ''.join('?' if '?' in middle[i:i+2] else
                   ALPHABET[6 * COORDINATES.index(middle[i]) +
                            COORDINATES.index(middle[i+1])]
                   for i in range(0, len(middle), 2))


def decode(ciphertext, ranks, square):
    assert sorted(square) == sorted(ALPHABET)
    return ''.join('?' if c == '?' else square[ALPHABET.index(c)]
                   for c in cells(ciphertext, ranks))


def profile_score(ciphertext, ranks, profile):
    counts = Counter(cells(ciphertext, ranks).replace('?', ''))
    ranked = sorted((counts[c] for c in ALPHABET), reverse=True)
    n = len(ciphertext) // 2
    return sum(-(count / n - p['mean']) ** 2 /
               (p['variance'] + .25 / (n*n))
               for count, p in zip(ranked, profile))


def maximum_assignment(count):
    """Exact integer Hungarian assignment, independent of the C++ replay."""
    n = 36
    u, v, p, way = ([0] * (n + 1) for _ in range(4))
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv, used = [10**9] * (n + 1), [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], 10**9, 0
            for j in range(1, n + 1):
                if used[j]:
                    continue
                cur = -count[i0-1][j-1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j], way[j] = cur, j0
                if minv[j] < delta:
                    delta, j1 = minv[j], j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if not p[j0]:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    return v[0]


def load_donors():
    data = json.loads(gzip.decompress((HERE / 'donor_inputs.json.gz').read_bytes()))
    prior_path = HERE / data['prior_corpus']
    assert sha(prior_path.read_bytes()) == data['prior_corpus_sha256']
    prior = read(prior_path)['corpus']
    for row in data['donors']:
        if 'prior_corpus_index' in row:
            assert 'text' not in row
            row['text'] = prior[row['prior_corpus_index']]['text']
    return data


def check_leader(row, queries, donors):
    q = queries[row['query_index']]
    d = donors[row['donor_index']]['text']
    a, b, length = row['query_start'], row['donor_start'], row['overlap']
    assert 0 <= a <= len(q)-length and 0 <= b <= len(d)-length
    count = [[0] * 36 for _ in range(36)]
    for x, y in zip(q[a:a+length], d[b:b+length]):
        if x in ALPHABET and y in ALPHABET:
            count[ALPHABET.index(x)][ALPHABET.index(y)] += 1
    assert sum(map(sum, count)) == row['known'] >= 60
    assert maximum_assignment(count) == row['matched']


def replay_donors(data, query_cells, expected):
    source = HERE.parent / 'src/substitution_agreement.cpp'
    text = f"{len(query_cells)} {len(data['donors'])} 60\n"
    text += '\n'.join(query_cells) + '\n'
    text += '\n'.join(r['text'] for r in data['donors']) + '\n'
    with tempfile.TemporaryDirectory(prefix='p73-donor-followup-') as tmp:
        binary = Path(tmp) / 'substitution_agreement'
        subprocess.run(['g++', '-O3', '-std=c++17', str(source), '-o', str(binary)],
                       check=True, capture_output=True)
        output = subprocess.run([str(binary)], input=text.encode(),
                                check=True, capture_output=True).stdout
    assert len(output.splitlines()) == expected['donor_pairwise_optima_emitted']
    assert sha(output) == expected['donor_raw_output_sha256']
    return {'emitted_optima': len(output.splitlines()), 'sha256': sha(output)}


def replay_profile(width, scope, ciphertext):
    run = next(r for r in scope['target_runs'] if r['width'] == width)
    with tempfile.TemporaryDirectory(prefix='p73-profile-followup-') as tmp:
        tmp = Path(tmp)
        binary, profile, source = tmp/'profile_pairing', tmp/'profile.txt', tmp/'source.txt'
        profile.write_text(''.join(f"{p['mean']:.14g} {p['variance']:.14g}\n"
                                   for p in scope['profile']['mean_variance']))
        assert sha(profile.read_bytes()) == scope['profile']['profile_txt_sha256']
        source.write_text(ciphertext + '\n')
        subprocess.run(['g++', '-O3', '-std=c++17', str(HERE/'profile_pairing.cpp'),
                        '-o', str(binary)], check=True, capture_output=True)
        output = subprocess.run([str(binary), str(profile), str(source), str(width),
                                 str(run['profile_restarts']), str(run['profile_iterations']),
                                 str(run['profile_seed']), '5'], check=True,
                                capture_output=True).stdout
    assert sha(output) == run['profile_stdout_sha256']
    return {'width': width, 'sha256': sha(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recompute-donors', action='store_true')
    parser.add_argument('--recompute-profile', type=int, choices=[10, 12, 14, 16])
    args = parser.parse_args()
    inputs, scope, cert = (read(HERE / name) for name in
                           ['inputs.json', 'scope.json', 'certificates.json'])
    ciphertext = inputs['source_ciphertext']
    assert ciphertext == read(HERE.parent/'inputs.json')['ciphertext']
    assert len(ciphertext) == 178 and ciphertext.count('?') == 2
    assert [i for i, c in enumerate(ciphertext) if c == '?'] == [1, 2]
    assert sum(c in COORDINATES for c in ciphertext) == 176
    assert sum(scope['source_geometry']['physical_row_lengths']) == 178
    truth = inputs['fresh_control_plaintext']
    assert len(truth) == 89
    assert len(scope['profile']['mean_variance']) == 36
    controls = []
    for row in inputs['controls']:
        source = row['ciphertext']
        planted = encode(truth, row['planted_ranks'], row['planted_square'])
        assert source == planted[:1] + '??' + planted[3:]
        raw = decode(source, row['selected_ranks'], row['selected_square'])
        assert raw == row['raw']
        assert sum(c != '?' for c in raw) == row['raw_fixed_positions'] == 87
        assert sum(a == b for a, b in zip(raw, truth) if a != '?') == row['raw_fixed_matches']
        witness = encode(truth, row['selected_ranks'], row['truth_square_witness'])
        assert witness == row['truth_reencryption_witness']
        price = sum(a != b for a, b in zip(source, witness) if a != '?')
        assert price == row['observed_coordinate_price_of_complete_control_truth'] == 0
        assert len(witness) == len(source) == 178
        assert math.isclose(profile_score(source, row['profile_seed_ranks'],
                                         scope['profile']['mean_variance']),
                            row['profile_score'], abs_tol=2e-9)
        controls.append({'width': row['width'], 'raw_matches': row['raw_fixed_matches'],
                         'raw_fixed': 87, 'truth_observed_coordinate_changes': price,
                         'printed_mask_fills_in_truth_witness': 2})
    assert [r['width'] for r in controls] == [10, 12, 14, 16]
    fits = inputs['target_best_per_pairing_seed']
    assert Counter(r['width'] for r in fits) == {10: 12, 12: 15, 14: 15, 16: 15}
    assert len(fits) == scope['pairing_seed_language_fits_total'] == 57
    for row in fits:
        assert len(row['selected_ranks']) == row['width']
        assert decode(ciphertext, row['selected_ranks'], row['selected_square']) == row['raw']
        assert len(row['raw']) == 89 and row['raw'].count('?') == 2
        assert math.isclose(profile_score(ciphertext, row['profile_seed_ranks'],
                                         scope['profile']['mean_variance']),
                            row['profile_score'], abs_tol=2e-9)
        assert row['seed'] == 20261130 + row['profile_rank']
    geometry = sum(math.comb(r['width'], 178 % r['width']) for r in scope['target_runs'])
    assert geometry == scope['source_segmentations_total'] == 1232
    for row in scope['target_runs']:
        assert row['source_segmentations'] == math.comb(row['width'], 178 % row['width'])
    data = load_donors()
    assert len(data['queries']) == scope['donor_queries'] == 104
    assert len(data['donors']) == scope['donor_strings'] == 944
    assert sum(r['group'] == 'p73' for r in data['queries']) == 103
    assert sum(r['curated_source_only'] for r in data['donors']) == 293
    assert sum('prior_corpus_index' in r for r in data['donors']) == 146
    assert [r['id'] for r in data['donors']] == list(range(944))
    assert data['control_query_ciphertext'] == inputs['controls'][0]['ciphertext']
    control_query = data['queries'][cert['best_control']['query_index']]
    assert control_query['group'] == 'control'
    assert control_query['ranks'] == inputs['controls'][0]['planted_ranks']
    assert data['donors'][cert['best_control']['donor_index']]['text'] == truth
    query_cells = [cells(data['control_query_ciphertext'] if r['group'] == 'control'
                         else ciphertext, r['ranks']) for r in data['queries']]
    for row in cert['donor_leaders']:
        check_leader(row, query_cells, data['donors'])
    assert len(cert['donor_leaders']) == cert['donor_leader_check_count'] == 41
    assert cert['best_control']['matched'] == cert['best_control']['known'] == 87
    assert cert['best_historical']['matched'] / cert['best_historical']['known'] == 31/61
    assert cert['best_curated_source_only']['matched'] / cert['best_curated_source_only']['known'] == .5
    assert cert['donor_pairwise_optima_emitted'] == scope['reported_donor_pairwise_optima'] == 94795
    assert not inputs['historical_reading_accepted'] and not cert['target_reading_accepted']
    result = {'controls': controls, 'source_segmentations': geometry,
              'target_pairing_seed_fits_checked': len(fits),
              'donor_leader_assignments_checked': 41,
              'donor_full_scan_replayed': False,
              'complete_stochastic_search_replayed': False,
              'historical_reading_accepted': False}
    if args.recompute_donors:
        result['donor_full_scan'] = replay_donors(data, query_cells, cert)
        result['donor_full_scan_replayed'] = True
    if args.recompute_profile:
        result['profile_replay'] = replay_profile(args.recompute_profile, scope, ciphertext)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
