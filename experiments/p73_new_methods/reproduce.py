#!/usr/bin/env python3
"""Replay one archived stochastic setting with hash-checked language inputs.

ADFGVX Cipher; icekylinx and GPT-6 Astra Pro. Runtime-limited searches can
complete different numbers of proposals on different machines; coordinate
verification of an archived candidate is deterministic (see verify.py).
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

from verify import HERE, ROOT, check_frozen_run, checked_square_run, read


def main():
    suites = read(HERE / 'completed_runs.json')['suites']
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', required=True, choices=sorted(suites))
    parser.add_argument('--run', required=True, help='The run_id stored in results/<suite>.json.')
    parser.add_argument('--quad', type=Path, required=True)
    parser.add_argument('--lexicon', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=float, help='Optional runtime override for fixed-square runs.')
    parser.add_argument('--restarts', type=int, help='Optional frozen-square restart override.')
    parser.add_argument('--iterations', type=int, help='Optional frozen-square iteration override.')
    args = parser.parse_args()
    records = read(HERE / 'results' / f'{args.suite}.json')
    record = next((r for r in records if r['run_id'] == args.run), None)
    if record is None:
        parser.error('No such completed run in this suite.')
    inputs = read(HERE / 'inputs.json')
    keys = {key['id']: key for key in inputs['catalogued_keys']}
    source_provenance = read(HERE / 'models/provenance.json')
    provenance = source_provenance['models']
    frozen = args.suite in ['anchor_screen', 'frozen_screen', 'frozen_controls', 'spacing_screen', 'spacing_controls',
                           'radio_rank_controls', 'radio_rank_p73']
    if args.suite.startswith('radio_rank_'):
        model_id = 'radio_book37' if record['model'] == 'radio' else 'book37_marginal'
    elif args.suite == 'radio_controls':
        model_id = 'radio_book36' if record['model'] == 'radio' else 'book36'
    elif args.suite.startswith('radio_'):
        model_id = 'radio_book36'
    elif args.suite.startswith('spacing_'):
        model_id = 'plain37' if record['convention'] == 'plain' else 'word_X37'
    else:
        model_id = 'book37_marginal' if frozen else 'book36'
    assert hashlib.sha256(args.quad.read_bytes()).hexdigest() == provenance[model_id]['sha256']
    if not frozen:
        if args.lexicon is None:
            parser.error('Fixed-square runs require the frozen word lexicon, including when weight=0.')
        assert hashlib.sha256(args.lexicon.read_bytes()).hexdigest() == provenance['word_lexicon']['sha256']
    ciphertext = record.get('ciphertext', inputs['ciphertext'])
    if args.suite == 'word_controls' and 'ciphertext' not in record:
        previous = next(r for r in records if r['run_id'] == record['initial_record'][:-5])
        ciphertext = previous['ciphertext']
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='adfgvx-p73-replay-') as directory:
        temporary = Path(directory)
        executable = temporary / 'search'
        if frozen:
            source = ROOT / source_provenance['anchored_engine_source']['path']
            assert hashlib.sha256(source.read_bytes()).hexdigest() == source_provenance['anchored_engine_source']['sha256']
            subprocess.run(['cc', '-O3', '-std=c11', str(source), '-lm', '-o', str(executable)], check=True)
            width = record['width']
            original_budget = record.get('budget', [record.get('restarts'), record.get('iterations')])
            restarts = args.restarts if args.restarts is not None else original_budget[0]
            iterations = args.iterations if args.iterations is not None else original_budget[1]
            assert restarts > 0 and iterations > 0
            square = keys[record['key_id']]['square']
            if any(character.isspace() for character in str(args.quad.resolve())):
                raise ValueError('The legacy anchored engine accepts a model path without whitespace.')
            data = f'{args.quad.resolve()} {width} {restarts} {iterations} {record["seed"]} 1\n{square}\n'
            data += ' '.join(['0'] * width) + '\n' + ciphertext + '\n'
            completed = subprocess.run([str(executable)], input=data, text=True, capture_output=True, check=True)
        else:
            warm = 'initial' in record or 'initial_square' in record
            source = HERE / 'src' / ('fixed_square.cpp' if warm else 'fixed_square_blind.cpp')
            assert hashlib.sha256(source.read_bytes()).hexdigest() == source_provenance['compiled_source_sha256'][source.name]
            subprocess.run(['c++', '-O3', '-std=c++17', str(source), '-o', str(executable)], check=True)
            ranks = record['ranks']
            input_path = temporary / 'cipher.txt'
            input_path.write_text(f'{len(ranks)} ' + '?' * 36 + '\n' + ' '.join(map(str, ranks)) + '\n' + ciphertext + '\n')
            seconds = args.seconds if args.seconds is not None else record.get('wall_budget_seconds', 120)
            assert seconds > 0
            command = [str(executable), str(args.quad.resolve()), str(args.lexicon.resolve()), str(input_path), str(seconds), str(record['best']['word_weight']), str(record['seed'])]
            if warm:
                initial = record.get('initial', {'square': record.get('initial_square'), 'fill': record.get('initial_erasure_fill')})
                initial_path = temporary / 'initial.txt'
                initial_path.write_text(initial['square'] + '\n' + initial['fill'] + '\n')
                command.append(str(initial_path))
            completed = subprocess.run(command, text=True, capture_output=True, check=True)
    emitted = [json.loads(line) for line in completed.stdout.splitlines() if line.startswith('{')]
    best = max(emitted, key=lambda row: row['score'])
    output = {'prepared_by': ['icekylinx', 'GPT-6 Astra Pro'], 'suite': args.suite, 'run_id': args.run,
              'seed': record['seed'], 'model_sha256': provenance[model_id]['sha256'], 'best': best,
              'elapsed_seconds_including_compilation': time.monotonic() - start,
              'ciphertext': ciphertext, 'accepted': False}
    if frozen:
        checking = {'best': best, 'key_id': record['key_id'], 'width': record['width']}
        check_frozen_run(checking, ciphertext, keys)
        output['configured_proposal_slots'] = restarts * iterations
        output['applied_budget'] = {'restarts': restarts, 'iterations': iterations}
        output['archived_budget'] = {'restarts': original_budget[0], 'iterations': original_budget[1]}
    else:
        output['ranks'] = record['ranks']
        checked_square_run(output, ciphertext, record['ranks'])
        output.update({'completed_proposals': emitted[-1]['proposals'], 'completed_restarts': emitted[-1]['restart']})
        output['applied_budget'] = {'seconds': seconds}
        output['archived_budget'] = {'seconds': record.get('wall_budget_seconds', 120)}
        if 'plaintext' in record:
            output['control_plaintext_matches'] = sum(a == b for a, b in zip(record['plaintext'], best['plaintext']))
    output['requested_overrides'] = {name: value for name, value in
                                    [('seconds', args.seconds), ('restarts', args.restarts),
                                     ('iterations', args.iterations)] if value is not None}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    args.output.with_suffix('.jsonl').write_text(completed.stdout)
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
