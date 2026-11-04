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
import re
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
            pattern = r'Current catalogue SHA-256: `[0-9a-f]{64}`\.'
            assert len(re.findall(pattern, before)) == len(re.findall(pattern, after)) == 1
            assert re.sub(pattern, '', before) == re.sub(pattern, '', after)
            current_catalog = digest((ROOT / 'data/reading_catalog.json').read_bytes())
            assert f'Current catalogue SHA-256: `{current_catalog}`.' in after
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
