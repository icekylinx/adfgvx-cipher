#!/usr/bin/env python3
"""Verify the native p151 E2 map-sheet fragment and its four word repairs.

icekylinx and GPT-6 Astra Pro. No source coordinate is inserted or excluded;
the two unknown key cells remain globally injective and unassigned.
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
from adfgvx.cipher import decrypt, encrypt, untranspose
from experiments.romanian_pacification_consultation.verify import inspect, repair
from data.reviews.check_reading_presentation import displays, expected_legend


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def fold(text):
    return re.sub(r'[^A-Z0-9?]', '', text.upper())


def build(pdf=None):
    inp = load(HERE / 'inputs.json')
    for path, digest in inp['core_sha256'].items():
        assert sha(ROOT / path) == digest
    key = inp['key']
    published = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    assert key == published
    record = inp['record']
    literal = ''.join(''.join(record['source_rows']).split())
    base = literal.replace('-', '?')
    mapping = list(range(len(base)))
    assert len(base) == record['advertised_length'] == 224
    assert len([c for c in base if c in 'ADFGVX']) == 222
    assert [i for i, c in enumerate(literal) if c == '-'] == [103, 104]
    assert set(literal) <= set('ADFGVX-')
    raw = inspect(base, key, mapping)
    assert raw['raw'] == record['expected_raw']
    assert raw['fixed_positions'] == 108
    candidate = repair(record['edited_output'], base, key, mapping, literal)
    assert candidate['raw'] == record['edited_output'] and candidate['fixed_positions'] == 110
    assert [[r['source_index'], r['from'], r['to']] for r in candidate['known_coordinate_substitutions']] == record['expected_substitutions']
    assert [[r['source_index'], r['to']] for r in candidate['erased_coordinate_fills']] == record['expected_mask_fills']
    changed = []
    for before, after in zip(raw['positions'], candidate['positions']):
        if before['raw'] != after['raw']:
            changed.append({'plaintext_index': before['plaintext_index'], 'raw': before, 'edited': after})
    assert [row['plaintext_index'] for row in changed] == [12, 28, 38, 93]
    unresolved = [p for p in candidate['positions'] if p['raw'] == '?']
    assert [(p['plaintext_index'], p['pair'], p['domain']) for p in unresolved] == [(109, 'VF', '56'), (110, 'XA', '56')]
    assert all(token in raw['raw'] and token in candidate['raw'] for token in record['protected_fields'])
    missing = [i for i, ch in enumerate(key['square']) if ch == '?']
    unused = sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(key['square']))
    assert len(missing) == 2 and unused == ['5', '6']
    global_witnesses = []
    for labels in itertools.permutations(unused):
        square = list(key['square'])
        assignments = []
        for cell, label in zip(missing, labels):
            square[cell] = label
            assignments.append({'cell_index': cell,
                                'coordinate_pair': 'ADFGVX'[cell // 6] + 'ADFGVX'[cell % 6],
                                'label': label})
        square = ''.join(square)
        assert len(set(square)) == 36
        cipher = candidate['ciphertext']
        text = decrypt(cipher, key['column_rank_order'], square)
        assert encrypt(text, key['column_rank_order'], square) == cipher
        assert all(a == '?' or a == b for a, b in zip(candidate['raw'], text))
        global_witnesses.append({'square': square, 'assignments': assignments,
                                 'ciphertext': cipher, 'plaintext': text,
                                 'literal_footer': text[-8:],
                                 'ordinary_roundtrip': True, 'historical_assignment_claim': False})
    assert {w['plaintext'][105:111] for w in global_witnesses} == {'1D7056', '1D7065'}
    prior = inp['prior_ocr']
    assert sha(HERE / prior['path']) == prior['sha256']
    old = load(HERE / prior['path'])
    live_old = next(r for r in load(ROOT / prior['source_path'])['blocks'] if r['id'] == old['id'])
    assert old == live_old
    source_groups = ' '.join(record['source_rows']).split()
    assert len(old['groups']) == len(source_groups) == 45
    group_differences = [{'group_1based': i + 1, 'earlier_OCR': a, 'reviewed_source': b}
                         for i, (a, b) in enumerate(zip(old['groups'], source_groups))
                         if a.replace('?', '-') != b]
    assert group_differences == [{'group_1based': 16, 'earlier_OCR': 'GGVVXX', 'reviewed_source': 'GGVVX'}]
    old_cipher = ''.join(old['groups'])
    assert len(old_cipher) == prior['expected_slots'] == 225
    old_raw = decrypt(old_cipher, key['column_rank_order'], key['square'], allow_unpaired=True)
    assert old_raw == prior['expected_odd_raw_paired_prefix']
    old_interim = untranspose(old_cipher, key['column_rank_order'])
    case = ROOT / inp['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(row['role_from_caption'] for row in fences + quotes)
    assert re.findall(r'```text\n(.*?)\n```', text, flags=re.S) == [record['expected_raw'], record['edited_output']]
    quote = ''.join(line[2:] for line in text.splitlines() if line.startswith('> '))
    assert fold(quote) == fold(record['readable_german']) == record['edited_output']
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        assert pdf.stat().st_size == inp['source']['pdf_bytes']
        crop = inp['source']['reviewed_pixels']
        doc = fitz.open(pdf)
        fitz.TOOLS.store_shrink(100)
        pix = doc[crop['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(crop['render_scale'], crop['render_scale']),
            clip=fitz.Rect(*crop['crop_pdf_points']), alpha=False)
        assert (pix.width, pix.height, pix.n) == (crop['width'], crop['height'], crop['channels'])
        assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']
    summary = {'physical_records': 1, 'printed_source_slots': 224,
               'valid_source_coordinates': 222, 'model_coordinates': 224,
               'plaintext_positions': 112, 'raw_fixed_positions': 108,
               'baseline_fixed_positions': 108,
               'edited_fixed_positions': 110, 'remaining_unknown_positions': 2,
               'observed_coordinate_substitutions': 2, 'known_coordinate_substitutions': 2,
               'printed_mask_fills': 2,
               'source_exclusions': 0, 'inserted_coordinates': 0,
               'source_reordering': False, 'key_changed': False,
               'globally_injective_key_completion_witnesses': 2,
               'core_data_unchanged': True}
    return {'schema': 'adfgvx-nov9-operations-map-sheets-certificate-v1',
            'authors': inp['authors'], 'source_record': record['id'],
            'inputs_sha256': sha(HERE / 'inputs.json'),
            'summary': summary, 'source': inp['source'],
            'literal_source': literal, 'model_to_source_indices': mapping,
            'raw': raw, 'optional_edition': candidate, 'four_changed_labels': changed,
            'remaining_coupled_unknown_positions': unresolved,
            'all_global_key_completion_witnesses': global_witnesses,
            'earlier_ocr_comparison': {'literal_OCR': old_cipher, 'slots': len(old_cipher),
              'group_differences': group_differences, 'paired_raw_prefix': old_raw,
              'unpaired_interim_suffix': old_interim[-1:],
              'scope': 'OCR diagnostic only, not a source frame adopted by the edition.'},
            'prior_credit': inp['prior_credit'], 'limits': inp['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    dest = HERE / 'certificates.json'
    if args.verify:
        assert load(dest) == result, 'Recomputed certificate differs'
    else:
        dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify,
                      'source_pixel_check': 'passed' if args.pdf else 'skipped: provide --pdf to reproduce the reviewed pixels',
                      **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
