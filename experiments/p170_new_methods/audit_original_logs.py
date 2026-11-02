#!/usr/bin/env python3
"""Read-only audit of the original p170 run assets; no search or model calls.

Prepared by icekylinx and GPT-6 Astra Pro. This script deliberately does not
import any of the experiment's collectors, verifiers, or cipher functions.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'experiments/p170_new_methods/'
FROZEN_RECORD_SHA256 = {
    'cross_period_results.json': '2997f5cc5808d29383b4da0c117e355a1d066bd69ba71969e98ab3ba7022f82e',
    'radio_rank_results.json': '84aa50331e9f13380e48075e0fe2581e149dc9cd4c9f75cd089c50c5b2d67673',
    'radio_historical_results.json': 'bc9ae4ed9c0ea40a3147cf59074d106a32f8a6ac7677d0415551114b83e0937c',
}
failures = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(condition, description):
    if not condition:
        failures.append(description)
    return bool(condition)


def repository_bytes(relative):
    return (ROOT / relative).read_bytes()


def optional_git_commit():
    """Metadata only: absent git, a ZIP, or a surrounding unrelated repo is OK."""
    try:
        top = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True, timeout=2, check=False)
        if top.returncode or Path(top.stdout.strip()).resolve() != ROOT:
            return None
        result = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, timeout=2, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cross-period-logs', required=True, type=Path,
                        help='Directory containing controls/, controls_stronger/, and historical_native_neighbours/.')
    parser.add_argument('--radio-rank-logs', required=True, type=Path,
                        help='Directory containing the 12 matched rank-control JSONL logs and JSON sidecars.')
    parser.add_argument('--radio-historical-logs', required=True, type=Path,
                        help='Directory containing the 28 historical radio JSONL logs and JSON sidecars.')
    parser.add_argument('--original-engine', required=True, type=Path,
                        help='Original uninstrumented anchored_joint binary; read and hashed, never executed.')
    parser.add_argument('--counted-engine', required=True, type=Path,
                        help='Original counter-instrumented binary; read and hashed, never executed.')
    parser.add_argument('--output', required=True, type=Path, help='Destination JSON report.')
    parser.add_argument('--source-commit', default=None,
                        help='Optional source commit label, used only as metadata. Otherwise detected when available.')
    return parser.parse_args()


def encrypt(plaintext, square, ranks):
    coordinates = 'ADFGVX'
    expanded = ''.join(coordinates[square.index(c) // 6] + coordinates[square.index(c) % 6]
                       for c in plaintext)
    width = len(ranks)
    return ''.join(expanded[column::width]
                   for column in sorted(range(width), key=lambda column: ranks[column]))


def audit(args):
    failures.clear()
    commit = args.source_commit or optional_git_commit()
    commit_origin = 'explicit_metadata' if args.source_commit else ('local_git_metadata' if commit else None)
    files = {}
    documents = {}
    for name in ['cross_period_results.json', 'radio_rank_results.json', 'radio_historical_results.json']:
        data = repository_bytes(PREFIX + name)
        files[PREFIX + name] = {
            'sha256': sha(data), 'bytes': len(data),
            'frozen_record_sha256': FROZEN_RECORD_SHA256[name],
            'matches_frozen_record_sha256': check(sha(data) == FROZEN_RECORD_SHA256[name],
                                                 name + ': frozen result-file SHA mismatch'),
        }
        documents[name] = json.loads(data)

    engine_specs = [
        ('original_uninstrumented', args.original_engine,
         '40e0b6b356f24e8d12a26c809ca80c11d5adebfab926f39a213469ec64af435e',
         'experiments/joint_search/src/anchored_joint.c',
         'b45b91e6a776332feee4e3d8207dbb73deb3032a3b1c0ad03af2e64224652168'),
        ('counted', args.counted_engine,
         '9f416add154009948de5afde395b0a1005306398623733a8cb98a5f8686d3820',
         PREFIX + 'counted_anchored_joint.c',
         '90262989af8926fb90fad5f6da1e6f8d8bab2eab436f3a0d0ee7cc4d6d053def'),
    ]
    engines = {}
    for name, path, expected, source_path, source_expected in engine_specs:
        data = path.read_bytes()
        source = repository_bytes(source_path)
        engines[name] = {
            'path': str(path), 'bytes': len(data), 'sha256': sha(data),
            'matches_recorded_binary_sha256': check(sha(data) == expected, name + ': binary SHA mismatch'),
            'source_path': source_path, 'source_sha256': sha(source),
            'source_matches_recorded_sha256': check(sha(source) == source_expected, name + ': source SHA mismatch'),
            'recipe_engine_identity_checks': 0,
        }

    cross = documents['cross_period_results.json']
    groups = [
        ('cross_period_initial_controls', cross['initial_controls'],
         args.cross_period_logs / 'controls', 6, False),
        ('cross_period_selected_failure_repeats', cross['selected_failure_repeats'],
         args.cross_period_logs / 'controls_stronger', 2, False),
        ('cross_period_historical', cross['historical'],
         args.cross_period_logs / 'historical_native_neighbours', 54, False),
        ('radio_rank_controls', documents['radio_rank_results.json'],
         args.radio_rank_logs, 12, True),
        ('radio_historical', documents['radio_historical_results.json'],
         args.radio_historical_logs, 28, True),
    ]

    all_jobs = []
    group_reports = []
    aggregate_counts = Counter()
    measured_by_objective = {}
    total_configured_uninstrumented = 0
    total_checkpoints = 0

    for group_name, group, directory, expected_count, instrumented in groups:
        records = group['records']
        check(len(records) == expected_count, group_name + ': unexpected record count')
        inventory = {x['filename']: x for x in group.get('runtime_log_inventory', [])}
        check(len(inventory) == (0 if group_name == 'radio_rank_controls' else expected_count),
              group_name + ': unexpected committed log inventory count')
        expected_logs = set()
        group_counts = Counter()
        configured_slots = 0
        group_checkpoints = 0
        jobs = []
        for record in records:
            case = record['case']
            stem = case['id'] + ('__' + record['model'] if group_name == 'radio_rank_controls' else '')
            log = directory / (stem + '.jsonl')
            sidecar = directory / (stem + '.json')
            expected_logs.add(log.name)
            before = len(failures)
            raw = log.read_bytes()
            sidecar_raw = sidecar.read_bytes()
            original_result = json.loads(sidecar_raw)
            check(original_result == record, stem + ': original sidecar differs from committed record')
            lines = raw.decode('utf-8').splitlines()
            check(bool(lines) and all(line.strip() for line in lines), stem + ': empty/non-JSON log line')
            states = [json.loads(line) for line in lines]
            check(states[-1] == record['best'], stem + ': last incumbent differs from committed best')
            check(max(states, key=lambda x: x['score']) == record['best'], stem + ': log maximum differs from best')
            check(all(a['score'] < b['score'] for a, b in zip(states, states[1:])),
                  stem + ': incumbent scores are not strictly increasing')
            check(all(a['restart'] <= b['restart'] for a, b in zip(states, states[1:])),
                  stem + ': restart indices are not nondecreasing')
            recipe = record['recipe'] if instrumented else record['provenance']
            settings = recipe['settings'] if instrumented else recipe
            restarts = settings['restarts']
            iterations = settings['iterations_per_restart'] if instrumented else settings['iterations']
            configured_slots += restarts * iterations
            engine_name = 'counted' if instrumented else 'original_uninstrumented'
            check(recipe['engine_sha256'] == engines[engine_name]['sha256'], stem + ': recipe binary SHA mismatch')
            engines[engine_name]['recipe_engine_identity_checks'] += 1
            if instrumented:
                check(recipe['engine_source_sha256'] == engines[engine_name]['source_sha256'],
                      stem + ': recipe engine source SHA mismatch')
            anchor = case.get('partial_square', case.get('full_square'))
            before_checkpoints = len(failures)
            for index, state in enumerate(states):
                tag = stem + ': checkpoint ' + str(index)
                check(set(state) == {'score', 'restart', 'known_square_cells', 'square', 'ranks', 'plaintexts'},
                      tag + ': unexpected state fields')
                check(isinstance(state['restart'], int) and 0 <= state['restart'] < restarts,
                      tag + ': restart outside configured range')
                check(len(state['square']) == 36 and set(state['square']) == set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'),
                      tag + ': not a complete 36-symbol permutation')
                check(len(state['ranks']) == case['width'] and sorted(state['ranks']) == list(range(1, case['width'] + 1)),
                      tag + ': rank permutation is invalid')
                check(state['known_square_cells'] == sum(c != '?' for c in anchor), tag + ': anchor count differs')
                check(all(c == '?' or c == state['square'][i] for i, c in enumerate(anchor)),
                      tag + ': a supplied square anchor changed')
                check(len(state['plaintexts']) == 1, tag + ': unexpected plaintext count')
                check(encrypt(state['plaintexts'][0], state['square'], state['ranks']) == case['ciphertext'],
                      tag + ': independently reconstructed ciphertext differs')
            checkpoints_passed = len(failures) == before_checkpoints
            pin = inventory.get(log.name)
            if pin is not None:
                check(pin['case_id'] == case['id'], stem + ': inventory case identifier differs')
                check(sha(raw) == pin['sha256'], stem + ': original log SHA differs from committed inventory')
                check(len(states) == pin['improving_checkpoints'], stem + ': inventory checkpoint count differs')
                check(pin['final_checkpoint_is_archived_best'] is True, stem + ': inventory final flag is false')
            else:
                check(group_name == 'radio_rank_controls', stem + ': unexpected unpinned log')
            job = {
                'filename': log.name, 'sha256': sha(raw), 'bytes': len(raw),
                'committed_log_hash_available': pin is not None,
                'committed_log_hash_matches': sha(raw) == pin['sha256'] if pin is not None else None,
                'sidecar_sha256': sha(sidecar_raw),
                'sidecar_matches_entire_committed_record': original_result == record,
                'improving_checkpoints': len(states),
                'last_incumbent_matches_committed_best': states[-1] == record['best'],
                'all_checkpoints_reencrypt_and_preserve_anchors': checkpoints_passed,
                'configured_restarts': restarts, 'configured_loop_slots': restarts * iterations,
            }
            if instrumented:
                counts = original_result['actual_search_counts']
                check(counts == record['actual_search_counts'], stem + ': counter sidecar differs from committed counters')
                check(set(counts) == {'completed_restarts', 'annealing_slots', 'annealing_fitness_calls',
                                     'polish_fitness_calls', 'total_fitness_calls'}, stem + ': unexpected counter fields')
                check(all(isinstance(value, int) and value >= 0 for value in counts.values()), stem + ': invalid count')
                check(counts['completed_restarts'] == restarts, stem + ': completed restarts differ')
                check(counts['annealing_slots'] == restarts * iterations, stem + ': annealing slot count differs')
                check(counts['annealing_fitness_calls'] <= counts['annealing_slots'], stem + ': too many annealing calls')
                if group_name == 'radio_rank_controls':
                    check(counts['annealing_fitness_calls'] == counts['annealing_slots'], stem + ': full-square skipped slot')
                check(counts['total_fitness_calls'] == counts['annealing_fitness_calls'] +
                      counts['polish_fitness_calls'] + counts['completed_restarts'], stem + ': total count arithmetic differs')
                group_counts.update(counts)
                aggregate_counts.update(counts)
                objective = record.get('model', 'radio_mixture')
                measured_by_objective.setdefault(objective, Counter()).update(counts)
                job['instrumented_counts_from_original_sidecar'] = counts
            else:
                check('actual_search_counts' not in original_result, stem + ': unexpected uninstrumented actual count')
            job['passed'] = len(failures) == before
            jobs.append(job)
            all_jobs.append(job)
            group_checkpoints += len(states)
        actual_logs = {x.name for x in directory.glob('*.jsonl')}
        check(actual_logs == expected_logs, group_name + ': missing or extra original JSONL files')
        check(not inventory or set(inventory) == expected_logs, group_name + ': inventory file set differs')
        if instrumented:
            key = 'total_actual_counts' if group_name == 'radio_rank_controls' else 'actual_search_counts'
            check(dict(group_counts) == group['summary'][key], group_name + ': recomputed sidecar counter totals differ')
        else:
            check(configured_slots == group['summary']['configured_proposal_slots'], group_name + ': configured slot sum differs')
            total_configured_uninstrumented += configured_slots
        group_reports.append({
            'group': group_name, 'directory': str(directory), 'jobs': len(jobs),
            'instrumented': instrumented, 'committed_log_hashes': len(inventory),
            'log_set_matches_records': actual_logs == expected_logs,
            'improving_checkpoints': group_checkpoints,
            'configured_loop_slots': configured_slots,
            'instrumented_counter_sum': dict(group_counts) if instrumented else None,
            'files': jobs,
        })
        total_checkpoints += group_checkpoints

    runner_files = {}
    for filename, results_name in [('run_radio_rank.py', 'radio_rank_results.json'),
                                   ('run_radio_historical.py', 'radio_historical_results.json')]:
        data = repository_bytes(PREFIX + filename)
        expected = {record['recipe']['runner_sha256'] for record in documents[results_name]['records']}
        runner_files[PREFIX + filename] = {
            'sha256': sha(data), 'bytes': len(data),
            'matches_all_recorded_runner_hashes': check(expected == {sha(data)},
                                                       filename + ': counter-capture runner SHA mismatch'),
        }

    report = {
        'schema': 'p170-portable-original-log-audit-v1',
        'prepared_by': ['icekylinx', 'GPT-6 Astra Pro'],
        'audited_at_utc': datetime.now(timezone.utc).isoformat(),
        'repository_commit': commit,
        'repository_commit_metadata_origin': commit_origin,
        'record_files_bound_by_frozen_sha256_without_git': True,
        'status': 'passed_with_explicit_provenance_limits' if not failures else 'failed',
        'method': 'Independent standard-library JSON/SHA audit of original run assets against committed records, plus standalone column-transposition reconstruction for every logged incumbent. No experiment verifier imported, no optimization/model search or executable rerun.',
        'summary': {
            'original_jsonl_logs_checked': len(all_jobs),
            'logs_with_preexisting_committed_sha256_inventory': sum(j['committed_log_hash_available'] for j in all_jobs),
            'logs_without_preexisting_sha_inventory_newly_hashed_here': sum(not j['committed_log_hash_available'] for j in all_jobs),
            'original_sidecars_equal_entire_committed_records': sum(j['sidecar_matches_entire_committed_record'] for j in all_jobs),
            'final_incumbents_equal_committed_best': sum(j['last_incumbent_matches_committed_best'] for j in all_jobs),
            'logged_incumbents_independently_reencrypted': total_checkpoints,
            'instrumented_jobs': sum('instrumented_counts_from_original_sidecar' in job for job in all_jobs),
            'instrumented_counter_totals_from_original_sidecars': dict(aggregate_counts),
            'instrumented_counter_totals_by_objective': {k: dict(v) for k, v in measured_by_objective.items()},
            'uninstrumented_jobs': sum('instrumented_counts_from_original_sidecar' not in job for job in all_jobs),
            'uninstrumented_configured_loop_slots_not_measured_calls': total_configured_uninstrumented,
            'failure_count': len(failures),
        },
        'scope_and_limits': [
            'Only 90 original JSONL logs have pre-existing SHA256 pins in the archived runtime_log_inventory. The 12 radio-rank control JSONL hashes were first recorded in the final original-log audit, not in that pre-existing inventory. This audit hashes those 12 logs and compares their last states and complete original JSON sidecars against the frozen records.',
            'All JSONL streams contain improving-incumbent stdout events, not terminal counter events. Their final incumbent restart index is not a completion counter.',
            'The 40 instrumented jobs have parsed engine counters preserved in original JSON result sidecars and matched against committed records. Their aggregate arithmetic and configured bounds were checked; this audit did not reexecute or independently recount the historical fitness calls.',
            'The checked runners capture exactly one JSON counter record from stderr after a successful subprocess.run(check=True), then retain those parsed counters in the result sidecar. The separate original stderr byte stream was not persisted in these run directories, so its original bytes cannot be hash-verified.',
            'The 7,000,000,000 loop slots for 62 uninstrumented book jobs are configured slots, not measured fitness calls or distinct candidate states. Successful runner-side results and incumbent logs do not measure those call counts.',
            'The 3,902,267,094 measured-by-engine calls include book-model control jobs as well as radio-mixture jobs. They must not all be labeled radio-objective calls.',
            'Binary SHA identity is verified against each run recipe; this audit does not prove reproducible compilation or independently rerun the binaries.',
            'Git is optional metadata only. All three result-file bytes are bound to explicit frozen SHA256 values, and every log is compared against those files. A null repository_commit outside a git checkout does not disable any evidence check.',
        ],
        'archived_record_files': files,
        'counter_capture_runner_files': runner_files,
        'engines': engines,
        'groups': group_reports,
        'audit_script_sha256': sha(Path(__file__).read_bytes()),
        'failures': failures,
    }
    check(len(all_jobs) == 102, 'overall: wrong original log count')
    check(sum(j['committed_log_hash_available'] for j in all_jobs) == 90, 'overall: wrong hash-pinned log count')
    check(aggregate_counts['total_fitness_calls'] == 3902267094, 'overall: wrong instrumented total')
    check(total_configured_uninstrumented == 7000000000, 'overall: wrong uninstrumented configured slot total')
    report['summary']['failure_count'] = len(failures)
    report['status'] = 'passed_with_explicit_provenance_limits' if not failures else 'failed'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(args.output), 'status': report['status'], 'summary': report['summary'],
                      'failures': failures}, indent=2))
    return 1 if failures else 0


def main():
    args = arguments()
    try:
        return audit(args)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        failures.append(type(error).__name__ + ': ' + str(error))
        report = {
            'schema': 'p170-portable-original-log-audit-v1',
            'prepared_by': ['icekylinx', 'GPT-6 Astra Pro'],
            'status': 'failed',
            'audit_incomplete': True,
            'failures': failures,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'report': str(args.output), **report}, indent=2))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
