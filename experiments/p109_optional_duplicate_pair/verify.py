#!/usr/bin/env python3
"""Verify the optional literal duplicate-pair geometry in p109 D.

Prepared by icekylinx and GPT-6 Astra Pro. The B-only geometry objective
retains surviving half-pairs and contains no proposed German plaintext.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from math import comb
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose
from experiments.mackensen_withdrawal_report.verify import inspect, inverse_order, stencil
from data.reviews.check_reading_presentation import displays, expected_legend


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def frame(source, excluded, key):
    mapping = [i for i in range(len(source)) if i not in excluded]
    cipher = ''.join(source[i] for i in mapping)
    return {'source_exclusion_indices': excluded,
            'source_exclusions': [{'source_index': i, 'coordinate': source[i]} for i in excluded],
            'retained_ciphertext': cipher, 'model_to_source_indices': mapping,
            'raw': inspect(cipher, key, mapping)}


def mismatches(a, b):
    assert len(a) == len(b)
    return sum(x != '?' and y != '?' and x != y for x, y in zip(a, b))


def minimum_against_B(source, encoded_B, key, scope):
    """All minimum ten-exclusion subsequences against observed B coordinates."""
    exclusions = len(source) - len(encoded_B)
    assert exclusions == 10
    infinity = len(source) + 1

    @lru_cache(None)
    def dp(i, d):
        j = i - d
        if i == len(source):
            return 0 if d == exclusions else infinity
        best = dp(i + 1, d + 1) if d < exclusions else infinity
        if j < len(encoded_B):
            cost = int(encoded_B[j] != '?' and source[i] != encoded_B[j])
            best = min(best, cost + dp(i + 1, d))
        return best

    @lru_cache(None)
    def count(i, d):
        if i == len(source):
            return int(d == exclusions)
        j, best = i - d, dp(i, d)
        n = count(i + 1, d + 1) if d < exclusions and dp(i + 1, d + 1) == best else 0
        if j < len(encoded_B):
            cost = int(encoded_B[j] != '?' and source[i] != encoded_B[j])
            if cost + dp(i + 1, d) == best:
                n += count(i + 1, d)
        return n

    descriptions = []

    def trace(i, d, excluded):
        if i == len(source):
            assert d == exclusions
            descriptions.append(excluded)
            return
        j, best = i - d, dp(i, d)
        if d < exclusions and dp(i + 1, d + 1) == best:
            trace(i + 1, d + 1, excluded + [i])
        if j < len(encoded_B):
            cost = int(encoded_B[j] != '?' and source[i] != encoded_B[j])
            if cost + dp(i + 1, d) == best:
                trace(i + 1, d, excluded)

    trace(0, 0, [])
    assert len(descriptions) == count(0, 0)
    grouped = {}
    for excluded in descriptions:
        value = ''.join(c for i, c in enumerate(source) if i not in excluded)
        assert mismatches(value, encoded_B) == dp(0, 0)
        raw = decrypt(value, key['column_rank_order'], key['square'])
        assert encrypt(raw, key['column_rank_order'], key['square']) == value
        grouped.setdefault(raw, []).append(excluded)
    common = ''.join(cs[0] if len(set(cs)) == 1 else '?' for cs in zip(*grouped))
    return {'scope': scope, 'encoded_B_objective': encoded_B,
            'source_exclusions': exclusions, 'source_subsequence_descriptions_in_scope': comb(len(source), exclusions),
            'minimum_known_coordinate_disagreements': dp(0, 0),
            'all_minimum_description_count': len(descriptions),
            'all_minimum_descriptions': descriptions,
            'distinct_raw_streams': [{'raw': s, 'source_exclusion_descriptions': ds} for s, ds in grouped.items()],
            'all_minimum_common_raw': common, 'enumeration_truncated': False,
            'German_target_used': False}


def repair_ledger(cipher, target, key, mapping):
    encoded = stencil(target, key)
    changes, fills = [], []
    for i, (old, new) in enumerate(zip(cipher, encoded)):
        if new == '?' or new == old:
            continue
        row = {'model_index': i, 'source_index': mapping[i], 'from': old, 'to': new}
        (fills if old == '?' else changes).append(row)
    return {'known_coordinate_substitutions': changes, 'printed_mask_fills': fills}


def check_pdf(inp, path):
    import fitz
    assert sha(path) == inp['source']['pdf_sha256']
    doc = fitz.open(path)
    item = inp['source']['fullpage_reviewed_pixels']
    fitz.TOOLS.store_shrink(100)
    pix = doc[item['pdf_page_1based'] - 1].get_pixmap(
        matrix=fitz.Matrix(item['scale'], item['scale']),
        clip=fitz.Rect(*item['crop_pdf_points']), alpha=False)
    assert (pix.width, pix.height, pix.n) == (item['width'], item['height'], item['channels'])
    assert hashlib.sha256(pix.samples).hexdigest() == item['rgb_sha256']
    item = inp['native_SAVE_witness']['image']
    fitz.TOOLS.store_shrink(100)
    pix = doc[item['pdf_page_1based'] - 1].get_pixmap(
        matrix=fitz.Matrix(item['scale'], item['scale']),
        clip=fitz.Rect(*item['clip_points']), alpha=False)
    assert hashlib.sha256(pix.samples).hexdigest() == item['pixel_sha256']


def build(inp, pdf=None):
    for path, digest in inp['base_sha256'].items():
        assert sha(ROOT / path) == digest
    current = next(r for r in load(ROOT / 'data/messages.json')['messages'] if r['id'] == 'p109')
    prior = next(r for r in load(ROOT / 'data/prior_readings.json')['messages'] if r['id'] == 'p109')
    assert current == inp['source_record_snapshot'] and prior == inp['prior_record_snapshot']
    parallel = load(ROOT / 'data/certificates/p109_parallel.json')
    assert parallel['source_B'] == inp['source_B_snapshot']
    assert parallel['source_D'] == inp['source_D_snapshot']
    old_ed = next(r for r in load(ROOT / 'data/certificates/editorial_readings.json')['readings'] if r['message_id'] == 'p109')
    assert old_ed == inp['earlier_editorial_snapshot']
    key = inp['key_snapshot']
    published = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    assert all(published[n] == value == prior['key'][n] for n, value in key.items())
    source = current['transcript']['analysis_ciphertext']
    b = parallel['source_B']['ciphertext']
    assert len(source) == 258 and len(b) == 248 and b.count('?') == 6
    assert source[65:75] == source[75:85] == inp['duplicate_model']['duplicated_coordinates']
    candidate = frame(source, inp['duplicate_model']['source_exclusion_indices'], key)
    other = frame(source, inp['duplicate_model']['other_complete_copy_exclusion_indices'], key)
    new = candidate['retained_ciphertext']
    raw = candidate['raw']['raw']
    assert new == other['retained_ciphertext'] and raw == inp['duplicate_model']['expected_raw']
    aliases = [i for i in range(len(source) - 9) if source[:i] + source[i+10:] == new]
    assert aliases == list(range(65, 78))
    old = prior['verified_variants'][0]['verification']['corrected_ciphertext']
    old_raw = decrypt(old, key['column_rank_order'], key['square'])
    assert old_raw == prior['verified_variants'][0]['verification']['raw_partial_plaintext']
    assert mismatches(b, old) == 42 and mismatches(b, new) == 38
    assert sum(x != '?' and x == y for x, y in zip(b, new)) == 204
    b_reading = inspect(b, key, list(range(len(b))))
    native = frame(source, [], key)
    order = inverse_order(248, key['column_rank_order'])
    audits = []
    for item in inp['B_only_optimization_scopes']:
        first, end = item['plaintext_scope']
        selected = set(order[2*first:2*end])
        masked_b = ''.join(ch if i in selected else '?' for i, ch in enumerate(b))
        result = minimum_against_B(source, masked_b, key, item['id'])
        result['plaintext_scope'] = [first, end]
        result['old_repaired_D_disagreements'] = mismatches(masked_b, old)
        result['duplicate_only_D_disagreements'] = mismatches(masked_b, new)
        assert candidate['source_exclusion_indices'] in result['all_minimum_descriptions']
        assert other['source_exclusion_indices'] in result['all_minimum_descriptions']
        audits.append(result)
    assert [(a['minimum_known_coordinate_disagreements'], a['all_minimum_description_count'], len(a['distinct_raw_streams']))
            for a in audits] == [(38, 118, 4), (36, 318, 32)]
    assert audits[1]['old_repaired_D_disagreements'] == 39
    diffs = [{'plaintext_index': i, 'old_raw': a, 'new_raw': z}
             for i, (a, z) in enumerate(zip(old_raw, raw)) if a != z]
    assert [d['plaintext_index'] for d in diffs] == [11, 21, 108, 117]
    target = inp['optional_edition']['plaintext']
    assert len(target) == len(raw) == 124
    for a, z in inp['optional_edition']['preserve_literal_spans']:
        assert target[a:z] == raw[a:z]
    repairs_D = repair_ledger(new, target, key, candidate['model_to_source_indices'])
    repairs_B = repair_ledger(b, target, key, list(range(len(b))))
    assert len(repairs_D['known_coordinate_substitutions']) == inp['optional_edition']['expected_D_substitutions'] == 21
    assert len(repairs_B['known_coordinate_substitutions']) == inp['optional_edition']['expected_B_substitutions'] == 21
    assert not repairs_D['printed_mask_fills'] and len(repairs_B['printed_mask_fills']) == 6
    encoded = encrypt(target, key['column_rank_order'], key['square'])
    assert decrypt(encoded, key['column_rank_order'], key['square']) == target
    old_target = old_ed['compact_plaintext']
    assert mismatches(new, encrypt(old_target, key['column_rank_order'], key['square'])) == 23
    assert mismatches(old, encrypt(old_target, key['column_rank_order'], key['square'])) == 23
    pair_b, pair_old, pair_new = [untranspose(value, key['column_rank_order']) for value in [b, old, new]]
    word_costs = []
    for start, word in [(18, 'SAVE'), (18, 'SAVA'), (23, 'UEBERGANG'), (39, 'TEILE')]:
        masked = '?' * start + word + '?' * (124 - start - len(word))
        code = stencil(masked, key)
        local_min = sum(min(mismatches(pair_b[2*i:2*i+2], stencil_char) + mismatches(pair_new[2*i:2*i+2], stencil_char)
                            for stencil_char in [a + z for a in 'ADFGVX' for z in 'ADFGVX'])
                        for i in range(start, start + len(word)))
        costs = {'B': mismatches(b, code), 'old_D': mismatches(old, code), 'duplicate_D': mismatches(new, code)}
        word_costs.append({'plaintext_start': start, 'word': word, 'observed_substitutions': costs,
                           'new_combined_local_minimum': local_min,
                           'new_combined_extra_cost': costs['B'] + costs['duplicate_D'] - local_min})
    assert [w['observed_substitutions'] for w in word_costs[:2]] == [
        {'B': 0, 'old_D': 3, 'duplicate_D': 2}, {'B': 1, 'old_D': 2, 'duplicate_D': 3}]
    witness = inp['native_SAVE_witness']
    live = load(ROOT / witness['input_path'])
    wr = next(r for r in live['records'] if r['id'] == witness['record_snapshot']['id'])
    assert wr == witness['record_snapshot'] and witness['key_snapshot'] == key
    literal = ''.join(''.join(wr['rows']).split())
    assert literal == wr['literal_source'] and len(literal) == 172
    assert wr['geometry']['kind'] == 'native' and wr['geometry']['source_origin_map'] == list(range(172))
    wraw = decrypt(literal, key['column_rank_order'], key['square'])
    assert wraw == wr['expected_raw'] and wr['expected_changes'] == []
    wreading = inspect(literal, key, list(range(172)))
    start = witness['plaintext_start']
    assert wraw[start:start + 4] == 'SAVE'
    native_word = {'id': wr['id'], 'key_id': key['id'], 'raw': wraw,
                  'plaintext_start': start, 'word': 'SAVE',
                  'observed_pair_witnesses': wreading['positions'][start:start + 4],
                  'source_exclusions': 0, 'source_substitutions': 0, 'coordinate_fills': 0,
                  'scope': witness['scope']}
    for item in inp['source']['bound_images']:
        assert sha(ROOT / item['path']) == item['sha256']
    if pdf:
        check_pdf(inp, pdf)
    primary = inp['primary_case']
    text = (ROOT / primary['path']).read_text()
    f, q = displays(text)
    assert [s for s in text.splitlines() if re.match(r'^#{1,6} ', s)] == primary['headings']
    assert [s['sha256'] for s in f] == primary['fence_sha256']
    assert [s['sha256'] for s in q] == primary['quote_sha256']
    page = HERE / 'README.md'
    text = page.read_text()
    f, q = displays(text)
    assert text.count(expected_legend(page)) == 1
    assert all(s['role_from_caption'] for s in f + q)
    assert re.findall(r'```text\n(.*?)\n```', text, flags=re.S) == [b_reading['raw'], old_raw, raw, target]
    quote = ''.join(s[2:] for s in text.splitlines() if s.startswith('> '))
    assert re.sub(r'[^A-Z0-9?]', '', quote.upper()) == target
    summary = {'physical_records_added': 0, 'printed_D_coordinates': 258,
               'retained_D_coordinates': 248, 'source_exclusions': 10,
               'raw_geometry_substitutions': 0, 'raw_geometry_fills': 0,
               'raw_plaintext_positions': 124, 'known_B_agreements': 204,
               'known_B_disagreements': 38, 'B_printed_masks': 6,
               'all_full_B_minimum_descriptions': 118, 'all_body_B_minimum_descriptions': 318,
               'optional_D_word_substitutions': 21, 'optional_B_comparison_substitutions': 21,
               'optional_B_comparison_mask_fills': 6,
               'primary_displays_unchanged': True, 'core_data_unchanged': True}
    return {'schema': 'adfgvx-p109-optional-duplicate-pair-certificate-v1',
            'prepared_by': inp['prepared_by'], 'inputs_sha256': sha(HERE / 'inputs.json'),
            'summary': summary, 'source': inp['source'], 'native_258_D': native,
            'native_B_reading': b_reading,
            'earlier_D': {'ciphertext': old, 'raw': old_raw, 'source_repair': prior['verified_variants'][0]['ciphertext_edits']},
            'duplicate_only_D': candidate, 'other_whole_copy_deletion': other,
            'all_equivalent_contiguous_ten_deletion_starts': aliases,
            'four_geometry_dependent_label_changes': diffs,
            'B_only_geometry_optimizations': audits,
            'optional_edition': {'plaintext': target, 'ciphertext': encoded,
                'D_repairs': repairs_D, 'B_comparison_repairs': repairs_B,
                'combined_known_substitutions': 42, 'combined_minimum': 38,
                'extra_above_combined_minimum': 4, 'ordinary_roundtrip': True},
            'fixed_earlier_full_editorial_candidate_D_cost': {'old_frame': 23, 'duplicate_frame': 23},
            'explicit_word_costs': word_costs, 'independent_native_SAVE_witness': native_word,
            'prior_credit': inp['prior_credit'], 'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(load(HERE / 'inputs.json'), args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert load(path) == result, 'Exact recomputation differs'
    else:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': args.pdf is not None,
                      **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
