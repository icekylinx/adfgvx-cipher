#!/usr/bin/env python3
"""Reconcile the already published p172 D2 and p175 B2 source witnesses.

The copy hypothesis is explicit. Original source editions are never rewritten.
Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
from itertools import permutations, product
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

C = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse_order(length, ranks):
    """Independent physical-column offsets, including an incomplete last row."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (col < length % width) for col in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[col])
              for col in range(width)]
    result = [starts[i % width] + i // width for i in range(length)]
    assert sorted(result) == list(range(length))
    return result


def inspect(cipher, key):
    order = inverse_order(len(cipher), key['column_rank_order'])
    assert len(cipher) % 2 == 0
    unknown_labels = set(ALPHABET) - set(key['square'])
    positions = []
    for index in range(len(cipher) // 2):
        indices = order[2 * index:2 * index + 2]
        pair = ''.join(cipher[j] for j in indices)
        domain = set()
        for row in range(6):
            for col in range(6):
                if pair[0] in ('?', C[row]) and pair[1] in ('?', C[col]):
                    label = key['square'][6 * row + col]
                    domain.update(unknown_labels if label == '?' else label)
        domain = ''.join(sorted(domain))
        positions.append({'plaintext_index': index, 'source_indices': indices,
                          'pair': pair, 'domain': domain,
                          'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(row['raw'] for row in positions)
    assert raw == decrypt(cipher, key['column_rank_order'], key['square'])
    assert [row['domain'] for row in positions] == plaintext_domains(cipher, key['column_rank_order'], key['square'])
    return {'ciphertext': cipher, 'raw': raw, 'fixed_positions': len(raw) - raw.count('?'),
            'positions': positions}


def repair(template, literal, key):
    cipher = ''.join(c if c in C else '?' for c in literal)
    order = inverse_order(len(cipher), key['column_rank_order'])
    target = list(cipher)
    assert len(template) * 2 == len(cipher)
    for index, label in enumerate(template):
        if label == '?':
            continue
        cell = key['square'].index(label)
        for source_index, coordinate in zip(order[2 * index:2 * index + 2], (C[cell // 6], C[cell % 6])):
            target[source_index] = coordinate
    target = ''.join(target)
    result = inspect(target, key)
    assert result['raw'] == template
    substitutions, fills = [], []
    for index, (before, after) in enumerate(zip(cipher, target)):
        if before != after:
            item = {'source_index': index, 'printed': literal[index], 'from': before, 'to': after}
            (fills if before == '?' else substitutions).append(item)
    return {**result, 'observed_substitutions': substitutions, 'source_mask_fills': fills}


def full_squares(key):
    cells = [i for i, label in enumerate(key['square']) if label == '?']
    unused = sorted(set(ALPHABET) - set(key['square']))
    assert unused == ['5', '6'] and len(cells) == 2
    for labels in permutations(unused):
        square = list(key['square'])
        for cell, label in zip(cells, labels):
            square[cell] = label
        yield ''.join(square)


def build(pdf=None):
    inputs = read(HERE / 'inputs.json')
    for path, expected in inputs['unchanged_source_artifacts'].items():
        assert digest(ROOT / path) == expected, path
    key = next(k for k in read(ROOT / 'data/keys.json')['keys'] if k['id'] == inputs['key_id'])
    original = {}
    for source in inputs['sources']:
        certificate = read(ROOT / source['certificate'])
        row = next(r for r in certificate['records'] if r['id'] == source['id'])
        literal = row['literal_source']
        assert len(literal) == 204
        raw = inspect(''.join(c if c in C else '?' for c in literal), key)
        assert raw['raw'] == row['raw']
        original[source['id']] = {'literal': literal, 'raw': raw, 'edition': row['readable_candidate']}
    first, second = (original[name] for name in ['p172_D2', 'p175_B2'])
    a, b = first['raw']['ciphertext'], second['raw']['ciphertext']
    joint = [i for i, (x, y) in enumerate(zip(a, b)) if x in C and y in C]
    conflicts = [i for i in joint if a[i] != b[i]]
    assert len(joint) == 190 and conflicts == [1, 134, 146, 153, 165]
    assert sum(a[i] == b[i] for i in joint) == 185
    assert not any(x == y == '?' for x, y in zip(a, b))

    copied = {}
    for name, source, other in [('p172_D2', a, b), ('p175_B2', b, a)]:
        fills = [{'source_index': i, 'value': other[i]} for i, value in enumerate(source) if value == '?']
        cipher = ''.join(other[i] if value == '?' else value for i, value in enumerate(source))
        copied[name] = {**inspect(cipher, key), 'copied_source_mask_fills': fills,
                        'observed_coordinate_changes': 0}
    assert [copied[x]['fixed_positions'] for x in ['p172_D2', 'p175_B2']] == [101, 100]

    primary_template = inputs['p175_conservative_copy_supported_template']
    primary = repair(primary_template, second['literal'], key)
    assert len(primary['observed_substitutions']) == 4 and len(primary['source_mask_fills']) == 10
    assert primary['fixed_positions'] == 100
    assert [r['source_index'] for r in primary['observed_substitutions']] == [1, 32, 38, 165]
    assert primary['positions'][62]['pair'] == primary['positions'][101]['pair'] == 'VF'
    assert primary['positions'][62]['domain'] == primary['positions'][101]['domain'] == '56'
    old_template = second['edition']['raw']
    changes = [{'plaintext_index': i, 'old': x, 'new': y}
               for i, (x, y) in enumerate(zip(old_template, primary_template)) if x != y]
    assert changes == [{'plaintext_index': 3, 'old': '?', 'new': '1'},
                       {'plaintext_index': 98, 'old': '?', 'new': '9'}]
    extra_fills = [x for x in primary['source_mask_fills']
                   if x['source_index'] not in {y['source_index'] for y in second['edition']['erased_coordinate_fills']}]
    assert [(x['source_index'], x['to']) for x in extra_fills] == [(154, 'F'), (203, 'G')]

    common_template = inputs['separate_common_copy_template']
    common = {name: repair(common_template, row['literal'], key) for name, row in original.items()}
    assert common['p172_D2']['ciphertext'] == common['p175_B2']['ciphertext']
    assert [len(common[x]['observed_substitutions']) for x in ['p172_D2', 'p175_B2']] == [3, 5]
    assert [len(common[x]['source_mask_fills']) for x in ['p172_D2', 'p175_B2']] == [4, 10]
    assert common_template[:-1] == primary_template[:-1] and common_template[-1] == 'X' and primary_template[-1] == '?'
    target_cipher = common['p172_D2']['ciphertext']
    assert '?' not in target_cipher

    support = []
    for index, label in enumerate(common_template):
        target_pair = common['p172_D2']['positions'][index]['pair']
        witnesses = [name for name, row in original.items()
                     if row['raw']['positions'][index]['pair'] == target_pair
                     and '?' not in target_pair]
        support.append({'plaintext_index': index, 'candidate_label': label,
                        'target_pair': target_pair, 'complete_observed_pair_witnesses': witnesses})
    unsupported_fixed = [row['plaintext_index'] for row in support
                         if row['candidate_label'] != '?' and not row['complete_observed_pair_witnesses']]
    assert unsupported_fixed == [29, 89]

    # In the common-copy model, each of the five observed disagreements
    # contributes at least one change across the two source records. Choosing
    # either printed value attains that bound. No position is jointly erased.
    choice_domains = [sorted({x, y} - {'?'}) for x, y in zip(a, b)]
    assert sum(len(x) == 2 for x in choice_domains) == 5
    base = [values[0] for values in choice_domains]
    family = []
    full_plaintexts = set()
    for choices in product(*[choice_domains[i] for i in conflicts]):
        cipher = base.copy()
        for index, value in zip(conflicts, choices):
            cipher[index] = value
        cipher = ''.join(cipher)
        total_cost = sum(x != '?' and x != y for source in (a, b) for x, y in zip(source, cipher))
        assert total_cost == 5
        raw = inspect(cipher, key)['raw']
        completions = []
        for square in full_squares(key):
            plaintext = decrypt(cipher, key['column_rank_order'], square)
            assert encrypt(plaintext, key['column_rank_order'], square) == cipher
            full_plaintexts.add(plaintext)
            completions.append({'square': square, 'plaintext': plaintext})
        family.append({'conflict_coordinates': list(choices), 'ciphertext': cipher,
                       'raw': raw, 'joint_observed_substitutions': total_cost,
                       'global_square_completions': completions})
    assert len(family) == 32 and len(full_plaintexts) == 64
    assert all(row['ciphertext'] != target_cipher for row in family)
    assert a[32] == b[32] == 'G' and target_cipher[32] == 'F'
    assert a[38] == '?' and b[38] == 'G' and target_cipher[38] == 'D'
    outside_copy_repairs = [
        {'source_index': 32, 'witnesses': ['p172_D2', 'p175_B2'],
         'observed': 'G', 'proposed': 'F', 'observed_change_cost': 2,
         'plaintext_index': 29, 'raw_label': 'Y', 'proposed_label': 'M'},
        {'source_index': 38, 'witnesses': ['p175_B2'],
         'observed': 'G', 'proposed': 'D', 'observed_change_cost': 1,
         'plaintext_index': 89, 'raw_label': 'G', 'proposed_label': 'L',
         'additional_p172_mask_fill': 'D'},
    ]
    observed_cost = sum(len(row['observed_substitutions']) for row in common.values())
    assert observed_cost == len(conflicts) + sum(x['observed_change_cost'] for x in outside_copy_repairs) == 8

    historical_variants = []
    for square in full_squares(key):
        primary_text = decrypt(primary['ciphertext'], key['column_rank_order'], square)
        common_text = decrypt(target_cipher, key['column_rank_order'], square)
        assert primary_text[62] == primary_text[101] and primary_text[62] in '56'
        assert encrypt(primary_text, key['column_rank_order'], square) == primary['ciphertext']
        assert encrypt(common_text, key['column_rank_order'], square) == target_cipher
        historical_variants.append({'square': square, 'conservative_p175': primary_text,
                                    'common_copy_candidate': common_text, 'historical_assignment_claim': False})
    # The reader-facing strings are checked directly, not just a detached
    # stored proposal. The final '?' in the quotation is positional evidence.
    readme = (HERE / 'README.md').read_text()
    for stream in [copied['p172_D2']['raw'], copied['p175_B2']['raw'],
                   primary_template, common_template]:
        assert '```text\n' + stream + '\n```' in readme
    quotes = re.findall(r'^> (.+)$', readme, flags=re.M)
    assert len(quotes) == 1
    quote_labels = ''.join(c for c in quotes[0].upper() if c in ALPHABET + '?')
    assert quote_labels == primary_template.replace('X', '')
    for case in ['cases/finance/hauptwechselamt_accounting.md',
                 'cases/finance/staatsbank_accounting_cheques.md']:
        assert '../../experiments/accounting_copy_reconciliation/README.md' in (ROOT / case).read_text()
    if pdf:
        from experiments.hauptwechselamt_accounting.verify import build as check_p175
        from experiments.staatsbank_accounting_cheques.verify import build as check_p172
        assert check_p175(pdf)['records'][0]['raw'] == second['raw']['raw']
        assert check_p172(pdf)['records'][1]['raw'] == first['raw']['raw']
    # Original position ledgers are already pinned in the source certificates.
    # Keep the new certificate focused on the comparison and its new claims.
    source_outputs = {name: {'literal_source': row['literal'],
                             'ciphertext': row['raw']['ciphertext'],
                             'raw': row['raw']['raw'],
                             'fixed_positions': row['raw']['fixed_positions'],
                             'original_edited_output': row['edition']['raw']}
                      for name, row in original.items()}
    compact = lambda row: {k: v for k, v in row.items() if k != 'positions'}
    primary_record = compact(primary)
    primary_record['retained_unknown_positions'] = [primary['positions'][i] for i in (62, 101)]
    return {'schema': 'adfgvx-accounting-copy-reconciliation-v1',
            'authors': inputs['authors'], 'input_sha256': digest(HERE / 'inputs.json'),
            'indexing': 'All source and plaintext indices are zero-based.',
            'new_physical_records': 0, 'key_id': key['id'],
            'summary': {'source_records_compared': 2, 'source_slots_per_record': 204,
                        'jointly_observed_coordinates': 190, 'agreeing_observed_coordinates': 185,
                        'conflicting_observed_coordinates': 5, 'disjoint_source_masks': 14,
                        'p175_newly_fixed_labels_without_new_observed_changes': 2,
                        'p175_conservative_fixed_positions': 100, 'plaintext_positions_per_record': 102,
                        'p175_conservative_observed_substitutions': 4, 'p175_conservative_mask_fills': 10,
                        'observation_choice_streams': 32, 'globally_completed_observation_choice_plaintexts': 64,
                        'common_candidate_fixed_positions': 101, 'fixed_labels_with_full_pair_witness': 99,
                        'common_candidate_joint_observed_substitutions': 8,
                        'common_candidate_joint_mask_fills': 14, 'published_key_changed': False},
            'original_source_outputs': source_outputs, 'coordinate_conflicts': [
                {'source_index': i, 'p172_D2': a[i], 'p175_B2': b[i]} for i in conflicts],
            'pure_observed_mask_transfer': {name: compact(row) for name, row in copied.items()},
            'conservative_p175_candidate': primary_record, 'two_new_labels': changes,
            'two_additional_source_mask_fills': extra_fills,
            'separate_common_copy_candidate': {name: compact(row) for name, row in common.items()},
            'complete_pair_support': support,
            'unsupported_fixed_plaintext_positions': unsupported_fixed,
            'minimum_observation_choice_family': family,
            'repairs_outside_observation_choice_family': outside_copy_repairs,
            'remaining_global_square_completions': historical_variants,
            'limits': inputs['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    target = HERE / 'certificates.json'
    if args.verify:
        assert result == read(target)
    else:
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
