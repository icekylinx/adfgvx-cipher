#!/usr/bin/env python3
"""Reproduce one declared stochastic case with validated inputs.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Wall-clock budgets make proposal totals hardware dependent. The seed fixes
the proposal stream, not the number reached on a different computer.
"""
import argparse
import json
from pathlib import Path
import subprocess

from verify import HERE, check_witness, sha, validate_input

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', required=True, help='The case_id in records.json')
parser.add_argument('--engine', type=Path, required=True)
parser.add_argument('--quad', type=Path, required=True)
parser.add_argument('--lexicon', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--seconds', type=float, help='Explicit override; otherwise use recorded budget')
args = parser.parse_args()
records = json.loads((HERE / 'records.json').read_text())
row = next(r for r in records['completed'] if r['case_id'] == args.case)
job = row['input']
validate_input(job['ranks'], job['partial_square'], job['source'])
assert sha(args.quad) == records['quad_model_sha256']
assert sha(args.lexicon) == records['lexicon_sha256']
assert args.engine.is_file()
seconds = args.seconds if args.seconds is not None else job['seconds']
assert seconds > 0
args.output.mkdir(parents=True, exist_ok=True)
input_path = args.output / 'input.txt'
input_path.write_text(f"{len(job['ranks'])} 5\n{job['partial_square']}\n" +
                      ' '.join(map(str, job['ranks'])) + '\n' + job['source'] + '\n')
seed_path = '-'
if row.get('initial_state'):
    initial = row['initial_state']
    check_witness(initial, job['ranks'], job['partial_square'], job['source'])
    path = args.output / 'initial.txt'
    path.write_text(initial['square'] + '\n' + ' '.join(map(str, initial['loss'])) +
                    '\n' + initial['fill'] + '\n')
    seed_path = str(path.resolve())
path = args.output / 'events.jsonl'
with path.open('w') as stream:
    subprocess.run([str(args.engine.resolve()), str(args.quad.resolve()),
                    str(args.lexicon.resolve()), str(input_path.resolve()),
                    str(seconds), str(job['word_weight']), str(job['seed']), seed_path],
                   stdout=stream, check=True)
events = [json.loads(line) for line in path.read_text().splitlines()]
final = events[-1]
check_witness(final, job['ranks'], job['partial_square'], job['source'])
print(json.dumps({'case': args.case, 'completed_mutation_proposals': final['proposal'],
                  'completed_restarts': final['restart'], 'final_score': final['score'],
                  'candidate': final['plaintext'], 'accepted_historical_reading': False}, indent=2))
