#!/usr/bin/env python3
"""Price three independently attested vessel-name spellings in p213 A2."""
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
from experiments.late_november_joint_completion.verify import CO, positions


def read(path):
    return json.loads((ROOT / path).read_text())


def changes(source, candidate):
    return [{'source_index': i, 'from': a, 'to': b}
            for i, (a, b) in enumerate(zip(source, candidate)) if a in CO and a != b]


def build():
    data = json.loads((HERE / 'inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    for witness in data['historical_sources']:
        crop = witness['crop']
        assert hashlib.sha256((HERE / crop['path']).read_bytes()).hexdigest() == crop['sha256']
    r = next(r for r in read('experiments/reval_steamer_notice/certificates.json')['records'] if r['id'] == data['record'])
    k = next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov22-24')
    base, ranks = k['square'], k['column_rank_order']
    square = read('experiments/p215_hungarian_y/certificates.json')['conditional_squares'][data['shared_layer']]
    source, earlier = r['literal_source'], r['readable_candidate']['ciphertext']
    baseline, _ = positions(earlier, ranks, base)
    shared, ps = positions(earlier, ranks, square)
    current = list(earlier)
    proposals = []
    for spec in data['proposals']:
        start, target = spec['start'], spec['proposed']
        end = start + len(target)
        assert baseline[start:end] == spec['baseline']
        assert shared[start:end] == spec['shared']
        assert any(s['candidate'] == spec['source_candidate'] for s in data['historical_sources'])
        candidate = list(earlier)
        supports = []
        for p, symbol in enumerate(target, start):
            cell = square.index(symbol)
            pair = CO[cell // 6] + CO[cell % 6]
            for i, coordinate in zip(ps[p]['source_indices'], pair):
                candidate[i] = coordinate
                current[i] = coordinate
            if shared[p] != symbol:
                supports.append({'plaintext_index': p, 'before': shared[p], 'after': symbol,
                                 'old_pair': ps[p]['pair'], 'new_pair': pair,
                                 'source_indices': ps[p]['source_indices']})
        candidate = ''.join(candidate)
        new_changes = changes(earlier, candidate)
        assert new_changes == spec['additional_changes'] and len(new_changes) == 2
        text = decrypt(candidate, ranks, square)
        assert text[start:end] == target
        assert '?' not in text and encrypt(text, ranks, square) == candidate
        proposals.append({'baseline_field': spec['baseline'], 'shared_field': spec['shared'],
                          'proposed_field': target, 'source_witness': spec['source_candidate'],
                          'additional_observed_substitutions': new_changes,
                          'changed_plaintext_positions': supports,
                          'individual_candidate_ciphertext': candidate,
                          'individual_candidate_plaintext': text})
    current = ''.join(current)
    text = decrypt(current, ranks, square)
    assert text == data['expected'] and len(text) == 104
    assert encrypt(text, ranks, square) == current
    assert len(changes(earlier, current)) == 6
    total_changes = changes(source, current)
    fills = [{'source_index': i, 'literal': a, 'to': b}
             for i, (a, b) in enumerate(zip(source, current)) if a not in CO and b in CO]
    assert len(total_changes) == 9 and fills == [{'source_index': 181, 'literal': 'C', 'to': 'G'}]
    baseline_candidate = encrypt(text, ranks, base)
    assert len(changes(source, baseline_candidate)) == 13
    for p, pair in ((88, 'GD'), (99, 'DD')):
        assert ps[p]['pair'] == pair
        assert all(source[i] == current[i] for i in ps[p]['source_indices'])
    labels = re.sub('[^A-Z0-9?]', '', data['german'].upper())
    assert labels == text.replace('X', '')
    assert '> ' + data['german'] in (ROOT / data['case']).read_text()
    return {
        'schema': 'adfgvx-reval-ship-name-comparison-v1', 'authors': data['authors'],
        'input_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
        'indexing': 'Zero-based plaintext and source positions.',
        'id': data['record'], 'literal_source': source, 'earlier_word_ciphertext': earlier,
        'baseline_word_edition': baseline, 'shared_word_edition': shared,
        'conditional_square': square, 'name_proposals': proposals,
        'combined_ciphertext': current, 'combined_plaintext': text,
        'positions': len(text), 'observed_substitutions': total_changes,
        'source_mask_fills': fills, 'additional_observed_substitutions': 6,
        'additional_source_mask_fills': 0,
        'same_wording_under_published_square_observed_cost': 13,
        'same_wording_under_shared_square_observed_cost': 9,
        'new_unknown_positions_resolved': 0, 'german': data['german'],
        'historical_source_spellings': [s['candidate'] for s in data['historical_sources']],
        'limits': data['limits'],
    }


def check_sources(directory):
    from PIL import Image
    import fitz
    data = json.loads((HERE / 'inputs.json').read_text())
    for source in data['historical_sources']:
        crop = source['crop']
        if 'source_image' in source:
            record = source['source_image']
            path = directory / record['filename']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
            original = Image.open(path).convert('RGB')
            assert original.size == (record['width'], record['height'])
            assert hashlib.sha256(original.tobytes()).hexdigest() == record['rgb_sha256']
            result = original.crop(crop['crop_rectangle_pixels'])
            pixels, size = result.tobytes(), result.size
        else:
            record = source['source_pdf']
            path = directory / record['filename']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
            doc = fitz.open(path)
            pix = doc[crop['pdf_page_index_zero_based']].get_pixmap(
                matrix=fitz.Matrix(*crop['render_matrix']),
                clip=fitz.Rect(crop['crop_rectangle_pdf_points']), alpha=False)
            pixels, size = pix.samples, (pix.width, pix.height)
        assert size == (crop['width'], crop['height'])
        assert hashlib.sha256(pixels).hexdigest() == crop['rgb_sha256']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    result = build()
    if args.source_dir:
        check_sources(args.source_dir)
    path = HERE / 'certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print('p213 ship-name proposals: 3 primary spellings, +6 observed substitutions; 9total+1fill under priorJ/Y; no new unknown-position gain.')


if __name__ == '__main__':
    main()
