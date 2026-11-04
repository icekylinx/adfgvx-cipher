#!/usr/bin/env python3
"""Verify the p167 D source-retaining partial dispatch-word proposal.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair
from data.reviews.check_reading_presentation import displays, expected_legend
C = 'ADFGVX'


def load(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def word_stencil(spans, key):
    """Independent physical-column construction for the known word spans."""
    plain = ['?'] * 95
    for span in spans:
        plain[span['start']:span['stop']] = span['text']
    middle = []
    for ch in plain:
        if ch == '?':
            middle.extend('??')
        else:
            row, col = divmod(key['square'].index(ch), 6)
            middle.extend([C[row], C[col]])
    columns = [[] for _ in key['column_rank_order']]
    for i, ch in enumerate(middle):
        columns[i % len(columns)].append(ch)
    return ''.join(''.join(columns[key['column_rank_order'].index(rank)])
                   for rank in range(1, len(columns) + 1))


def global_witnesses(candidate, key, literal, mapping):
    unfilled = [i for i, ch in enumerate(candidate['ciphertext']) if ch == '?']
    out, texts = [], set()
    for values in itertools.permutations('56'):
        it = iter(values)
        square = ''.join(next(it) if ch == '?' else ch for ch in key['square'])
        assert len(set(square)) == 36
        for fills in itertools.product(C, repeat=len(unfilled)):
            cipher = list(candidate['ciphertext'])
            for i, ch in zip(unfilled, fills):
                cipher[i] = ch
            cipher = ''.join(cipher)
            text = decrypt(cipher, key['column_rank_order'], square)
            assert encrypt(text, key['column_rank_order'], square) == cipher
            assert all(a == '?' or a == b for a, b in zip(candidate['raw'], text))
            # Reprice the full witness against the source, retaining every slot.
            assert sum(literal[src] in C and literal[src] != cipher[i]
                       for i, src in enumerate(mapping) if src is not None) == 10
            texts.add(text)
            out.append({'square_values_in_unknown_cell_order': ''.join(values),
                        'unfilled_model_indices': unfilled,
                        'coordinate_fill_string': ''.join(fills), 'plaintext': text,
                        'full_roundtrip_verified': True, 'historical_completion_claim': False})
    return {'unfilled_model_indices': unfilled, 'full_square_and_coordinate_witnesses': len(out),
            'distinct_compatible_plaintexts': len(texts), 'witnesses': out}


def name_proposal(data, literal, models, primary):
    proposal, key = data['optional_name_proposal'], data['key']
    spans = data['records'][0]['proposed_spans'] + [{
        'start': proposal['plaintext_start'], 'stop': proposal['plaintext_stop'],
        'text': proposal['proposal']}]
    stencil = word_stencil(spans, key)
    prices = [{'source_insertion_boundaries': m['source_insertion_boundaries'],
               'observed_substitutions': sum(src is not None and literal[src] in C and target in C and literal[src] != target
                                             for src, target in zip(m['model_to_source_indices'], stencil))}
              for m in models]
    minimum = min(p['observed_substitutions'] for p in prices)
    minima = [p['source_insertion_boundaries'] for p in prices if p['observed_substitutions'] == minimum]
    assert minimum == 14 and minima == data['geometry_scope']['all_six_observed_price_minima']
    variants = []
    for model in models:
        if model['source_insertion_boundaries'] not in minima:
            continue
        base = model['readable_candidate']
        start, stop = proposal['plaintext_start'], proposal['plaintext_stop']
        assert base['raw'][start:stop] == proposal['raw']
        text = base['raw'][:start] + proposal['proposal'] + base['raw'][stop:]
        extra = repair(text, base['ciphertext'], key, model['model_to_source_indices'], literal)
        assert [[e['source_index'], e['from'], e['to']] for e in extra['known_coordinate_substitutions']] == proposal['additional_observed_substitutions']
        assert not extra['erased_coordinate_fills']
        variants.append({'source_insertion_boundaries': model['source_insertion_boundaries'],
                         'additional_observed_substitutions': extra['known_coordinate_substitutions'],
                         'additional_source_or_added_fills': 0})
        if model is primary:
            completed = repair(text, model['ciphertext'], key, model['model_to_source_indices'], literal)
    donor_spec = proposal['donor']
    donor_data = load(ROOT / donor_spec['inputs'])
    donor = next(r for r in donor_data['records'] if r['id'] == donor_spec['record'])
    donor_literal = ''.join(''.join(donor['source_rows']).split())
    assert hashlib.sha256(donor_literal.encode()).hexdigest() == donor_spec['source_sha256']
    donor_key = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == donor_spec['key_id'])
    donor_raw = inspect(donor_literal, donor_key, list(range(len(donor_literal))))
    assert donor_raw['raw'] == donor['expected_raw']
    start = donor_raw['raw'].index(donor_spec['observed_phrase'])
    positions = donor_raw['positions'][start:start + len(donor_spec['observed_phrase'])]
    assert all(len(p['domain']) == 1 and set(p['pair']) <= set(C) for p in positions)
    display = re.sub('[^A-Z0-9?]', '', proposal['readable_german'].replace('[…]', '').upper())
    displayed_spans = sorted(spans, key=lambda s: s['start'])
    assert display == ''.join(s['text'] for s in displayed_spans).replace('X', '')
    return {'proposal': proposal['proposal'], 'primary_completed_word_layer': completed,
            'readable_german': proposal['readable_german'], 'additional_proposed_span_positions': 10,
            'total_proposed_span_positions': 55, 'all_model_prices': prices,
            'minimum_substitution_maps': minima, 'tied_variants': variants,
            'donor': {**donor_spec, 'plaintext_start': start, 'positions': positions},
            'scope': proposal['scope']}


def build(pdf=None):
    d = load(HERE / 'inputs.json')
    key = d['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov7-9')
    evidence = verify_source_evidence(pdf, d['source'], d['source_images'], HERE)
    prior = d['prior_ocr']
    assert sha(HERE / prior['path']) == prior['sha256']
    assert sha(ROOT / prior['origin']) == prior['origin_sha256']
    assert load(HERE / prior['path']) == next(r for r in load(ROOT / prior['origin'])['blocks'] if r['id'] == 'p167_ocr_block7')
    r = d['records'][0]
    lit = ''.join(''.join(r['source_rows']).split())
    assert len(lit) == r['source_slots'] == 187 and r['advertised_length'] == 190
    assert [(i, ch) for i, ch in enumerate(lit) if ch not in C] == [(91, 'C'), (98, 'W'), (130, '-'), (131, '-')]
    for group in d['geometry_scope']['short_groups']:
        assert lit[group['source_start']:group['source_start'] + 4] == group['source_text']
    stencil = word_stencil(r['proposed_spans'], key)
    models = []
    for shifts in itertools.product(range(5), repeat=3):
        gaps = [a + b for a, b in zip([35, 59, 98], shifts)]
        mapping = []
        for i in range(188):
            mapping.extend([None] * gaps.count(i))
            if i < 187:
                mapping.append(i)
        assert [i for i in mapping if i is not None] == list(range(187))
        frame = ''.join(lit[i] if i is not None and lit[i] in C else '?' for i in mapping)
        raw = inspect(frame, key, mapping)
        text = list(raw['raw'])
        for span in r['proposed_spans']:
            text[span['start']:span['stop']] = span['text']
        candidate = repair(''.join(text), frame, key, mapping, lit)
        independently_priced = sum(src is not None and lit[src] in C and target in C and lit[src] != target
                                   for src, target in zip(mapping, stencil))
        assert independently_priced == len(candidate['known_coordinate_substitutions'])
        for start, stop in r['retained_raw_intervals']:
            assert candidate['raw'][start:stop] == raw['raw'][start:stop]
        events = candidate['erased_coordinate_fills']
        models.append({'source_insertion_boundaries': gaps, 'model_to_source_indices': mapping,
                       'ciphertext': frame, **raw, 'readable_candidate': candidate,
                       'observed_substitutions': independently_priced,
                       'source_mask_fills': sum(e['source_index'] is not None for e in events),
                       'added_slot_fills': sum(e['source_index'] is None for e in events)})
    assert len(models) == d['geometry_scope']['total_maps'] == 125
    minimum = min(m['observed_substitutions'] for m in models)
    assert minimum == 10
    tied = [m for m in models if m['observed_substitutions'] == minimum]
    assert [m['source_insertion_boundaries'] for m in tied] == d['geometry_scope']['all_six_observed_price_minima']
    assert [m['source_mask_fills'] for m in tied] == [2] * 6
    assert [m['added_slot_fills'] for m in tied] == [3, 3, 2, 2, 3, 3]
    primary = min(tied, key=lambda m: (m['source_mask_fills'] + m['added_slot_fills'], m['source_insertion_boundaries']))
    assert primary['source_insertion_boundaries'] == r['primary_gap_boundaries'] == [36, 59, 100]
    assert primary['raw'] == r['expected_raw'] and primary['fixed_positions'] == 84
    candidate = primary['readable_candidate']
    assert candidate['raw'] == r['readable_candidate'] and candidate['fixed_positions'] == 89
    assert candidate['raw'].count('?') == 6
    assert [(e['source_index'], e['from'], e['to']) for e in candidate['known_coordinate_substitutions']] == [
        (34, 'D', 'X'), (52, 'A', 'X'), (53, 'X', 'F'), (56, 'D', 'A'), (82, 'X', 'G'),
        (117, 'D', 'X'), (119, 'X', 'V'), (126, 'F', 'V'), (158, 'F', 'V'), (166, 'F', 'D')]
    assert [(e['source_index'], e['to']) for e in candidate['erased_coordinate_fills']] == [(None, 'F'), (91, 'G'), (None, 'D'), (131, 'A')]
    assert [p['plaintext_index'] for p in candidate['positions'] if p['raw'] == '?'] == [41, 49, 52, 89, 91, 94]
    completions = global_witnesses(candidate, key, lit, primary['model_to_source_indices'])
    assert completions['unfilled_model_indices'] == [36, 100, 133]
    assert completions['full_square_and_coordinate_witnesses'] == completions['distinct_compatible_plaintexts'] == 432
    for m in tied:
        m['global_completions'] = global_witnesses(m['readable_candidate'], key, lit, m['model_to_source_indices'])
    assert [m['global_completions']['full_square_and_coordinate_witnesses'] for m in tied] == [72, 72, 432, 432, 72, 72]
    optional_name = name_proposal(d, lit, models, primary)
    folded = re.sub('[^A-Z0-9?]', '', r['readable_german'].replace('[…]', '').upper())
    assert folded == ''.join(span['text'] for span in r['proposed_spans']).replace('X', '')
    case = ROOT / d['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(f['role_from_caption'] in {'raw_output', 'edited_output', 'source_transcription'} for f in fences)
    actual_streams = re.findall(r'```text\n(.*?)\n```', text, re.S)
    for required in [primary['raw'], candidate['raw'], '\n'.join(r['source_rows']), optional_name['primary_completed_word_layer']['raw']]:
        assert required in actual_streams
    actual_quotes = re.findall(r'^> (.*)$', text, re.M)
    assert r['readable_german'] in actual_quotes and optional_name['readable_german'] in actual_quotes
    return {'schema': 'adfgvx-p167-captain-dispatch-fragment-certificate-v1',
            'authors': d['authors'], 'input_sha256': sha(HERE / 'inputs.json'), 'indexing': d['indexing'],
            'summary': {'physical_records': 1, 'printed_source_slots': 187,
                'valid_source_coordinates': 183, 'source_masks_or_invalid_glyphs': 4,
                'added_model_slots': 3, 'modeled_coordinates': 190, 'plaintext_positions': 95,
                'baseline_fixed_positions': 84, 'candidate_fixed_positions': 89,
                'candidate_unknown_positions': 6, 'proposed_word_span_positions': 45,
                'known_coordinate_substitutions': 10, 'source_mask_fills': 2,
                'added_slot_fills': 2, 'source_deletions_or_movements': 0,
                'source_models_checked': 125, 'minimum_substitution_maps': 6,
                'minimum_fill_maps_within_those_six': 2,
                'primary_global_square_and_coordinate_completions': 432,
                'published_key_changed': False, 'complete_message_claim': False},
            'records': [{'id': r['id'], 'literal_source': lit, 'source_slots': 187,
                'valid_coordinates': 183, 'ciphertext': primary['ciphertext'],
                'model_to_source_indices': primary['model_to_source_indices'],
                'raw': primary['raw'], 'fixed_positions': primary['fixed_positions'],
                'positions': primary['positions'], 'readable_candidate': candidate,
                'readable_german': r['readable_german'], 'global_completions': completions,
                'optional_name_proposal': optional_name}],
            'geometry_enumeration': {'all_model_prices': [{k: m[k] for k in ['source_insertion_boundaries', 'observed_substitutions', 'source_mask_fills', 'added_slot_fills']} for m in models], 'all_six_minimum_maps': tied},
            'header': d['header'], 'prior_credit': d['prior_credit'], 'limits': d['limits']}, evidence


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
