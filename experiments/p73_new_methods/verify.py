#!/usr/bin/env python3
"""Independent arithmetic verification of the archived p73 method experiments.

ADFGVX Cipher; icekylinx and GPT-6 Astra Pro.
No historical reading is accepted by this verifier. A free substitution square
always admits some plaintext; a coordinate roundtrip alone is not authentication.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'


def read(path):
    return json.loads(path.read_text())


def rank_order(ranks):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    return sorted(range(len(ranks)), key=lambda column: ranks[column])


def inverse_slots(ciphertext, ranks):
    result = [''] * len(ciphertext)
    position = 0
    for column in rank_order(ranks):
        for index in range(column, len(ciphertext), len(ranks)):
            result[index] = ciphertext[position]
            position += 1
    assert position == len(ciphertext)
    return ''.join(result)


def encrypt(plaintext, ranks, square):
    assert sorted(square) == sorted(ALPHABET)
    pairs = {symbol: COORDINATES[index // 6] + COORDINATES[index % 6]
             for index, symbol in enumerate(square)}
    stream = ''.join(pairs[symbol] for symbol in plaintext)
    return ''.join(stream[column::len(ranks)] for column in rank_order(ranks))


def domains(ciphertext, ranks, square):
    assert sorted(square) == sorted(ALPHABET)
    assert len(ciphertext) % 2 == 0
    stream = inverse_slots(ciphertext, ranks)
    result = []
    for index in range(0, len(stream), 2):
        a, b = stream[index:index + 2]
        choices_a = range(6) if a == '?' else [COORDINATES.index(a)]
        choices_b = range(6) if b == '?' else [COORDINATES.index(b)]
        result.append(''.join(sorted(square[6 * x + y]
                                    for x in choices_a for y in choices_b)))
    return result


def source_agrees(ciphertext, witness):
    return len(ciphertext) == len(witness) and all(
        a == '?' or a == b for a, b in zip(ciphertext, witness))


def checked_square_run(record, ciphertext, ranks):
    best = record['best']
    square = best['square']
    assert len(best['plaintext']) * 2 == len(ciphertext)
    witness = encrypt(best['plaintext'], ranks, square)
    assert source_agrees(ciphertext, witness)
    assert ''.join(witness[i] for i, c in enumerate(ciphertext) if c == '?') == best['erasure_fill']
    computed = domains(ciphertext, ranks, square)
    if 'domains' in record:
        assert computed == record['domains']
    if 'plaintext' in record:
        assert len(record['plaintext']) == len(best['plaintext'])
        assert record['plaintext_matches'] == sum(
            a == b for a, b in zip(record['plaintext'], best['plaintext']))
        if 'true_square' in record:
            assert source_agrees(ciphertext, encrypt(record['plaintext'], ranks, record['true_square']))
            assert [i for i, c in enumerate(ciphertext) if c == '?'] == [1, 2]
    return computed


def check_frozen_run(record, ciphertext, keys):
    best = record['best']
    ranks, square = best['ranks'], best['square']
    anchors = keys[record['key_id']]['square']
    assert len(ranks) == record['width']
    assert all(a == '?' or a == b for a, b in zip(anchors, square))
    computed = domains(ciphertext, ranks, square)
    partial = ''.join(d if len(d) == 1 else '?' for d in computed)
    assert partial == best['plaintexts'][0]
    if 'domains' in record:
        assert computed == record['domains']
    # Select an arbitrary compatible completion only to check the coordinates.
    assert source_agrees(ciphertext, encrypt(''.join(d[0] for d in computed), ranks, square))
    if 'plaintext' in record:
        assert source_agrees(ciphertext, encrypt(record['plaintext'], record['true_ranks'], anchors))
        assert [i for i, c in enumerate(ciphertext) if c == '?'] == [1, 2]
        fixed = [i for i, d in enumerate(computed) if len(d) == 1]
        assert record['fixed_plaintext_positions'] == len(fixed)
        assert record['fixed_plaintext_matches'] == sum(
            computed[i] == record['plaintext'][i] for i in fixed)
        assert record['exact_rank_recovery'] == (ranks == record['true_ranks'])
        truth_in_domains = all(record['plaintext'][i] in d for i, d in enumerate(computed))
        field = 'all_plaintext_domains_contain_truth' if 'all_plaintext_domains_contain_truth' in record else 'all_domains_contain_truth'
        assert record[field] == truth_in_domains


def check_retrieval(recompute, skip_assignment=False):
    if not skip_assignment:
        import numpy as np
        from scipy.optimize import linear_sum_assignment
    snapshot_path = HERE / 'retrieval_inputs.json'
    snapshot = read(snapshot_path)
    result = read(HERE / 'results/fuzzy_retrieval.json')
    assert hashlib.sha256(snapshot_path.read_bytes()).hexdigest() == result['input_sha256']
    queries, corpus = snapshot['queries'], snapshot['corpus']
    assert len(queries) == result['query_count']
    assert len(corpus) == result['corpus_count']
    by_id = {q['id']: q for q in queries}
    inputs = read(HERE / 'inputs.json')
    for query in queries:
        if query['group'] == 'p73':
            stream = inverse_slots(inputs['ciphertext'], query['ranks'])
            labels = ''.join('?' if '?' in stream[i:i + 2] else ALPHABET[
                6 * COORDINATES.index(stream[i]) + COORDINATES.index(stream[i + 1])]
                for i in range(0, len(stream), 2))
            assert labels == query['cells']
        elif query['group'] == 'shuffled-p73':
            assert Counter(query['cells']) == Counter(by_id[query['id'][9:]]['cells'])
        elif query['group'] == 'positive':
            restored = list(query['cells'])
            for position, old, new in query['errors']:
                assert restored[position] == new
                restored[position] = old
            pairs = [(a, b) for a, b in zip(restored, query['truth']) if '?' not in (a, b)]
            assert len({a for a, b in pairs}) == len(set(pairs)) == len({b for a, b in pairs})
    raw = gzip.decompress((HERE / 'results/fuzzy_pair_maxima.txt.gz').read_bytes()).decode()
    group_best = {}
    pairs_checked = assignments_checked = 0
    for line in raw.splitlines():
        qi, pi, matched, known, length, qs, ps = map(int, line.split())
        query, reference = queries[qi], corpus[pi]
        a = query['cells'][qs:qs + length]
        b = reference['text'][ps:ps + length]
        assert len(a) == len(b) == length
        frequencies = Counter()
        for x, y in zip(a, b):
            if '?' not in (x, y):
                frequencies[ALPHABET.index(x), ALPHABET.index(y)] += 1
        assert sum(frequencies.values()) == known >= snapshot['minimum_known_overlap']
        assert 0 <= matched <= known
        if not skip_assignment:
            matrix = np.zeros((36, 36), dtype=np.int16)
            for pair, count in frequencies.items():
                matrix[pair] = count
            rows, columns = linear_sum_assignment(matrix, maximize=True)
            assert int(matrix[rows, columns].sum()) == matched
            assignments_checked += 1
        group_best[query['group']] = max(group_best.get(query['group'], 0), matched / known)
        pairs_checked += 1
    for group, best in group_best.items():
        assert best == result['groups'][group]['best_agreement']
    if recompute:
        with tempfile.TemporaryDirectory(prefix='adfgvx-p73-retrieval-') as temporary:
            executable = Path(temporary) / 'retrieve'
            subprocess.run(['c++', '-O3', '-std=c++17', str(HERE / 'src/substitution_agreement.cpp'), '-o', str(executable)], check=True)
            data = f'{len(queries)} {len(corpus)} {snapshot["minimum_known_overlap"]}\n'
            data += '\n'.join(q['cells'] for q in queries) + '\n'
            data += '\n'.join(r['text'] for r in corpus) + '\n'
            rerun = subprocess.run([str(executable)], input=data, text=True, capture_output=True, check=True)
            assert rerun.stdout == raw
    return pairs_checked, assignments_checked


def check_prior_scope(inputs, keys):
    path = HERE / 'prior_scope_inventory.json'
    if not path.exists():
        return 0
    inventory = read(path)
    archive_path = HERE / 'results/prior_anchor_archive.json.gz'
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == inventory['archive_sha256']
    archive = json.loads(gzip.decompress(archive_path.read_bytes()))
    seen = set()
    for item in inventory['records']:
        name = item['runtime_filename']
        raw = archive['records'][name]
        assert hashlib.sha256(raw.encode()).hexdigest() == item['record_sha256']
        record = json.loads(raw)
        case = record['case']
        assert case['id'] == 'p73' and case['ciphertext'] == inputs['ciphertext']
        assert case['partial_square'] == keys[case['key_id']]['square']
        assert (record['requested_restarts'], record['iterations_per_restart']) == (1000, 100000)
        check_frozen_run({'best': record['best'], 'key_id': case['key_id'],
                          'width': case['width'], 'domains': record['domains']}, inputs['ciphertext'], keys)
        log = archive['logs'][name[:-5] + '.jsonl']
        assert hashlib.sha256(log.encode()).hexdigest() == item['log_sha256']
        events = [json.loads(line) for line in log.splitlines() if line.startswith('{')]
        assert max(events, key=lambda row: row['score']) == record['best']
        seen.add((case['key_id'], case['width']))
    assert len(seen) == len(inventory['records']) == 35
    assert seen == {(key, width) for key in ['Oct28-31', 'Nov1-3', 'Nov4-6', 'Nov7-9', 'Nov10-12']
                    for width in range(16, 23)}
    return len(seen)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recompute-retrieval', action='store_true', help='Also repeat every offset in the deterministic C++ retrieval.')
    parser.add_argument('--skip-assignment', action='store_true',
                        help='Use only the standard library; skip independent SciPy assignment optima while retaining source, counter, overlap and prior-scope checks.')
    args = parser.parse_args()
    inputs = read(HERE / 'inputs.json')
    keys = {key['id']: key for key in inputs['catalogued_keys']}
    hypotheses = [tuple(ranks) for key in keys.values()
                  for ranks in [key['column_rank_order'],
                                [len(key['column_rank_order']) + 1 - r for r in key['column_rank_order']]]]
    assert len(keys) == 25 and len(set(hypotheses)) == 50
    target = next(message for message in read(ROOT / 'data/messages.json')['messages'] if message['id'] == 'p73')
    assert target['transcript']['analysis_ciphertext'] == inputs['ciphertext']
    assert len(inputs['ciphertext']) == 178 and inputs['ciphertext'].count('?') == 2
    logs = json.loads(gzip.decompress((HERE / 'results/engine_logs.json.gz').read_bytes()))
    summary = read(HERE / 'completed_runs.json')
    total_runs, total_proposals = 0, 0
    for suite, expected in summary['suites'].items():
        records = read(HERE / 'results' / f'{suite}.json')
        assert len(records) == expected['completed_runs']
        proposal_count = 0
        for record in records:
            if suite in ['anchor_screen', 'frozen_screen', 'spacing_screen', 'radio_rank_p73']:
                check_frozen_run(record, inputs['ciphertext'], keys)
            elif suite in ['frozen_controls', 'spacing_controls', 'radio_rank_controls']:
                check_frozen_run(record, record['ciphertext'], keys)
            elif suite == 'word_controls':
                ciphertext = record.get('ciphertext')
                if ciphertext is None:
                    previous_id = record['initial_record'][:-5]
                    previous = next(r for r in records if r['run_id'] == previous_id)
                    ciphertext = previous['ciphertext']
                    assert record['plaintext'] == previous['plaintext']
                    assert record['ranks'] == previous['ranks']
                    assert record['initial_square'] == previous['best']['square']
                    assert record['initial_erasure_fill'] == previous['best']['erasure_fill']
                checked_square_run(record, ciphertext, record['ranks'])
            elif suite == 'radio_controls':
                checked_square_run(record, record['ciphertext'], record['ranks'])
            else:
                checked_square_run(record, inputs['ciphertext'], record['ranks'])
                assert record['accepted'] is False
                expected_ranks = keys[record['rank_source']]['column_rank_order']
                if record.get('reversed_ranks', False):
                    expected_ranks = [len(expected_ranks) + 1 - r for r in expected_ranks]
                assert record['ranks'] == expected_ranks
                if 'initial' in record:
                    initial = record['initial']
                    witness = encrypt(initial['plaintext'], record['ranks'], initial['square'])
                    assert source_agrees(inputs['ciphertext'], witness)
                    assert ''.join(witness[i] for i, c in enumerate(inputs['ciphertext']) if c == '?') == initial['fill']
            if 'completed_proposals' in record:
                emitted = logs[suite + '/' + record['run_id']]
                final = emitted[-1]
                assert final['proposals'] == record['completed_proposals']
                assert final['restart'] == record['completed_restarts']
                assert final['seconds'] == record['engine_seconds']
                assert max(row['score'] for row in emitted) == record['best']['score']
                assert final['score'] == record['best']['score']
                assert record['best']['proposals'] <= record['completed_proposals']
                proposal_count += record['completed_proposals']
        if 'completed_proposals' in expected:
            assert expected['completed_proposals'] == proposal_count
        if suite in ['word_blind', 'word_staged']:
            recorded_ranks = [tuple(record['ranks']) for record in records]
            assert len(set(recorded_ranks)) == len(records)
            if len(records) == 50:
                assert set(recorded_ranks) == set(hypotheses)
        total_proposals += proposal_count
        total_runs += len(records)
    provenance = read(HERE / 'models/provenance.json')
    for name, expected in provenance['compiled_source_sha256'].items():
        assert hashlib.sha256((HERE / 'src' / name).read_bytes()).hexdigest() == expected
    anchored_source = provenance['anchored_engine_source']
    assert hashlib.sha256((ROOT / anchored_source['path']).read_bytes()).hexdigest() == anchored_source['sha256']
    gate_path = HERE / 'results/radio_rank_gate.json'
    if gate_path.exists():
        gate = read(gate_path)
        protocol = read(HERE / 'results/radio_rank_protocol.json')
        assert protocol['fixed_before_search'] is True
        assert hashlib.sha256((ROOT / 'experiments/joint_search/src/anchored_joint.c').read_bytes()).hexdigest() == protocol['engine_source_sha256']
        controls = read(HERE / 'results/radio_rank_controls.json')
        assert len(controls) == 4
        radio = [r for r in controls if r['model'] == 'radio']
        book = [r for r in controls if r['model'] == 'book']
        assert len(radio) == len(book) == 2
        passed = all(r['exact_rank_recovery'] and
                     r['fixed_plaintext_matches'] == r['fixed_plaintext_positions'] and
                     r['all_domains_contain_truth'] for r in radio)
        passed = passed and sum(r['fixed_plaintext_matches'] for r in radio) >= sum(r['fixed_plaintext_matches'] for r in book)
        assert passed == gate['passed']
        for radio_run, book_run in zip(sorted(radio, key=lambda r: r['control_seed']),
                                       sorted(book, key=lambda r: r['control_seed'])):
            for field in ['seed', 'ciphertext', 'true_ranks', 'plaintext', 'restarts', 'iterations']:
                assert radio_run[field] == book_run[field]
        historical = read(HERE / 'results/radio_rank_p73.json') if 'radio_rank_p73' in summary['suites'] else []
        assert not historical or passed
        assert all([r['key_id'], r['width']] in protocol['conditional_historical_settings'] for r in historical)
    prior_runs = check_prior_scope(inputs, keys)
    retrieval_pairs, assignment_pairs = check_retrieval(args.recompute_retrieval, args.skip_assignment)
    print(json.dumps({'source_coordinate_runs_checked': total_runs,
        'prior_source_coordinate_runs_checked_separately': prior_runs,
        'completed_fixed_square_proposals_checked_against_final_logs': total_proposals,
        'retrieval_pair_records_checked': retrieval_pairs,
        'retrieval_pair_assignments_independently_checked': assignment_pairs,
        'deterministic_retrieval_recomputed': args.recompute_retrieval,
        'accepted_p73_plaintexts': 0}))


if __name__ == '__main__':
    main()
