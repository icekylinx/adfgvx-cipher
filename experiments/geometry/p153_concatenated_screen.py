#!/usr/bin/env python3
"""Direct fixed-key screen of p153's two parts as one 240-coordinate stream.

Both part orders are tested. This low-prior hypothesis differs from applying
one key separately to two transposition rectangles. Source values and erasures
remain unchanged. The optional language score is a ranking aid, not a proof.
"""
from pathlib import Path
import argparse
import array
import hashlib
import json
import sys

COORDS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def transpose(stream, ranks):
    return ''.join(stream[column::len(ranks)]
                   for column in sorted(range(len(ranks)), key=lambda i: ranks[i]))


def decode(ciphertext, ranks, square):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    columns, offset = [None] * len(ranks), 0
    for column in sorted(range(len(ranks)), key=lambda i: ranks[i]):
        size = len(ciphertext) // len(ranks) + (column < len(ciphertext) % len(ranks))
        columns[column] = ciphertext[offset:offset + size]
        offset += size
    stream = ''.join(columns[column][row]
                     for row in range(max(map(len, columns)))
                     for column in range(len(ranks)) if row < len(columns[column]))
    assert transpose(stream, ranks) == ciphertext
    raw = ''.join(square[6 * COORDS.index(a) + COORDS.index(b)]
                  if a in COORDS and b in COORDS else '?'
                  for a, b in zip(stream[::2], stream[1::2]))
    return stream, raw


def score(plaintext, model):
    values = []
    for i in range(len(plaintext) - 3):
        window = plaintext[i:i + 4]
        if '?' in window:
            values.append(-7.4)
        else:
            index = 0
            for c in window:
                index = 36 * index + ALPHABET.index(c)
            values.append(float(model[index]))
    return sum(values) / len(values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    keys_path = args.repository / 'data/keys.json'
    messages_path = args.repository / 'data/messages.json'
    keys = json.loads(keys_path.read_text())['keys']
    messages = {row['id']: row for row in json.loads(messages_path.read_text())['messages']}
    parts = {mid: messages[mid]['transcript']['analysis_ciphertext'] for mid in ['p153a', 'p153b']}
    assert len(parts['p153a']) == 132 and len(parts['p153b']) == 108
    assert parts['p153a'].count('?') == 0 and parts['p153b'].count('?') == 15
    model = None
    if args.model:
        model = array.array('f')
        model.frombytes(args.model.read_bytes())
        if sys.byteorder != 'little':
            model.byteswap()
        assert len(model) == 36 ** 4
    rows = []
    for part_order in [('p153a', 'p153b'), ('p153b', 'p153a')]:
        ciphertext = ''.join(parts[mid] for mid in part_order)
        for key in keys:
            square = key['square'].replace('+', '?')
            stream, raw = decode(ciphertext, key['column_rank_order'], square)
            row = {'part_order': list(part_order), 'key_id': key['id'],
                   'square_known_cells': 36 - square.count('?'),
                   'raw_partial_plaintext': raw,
                   'fixed_plaintext_characters': len(raw) - raw.count('?'),
                   'intermediate_coordinate_stream': stream,
                   'coordinate_transposition_roundtrip': True,
                   'all_225_known_source_coordinates_preserved': True}
            if model is not None:
                row['ranking_score'] = score(raw, model)
            rows.append(row)
    key = next(k for k in keys if k['id'] == 'Nov7-9')
    body = ('INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHESZWISCHENDEUTSCHLAND'
            'UNDSOWJETREGIERUNGUNDERWARTUNGDERWIEDERHERSTELLUNGRUSSLANDS')[:120]
    assert len(body) == 120
    stream = ''.join(COORDS[key['square'].index(c) // 6] + COORDS[key['square'].index(c) % 6]
                     for c in body)
    full = transpose(stream, key['column_rank_order'])
    control_parts = [full[:132], full[132:137] + '?' * 15 + full[152:]]
    _, partial = decode(''.join(control_parts), key['column_rank_order'], key['square'])
    assert all(a == '?' or a == b for a, b in zip(partial, body))
    control = {'type': 'implementation control, not blind ranking validation',
               'key': key['id'], 'complete_plaintext': body, 'full_ciphertext': full,
               'observed_parts': control_parts, 'recovered_partial_plaintext': partial,
               'fixed_plaintext_characters': len(partial) - partial.count('?'),
               'all_fixed_characters_correct': True}
    output = {'format_version': 1, 'authors': ['icekylinx', 'GPT-6 Astra Pro'],
              'scope': __doc__, 'source_parts': parts,
              'source_headers': {mid: messages[mid]['source']['header_transcription'] for mid in parts},
              'source_model_prior': 'The separate CHI-132 and CHI-108 part headers favor separate rectangles; concatenation is a low-prior alternative tested explicitly.',
              'key_count': len(keys), 'tested_order_key_pairs': len(rows),
              'keys_without_any_attested_square_cell': [k['id'] for k in keys if k['square'] == '?' * 36],
              'key_snapshot': [{'id': k['id'], 'column_rank_order': k['column_rank_order'], 'square': k['square']} for k in keys],
              'input_sha256': {'keys': hashlib.sha256(keys_path.read_bytes()).hexdigest(),
                               'messages': hashlib.sha256(messages_path.read_bytes()).hexdigest()},
              'model_sha256': hashlib.sha256(args.model.read_bytes()).hexdigest() if args.model else None,
              'unknown_window_ranking_score': -7.4 if args.model else None,
              'positive_control': control,
              'candidates': sorted(rows, key=lambda r: r.get('ranking_score', 0.), reverse=True),
              'result': 'No newly accepted plaintext; direct fixed-key check only',
              'limits': 'No arbitrary unknown square or transposition, coordinate relabeling, source substitutions, or other fragment loss is searched here.'}
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'key_count': len(keys), 'tested_order_key_pairs': len(rows),
                      'positive_control_fixed_characters': control['fixed_plaintext_characters'],
                      'best_candidates': output['candidates'][:5]}, indent=2))


if __name__ == '__main__':
    main()
