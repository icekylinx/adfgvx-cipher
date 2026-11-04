#!/usr/bin/env python3
"""Check an optional separator fill at the boundary of the p214 quotation."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.late_november_joint_completion.verify import CO, positions


def read(path):
    return json.loads((ROOT / path).read_text())


def build():
    data = json.loads((HERE / 'p214_completion_inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    prior = read('experiments/open_targets_continuation/certificates.json')
    r = next(r for r in prior['results'] if r['id'] == data['record'])
    donor = next(r for r in prior['results'] if r['id'] == 'p181_A')
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == r['key_id'])
    ranks, square = key['column_rank_order'], key['square']
    source, old = r['literal_ciphertext'], r['editorial']['ciphertext']
    before, bp = positions(old, ranks, square)
    p, i = data['plaintext_index'], data['source_index']
    assert before == r['editorial']['plaintext']
    assert source[i] == '-' and old[i] == '?'
    assert bp[p]['pair'] == '?X' and bp[p]['source_indices'] == [3, 189]
    assert bp[p]['domain'] == '1GJKWX'
    after_cipher = old[:i] + data['coordinate'] + old[i+1:]
    text, pp = positions(after_cipher, ranks, square)
    assert text[p] == data['symbol'] == 'X' and pp[p]['pair'] == 'AX'
    assert text[38:130] == donor['editorial']['plaintext']
    changes = [{'source_index': j, 'from': a, 'to': b}
               for j, (a, b) in enumerate(zip(source, after_cipher)) if a in CO and a != b]
    fills = [{'source_index': j, 'literal': a, 'to': b}
             for j, (a, b) in enumerate(zip(source, after_cipher)) if a not in CO and b in CO]
    assert len(changes) == 3 and len(fills) == 4
    assert [(x['source_index'], x['to']) for x in fills] == [(3, 'A'), (4, 'G'), (56, 'G'), (165, 'V')]
    assert text.count('?') == 1 and len(text) == 146
    witnesses = []
    for coordinate in CO:
        concrete = after_cipher[:78] + coordinate + after_cipher[79:]
        full = decrypt(concrete, ranks, square)
        assert encrypt(full, ranks, square) == concrete
        assert full[:130] == text[:130]
        witnesses.append({'remaining_source78': coordinate, 'remaining_plaintext143': full[143]})
    a, b = data['quote_span']
    quoted = text[a:b]
    labels = re.sub('[^A-Z0-9?]', '', data['german'].upper())
    assert labels == quoted.replace('X', '')
    assert '> ' + data['german'] in (ROOT / data['case']).read_text()
    return {
        'schema': 'adfgvx-p214-quote-boundary-v1', 'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'p214_completion_inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'id': data['record'], 'literal_ciphertext': source, 'earlier_edition': before,
        'edited_ciphertext': after_cipher, 'edited_plaintext': text,
        'fixed_before': len(before)-before.count('?'), 'fixed_after': len(text)-text.count('?'),
        'positions': len(text), 'additional_fill': {'source_index': i, 'from': '-', 'to': 'A',
                                                 'plaintext_index': p, 'symbol': 'X',
                                                 'earlier_domain': bp[p]['domain']},
        'observed_substitutions': changes, 'source_mask_fills': fills,
        'remaining_domain': pp[143], 'all_remaining_mask_witnesses': witnesses,
        'quote_span': data['quote_span'], 'quote_plaintext': quoted,
        'german': data['german'], 'assumption': data['assumption'], 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'p214_completion_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print('p214 quote boundary: 144→145/146; one optional separator fill; 3 substitutions + 4 fills total; footer erasure retained.')


if __name__ == '__main__':
    main()
