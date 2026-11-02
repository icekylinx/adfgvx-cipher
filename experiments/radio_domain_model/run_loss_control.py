#!/usr/bin/env python3
"""Replay a matched control under a selected frozen radio or book objective.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Control truth is used for evaluation only and is never passed to the engine.
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
parser.add_argument('--variant', choices=['36', 'class', 'numeric'], required=True)
parser.add_argument('--control', type=int, required=True, help='Zero-based index in the selected dataset')
parser.add_argument('--model', choices=['book', 'radio', 'book_class', 'radio_class'], required=True)
parser.add_argument('--engine', type=Path, required=True)
parser.add_argument('--quad', type=Path, required=True)
parser.add_argument('--lexicon', type=Path, required=True, help='Loaded by the engine but unused at word weight zero')
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--seconds', type=float, default=120)
args = parser.parse_args()
assert args.seconds > 0
dataset_name, report_name = {
    '36': ('dataset.json', 'loss_controls.json'),
    'class': ('class_dataset.json', 'class_loss_controls.json'),
    'numeric': ('numeric_dataset.json', 'numeric_loss_controls.json'),
}[args.variant]
dataset = json.loads((HERE / dataset_name).read_text())
report = json.loads((HERE / report_name).read_text())
assert 0 <= args.control < len(dataset['controls'])
case = dataset['controls'][args.control]
assert args.variant == 'numeric' or args.model in ('book', 'radio')
name = args.model + '_class' if args.variant == 'class' else args.model
row = next(r for r in report['results'] if r['control_id'] == case['id'] and r['model'] == name)
assert witness.sha(args.quad) == report['model_sha256'][name]
assert witness.sha(args.lexicon) == json.loads((HERE.parent / 'p198_word_search/lexicon_provenance.json').read_text())['lexicon_sha256']
witness.validate_input(case['column_rank_order'], case['partial_square'], case['received_ciphertext'])
args.output.mkdir(parents=True, exist_ok=True)
input_path = args.output / 'input.txt'
input_path.write_text(f"{len(case['column_rank_order'])} 5\n{case['partial_square']}\n" +
                      ' '.join(map(str, case['column_rank_order'])) + '\n' + case['received_ciphertext'] + '\n')
path = args.output / 'events.jsonl'
with path.open('w') as stream:
    subprocess.run([str(args.engine.resolve()), str(args.quad.resolve()),
                    str(args.lexicon.resolve()), str(input_path.resolve()),
                    str(args.seconds), '0', str(row['seed']), '-'],
                   stdout=stream, check=True)
final = json.loads(path.read_text().splitlines()[-1])
witness.check_witness(final, case['column_rank_order'], case['partial_square'], case['received_ciphertext'])
print(json.dumps({'control': case['id'], 'model': name,
                  'correct_characters': sum(a == b for a, b in zip(case['truth'], final['plaintext'])),
                  'completed_mutation_proposals': final['proposal'], 'candidate': final['plaintext']}, indent=2))
