#!/usr/bin/env python3
"""Verify exact source-retention bounds for the fixed earlier p176a proposal.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect
from data.reviews.check_reading_presentation import displays, expected_legend
from independent_check import check as independent_check
C = 'ADFGVX'


def load(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def align(source, target, enumerate_maps=False):
    """Forward prefix DP; count every monotone injection, not edit scripts."""
    n, extra = len(source), len(target) - len(source)
    costs = [[10000] * (extra + 1) for _ in range(n + 1)]
    counts = [[0] * (extra + 1) for _ in range(n + 1)]
    costs[0][0], counts[0][0] = 0, 1
    for i in range(n + 1):
        for added in range(extra + 1):
            value, count = costs[i][added], counts[i][added]
            if not count:
                continue
            options = []
            if added < extra:
                options.append((i, added + 1, value))
            if i < n:
                options.append((i + 1, added, value + (source[i] != '-' and source[i] != target[i + added])))
            for ni, na, nv in options:
                if nv < costs[ni][na]:
                    costs[ni][na], counts[ni][na] = nv, count
                elif nv == costs[ni][na]:
                    counts[ni][na] += count
    result = {'minimum_observed_substitutions': costs[n][extra],
              'exact_optimal_map_count': counts[n][extra], 'added_slots': extra}
    if enumerate_maps:
        @lru_cache(None)
        def paths(i, added):
            if (i, added) == (0, 0):
                return ((),)
            current, found = costs[i][added], []
            if i and current == costs[i - 1][added] + (source[i - 1] != '-' and source[i - 1] != target[i + added - 1]):
                found.extend(paths(i - 1, added))
            if added and current == costs[i][added - 1]:
                found.extend(p + (i + added - 1,) for p in paths(i, added - 1))
            return tuple(found)
        maps = sorted(set(paths(n, extra)))
        assert len(maps) == result['exact_optimal_map_count']
        result['all_optimal_added_model_indices'] = [list(p) for p in maps]
    return result


def witness(literal, excluded, inserted, target, key):
    retained = [i for i in range(len(literal)) if i != excluded]
    added = set(inserted)
    it = iter(retained)
    mapping = [None if i in added else next(it) for i in range(len(target))]
    assert [i for i in mapping if i is not None] == retained
    frame = ''.join('?' if i is None or literal[i] == '-' else literal[i] for i in mapping)
    events = []
    for j, (a, b) in enumerate(zip(frame, target)):
        if a != b:
            src = mapping[j]
            kind = 'added_slot_fill' if src is None else ('printed_mask_fill' if literal[src] == '-' else 'observed_substitution')
            events.append({'model_index': j, 'source_index': src, 'from': a, 'to': b, 'kind': kind})
    return {'excluded_printed_mask_index': excluded, 'added_model_indices': inserted,
            'model_to_source_indices': mapping, 'unfilled_frame': frame,
            'unfilled_raw': decrypt(frame, key['column_rank_order'], key['square']),
            'completed_ciphertext': target, 'events': events,
            'observed_substitutions': sum(e['kind'] == 'observed_substitution' for e in events),
            'printed_mask_fills': sum(e['kind'] == 'printed_mask_fill' for e in events),
            'added_slot_fills': sum(e['kind'] == 'added_slot_fill' for e in events),
            'all_observed_source_coordinates_retained_in_order': True}


def build(pdf=None):
    d = load(HERE / 'inputs.json')
    key = d['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov10-12')
    evidence = verify_source_evidence(pdf, d['source'], d['source_images'], HERE)
    for name in ['prior_snapshot', 'prior_case_displays']:
        assert sha(HERE / d[name]['path']) == d[name]['sha256']
    snap = load(HERE / d['prior_snapshot']['path'])
    assert sha(ROOT / snap['messages_origin']) == snap['messages_origin_sha256']
    assert sha(ROOT / snap['prior_origin']) == snap['prior_origin_sha256']
    assert d['fixed_target']['plaintext'] == snap['prior_record']['published_readings'][0]['compact_plaintext']
    plain = d['fixed_target']['plaintext']
    assert len(plain) == 112 and 'BEEURTEILT' in plain and '?' not in plain
    assert all(ch in key['square'] for ch in plain)
    target = encrypt(plain, key['column_rank_order'], key['square'])
    source = d['records'][0]
    literal = ''.join(''.join(source['source_rows']).split())
    assert literal == snap['message']['transcript']['raw_source_compact']
    assert len(literal) == 214 and sum(ch in C for ch in literal) == 204
    masks = [i for i, ch in enumerate(literal) if ch == '-']
    assert masks == [36, 37, 38, 123, 127, 128, 186, 187, 188, 213]
    raw = inspect(literal.replace('-', '?'), key, list(range(214)))
    assert raw['raw'] == source['expected_raw']
    bounds = []
    for excluded in [None] + masks:
        retained = ''.join(ch for i, ch in enumerate(literal) if i != excluded)
        result = align(retained, target, enumerate_maps=excluded in (None, 213))
        bounds.append({'excluded_printed_mask_index': excluded, **result})
    independent = independent_check()
    assert independent['encoded_target'] == target
    assert independent['bounds'] == [{k: v for k, v in b.items() if k != 'all_optimal_added_model_indices'} for b in bounds]
    assert bounds[0]['minimum_observed_substitutions'] == 68 and bounds[0]['exact_optimal_map_count'] == 252
    assert [(b['excluded_printed_mask_index'], b['minimum_observed_substitutions'], b['exact_optimal_map_count']) for b in bounds[1:]] == [
        (36, 68, 756), (37, 68, 756), (38, 68, 756), (123, 68, 1296),
        (127, 66, 36), (128, 66, 36), (186, 30, 2), (187, 30, 2), (188, 30, 2), (213, 13, 2)]
    witnesses = []
    for bound in [bounds[0], bounds[-1]]:
        excluded = bound['excluded_printed_mask_index']
        for added in bound['all_optimal_added_model_indices']:
            w = witness(literal, excluded, added, target, key)
            assert w['observed_substitutions'] == bound['minimum_observed_substitutions']
            assert w['printed_mask_fills'] == (10 if excluded is None else 9)
            assert w['added_slot_fills'] == (10 if excluded is None else 11)
        witnesses.append(witness(literal, excluded, bound['all_optimal_added_model_indices'][0], target, key))
    global_witnesses = []
    for values in itertools.permutations('56789'):
        it = iter(values)
        square = ''.join(next(it) if ch == '?' else ch for ch in key['square'])
        assert len(set(square)) == 36
        assert encrypt(plain, key['column_rank_order'], square) == target
        assert decrypt(target, key['column_rank_order'], square) == plain
        global_witnesses.append({'unknown_cell_assignment_in_square_order': ''.join(values), 'identical_target_ciphertext_and_roundtrip': True})
    assert len(global_witnesses) == 120
    case = ROOT / d['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    old = load(HERE / d['prior_case_displays']['path'])
    assert re.findall(r'```[^\n]*\n.*?\n```', text, re.S) == old['fenced_displays']
    assert re.findall(r'^> .*$', text, re.M) == old['quoted_lines']
    section = text.split('## ' + d['section_heading'] + '\n', 1)[1].split('\n## ', 1)[0]
    assert not any(displays(section))
    assert '| All 214 source slots | 10 | None | **68** | 252 |' in section
    assert '| Exclude final printed mask 213 | 11 | One mask | **13** | 2 |' in section
    return {'schema': 'adfgvx-p176a-source-retention-bound-certificate-v1',
            'authors': d['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': d['indexing'], 'fixed_target': d['fixed_target'],
            'summary': {'physical_sources': 1, 'native_source_slots': 214,
                'observed_source_coordinates': 204, 'native_printed_masks': 10,
                'conditional_target_positions': 112, 'conditional_model_slots': 224,
                'all_source_ten_insertion_minimum_observed_substitutions': 68,
                'all_source_optimal_maps': 252,
                'one_mask_exclusion_eleven_insertion_minimum_observed_substitutions': 13,
                'best_excluded_source_mask_index': 213, 'best_exclusion_optimal_maps': 2,
                'global_square_completions_checked': 120, 'historical_wording_uniqueness_claim': False},
            'records': [{'id': source['id'], 'literal_source': literal, 'source_slots': 214,
                'valid_coordinates': 204, 'ciphertext': literal.replace('-', '?'),
                'model_to_source_indices': list(range(214)), **raw}],
            'exact_alignment_bounds': bounds, 'one_attaining_witness_per_primary_family': witnesses,
            'independent_dp_check': independent, 'global_target_roundtrip_witnesses': global_witnesses,
            'limits': d['limits'], 'credit': d['credit']}, evidence


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    a = p.parse_args()
    result, evidence = build(a.pdf)
    if a.verify:
        assert result == load(HERE / 'certificates.json')
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': a.verify, **result['summary'], 'source_evidence': evidence['summary']}, indent=2))
