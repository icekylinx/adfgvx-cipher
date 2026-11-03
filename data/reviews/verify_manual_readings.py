#!/usr/bin/env python3
"""Read-only audit of twelve manually clarified German reading layers.

Prepared by icekylinx and GPT-6 Astra Pro. Python standard library only.
Original source/decoded strings, section anchors and inline evidence remain
protected independently of later prose additions.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FENCE = re.compile(r'^```[^\n]*\n.*?^```[^\n]*$', re.M | re.S)
HEADING = re.compile(r'^#{1,6} .*$', re.M)
INLINE = re.compile(r'(?<!`)`([^`\n]+)`(?!`)')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_subsequence(old, current):
    """Retain every original occurrence, including duplicates, in order."""
    j = 0
    for item in current:
        if j < len(old) and item == old[j]:
            j += 1
    return j == len(old)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    audit = read_json(HERE / 'reading_conventions_manual_audit.json')
    before_path = ROOT / audit['before_snapshot_path']
    assert sha(before_path) == audit['before_snapshot_sha256']
    before = read_json(before_path)
    originals = {row['path']: row for row in before['files']}
    assert len(originals) == len(before['files']) == len(audit['files']) == 12
    totals = {'case_files': 0, 'existing_fenced_blocks_unchanged': 0,
              'existing_headings_unchanged': 0, 'existing_inline_code_tokens_preserved': 0}
    whole_file_snapshot_matches = []
    for row in audit['files']:
        source = originals[row['path']]
        text = source['markdown']
        assert hashlib.sha256(text.encode('utf-8')).hexdigest() == source['sha256'] == row['before_sha256']
        path = ROOT / row['path']
        current = path.read_text(encoding='utf-8')
        old_fences, new_fences = FENCE.findall(text), FENCE.findall(current)
        old_headings, new_headings = HEADING.findall(text), HEADING.findall(current)
        old_inline = INLINE.findall(FENCE.sub('', text))
        new_inline = INLINE.findall(FENCE.sub('', current))
        assert len(old_fences) == row['fenced_blocks_preserved']
        assert len(old_headings) == row['existing_headings_preserved']
        assert len(old_inline) == row['preexisting_inline_code_tokens_preserved']
        assert is_subsequence(old_fences, new_fences), (row['path'], 'changed or missing fenced evidence')
        assert is_subsequence(old_headings, new_headings), (row['path'], 'changed or missing existing heading')
        assert is_subsequence(old_inline, new_inline), (row['path'], 'changed or missing inline evidence')
        assert current.count('**Reading layers:**') == 1
        totals['case_files'] += 1
        totals['existing_fenced_blocks_unchanged'] += len(old_fences)
        totals['existing_headings_unchanged'] += len(old_headings)
        totals['existing_inline_code_tokens_preserved'] += len(old_inline)
        if sha(path) == row['final_sha256']:
            whole_file_snapshot_matches.append(row['path'])
    assert totals == audit['summary'] == {
        'case_files': 12, 'existing_fenced_blocks_unchanged': 42,
        'existing_headings_unchanged': 92, 'existing_inline_code_tokens_preserved': 349}

    mapping = read_json(ROOT / audit['tiflis_mapping_path'])
    certificate_path = ROOT / mapping['source_certificate_path']
    assert sha(certificate_path) == mapping['source_certificate_sha256']
    certificate = read_json(certificate_path)
    records = {r['id']: r for r in certificate['records']}
    first = next(c for c in records['p199_B1']['editorial_candidates'] if c['id'] == 'ordinary_word_repairs')['template']
    second = next(c for c in records['p192_2']['editorial_candidates'] if c['id'] == 'ordinary_word')['template']
    third = records['p192_3']['ordinary_word_repair']['template']
    assert '?1?' in first and 'ASERBEJNZAN' in second and 'T?DE?SKI' in third
    # These explicitly reviewed three strings contain separator X labels only.
    # DOPPELPUNKT is a transmitted word rendered as a colon in the German display.
    expected = (first + second + third).replace('X', '').replace('DOPPELPUNKT', '')
    page = (ROOT / mapping['case']).read_text(encoding='utf-8')
    marker = mapping['readable_block_marker'] + '\n\n'
    assert page.count(marker) == 1
    block = page.split(marker, 1)[1].split('\n\n', 1)[0]
    assert block == mapping['displayed_german_block']
    actual = ''.join(c for c in block.upper() if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?')
    assert actual == expected == mapping['normalized_shown'] == mapping['expected_selected_exact_text_without_separator_X_and_spelled_colon']
    assert len(actual) == 330
    assert all(field in block for field in mapping['unknown_fields_preserved'])
    assert mapping['historical_name_completion_used'] is False
    print(json.dumps({'verified': True, **totals, 'tiflis_nonseparator_labels_matched': len(actual),
                      'case_files_still_equal_manual_after_snapshot': len(whole_file_snapshot_matches),
                      'source_certificate_unchanged': True}, indent=2))


if __name__ == '__main__':
    main()
