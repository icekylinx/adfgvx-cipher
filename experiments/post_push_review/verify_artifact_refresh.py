#!/usr/bin/env python3
"""Check the narrowly reviewed refresh of a preserved inventory's artifact pins.

The original inputs, inventory, counts and every changed byte remain recoverable.
No git checkout or network access is required. icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations

from difflib import unified_diff
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'data/reviews'))
from verify_reading_conventions import fence_blocks

AUDIT = 'experiments/post_push_review/artifact_refresh_20261104.json'
BEFORE_INPUTS = 'experiments/post_push_review/artifact_refresh_20261104_before_inputs.json'
BEFORE_INVENTORY = 'experiments/post_push_review/artifact_refresh_20261104_before_inventory.json'
VERIFIER = 'experiments/post_push_review/verify_artifact_refresh.py'
ADDED_ARTIFACTS = {AUDIT, BEFORE_INPUTS, BEFORE_INVENTORY, VERIFIER}


def digest(data):
    return sha256(data).hexdigest()


def load(relative):
    path = (ROOT / relative).resolve()
    assert path.is_relative_to(ROOT), relative
    return json.loads(path.read_bytes())


def restore_before(record, after):
    """Reverse exact reviewed text spans, preserving all untouched characters."""
    pieces = []
    before_cursor = after_cursor = 0
    for change in record['changes']:
        a, b = change['after_start'], change['after_end']
        c, d = change['before_start'], change['before_end']
        assert a >= after_cursor and c >= before_cursor
        unchanged = after[after_cursor:a]
        assert c == before_cursor + len(unchanged)
        assert after[a:b] == change['after_text']
        assert b - a == len(change['after_text'])
        assert d - c == len(change['before_text'])
        assert change['before_text'] != change['after_text']
        pieces.extend((unchanged, change['before_text']))
        before_cursor, after_cursor = d, b
    pieces.append(after[after_cursor:])
    return ''.join(pieces)


def verify_manifest(before, after, record):
    old, new = json.loads(before), json.loads(after)
    assert set(old) == set(new)
    assert {k: v for k, v in old.items() if k not in ('review_date_utc', 'files')} == {
        k: v for k, v in new.items() if k not in ('review_date_utc', 'files')}
    earlier = {r['path']: r for r in old['files']}
    current = {r['path']: r for r in new['files']}
    assert len(earlier) == len(old['files'])
    assert len(current) == len(new['files'])
    assert set(earlier) <= set(current)
    changed = []
    for path, value in earlier.items():
        other = current[path]
        assert {k: v for k, v in value.items() if k != 'file_sha256_at_review'} == {
            k: v for k, v in other.items() if k != 'file_sha256_at_review'}, path
        if value['file_sha256_at_review'] != other['file_sha256_at_review']:
            changed.append(path)
            assert other['file_sha256_at_review'] == digest((ROOT / path).read_bytes())
    assert sorted(changed) == record['manifest_review']['changed_existing_case_hashes']
    assert sorted(set(current) - set(earlier)) == record['manifest_review']['added_case_paths']


def verify_coverage_extension(before, after, record):
    """Admit exactly one newly catalogued, independently recomputed source.

    Reverse its live accounting contribution and recover the original pinned
    dashboard byte-for-byte. The older source inventory remains unchanged.
    """
    from copy import deepcopy
    import verify_childs_material_coverage as coverage

    review = record['coverage_source_extension']
    assert review['record_id'] == 'p163_A16'
    manifest = coverage.read(str(coverage.DEFAULT.relative_to(ROOT)))
    live = coverage.build(manifest)
    assert not live['quantitative_contract_rejections']
    assert coverage.render(live, manifest) == after
    targets = [r for r in live['records']
               if (r['printed_page'], r['source_section']) == (163, 'A16')]
    assert len(targets) == 1
    target = targets[0]
    assert target['catalogue_edition_ids'] == ['p163_A16']
    assert target['source_reviewed_in_current_catalogue_metadata'] is True
    count = target['counts']
    required = {
        'record_id': 'p163_A16', 'key_id': 'Nov7-9',
        'native_source_slots': 121, 'valid_source_coordinates': 121,
        'native_mask_slots': 0, 'frame_kind': 'modified_frame',
        'model_slots': 286, 'model_positions': 143,
        'fixed_raw_labels_with_all_unobserved_coordinates_unassigned': 0,
        'fixed_raw_labels_as_displayed_in_primary_certificate': 0,
        'additional_fixed_labels_from_supplied_unobserved_coordinates': 0,
        'prefilled_unobserved_model_indices': [], 'added_model_slots': 165,
        'excluded_source_slots': 0, 'excluded_valid_source_coordinates': 0,
        'candidate_counts': {'fixed_candidate_labels': 59,
                             'observed_coordinate_substitutions': 0,
                             'source_mask_fills': 0, 'added_coordinate_fills': 65},
    }
    assert {key: count[key] for key in required} == required
    assert review['expected_primary_counts'] == required
    prior = review['prior_unquantified_record']
    assert (prior['printed_page'], prior['source_section']) == (163, 'A16')
    assert prior['catalogue_edition_ids'] == [] and prior['counts'] is None
    assert prior['source_reviewed_in_current_catalogue_metadata'] is False
    before_current = review['before_current_summary']
    deltas = {'catalogue_entries': 1, 'catalogued_physical_sources': 1,
              'source_reviewed_physical_sources_per_metadata': 1,
              'other_entries': 1, 'additional_physical_sources_beyond_challenges': 1,
              'uncatalogued_bodies': -1, 'independently_quantified_primary_records': 1,
              'unquantified_primary_records': -1}
    assert set(before_current) == set(live['current'])
    assert live['current'] == {key: value + deltas.get(key, 0)
                               for key, value in before_current.items()}
    before_totals = review['before_quantified_subset_totals']
    expected_totals = deepcopy(before_totals)
    changed = expected_totals['modified_frame']
    changed['physical_sources'] += 1
    changed['native_unpaired_orphan_coordinates'] += count['native_orphan_source_index'] is not None
    changed['model_unpaired_orphan_coordinates'] += count['model_orphan_index'] is not None
    special = {'physical_sources', 'native_unpaired_orphan_coordinates',
               'model_unpaired_orphan_coordinates'}
    for key in set(changed) - special:
        changed[key] += count[key]
    assert expected_totals == live['quantified_subset_totals']
    original = deepcopy(live)
    original['current'] = before_current
    original['quantified_subset_totals'] = before_totals
    original['current_catalogue_sha256'] = review['original_dashboard_catalogue_sha256']
    original['records'] = [prior if (r['printed_page'], r['source_section']) == (163, 'A16') else r
                           for r in live['records']]
    assert coverage.render(original, manifest) == before


def run():
    inputs = load('experiments/post_push_review/inputs.json')
    inventory = load('experiments/post_push_review/inventory.json')
    audit = load(AUDIT)
    old_inputs, old_inventory = load(BEFORE_INPUTS), load(BEFORE_INVENTORY)
    pins, old_pins = inputs['artifact_sha256s'], old_inputs['artifact_sha256s']
    assert audit['schema'] == 'adfgvx-reviewed-artifact-refresh-v1'
    assert audit['offset_unit'] == 'zero-based Unicode code points; UTF-8 byte hashes'
    for path in ADDED_ARTIFACTS:
        assert digest((ROOT / path).read_bytes()) == pins[path], path
    assert set(pins) == set(old_pins) | ADDED_ARTIFACTS
    assert not (set(old_pins) & ADDED_ARTIFACTS)
    assert {k: v for k, v in inputs.items() if k != 'artifact_sha256s'} == {
        k: v for k, v in old_inputs.items() if k != 'artifact_sha256s'}
    old_inputs_hash = digest((ROOT / BEFORE_INPUTS).read_bytes())
    old_inventory_hash = digest((ROOT / BEFORE_INVENTORY).read_bytes())
    assert audit['preserved_inputs_sha256'] == old_inputs_hash
    assert audit['preserved_inventory_sha256'] == old_inventory_hash
    assert old_inventory['inputs_sha256'] == old_inputs_hash
    assert old_inventory['pinned_artifact_count'] == len(old_pins)
    assert set(inventory) == set(old_inventory)
    for key, value in old_inventory.items():
        if key == 'inputs_sha256':
            assert inventory[key] == digest((HERE / 'inputs.json').read_bytes())
        elif key == 'pinned_artifact_count':
            assert inventory[key] == len(pins)
        else:
            assert inventory[key] == value, key
    records = {r['path']: r for r in audit['artifacts']}
    assert len(records) == len(audit['artifacts'])
    changed_pins = {path for path in old_pins if pins[path] != old_pins[path]}
    assert changed_pins == set(records)
    for path, expected in pins.items():
        assert digest((ROOT / path).read_bytes()) == expected, path
    restored_count = 0
    case_count = 0
    for path, record in records.items():
        assert record['before_sha256'] == old_pins[path]
        assert record['after_sha256'] == pins[path]
        assert record['review_reason'] and record['changes']
        after = (ROOT / path).read_text()
        before = restore_before(record, after)
        assert digest(before.encode()) == old_pins[path], path
        assert digest(after.encode()) == pins[path], path
        diff = ''.join(unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                    fromfile='a/' + path, tofile='b/' + path))
        assert diff == record['unified_diff'], path
        if record['kind'] == 'case_prose':
            assert fence_blocks(before) == fence_blocks(after), path
            case_count += 1
        elif record['kind'] == 'reading_layer_manifest':
            verify_manifest(before, after, record)
        elif record['kind'] == 'coverage_dashboard':
            verify_coverage_extension(before, after, record)
        else:
            raise AssertionError(record['kind'])
        for dependency in record['review_evidence']:
            assert digest((ROOT / dependency['path']).read_bytes()) == dependency['sha256'], dependency['path']
        restored_count += 1
    result = dict(reviewed_artifact_updates=restored_count,
                  case_pages_with_all_original_fences_and_headings_preserved=case_count,
                  original_pinned_artifacts=len(old_pins), current_pinned_artifacts=len(pins),
                  added_review_evidence_artifacts=len(ADDED_ARTIFACTS),
                  original_inventory_counts_and_source_packages_unchanged=True)
    assert result == audit['summary']
    return result


if __name__ == '__main__':
    print(json.dumps(dict(verified=True, **run()), indent=2))
