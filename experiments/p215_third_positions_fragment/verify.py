#!/usr/bin/env python3
"""Verify conditional p215 B3 source geometry, words and the inherited global J/Y layer.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'
ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
HELPER = ROOT / 'experiments/p215_breslau_dispatch/verify.py'
spec = importlib.util.spec_from_file_location('dispatch_arithmetic', HELPER)
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_map(source, frame):
    insert = {int(k): v for k, v in frame['insert_unknown_before_source_indices'].items()}
    assert insert == {79: 5, 155: 10}
    origins = []
    for i in range(len(source)):
        origins.extend([None] * insert.get(i, 0))
        origins.append(i)
    block_range = frame['move_printed_mask_source_range']
    if block_range is not None:
        start, end = block_range
        assert (start, end) == (79, 87) and source[start:end] == '-' * 8
        block = list(range(start, end))
        at = origins.index(start)
        assert origins[at:at + 8] == block
        del origins[at:at + 8]
        destination = frame['insert_mask_block_at_shortened_frame_boundary']
        assert destination in (85, 86) and len(origins) == 226
        origins[destination:destination] = block
    assert len(origins) == 234 and origins.count(None) == 15
    assert sorted(i for i in origins if i is not None) == list(range(219))
    assert [i for i in origins if i is not None and source[i] in C] == [i for i, c in enumerate(source) if c in C]
    return origins


def prices(layer):
    return dict(fixed_positions=layer['fixed_positions'],
                observed_substitutions=len(layer['observed_coordinate_substitutions']),
                printed_mask_fills=len(layer['printed_mask_fills']),
                inserted_slot_fills=len(layer['inserted_slot_fills']))


def shared_square(key):
    inherited = load(ROOT / 'experiments/p215_hungarian_y/inputs.json')
    assert inherited['key']['square'] == key['square']
    clear = inherited['ambiguous_baseline_labels']
    assignments = dict(inherited['prior_numeric_assignments'])
    for field in ['prior_lexical_J', 'new_lexical_Y']:
        item = inherited[field]
        assignments[item['baseline_label']] = item['letter']
    assert clear == '0123456789JQY'
    assert assignments == {'Y': '1', 'J': '2', '2': '6', '9': 'J', '4': 'Y'}
    partial = ''.join(assignments.get(c, '?' if c in clear else c) for c in key['square'])
    assigned = partial.replace('?', '')
    assert len(set(assigned)) == len(assigned) == 28
    unused = ''.join(sorted(set(ALPHABET) - set(assigned)))
    remaining = iter(unused)
    complete = ''.join(next(remaining) if c == '?' else c for c in partial)
    assert len(set(complete)) == 36
    return dict(clear_baseline_labels=clear, assignments=assignments, partial_square=partial,
                unused_symbols=unused, compatible_full_squares=math.factorial(len(unused)),
                complete_square_witness=complete,
                qualification='Inherited optional global assumptions; unassigned cells are jointly injective. The canonical completion is an arithmetic witness, not a recovered key.')


def joint_layer(layer, key, shared):
    partial = shared['partial_square']
    unused = shared['unused_symbols']
    _, inverse = arithmetic.order(len(layer['ciphertext']), key['column_rank_order'])
    domains = []
    for p in range(len(layer['raw'])):
        a, b = (layer['ciphertext'][i] for i in inverse[2*p:2*p+2])
        cells = [6*C.index(x)+C.index(y) for x in (C if a == '?' else a) for y in (C if b == '?' else b)]
        domains.append(''.join(sorted({v for cell in cells for v in (unused if partial[cell] == '?' else partial[cell])})))
    output = ''.join(d if len(d) == 1 else '?' for d in domains)
    square = shared['complete_square_witness']
    full = layer['ciphertext'].replace('?', 'A')
    text = decrypt(full, key['column_rank_order'], square)
    assert encrypt(text, key['column_rank_order'], square) == full
    assert all(c in domain for c, domain in zip(text, domains))
    assert output[7:40] == 'RAUMGYULAXSIKLOXKISJENOEXERREICHT'
    assert output[73:105] == 'STRECKERUTTKAXTESCHENXABGEFAHREN'
    return dict(output=output, domains=domains, additional_observed_substitutions=0,
                full_global_witness=dict(square=square, ciphertext=full, plaintext=text,
                                         historical_fill_claim=False))


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    for path, digest in data['dependencies'].items():
        assert sha(ROOT / path) == digest, path
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov22-24')
    record = data['records'][0]
    audit = next(r for r in load(ROOT / 'data/reviews/source_gap_audit_20261103.json')['records'] if r['id'] == record['id'])
    assert record['source_rows'] == audit['source_rows']
    assert record['header_transcription'] == audit['header_transcription']
    source = ''.join(''.join(record['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == audit['literal_sha256']
    assert len(source) == 219 and sum(c in C for c in source) == 200
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    shared = shared_square(key)
    editions = []
    for model in record['models']:
        origins = source_map(source, model['frame'])
        cipher = ''.join(source[i] if i is not None and source[i] in C else '?' for i in origins)
        raw = arithmetic.analyze(cipher, key, origins)
        assert raw['raw'] == model['expected_raw'] and raw['fixed_positions'] == 88
        words = arithmetic.edited_layer(model['word_proposal'], cipher, source, origins, key)
        assert prices(words) == model['expected_word_prices']
        optional = arithmetic.edited_layer(model['optional_place_proposal'], cipher, source, origins, key)
        assert prices(optional) == model['expected_optional_prices']
        gain = [i for i, (a, b) in enumerate(zip(raw['raw'], words['raw'])) if a == '?' and b != '?']
        wholly_absent = [i for i in gain if raw['positions'][i]['pair'] == '??']
        assert wholly_absent == [82, 93, 104]
        optional_gain = [i for i, (a, b) in enumerate(zip(words['raw'], optional['raw'])) if a == '?' and b != '?']
        assert optional_gain == [54, 56]
        assert all(sum(c in C for c in raw['positions'][i]['pair']) == 1 for i in optional_gain)
        row = dict(id=model['id'], frame=model['frame'], ciphertext=cipher,
                   model_to_source_indices=origins, **raw,
                   full_roundtrip_witness=arithmetic.witness(cipher, key), readable_candidate=words,
                   word_gain_positions=gain, wholly_unobserved_word_completions=wholly_absent,
                   optional_alsosimand=optional, shared_jy_word_interpretation=joint_layer(words, key, shared),
                   shared_jy_optional_interpretation=joint_layer(optional, key, shared))
        if model['id'] == 'printed8_relocation':
            alternate = dict(model['frame'], insert_mask_block_at_shortened_frame_boundary=86)
            aliases = source_map(source, alternate)
            other = ''.join(source[i] if i is not None and source[i] in C else '?' for i in aliases)
            assert other == cipher
            row['equivalent_mask_destinations'] = [85, 86]
            row['alternative_mask_ownership_sha256'] = hashlib.sha256(json.dumps(aliases, separators=(',', ':')).encode()).hexdigest()
        editions.append(row)
    primary = next(e for e in editions if e['id'] == record['primary_model_id'])
    primary_record = dict(primary, id=record['id'], model_id=primary['id'], literal_source=source)
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(x['role_from_caption'] is not None for x in fences + quotes)
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    for required in ['\n'.join(record['source_rows']), primary['raw'], primary['readable_candidate']['raw'],
                     primary['shared_jy_word_interpretation']['output'], primary['optional_alsosimand']['raw']]:
        assert required in bodies
    summary = dict(physical_sources=1, literal_source_slots=219, observed_source_coordinates=200,
                   printed_masks=19, frame_slots=234, plaintext_positions=117, inserted_unknown_slots=15,
                   relocated_printed_mask_slots=8, excluded_source_slots=0, excluded_observed_coordinates=0,
                   raw_source_substitutions=0, observed_coordinate_order_preserved=True,
                   primary_fixed_raw_positions=88, primary_edited_fixed_positions=109,
                   primary_edited_observed_substitutions=2, primary_printed_mask_fills=14,
                   primary_inserted_slot_fills=10, wholly_unobserved_word_completions=[82,93,104])
    return dict(schema='adfgvx-p215-third-positions-certificate-v1', authors=data['authors'],
                input_sha256=sha(HERE / 'inputs.json'), indexing='Zero based; ranges half open.',
                summary=summary, shared_jy_square=shared, records=[primary_record],
                alternative_models=[row for row in editions if row['id'] != primary['id']]), evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result, evidence = build(args.pdf)
    target = HERE / 'certificates.json'
    if args.verify:
        assert load(target) == result, 'Certificate differs; inspect before regeneration'
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(verified=True, **result['summary'], source_evidence=evidence), indent=2))


if __name__ == '__main__':
    main()
