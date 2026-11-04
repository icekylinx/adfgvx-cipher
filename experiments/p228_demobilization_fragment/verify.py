#!/usr/bin/env python3
"""Verify the source-preserving p228 B2 mask relocation and priced word layer.

icekylinx and GPT-6 Astra Pro. Apache-2.0. Zero-based indices throughout.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'
HELPER = ROOT / 'experiments/p215_breslau_dispatch/verify.py'
spec = importlib.util.spec_from_file_location('dispatch_arithmetic', HELPER)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_map(source, start=195):
    assert 192 <= start <= 215 and source[start:start + 5] == '-----'
    owners = list(range(len(source)))
    block = owners[start:start + 5]
    del owners[start:start + 5]
    assert len(owners) == 259
    owners[246:246] = block
    assert sorted(owners) == list(range(264))
    assert [i for i in owners if source[i] in C] == [i for i, c in enumerate(source) if c in C]
    return owners


def prices(layer):
    return dict(fixed_positions=layer['fixed_positions'],
                observed_substitutions=len(layer['observed_coordinate_substitutions']),
                printed_mask_fills=len(layer['printed_mask_fills']),
                inserted_slot_fills=len(layer['inserted_slot_fills']))


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    for name, digest in data['dependencies'].items():
        assert sha(ROOT / name) == digest, name
    prior = load(ROOT / 'experiments/neuhof_demobilization/inputs.json')
    source_record = next(r for r in prior['records'] if r['id'] == 'p228_B2')
    record = data['records'][0]
    key = data['key']
    assert key == prior['key']
    registered = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    assert all(registered[k] == key[k] for k in key)
    assert record['source_rows'] == source_record['source_rows']
    assert record['header_transcription'] == prior['source']['header_literal']
    source = ''.join(''.join(record['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == record['literal_sha256']
    assert len(source) == 264 and sum(c in C for c in source) == 221
    assert record['frame'] == dict(move_source_mask_range=[195, 200], insert_at_shortened_boundary=246)
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    origins = source_map(source)
    cipher = ''.join(source[i] if source[i] in C else '?' for i in origins)
    raw = a.analyze(cipher, key, origins)
    assert raw['raw'] == record['expected_raw'] and raw['fixed_positions'] == 90
    template = list(raw['raw'])
    selected = []
    for span in record['word_spans']:
        start, text = span['start'], span['text']
        assert 0 <= start < start + len(text) <= 132
        for i, c in enumerate(text, start):
            assert i not in selected
            selected.append(i)
            template[i] = c
    assert len(selected) == 95
    words = a.edited_layer(''.join(template), cipher, source, origins, key)
    assert words['raw'] == record['expected_word']
    assert prices(words) == record['expected_word_prices']
    gained = [i for i, (x, y) in enumerate(zip(raw['raw'], words['raw'])) if x == '?' and y != '?']
    wholly = [i for i in gained if raw['positions'][i]['pair'] == '??']
    tail_gained = [i for i in gained if i >= 33]
    assert len(gained) == 31 and wholly == [4] and len(tail_gained) == 22
    assert all(sum(c in C for c in raw['positions'][i]['pair']) == 1 for i in tail_gained)
    assert words['raw'][116:121] == '???CK'
    aliases = []
    for start in range(192, 216):
        alias = source_map(source, start)
        wire = ''.join(source[i] if source[i] in C else '?' for i in alias)
        assert wire == cipher
        aliases.append(dict(moved_source_range=[start, start + 5],
                            mapping_sha256=hashlib.sha256(json.dumps(alias, separators=(',', ':')).encode()).hexdigest()))
    native_origins = list(range(264))
    native_cipher = source.replace('-', '?')
    native_raw = a.analyze(native_cipher, key, native_origins)
    assert native_raw['raw'] == source_record['expected_raw'] and native_raw['fixed_positions'] == 89
    opening = source_record['editorial_recipe']['text'][:33]
    previous = a.edited_layer(opening + native_raw['raw'][33:], native_cipher, source, native_origins, key)
    relocated_opening = a.edited_layer(opening + raw['raw'][33:], cipher, source, origins, key)
    assert prices(previous) == dict(fixed_positions=99, observed_substitutions=5, printed_mask_fills=10, inserted_slot_fills=0)
    assert prices(relocated_opening) == dict(fixed_positions=99, observed_substitutions=1, printed_mask_fills=10, inserted_slot_fills=0)
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(x['role_from_caption'] is not None for x in fences + quotes)
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    for required in ['\n'.join(record['source_rows']), raw['raw'], words['raw']]:
        assert required in bodies
    row = dict(id='p228_B2', literal_source=source, ciphertext=cipher,
               model_to_source_indices=origins, **raw, readable_candidate=words,
               word_span_positions=selected, new_word_positions=gained,
               new_tail_word_positions=tail_gained, wholly_unobserved_word_completions=wholly,
               equivalent_mask_ownerships=aliases, full_roundtrip_witness=a.witness(cipher, key))
    summary = dict(physical_sources=1, literal_source_slots=264, observed_source_coordinates=221,
                   printed_masks=43, frame_slots=264, plaintext_positions=132,
                   relocated_printed_mask_slots=5, inserted_slots=0, excluded_source_slots=0,
                   raw_observed_substitutions=0, observed_coordinate_order_preserved=True,
                   raw_fixed_positions=90, word_fixed_positions=121, proposed_word_positions=95,
                   word_observed_substitutions=5, word_printed_mask_fills=32,
                   wholly_unobserved_word_completions=[4], new_fixed_tail_word_positions=22,
                   unresolved_word_positions=[i for i, c in enumerate(words['raw']) if c == '?'])
    return dict(schema='adfgvx-p228-demobilization-fragment-certificate-v1', authors=data['authors'],
                input_sha256=sha(HERE / 'inputs.json'), indexing='Zero based; ranges half open.',
                summary=summary, records=[row],
                previous_native_edition=dict(raw=native_raw['raw'], fixed_positions=89,
                                             readable_candidate=previous, claimed_word_span=[0, 33]),
                opening_only_in_relocated_frame=relocated_opening), evidence


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
