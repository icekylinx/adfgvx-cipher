#!/usr/bin/env python3
"""Verify the preserved post-publication source-recovery inventory.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The optional PDF check independently authenticates every delivered source crop.
"""
from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def build(pdf=None):
    inputs = read(HERE / 'inputs.json')
    start, end = read(HERE / 'start_reading_catalog.json'), read(HERE / 'final_reading_catalog.json')
    assert sha(HERE / 'start_reading_catalog.json') == inputs['start_catalog_sha256']
    assert sha(HERE / 'final_reading_catalog.json') == inputs['final_catalog_sha256']
    assert start['challenge'] == end['challenge'] and len(end['challenge']) == 22
    before = {r['id']: r for r in start['other']}
    after = {r['id']: r for r in end['other']}
    assert len(before) == len(start['other']) == 195
    assert len(after) == len(end['other']) and set(before) <= set(after)
    assert list(before) == [r['id'] for r in end['other'][:195]]
    aliases = {a['old_path']: a['canonical_path']
               for a in read(ROOT / 'data/case_path_aliases.json')['aliases']}
    changed_paths = []
    for ident, old in before.items():
        new = after[ident]
        assert {k: v for k, v in old.items() if k != 'path'} == {k: v for k, v in new.items() if k != 'path'}, ident
        if old['path'] != new['path']:
            path, marker, anchor = old['path'].partition('#')
            assert new['path'] == aliases[path] + (marker + anchor if marker else '')
            changed_paths.append(ident)
    added = set(after) - set(before)
    represented = []
    for package in inputs['source_packages']:
        folder = ROOT / 'experiments' / package['name']
        proposals = read(folder / 'catalog_proposal.json')
        certificate = read(folder / 'certificates.json')
        assert package['record_ids'] == [r['id'] for r in proposals]
        if certificate.get('schema') == 'adfgvx-bidirectional-deciphering-certificate-v1':
            # Two equal-cost geometries belong to one physical received record.
            certificate_ids = {certificate['source_record']}
            assert package['normalized_counts'] == {
                'physical_records': 1,
                'source_slots': certificate['source_slots'],
                'modeled_plaintext_positions': certificate['conditional_plaintext_positions'],
                'fixed_raw_label_positions_under_stated_geometry': certificate['conditional_raw_fixed_positions'],
                'known_coordinate_substitutions': certificate['known_coordinate_substitutions_per_variant'],
            }
        elif certificate.get('schema') == 'adfgvx-nov9-urgent-embassy-address-certificates-v1':
            certificate_ids = {certificate['record']['id']}
        else:
            certificate_ids = {r['id'] for r in certificate['records']}
        assert set(package['record_ids']) == certificate_ids
        assert package['original_summary'] == certificate.get('summary', certificate.get('totals'))
        assert len(proposals) == package['normalized_counts']['physical_records']
        for row in proposals:
            assert row == after[row['id']]
        represented.extend(package['record_ids'])
    assert len(represented) == len(set(represented)) and set(represented) == added
    for relative, expected in inputs['artifact_sha256s'].items():
        path = (ROOT / relative).resolve()
        assert path.is_relative_to(ROOT)
        assert sha(path) == expected, relative
    expected_core = {
        'data/keys.json': '8902ab53ea0005370f5578a36e74cb8ef04d667cf5f714f93acfa7cd535e0dc1',
        'data/messages.json': '1e4013252eb54065435ae1591abea729df8e40e482a6fe57165b512a9ba9c373',
    }
    assert inputs['unchanged_core_files'] == expected_core
    for relative, expected in expected_core.items():
        assert sha(ROOT / relative) == expected
    seen_images = set()
    for image in inputs['source_images']:
        assert image['path'] not in seen_images
        seen_images.add(image['path'])
        assert sha(ROOT / image['path']) == image['png_sha256']
        assert image['pdf_page_1based'] > 0 and image['scale'] > 0
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf) == inputs['source_pdf']['sha256']
        assert pdf.stat().st_size == inputs['source_pdf']['bytes']
        doc = fitz.open(pdf)
        for item in inputs['source_images']:
            if item.get('fresh_render_cache'):
                fitz.TOOLS.store_shrink(100)
            scale = item['scale']
            pix = doc[item['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*item['clip_pdf_points']))
            saved = Image.open(ROOT / item['path']).convert('RGB')
            assert saved.size == (item['width'], item['height']) == (pix.width, pix.height), item['path']
            assert saved.tobytes() == pix.samples, item['path']
            assert hashlib.sha256(pix.samples).hexdigest() == item['rgb_pixel_sha256'], item['path']
    start_time = datetime.fromisoformat(inputs['initial_push_confirmed_utc'].replace('Z', '+00:00'))
    minimum = datetime.fromisoformat(inputs['minimum_followup_end_utc'].replace('Z', '+00:00'))
    assert int((minimum - start_time).total_seconds()) == inputs['minimum_required_followup_seconds'] == 7200
    extended_until = inputs.get('extended_work_until_utc')
    if extended_until:
        extended_time = datetime.fromisoformat(extended_until.replace('Z', '+00:00'))
        assert extended_time >= minimum
    finished = inputs['review_finished_utc']
    elapsed = None
    if finished is not None:
        finish_time = datetime.fromisoformat(finished.replace('Z', '+00:00'))
        elapsed = int((finish_time - start_time).total_seconds())
        assert elapsed >= inputs['minimum_required_followup_seconds']
        if extended_until:
            assert finish_time >= extended_time
    totals = {name: sum(p['normalized_counts'][name] for p in inputs['source_packages'])
              for name in ('physical_records', 'source_slots', 'modeled_plaintext_positions',
                           'fixed_raw_label_positions_under_stated_geometry', 'known_coordinate_substitutions')}
    assert totals['physical_records'] == len(added)
    cases = sorted({path for p in inputs['source_packages'] for path in p['case_pages']})
    return {'schema': 'adfgvx-post-publication-review-v1', 'authors': inputs['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'),
            'review_state': 'completed' if finished else 'in_progress',
            'initial_push_confirmed_utc': inputs['initial_push_confirmed_utc'],
            'minimum_followup_end_utc': inputs['minimum_followup_end_utc'],
            'extended_work_until_utc': extended_until,
            'review_finished_utc': finished, 'completed_elapsed_seconds_after_push': elapsed,
            'catalogue': {'challenge_entries': 22, 'other_records_before': 195,
                          'other_records_after': len(after), 'new_physical_records': len(added),
                          'removed_records': [], 'prior_metadata_changes_other_than_paths': [],
                          'canonical_path_updates': len(changed_paths)},
            'source_package_count': len(inputs['source_packages']), 'new_case_pages': cases,
            'source_image_count': len(seen_images), 'pinned_artifact_count': len(inputs['artifact_sha256s']),
            'coverage_totals': totals, 'source_packages': inputs['source_packages'],
            'additional_packages': inputs['additional_packages'],
            'new_record_ids': sorted(added, key=lambda ident: (after[ident]['printed_page'], after[ident]['source_section'])),
            'counting_limits': inputs['counting_limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    target = HERE / 'inventory.json'
    if args.verify:
        assert result == read(target)
    else:
        target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': bool(args.pdf),
                      'state': result['review_state'], **result['catalogue'],
                      'source_images': result['source_image_count'], **result['coverage_totals']}, indent=2))


if __name__ == '__main__':
    main()
