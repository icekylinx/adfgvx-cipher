#!/usr/bin/env python3
"""Run frozen anchored-square cases using the shared joint_search engine.

The C engine receives a partial square, zero ranks and ciphertext only. Control
plaintexts and true ranks are used after search solely for evaluation.
"""
import argparse
import concurrent.futures
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from arithmetic import case_label, control_evaluation, domains, seed_for, validate_case, verify_record

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def atomic_json(path, value):
    temp = path.with_name(path.name + f'.{os.getpid()}.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(path)


def positive(value):
    value = int(value)
    if not 1 <= value <= 2147483647:
        raise argparse.ArgumentTypeError('Expected a positive signed-32-bit integer')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=HERE.parents[1])
    parser.add_argument('--engine', type=Path)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--workers', type=positive, default=1)
    parser.add_argument('--restarts', type=positive, default=1000)
    parser.add_argument('--iterations', type=positive, default=100000)
    parser.add_argument('--only', default='*', help='Glob over complete case labels')
    parser.add_argument('--limit', type=positive)
    parser.add_argument('--reverse', action='store_true', help='Reverse job order; inputs, seeds and objectives do not change')
    parser.add_argument('--list', action='store_true', help='List selected labels without compiling or searching')
    args = parser.parse_args()
    frozen = json.loads((HERE / 'data/cases.json').read_text())
    all_cases = frozen['historical'] + frozen['controls']
    selected = frozen['controls'] if args.controls else frozen['historical']
    selected = [c for c in selected if fnmatch.fnmatchcase(case_label(c, args.restarts, args.iterations), args.only)]
    if args.reverse:
        selected = list(reversed(selected))
    if args.limit:
        selected = selected[:args.limit]
    for case in selected:
        validate_case(case)
    if args.list:
        print(json.dumps([case_label(c, args.restarts, args.iterations) for c in selected], indent=2))
        return
    if not selected:
        parser.error('No cases selected')
    if args.model is None or args.output is None:
        parser.error('--model and --output are required for a search')
    engine = (args.engine or args.repository / 'experiments/joint_search/bin/anchored_joint').resolve()
    model = args.model.resolve()
    if sys.byteorder != 'little':
        parser.error('The shared C model reader requires a little-endian host')
    if len(str(model).encode()) >= 1024:
        parser.error('Model path exceeds the C header buffer')
    if any(ch.isspace() for ch in str(model)):
        parser.error('The C stdin format requires a model path without whitespace')
    provenance = json.loads((HERE / 'data/provenance.json').read_text())
    if digest(model) != provenance['files']['model']['sha256']:
        parser.error('Model hash differs from the pinned military37 table')
    recipe = {'format_version': 1, 'cases_sha256': digest(HERE / 'data/cases.json'),
              'engine_sha256': digest(engine), 'model_sha256': digest(model),
              'runner_sha256': digest(Path(__file__)), 'arithmetic_sha256': digest(HERE / 'arithmetic.py'),
              'restarts': args.restarts, 'iterations': args.iterations}
    fingerprint = canonical_hash(recipe)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / 'RUN.json'
    # Validate the old manifest and every reused record before any mutation.
    if manifest.exists():
        previous = json.loads(manifest.read_text())
        if previous.get('recipe_fingerprint') != fingerprint:
            parser.error('Existing output belongs to a different recipe; choose a new directory')
    reused = {}
    for case in selected:
        label = case_label(case, args.restarts, args.iterations)
        path = output / (label + '.json')
        if path.exists():
            record = json.loads(path.read_text())
            if record.get('recipe_fingerprint') != fingerprint:
                parser.error(f'Cannot resume incompatible record {label}')
            verify_record(record, all_cases)
            reused[label] = record
    atomic_json(manifest, {'recipe': recipe, 'recipe_fingerprint': fingerprint,
                          'selected_labels': [case_label(c, args.restarts, args.iterations) for c in selected],
                          'reverse_execution_order': args.reverse})

    def run(case):
        label = case_label(case, args.restarts, args.iterations)
        if label in reused:
            print(json.dumps({'label': label, 'resumed': True}), flush=True)
            return reused[label]
        seed = seed_for(label)
        engine_input = '\n'.join([f'{model} {case["width"]} {args.restarts} {args.iterations} {seed} 1',
                                   case['partial_square'], ' '.join(['0'] * case['width']), case['ciphertext']]) + '\n'
        start = time.monotonic()
        result = subprocess.run([str(engine)], input=engine_input, text=True, capture_output=True, check=True)
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
        if not rows:
            raise RuntimeError(f'{label}: engine returned no candidate')
        best = max(rows, key=lambda row: row['score'])
        letter_domains = domains(case['ciphertext'], best['ranks'], best['square'])
        record = {'case': case, 'best': best, 'domains': letter_domains,
                  'requested_restarts': args.restarts, 'iterations_per_restart': args.iterations,
                  'seed': seed, 'elapsed_seconds': time.monotonic() - start,
                  'model': 'Whole-cell wildcard marginal quadgrams; exact domains restored after ranking',
                  'provenance': recipe, 'recipe_fingerprint': fingerprint,
                  'accepted_historical_plaintext': False}
        if 'evaluation_only' in case:
            record['control_evaluation'] = control_evaluation(case, best, letter_domains)
        verify_record(record, all_cases)
        (output / (label + '.jsonl')).write_text(result.stdout)
        atomic_json(output / (label + '.json'), record)
        print(json.dumps({'label': label, 'score': best['score'], 'plaintext': best['plaintexts'][0],
                          'control_evaluation': record.get('control_evaluation')}), flush=True)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(run, selected))
    print(json.dumps({'completed_selected_cases': len(results), 'controls': args.controls,
                      'accepted_historical_plaintexts': 0}), flush=True)


if __name__ == '__main__':
    main()
