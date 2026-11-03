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
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.catalog import physical_source_accounting
from adfgvx.cipher import plaintext_domains
from adfgvx.source_evidence import verify_source_evidence

LINKED_FIXED_FIELD = 'source_linked_additional_fixed_label_positions'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify_source_linked_raw_normalization(package, certificate):
    """Separate the reviewed added-coordinate gain from the fixed-raw total.

    This handles the p158 E1 source-linked A and the origin-mapped p162/p166
    family. Other earlier copy-conditioned packages retain their recorded
    normalization; absent explicit reviewed metadata means zero.
    """
    counts = package['normalized_counts']
    reported_gain = counts.get(LINKED_FIXED_FIELD, 0)
    assert type(reported_gain) is int and reported_gain >= 0
    if certificate.get('schema') == 'adfgvx-nov9-wire-return-source-family-certificate-v1':
        inputs = read(ROOT / 'experiments' / package['name'] / 'inputs.json')
        key = inputs['key']
        sources = {r['id']: ''.join(''.join(r['source_rows']).split()) for r in inputs['records']}
        before = {r['id']: r for r in certificate['primary_unfilled_records']}
        after = {r['id']: r for r in certificate['source_linked_records']}
        assert set(before) == set(after) == set(package['record_ids'])
        raw_fixed = linked_fixed = 0
        for rid, old in before.items():
            new = after[rid]
            assert old['model_to_source_indices'] == new['model_to_source_indices']
            assert len(old['ciphertext']) == len(new['ciphertext'])
            for i, source_index in enumerate(old['model_to_source_indices']):
                if source_index is None:
                    assert old['ciphertext'][i] == '?'
                else:
                    assert old['ciphertext'][i] == new['ciphertext'][i] == sources[rid][source_index]
                origin = new['model_to_coordinate_origins'][i]
                assert new['ciphertext'][i] == sources[origin['record_id']][origin['source_index']]
            old_domains = plaintext_domains(old['ciphertext'], key['column_rank_order'], key['square'])
            new_domains = plaintext_domains(new['ciphertext'], key['column_rank_order'], key['square'])
            assert old_domains == [p['domain'] for p in old['positions']]
            assert new_domains == [p['domain'] for p in new['positions']]
            assert all(set(b) <= set(a) for a, b in zip(old_domains, new_domains))
            raw_fixed += sum(len(d) == 1 for d in old_domains)
            linked_fixed += sum(len(d) == 1 for d in new_domains)
        assert raw_fixed == counts['fixed_raw_label_positions_under_stated_geometry'] == 205
        assert linked_fixed - raw_fixed == reported_gain == 157
        edits = certificate['deduplicated_cross_copy_substitutions'] + certificate['deduplicated_lexical_substitutions']
        assert len({(r['record_id'], r['source_index']) for r in edits}) == len(edits) == 6
        assert counts['known_coordinate_substitutions'] == 6
        return reported_gain
    if certificate.get('schema') != 'adfgvx-source-linked-one-coordinate-parallel-certificate-v1':
        assert reported_gain == 0, (package['name'], 'Unreviewed source-linked fixed-position gain')
        return 0
    record, summary = certificate['record'], certificate['summary']
    unfilled = record['unfilled_gap']
    before, after = unfilled['positions'], record['positions']
    assert len(before) == len(after) == summary['plaintext_positions']
    fixed_before = sum(len(p['domain']) == 1 for p in before)
    fixed_after = sum(len(p['domain']) == 1 for p in after)
    assert fixed_before == len(unfilled['raw']) - unfilled['raw'].count('?')
    assert fixed_after == len(record['raw']) - record['raw'].count('?')
    assert fixed_before == unfilled['fixed_positions'] == summary['unfilled_gap_fixed_positions']
    assert fixed_after == record['fixed_positions'] == summary['baseline_fixed_positions']
    added = {i for i, source in enumerate(record['model_to_source_indices']) if source is None}
    assert len(added) == summary['source_linked_coordinate_additions'] == 1
    gained = []
    for old, new in zip(before, after):
        assert old['plaintext_index'] == new['plaintext_index']
        assert old['model_indices'] == new['model_indices']
        assert old['source_indices'] == new['source_indices']
        if not added.intersection(old['model_indices']):
            assert old == new
        assert set(new['domain']) <= set(old['domain'])
        if len(old['domain']) != 1 and len(new['domain']) == 1:
            gained.append(new['plaintext_index'])
    assert fixed_after - fixed_before == len(gained) == reported_gain == 1
    assert counts['fixed_raw_label_positions_under_stated_geometry'] == fixed_before, (
        package['name'], 'Fixed-raw normalization must leave the added coordinate unassigned')
    return reported_gain


