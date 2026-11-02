#!/usr/bin/env python3
"""Reproduce the bounded p170 contiguous-fragment search and two controls.

Requires NumPy, a C compiler, and the checksummed upstream quadgram table.
All subprocesses run sequentially. Set OPENBLAS_NUM_THREADS=1 to use one worker.
The 23 MB coordinate arrays are generated in a temporary directory and removed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import tempfile
from marginal_model import build, load_quad26


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', type=Path, required=True)
    parser.add_argument('--quad26', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--key', action='append', help='Restrict to one or more stated key IDs.')
    parser.add_argument('--controls-only', action='store_true')
    parser.add_argument('--no-controls', action='store_true')
    parser.add_argument('--cc', default='cc')
    args = parser.parse_args()
    experiment = json.loads(args.experiment.read_text())
    keys = {row['id']: row for row in experiment['keys']}
    if args.key and any(key not in keys for key in args.key):
        parser.error('An unknown key ID was requested.')
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    executable = output_dir / 'p170_scan'
    subprocess.run([args.cc, '-O3', '-std=gnu11',
                    str(Path(__file__).with_name('p170_scan.c')), '-o', str(executable)], check=True)
    quad26 = load_quad26(args.quad26)
    jobs = []
    if not args.controls_only:
        for key_id in args.key or list(keys):
            jobs.append((key_id, keys[key_id], experiment['source']['analysis_ciphertext'],
                         experiment['search_output_sha256'][key_id]))
    if not args.no_controls:
        for record in experiment['controls']['records']:
            jobs.append((record['id'], keys['Nov7-9'], record['observed_fragment'],
                         experiment['controls']['output_sha256'][record['id']]))
    reports = []
    with tempfile.TemporaryDirectory(prefix='p170_models_', dir=output_dir) as temporary:
        temporary = Path(temporary)
        last_square = None
        for label, key, received, original_sha in jobs:
            if key['square'] != last_square:
                quad, _, probability = build(key['square'], quad26)
                quad.tofile(temporary / 'quad49.bin')
                probability.tofile(temporary / 'probability49.bin')
                last_square = key['square']
            output = output_dir / (label + '.jsonl')
            command = [str(executable), received, ','.join(map(str, key['column_rank_order'])),
                       key['square'], '600', str(temporary / 'quad49.bin'),
                       str(temporary / 'probability49.bin'), label]
            with output.open('w') as stream:
                subprocess.run(command, stdout=stream, check=True)
            sha = hashlib.sha256(output.read_bytes()).hexdigest()
            records = [json.loads(line) for line in output.read_text().splitlines()]
            reports.append({'label': label, 'trials': records[0]['trials'], 'output': output.name,
                            'sha256': sha, 'matches_archived_output_byte_for_byte': sha == original_sha})
    report = {'completed': True, 'runs': reports,
              'all_archived_outputs_reproduced_exactly': all(x['matches_archived_output_byte_for_byte'] for x in reports),
              'caveat': 'Enumerating geometry and reproducing language scores does not establish or exclude a historical decryption.'}
    (output_dir / 'reproduction_report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
