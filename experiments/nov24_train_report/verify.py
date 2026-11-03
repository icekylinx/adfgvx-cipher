#!/usr/bin/env python3
"""Verify the conditional p217 B1 train and divisional-position reading.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, permutation
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame(literal, deletion, gap):
    assert literal[deletion:deletion + 5] == 'FXXXF'
    retained = [i for i in range(len(literal)) if not deletion <= i < deletion + 5]
    assert 0 <= gap <= len(retained)
    mapping = retained[:gap] + [None] * 5 + retained[gap:]
    base = ''.join(literal[i] if i is not None and literal[i] in C else '?' for i in mapping)
    assert len(mapping) == len(base) == len(literal) == 204
    assert len(set(i for i in mapping if i is not None)) == 199
    return base, mapping


def stencil(template, key):
    # Independent offset inverse: assign each encoded pair to its received slot.
    middle = ''.join('??' if ch == '?' else C[key['square'].index(ch) // 6] +
                     C[key['square'].index(ch) % 6] for ch in template)
    result = ['?'] * len(middle)
    for ch, received in zip(middle, permutation(len(middle), key['column_rank_order'])):
        result[received] = ch
    return ''.join(result)


def price(base, target, mapping):
    changed = [i for i, (a, b) in enumerate(zip(base, target)) if b in C and a in C and a != b]
    source_fills = [i for i, (a, b) in enumerate(zip(base, target)) if b in C and a == '?' and mapping[i] is not None]
    added_fills = [i for i, (a, b) in enumerate(zip(base, target)) if b in C and a == '?' and mapping[i] is None]
    return len(changed), len(source_fills), len(added_fills)


def layer(template, base, mapping, literal, key):
    target = stencil(template, key)
    corrected = ''.join(b if b in C else a for a, b in zip(base, target))
    output = inspect(corrected, key, mapping)
    assert all(wanted == '?' or wanted == actual for wanted, actual in zip(template, output['raw']))
    edits, masks, added = [], [], []
    for i, (a, b) in enumerate(zip(base, corrected)):
        if a == b:
            continue
        origin = mapping[i]
        event = {'model_index': i, 'source_index': origin,
                 'printed': literal[origin] if origin is not None else None, 'from': a, 'to': b}
        (edits if a in C else masks if origin is not None else added).append(event)
    assert price(base, target, mapping) == (len(edits), len(masks), len(added))
    restored = list(base)
    for event in edits + masks + added:
        restored[event['model_index']] = event['to']
    assert ''.join(restored) == corrected
    complete = corrected.replace('?', 'A')
    witness = decrypt(complete, key['column_rank_order'], key['square'])
    assert encrypt(witness, key['column_rank_order'], key['square']) == complete
    assert all(a == '?' or a == b for a, b in zip(output['raw'], witness))
    return {'template': template, 'ciphertext': corrected, **output,
            'known_coordinate_substitutions': edits, 'printed_mask_fills': masks,
            'inserted_slot_fills': added,
            'full_completion_witness': {'ciphertext': complete, 'plaintext': witness,
                                        'roundtrip_verified': True, 'historical_value_claim': False}}


def all_frames(literal, key, template):
    target = stencil(template, key)
    rows = []
    for deletion in [45, 50]:
        for gap in range(200):
            base, mapping = frame(literal, deletion, gap)
            costs = price(base, target, mapping)
            rows.append({'excluded_source_start': deletion, 'gap_in_retained_stream': gap,
                         'known_coordinate_substitutions': costs[0],
                         'printed_mask_fills': costs[1], 'inserted_slot_fills': costs[2]})
    assert len(rows) == 400
    minimum = min(r['known_coordinate_substitutions'] for r in rows)
    ties = []
    for row in rows:
        if row['known_coordinate_substitutions'] != minimum:
            continue
        base, mapping = frame(literal, row['excluded_source_start'], row['gap_in_retained_stream'])
        corrected = ''.join(b if b in C else a for a, b in zip(base, target))
        ties.append(dict(row, raw=decrypt(base, key['column_rank_order'], key['square']),
                         edited_raw=decrypt(corrected, key['column_rank_order'], key['square']),
                         frame_sha256=hashlib.sha256(base.encode()).hexdigest(),
                         edited_ciphertext_sha256=hashlib.sha256(corrected.encode()).hexdigest()))
    return {'maps_checked': len(rows), 'minimum_observed_substitutions': minimum,
            'all_prices': rows, 'all_minimum_maps': ties,
            'distinct_edited_streams_at_minimum': len({r['edited_ciphertext_sha256'] for r in ties})}


def folded(text):
    return re.sub('[^A-Z0-9?]', '', text.upper()).replace('X', '')


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov22-24')
    old = data['prior_source_snapshot']
    assert sha(ROOT / old['path']) == old['sha256']
    previous = load(ROOT / old['path'])
    record = data['records'][0]
    assert record['source_rows'] == previous['unaccepted_first_part']['source_rows']
    literal = ''.join(''.join(record['source_rows']).split())
    assert len(literal) == record['source_slots'] == record['advertised_length'] == 204
    assert literal.count('-') == 21 and literal[45:50] == literal[50:55] == 'FXXXF'
    native = inspect(literal.replace('-', '?'), key, list(range(len(literal))))
    assert native['raw'] == previous['unaccepted_first_part']['expected_raw_native']
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    base, mapping = frame(literal, 45, 12)
    raw = inspect(base, key, mapping)
    assert raw['fixed_positions'] == 76
    primary = layer(data['primary_zero_substitution_template'], base, mapping, literal, key)
    optional = layer(data['optional_word_template'], base, mapping, literal, key)
    assert (primary['fixed_positions'], len(primary['known_coordinate_substitutions']),
            len(primary['printed_mask_fills']), len(primary['inserted_slot_fills'])) == (96, 0, 16, 4)
    assert (optional['fixed_positions'], len(optional['known_coordinate_substitutions']),
            len(optional['printed_mask_fills']), len(optional['inserted_slot_fills'])) == (99, 4, 19, 4)
    pscope = all_frames(literal, key, data['primary_zero_substitution_template'])
    oscope = all_frames(literal, key, data['optional_word_template'])
    assert len(pscope['all_minimum_maps']) == 16 and pscope['minimum_observed_substitutions'] == 0
    assert len(oscope['all_minimum_maps']) == 20 and oscope['minimum_observed_substitutions'] == 4
    assert pscope['distinct_edited_streams_at_minimum'] == oscope['distinct_edited_streams_at_minimum'] == 2
    # The central sentence uses no observed substitution in either layer.
    assert primary['raw'][20:42] == optional['raw'][20:42] == '8WEITEREZUEGEABGEROLLT'
    assert primary['raw'][64:80] == 'RDANFANGOROSHAZA'
    assert raw['positions'][52]['domain'] == '1GJKWX' and 'E' not in raw['positions'][52]['domain']
    assert primary['raw'][52] == '?' and optional['raw'][52] == 'E'
    for index in [20, 43, 44, 45, 62, 82, 101]:
        assert primary['raw'][index] == optional['raw'][index] == raw['raw'][index]
    context = data['attested_context']
    context_record = next(r for r in load(ROOT / context['path'])['records']
                          if r['id'] == context['record_id'])
    context_source = ''.join(''.join(context_record['source_rows']).split())
    assert len(context_source) == context_record['advertised_length'] == 240
    context_raw = inspect(context_source, key, list(range(len(context_source))))
    start = context_raw['raw'].index(context['term'])
    context_witness = {'record_id': context_record['id'], 'term': context['term'],
                       'plaintext_start': start, 'plaintext_end': start + len(context['term']),
                       'positions': context_raw['positions'][start:start + len(context['term'])],
                       'limit': context['limit']}
    assert all(len(p['domain']) == 1 for p in context_witness['positions'])
    case_path = ROOT / data['case']
    text = case_path.read_text()
    assert text.count(expected_legend(case_path)) == 1
    fences, quotes = displays(text)
    assert [r['role_from_caption'] for r in fences] == ['raw_output', 'edited_output', 'edited_output', 'source_transcription']
    assert [r['role_from_caption'] for r in quotes] == ['readable_german', 'readable_german']
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    assert bodies[:3] == [raw['raw'], primary['raw'], optional['raw']]
    assert ''.join(bodies[3].split()) == literal
    visible = re.findall(r'^> (.*)$', text, re.M)
    assert len(visible) == 2 and folded(visible[0]) == folded(primary['raw'])
    assert folded(visible[1]) == folded(optional['raw'])
    summary = {'physical_records': 1, 'printed_source_slots': 204, 'valid_source_coordinates': 183,
               'printed_mask_slots': 21, 'excluded_observed_coordinates': 5, 'added_unknown_slots': 5,
               'modeled_coordinates': 204, 'plaintext_positions': 102, 'raw_fixed_positions': 76,
               'zero_substitution_lexical_fixed_positions': 96, 'zero_substitution_lexical_printed_mask_fills': 16,
               'zero_substitution_lexical_added_slot_fills': 4, 'optional_fixed_positions': 99,
               'optional_observed_substitutions': 4, 'optional_printed_mask_fills': 19, 'optional_added_slot_fills': 4}
    return {'schema': 'adfgvx-late-remaining-source-certificate-v1', 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': data['indexing'], 'summary': summary,
            'records': [{'id': 'p217_B1', 'literal_source': literal, 'source_slots': 204,
                         'ciphertext': base, 'model_to_source_indices': mapping,
                         'excluded_source_indices': list(range(45, 50)), **raw,
                         'native_baseline': native, 'primary_lexical_completion': primary,
                         'optional_word_candidate': optional}],
            'primary_geometry_enumeration': pscope, 'optional_geometry_enumeration': oscope,
            'independent_place_spelling_witness': context_witness,
            'prior_credit': data['prior_credit'], 'limits': data['limits']}, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    certificate, evidence = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert certificate == load(path)
    else:
        path.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
