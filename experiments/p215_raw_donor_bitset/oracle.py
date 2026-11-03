#!/usr/bin/env python3
"""Independent exhaustive miniature oracle: shared square, domains, ranks, loss."""
from itertools import permutations, combinations
from pathlib import Path
import argparse
import json
import random
import time

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDS = 'ADFGVX'


def squares(partial):
    missing_positions = [i for i, c in enumerate(partial) if c == '?']
    unused = sorted(set(ALPHABET) - set(partial))
    assert len(unused) == len(missing_positions)
    for assignment in permutations(unused):
        result = list(partial)
        for i, c in zip(missing_positions, assignment):
            result[i] = c
        yield ''.join(result)


def encode(text, square, width, order):
    stream = ''.join(COORDS[square.index(c)//6] + COORDS[square.index(c)%6] for c in text)
    indices = [i for col in order for i in range(col, len(stream), width)]
    return ''.join(stream[i] for i in indices), indices


def solve(case):
    domains = [set(d) for d in case['domains']]
    target = case['target']
    width = case['width']
    size = 2*len(domains)
    deletions = size - len(target)
    assert 0 <= deletions < size
    checks = 0
    # This intentionally uses direct exhaustive loops, no propagation bitset.
    for square in squares(case['square']):
        allowed = []
        for domain in domains:
            cells = [i for i, c in enumerate(square) if c in domain]
            allowed.append([(COORDS[i//6], COORDS[i%6]) for i in cells])
        for order in permutations(range(width)):
            interim_indices = [i for col in order for i in range(col, size, width)]
            for lost in combinations(range(size), deletions):
                checks += 1
                lost_set = set(lost)
                interim = ['?']*size
                cursor = 0
                for transmitted_index, interim_index in enumerate(interim_indices):
                    if transmitted_index not in lost_set:
                        interim[interim_index] = target[cursor]
                        cursor += 1
                chosen = []
                for position, pairs in enumerate(allowed):
                    a, b = interim[2*position:2*position+2]
                    pair = next(((x, y) for x, y in pairs if a in ('?', x) and b in ('?', y)), None)
                    if pair is None:
                        break
                    chosen.append(square[6*COORDS.index(pair[0])+COORDS.index(pair[1])])
                else:
                    text = ''.join(chosen)
                    ciphertext, _ = encode(text, square, width, order)
                    received = ''.join(c for i, c in enumerate(ciphertext) if i not in lost_set)
                    assert all(a == '?' or a == b for a, b in zip(target, received))
                    return {'feasible': True, 'checks': checks, 'witness': {
                        'square': square, 'order': list(order), 'lost': list(lost),
                        'plaintext': text, 'ciphertext': ciphertext, 'received': received}}
    return {'feasible': False, 'checks': checks, 'witness': None}


def generate():
    rng = random.Random(20261104215)
    base = 'QNZ72XS4C0IJY3RBEKL9FD6GMTHUVWA5O8P1'
    cases = []
    for number in range(36):
        width = 4
        length = 6 if number < 18 else 7 if number < 30 else 8
        unknown_count = 2 if number % 3 else 3
        unknown_cells = rng.sample(range(36), unknown_count)
        partial = ''.join('?' if i in unknown_cells else c for i, c in enumerate(base))
        used_unknown = [base[i] for i in unknown_cells]
        plaintext = ''.join(rng.choice(used_unknown if i < 3 else ALPHABET) for i in range(length))
        domains = []
        for i, c in enumerate(plaintext):
            extra = rng.sample(ALPHABET, (number+i) % 3)
            domains.append(''.join(sorted(set(c + ''.join(extra)))))
        order = list(range(width)); rng.shuffle(order)
        ciphertext, _ = encode(plaintext, base, width, order)
        lost = sorted(rng.sample(range(2*length), 1 + (number % 2)))
        target = ''.join(c for i, c in enumerate(ciphertext) if i not in lost)
        masked = set(rng.sample(range(len(target)), number % 3))
        target = ''.join('?' if i in masked else c for i, c in enumerate(target))
        if number % 3 == 2:
            target = ''.join(rng.choice(COORDS) if c != '?' else '?' for c in target)
        cases.append({'id': f'mini_{number:02d}', 'width': width, 'square': partial,
                      'domains': domains, 'target': target,
                      'construction': 'random target' if number % 3 == 2 else 'planted feasible',
                      'planted': None if number % 3 == 2 else {'plaintext': plaintext, 'order': order, 'lost': lost}})
    # Every position could independently call AA, AD or DA the letter Q, but
    # no single injective square may call all three cells Q. The source loss
    # and all column permutations are still exhaustively allowed by solve().
    partial = ''.join('?' if i in (0, 1, 6) else c for i, c in enumerate(base))
    interim = 'AAADDAAAADDA'
    transmitted = ''.join(interim[c::4] for c in range(4))
    cases.append({'id': 'global_coupling_counterexample', 'width': 4,
                  'square': partial, 'domains': ['Q']*6,
                  'target': transmitted[1:], 'construction': 'independent-cell relaxation trap',
                  'local_relaxation_witness': {'order': [0, 1, 2, 3], 'lost': [0],
                                               'interim': interim, 'ciphertext': transmitted,
                                               'label_reused_at_distinct_cells': 'Q'}})
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cases = json.loads(args.input.read_text())['cases'] if args.input else generate()
    result = []
    start = time.monotonic()
    for case in cases:
        solved = solve(case)
        if case.get('construction') == 'planted feasible':
            assert solved['feasible'], case['id']
        result.append(dict(case, oracle=solved))
    output = {'schema': 'p215-independent-miniature-oracle-v1',
              'scope': 'Every square completion, every column permutation, every transmitted deletion set; masks retained.',
              'seconds': time.monotonic()-start, 'cases': result,
              'feasible': sum(r['oracle']['feasible'] for r in result),
              'infeasible': sum(not r['oracle']['feasible'] for r in result)}
    args.output.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
