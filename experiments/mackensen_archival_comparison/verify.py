#!/usr/bin/env python3
"""Audit the cipher-side costs of the independent Berlin signature witness."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, untranspose

CO = 'ADFGVX'


def read(name):
    return json.loads((ROOT / name).read_text())


def build():
    data = json.loads((HERE / 'inputs.json').read_text())
    for name, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    original = read('experiments/corpus_extension/inputs.json')
    earlier = read('experiments/corpus_extension/certificates.json')
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov28-Dec1')
    square, ranks = key['square'], key['column_rank_order']
    record = next(r for r in original['records'] if r['id'] == 'p227_A4')
    src = ''.join(''.join(record['source_rows']).split())
    assert len(src) == 392 and all(c in CO for c in src)
    raw = decrypt(src, ranks, square)
    assert raw == record['expected_model_raw']
    n, width = len(src), len(ranks)
    heights = [n // width + (c < n % width) for c in range(width)]
    starts = [sum(heights[d] for d in range(width) if ranks[d] < ranks[c])
              for c in range(width)]
    mapping = [starts[p % width] + p // width for p in range(n)]
    assert ''.join(src[i] for i in mapping) == untranspose(src, ranks)
    target = raw
    evidence = []
    for field in data['signatures']:
        old, new = field['raw'], field['supported_surname']
        at = raw.index(old)
        assert at == field['plaintext_start'] and len(old) == len(new)
        changed_positions = [p for p, (a, b) in enumerate(zip(old, new), at) if a != b]
        assert len(changed_positions) == 1
        p = changed_positions[0]
        pair = ''.join(src[i] for i in mapping[2*p:2*p+2])
        plaintext = raw[:at] + new + raw[at+len(old):]
        edited = encrypt(plaintext, ranks, square)
        changes = [{'source_index': i, 'from': a, 'to': b}
                   for i, (a, b) in enumerate(zip(src, edited)) if a != b]
        assert len(changes) == 1 and decrypt(edited, ranks, square) == plaintext
        evidence.append({**field, 'changed_plaintext_index': p,
                         'source_indices': mapping[2*p:2*p+2],
                         'raw_pair': pair, 'coordinate_change': changes[0]})
        target = target.replace(old, new)
    name_cipher = encrypt(target, ranks, square)
    assert sum(a != b for a, b in zip(src, name_cipher)) == 2
    assert decrypt(name_cipher, ranks, square) == target
    old_record = next(r for r in earlier['records'] if r['id'] == 'p227_A4')
    prices = {}
    for candidate in record['editorial_candidates']:
        candidate_cipher = encrypt(candidate['plaintext'], ranks, square)
        changes = [{'source_index': i, 'from': a, 'to': b}
                   for i, (a, b) in enumerate(zip(src, candidate_cipher)) if a != b]
        existing = next(c for c in old_record['editorial_candidates'] if c['id'] == candidate['id'])
        assert changes == [{k: change[k] for k in ('source_index', 'from', 'to')}
                           for change in existing['known_coordinate_substitutions']]
        prices[candidate['id']] = len(changes)
    assert prices == {'readable': 12, 'molkenbuhr_proposal': 13}
    first = next(r for r in original['records'] if r['id'] == 'p226_C1')
    assert data['noun_variants']['raw'] in first['expected_model_raw']
    lengths = {name: len(word) for name, word in data['noun_variants'].items()}
    assert lengths == {'raw': 9, 'earlier_publication': 11, 'archival_counterpart': 8}
    page = (ROOT / data['case']).read_text()
    for row in data['case_table_rows']:
        assert row in page
    return {'schema': 'adfgvx-mackensen-archival-comparison-certificate-v1',
            'input_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
            'source_slots': len(src), 'baseline_plaintext': raw,
            'signatures': evidence, 'signature_only_ciphertext': name_cipher,
            'signature_only_plaintext': target, 'signature_coordinate_changes': 2,
            'existing_full_edition_costs': prices, 'noun_lengths': lengths,
            'new_cipher_positions_claimed': 0,
            'new_result': 'Independent documentary support for earlier surname proposals; explicit version comparison.',
            'case_signature_table_verified': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Berlin witness: two surname repairs at one coordinate each; existing 12/13-edit editions preserved; noun lengths 9/11/8.')


if __name__ == '__main__':
    main()
