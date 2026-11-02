#!/usr/bin/env python3
"""Reproduce exact even-width checks and seeded ragged-rectangle controls."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from math import comb
from pathlib import Path
import random
import subprocess

HERE = Path(__file__).resolve().parent
WIDTHS = [14, 16, 18, 20, 22, 24, 26]
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
CO = 'ADFGVX'


def encode(plaintext, ranks, square):
    stream = ''.join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in plaintext)
    return ''.join(stream[col::len(ranks)] for col in sorted(range(len(ranks)), key=lambda i: ranks[i]))


def decode_stream(ciphertext, ranks):
    width = len(ranks)
    columns = [''] * width
    offset = 0
    for col in sorted(range(width), key=lambda i: ranks[i]):
        length = len(ciphertext) // width + (col < len(ciphertext) % width)
        columns[col] = ciphertext[offset:offset + length]
        offset += length
    assert offset == len(ciphertext)
    return ''.join(columns[i % width][i // width] for i in range(len(ciphertext)))


def check_solutions(rows, input_text, width):
    crib, ciphertext, second, other = input_text.split()
    solutions = [row for row in rows if row['kind'] == 'solution']
    summary = rows[-1]
    assert summary['kind'] == 'summary' and summary['width'] == width
    assert summary['complete'], summary
    assert summary['segmentations'] == comb(width, 132 % width)
    assert summary['solutions'] == len(solutions)
    for solution in solutions:
        ranks, square = solution['ranks'], solution['partial_square']
        assert sorted(ranks) == list(range(1, width + 1))
        assert len(square) == 36 and len(set(square.replace('?', ''))) == len(square.replace('?', ''))
        stream = decode_stream(ciphertext, ranks)
        for i, letter in enumerate(crib):
            if letter != '?':
                cell = CO.index(stream[2 * i]) * 6 + CO.index(stream[2 * i + 1])
                assert square[cell] == letter
        # Build an independent fixed-length second rectangle. Unknown tail
        # positions stay unassigned and do not enter mismatch comparisons.
        inter = ''
        for letter in second.ljust(54, '?'):
            if letter == '?':
                inter += '??'
            else:
                cell = square.index(letter)
                inter += CO[cell // 6] + CO[cell % 6]
        prediction = ''.join(inter[col::width] for col in sorted(range(width), key=lambda i: ranks[i]))
        edits = [{'source_index': i, 'observed': a, 'proposed': b} for i, (a, b) in enumerate(zip(other, prediction))
                 if a != '?' and b != '?' and a != b]
        assert sorted(solution['edits'], key=lambda edit: edit['source_index']) == edits
        assert len(edits) == solution['second_crib_known_coordinate_mismatches']
    return summary


def run(engine, path, width):
    completed = subprocess.run([str(engine), str(path), str(width), '240', '100000000', '1000'],
                               text=True, capture_output=True, check=True)
    rows = [json.loads(line) for line in completed.stdout.splitlines()]
    summary = check_solutions(rows, path.read_text(), width)
    return completed.stdout, rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    engine = args.engine.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    control_dir = output / 'controls'
    control_dir.mkdir(exist_ok=True)
    historical = HERE / 'historical_input.txt'
    first, _, second, _ = historical.read_text().split()
    history, controls = [], []
    for width in WIDTHS:
        text, rows, summary = run(engine, historical, width)
        (output / f'historical_k{width}.jsonl').write_text(text)
        history.append(summary)
        seed = 2026110200 + width
        rng = random.Random(seed)
        square = list(AL); rng.shuffle(square); square = ''.join(square)
        ranks = list(range(1, width + 1)); rng.shuffle(ranks)
        truth1 = 'ANORDNUNGENVOM7TEN11TENNR232BEZIEHENLASSENSOWEITNOCHNICHTGESCHEHEN'
        truth2 = second + 'X4XGXR123BXA'
        cipher1 = encode(truth1, ranks, square)
        complete2 = encode(truth2, ranks, square)
        received2 = list(complete2); received2[5:20] = '?' * 15
        for index in [0, 1]:
            received2[index] = CO[(CO.index(received2[index]) + 1) % 6]
        received2 = ''.join(received2)
        path = control_dir / f'control_k{width}.txt'
        path.write_text('\n'.join([first, cipher1, second, received2]) + '\n')
        text, rows, summary = run(engine, path, width)
        (control_dir / f'control_k{width}.jsonl').write_text(text)
        matches = [row for row in rows if row['kind'] == 'solution' and row['ranks'] == ranks]
        assert len(matches) == 1
        assert sorted(edit['source_index'] for edit in matches[0]['edits']) == [0, 1]
        # The paired/transposed representation must also survive.
        equivalent = [ranks[i ^ 1] for i in range(width)]
        assert any(row['kind'] == 'solution' and row['ranks'] == equivalent for row in rows)
        controls.append({'width': width, 'seed': seed, 'truth_ranks': ranks, 'truth_square': square,
                         'truth_plaintexts': [truth1, truth2], 'source_erasures': list(range(5, 20)),
                         'deliberate_known_coordinate_errors': [0, 1],
                         'true_and_equivalent_ranks_present': True, 'summary': summary,
                         'truth_used_only_for_generation_and_verification': True})
    result = {'generated_utc': datetime.now(timezone.utc).isoformat(),
              'source_sha256': hashlib.sha256((HERE / 'enumerate_even.c').read_bytes()).hexdigest(),
              'input_sha256': hashlib.sha256(historical.read_bytes()).hexdigest(),
              'historical': history, 'controls': controls,
              'all_returned_keys_independently_reencrypted': True,
              'scope': 'Post-discovery exact consistency under the supplied first crib, even widths 14 through 26, standard per-part resetting and injective square. No unrestricted historical uniqueness or digit recovery claim.'}
    (output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'historical': [{'width': row['width'], 'complete': row['complete'], 'solutions': row['solutions']} for row in history],
                      'all_width_controls_verified': len(controls), 'output': str(output)}))


if __name__ == '__main__':
    main()
