#!/usr/bin/env python3
"""Replay the p117/p124 cross-key withdrawal-phrase witness.

icekylinx and GPT-6 Astra Pro. Existing source transcripts and keys are unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

C = 'ADFGVX'
INPUTS = {
    'target': 'experiments/hungarian_armistice_instructions/inputs.json',
    'donor': 'experiments/nov3_medical_radio_withdrawal/inputs.json',
}
# Pin the reviewed source packages, rather than copying their transcripts.
HASHES = {'target': 'f96b5d2f58c14fe55fe4d27722535b6663fbc497c64e4cb963b3f30daf68a10a', 'donor': 'f3a98d7b8bcd0c3931901b4c3d624c67c273750481b4e219f2c4dedfccce5b00'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(source, key):
    """Recover source indices by filling original matrix columns in read order."""
    ranks = key['column_rank_order']
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    inverse = [None] * len(source)
    consumed = 0
    for column in sorted(range(width), key=lambda j: ranks[j]):
        for interim in range(column, len(source), width):
            inverse[interim] = consumed
            consumed += 1
    assert consumed == len(source) and sorted(inverse) == list(range(len(source)))
    pairs = [''.join(source[j] for j in inverse[i:i+2])
             for i in range(0, len(source), 2)]
    text = ''.join(key['square'][C.index(p[0]) * 6 + C.index(p[1])] for p in pairs)
    assert text == decrypt(source, ranks, key['square'])
    assert encrypt(text, ranks, key['square']) == source
    return text, [{'plaintext_index': i, 'letter': letter, 'pair': pairs[i],
                   'source_indices': inverse[2*i:2*i+2]} for i, letter in enumerate(text)]


def verify_pixels(pdf, crops):
    import fitz
    from PIL import Image
    assert pdf.stat().st_size == 156848258
    assert sha(pdf) == '157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06'
    document = fitz.open(pdf)
    for path, crop in crops:
        clip = crop.get('crop_pdf_points', crop.get('clip_points'))
        scale = crop.get('render_scale', crop.get('scale'))
        pixels = document[crop['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*clip))
        im = Image.open(path).convert('RGB')
        assert im.size == (pixels.width, pixels.height)
        assert im.tobytes() == pixels.samples


def build(pdf=None):
    for role, rel in INPUTS.items():
        assert sha(ROOT / rel) == HASHES[role], (role, 'source package changed')
    target_package = json.loads((ROOT / INPUTS['target']).read_text())
    donor_package = json.loads((ROOT / INPUTS['donor']).read_text())
    target = next(r for r in target_package['records'] if r['id'] == 'p124_A1')
    donor = next(r for r in donor_package['records'] if r['id'] == 'p117_C3')
    keys = {r['id']: r for r in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    target_key = target_package['key']
    donor_key = next(k for k in donor_package['keys'] if k['id'] == donor['key_id'])
    assert target_key == keys['Nov4-6'] and donor_key == keys['Nov1-3']
    target_source = ''.join(target['source_rows']).replace(' ', '')
    donor_source = ''.join(donor['rows']).replace(' ', '')
    assert donor_source == donor['literal_source'] == donor['analysis_source']
    assert donor['excluded_source_indices'] == [] and donor['expected_source_changes'] == []
    assert len(target_source) == 352 and len(donor_source) == 160
    assert set(target_source + donor_source) <= set(C)
    target_raw, target_positions = decode(target_source, target_key)
    donor_raw, donor_positions = decode(donor_source, donor_key)
    assert target_raw == target['expected_raw'] and donor_raw == donor['expected_raw']
    assert donor_raw == donor['editorial_text']
    phrase = 'SOBALDALSMOEGLICHUNGARISCHENUNDSUEDSLAVISCHENBODENVERLASSEN'
    assert len(phrase) == 59 and donor_raw[21:80] == phrase
    assert target_raw[95:110] == donor_raw[:15] == 'DEUTSCHETRUPPEN'
    assert target_raw[110:116] == 'SOLLEN' and donor_raw[15:21] == 'WERDEN'
    aligned = [{'target': target_positions[116+i], 'donor': donor_positions[21+i],
                'agrees': target_raw[116+i] == donor_raw[21+i]} for i in range(59)]
    differences = [r for r in aligned if not r['agrees']]
    assert [r['target']['plaintext_index'] for r in differences] == [133, 158]
    # Transfer decoded letters across the different squares; do not copy a raw
    # coordinate value from one key period into another.
    proposal = list(target_raw)
    for row in differences:
        proposal[row['target']['plaintext_index']] = row['donor']['letter']
    proposal = ''.join(proposal)
    completed = encrypt(proposal, target_key['column_rank_order'], target_key['square'])
    repairs = [{'source_index': i, 'from': a, 'to': b}
               for i, (a, b) in enumerate(zip(target_source, completed)) if a != b]
    assert repairs == [{'source_index': 80, 'from': 'G', 'to': 'A'},
                       {'source_index': 306, 'from': 'X', 'to': 'V'}]
    assert proposal[116:175] == phrase
    assert proposal[63] == target_raw[63] == 'D'  # FDER remains outside this witness.
    assert proposal[23:29] == target_raw[23:29] and proposal.endswith('0')
    assert decrypt(completed, target_key['column_rank_order'], target_key['square']) == proposal
    old_proposal = target['readable_candidate']
    remaining = [(i, a, b) for i, (a, b) in enumerate(zip(proposal, old_proposal)) if a != b]
    assert remaining == [(63, 'D', 'U')]
    target_crop = next(c for c in target_package['source_images'] if c['path'].endswith('p124_A1.png'))
    donor_crop = next(c for c in donor_package['source']['images'] if c['path'].endswith('p117_C_detail.png'))
    crops = [(HERE / target_crop['path'], target_crop),
             (ROOT / Path(INPUTS['donor']).parent / donor_crop['path'], donor_crop)]
    crop_refs = []
    for path, crop in crops:
        assert sha(path) == crop['sha256']
        crop_refs.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path),
                          'pdf_page_1based': crop['pdf_page_1based']})
    if pdf:
        verify_pixels(pdf, crops)
    return {'schema': 'adfgvx-withdrawal-cross-key-phrase-v1',
            'authors': 'icekylinx and GPT-6 Astra Pro',
            'source_dependencies': {role: {'path': rel, 'sha256': HASHES[role]}
                                    for role, rel in INPUTS.items()},
            'source_crops': crop_refs,
            'donor': {'id': donor['id'], 'key_id': donor_key['id'], 'raw': donor_raw,
                      'header': donor['header_transcription'], 'source_edits': 0},
            'target': {'id': target['id'], 'key_id': target_key['id'], 'raw': target_raw,
                       'headers': target_package['headers'], 'joint_phrase_layer': proposal,
                       'joint_phrase_ciphertext': completed, 'repairs': repairs},
            'alignment': {'donor_start': 21, 'target_start': 116, 'length': 59,
                          'unchanged_matching_positions': 57, 'phrase': phrase,
                          'positions': aligned},
            'limits': ['The same withdrawal phrase is witnessed under two different period keys.',
                       'The messages have different headers and WERDEN/SOLLEN wording; no identical transmission is asserted.',
                       'The two p124 repairs were already proposed in its existing edition. This strengthens their evidence without adding fixed positions or physical messages.',
                       'The separate FDER-to-FUER proposal, KOOVES and final 0 are not established by this parallel.'],
            'checks': {'raw_roundtrips': 2, 'joint_phrase_roundtrip': True,
                       'keys_changed': False, 'new_fixed_positions': 0,
                       'new_physical_records': 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'withdrawal_parallel.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'parallel_letters': 59, 'existing_repairs_with_new_source_support': 2,
                      'new_fixed_positions': 0, 'original_pdf_pixels_checked': args.pdf is not None}))


if __name__ == '__main__':
    main()
