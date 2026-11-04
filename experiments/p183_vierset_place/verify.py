#!/usr/bin/env python3
"""Price the p183 F Vierset-Barse correction without completing its numerals."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, transposition_indices


def read(path):
    return json.loads(path.read_text())


def build():
    data = read(HERE / 'inputs.json')
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    history = data['historical_source']
    assert hashlib.sha256((HERE / history['local_image']).read_bytes()).hexdigest() == history['image_sha256']
    key = next(k for k in read(ROOT / 'data/keys.json')['keys'] if k['id'] == data['key_id'])
    record = next(r for r in read(ROOT / 'experiments/jaeger_accommodation_area/certificates.json')['records'] if r['id'] == data['source_id'])
    square, ranks = key['square'], key['column_rank_order']
    source, previous = record['literal_source'], record['readable_candidate']
    before = previous['ciphertext']
    assert len(source) == len(before) == 230
    assert record['model_to_source_indices'] == list(range(230))
    assert source[170] == before[170] == 'D'
    after = before[:170] + 'X' + before[171:]
    old = decrypt(before, ranks, square)
    new = decrypt(after, ranks, square)
    assert old == previous['raw']
    assert old[83:97] == 'VIERSWTXBARSEX'
    assert new == old[:88] + 'E' + old[89:]
    assert new[83:97] == 'VIERSETXBARSEX'
    order = transposition_indices(230, ranks)
    origins = [order.index(176), order.index(177)]
    assert origins == [126, 170]
    assert ''.join(source[i] for i in origins) == 'VD'
    assert ''.join(after[i] for i in origins) == 'VX'
    substitutions = [{'source_index': i, 'from': a, 'to': b}
                     for i, (a, b) in enumerate(zip(source, after))
                     if a in 'ADFGVX' and a != b]
    fills = [{'source_index': i, 'from': a, 'to': b}
             for i, (a, b) in enumerate(zip(source, after)) if a not in 'ADFGVX' and a != b]
    assert substitutions == [{'source_index': 170, 'from': 'D', 'to': 'X'}, {'source_index': 180, 'from': 'X', 'to': 'F'}]
    assert [r['source_index'] for r in fills] == [182, 183]
    blanks = [i for i, c in enumerate(square) if c == '?']
    remaining = sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(square))
    assert remaining == list('56789') and len(blanks) == 5
    variants = []
    for assignment in itertools.permutations(remaining):
        full = list(square)
        for i, value in zip(blanks, assignment):
            full[i] = value
        full = ''.join(full)
        text = decrypt(after, ranks, full)
        assert text[83:97] == 'VIERSETXBARSEX'
        assert encrypt(text, ranks, full) == after
        variants.append(text)
    domains = plaintext_domains(after, ranks, square)
    assert [i for i, domain in enumerate(domains) if len(domain) != 1] == [8, 62, 109]
    assert len(new) - new.count('?') == 112
    page = (ROOT / 'cases/military/jaeger_accommodation_area.md').read_text()
    assert new in page and 'source **170 D→X**' in page
    return {'schema': 'p183-vierset-place-certificate-v1', 'id': 'p183_F',
            'old_plaintext': old, 'proposed_plaintext': new,
            'ciphertext': after, 'plaintext_positions': 115, 'fixed_positions': 112,
            'new_fixed_positions': 0, 'corrected_word': 'VIERSET',
            'changed_plaintext_index': 88, 'pair_origins': origins,
            'observed_substitutions': substitutions, 'source_mask_fills': fills,
            'source_exclusions': [], 'added_coordinates': [],
            'remaining_domains': {str(i): domains[i] for i in [8, 62, 109]},
            'complete_squares_checked': len(variants),
            'full_reencryptions_checked': len(variants)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    target = HERE / 'certificate.json'
    if args.verify:
        assert read(target) == result
    else:
        target.write_text(json.dumps(result, indent=2) + '\n')
    print('p183 F: Vierset-Barse; one additional substitution; all 120 square completions verified.')


if __name__ == '__main__':
    main()
