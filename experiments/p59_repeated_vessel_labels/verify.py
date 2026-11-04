#!/usr/bin/env python3
"""Verify the p59 A1 conditional transfers without selecting a vessel identity.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
All source and plaintext indices are zero-based.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.supplementary import calc as independent_calc
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair
from experiments.poti_first_part_conditional.verify import constrained_stream, exact_alignment

CO = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repeated_field_census(raw, spec, key):
    """Factor the exact equality cost over every label at each common position."""
    starts, length = spec['plaintext_starts'], spec['length']
    assert [raw['raw'][s:s + length] for s in starts] == spec['raw_copies']
    pairs = {c: CO[i // 6] + CO[i % 6] for i, c in enumerate(key['square'])}
    columns = []
    for offset in range(length):
        received = [raw['positions'][s + offset]['pair'] for s in starts]
        costs = {label: sum(a != '?' and a != b for pair in received
                           for a, b in zip(pair, encoded))
                 for label, encoded in pairs.items()}
        minimum = min(costs.values())
        best = ''.join(c for c in ALPHABET if costs[c] == minimum)
        columns.append({'field_offset': offset, 'received_pairs': received,
                        'cost_by_label': {c: costs[c] for c in ALPHABET},
                        'minimum_observed_substitutions': minimum,
                        'minimizing_labels': best})
    variants = [''.join(chars) for chars in itertools.product(
        *(column['minimizing_labels'] for column in columns))]
    assert variants == spec['minimum_equal_copy_variants']
    return {'id': spec['id'], 'plaintext_starts': starts, 'length': length,
            'all_strings_in_factored_scope': 36 ** length,
            'minimum_observed_substitutions': sum(c['minimum_observed_substitutions'] for c in columns),
            'minimum_equal_copy_variants': variants, 'positions': columns}


def layer(template, cipher, key, mapping, literal):
    result = repair(template, cipher, key, mapping, literal)
    independent = independent_calc(result['ciphertext'], key)
    assert independent['plaintext'] == result['raw'] == template
    assert independent['coordinate_roundtrip']
    assert not independent['fixed_plaintext_reencoding_known_coordinate_conflicts']
    assert independent['plaintext_domains'] == [p['domain'] for p in result['positions']]
    complete_cipher = result['ciphertext'].replace('?', 'A')
    complete_text = decrypt(complete_cipher, key['column_rank_order'], key['square'])
    assert encrypt(complete_text, key['column_rank_order'], key['square']) == complete_cipher
    assert all(a == '?' or a == b for a, b in zip(template, complete_text))
    return result


def build(inp):
    baseline = inp['baseline']
    assert sha(ROOT / baseline['inputs']) == baseline['inputs_sha256']
    assert sha(ROOT / baseline['certificate']) == baseline['certificate_sha256']
    original, certificate = load(ROOT / baseline['inputs']), load(ROOT / baseline['certificate'])
    source_record, key = original['record'], original['key']
    assert source_record['id'] == baseline['record_id'] == 'p59_A1'
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Sep19-21')
    literal = ''.join(''.join(source_record['source_rows']).split())
    source = ''.join(c if c in CO else '?' for c in literal)
    assert len(source) == 225 and sum(c in CO for c in literal) == 217
    assert source_record['advertised_length'] == 220
    _, stencil = constrained_stream(source_record['ordinary_word_anchors'], key)
    original_search = exact_alignment(source, stencil, True)
    maps = original_search['excluded_source_index_sets']
    assert original_search['minimum_cost'] == [5, 2]
    assert len(maps) == baseline['existing_frame_maps'] == 21
    assert maps == [r['excluded_source_indices'] for r in certificate['all_minimum_frames']]
    assert [(a['plaintext_index'], a['label'], a['donor_plaintext_index'])
            for a in inp['common_assignments']] == [(35, 'N', 41), (40, 'R', 34), (81, 'L', 74)]
    results, all_censuses, all_transfers = [], [], []
    for excluded, prior in zip(maps, certificate['all_minimum_frames']):
        mapping = [i for i in range(225) if i not in excluded]
        assert mapping == prior['model_to_source_indices'] and len(mapping) == 220
        wire = ''.join(source[i] for i in mapping)
        raw = inspect(wire, key, mapping)
        assert raw == prior['baseline'] and raw['fixed_positions'] == 103
        before = layer(prior['limited_candidate']['template'], wire, key, mapping, literal)
        assert before == prior['limited_candidate']
        assert before['fixed_positions'] == 105
        censuses = [repeated_field_census(raw, spec, key) for spec in inp['repeated_fields']]
        assert [r['minimum_observed_substitutions'] for r in censuses] == [1, 1]
        all_censuses.append(censuses)
        common = list(before['raw']); transfers = []
        for assignment in inp['common_assignments']:
            i, letter, donor_i = assignment['plaintext_index'], assignment['label'], assignment['donor_plaintext_index']
            target, donor = raw['positions'][i], raw['positions'][donor_i]
            assert target['raw'] == '?' and donor['raw'] == letter
            assert len(donor['domain']) == 1 and '?' not in donor['pair']
            assert letter in target['domain'] and common[i] == '?'
            relevant = next(s for s in inp['repeated_fields'] if any(
                start <= i < start + s['length'] for start in s['plaintext_starts']))
            start = next(start for start in relevant['plaintext_starts'] if start <= i < start + relevant['length'])
            assert all(v[i - start] == letter for v in relevant['minimum_equal_copy_variants'])
            common[i] = letter
            transfers.append({**assignment, 'original_pair': target['pair'], 'original_domain': target['domain'],
                              'source_indices': target['source_indices'], 'donor_pair': donor['pair'],
                              'donor_source_indices': donor['source_indices']})
        all_transfers.append(transfers)
        common = layer(''.join(common), wire, key, mapping, literal)
        assert common['known_coordinate_substitutions'] == before['known_coordinate_substitutions']
        added = [r for r in common['erased_coordinate_fills'] if r not in before['erased_coordinate_fills']]
        assert len(added) == 4 and len(common['erased_coordinate_fills']) == 6
        assert common['fixed_positions'] == 108 and common['raw'][37] == '4'
        unresolved = [p for p in common['positions'] if p['raw'] == '?']
        assert [p['plaintext_index'] for p in unresolved] == [2, 3]
        remaining = math.prod(len(p['domain']) for p in unresolved)
        assert remaining == 36
        joint = []
        for words in itertools.product(*(s['minimum_equal_copy_variants'] for s in inp['repeated_fields'])):
            text = list(before['raw'])
            for spec, word in zip(inp['repeated_fields'], words):
                for start in spec['plaintext_starts']:
                    text[start:start + len(word)] = word
            candidate = layer(''.join(text), wire, key, mapping, literal)
            assert len(candidate['known_coordinate_substitutions']) == 7
            assert candidate['erased_coordinate_fills'] == common['erased_coordinate_fills']
            added_substitutions = [r for r in candidate['known_coordinate_substitutions']
                                   if r not in before['known_coordinate_substitutions']]
            assert len(added_substitutions) == 2 and candidate['raw'][37] == '4'
            joint.append({'field_values': list(words), 'plaintext': candidate['raw'],
                          'ciphertext': candidate['ciphertext'], 'additional_substitutions': added_substitutions,
                          'total_observed_substitutions': 7, 'total_mask_fills': 6,
                          'remaining_complete_plaintexts': remaining})
        assert len(joint) == 4
        results.append({'excluded_source_indices': excluded, 'raw_before_word_repairs': raw['raw'],
                        'earlier_candidate': before['raw'], 'common_plaintext': common['raw'],
                        'common_ciphertext': common['ciphertext'], 'additional_mask_fills': added,
                        'total_observed_substitutions': 5, 'total_mask_fills': 6,
                        'remaining_domains': unresolved, 'remaining_complete_plaintexts': remaining,
                        'joint_equal_field_variants': joint})
    assert all(x == all_censuses[0] for x in all_censuses)
    assert all(x == all_transfers[0] for x in all_transfers)
    representative = next(r for r in results if r['excluded_source_indices'] == baseline['representative_excluded_source_indices'])
    assert representative['common_plaintext'] == inp['representative_common_plaintext']
    case = (ROOT / inp['case']).read_text()
    section = case.split('## Conditional repeated-field completion\n', 1)[1].split('\n## ', 1)[0]
    displays = re.findall(r'```text\n(.*?)\n```', section, re.S)
    assert displays == [inp['representative_common_plaintext']]
    quote = '\n'.join(line[2:] for line in section.splitlines() if line.startswith('> '))
    assert quote == inp['representative_readable_german']
    assert re.sub('[^A-Z0-9?]', '', quote.upper()) == inp['representative_common_plaintext']
    return {'schema': 'adfgvx-p59-repeated-vessel-labels-certificate-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'baseline': baseline,
            'summary': {'physical_records_added': 0, 'printed_source_slots': 225, 'valid_source_coordinates': 217,
                        'modeled_coordinates': 220, 'source_exclusions': 5, 'existing_frame_maps_retained': 21,
                        'plaintext_positions': 110, 'fixed_raw_positions_under_conditional_frame': 103,
                        'earlier_conditional_fixed': 105, 'common_conditional_fixed': 108,
                        'new_conditional_labels': 3, 'additional_observed_substitutions': 0,
                        'additional_mask_fills': 4, 'total_observed_substitutions': 5, 'total_mask_fills': 6,
                        'remaining_unresolved_positions': 2, 'remaining_complete_plaintexts_per_frame': 36,
                        'minimum_equal_copy_joint_variants_per_frame': 4,
                        'equal_copy_total_observed_substitutions': 7,
                        'all_source_frame_maps_unchanged': True, 'published_key_changed': False},
            'repeated_field_censuses': all_censuses[0], 'common_transfer_evidence': all_transfers[0],
            'representative': representative, 'all_frame_results': results,
            'contextual_sources': inp['contextual_sources'], 'limits': inp['limits'], 'credit': inp['credit']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    assert not (args.write and args.verify)
    inp = load(HERE / 'inputs.json'); certificate = build(inp)
    if args.write:
        (HERE / 'certificates.json').write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + '\n')
    else:
        assert certificate == load(HERE / 'certificates.json')
    evidence = verify_source_evidence(args.pdf, inp['source'], inp['source_images'], HERE)
    print(json.dumps({'verified': not args.write, **certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))


if __name__ == '__main__':
    main()
