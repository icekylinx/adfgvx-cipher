#!/usr/bin/env python3
"""Verify five optional lexical spans in the explicitly jammed p116 A13.

Prepared by icekylinx and GPT-6 Astra Pro. The primary raw-only edition and
the published Nov1-3 key remain unchanged. Every fill is target-conditioned.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.mackensen_withdrawal_report.verify import (
    CO, frame_for, inspect, record_certificate, stencil)
from data.reviews.check_reading_presentation import displays, expected_legend


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alignment_audit(word, model, mapping, key, length):
    rows = []
    for start in range(length - len(word) + 1):
        target = '?' * start + word + '?' * (length - start - len(word))
        encoded = stencil(target, key)
        changes = [(i, old, new) for i, (old, new) in enumerate(zip(model, encoded))
                   if new != '?' and old != new]
        rows.append({
            'plaintext_start': start,
            'observed_substitutions': sum(old in CO for _, old, _ in changes),
            'printed_mask_fills': sum(old == '?' and mapping[i] is not None
                                      for i, old, _ in changes),
            'lost_tail_fills': sum(old == '?' and mapping[i] is None
                                   for i, old, _ in changes)})
    minimum = min(row['observed_substitutions'] for row in rows)
    return {'word': word, 'all_start_positions': rows,
            'minimum_observed_substitutions': minimum,
            'all_minimum_starts': [row['plaintext_start'] for row in rows
                                   if row['observed_substitutions'] == minimum],
            'limit': 'This fixed word was selected after reading the prior translation and source. Unique placement among its possible offsets is not uniqueness among other words or a historical proof.'}


def check_image(item, document=None):
    assert sha(ROOT / item['path']) == item['sha256']
    if document is not None:
        import fitz
        if item.get('fresh_render_cache'):
            fitz.TOOLS.store_shrink(100)
        pix = document[item['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(item['render_scale'], item['render_scale']),
            clip=fitz.Rect(*item['crop_pdf_points']), alpha=False)
        saved = fitz.Pixmap(str(ROOT / item['path']))
        assert (pix.width, pix.height, pix.n) == (saved.width, saved.height, saved.n)
        assert pix.samples == saved.samples


def rebuild(inp, pdf=None):
    live = json.loads((ROOT / inp['live_input_path']).read_text())
    record = next(row for row in live['records'] if row['id'] == 'p116_A13')
    key = live['key']
    assert record == inp['record_snapshot'] and key == inp['key_snapshot']
    published = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                     if k['id'] == key['id'])
    assert all(published[k] == v for k, v in key.items())
    assert live['prior_credit'] == inp['prior_credit']
    literal, model, mapping = frame_for(record)
    assert len(literal) == 160 and literal.count('-') == 16
    assert len(model) == 222 and mapping == list(range(160)) + [None] * 62
    assert record['frame_model'] == {'kind': 'explicit_jammed_tail',
                                     'source_gap_index': 160, 'added_coordinates': 62}
    native = inspect(literal.replace('-', '?'), key, list(range(160)))
    primary = record_certificate(record, key)
    assert primary['raw']['raw'] == primary['edition']['raw'] == record['expected_raw']
    assert primary['raw']['fixed_positions'] == 38
    assert not (primary['known_coordinate_substitutions'] or primary['source_mask_fills']
                or primary['inserted_coordinate_fills'])
    proposal = inp['proposal']
    target = list(record['expected_raw'])
    positions_chosen = set()
    for word in proposal['new_word_spans']:
        start, text = word['start'], word['text']
        assert not positions_chosen.intersection(range(start, start + len(text)))
        positions_chosen.update(range(start, start + len(text)))
        target[start:start + len(text)] = text
    target = ''.join(target)
    assert target == proposal['editorial_text'] and len(target) == 111
    assert all(old == new for i, (old, new) in enumerate(zip(record['expected_raw'], target))
               if i not in positions_chosen)
    optional_record = {**record, 'editorial_plaintext': target,
                       'edition_scope': 'Optional target-conditioned lexical supplement only'}
    optional = record_certificate(optional_record, key)
    assert optional['known_coordinate_substitutions'] == []
    assert optional['edition']['fixed_positions'] == proposal['expected_fixed_positions'] == 75
    printed_fills = optional['source_mask_fills']
    lost_fills = optional['inserted_coordinate_fills']
    assert [[e['source_index'], e['to']] for e in printed_fills] == proposal['expected_printed_mask_fills']
    assert [[e['model_index'], e['to']] for e in lost_fills] == proposal['expected_lost_tail_fills']
    assert len(printed_fills) == 5 and len(lost_fills) == 32
    changes = {e['model_index']: e for e in printed_fills + lost_fills}
    new_labels = []
    for before, after in zip(primary['raw']['positions'], optional['edition']['positions']):
        if before['raw_label'] == after['raw_label']:
            continue
        assert before['raw_label'] == '?' and after['raw_label'] != '?'
        assert before['pair'].count('?') == 1 and len(before['domain']) == 6
        assert after['raw_label'] in before['domain']
        known_pair_index = 0 if before['pair'][0] in CO else 1
        known_model_index = before['model_indices'][known_pair_index]
        assert mapping[known_model_index] is not None
        assert model[known_model_index] == optional['edition']['ciphertext'][known_model_index]
        filled_index = before['model_indices'][1 - known_pair_index]
        new_labels.append({
            'plaintext_position': before['plaintext_position'],
            'raw_pair': before['pair'], 'raw_domain': before['domain'],
            'proposed_label': after['raw_label'], 'proposed_pair': after['pair'],
            'model_indices': before['model_indices'], 'source_indices': before['source_indices'],
            'unchanged_observed_model_index': known_model_index,
            'unchanged_observed_source_index': mapping[known_model_index],
            'unchanged_observed_coordinate': model[known_model_index],
            'conditional_fill': changes[filled_index]})
    assert len(new_labels) == 37
    assert {e['conditional_fill']['model_index'] for e in new_labels} == set(changes)
    assert all(old == '?' or old == new for old, new in zip(model, optional['edition']['ciphertext']))
    unresolved = [p for p in optional['edition']['positions'] if p['raw_label'] == '?']
    assert len(unresolved) == 36
    assert [p['plaintext_position'] for p in unresolved] == proposal['preserved_unknown_positions']
    army = optional['edition']['positions'][10:13]
    assert [p['raw_label'] for p in army] == ['?', '?', '?']
    assert [p['domain'] for p in army] == ['1GHLWZ', '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'CRSVXZ']
    numeral = optional['edition']['positions'][103]
    assert numeral['raw_label'] == '1' and numeral == primary['raw']['positions'][103]
    audits = []
    span_ledger = []
    for word in proposal['new_word_spans']:
        audit = alignment_audit(word['text'], model, mapping, key, 111)
        assert audit['minimum_observed_substitutions'] == 0
        assert audit['all_minimum_starts'] == [word['start']]
        audits.append(audit)
        a, b = word['start'], word['start'] + len(word['text'])
        added = [p for p in new_labels if a <= p['plaintext_position'] < b]
        span_ledger.append({'start': a, 'end_exclusive': b, 'text': word['text'],
                            'unchanged_raw_span': record['expected_raw'][a:b],
                            'raw_fixed_labels': b - a - len(added),
                            'newly_proposed_labels': len(added),
                            'printed_mask_fills': sum(p['conditional_fill']['source_index'] is not None for p in added),
                            'lost_tail_fills': sum(p['conditional_fill']['source_index'] is None for p in added)})
    assert sum(len(a['all_start_positions']) for a in audits) == 503
    document = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        document = fitz.open(pdf)
    check_image(inp['source']['image'], document)
    case = inp['primary_case']
    case_text = (ROOT / case['path']).read_text()
    fences, quotes = displays(case_text)
    assert [line for line in case_text.splitlines() if re.match(r'^#{1,6} ', line)] == case['headings']
    assert [x['sha256'] for x in fences] == case['fence_sha256']
    assert [x['sha256'] for x in quotes] == case['quote_sha256']
    page = HERE / 'README.md'
    text = page.read_text()
    assert text.count(expected_legend(page)) == 1
    fences, quotes = displays(text)
    assert all(x['role_from_caption'] for x in fences + quotes)
    assert re.findall(r'```text\n(.*?)\n```', text, flags=re.S) == [record['expected_raw'], target]
    quote = ''.join(line[2:] for line in text.splitlines() if line.startswith('> '))
    assert re.sub(r'[^A-Z0-9?]', '', quote.upper()) == target
    summary = {'physical_records_added': 0, 'printed_source_slots': 160,
               'valid_source_coordinates': 144, 'existing_modeled_coordinates': 222,
               'plaintext_positions': 111, 'primary_raw_fixed_positions': 38,
               'optional_fixed_positions': 75, 'remaining_unknown_positions': 36,
               'observed_coordinate_substitutions': 0,
               'printed_mask_fills': 5, 'existing_lost_tail_fills': 32,
               'printed_masks_left_unknown': 11, 'lost_tail_coordinates_left_unknown': 30,
               'newly_chosen_labels_with_one_observed_coordinate': 37,
               'fixed_word_alignment_comparisons': 503,
               'additional_frame_assumptions': 0, 'source_deletions': 0,
               'source_reordering': False, 'published_key_changed': False,
               'primary_case_displays_unchanged': True}
    return {'schema': 'adfgvx-p116-optional-route-fragment-certificate-v1',
            'prepared_by': inp['prepared_by'], 'inputs_sha256': sha(HERE / 'inputs.json'),
            'summary': summary,
            'native_160_slot_reading': native,
            'unchanged_primary_raw_only_record': primary,
            'optional_lexical_completion': optional,
            'five_optional_spans': span_ledger,
            'all_37_conditional_label_fills': new_labels,
            'all_36_unresolved_positions': unresolved,
            'unresolved_army_label': army,
            'preserved_literal_numeral': numeral,
            'all_fixed_word_alignment_audits': audits,
            'translation_selection_aid': inp['translation_selection_aid'],
            'prior_credit': inp['prior_credit'], 'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    inp = json.loads((HERE / 'inputs.json').read_text())
    result = rebuild(inp, args.pdf)
    dest = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(dest.read_text()), 'Recomputed certificate differs'
    else:
        dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': args.pdf is not None,
                      **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
