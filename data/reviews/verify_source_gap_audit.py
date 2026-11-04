#!/usr/bin/env python3
"""Check the 21-source gap-audit snapshot and its live reading links.

Source review: icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.source_evidence import verify_source_evidence
from adfgvx.catalog import load_catalog
from adfgvx.source_editions import page_target

TARGETS = set('p70_B1 p71_A2 p84_C p127_B2 p137_A6 p137_B p145_A '
              'p152_A2 p154_A2 p163_A16 p164_D p167_C1 p167_D p176_A6 '
              'p194_D1 p198_A p212_A4 p215_A p215_B1 p215_B3 p219_C'.split())


def load(path):
    return json.loads(path.read_text())


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def resolve_native_input(path, candidate):
    """Resolve a joint-analysis reference without counting it as another copy."""
    if 'source_rows' in candidate:
        return path, candidate, None
    ident = candidate['id']
    assert candidate.get('record_id') == ident, (path, ident, 'Reference identifier differs')
    assert candidate.get('rows_field') == 'source_rows', (path, ident, 'Unknown source field')
    native_path = candidate.get('inputs')
    assert isinstance(native_path, str) and native_path.endswith('/inputs.json'), (
        path, ident, 'Missing canonical input reference')
    source = load(ROOT / native_path)
    for key in candidate.get('input_root', []):
        source = source[key]
    records = source.get('records')
    if records is None and isinstance(source.get('record'), dict):
        records = [source['record']]
    matches = [r for r in (records or []) if r['id'] == ident]
    assert len(matches) == 1, (path, ident, 'Reference must resolve to one native record')
    native = matches[0]
    assert 'source_rows' in native, (path, ident, 'Reference does not resolve to a transcription')
    assert hashlib.sha256(literal(native).encode()).hexdigest() == candidate.get('source_sha256'), (
        path, ident, 'Referenced source digest differs')
    return native_path, native, dict(source_id=ident, derived_input=path, native_input=native_path)


def verify_matching_inputs(audited, matching):
    """Verify every cited native transcription, including later supplements.

    Several packages may cite the same physical body. They are acceptable only
    when each independently agrees with the frozen source and its identity;
    a repeated record inside one input file is not additional evidence.
    """
    ident = audited['id']
    assert matching, (ident, 'No matching canonical source input')
    paths = [path for path, _ in matching]
    assert len(paths) == len(set(paths)), (ident, 'Repeated source record in one input file')
    expected = literal(audited)
    for path, candidate in matching:
        assert candidate['id'] == ident, (path, ident, 'Source identifier differs')
        assert candidate['printed_page'] == audited['printed_page'], (path, ident, 'Printed page differs')
        assert literal(candidate) == expected, (path, ident, 'Native source transcription differs')
        for field in ('pdf_page_1based', 'source_section', 'source_slots',
                      'advertised_length', 'literal_sha256'):
            if field in candidate:
                assert candidate[field] == audited[field], (path, ident, field + ' differs')
        for field in ('observed_coordinates', 'valid_source_coordinates'):
            if field in candidate:
                assert candidate[field] == audited['valid_source_coordinates'], (
                    path, ident, field + ' differs')
        if 'printed_masks' in candidate:
            assert candidate['printed_masks'] == len(audited['masked_or_invalid_source_slots']), (
                path, ident, 'Printed-mask count differs')
        if len(matching) > 1:
            assert candidate['source_rows'] == audited['source_rows'], (
                path, ident, 'Repeated evidence changes native grouping')
            assert 'source_section' in candidate or 'header_transcription' in candidate, (
                path, ident, 'Repeated evidence lacks an explicit section or header')
            if 'header_transcription' in candidate:
                assert candidate['header_transcription'] == audited['header_transcription'], (
                    path, ident, 'Repeated evidence header differs')
    return dict(source_id=ident, native_records_verified=len(matching), evidence_paths=paths)


def report(data, editions):
    lines = ['# Source audit for 21 damaged or short bodies', '',
             'Source review: **icekylinx and GPT-6 Astra Pro**. The literal audit was recorded on 3 November 2026; catalogue states below are current.', '',
             'All 21 bodies have an explicit native transcription, slot count and '
             'reproducible original-PDF pixel reference. Each now has one canonical '
             'catalogue entry, including four OPEN sources with no accepted body reading. '
             'Source transcription and plaintext recovery remain separate results.', '',
             '| Source | Native slots | Valid coordinates | Mask/invalid slots | Advertised length | Current state |',
             '|---|---:|---:|---:|---:|---|']
    for r in data['records']:
        edition = editions.get(r['id'])
        link = ('[' + edition['state'] + '](../' + page_target(edition['path']) + ')'
                if edition else 'No accepted edition')
        lines.append('| ' + ' | '.join(map(str, [r['id'], r['source_slots'],
                     r['valid_source_coordinates'], len(r['masked_or_invalid_source_slots']),
                     r['advertised_length'] if r['advertised_length'] is not None else 'Not printed', link])) + ' |')
    lines += ['', 'The 21 literal transcriptions contain **3,451 source slots: 3,232 valid '
              'coordinates and 219 printed masks or invalid glyphs**. Source annotations '
              'are retained separately from coordinates.', '',
              'The main boundary corrections are p84 C’s final four-dash group, p145 A’s '
              'left-margin designator, p154 A2’s six-coordinate group, and p215 A’s final '
              'two-coordinate group. The p163 A16 label is a local identifier for the '
              'unlabelled fragment between printed parts 15 and 17. The p198 A C/G glyph '
              'alternatives, p215 B1 X/A alternative, and p219 C parentheses, duplicate '
              'prefix and jamming boundary remain explicit in the audit.', '',
              'Searches proceeded across source-directed loss frames, published square/rank '
              'components, source-copy constraints retaining half-coordinates, and calibrated '
              'word or unknown-rank searches. A failed search does not exclude a key, a '
              'different original length or another loss model. The linked editions carry '
              'their own exact repair prices and complete witnesses; fluency scores do '
              'not establish historical text.', '',
              '[Literal source audit and pixel recipes](../data/reviews/source_gap_audit_20261103.json) '
              '· [Live whole-material census](whole-material-coverage.md) '
              '· [Reading conventions](reading-conventions.md)', '',
              'Reproduce the count/link checks with '
              '`python data/reviews/verify_source_gap_audit.py --verify`. '
              'Add `--pdf /path/to/childs.pdf` to authenticate the original PDF and '
              'compare all 21 recorded crop pixel digests. Without that argument, the '
              'verifier explicitly reports that original-PDF pixels were not checked.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--verify', action='store_true', help='also check the generated report')
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    data = load(HERE / 'source_gap_audit_20261103.json')
    rows = data['records']
    assert len(rows) == 21 and {r['id'] for r in rows} == TARGETS
    assert len(data['source_images']) == 21
    assert {r['id'] for r in data['source_images']} == TARGETS
    by_id = {r['id']: r for r in rows}
    catalogue = load_catalog()
    editions = {r['id']: r for r in catalogue['challenge'] + catalogue['other']}
    input_reviews, reference_reviews = [], []
    for r in rows:
        text = literal(r)
        assert r['pdf_page_1based'] == r['printed_page'] + 3
        assert len(text) == r['source_slots']
        assert hashlib.sha256(text.encode()).hexdigest() == r['literal_sha256']
        masks = [{'source_index': i, 'glyph': c} for i, c in enumerate(text) if c not in 'ADFGVX']
        assert masks == r['masked_or_invalid_source_slots']
        assert r['valid_source_coordinates'] + len(masks) == len(text)
        assert isinstance(r['header_transcription'], str) and r['header_transcription']
        if r['id'] in editions:
            matching = {}
            for name in dict.fromkeys(editions[r['id']]['evidence']):
                if name.endswith('/inputs.json'):
                    inputs = load(ROOT / name)
                    records = inputs.get('records')
                    if records is None and isinstance(inputs.get('record'), dict):
                        records = [inputs['record']]
                    selected = [x for x in (records or []) if x['id'] == r['id']]
                    assert len(selected) <= 1, (name, r['id'], 'Repeated record in one input file')
                    for candidate in selected:
                        native_path, native, reference = resolve_native_input(name, candidate)
                        if native_path in matching:
                            assert matching[native_path] == native, (native_path, r['id'], 'Conflicting source reference')
                        matching[native_path] = native
                        if reference is not None:
                            reference_reviews.append(reference)
            input_reviews.append(verify_matching_inputs(r, list(matching.items())))
    assert sum(r['source_slots'] for r in rows) == 3451
    assert sum(r['valid_source_coordinates'] for r in rows) == 3232
    assert by_id['p84_C']['source_rows'][-1].endswith('FA--- ----')
    assert by_id['p145_A']['source_slots'] == 192
    assert literal(by_id['p145_A']).startswith('-----FDVXF')
    assert 'VDFDVD' in literal(by_id['p154_A2'])
    assert literal(by_id['p215_A']).endswith('DA') and by_id['p215_A']['source_slots'] == 390
    evidence = verify_source_evidence(args.pdf, data['source'], data['source_images'], HERE)
    rendered = report(data, editions)
    destination = ROOT / 'docs/source-gap-audit.md'
    if args.write_report:
        destination.write_text(rendered)
    if args.verify:
        assert destination.read_text() == rendered, 'Refresh the source-gap audit report'
    print(json.dumps({'verified': True, 'audited_physical_sources': 21,
                      'source_slots': 3451, 'valid_coordinates': 3232, 'mask_or_invalid_slots': 219,
                      'audited_sources_in_catalogue': len(TARGETS & editions.keys()),
                      'audited_sources_with_readable_editions': sum(
                          editions[ident]['state'] != 'OPEN' for ident in TARGETS & editions.keys()),
                      'audited_sources_still_open': sorted(
                          ident for ident in TARGETS & editions.keys() if editions[ident]['state'] == 'OPEN'),
                      'native_input_records_verified': sum(r['native_records_verified'] for r in input_reviews),
                      'derived_source_references_verified': reference_reviews,
                      'sources_with_identical_supplemental_inputs': [r for r in input_reviews
                          if r['native_records_verified'] > 1],
                      'source_evidence': evidence['summary']}, indent=2))


if __name__ == '__main__':
    main()
