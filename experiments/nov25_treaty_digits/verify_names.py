#!/usr/bin/env python3
"""Check the shared Y in Strzemieczny and Nagymagocs against received pairs.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    return json.loads((ROOT / path).read_text())


def source_records(data, base, manifest, treaty):
    earlier = {r['id']: r for r in treaty['records']}
    records = base.normalized_records(manifest)
    for rec in records:
        edition = list(rec['ciphertext'])
        for change in earlier[rec['id']]['conditional_coordinate_changes']:
            assert edition[change['frame_index']] == change['from']
            edition[change['frame_index']] = change['to']
        rec['edition_ciphertext'] = ''.join(edition)
        rec['cohort'] = 'previous_23_record_snapshot'
    for source in data['additional_source_packages']:
        inputs = read(source['input'])
        key = inputs['keys']['Nov25-28']
        assert key['square'] == manifest['key']['square']
        assert key['column_rank_order'] == manifest['key']['column_rank_order']
        certificate = read(source['certificate'])
        assert certificate['input_sha256'] == digest(ROOT / source['input'])
        for rec in certificate['records']:
            native = rec.get('ciphertext', ''.join(
                c if c in base.CO else '?' for c in rec['literal_source']))
            edition = rec['readable_candidate']
            records.append({
                'id': rec['id'], 'literal': rec['literal_source'],
                'ciphertext': native, 'mapping': rec['model_to_source_indices'],
                'raw': rec['raw'], 'edition_ciphertext': edition['ciphertext'],
                'certificate': source['certificate'],
                'cohort': 'additional_source_reviewed_records',
            })
    assert len({r['id'] for r in records}) == len(records)
    return sorted(records, key=lambda r: r['id'])


def check_historical(data, paths):
    for source in data['historical_sources']:
        for crop in source['crops']:
            assert digest(HERE / crop['path']) == crop['sha256']
        if source['id'] not in paths:
            continue
        import fitz
        path = paths[source['id']]
        assert path.stat().st_size == source['pdf_bytes']
        assert digest(path) == source['pdf_sha256']
        doc = fitz.open(path)
        for crop in source['crops']:
            pix = doc[crop['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(crop['scale'], crop['scale']),
                clip=fitz.Rect(crop['clip_points']), alpha=False)
            assert (pix.width, pix.height) == (crop['width'], crop['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']


def build(historical_paths=None, check_cases=True):
    data = json.loads((HERE / 'names_inputs.json').read_text())
    for path, sha in data['dependencies'].items():
        assert digest(ROOT / path) == sha, path
    check_historical(data, historical_paths or {})
    earlier = load(ROOT / 'experiments/nov25_treaty_digits/verify_breslau.py',
                   'names_breslau')
    prior = earlier.run()
    assert prior == read(data['prior_certificate'])
    treaty_module = load(ROOT / 'experiments/nov25_treaty_digits/verify.py',
                         'names_treaty')
    treaty = treaty_module.run()
    base = treaty_module.load_prior()
    manifest = read('experiments/nov25_letter_constraint/inputs.json')
    key = manifest['key']
    ranks, square = key['column_rank_order'], key['square']
    assignment = data['assignment']
    pair, letter = assignment['pair'], assignment['value']
    cell = base.CO.index(pair[0]) * 6 + base.CO.index(pair[1])
    partial = list(prior['conditional_partial_square'])
    assert square[cell] == assignment['original_label']
    assert partial[cell] == '?' and letter not in partial
    partial[cell] = letter
    partial = ''.join(partial)
    unused = ''.join(sorted(set(base.ALPHABET) - (set(partial) - {'?'})))
    assert unused == '0345789Q'
    records, occurrences, new_positions = [], [], []
    inputs = source_records(data, base, manifest, treaty)
    for rec in inputs:
        source, edition = rec['ciphertext'], rec['edition_ciphertext']
        assert len(source) == len(edition) == len(rec['mapping'])
        used = [i for i in rec['mapping'] if i is not None]
        assert len(used) == len(set(used))
        for i, original in enumerate(rec['mapping']):
            value = rec['literal'][original] if original is not None else '?'
            assert source[i] == (value if value in base.CO else '?')
        native = base.read(source, ranks, square)
        assert native['plaintext'] == rec['raw']
        before = base.read(edition, ranks, prior['conditional_partial_square'])
        after = base.read(edition, ranks, partial)
        changes = treaty_module.changes(source, edition, rec['mapping'])
        for old, new in zip(before['positions'], after['positions']):
            assert set(new['domain']) <= set(old['domain'])
            if len(old['domain']) > 1 and len(new['domain']) == 1:
                assert new['pair'] == pair and new['domain'] == letter
                assert all(source[i] == edition[i] and source[i] in base.CO
                           for i in new['frame_indices'])
                new_positions.append({'record_id': rec['id'],
                                      'plaintext_index': new['index'],
                                      'pair': pair,
                                      'source_indices': [rec['mapping'][i]
                                                         for i in new['frame_indices']]})
        for pos in native['positions']:
            if pos['pair'] != pair:
                continue
            index = pos['index']
            edited_pair = ''.join(edition[i] for i in pos['frame_indices'])
            retained = edited_pair == pair
            occurrences.append({
                'record_id': rec['id'], 'plaintext_index': index,
                'pair': pair, 'source_indices': [rec['mapping'][i]
                                                for i in pos['frame_indices']],
                'baseline_context': rec['raw'][max(0, index - 15):index + 16],
                'conditional_edition_context': after['plaintext'][max(0, index - 15):index + 16],
                'retained_in_edition': retained,
                'previous_word_repairs_at_this_position': [c for c in changes
                                                          if c['frame_index'] in pos['frame_indices']],
            })
        records.append({
            'id': rec['id'], 'cohort': rec['cohort'],
            'source_certificate': rec['certificate'],
            'conditional_edition': after['plaintext'],
            'fixed_before': sum(len(p['domain']) == 1 for p in before['positions']),
            'fixed_after': sum(len(p['domain']) == 1 for p in after['positions']),
            'previous_coordinate_changes': changes,
            'additional_coordinate_changes': [],
            'native_roundtrip_witness': base.witness(source, ranks, partial),
            'edition_roundtrip_witness': base.witness(edition, ranks, partial),
        })
    by_id = {r['id']: r for r in records}
    input_by_id = {r['id']: r for r in inputs}
    for anchor in data['anchors']:
        matches = [o for o in occurrences
                   if (o['record_id'], o['plaintext_index']) ==
                   (anchor['record_id'], anchor['plaintext_index'])]
        assert len(matches) == 1 and matches[0]['retained_in_edition']
        assert matches[0]['source_indices'] == anchor['source_indices']
        start, end = anchor['word_range']
        assert input_by_id[anchor['record_id']]['raw'][start:end] == anchor['baseline_word']
        assert by_id[anchor['record_id']]['conditional_edition'][start:end] == anchor['interpreted_word']
    summary = {
        'reviewed_records': len(records),
        'plaintext_positions': sum(len(r['conditional_edition']) for r in records),
        'previous_snapshot_records': sum(r['cohort'] == 'previous_23_record_snapshot' for r in records),
        'additional_records': sum(r['cohort'] == 'additional_source_reviewed_records' for r in records),
        'observed_AD_occurrences': len(occurrences),
        'retained_edition_occurrences': sum(o['retained_in_edition'] for o in occurrences),
        'inconvenient_raw_occurrences': sum(not o['retained_in_edition'] for o in occurrences),
        'new_fixed_body_positions': len(new_positions),
        'additional_coordinate_changes': 0,
        'prior_square_completions': math.factorial(prior['conditional_partial_square'].count('?')),
        'remaining_square_completions': math.factorial(partial.count('?')),
    }
    assert summary == data['expected'], summary
    assert {(o['record_id'], o['plaintext_index']) for o in occurrences
            if not o['retained_in_edition']} == {('p221_B4', 42), ('p224_A2', 3)}
    for field in data['case_fields']:
        start, end = field['range']
        assert by_id[field['record_id']]['conditional_edition'][start:end] == field['text']
        if check_cases:
            assert '`' + field['text'] + '`' in (ROOT / field['case']).read_text()
    display = data['readable_quote']
    expected = ''.join(by_id[r]['conditional_edition'] for r in display['record_ids'])
    labels = re.sub('[^A-Z0-9?]', '', display['german'].upper())
    assert labels == expected.replace('X', '')
    if check_cases:
        page = (ROOT / display['case']).read_text()
        quotes = [' '.join(line[2:] for line in match[0].splitlines())
                  for match in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', page, re.M)]
        assert display['german'] in quotes
    return {
        'schema': 'adfgvx-nov25-names-certificate-v1',
        'prepared_by': data['prepared_by'],
        'input_sha256': digest(HERE / 'names_inputs.json'),
        'prior_partial_square': prior['conditional_partial_square'],
        'conditional_partial_square': partial, 'remaining_cell_domain': unused,
        'summary': summary, 'anchors': data['anchors'],
        'new_fixed_body_positions': new_positions,
        'all_observed_AD_occurrences': occurrences,
        'records': records, 'checked_case_fields': data['case_fields'],
        'readable_quote_verified': display,
        'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--surname-pdf', type=Path)
    parser.add_argument('--place-pdf', type=Path)
    args = parser.parse_args()
    paths = {k: v for k, v in [('surname', args.surname_pdf), ('place', args.place_pdf)] if v}
    result = build(paths)
    target = HERE / 'names_certificate.json'
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
