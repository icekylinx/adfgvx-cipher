#!/usr/bin/env python3
"""Reconcile the source edition against the preserved pre-session catalogue.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Counts describe reviewed physical records, not first decipherments.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASELINE = 'ffc0c91e75b80e628524d665af9507f123fd664c'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    old = json.loads((HERE / 'baseline_reading_catalog.json').read_text())
    current = json.loads((ROOT / 'data/reading_catalog.json').read_text())
    assert len(old['challenge']) == len(current['challenge']) == 22
    assert len(old['other']) == 87
    old_rows = {r['id']: r for r in old['other']}
    rows = {r['id']: r for r in current['other']}
    assert len(rows) == len(current['other'])
    assert set(old_rows) <= set(rows)
    additions = [r for r in current['other'] if r['id'] not in old_rows]
    assert all(r['source_reviewed'] for r in additions)
    groups = defaultdict(list)
    for row in additions:
        groups[row['path'].split('#')[0]].append(row['id'])
    revisions = []
    for identifier, before in old_rows.items():
        after = rows[identifier]
        changes = {key: {'before': before.get(key), 'after': after.get(key)}
                   for key in sorted(set(before) | set(after))
                   if before.get(key) != after.get(key)}
        if changes:
            revisions.append({'id': identifier, 'changes': changes})
    unchanged = {'data/keys.json': '8902ab53ea0005370f5578a36e74cb8ef04d667cf5f714f93acfa7cd535e0dc1',
                 'data/messages.json': '1e4013252eb54065435ae1591abea729df8e40e482a6fe57165b512a9ba9c373'}
    for path, expected in unchanged.items():
        assert sha(ROOT / path) == expected
    return {'schema': 'adfgvx-source-extension-review-v1',
            'prepared_by': 'icekylinx and GPT-6 Astra Pro',
            'baseline_commit': BASELINE,
            'baseline_catalogue_sha256': sha(HERE / 'baseline_reading_catalog.json'),
            'current_catalogue_sha256': sha(ROOT / 'data/reading_catalog.json'),
            'challenge_entries_before': 22, 'challenge_entries_after': 22,
            'other_source_records_before': 87,
            'other_source_records_after': len(rows),
            'new_source_reviewed_records': len(additions),
            'removed_records': [], 'unchanged_core_files_sha256': unchanged,
            'additions_by_case': [{'path': path, 'count': len(ids), 'record_ids': ids}
                                  for path, ids in sorted(groups.items())],
            'added_records_with_original_status_and_credit': additions,
            'revisions_to_preexisting_rows': revisions,
            'challenge_row_revisions': [
                {'id': before['id'], 'before': before, 'after': after}
                for before in old['challenge']
                for after in current['challenge']
                if before['id'] == after['id'] and before != after],
            'limits': ['A physical-record addition can be a repeated intercept, multipart segment, prior reading, or conditional source edition.',
                       'The count of new source-reviewed rows is not a count of independently solved original ciphertexts or first historical decipherments.',
                       'The p153 partial decipherment predates this baseline and is not a new recovery in this extension.',
                       'p73, p170 and p198 D remain wholly open.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'inventory.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['baseline_commit', 'challenge_entries_after',
                                           'other_source_records_before', 'other_source_records_after',
                                           'new_source_reviewed_records', 'removed_records']}, indent=2))


if __name__ == '__main__':
    main()
