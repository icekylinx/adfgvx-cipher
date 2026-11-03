#!/usr/bin/env python3
"""Price all five-exclusion maps for the explicitly partial p59 A1 stencil.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
All minimum frames survive; names and numerical fields never enter the stencil.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, untranspose
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import (
    inspect, repair, permutation, masked_encryption,
)

C = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def constrained_stream(anchors, key, positions=110):
    text = ['?'] * positions
    for start, word in anchors:
        for i, letter in enumerate(word, start):
            assert text[i] in ('?', letter)
            text[i] = letter
    return ''.join(text), masked_encryption(''.join(text), key)


def exact_alignment(source, target, enumerate_minima=False):
    """Optimal monotone keep/drop paths, lexicographic observed/masked cost.

    State(i,d) has consumed i literal source positions and excluded exactly d.
    Every other consumed position is aligned to the target at i-d. Thus every
    five-exclusion subset occurs exactly once, regardless of identical glyphs.
    """
    n, m = len(source), len(target)
    removed = n - m
    costs = [[None] * (removed + 1) for _ in range(n + 1)]
    counts = [[0] * (removed + 1) for _ in range(n + 1)]
    costs[0][0], counts[0][0] = (0, 0), 1

    def addition(a, b):
        return (int(a in C and b in C and a != b), int(a not in C and b in C))

    def offer(i, d, cost, ways):
        if costs[i][d] is None or cost < costs[i][d]:
            costs[i][d], counts[i][d] = cost, ways
        elif cost == costs[i][d]:
            counts[i][d] += ways

    for i in range(n):
        for d in range(removed + 1):
            value = costs[i][d]
            if value is None:
                continue
            if d < removed:
                offer(i + 1, d + 1, value, counts[i][d])
            j = i - d
            if 0 <= j < m:
                a, b = addition(source[i], target[j])
                offer(i + 1, d, (value[0] + a, value[1] + b), counts[i][d])
    paths = []

    def backtrack(i, d, excluded):
        if i == 0:
            assert d == 0
            paths.append(sorted(excluded))
            return
        if d and costs[i-1][d-1] == costs[i][d]:
            backtrack(i-1, d-1, excluded + [i-1])
        j = i - d
        if j > 0 and costs[i-1][d] is not None:
            prior = costs[i-1][d]
            a, b = addition(source[i-1], target[j-1])
            if (prior[0] + a, prior[1] + b) == costs[i][d]:
                backtrack(i-1, d, excluded)

    if enumerate_minima:
        backtrack(n, removed, [])
        paths.sort()
        assert len(paths) == len({tuple(p) for p in paths}) == counts[n][removed]
    return {'minimum_cost': list(costs[n][removed]), 'minimum_paths': counts[n][removed],
            'excluded_source_index_sets': paths,
            'covered_five_exclusion_subsets': math.comb(n, removed),
            'terminal_state': {'source_positions_consumed': n, 'excluded': removed,
                               'target_positions_consumed': m}}


def build():
    inp = json.loads((HERE / 'inputs.json').read_text())
    key, record = inp['key'], inp['record']
    assert inp['authors'] == 'icekylinx and GPT-6 Astra Pro'
    assert key == next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                       if k['id'] == key['id'])
    prior = inp['prior_source_edition']
    assert sha(ROOT / prior['path']) == prior['sha256']
    old = json.loads((ROOT / prior['path']).read_text())
    witness = next(r for r in old['contextual_unread_records'] if r['id'] == record['id'])
    assert record['source_rows'] == witness['source_rows']
    literal = ''.join(''.join(record['source_rows']).split())
    source = ''.join(c if c in C else '?' for c in literal)
    assert len(source) == record['source_slots'] == 225
    assert record['advertised_length'] == 220
    assert sum(c in C for c in literal) == 217
    native_order = permutation(len(source), key['column_rank_order'])
    native_middle = untranspose(source, key['column_rank_order'])
    assert native_middle == ''.join(source[i] for i in native_order)
    native = {'source_slots': len(source), 'literal_source': literal,
              'paired_plaintext': decrypt(source, key['column_rank_order'], key['square'], allow_unpaired=True),
              'paired_positions': len(source)//2,
              'orphan': {'intermediate_index': 224, 'source_index': native_order[-1],
                         'coordinate': native_middle[-1]}, 'source_exclusions': []}
    anchors = record['ordinary_word_anchors']
    template, target = constrained_stream(anchors, key)
    search = exact_alignment(source, target, True)
    expected = inp['bounded_search']
    assert search['minimum_cost'] == expected['expected_minimum_cost']
    assert search['minimum_paths'] == expected['expected_minimizing_source_maps']
    assert search['covered_five_exclusion_subsets'] == 4595146920
    alternatives = []
    for excluded in search['excluded_source_index_sets']:
        mapping = [i for i in range(len(source)) if i not in excluded]
        cipher = ''.join(source[i] for i in mapping)
        raw = inspect(cipher, key, mapping)
        edited = list(raw['raw'])
        for at, word in anchors:
            edited[at:at+len(word)] = word
        candidate = repair(''.join(edited), cipher, key, mapping, literal)
        assert [len(candidate['known_coordinate_substitutions']),
                len(candidate['erased_coordinate_fills'])] == search['minimum_cost']
        complete_cipher = candidate['ciphertext'].replace('?', 'A')
        complete_plaintext = decrypt(complete_cipher, key['column_rank_order'], key['square'])
        assert encrypt(complete_plaintext, key['column_rank_order'], key['square']) == complete_cipher
        assert all(a == '?' or a == b for a, b in zip(candidate['raw'], complete_plaintext))
        alternatives.append({'excluded_source_indices': excluded,
                             'excluded_literal_coordinates': ''.join(literal[i] for i in excluded),
                             'excluded_valid_coordinates': sum(literal[i] in C for i in excluded),
                             'model_to_source_indices': mapping, 'baseline': raw,
                             'limited_candidate': candidate,
                             'remaining_completion_count': math.prod(len(p['domain']) for p in candidate['positions']),
                             'completion_witness': {'ciphertext': complete_cipher, 'plaintext': complete_plaintext,
                                                    'exact_roundtrip': True, 'historical_completion_claim': False}})
    assert len({r['baseline']['raw'] for r in alternatives}) == expected['expected_distinct_raw_streams']
    primary = next(r for r in alternatives if r['excluded_source_indices'] == record['conditional_excluded_source_indices'])
    assert primary['baseline']['raw'] == record['expected_raw']
    assert primary['limited_candidate']['raw'] == record['edited_output']
    assert primary['baseline']['fixed_positions'] == 103
    assert primary['limited_candidate']['fixed_positions'] == 105
    holdouts = {}
    for name, spec in expected['holdouts'].items():
        chosen = [anchors[i] for i in spec['anchor_indices']]
        stencil, wanted = constrained_stream(chosen, key)
        result = exact_alignment(source, wanted)
        assert result['minimum_cost'] == spec['minimum_cost'], (name, result)
        assert result['minimum_paths'] == spec['minimum_paths'], (name, result)
        holdouts[name] = {**result, 'anchors': chosen, 'plaintext_stencil': stencil}
    case = (ROOT / inp['case']).read_text()
    displays = re.findall(r'```text\n(.*?)\n```', case, re.S)
    assert displays == [record['expected_raw'], record['edited_output']]
    quote = '\n'.join(line[2:] for line in case.splitlines() if line.startswith('> '))
    assert quote == record['readable_german']
    fold = lambda s: re.sub('[^A-Z0-9?]', '', s.upper()).replace('X', '')
    assert fold(quote) == fold(record['edited_output'])
    for token in record['protected_fields']:
        assert token in record['expected_raw'] and token in record['edited_output']
    summary = {'physical_records': 1, 'printed_source_slots': 225, 'valid_source_coordinates': 217,
               'modeled_coordinates': 220, 'plaintext_positions': 110, 'baseline_fixed_positions': 103,
               'candidate_fixed_positions': 105, 'known_coordinate_substitutions': 5,
               'printed_mask_fills': 2, 'source_exclusions': 5, 'excluded_valid_source_coordinates': 5,
               'added_model_slots': 0, 'minimum_source_maps': 21, 'distinct_raw_streams': 8,
               'published_key_changed': False, 'frame_historically_established': False}
    return {'schema': 'adfgvx-poti-first-part-conditional-certificate-v1',
            'authors': inp['authors'], 'source_record': record['id'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'summary': summary,
            'native_diagnostic': native, 'record': {'id': record['id'], **primary},
            'plaintext_stencil': template, 'ciphertext_stencil': target,
            'bounded_search': search, 'all_minimum_frames': alternatives,
            'withheld_constraint_searches': holdouts, 'prior_credit': inp['credit'], 'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    inp = json.loads((HERE / 'inputs.json').read_text())
    evidence = verify_source_evidence(args.pdf, inp['source'], inp['source_images'], HERE)
    certificate = build()
    path = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(path.read_text()) == certificate
    else:
        path.write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': True, 'summary': certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))


if __name__ == '__main__':
    main()
