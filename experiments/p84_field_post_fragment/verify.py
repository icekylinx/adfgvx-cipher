#!/usr/bin/env python3
"""Verify p84 C's five source frames and conditional German field-post fragment.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
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
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    for path, digest in data['dependencies'].items():
        assert sha(ROOT / path) == digest, path
    key = data['key']
    assert key == next(k for k in load(ROOT/'data/keys.json')['keys'] if k['id'] == 'Oct28-31')
    record = data['records'][0]
    audit = next(r for r in load(ROOT/'data/reviews/source_gap_audit_20261103.json')['records'] if r['id'] == 'p84_C')
    assert record['source_rows'] == audit['source_rows']
    assert record['header_transcription'] == audit['header_transcription']
    source = ''.join(''.join(record['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == audit['literal_sha256'] == record['literal_sha256']
    assert len(source) == 118 and sum(c in C for c in source) == 111 and source.count('-') == 7
    assert source[75:79] == 'FDFG' and source[-9:] == 'FA-------'
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    frames = []
    expected_raw = record['expected_raw']
    expected_word = record['word_proposal']
    rebuilt = list(expected_raw)
    for fragment in record['word_fragments']:
        start, word = fragment['start'], fragment['word']
        rebuilt[start:start+len(word)] = word
    assert ''.join(rebuilt) == expected_word
    for at in record['frame']['possible_insert_before_source_indices']:
        assert 75 <= at <= 79
        origins = list(range(at)) + [None] + list(range(at,118)) + [None]*125
        assert len(origins) == 244
        assert [i for i in origins if i is not None] == list(range(118))
        wire = ''.join('?' if i is None or source[i] not in C else source[i] for i in origins)
        raw = arithmetic.analyze(wire,key,origins)
        assert raw['raw'] == expected_raw and raw['fixed_positions'] == 14
        layer = arithmetic.edited_layer(expected_word,wire,source,origins,key)
        prices = dict(fixed_positions=layer['fixed_positions'],
                      observed_substitutions=len(layer['observed_coordinate_substitutions']),
                      printed_mask_fills=len(layer['printed_mask_fills']),
                      inserted_slot_fills=len(layer['inserted_slot_fills']))
        assert prices == record['expected_word_prices']
        assert layer['raw'] == expected_word
        gained = [i for i,(a,b) in enumerate(zip(expected_raw,expected_word)) if a == '?' and b != '?']
        wholly = [i for i in gained if all(c == '?' for c in raw['positions'][i]['pair'])]
        half = [i for i in gained if sum(c in C for c in raw['positions'][i]['pair']) == 1]
        assert len(gained) == 14 and len(half) == 11 and wholly == [53,55,62]
        assert [{'position':i,'letter':expected_word[i]} for i in wholly] == record['wholly_unobserved_word_positions']
        assert len(layer['inserted_slot_fills']) == 15
        assert all(x['model_index'] >= 119 for x in layer['inserted_slot_fills'])
        frames.append(dict(id=f'short_group_{at}',insert_before_source=at,
                           ciphertext=wire,model_to_source_indices=origins,**raw,
                           full_roundtrip_witness=arithmetic.witness(wire,key),
                           readable_candidate=layer,new_word_positions_with_one_observed_half=half,
                           wholly_unobserved_word_positions=record['wholly_unobserved_word_positions']))
    # Phrase-conditioned native comparator preserves every source slot but omits
    # the short-group loss. Its four substitutions are not adopted corrections.
    native = source.replace('-','?')+'?'*126
    native_origins = list(range(118))+[None]*126
    native_raw = arithmetic.analyze(native,key,native_origins)['raw']
    template = native_raw[:47]+'DEUTSCHEFELDPOST'+native_raw[63:]
    comparator = arithmetic.edited_layer(template,native,source,native_origins,key)
    assert len(comparator['observed_coordinate_substitutions']) == 4
    assert len(comparator['printed_mask_fills']) == 2 and len(comparator['inserted_slot_fills']) == 15
    # The raw vocabulary donor is recorded literally; it is not a retransmission.
    donor = next(r for r in load(ROOT/'experiments/corpus_recovery/inputs.json')['records'] if r['id'] == 'p210_C')
    assert donor['expected_raw'][66:83] == 'XDEUTSCLEFELDPOST'
    text = (ROOT/data['case']).read_text()
    assert text.count(expected_legend(ROOT/data['case'])) == 1
    fences,quotes = displays(text)
    assert all(x['role_from_caption'] is not None for x in fences+quotes)
    bodies = re.findall(r'```text\n(.*?)\n```',text,re.S)
    assert all(x in bodies for x in ['\n'.join(record['source_rows']),expected_raw,expected_word])
    summary = dict(physical_sources=1,literal_source_slots=118,observed_source_coordinates=111,
                   printed_masks=7,retained_observed_coordinates=111,frame_slots=244,
                   plaintext_positions=122,inserted_unknown_slots=126,excluded_source_slots=0,
                   distinct_source_frames=5,primary_fixed_raw_positions=14,
                   primary_edited_fixed_positions=28,primary_edited_observed_substitutions=0,
                   primary_printed_mask_fills=2,primary_inserted_slot_fills=15,
                   new_word_positions_with_one_observed_half=11,
                   wholly_unobserved_word_completions=record['wholly_unobserved_word_positions'])
    return dict(schema='adfgvx-p84-field-post-certificate-v1',authors=data['authors'],
                input_sha256=sha(HERE/'inputs.json'),indexing='Zero based; ranges half open.',
                summary=summary,records=[dict(frames[1],id='p84_C')],
                alternative_frames=[row for row in frames if row['insert_before_source'] != 76],
                native_frame_phrase_comparison=dict(observed_substitutions=4,
                    printed_mask_fills=2,inserted_slot_fills=15,
                    observed_coordinate_substitutions=comparator['observed_coordinate_substitutions'],
                    scope='Word-conditioned native244 prefix comparator; no unrestricted historical optimum claim.')), evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args()
    result,evidence = build(args.pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert load(path) == result, 'Certificate differs; inspect before regeneration'
    else:
        path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(verified=True,**result['summary'],source_evidence=evidence),indent=2))


if __name__ == '__main__':
    main()
