#!/usr/bin/env python3
"""Check an optional six-half lexical delta against the frozen primary edition."""
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
HERE = Path(__file__).resolve().parent
parser.add_argument('--verify', action='store_true')
parser.add_argument('--base', type=Path, default=HERE)
parser.add_argument('--delta', type=Path, default=HERE / 'optional_underpersonal.json')
args = parser.parse_args()
base = args.base.resolve()
spec = importlib.util.spec_from_file_location('primary_verifier', base / 'verify.py')
primary_verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(primary_verifier)
primary_verifier.verify()
delta = json.loads(args.delta.read_text())
assert hashlib.sha256((base / 'inputs.json').read_bytes()).hexdigest() == delta['base_input_sha256']
assert hashlib.sha256((base / 'certificates.json').read_bytes()).hexdigest() == delta['base_certificate_sha256']
inputs = json.loads((base / 'inputs.json').read_text())
certificate = json.loads((base / 'certificates.json').read_text())
record = certificate['record']
key = inputs['key']
source = record['literal_source']
primary = record['primary']
frame = list(primary['ciphertext'])
expected_fills = []
span = delta['span']
assert span == {'start': 95, 'text': 'MITUNTERPERSONALUMEDIKAMENTEN'}
permutation = primary_verifier.layout(302, key['column_rank_order'])
for position, character in enumerate(span['text'], span['start']):
    assert character in record['raw_domains'][position]
    cell = key['square'].index(character)
    for side, value in enumerate(('ADFGVX'[cell // 6], 'ADFGVX'[cell % 6])):
        index = permutation[2 * position + side]
        if frame[index] == '?':
            assert index < 105
            expected_fills.append({'model_index': index, 'source_index': None,
                                   'plaintext_index': position, 'pair_side': side,
                                   'from': '?', 'to': value, 'selected_label': character})
            frame[index] = value
        else:
            assert frame[index] == value
assert len(expected_fills) == 6
assert sorted(expected_fills, key=lambda x: x['model_index']) == delta['additional_inserted_coordinate_fills']
frame = ''.join(frame)
assert frame[105:] == source
_, domains, output = primary_verifier.decode(frame, key['column_rank_order'], key['square'])
assert output == delta['optional_output']
assert len(output) == 151 and output.count('?') == 16
assert frame.count('?') == 16
assert all(old == '?' or old == new for old, new in zip(primary['raw'], output))
assert [i for i, (old, new) in enumerate(zip(primary['raw'], output)) if old != new] == [96, 97, 98, 99, 100, 111]
assert delta['prices'] == {'additional_observed_coordinate_substitutions': 0,
                           'additional_source_mask_fills': 0,
                           'additional_inserted_slot_fills': 6,
                           'total_inserted_slot_fills': 89,
                           'fixed_optional_positions': 135,
                           'plaintext_positions': 151,
                           'remaining_unassigned_inserted_slots': 16}
complete_frame = frame.replace('?', 'A')
_, complete_domains, complete_text = primary_verifier.decode(complete_frame, key['column_rank_order'], key['square'])
assert all(len(d) == 1 for d in complete_domains)
assert primary_verifier.encrypt(complete_text, key['column_rank_order'], key['square']) == complete_frame
case = (base.parents[1] / delta['case_path']).read_text()
assert delta['case_section'] in case
assert f"`{output}`" in case
assert delta['optional_readable_german_excerpt'] in case
normalized = re.sub('[^A-Z0-9]', '', delta['optional_readable_german_excerpt'].replace('[nd]', '').upper())
assert normalized == output[95:]
assert '**Optional edited output — 135/151 positions; 89 total inserted-half fills; 16 unresolved:**' in case
assert '**Optional readable German — U expanded as u[nd]; literal 9 retained:**' in case
assert '| Additional missing-half fills / total fills / unassigned slots | 6 / 89 / 16 |' in case
assert '| Observed-coordinate substitutions / source-mask fills | 0 / 0 |' in case
print('Optional extension verified: +6 inserted-half fills; 135/151 fixed; '
      '16 unresolved; every primary label and all 197 observations preserved.')
