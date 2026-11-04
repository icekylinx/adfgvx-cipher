#!/usr/bin/env python3
"""Recompute the conditional p154 A2 source frame and two costed word fragments.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
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
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_map(source, frame):
    assert len(source) == 118 and all(c in C for c in source)
    assert source[25:31] == 'VDFDVD' and source[28] == 'D'
    assert frame['excluded_observed_source_indices'] == [28]
    assert frame['inserted_unknown_prefix'] == 45
    origins = [None] * 45 + [i for i in range(118) if i != 28]
    assert len(origins) == 162
    assert [i for i in origins if i is not None] == [i for i in range(118) if i != 28]
    return origins


def word_cost_comparison(source, rows, fragments, key):
    template = ['?'] * 81
    for fragment in fragments:
        start, word = fragment['start'], fragment['word']
        template[start:start + len(word)] = word
    desired = arithmetic.edited_layer(''.join(template), '?'*162, source,
                                      [None]*162, key)['ciphertext']
    def cost(wire):
        edits = sum(a in C and b in C and a != b for a, b in zip(wire, desired))
        fills = sum(a == '?' and b in C for a, b in zip(wire, desired))
        return edits, fills
    single = []
    for a in range(119):
        e, f = cost(source[:a] + '?'*44 + source[a:])
        single.append(dict(boundary=a, observed_substitutions=e, inserted_fills=f))
    best_single = min(r['observed_substitutions'] for r in single)
    boundaries = [0]
    for row in rows:
        for group in row.split():
            boundaries.append(boundaries[-1] + len(group))
    count = 0
    best = 999
    winners = []
    for a, b in itertools.combinations(boundaries, 2):
        for first in range(1, 44):
            wire = source[:a]+'?'*first+source[a:b]+'?'*(44-first)+source[b:]
            edits, fills = cost(wire)
            count += 1
            if edits < best:
                best = edits
                winners = []
            if edits == best:
                winners.append(dict(boundaries=[a,b], added_counts=[first,44-first],
                                    observed_substitutions=edits, inserted_fills=fills))
    assert count == 12900 and best == 7 and best_single == 10
    return dict(scope='Same two proposed phrases at their stated positions; no source exclusion. This is a word-conditioned comparison, not blind recovery.',
                single_44_gap_models=119, minimum_single_gap_substitutions=best_single,
                group_boundary_two_gap_models=count, minimum_two_gap_substitutions=best,
                two_gap_minimizers=winners)


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    for path, digest in data['dependencies'].items():
        assert sha(ROOT / path) == digest, path
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov4-6')
    record = data['records'][0]
    audit = next(r for r in load(ROOT / 'data/reviews/source_gap_audit_20261103.json')['records'] if r['id'] == record['id'])
    assert record['source_rows'] == audit['source_rows']
    assert record['header_transcription'] == audit['header_transcription']
    source = ''.join(''.join(record['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == audit['literal_sha256']
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    origins = source_map(source, record['frame'])
    cipher = ''.join('?' if i is None else source[i] for i in origins)
    raw = arithmetic.analyze(cipher, key, origins)
    assert raw['raw'] == record['expected_raw'] and raw['fixed_positions'] == 36
    layer = arithmetic.edited_layer(record['word_proposal'], cipher, source, origins, key)
    actual = dict(fixed_positions=layer['fixed_positions'],
                  observed_substitutions=len(layer['observed_coordinate_substitutions']),
                  printed_mask_fills=len(layer['printed_mask_fills']),
                  inserted_slot_fills=len(layer['inserted_slot_fills']))
    assert actual == record['expected_word_prices']
    assert [(x['source_index'],x['before'],x['after']) for x in layer['observed_coordinate_substitutions']] == [(94,'F','V'),(106,'A','G')]
    gained = [i for i,(a,b) in enumerate(zip(raw['raw'],layer['raw'])) if a == '?' and b != '?']
    assert len(gained) == 20
    assert all(sum(c in C for c in raw['positions'][i]['pair']) == 1 for i in gained)
    # The full proposal must change only the two declared word spans.
    rebuilt = list(raw['raw'])
    for fragment in record['word_fragments']:
        start, word = fragment['start'], fragment['word']
        rebuilt[start:start+len(word)] = word
    assert ''.join(rebuilt) == layer['raw']
    comparison = word_cost_comparison(source, record['source_rows'], record['word_fragments'], key)
    row = dict(id=record['id'], literal_source=source, frame=record['frame'], ciphertext=cipher,
               model_to_source_indices=origins, **raw,
               excluded_source_coordinates=[dict(source_index=28,glyph='D',reason='Explicitly priced surplus-glyph hypothesis in six-character VDFDVD.')],
               full_roundtrip_witness=arithmetic.witness(cipher,key), readable_candidate=layer,
               new_word_positions_with_one_observed_half=gained)
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(x['role_from_caption'] is not None for x in fences+quotes)
    bodies = re.findall(r'```text\n(.*?)\n```',text,re.S)
    for wanted in ['\n'.join(record['source_rows']),raw['raw'],layer['raw']]:
        assert wanted in bodies
    summary = dict(physical_sources=1,literal_source_slots=118,observed_source_coordinates=118,
                   retained_observed_coordinates=117,printed_masks=0,frame_slots=162,
                   plaintext_positions=81,inserted_unknown_slots=45,excluded_source_slots=1,
                   excluded_observed_coordinates=1,raw_source_substitutions=0,
                   retained_observed_coordinate_order_preserved=True,primary_fixed_raw_positions=36,
                   primary_edited_fixed_positions=56,primary_edited_observed_substitutions=2,
                   primary_printed_mask_fills=0,primary_inserted_slot_fills=20,
                   wholly_unobserved_word_completions=[])
    return dict(schema='adfgvx-p154-weisskirchen-certificate-v1',authors=data['authors'],
                input_sha256=sha(HERE/'inputs.json'),indexing='Zero based; ranges half open.',
                summary=summary,records=[row],word_conditioned_source_preserving_comparison=comparison), evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args()
    result,evidence = build(args.pdf)
    target = HERE/'certificates.json'
    if args.verify:
        assert load(target) == result, 'Certificate differs; inspect before regeneration'
    else:
        target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(verified=True,**result['summary'],source_evidence=evidence),indent=2))


if __name__ == '__main__':
    main()
