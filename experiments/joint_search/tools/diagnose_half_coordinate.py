"""Reproduce a post-search control objective diagnostic, not a blind recovery."""
from pathlib import Path
import argparse
import json
import subprocess

from cipher import ALPHABET, cells, encrypt, mismatches, untranspose

ROOT = Path(__file__).resolve().parent.parent


def splitmix(state):
    mask = (1 << 64) - 1
    state = (state + 0x9e3779b97f4a7c15) & mask
    value = state
    value = ((value ^ (value >> 30))*0xbf58476d1ce4e5b9) & mask
    value = ((value ^ (value >> 27))*0x94d049bb133111eb) & mask
    return state, value ^ (value >> 31)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', default='fresh_control_k18')
    parser.add_argument('--letter', default='K')
    parser.add_argument('--models', type=Path, default=ROOT/'models')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if len(args.letter) != 1 or args.letter not in ALPHABET:
        parser.error('letter must be one alphabet character')
    fixture = next(row for row in json.loads((ROOT/'cases/cases.json').read_text())['cases']
                   if row['id'] == args.case)
    if 'plaintexts' not in fixture:
        parser.error('This diagnostic requires an invented control with evaluation truth')
    record = next(row for row in json.loads((ROOT/'results/control_certificates.json').read_text())
                  if row['case'] == args.case and row['stage'] == 'component_columns_then_exact_coordinate_refinement')
    ranks, initial = record['ranks'], record['square']
    known = {ALPHABET.index(ch) for ct in fixture['ciphertexts'] for ch in cells(ct,ranks) if ch != '?'}
    free = [index for index in range(36) if index not in known]
    old = initial.index(args.letter)
    if old not in free:
        parser.error('The chosen letter occurs in a fully observed cell')
    for seed in range(10000):
        state, a = splitmix(seed)
        _, b = splitmix(state)
        if a % 36 == b % 36:
            break
    interims = '|'.join(untranspose(ct,ranks) for ct in fixture['ciphertexts'])
    results = []
    for weight in [0.0,.7,1.0]:
        alternatives = []
        for target in free:
            square = list(initial)
            square[old],square[target] = square[target],square[old]
            square = ''.join(square)
            proc = subprocess.run([str(ROOT/'bin/joint_domain_subsolve6'),
                str(args.models/'german_military36_quad.bin'),str(args.models/'german_military36_sixgram.bin'),
                str(weight),interims,'1','1',str(seed),square],
                capture_output=True,text=True,check=True)
            result = json.loads(proc.stdout.splitlines()[-1])
            assert result['square'] == square, 'The score-only proposal must be skipped'
            differences = [mismatches(ct,encrypt(text,ranks,square))
                           for ct,text in zip(fixture['ciphertexts'],fixture['plaintexts'])]
            alternatives.append(dict(letter_cell=target,score=result['score'],
                                     observed_coordinate_mismatches=differences))
        alternatives.sort(key=lambda row:row['score'],reverse=True)
        results.append(dict(sixgram_weight=weight,alternatives=alternatives))
    output = dict(case=args.case,letter=args.letter,free_cells=len(free),score_only_seed=seed,
                  weights=results,control_truth_used_only_to_label_scored_alternatives=True,
                  scope='This post-search diagnostic is not an accepted blind plaintext recovery.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'scored_alternatives':3*len(free)}))


if __name__ == '__main__':
    main()
