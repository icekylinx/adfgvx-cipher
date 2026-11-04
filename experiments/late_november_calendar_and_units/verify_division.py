#!/usr/bin/env python3
"""Price the historical 303rd Division proposal without changing the shared key.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(check_case=True):
    sys.path.insert(0, str(ROOT))
    from adfgvx.cipher import decrypt, encrypt
    from experiments.late_november_joint_completion.verify import CO, completions, positions
    data = json.loads((HERE / 'division_inputs.json').read_text())
    for path, expected in data['dependencies'].items():
        assert digest(ROOT / path) == expected, path
    path = ROOT / 'experiments/late_november_calendar_and_units/verify.py'
    spec = importlib.util.spec_from_file_location('division_prior', path)
    prior_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior_module)
    prior = prior_module.build()
    assert prior == json.loads((path.parent / 'certificates.json').read_text())
    rec = next(r for r in prior['records'] if r['id'] == data['record_id'])
    original = rec['literal']
    earlier = rec['edition_ciphertext']
    source_input = json.loads((path.parent / 'inputs.json').read_text())
    key = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
               if k['id'] == source_input['key_id'])
    ranks = key['column_rank_order']
    square = source_input['unit_square']
    squares = list(completions(square))
    raw, ps = positions(original, ranks, square)
    proposal = data['proposal']
    pos = ps[proposal['plaintext_index']]
    assert pos['pair'] == proposal['native_pair']
    assert pos['source_indices'] == proposal['native_source_indices']
    assert raw[6:9] == proposal['from']
    change = proposal['additional_substitution']
    i = change['source_index']
    assert i in pos['source_indices']
    assert original[i] == earlier[i] == change['from']
    revised = earlier[:i] + change['to'] + earlier[i + 1:]
    after, revised_positions = positions(revised, ranks, square)
    assert after.startswith(proposal['conditional_prefix'])
    assert after[6:9] == proposal['to']
    assert revised_positions[proposal['plaintext_index']]['pair'] == 'GA'
    changes = [{'source_index': j, 'from': a, 'to': b}
               for j, (a, b) in enumerate(zip(original, revised)) if a != b]
    assert all(c['from'] in CO and c['to'] in CO for c in changes)
    assert changes == rec['earlier_observed_substitutions'] + [change]
    rival_map = {}
    for j in pos['source_indices']:
        for value in CO:
            if value == earlier[j]:
                continue
            candidate = earlier[:j] + value + earlier[j + 1:]
            fields = {decrypt(candidate, ranks, s)[6:9] for s in squares}
            if len(fields) == 1 and next(iter(fields)).isdigit():
                field = fields.pop()
                rival_map[field] = {'source_index': j, 'from': earlier[j], 'to': value}
    summary = {
        'source_slots': len(original), 'plaintext_positions': len(after),
        'earlier_observed_substitutions': len(rec['earlier_observed_substitutions']),
        'additional_observed_substitutions': 1,
        'total_observed_substitutions': len(changes), 'source_mask_fills': 0,
        'surviving_squares': len(squares),
        'one_additional_substitution_numeric_rivals': sorted(rival_map),
    }
    assert summary == data['expected'], summary
    witnesses = []
    for s in squares:
        text = decrypt(revised, ranks, s)
        assert text == after and encrypt(text, ranks, s) == revised
        witnesses.append({'square': s, 'plaintext': text, 'ciphertext': revised})
    if check_case:
        case = (ROOT / data['case']).read_text()
        assert '`' + data['displayed_field'] + '`' in case
    return {
        'schema': 'adfgvx-p230-303rd-division-certificate-v1',
        'authors': data['authors'], 'input_sha256': digest(HERE / 'division_inputs.json'),
        'indexing': 'Zero-based plaintext and original source positions.',
        'record_id': data['record_id'], 'summary': summary,
        'literal_source': original, 'native_interpretation': raw,
        'prior_conditional_edition': rec['interpreted_edition'],
        'historically_identified_edition': after,
        'published_label_edition': decrypt(revised, ranks, key['square']),
        'native_field_position': pos,
        'revised_field_position': revised_positions[proposal['plaintext_index']],
        'earlier_observed_substitutions': rec['earlier_observed_substitutions'],
        'additional_observed_substitution': change,
        'all_observed_substitutions': changes,
        'equal_cost_numeric_fields': rival_map, 'global_witnesses': witnesses,
        'historical_source': data['historical_source'], 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'division_certificate.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
