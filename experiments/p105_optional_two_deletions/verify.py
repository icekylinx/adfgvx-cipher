#!/usr/bin/env python3
"""Verify an optional two-source-deletion model for original challenge p105.

icekylinx and GPT-6 Astra Pro. Earlier plaintext, key and source credits remain.
The optimization is explicitly conditioned on retrospective fixed word spans.
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


def make_target(length, spans, selected):
    target = ['?'] * length
    covered = set()
    for i in selected:
        row = spans[i]
        start, word = row['plaintext_start'], row['text']
        assert start + len(word) <= length
        assert not covered.intersection(range(start, start + len(word)))
        covered.update(range(start, start + len(word)))
        target[start:start + len(word)] = word
    return ''.join(target)


def reduced_source(source, excluded):
    assert sorted(set(excluded)) == excluded
    assert all(0 <= i < len(source) for i in excluded)
    mapping = [i for i in range(len(source)) if i not in excluded]
    return ''.join(source[i] for i in mapping), mapping


def price(model, target, mapping, key):
    encoded = stencil(target, key)
    assert len(encoded) == len(model) == len(mapping)
    return [{'model_index': i, 'source_index': mapping[i], 'from': old, 'to': new}
            for i, (old, new) in enumerate(zip(model, encoded))
            if new != '?' and old != new]


def minimum_exclusions(source, key, deletion_count, target, scope):
    """All exact minimum-cost subsequences, retaining original source order.

    A state (i, d) consumes source prefix i with d exclusions. Retaining the
    next source coordinate compares it with encoded stencil index i-d;
    excluding it has its separately declared source-loss cost, never a free
    observed-coordinate substitution. Every tied optimum is enumerated.
    """
    encoded = stencil(target, key)
    assert len(source) - deletion_count == len(encoded)
    infinity = len(source) + 1

    @lru_cache(None)
    def dp(i, d):
        j = i - d
        if i == len(source):
            return 0 if d == deletion_count and j == len(encoded) else infinity
        best = dp(i + 1, d + 1) if d < deletion_count else infinity
        if j < len(encoded):
            mismatch = int(encoded[j] != '?' and source[i] != encoded[j])
            best = min(best, mismatch + dp(i + 1, d))
        return best

    @lru_cache(None)
    def count(i, d):
        if i == len(source):
            return int(d == deletion_count)
        j, best = i - d, dp(i, d)
        ways = 0
        if d < deletion_count and dp(i + 1, d + 1) == best:
            ways += count(i + 1, d + 1)
        if j < len(encoded):
            mismatch = int(encoded[j] != '?' and source[i] != encoded[j])
            if mismatch + dp(i + 1, d) == best:
                ways += count(i + 1, d)
        return ways

    descriptions = []

    def trace(i, d, excluded):
        if i == len(source):
            assert d == deletion_count
            descriptions.append(excluded)
            return
        j, best = i - d, dp(i, d)
        if d < deletion_count and dp(i + 1, d + 1) == best:
            trace(i + 1, d + 1, excluded + [i])
        if j < len(encoded):
            mismatch = int(encoded[j] != '?' and source[i] != encoded[j])
            if mismatch + dp(i + 1, d) == best:
                trace(i + 1, d, excluded)

    trace(0, 0, [])
    assert len(descriptions) == count(0, 0)
    assert descriptions == sorted(descriptions)
    grouped = {}
    for excluded in descriptions:
        model, mapping = reduced_source(source, excluded)
        raw = decrypt(model, key['column_rank_order'], key['square'])
        assert encrypt(raw, key['column_rank_order'], key['square']) == model
        assert len(price(model, target, mapping, key)) == dp(0, 0)
        grouped.setdefault(raw, []).append(excluded)
    common = ''.join(chars[0] if len(set(chars)) == 1 else '?'
                     for chars in zip(*grouped))
    return {'scope': scope, 'source_exclusions': deletion_count,
            'source_subsequence_descriptions_in_scope': comb(len(source), deletion_count),
            'retained_coordinates': len(encoded), 'plaintext_positions': len(target),
            'plaintext_stencil': target, 'encoded_stencil': encoded,
            'minimum_observed_substitutions': dp(0, 0),
            'unit_cost_exclusions_plus_substitutions': deletion_count + dp(0, 0),
            'all_minimum_description_count': len(descriptions),
            'all_minimum_descriptions': descriptions,
            'distinct_raw_streams': [{'raw': raw, 'source_exclusion_descriptions': ds}
                                   for raw, ds in grouped.items()],
            'all_minimum_common_raw': common,
            'common_raw_fixed_positions': len(common) - common.count('?'),
            'enumeration_truncated': False}


def frame(source, excluded, key):
    model, mapping = reduced_source(source, excluded)
    raw = inspect(model, key, mapping)
    assert encrypt(raw['raw'], key['column_rank_order'], key['square']) == model
    return {'source_exclusion_indices': excluded,
            'source_exclusions': [{'source_index': i, 'observed_coordinate': source[i],
                                   'group_1based': i // 5 + 1,
                                   'offset_within_group_0based': i % 5}
                                  for i in excluded],
            'retained_ciphertext': model, 'model_to_source_indices': mapping,
            'raw': raw, 'ordinary_roundtrip': True}


def native_word_witness(item):
    live = load(ROOT / item['live_input_path'])
    record = next(row for row in live['records'] if row['id'] == item['record_id'])
    assert record == item['record_snapshot']
    key = item['key_snapshot']
    published = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    assert all(published[k] == v for k, v in key.items())
    literal = ''.join(''.join(record['source_rows']).split())
    assert set(literal) <= set('ADFGVX')
    assert len(literal) == record['advertised_length'] == record['source_slots']
    raw = decrypt(literal, key['column_rank_order'], key['square'])
    assert raw == record['expected_raw']
    domains = plaintext_domains(literal, key['column_rank_order'], key['square'])
    order = inverse_order(len(literal), key['column_rank_order'])
    interim = untranspose(literal, key['column_rank_order'])
    spans = []
    for span in item['attested_spans']:
        start, text = span['plaintext_start'], span['text']
        assert raw[start:start + len(text)] == text
        letters = []
        for i in range(start, start + len(text)):
            pair = interim[2*i:2*i+2]
            assert domains[i] == raw[i]
            letters.append({'plaintext_position': i, 'label': raw[i], 'pair': pair,
                            'source_indices': order[2*i:2*i+2]})
        spans.append({**span, 'letters': letters})
    assert sha(ROOT / item['source_image']['path']) == item['source_image']['sha256']
    return {'record_id': record['id'], 'key_id': key['id'], 'native_coordinates': len(literal),
            'raw': raw, 'attested_spans': spans, 'source_image': item['source_image'],
            'source_exclusions': 0, 'coordinate_substitutions': 0, 'fills': 0,
            'scope': 'Exact native vocabulary witness only; no shared-message or date inference.'}


def check_pdf(inp, path):
    import fitz
    assert sha(path) == inp['source']['pdf_sha256']
    doc = fitz.open(path)
    crop = inp['source']['reviewed_crop']
    fitz.TOOLS.store_shrink(100)
    pix = doc[inp['source']['pdf_page_1based'] - 1].get_pixmap(
        matrix=fitz.Matrix(crop['render_scale'], crop['render_scale']),
        clip=fitz.Rect(*crop['crop_pdf_points']), alpha=False)
    assert (pix.width, pix.height, pix.n) == (crop['width'], crop['height'], crop['channels'])
    assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']
    for witness in inp['native_word_witnesses']:
        item = witness['source_image']
        fitz.TOOLS.store_shrink(100)
        pix = doc[item['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(item['render_scale'], item['render_scale']),
            clip=fitz.Rect(*item['crop_pdf_points']), alpha=False)
        saved = fitz.Pixmap(str(ROOT / item['path']))
        assert (pix.width, pix.height, pix.n) == (saved.width, saved.height, saved.n)
        assert pix.samples == saved.samples


def build(inp, pdf=None):
    for path, digest in inp['base_sha256'].items():
        assert sha(ROOT / path) == digest
    source_record = next(r for r in load(ROOT / 'data/messages.json')['messages'] if r['id'] == 'p105')
    prior = next(r for r in load(ROOT / 'data/prior_readings.json')['messages'] if r['id'] == 'p105')
    assert source_record == inp['source_record_snapshot']
    assert prior == inp['prior_record_snapshot']
    source = ''.join(''.join(inp['source']['source_rows']).split())
    assert source == source_record['transcript']['raw_source_compact'] == prior['analysis_ciphertext']
    assert len(source) == 290 and set(source) <= set('ADFGVX')
    key = inp['key_snapshot']
    assert all(prior['key'][k] == v for k, v in key.items())
    published = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    assert all(published[k] == v for k, v in key.items())
    spans = inp['ordinary_word_spans']
    scopes = inp['selection_scopes']
    audits = []
    for dels in [0, 2, 4]:
        for scope in scopes if dels == 2 else scopes[:1]:
            target = make_target((len(source) - dels) // 2, spans, scope['span_indices'])
            audit = minimum_exclusions(source, key, dels, target, scope['id'])
            audit['selected_span_indices'] = scope['span_indices']
            audits.append(audit)
    full = next(a for a in audits if a['source_exclusions'] == 2 and a['scope'] == 'all_words')
    assert full['minimum_observed_substitutions'] == 3
    assert full['all_minimum_descriptions'] == [[a, b] for a in range(99, 105) for b in [107, 108]]
    assert len(full['distinct_raw_streams']) == 4
    prefix = next(a for a in audits if a['scope'] == 'prefix_only')
    assert prefix['minimum_observed_substitutions'] == 2
    assert prefix['all_minimum_description_count'] == 55
    assert prefix['all_minimum_common_raw'][105] == '1'
    assert prefix['all_minimum_common_raw'][131:135] == 'STAB'
    assert prefix['all_minimum_common_raw'][136:] == '32398XBR'
    no_div = next(a for a in audits if a['scope'] == 'without_mediterranean_division')
    assert no_div['all_minimum_descriptions'] == full['all_minimum_descriptions']
    native = frame(source, [], key)
    old = inp['older_frame']
    odd_model, odd_mapping = reduced_source(source, old['source_exclusions'])
    odd_interim = untranspose(odd_model, key['column_rank_order'])
    assert odd_interim[-1:] == old['unpaired_interim_suffix']
    assert odd_mapping[inverse_order(len(odd_model), key['column_rank_order'])[-1]] == old['explicit_orphan_source_index']
    odd_raw = decrypt(odd_model, key['column_rank_order'], key['square'], allow_unpaired=True)
    assert odd_raw == old['expected_raw']
    baseline = frame(source, old['source_exclusions'] + [old['explicit_orphan_source_index']], key)
    assert baseline['raw']['raw'] == odd_raw
    exploratory = inp['intermediate_full_target_comparison']
    exploratory_audit = minimum_exclusions(source, key, 4, exploratory['full_target'], 'older_full_target_including_reference_labels')
    assert exploratory_audit['minimum_observed_substitutions'] == exploratory['expected_minimum_observed_substitutions']
    assert exploratory_audit['all_minimum_descriptions'] == exploratory['expected_all_minimum_descriptions']
    intermediate = frame(source, exploratory['source_exclusions'], key)
    assert intermediate['raw']['raw'] == exploratory['expected_raw']
    chosen = inp['main_candidate']
    candidate = frame(source, chosen['source_exclusions'], key)
    raw = candidate['raw']['raw']
    assert raw == chosen['expected_raw']
    aliases = []
    for ds in chosen['equivalent_double_D_descriptions']:
        assert ds in full['all_minimum_descriptions']
        other = frame(source, ds, key)
        assert other['retained_ciphertext'] == candidate['retained_ciphertext']
        aliases.append(other)
    edited = list(raw)
    for edit in chosen['optional_word_changes']:
        assert edited[edit['plaintext_position']] == edit['from']
        edited[edit['plaintext_position']] = edit['to']
    edited = ''.join(edited)
    repairs = price(candidate['retained_ciphertext'], edited, candidate['model_to_source_indices'], key)
    assert [[r['source_index'], r['from'], r['to']] for r in repairs] == chosen['expected_observed_substitutions']
    repaired = encrypt(edited, key['column_rank_order'], key['square'])
    assert decrypt(repaired, key['column_rank_order'], key['square']) == edited
    edition = inspect(repaired, key, candidate['model_to_source_indices'])
    changes = []
    for edit in chosen['optional_word_changes']:
        i = edit['plaintext_position']
        changes.append({**edit, 'raw_pair': candidate['raw']['positions'][i],
                        'edited_pair': edition['positions'][i]})
    compared_frames = [('native_290', native), ('old_explicit_orphan_286', baseline),
                       ('intermediate_reference_conditioned_286', intermediate),
                       ('optional_double_D_288', candidate)]
    costs, span_gains, fields = [], [], []
    for name, value in compared_frames:
        target = make_target(len(value['raw']['raw']), spans, list(range(len(spans))))
        cost = price(value['retained_ciphertext'], target, value['model_to_source_indices'], key)
        costs.append({'frame': name, 'source_exclusions': len(value['source_exclusion_indices']),
                      'observed_substitutions_for_same_ten_words': len(cost),
                      'unit_cost_total': len(value['source_exclusion_indices']) + len(cost),
                      'substitution_ledger': cost})
        s = value['raw']['raw']
        fields.append({'frame': name, 'first_reference': s[62:64], 'second_reference': s[80:82],
                       'five_digit_reference': s[90:95], 'following_literal_label': s[96:98],
                       'date_field': s[105:115], 'closing_field': s[136:]})
    for span in spans:
        start, word = span['plaintext_start'], span['text']
        old_span = baseline['raw']['raw'][start:start + len(word)]
        new_span = raw[start:start + len(word)]
        span_gains.append({**span, 'baseline_raw': old_span, 'optional_raw': new_span,
                           'baseline_exact_labels': sum(a == b for a, b in zip(old_span, word)),
                           'optional_exact_labels': sum(a == b for a, b in zip(new_span, word))})
    witnesses = [native_word_witness(w) for w in inp['native_word_witnesses']]
    if pdf:
        check_pdf(inp, pdf)
    primary = inp['primary_case']
    case_text = (ROOT / primary['path']).read_text()
    fences, quotes = displays(case_text)
    assert [line for line in case_text.splitlines() if re.match(r'^#{1,6} ', line)] == primary['headings']
    assert [f['sha256'] for f in fences] == primary['fence_sha256']
    assert [q['sha256'] for q in quotes] == primary['quote_sha256']
    page = HERE / 'README.md'
    text = page.read_text()
    assert text.count(expected_legend(page)) == 1
    fences, quotes = displays(text)
    assert all(row['role_from_caption'] for row in fences + quotes)
    expected_streams = [source, native['raw']['raw'], baseline['raw']['raw'], raw, edited]
    actual_streams = [''.join(s.split()) for s in re.findall(r'```text\n(.*?)\n```', text, flags=re.S)]
    assert actual_streams == expected_streams
    quote = ''.join(line[2:] for line in text.splitlines() if line.startswith('> '))
    assert re.sub(r'[^A-Z0-9?]', '', quote.upper()) == edited
    summary = {'physical_records_added': 0, 'printed_coordinates': len(source),
               'retained_coordinates': len(candidate['retained_ciphertext']),
               'plaintext_positions': len(raw), 'source_exclusions': 2,
               'observed_coordinate_substitutions': len(repairs), 'coordinate_fills': 0,
               'unit_cost_exclusions_plus_substitutions': 2 + len(repairs),
               'all_two_exclusion_word_minima': len(full['all_minimum_descriptions']),
               'distinct_two_exclusion_raw_streams': len(full['distinct_raw_streams']),
               'selected_double_D_aliases': len(aliases),
               'prefix_only_minimum_descriptions': 55,
               'native_word_witness_records': len(witnesses),
               'native_word_witness_spans': sum(len(w['attested_spans']) for w in witnesses),
               'primary_p105_displays_unchanged': True, 'core_data_unchanged': True,
               'published_key_changed': False, 'source_order_changed': False}
    return {'schema': 'adfgvx-p105-optional-two-deletions-certificate-v1',
            'prepared_by': inp['prepared_by'], 'inputs_sha256': sha(HERE / 'inputs.json'),
            'summary': summary, 'source': inp['source'], 'native_290': native,
            'prior_287_with_unpaired_suffix': {'source_exclusion_indices': old['source_exclusions'],
              'retained_ciphertext': odd_model, 'model_to_source_indices': odd_mapping,
              'interim': odd_interim, 'paired_raw': odd_raw,
              'unpaired_suffix': old['unpaired_interim_suffix'],
              'unpaired_suffix_original_source_index': old['explicit_orphan_source_index']},
            'prior_286_explicit_orphan': baseline,
            'intermediate_286_reference_conditioned': intermediate,
            'intermediate_retrospective_full_target_audit': exploratory_audit,
            'optional_288_frame': candidate, 'equivalent_double_D_descriptions': aliases,
            'optional_word_edition': {'plaintext': edited, 'ciphertext': repaired,
              'known_coordinate_substitutions': repairs, 'changed_labels': changes,
              'source_mask_fills': [], 'inserted_coordinates': [], 'ordinary_roundtrip': True},
            'same_word_objective_frame_comparison': costs, 'raw_span_gains': span_gains,
            'geometry_dependent_literal_fields': fields,
            'all_exact_optimization_and_holdout_results': audits,
            'independent_native_word_witnesses': witnesses,
            'prior_credit': inp['prior_credit'], 'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(load(HERE / 'inputs.json'), args.pdf)
    dest = HERE / 'certificates.json'
    if args.verify:
        assert load(dest) == result, 'Certificate differs from exact recomputation'
    else:
        dest.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': args.pdf is not None,
                      **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
