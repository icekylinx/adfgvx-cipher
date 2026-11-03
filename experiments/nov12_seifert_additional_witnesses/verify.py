#!/usr/bin/env python3
"""Verify two further Seifert-service witnesses against independent raw sources.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, untranspose
from experiments.romanian_pacification_consultation.verify import (
    inspect, permutation, repair, verify_crops,
)

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(rows):
    return ''.join(''.join(rows).split())


def mask(literal):
    return ''.join(c if c in C else '?' for c in literal)


def native(literal, key):
    cipher = mask(literal)
    order = permutation(len(cipher), key['column_rank_order'])
    middle = ''.join(cipher[i] for i in order)
    assert middle == untranspose(cipher, key['column_rank_order'])
    raw = decrypt(cipher, key['column_rank_order'], key['square'], allow_unpaired=True)
    return {'ciphertext': cipher, 'source_slots': len(cipher), 'raw': raw,
            'fixed_positions': len(raw) - raw.count('?'),
            'paired_plaintext_positions': len(cipher) // 2,
            'intermediate': middle, 'intermediate_to_source_indices': order,
            'unpaired_coordinate': {'value': middle[-1], 'source_index': order[-1],
                                   'intermediate_index': len(cipher) - 1},
            'silently_dropped_source_coordinate': False}


def price(mapping, literal, target):
    conflicts = []
    masks = 0
    for j, i in enumerate(mapping):
        if i is None:
            continue
        if literal[i] not in C:
            masks += 1
        elif literal[i] != target[j]:
            conflicts.append([j, i, literal[i], target[j]])
    return conflicts, masks


from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data = json.loads((HERE / 'inputs.json').read_text())
    key = data['key']
    assert data['authors'] == 'icekylinx and GPT-6 Astra Pro'
    assert key == next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                       if k['id'] == key['id'])
    for name, digest in data['prior_artifacts'].items():
        assert sha(HERE / name) == digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))

    frozen = json.loads((HERE / 'parallel_witnesses.json').read_text())
    witnesses = {r['id']: r for r in frozen['records']}
    for rid, record in witnesses.items():
        current = json.loads((ROOT / record['origin_path']).read_text())
        current_record = next(r for r in current['records'] if r['id'] == rid)
        rows = current_record.get('source_rows', current_record.get('raw_source_rows'))
        assert rows == record['source_rows']
        assert mask(compact(rows)) == record['analysis_ciphertext']
        assert decrypt(record['analysis_ciphertext'], key['column_rank_order'], key['square']) == record['raw_plaintext']
    old_b, new_b = [witnesses[r]['analysis_ciphertext'] for r in ['p174_B', 'p183_B']]
    assert len(old_b) == len(new_b) == 74
    assert all(a == '?' or b == '?' or a == b for a, b in zip(old_b, new_b))
    consensus = ''.join(a if a != '?' else b for a, b in zip(old_b, new_b))
    assert '?' not in consensus
    consensus_plain = decrypt(consensus, key['column_rank_order'], key['square'])
    order74 = permutation(74, key['column_rank_order'])
    complete_pair_support = []
    for p in range(37):
        indices = order74[2*p:2*p+2]
        owners = [rid for rid, body in [('p174_B', old_b), ('p183_B', new_b)]
                  if all(body[i] == consensus[i] for i in indices)]
        assert owners
        complete_pair_support.append({'plaintext_index': p, 'label': consensus_plain[p],
            'model_indices': indices, 'raw_witnesses': owners})
    target_c = witnesses['p174_C']['analysis_ciphertext']
    assert len(target_c) == 48 and set(target_c) <= set(C)
    assert encrypt(witnesses['p174_C']['raw_plaintext'], key['column_rank_order'], key['square']) == target_c

    records = []
    for source in data['records']:
        literal = compact(source['source_rows'])
        assert len(literal) == source['source_slots']
        assert sum(c in C for c in literal) == source['valid_source_coordinates']
        baseline = native(literal, key)
        target = consensus if source['id'] == 'p182_A' else target_c
        assert decrypt(target, key['column_rank_order'], key['square']) == source['target']
        assert encrypt(source['target'], key['column_rank_order'], key['square']) == target
        rows = []
        for excluded in range(len(literal)):
            m0 = [i for i in range(len(literal)) if i != excluded]
            gap_positions = range(55) if source['id'] == 'p182_A' else [None]
            for gap in gap_positions:
                mapping = m0[:gap] + [None] * 20 + m0[gap:] if gap is not None else m0
                conflicts, masks = price(mapping, literal, target)
                rows.append({'excluded_source_index': excluded,
                    'excluded_glyph': literal[excluded],
                    'gap_after_shortened_slots': gap,
                    'substitution_count': len(conflicts),
                    'observed_slot_exclusions': int(literal[excluded] in C),
                    'masked_slot_exclusions': int(literal[excluded] not in C),
                    'source_mask_fills': masks, 'added_slot_fills': mapping.count(None)})
        best = min(r['substitution_count'] for r in rows)
        minimum_rows = [r for r in rows if r['substitution_count'] == best]
        if source['id'] == 'p182_A':
            assert len(literal) == 55 and source['advertised_length'] == 74
            assert [i for i, c in enumerate(literal) if c not in C] == [8, 29, 32, 45, 46, 47, 48]
            assert len(rows) == 3025 and best == 1
            assert [(r['excluded_source_index'], r['gap_after_shortened_slots'])
                    for r in minimum_rows] == [(i, 5) for i in range(40, 51)]
        else:
            assert len(literal) == 49 and source['advertised_length'] == 56
            assert len(rows) == 49 and best == 1
            assert [r['excluded_source_index'] for r in minimum_rows] == [48]
        branches = []
        for row in minimum_rows:
            excluded, gap = row['excluded_source_index'], row['gap_after_shortened_slots']
            m0 = [i for i in range(len(literal)) if i != excluded]
            mapping = m0[:gap] + [None] * 20 + m0[gap:] if gap is not None else m0
            model = ''.join('?' if i is None or literal[i] not in C else literal[i] for i in mapping)
            raw = inspect(model, key, mapping)
            candidate = repair(source['target'], model, key, mapping, literal)
            assert candidate['ciphertext'] == target
            assert len(candidate['known_coordinate_substitutions']) == row['substitution_count']
            assert sum(e['source_index'] is not None for e in candidate['erased_coordinate_fills']) == row['source_mask_fills']
            assert sum(e['source_index'] is None for e in candidate['erased_coordinate_fills']) == row['added_slot_fills']
            branches.append({**row, 'model_to_source_indices': mapping, 'ciphertext': model,
                **raw, 'readable_candidate': candidate})
        primary = next(r for r in branches if r['excluded_source_index'] == source['primary_excluded_source_index'])
        if source['id'] == 'p182_A':
            assert primary['excluded_source_index'] == 48 and primary['masked_slot_exclusions'] == 1
            assert primary['source_mask_fills'] == 6 and primary['added_slot_fills'] == 20
            assert primary['fixed_positions'] == 11
            assert primary['readable_candidate']['known_coordinate_substitutions'] == [
                {'model_index': 0, 'source_index': 0, 'printed': 'V', 'from': 'V', 'to': 'D'}]
        else:
            assert primary['observed_slot_exclusions'] == 1 and primary['fixed_positions'] == 24
            assert primary['readable_candidate']['known_coordinate_substitutions'] == [
                {'model_index': 8, 'source_index': 8, 'printed': 'F', 'from': 'F', 'to': 'V'}]
        folded = ''.join(c for c in source['readable_german'].upper() if c in A + '?')
        assert folded == source['target'].replace('X', '')
        records.append({'id': source['id'], 'literal_header': source['literal_header'],
            'literal_source': literal, 'literal_source_rows': source['source_rows'],
            'advertised_length': source['advertised_length'], 'native_frame': baseline,
            'raw_is_conditional_frame': True, 'primary': primary,
            'all_minimum_branches': branches, 'readable_german': source['readable_german'],
            'bounded_source_alignment_scan': {'model_count': len(rows),
                'objective': 'Minimize observed-coordinate conflicts against the independently observed raw source consensus, after explicitly classified frame operations.',
                'minimum_observed_substitutions': best, 'rows': rows}})

    # Unknown digit cells never enter these all-letter bodies; every global square
    # completion gives the same independent target ciphertexts.
    unknown = [i for i, c in enumerate(key['square']) if c == '?']
    labels = sorted(set(A) - set(key['square']))
    completed = 0
    for symbols in itertools.permutations(labels):
        square = list(key['square'])
        for i, c in zip(unknown, symbols):
            square[i] = c
        square = ''.join(square)
        for record, target in zip(data['records'], [consensus, target_c]):
            assert encrypt(record['target'], key['column_rank_order'], square) == target
        completed += 1
    assert completed == 120

    case = (ROOT / data['case']).read_text()
    for source, record in zip(data['records'], records):
        assert 'Literal header: `' + source['literal_header'] + '`.' in case
        assert '\n'.join(source['source_rows']) in case
        for plain in [record['native_frame']['raw'], record['primary']['raw'], source['target']]:
            assert '\n```text\n' + plain + '\n```\n' in case
        assert '> ' + source['readable_german'] + '\n' in case
    assert 'four exclude a masked glyph' in case and 'seven exclude an observed D' in case
    return {'schema': 'adfgvx-cross-source-seifert-witness-certificate-v1',
        'project': data['project'], 'authors': data['authors'],
        'input_sha256': sha(HERE / 'inputs.json'), 'indexing': 'All indices are zero-based.',
        'summary': {'physical_records': 2, 'printed_source_slots': 104,
            'valid_source_coordinates': 97, 'modeled_coordinates': 122,
            'plaintext_positions': 61, 'baseline_fixed_positions': 35,
            'candidate_fixed_positions': 61, 'known_coordinate_substitutions': 2,
            'printed_mask_fills': 6, 'added_model_slots': 20, 'added_slot_fills': 20,
            'observed_coordinate_exclusions': 1, 'masked_slot_exclusions': 1,
            'source_exclusions': 2, 'published_key_changed': False,
            'scope': 'Primary p182 A source48-mask exclusion plus p182 C source48-X exclusion. All other A minima remain separate.'},
        'records': records,
        'arrival_enquiry_raw_consensus': {'witness_ids': ['p174_B', 'p183_B'],
            'ciphertext': consensus, 'raw': consensus_plain,
            'shared_known_coordinates': sum(a != '?' and b != '?' for a, b in zip(old_b, new_b)),
            'observed_coordinate_conflicts': 0, 'covered_coordinates': 74,
            'complete_pair_support': complete_pair_support, 'new_record_counted': False},
        'return_enquiry_native_witness': {'id': 'p174_C', 'ciphertext': target_c,
            'raw': witnesses['p174_C']['raw_plaintext'], 'new_record_counted': False},
        'all_global_square_completions_checked': completed,
        'prior_credit': data['prior_credit'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
