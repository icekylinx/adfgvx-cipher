#!/usr/bin/env python3
"""Price the p155 shipping reading and verify its observed word witnesses."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.context155 import verify as verify_base
from experiments.premium_payment_stop.verify import C, inspect, masked_encryption, repair, sha


def observed_word(reading, word):
    start = reading['raw'].index(word)
    positions = reading['positions'][start:start + len(word)]
    assert all(len(p['domain']) == 1 and set(p['pair']) <= set(C) for p in positions)
    return {'word': word, 'plaintext_start': start, 'positions': positions}


def build():
    data = json.loads((HERE / 'inputs.json').read_text())
    base_path = ROOT / data['base_certificate']
    assert sha(base_path) == data['base_certificate_sha256']
    base = json.loads(base_path.read_text())
    verify_base(base)
    keys = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    key = keys[base['key']['id']]
    assert (key['square'], key['column_rank_order']) == (base['key']['square'], base['key']['column_rank_order'])
    records, name_witnesses = [], []
    for proposal in data['records']:
        original = next(s for s in base['sections'] if s['id'] == proposal['id'])
        literal, source = original['raw_literal'], original['analysis_ciphertext']
        assert len(source) == proposal['source_slots']
        target = masked_encryption(proposal['proposal'], key)
        boundaries = [None] if len(source) == len(target) else list(range(len(source) + 1))
        prices = []
        for gap in boundaries:
            model = source if gap is None else source[:gap] + '?' + source[gap:]
            prices.append(sum(a in C and a != b for a, b in zip(model, target)))
        minima = [gap for gap, price in zip(boundaries, prices) if price == min(prices)]
        assert minima == proposal['preferred_gap_boundaries']
        variants = []
        for gap in minima:
            mapping = list(range(len(source)))
            model = source
            if gap is not None:
                model = source[:gap] + '?' + source[gap:]
                mapping.insert(gap, None)
            raw = inspect(model, key, mapping)
            repaired = repair(proposal['proposal'], model, key, mapping, literal)
            assert len(repaired['known_coordinate_substitutions']) == proposal['expected_substitutions']
            assert sum(e['source_index'] is not None for e in repaired['erased_coordinate_fills']) == proposal['expected_source_mask_fills']
            assert sum(e['source_index'] is None for e in repaired['erased_coordinate_fills']) == proposal['expected_inserted_slot_fills']
            assert repaired['full_plaintext_reencryption_verified']
            variants.append({'insert_unknown_before_source_0based': gap,
                             'model_to_source_indices': mapping, 'raw': raw,
                             'completed_reading': repaired})
            name_witnesses.append({'record': proposal['id'], 'gap': gap,
                                   **observed_word(raw, data['same_message_name_witness']['word'])})
        assert len({v['completed_reading']['ciphertext'] for v in variants}) == 1
        records.append({'id': proposal['id'], 'literal_source_sha256': original['raw_literal_sha256'],
                        'source_slots': len(literal), 'plaintext_positions': len(proposal['proposal']),
                        'fixed_body_gap_prices': prices, 'minimum_gap_boundaries': minima,
                        'minimum_observed_substitutions': min(prices), 'variants': variants})
    donors = []
    for spec in data['donors']:
        donor = json.loads((ROOT / spec['inputs']).read_text())
        record = next(r for r in donor['records'] if r['id'] == spec['record'])
        literal = ''.join(''.join(record['source_rows']).split())
        assert hashlib.sha256(literal.encode()).hexdigest() == spec['source_sha256']
        source = ''.join(c if c in C else '?' for c in literal)
        raw = inspect(source, keys[spec['key_id']], list(range(len(source))))
        assert raw['raw'] == record['expected_raw']
        donors.append({**spec, **observed_word(raw, spec['word'])})
    combined = ''.join(r['proposal'] for r in data['records'])
    display = data['readable_german'].upper().replace('Ä', 'AE').replace('Ö', 'OE').replace('Ü', 'UE')
    assert re.sub('[^A-Z0-9?]', '', display) == combined.replace('X', '')
    case = (ROOT / data['case']).read_text()
    assert '> ' + data['readable_german'] in case
    assert combined in re.findall(r'```text\n(.*?)\n```', case, re.S)
    return {'schema': 'adfgvx-p155-shipping-completion-certificate-v1',
            'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
            'base_certificate': data['base_certificate'], 'base_certificate_sha256': sha(base_path),
            'records': records, 'same_message_name_witnesses': name_witnesses,
            'vocabulary_witnesses': donors, 'combined_reading': combined,
            'readable_german': data['readable_german'],
            'summary': {'physical_sources_extended': 2, 'plaintext_positions': len(combined),
                        'native_A1_fixed_positions': 84, 'conditional_A2_raw_fixed_positions': 90,
                        'completed_fixed_positions': len(combined),
                        'observed_substitutions': 5, 'source_mask_fills': 3,
                        'inserted_slot_fills': 1, 'new_physical_sources': 0},
            'prior_reading': data['prior_reading'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
