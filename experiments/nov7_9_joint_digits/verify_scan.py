#!/usr/bin/env python3
"""Replay the bounded inventory of source-reviewed Nov7-9 traffic.

This audits existing frames and both shared digit assignments. It does not
attack unknown keys, select additional source models, or recount old gains.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.nov7_9_joint_digits.verify import (
    CO, decode, full_square, roundtrip, transpose,
)


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def build():
    inputs = json.loads((HERE / 'source_scan_inputs.json').read_text())
    joint = json.loads((HERE / 'inputs.json').read_text())
    keys = json.loads((ROOT / 'data/keys.json').read_text())['keys']
    key = next(k for k in keys if k['id'] == 'Nov7-9')
    square = full_square(key['square'], joint['assignment'])
    rival = full_square(key['square'], joint['alternative_assignment'])
    cache = {}

    def value_at(filename, path):
        if filename not in cache:
            cache[filename] = json.loads((ROOT / filename).read_text())
        value = cache[filename]
        for part in path:
            value = value[part]
        return value

    records = []
    identifiers = [r['id'] for r in inputs['records']]
    assert len(identifiers) == len(set(identifiers)) == 101
    assert {r['id'] for r in joint['records']} <= set(identifiers)
    for record in inputs['records']:
        views = []
        assert record['views'], record['id']
        for view in record['views']:
            value = value_at(view['artifact'], view['value_path'])
            raw = ''.join(''.join(value).split()) if isinstance(value, list) else value
            assert digest(raw) == view['literal_value_sha256']
            if view['transformation'] == 'transpose_interim':
                cipher = transpose(raw, key['column_rank_order'])
            else:
                assert view['transformation'] in ('clean_coordinates', 'join_rows_and_clean')
                cipher = ''.join(c if c in CO else '?' for c in raw)
            assert digest(cipher) == view['ciphertext_sha256']
            baseline, positions = decode(cipher, key['column_rank_order'], key['square'])
            selected, _ = decode(cipher, key['column_rank_order'], square)
            opposite, _ = decode(cipher, key['column_rank_order'], rival)
            assert baseline == view['expected_plaintext']
            occurrences = [
                {'position': p['position'], 'pair': p['pair'],
                 'selected': selected[p['position']], 'alternative': opposite[p['position']]}
                for p in positions if p['pair'] in joint['assignment']
            ]
            assert occurrences == view['expected_occurrences']
            changed = [i for i, (a, b) in enumerate(zip(baseline, selected)) if a != b]
            assert changed == [p['position'] for p in occurrences]
            roundtrip(cipher, key['column_rank_order'], square)
            roundtrip(cipher, key['column_rank_order'], rival)
            effects = []
            for item in occurrences:
                p = item['position']
                lo, hi = max(0, p - 12), min(len(baseline), p + 13)
                effects.append({**item, 'baseline_context': baseline[lo:hi],
                                'selected_context': selected[lo:hi],
                                'alternative_context': opposite[lo:hi]})
            views.append({'artifact': view['artifact'], 'value_path': view['value_path'],
                          'coordinates': len(cipher), 'plaintext_positions': len(baseline),
                          'shared_cell_effects': effects,
                          'source_confirmation_scope': view['source_confirmation_scope']})
        records.append({'id': record['id'], 'disposition': record['disposition'],
                        'views': views, 'new_positions_counted_by_inventory': 0})

    p168 = inputs['p168_D_original_source_check']
    source = ''.join(''.join(p168['source_rows']).split())
    assert len(source) == p168['source_slots'] == 243
    assert hashlib.sha256((ROOT / p168['source_image']).read_bytes()).hexdigest() == p168['source_image_sha256']
    components = value_at('data/certificates/p158.json', ['components', 'readings'])
    earlier = next(r for r in components if r['id'] == 'p159C_one_deletion')
    assert source == earlier['raw_ciphertext']
    exclusion = p168['source_exclusion_in_adopted_frame']
    assert exclusion == 148 and source[exclusion] == 'A'
    assert source[:exclusion] + source[exclusion + 1:] == earlier['corrected_ciphertext']
    return {'schema': 'adfgvx-nov7-9-bounded-source-scan-v1', 'authors': inputs['authors'],
            'input_sha256': digest((HERE / 'source_scan_inputs.json').read_text()),
            'scope': inputs['scope'], 'records_scanned': len(records),
            'existing_views_replayed': sum(len(r['views']) for r in records),
            'both_shared_assignments_reencrypted': True,
            'records': records, 'p168_D_original_source_check': p168,
            'negative_or_prior_only_effects': inputs['negative_or_prior_only_effects'],
            'new_positions_counted_by_inventory': 0, 'limits': inputs['limits']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'source_scan_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(f"Nov7-9 bounded source inventory: {result['records_scanned']} records, "
          f"{result['existing_views_replayed']} existing views; both assignments retained; "
          "no extra gain counted by inventory.")
