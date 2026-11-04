#!/usr/bin/env python3
"""Retain the adverse p191 quantity consequence of the shared Q assignment."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.late_november_joint_completion.verify import CO, completions, positions


def read(path):
    return json.loads((ROOT / path).read_text())


def build():
    data = json.loads((HERE / 'compatibility_inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov13-15b')
    ranks = key['column_rank_order']
    joint = read('experiments/nov13_joint_completion/inputs.json')['joint_square']
    record = next(r for r in read('experiments/boots_request/certificate.json')['records'] if r['id'] == data['record'])
    cipher = record['edition']['ciphertext']
    baseline, _ = positions(cipher, ranks, key['square'])
    text, ps = positions(cipher, ranks, joint)
    p = data['Q_position']
    assert ps[p]['pair'] == 'XX' and ps[p]['source_indices'] == data['Q_source_indices']
    assert all(record['framed_position_to_received_position_0based'][i] == i for i in ps[p]['source_indices'])
    a, b = data['quantity_span']
    assert baseline[a:b] == '?0?0' and text[a:b] == '?0Q0'
    ycell = CO.index('F') * 6 + CO.index('X')
    historical_y = read('experiments/tiflis_appointment/certificates.json')['conditional_key_layers']['layer1']['assignment']
    assert historical_y == {'key_id': 'Nov13-15b', 'coordinate_pair': 'FX',
                            'square_cell_index': ycell, 'symbol': 'Y'}
    with_y = joint[:ycell] + 'Y' + joint[ycell+1:]
    # Enumerate coordinate neighbours using the surviving square families.
    # The entire two-coordinate XX pair is observed, so a decimal value
    # requires at least one actual source substitution.
    alternatives = []
    for square in (joint, with_y):
        possible = set()
        for full in completions(square):
            for side, index in enumerate(ps[p]['source_indices']):
                for coordinate in CO:
                    if coordinate == cipher[index]:
                        continue
                    pair = list('XX')
                    pair[side] = coordinate
                    symbol = full[CO.index(pair[0]) * 6 + CO.index(pair[1])]
                    if symbol.isdigit():
                        possible.add((index, coordinate, symbol))
        alternatives.append([{'source_index': i, 'coordinate': c, 'digit': v}
                             for i, c, v in sorted(possible)])
    assert [(x['source_index'], x['coordinate'], x['digit']) for x in alternatives[0]] == [
        (102, 'D', '0'), (102, 'F', '3'), (102, 'F', '4'),
        (102, 'F', '7'), (102, 'F', '8'), (102, 'F', '9')]
    assert alternatives[1] == [{'source_index': 102, 'coordinate': 'D', 'digit': '0'}]
    repair = data['optional_numeric_repair']
    assert record['literal_source'][repair['source_index']] == repair['from'] == 'X'
    repaired = cipher[:repair['source_index']] + repair['to'] + cipher[repair['source_index']+1:]
    after, _ = positions(repaired, ranks, with_y)
    assert after[a:b] == '?000'
    quantities = set()
    squares = list(completions(with_y))
    assert len(squares) == 120
    for full in squares:
        concrete = decrypt(repaired, ranks, full)
        quantities.add(concrete[a:b])
        assert encrypt(concrete, ranks, full) == repaired
    assert quantities == {'3000', '4000', '7000', '8000', '9000'}
    case = (ROOT / data['case']).read_text()
    assert '`?0Q0`' in case and '`?000`' in case and 'source position 102' in case
    return {
        'schema': 'adfgvx-nov13-quantity-compatibility-v1', 'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'compatibility_inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'record': data['record'], 'published_edition': baseline,
        'joint_interpretation': text, 'Q_position': ps[p],
        'one_coordinate_decimal_repairs_without_Y': alternatives[0],
        'one_coordinate_decimal_repairs_with_Y': alternatives[1],
        'optional_repaired_ciphertext': repaired, 'optional_repaired_text': after,
        'additional_observed_substitution': repair, 'additional_mask_fills': [],
        'quantity_candidates': sorted(quantities), 'full_squares_with_Y': len(squares),
        'counted_as_recovered_positions': 0, 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'compatibility_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('p191 Q compatibility: native quantity ?0Q0; with independent FX=Y, unique one-coordinate decimal repair gives ?000; no recovery gain counted.')


if __name__ == '__main__':
    main()
