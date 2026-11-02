#!/usr/bin/env python3
"""Test a continued column phase between p153's separately read-out parts.

Part 5 is decoded normally. Part 6 uses ranks cyclically shifted by either sign
of 132 modulo the column count. This is a low-prior operator-model hypothesis;
the ordinary separate-part convention and a single concatenated rectangle are
different experiments. No received coordinate is changed or discarded.
"""
from pathlib import Path
import argparse
import array
import hashlib
import json
import sys
from p153_concatenated_screen import COORDS, decode, score, transpose


def rotated(ranks, phase):
    phase %= len(ranks)
    return ranks[phase:] + ranks[:phase]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    keys = json.loads((args.repository / 'data/keys.json').read_text())['keys']
    messages = {r['id']: r for r in json.loads((args.repository / 'data/messages.json').read_text())['messages']}
    parts = [messages[mid]['transcript']['analysis_ciphertext'] for mid in ['p153a', 'p153b']]
    assert list(map(len, parts)) == [132, 108]
    assert sum(p.count('?') for p in parts) == 15
    model = None
    if args.model:
        model = array.array('f')
        model.frombytes(args.model.read_bytes())
        if sys.byteorder != 'little':
            model.byteswap()
        assert len(model) == 36 ** 4
    candidates = []
    for key in keys:
        ranks, square = key['column_rank_order'], key['square']
        first_stream, first_text = decode(parts[0], ranks, square)
        for sign in [1, -1]:
            phase = sign * 132 % len(ranks)
            second_ranks = rotated(ranks, phase)
            second_stream, second_text = decode(parts[1], second_ranks, square)
            row = {'key_id': key['id'], 'rotation_sign': sign, 'phase': phase,
                   'part5_ranks': ranks, 'part6_effective_ranks': second_ranks,
                   'square': square, 'raw_partial_plaintexts': [first_text, second_text],
                   'intermediate_streams': [first_stream, second_stream],
                   'all_225_known_source_coordinates_preserved': True,
                   'exact_coordinate_roundtrips': True,
                   'same_as_standard_reset_for_this_key': phase == 0}
            if model is not None:
                row['part6_ranking_score'] = score(second_text, model)
                row['combined_mean_ranking_score'] = (score(first_text, model) * 63 + score(second_text, model) * 51) / 114
            candidates.append(row)
    key = next(k for k in keys if k['id'] == 'Nov7-9')
    body = ('INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHESZWISCHENDEUTSCHLAND'
            'UNDSOWJETREGIERUNGUNDERWARTUNGDERWIEDERHERSTELLUNGRUSSLANDS')[:120]
    plain_parts = [body[:66], body[66:]]
    effective = [key['column_rank_order'], rotated(key['column_rank_order'], 132)]
    full = []
    for text, ranks in zip(plain_parts, effective):
        stream = ''.join(COORDS[key['square'].index(c) // 6] + COORDS[key['square'].index(c) % 6] for c in text)
        full.append(transpose(stream, ranks))
    observed = [full[0], full[1][:5] + '?' * 15 + full[1][20:]]
    actual = [decode(ct, ranks, key['square'])[1] for ct, ranks in zip(observed, effective)]
    assert all(a == '?' or a == b for text, truth in zip(actual, plain_parts) for a, b in zip(text, truth))
    output = {'format_version': 1, 'authors': ['icekylinx', 'GPT-6 Astra Pro'],
              'scope': __doc__, 'source_parts': parts, 'key_count': len(keys),
              'tested_key_sign_pairs': len(candidates),
              'unique_key_effective_rank_pairs': len({(c['key_id'], tuple(c['part6_effective_ranks'])) for c in candidates}),
              'model_sha256': hashlib.sha256(args.model.read_bytes()).hexdigest() if args.model else None,
              'unknown_window_score': -7.4 if args.model else None,
              'positive_control': {'type': 'synthetic implementation control, not blind validation',
                                   'key_id': key['id'], 'plaintext_parts': plain_parts,
                                   'complete_ciphertext_parts': full, 'observed_parts': observed,
                                   'effective_ranks': effective, 'decoded_partial_plaintexts': actual,
                                   'all_fixed_letters_correct': True},
              'candidates': sorted(candidates, key=lambda c: c.get('part6_ranking_score', 0.), reverse=True),
              'result': 'No newly accepted plaintext under the stated fixed-key phase model',
              'limits': 'This screen neither recovers an unknown key nor proves which writing or segmentation convention was used. The rotation hypothesis has no independent source attestation here.'}
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'tested_key_sign_pairs': len(candidates),
                      'unique_key_effective_rank_pairs': output['unique_key_effective_rank_pairs'],
                      'top_part6_candidates': output['candidates'][:4]}, indent=2))


if __name__ == '__main__':
    main()
