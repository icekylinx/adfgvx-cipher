#!/usr/bin/env python3
"""Replay a completed conditional p198 search with all received coordinates kept.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The historical surname-to-key condition remains an explicit hypothesis.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('loss_witness', HERE.parent / 'p198_word_search/verify.py')
witness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(witness)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', required=True)
parser.add_argument('--engine', type=Path, required=True)
parser.add_argument('--quad', type=Path, required=True)
parser.add_argument('--lexicon', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--seconds', type=float)
args = parser.parse_args()
report = json.loads((HERE / 'conditional_targets.json').read_text())
job = next(j for j in report['jobs'] if j['id'] == args.case)
assert witness.sha(args.quad) == job['model_sha256']
assert witness.sha(args.lexicon) == report['lexicon_sha256']
witness.validate_input(job['column_rank_order'], job['partial_square'], job['received_ciphertext'])
seconds = job['seconds'] if args.seconds is None else args.seconds
assert seconds > 0
args.output.mkdir(parents=True, exist_ok=True)
path = args.output / 'input.txt'
path.write_text(f"{len(job['column_rank_order'])} 5\n{job['partial_square']}\n" +
                ' '.join(map(str, job['column_rank_order'])) + '\n' +
                job['received_ciphertext'] + '\n')
log = args.output / 'events.jsonl'
with log.open('w') as stream:
    subprocess.run([str(args.engine.resolve()), str(args.quad.resolve()),
                    str(args.lexicon.resolve()), str(path.resolve()), str(seconds),
                    str(job['word_weight']), str(job['seed']), '-'], stdout=stream, check=True)
final = json.loads(log.read_text().splitlines()[-1])
witness.check_witness(final, job['column_rank_order'], job['partial_square'], job['received_ciphertext'])
print(json.dumps({'case': job['id'], 'condition': job['condition'],
                  'completed_mutation_proposals': final['proposal'],
                  'candidate': final['plaintext'], 'accepted_historical_reading': False}, indent=2))
