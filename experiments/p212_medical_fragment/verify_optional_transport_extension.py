#!/usr/bin/env python3
"""Verify the optional thirteen-half extension and one global conditional square."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify():
    spec = importlib.util.spec_from_file_location('primary_verifier', HERE / 'verify.py')
    primary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(primary)
    primary.verify()
    data = json.loads((HERE / 'optional_transport_extension.json').read_text())
    inputs = json.loads((HERE / 'inputs.json').read_text())
    certificate = json.loads((HERE / 'certificates.json').read_text())
    earlier = json.loads((HERE / 'optional_underpersonal.json').read_text())
    assert sha(HERE / 'inputs.json') == data['base_input_sha256']
    assert sha(HERE / 'certificates.json') == data['base_certificate_sha256']
    assert sha(HERE / 'optional_underpersonal.json') == data['base_underpersonal_sha256']
    record = certificate['record']
    square = inputs['key']['square']
    ranks = inputs['key']['column_rank_order']
    frame = list(record['primary']['ciphertext'])
    for fill in earlier['additional_inserted_coordinate_fills']:
        assert frame[fill['model_index']] == '?'
        frame[fill['model_index']] = fill['to']
    _, _, previous_output = primary.decode(''.join(frame), ranks, square)
    assert previous_output == earlier['optional_output']
    permutation = primary.layout(302, ranks)
    expected_fills = []
    assert data['spans'] == [{'start': 70, 'text': 'XZU9EDEM'},
                             {'start': 87, 'text': 'ZUGYARZT'}]
    for span in data['spans']:
        for position, character in enumerate(span['text'], span['start']):
            assert character in record['raw_domains'][position]
            assert previous_output[position] in ('?', character)
            cell = square.index(character)
            for side, value in enumerate((COORDINATES[cell // 6], COORDINATES[cell % 6])):
                index = permutation[2 * position + side]
                if frame[index] == '?':
                    assert index < 105
                    expected_fills.append({'model_index': index, 'source_index': None,
                                           'plaintext_index': position, 'pair_side': side,
                                           'from': '?', 'to': value, 'selected_label': character})
                    frame[index] = value
                else:
                    assert frame[index] == value
    assert len(expected_fills) == 13
    assert sorted(expected_fills, key=lambda x: x['model_index']) == data['additional_inserted_coordinate_fills']
    frame = ''.join(frame)
    interim, domains, output = primary.decode(frame, ranks, square)
    assert output == data['optional_output']
    assert len(output) == 151 and output.count('?') == frame.count('?') == 3
    assert [i for i, c in enumerate(output) if c == '?'] == data['unresolved_plaintext_positions'] == [8, 9, 10]
    assert frame[105:] == record['literal_source']
    assert data['source_observations_preserved'] == len(record['literal_source']) == 197
    assert all(old == '?' or old == new for old, new in zip(previous_output, output))
    assert sum(old != new for old, new in zip(previous_output, output)) == 13
    assert data['unresolved_domains'] == [
        {'plaintext_index': i, 'labels': domains[i]} for i in (8, 9, 10)]
    opening_ciphertexts = set()
    for labels in itertools.product(*(domains[i] for i in (8, 9, 10))):
        complete = list(output)
        for i, label in zip((8, 9, 10), labels):
            complete[i] = label
        ciphertext = primary.encrypt(''.join(complete), ranks, square)
        assert ciphertext[105:] == record['literal_source']
        assert all(a == '?' or a == b for a, b in zip(frame, ciphertext))
        opening_ciphertexts.add(ciphertext)
    assert len(opening_ciphertexts) == data['compatible_opening_completions'] == 216
    assert data['prices'] == {'additional_inserted_slot_fills': 13,
                              'total_inserted_slot_fills': 102,
                              'fixed_optional_positions': 148,
                              'plaintext_positions': 151,
                              'remaining_unassigned_inserted_slots': 3,
                              'observed_coordinate_substitutions': 0,
                              'source_mask_fills': 0}
    assert output[68:71] == data['literal_field_boundaries']['plaintext68_71'] == '3XX'
    for field in data['unchanged_field_source_witnesses']:
        position = record['positions'][field['plaintext_index']]
        assert field == {'plaintext_index': position['plaintext_index'],
                         'baseline_label': position['raw'], 'pair': position['pair'],
                         'model_indices': position['model_indices'],
                         'source_indices': position['source_indices']}
    witness = data['full_baseline_feasibility_witness']
    assert witness['ciphertext'] == frame.replace('?', 'A')
    assert primary.encrypt(witness['plaintext'], ranks, square) == witness['ciphertext']
    assert witness['ciphertext'][105:] == record['literal_source']
    alternative = data['source_compatible_alternative']
    assert alternative['start'] == 87 and alternative['text'] == 'ZUGYACHT'
    for position, character in enumerate(alternative['text'], 87):
        assert character in record['raw_domains'][position]
        assert previous_output[position] in ('?', character)
    assert [87 + i for i, (a, b) in enumerate(zip('ZUGYARZT', alternative['text'])) if a != b] == [92, 93]
    conditional = data['conditional_interpretation']
    dependency = conditional['dependency']
    assert sha(ROOT / dependency['path']) == dependency['sha256']
    published = json.loads((ROOT / dependency['path']).read_text())
    assignments = dict(published['prior_numeric_assignments'])
    assignments[published['conditional_assignment']['baseline_label']] = published['conditional_assignment']['proposed_letter']
    assert assignments == conditional['assignments'] == {'Y': '1', 'J': '2', '2': '6', '9': 'J'}
    ambiguous = published['ambiguous_baseline_labels']
    assert conditional['clear_baseline_labels'] == ambiguous == '0123456789JQY'
    partial_square = ['?' if label in ambiguous else label for label in square]
    for old, new in assignments.items():
        assert partial_square[square.index(old)] == '?'
        partial_square[square.index(old)] = new
    partial_square = ''.join(partial_square)
    assert partial_square == conditional['partial_square']
    anchors = partial_square.replace('?', '')
    assert len(anchors) == len(set(anchors)) == 27
    unused = ''.join(sorted(set(ALPHABET) - set(anchors)))
    assert len(unused) == 9 and unused == conditional['unused_symbols']
    completion = conditional['complete_square_witness']
    assert len(completion) == len(set(completion)) == 36
    assert set(completion) == set(ALPHABET)
    assert all(anchor == '?' or anchor == actual for anchor, actual in zip(partial_square, completion))
    assert partial_square[square.index('9')] == 'J'
    assert partial_square[square.index('Y')] == '1'
    assert partial_square[square.index('J')] == '2'
    assert partial_square[square.index('3')] == '?'
    start, end = conditional['excerpt_start'], conditional['excerpt_end_exclusive']
    assert (start, end) == (71, 151)
    excerpt = ''
    for i in range(start, end):
        pair = interim[2 * i:2 * i + 2]
        assert '?' not in pair
        label = partial_square[6 * COORDINATES.index(pair[0]) + COORDINATES.index(pair[1])]
        assert label != '?'
        excerpt += label
    assert excerpt == conditional['excerpt']
    assert excerpt.startswith('ZUJEDEMTRANSPORTZUG1ARZT') and excerpt.endswith('INJEDEMZUG')
    assert conditional['full_witness_ciphertext'] == frame.replace('?', 'A')
    assert primary.encrypt(conditional['full_witness_plaintext'], ranks, completion) == conditional['full_witness_ciphertext']
    assert conditional['full_witness_ciphertext'][105:] == record['literal_source']
    german = conditional['readable_german']
    assert german.endswith('[…]')
    assert re.sub('[^A-Z0-9]', '', german.replace('[nd]', '').upper()) == excerpt
    case = (ROOT / data['case_path']).read_text()
    assert data['case_section'] in case
    assert f'`{output}`' in case and german in case
    assert '**Further optional edited output — 148/151 positions; 102 total inserted-half fills; 3 unresolved:**' in case
    assert '**Conditional readable German — positions 71–151, end exclusive; published numeric+J assumptions:**' in case
    for row in ['| Additional missing-half fills / total fills / unassigned slots | 13 / 102 / 3 |',
                '| Observed-coordinate substitutions / source-mask fills | 0 / 0 |']:
        assert row in case
    print('Further optional extension verified: +13 inserted halves; 148/151 positions; '
          'all 135 earlier labels and 197 observations preserved; one global numeric+J witness.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.parse_args()
    verify()
