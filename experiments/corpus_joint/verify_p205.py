#!/usr/bin/env python3
"""Audit the p205 source package against the independent project cipher.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This does not import build_readings.py or alter any source or key assignment.
"""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import (SYMBOLS, decrypt, plaintext_domains,
                          transposition_indices, untranspose)


def main():
    inputs = json.loads((HERE / 'p205_inputs.json').read_text())
    recorded = json.loads((HERE / 'p205_readings.json').read_text())
    catalogue = {k['id']: k for k in json.loads(
        (ROOT / 'data/keys.json').read_text())['keys']}
    keys = {k['id']: k for k in inputs['keys']}
    for key in keys.values():
        original = catalogue[key['id']]
        assert key['square'] == original['square']
        assert key['column_rank_order'] == original['column_rank_order']
    for source_image in inputs['source_images']:
        assert hashlib.sha256((HERE / source_image['path']).read_bytes()).hexdigest() == source_image['sha256']
    results = {r['id']: r for r in recorded['results']}
    assert set(results) == {r['id'] for r in inputs['records']}
    counts = dict(parts=0, coordinates=0, source_fixed=0,
                  plaintext_positions=0, editorial_substitutions=0,
                  remaining_unknown_positions=0)
    for source in inputs['records']:
        result = results[source['id']]
        key = keys[source['key_id']]
        cipher = ''.join(source['source_groups'])
        assert len(cipher) == source['advertised_length']
        assert set(cipher) <= set(SYMBOLS)
        ranks, square = key['column_rank_order'], key['square']
        plain = decrypt(cipher, ranks, square)
        domains = plaintext_domains(cipher, ranks, square)
        assert plain == result['source_plaintext']
        assert domains == result['plaintext_domains']
        stream = untranspose(cipher, ranks)
        transmitted_indices = transposition_indices(len(cipher), ranks)
        inverse = {interim: transmitted for transmitted, interim in enumerate(transmitted_indices)}
        maps = [[inverse[2*p], inverse[2*p+1]] for p in range(len(plain))]
        assert maps == result['plaintext_to_ciphertext_offsets']
        edited = list(cipher)
        expected_plain = list(plain)
        changes = []
        proposals = {p['plaintext_index']: p for p in source['editorial_readings']}
        assert len(proposals) == len(source['editorial_readings'])
        for p, proposal in proposals.items():
            char = proposal['proposed_symbol']
            cell = square.index(char)
            pair = SYMBOLS[cell // 6] + SYMBOLS[cell % 6]
            expected_plain[p] = char
            for index, value in zip(maps[p], pair):
                if cipher[index] != value:
                    changes.append((index, cipher[index], value))
                    edited[index] = value
        changed = ''.join(edited)
        assert decrypt(changed, ranks, square) == ''.join(expected_plain)
        assert ''.join(expected_plain) == result['editorial_plaintext']
        assert len(changes) == result['editorial_coordinate_cost']
        assert len(changes) == sum(a != b for a, b in zip(cipher, changed))
        recorded_changes = sorted((e['ciphertext_offset'], e['source'], e['proposed'])
            for proposal in result['editorial_readings']
            for e in proposal['coordinate_replacements'])
        assert sorted(changes) == recorded_changes
        for p, domain in enumerate(domains):
            cell = 6 * SYMBOLS.index(stream[2*p]) + SYMBOLS.index(stream[2*p+1])
            assert result['plaintext_cell_domains'][p] == [cell]
            if len(domain) == 1:
                assert square[cell] == domain
            elif p not in proposals:
                assert set(domain) <= set('0123456789')
        counts['parts'] += 1
        counts['coordinates'] += len(cipher)
        counts['source_fixed'] += len(plain) - plain.count('?')
        counts['plaintext_positions'] += len(plain)
        counts['editorial_substitutions'] += len(changes)
        counts['remaining_unknown_positions'] += ''.join(expected_plain).count('?')
    assert counts == dict(parts=6, coordinates=1514, source_fixed=750,
                         plaintext_positions=757, editorial_substitutions=4,
                         remaining_unknown_positions=6)
    b2 = results['p205_B2']
    assert b2['plaintext_domains'][0] == '03456789'
    assert b2['editorial_plaintext'].startswith('SIND')
    assert keys['Nov16-18']['square'][18] == 'S'
    print(json.dumps({'status': 'pass', **counts,
                     'scope': 'All source coordinates and key assignments remain unchanged in the base readings; editorial corrections are separately charged.'}, indent=2))


if __name__ == '__main__':
    main()
