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

TARGETS = set('p70_B1 p71_A2 p84_C p127_B2 p137_A6 p137_B p145_A '
              'p152_A2 p154_A2 p163_A16 p164_D p167_C1 p167_D p176_A6 '
              'p194_D1 p198_A p212_A4 p215_A p215_B1 p215_B3 p219_C'.split())


def load(path):
    return json.loads(path.read_text())


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def report(data, editions):
    lines = ['# Review of the 21 source gaps', '',
             '**icekylinx and GPT-6 Astra Pro · 3 November 2026**', '',
             'This audit covers the 21 physical bodies outside the readable catalogue at '
             '`f3badb0`. All 21 have a fresh source transcription, an explicit slot count '
             'and a reproducible original-PDF pixel reference. A source audit alone does '
             'not turn an unread body into a recovered message. The edition column below '
             'uses the current catalogue and includes partial and conditional readings.', '',
             '| Source | Native slots | Valid coordinates | Mask/invalid slots | Advertised length | Current edition |',
             '|---|---:|---:|---:|---:|---|']
    for r in data['records']:
        edition = editions.get(r['id'])
        link = ('[Partial/conditional edition](../' + edition['path'] + ')'
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
    catalogue = load(ROOT / 'data/reading_catalog.json')
    editions = {r['id']: r for r in catalogue['challenge'] + catalogue['other']}
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
            matching = []
            for name in editions[r['id']]['evidence']:
                if name.endswith('/inputs.json'):
                    inputs = load(ROOT / name)
                    records = inputs.get('records')
                    if records is None and isinstance(inputs.get('record'), dict):
                        records = [inputs['record']]
                    matching += [x for x in (records or []) if x['id'] == r['id']]
            assert len(matching) == 1, r['id']
            assert literal(matching[0]) == text, r['id']
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
                      'audited_sources_with_readable_editions': len(TARGETS & editions.keys()),
                      'source_evidence': evidence['summary']}, indent=2))


if __name__ == '__main__':
    main()
