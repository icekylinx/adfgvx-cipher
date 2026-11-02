"""Refine one ranked pairing candidate without using a control key or text."""
from pathlib import Path
import argparse
import hashlib
import heapq
import json
import subprocess

from cipher import cells, decrypt, encrypt, mismatches, untranspose

ROOT = Path(__file__).resolve().parent.parent


def best(lines):
    return max((json.loads(line) for line in lines.splitlines()), key=lambda row: row['score'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', required=True)
    parser.add_argument('--candidates', required=True, type=Path)
    parser.add_argument('--rank', type=int, default=0, help='Zero-based descending profile rank')
    parser.add_argument('--models', type=Path, default=ROOT/'models')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--seed', type=int, default=2026110281)
    parser.add_argument('--initial-restarts', type=int, default=50)
    parser.add_argument('--restarts', type=int, default=100)
    parser.add_argument('--iterations', type=int, default=60000)
    parser.add_argument('--component-columns', action='store_true',
                        help='Refine individual component columns after the fixed-pair stage')
    parser.add_argument('--component-restarts', type=int, default=100)
    parser.add_argument('--component-iterations', type=int, default=100000)
    parser.add_argument('--exact-restarts', type=int, default=30)
    parser.add_argument('--exact-iterations', type=int, default=60000)
    parser.add_argument('--six-weight', type=float, default=.7)
    args = parser.parse_args()
    if args.rank < 0: parser.error('rank must be nonnegative')
    cases = json.loads((ROOT/'cases/cases.json').read_text())['cases']
    case = next(row for row in cases if row['id'] == args.case)
    heap = []
    for index, line in enumerate(args.candidates.open()):
        row = json.loads(line)
        item = (row['profile_score'], -index, row)
        if len(heap) <= args.rank: heapq.heappush(heap, item)
        elif item[:2] > heap[0][:2]: heapq.heapreplace(heap, item)
    if len(heap) <= args.rank: raise ValueError('Requested rank exceeds candidate count')
    candidate = sorted(heap, reverse=True)[args.rank][2]
    ciphertexts = case['ciphertexts']
    assert [cells(ct, candidate['ranks']) for ct in ciphertexts] == candidate['cells']
    model = args.models/'german_military37_quad_marginal.bin'
    proc = subprocess.run([str(ROOT/'bin/subsolve_marginal'), str(model),
                           '|'.join(candidate['cells']), str(args.initial_restarts),
                           '30000', str(args.seed)], capture_output=True, text=True, check=True)
    initial = best(proc.stdout)
    width = len(candidate['ranks'])
    raw = f'{model} {width} {args.restarts} {args.iterations} {args.seed+1} 2\n'
    raw += initial['square']+'\n'+' '.join(map(str, candidate['ranks']))+'\n'
    raw += '\n'.join(ciphertexts)+'\n'
    proc = subprocess.run([str(ROOT/'bin/pair_marginal')], input=raw,
                          capture_output=True, text=True, check=True)
    pair = best(proc.stdout)
    assert [decrypt(ct, pair['ranks'], pair['square']) for ct in ciphertexts] == pair['plaintexts']
    component = None
    current = pair
    if args.component_columns:
        raw = f'{model} {width} {args.component_restarts} {args.component_iterations} {args.seed+2} 2\n'
        raw += pair['square']+'\n'+' '.join(map(str, pair['ranks']))+'\n'
        raw += '\n'.join(ciphertexts)+'\n'
        proc = subprocess.run([str(ROOT/'bin/joint_rectangle_warm')], input=raw,
                              capture_output=True, text=True, check=True)
        component = best(proc.stdout)
        assert [decrypt(ct, component['ranks'], component['square']) for ct in ciphertexts] == component['plaintexts']
        current = component
    interims = [untranspose(ct, current['ranks']) for ct in ciphertexts]
    proc = subprocess.run([str(ROOT/'bin/joint_domain_subsolve6'),
                           str(args.models/'german_military36_quad.bin'),
                           str(args.models/'german_military36_sixgram.bin'),
                           str(args.six_weight), '|'.join(interims),
                           str(args.exact_restarts), str(args.exact_iterations),
                           str(args.seed+3 if args.component_columns else args.seed+2), current['square']],
                          capture_output=True, text=True, check=True)
    final = best(proc.stdout)
    assert [decrypt(ct, current['ranks'], final['square']) for ct in ciphertexts] == final['plaintexts']
    evaluation = None
    if 'plaintexts' in case:
        regenerated = [encrypt(text, current['ranks'], final['square']) for text in case['plaintexts']]
        differences = [mismatches(ct, out) for ct, out in zip(ciphertexts, regenerated)]
        evaluation = dict(observed_coordinate_mismatch_positions=differences,
                          every_observed_coordinate_matches=not any(differences),
                          evaluation_key_never_supplied_to_search=True)
    record = dict(case=args.case, selected_profile_rank_zero_based=args.rank,
                  input_candidate=candidate, initial_square_fit=initial,
                  wildcard_pair_refinement=pair, component_column_refinement=component,
                  exact_coordinate_refinement=final,
                  ranks=current['ranks'], interims=interims, evaluation=evaluation,
                  seed=args.seed, independent_decryption_checks=True,
                  model_hashes={path.name:hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in [model,args.models/'german_military36_quad.bin',
                                             args.models/'german_military36_sixgram.bin']},
                  scope='Bounded heuristic candidate refinement; score alone is not a historical plaintext certificate.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2))
    print(json.dumps({'output': str(args.output), 'score': final['score'], 'evaluation': evaluation}))


if __name__ == '__main__': main()