def build(pdf=None):
    inputs = read(HERE / 'inputs.json')
    start, end = read(HERE / 'start_reading_catalog.json'), read(HERE / 'final_reading_catalog.json')
    assert sha(HERE / 'start_reading_catalog.json') == inputs['start_catalog_sha256']
    assert sha(HERE / 'final_reading_catalog.json') == inputs['final_catalog_sha256']
    assert start['challenge'] == end['challenge'] and len(end['challenge']) == 22
    start_sources = physical_source_accounting(start)
    end_sources = physical_source_accounting(end)
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
        verify_source_linked_raw_normalization(package, certificate)
        base_counts = {k: v for k, v in package['normalized_counts'].items()
                       if k != LINKED_FIXED_FIELD}
        if certificate.get('schema') == 'adfgvx-bidirectional-deciphering-certificate-v1':
            # Two equal-cost geometries belong to one physical received record.
            certificate_ids = {certificate['source_record']}
            assert base_counts == {
                'physical_records': 1,
                'source_slots': certificate['source_slots'],
                'modeled_plaintext_positions': certificate['conditional_plaintext_positions'],
                'fixed_raw_label_positions_under_stated_geometry': certificate['conditional_raw_fixed_positions'],
                'known_coordinate_substitutions': certificate['known_coordinate_substitutions_per_variant'],
            }
        elif certificate.get('schema') == 'adfgvx-warsaw-station-missing-row-certificate-v1':
            # Three compatible gap placements are alternative models of one source.
            certificate_ids = {certificate['source_record']}
            summary = certificate['summary']
            assert summary['physical_records'] == 1
            assert base_counts == {
                'physical_records': 1,
                'source_slots': summary['printed_source_slots'],
                'modeled_plaintext_positions': summary['plaintext_positions'],
                'fixed_raw_label_positions_under_stated_geometry': summary['baseline_fixed_positions'],
                'known_coordinate_substitutions': summary['known_coordinate_substitutions'],
            }
        elif certificate.get('schema') in (
                'adfgvx-nov9-urgent-embassy-address-certificates-v1',
                'adfgvx-source-linked-one-coordinate-parallel-certificate-v1',
                'adfgvx-conditional-two-duplicate-partial-certificate-v1'):
            certificate_ids = {certificate['record']['id']}
        elif 'source_records' in certificate:
            certificate_ids = set(certificate['source_records'])
        elif 'source_record' in certificate or 'record_id' in certificate:
            certificate_ids = {certificate.get('source_record', certificate.get('record_id'))}
        else:
            certificate_ids = {r['id'] for r in certificate['records']}
        assert set(package['record_ids']) == certificate_ids
        assert package['original_summary'] == certificate.get('summary', certificate.get('totals', certificate.get('normalized_counts')))
        if certificate.get('schema') == 'adfgvx-odessa-courier-pretransposition-certificate-v1':
            assert package['normalized_counts']['fixed_raw_label_positions_under_stated_geometry'] == certificate['summary']['unfilled_loss_model_fixed_positions']
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
    external_references = inputs.get('external_source_references', [])
    assert len({r['reference_id'] for r in external_references}) == len(external_references)
    assert all(r['storage'] == 'external_pdf_reference' for r in external_references)
    # Reference metadata is checked in the portable run; actual source pixels
    # are checked only when the caller provides the authenticated original PDF.
    source_reference_report = verify_source_evidence(
        pdf, inputs['source_pdf'], external_references, ROOT)
    assert source_reference_report['summary']['external_pdf_references'] == len(external_references)
    assert source_reference_report['summary']['embedded_pngs_checked'] == 0
    assert source_reference_report['summary']['crops_checked_against_pdf_pixels'] == (
        len(external_references) if pdf else 0)
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
    continuation = inputs.get('current_continuation')
    if continuation:
        continuation_start = datetime.fromisoformat(continuation['started_utc'].replace('Z', '+00:00'))
        continuation_end = datetime.fromisoformat(continuation['requested_until_utc'].replace('Z', '+00:00'))
        assert int((continuation_end - continuation_start).total_seconds()) == continuation['requested_seconds']
        assert continuation_end == extended_time
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
    totals[LINKED_FIXED_FIELD] = sum(p['normalized_counts'].get(LINKED_FIXED_FIELD, 0)
                                   for p in inputs['source_packages'])
    assert totals['physical_records'] == len(added)
    before_sources = set(start_sources['canonical_source_ids'].values())
    after_sources = set(end_sources['canonical_source_ids'].values())
    assert before_sources <= after_sources
    new_sources = after_sources - before_sources
    reviewed_sources = {end_sources['canonical_source_ids'][ident] for ident in represented}
    existing_source_editions = {ident for ident in added
                               if end_sources['canonical_source_ids'][ident] in before_sources}
    assert new_sources <= reviewed_sources
    # Package coverage includes the later edition of p132. It is useful reviewed
    # evidence, but its source was already present among the original challenges.
    totals['reviewed_record_entries'] = totals.pop('physical_records')
    totals['unique_reviewed_physical_sources'] = len(reviewed_sources)
    totals['new_physical_sources'] = len(new_sources)
    totals['previously_catalogued_physical_sources'] = len(reviewed_sources & before_sources)
    sort_entry = lambda ident: (after[ident]['printed_page'], after[ident]['source_section'], ident)
    cases = sorted({path for p in inputs['source_packages'] for path in p['case_pages']})
    return {'schema': 'adfgvx-post-publication-review-v2', 'authors': inputs['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'),
            'review_state': 'completed' if finished else 'in_progress',
            'initial_push_confirmed_utc': inputs['initial_push_confirmed_utc'],
            'minimum_followup_end_utc': inputs['minimum_followup_end_utc'],
            'extended_work_until_utc': extended_until,
            'review_finished_utc': finished, 'completed_elapsed_seconds_after_push': elapsed,
            'catalogue': {'challenge_entries': 22, 'other_reviewed_entries_before': 195,
                          'other_reviewed_entries_after': len(after),
                          'added_catalogue_entries': len(added),
                          'unique_physical_sources_before': start_sources['unique_physical_sources'],
                          'unique_physical_sources_after': end_sources['unique_physical_sources'],
                          'additional_physical_sources_before': start_sources['additional_physical_sources'],
                          'additional_physical_sources_after': end_sources['additional_physical_sources'],
                          'new_physical_records': len(new_sources),
                          'added_editions_of_existing_sources': len(existing_source_editions),
                          'registered_source_overlaps': end_sources['registered_overlaps'],
                          'removed_records': [], 'prior_metadata_changes_other_than_paths': [],
                          'canonical_path_updates': len(changed_paths)},
            'source_package_count': len(inputs['source_packages']), 'new_case_pages': cases,
            'source_image_count': len(seen_images),
            'external_pdf_source_reference_count': len(external_references),
            'external_source_pixels_require_original_pdf': True,
            'current_continuation': continuation,
            'pinned_artifact_count': len(inputs['artifact_sha256s']),
            'coverage_totals': totals, 'source_packages': inputs['source_packages'],
            'additional_packages': inputs['additional_packages'],
            'added_catalogue_entry_ids': sorted(added, key=sort_entry),
            'new_physical_source_ids': sorted(new_sources, key=sort_entry),
            'later_edition_ids_for_existing_sources': sorted(existing_source_editions, key=sort_entry),
            'counting_limits': inputs['counting_limits'] + [
                'Catalogue entries and physical sources are separate counts. Registered p132_B is a later edition of challenge p132 and adds no new physical source.',
                'Package coverage retains every reviewed entry and its modeled positions, including that existing source. Coverage totals separately report unique reviewed sources and genuinely new physical sources.',
                'Every unregistered duplicate printed-page/source-section location is rejected; similar bodies at different physical source locations are not merged.',
                'The p162/p166 source family leaves all195 copied prefix coordinates and its one added X unassigned in the fixed-raw baseline. Its157 additional fixed labels are reported separately, and repeated donor-prefix edits are charged once at their observed source origins.',
                'The fixed-raw total leaves the source-linked added coordinate of p158 E1 unassigned. Its one extra fixed position from the p170 B1 A is counted separately as source_linked_additional_fixed_label_positions. Existing copy-conditioned packages retain their original normalization; absent new metadata defaults to zero.']}


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
