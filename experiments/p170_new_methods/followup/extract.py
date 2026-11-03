#!/usr/bin/env python3
"""Extract source-derived donor candidates; the frozen inputs retain the tested scope.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from data.reviews.verify_childs_material_coverage import (
    Unsupported, quantify, read, record, literal, key_for,
)
from experiments.romanian_pacification_consultation.verify import inspect
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'
FIELDS = {'edited_output', 'editorial_template', 'expected_raw', 'raw_plaintext',
          'compact_plaintext', 'primary_template'}
EXCLUDED_PACKAGES = {'p170_new_methods', 'open_targets', 'anchored_search',
                     'joint_search', 'radio_domain_model'}


def complete_donors():
    pool = {}
    def visit(value, path, origin):
        if isinstance(value, dict):
            for key, child in value.items():
                at = path + [key]
                excluded = any(any(word in str(part).lower() for word in
                                   ['control', 'synthetic', 'diagnostic', 'example', 'search_result'])
                               for part in at)
                if (key in FIELDS and isinstance(child, str) and len(child) >= 53
                        and set(child) <= set(ALPHABET)
                        and not set(child) <= set(COORDINATES) and not excluded):
                    pool.setdefault(child, []).append([origin, at])
                visit(child, at, origin)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                visit(child, path + [i], origin)
    for path in sorted((ROOT / 'experiments').glob('*/inputs.json')):
        if path.parent.name in EXCLUDED_PACKAGES:
            continue
        try:
            visit(json.loads(path.read_text()), [], str(path.relative_to(ROOT)))
        except (OSError, ValueError):
            continue
    return [{'id': i, 'text': text, 'origins': origins}
            for i, (text, origins) in enumerate(sorted(pool.items()))]


def partial_donors():
    catalogue = read('data/reading_catalog.json')
    donors, reasons = {}, Counter()
    considered = 0
    for row in catalogue['challenge'] + catalogue['other']:
        if row['id'] == 'p170':
            continue
        for evidence in row.get('evidence', []):
            cp = Path(evidence)
            if not (evidence.startswith('experiments/') and cp.suffix == '.json'
                    and 'certif' in cp.name):
                continue
            considered += 1
            try:
                counts = quantify(evidence, row['id'])
                data, certificate = read(str(cp.parent / 'inputs.json')), read(evidence)
                source_record, cert_record = record(data, row['id']), record(certificate, row['id'])
                key = key_for(data, source_record, cert_record)
            except (Unsupported, AssertionError, KeyError, ValueError, OSError, TypeError) as error:
                reasons[type(error).__name__ + ':' + str(error)[:95]] += 1
                continue
            if '?' in key['square'] or len(set(key['square'])) != 36:
                reasons['source square is partial'] += 1
                continue
            if counts['frame_kind'] != 'native_order_and_length':
                reasons['non-native selected frame omitted'] += 1
                continue
            source = literal(source_record)
            if len(source) != counts['native_source_slots']:
                reasons['annotated source requires a dedicated tokenization adapter'] += 1
                continue
            if len(source) % 2:
                reasons['odd source length omitted'] += 1
                continue
            frame = ''.join(c if c in COORDINATES else '?' for c in source)
            result = inspect(frame, key, list(range(len(frame))))
            n, fixed = len(frame) // 2, result['fixed_positions']
            assert n == counts['model_positions']
            assert fixed == counts['fixed_raw_labels_with_all_unobserved_coordinates_unassigned']
            if n < 53 or fixed < 45 or fixed == n:
                reasons['not a partial body with >=53 positions and >=45 native fixed positions'] += 1
                continue
            fingerprint = (key['id'], tuple(p['domain'] for p in result['positions']))
            item = donors.setdefault(fingerprint, {
                'id': len(donors), 'source_literal': source, 'source_key_id': key['id'],
                'source_slots': len(source), 'raw_fixed_positions': fixed, 'origins': [],
            })
            item['origins'].append({
                'record_id': row['id'], 'certificate': evidence,
                'inputs': str(cp.parent / 'inputs.json'), 'case': row['path'],
                'native_source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                'quantify_native_contract_passed': True,
            })
    scope = {'catalogue_certificate_pairs_considered': considered,
             'partial_donor_domain_families': len(donors),
             'source_origins': sum(len(x['origins']) for x in donors.values()),
             'source_squares_complete': True, 'all_native_slots_retained': True,
             'target_support_threshold': 90, 'omissions': dict(reasons)}
    return sorted(donors.values(), key=lambda x: x['id']), scope


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='Write a candidate snapshot; does not replace the frozen tested inputs.')
    args = parser.parse_args()
    partial, scope = partial_donors()
    result = {'complete_donors': complete_donors(), 'partial_donors': partial,
              'partial_extraction_scope': scope}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'complete_donors': len(result['complete_donors']),
                      'partial_donors': len(partial)}, indent=2))
