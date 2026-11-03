#!/usr/bin/env python3
"""Check the seven live Seifert reading-table cells against frozen evidence.

This is a display check, separate from source authentication and cipher
verification. Every bracketed insertion and question mark has an explicit
reviewed role. Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'data/reviews/seifert_readable_table_20261103.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_section(text, heading):
    headings = list(re.finditer(r'^## (.+)$', text, re.M))
    found = [(i, match) for i, match in enumerate(headings)
             if match[1] == heading]
    require(len(found) == 1, 'Missing or repeated table section: ' + heading)
    i, match = found[0]
    end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
    return text[match.end():end]


def table_rows(section, manifest):
    require(manifest['table_caption'] in section,
            'The table\'s editorial qualification changed')
    blocks = re.findall(r'(?:^\|[^\n]*(?:\n|$))+', section, re.M)
    require(len(blocks) == 1, 'Expected exactly one reading table')
    rows = []
    for line in blocks[0].splitlines():
        require(line.startswith('|') and line.endswith('|'),
                'Table row lacks outer delimiters')
        cells = [cell.strip() for cell in line[1:-1].split('|')]
        require(len(cells) == 3, 'Unreviewed table column or pipe delimiter')
        rows.append(cells)
    require(rows[0] == manifest['table_header'], 'Reading-table header changed')
    require(all(re.fullmatch(r':?-{3,}:?', cell) for cell in rows[1]),
            'Invalid reading-table divider')
    return rows[2:]


def display_labels(text, row):
    brackets = re.findall(r'\[[^\[\]]*\]', text)
    require(brackets == [item['text'] for item in row['brackets']],
            row['id'] + ': unreviewed bracketed material')
    index = 0

    def replace_bracket(match):
        nonlocal index
        item = row['brackets'][index]
        index += 1
        if item['role'] == 'display_only_expansion':
            return ''
        require(item['role'] == 'source_mask_completion',
                row['id'] + ': unknown bracket role')
        return match[0][1:-1]

    value = re.sub(r'\[[^\[\]]*\]', replace_bracket, text)
    require('[' not in value and ']' not in value,
            row['id'] + ': unbalanced bracket delimiters')
    for context in row.get('question_punctuation', []):
        require(context.endswith('?') and context.count('?') == 1,
                row['id'] + ': invalid question-punctuation declaration')
        require(value.count(context) == 1,
                row['id'] + ': question-punctuation context changed')
        value = value.replace(context, context[:-1])
    value = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', lambda m: m[1], value)
    require('`' not in value, row['id'] + ': unbalanced code-span delimiters')
    value = value.upper()
    for old, new in (('Ä', 'AE'), ('Ö', 'OE'), ('Ü', 'UE'), ('ẞ', 'SS')):
        value = value.replace(old, new)
    labels = []
    for char in value:
        if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?':
            labels.append(char)
        else:
            require(char.isspace() or unicodedata.category(char).startswith('P'),
                    row['id'] + ': unreviewed display character ' + repr(char))
    return ''.join(labels)


def evidence_plaintext(row, records):
    record = records[row['record_id']]
    if row.get('edition_id') is None:
        return record['raw_plaintext']
    editions = [item for item in record['editions']
                if item['id'] == row['edition_id']]
    require(len(editions) == 1, row['id'] + ': missing or repeated edition')
    edition = editions[0]
    require(edition['kind'] == row['edition_kind'],
            row['id'] + ': source-edit qualification changed')
    require(len(edition['known_coordinate_substitutions'])
            == row['observed_coordinate_substitutions'],
            row['id'] + ': observed-coordinate cost changed')
    require(len(edition['fills']) == row['source_mask_fills'],
            row['id'] + ': source-mask fill count changed')
    return edition['plaintext']


def verify(manifest):
    evidence_path = ROOT / manifest['evidence_path']
    require(sha(evidence_path.read_bytes()) == manifest['evidence_sha256'],
            'The protected source/cipher evidence changed')
    evidence = json.loads(evidence_path.read_text())
    records = {record['id']: record for record in evidence['records']}
    text = (ROOT / manifest['case_path']).read_text()
    rows = table_rows(read_section(text, manifest['section']), manifest)
    require(len(rows) == len(manifest['rows']), 'Reading-table row count changed')
    seen = set()
    total = unknowns = display_insertions = completions = 0
    for cells, row in zip(rows, manifest['rows']):
        require(row['id'] not in seen, 'Repeated manifest row: ' + row['id'])
        seen.add(row['id'])
        require(cells[0] == row['source_cell'], row['id'] + ': source label changed')
        require(sha(cells[2].encode()) == row['qualification_sha256'],
                row['id'] + ': meaning or evidence qualification changed')
        expected = evidence_plaintext(row, records)
        retained = row.get('retained_separator_positions', [])
        require(len(set(retained)) == len(retained)
                and all(expected[i] == 'X' for i in retained),
                row['id'] + ': invalid retained separator declaration')
        expected = ''.join(c for i, c in enumerate(expected)
                           if c != 'X' or i in retained)
        labels = display_labels(cells[1], row)
        require(labels == expected, row['id'] + ': readable labels differ from evidence')
        require(len(labels) == row['mapped_positions']
                and labels.count('?') == row['unresolved_positions'],
                row['id'] + ': mapped-position counts changed')
        for field in row.get('protected_fields', []):
            require(field in cells[1] and field in expected,
                    row['id'] + ': protected literal field changed')
        total += len(labels)
        unknowns += labels.count('?')
        for item in row['brackets']:
            count = sum(char.isalpha() for char in item['text'][1:-1])
            if item['role'] == 'display_only_expansion':
                display_insertions += count
            else:
                completions += count
    for field in manifest['coupled_fields']:
        copies = [records[name] for name in field['record_ids']]
        first = copies[0]
        for copy in copies[1:]:
            require(all(copy[key] == first[key] for key in (
                'analysis_ciphertext', 'partial_square', 'column_rank_order',
                'raw_plaintext', 'raw_domains')),
                'Identical-copy key or ciphertext relation changed')
        position = field['plaintext_position']
        require(first['raw_plaintext'][position] == '?'
                and first['raw_domains'][position] == field['domain'],
                'The shared unknown-cell domain changed')
        require(first['raw_plaintext'][position:position + len(field['literal_field'])]
                == field['literal_field'], 'The shared literal field changed')
    summary = {
        'table_rows': len(rows),
        'mapped_nonseparator_positions': total,
        'unresolved_positions_in_display': unknowns,
        'display_only_inserted_letters': display_insertions,
        'bracketed_source_mask_completion_letters': completions,
        'coupled_source_records': sum(len(field['record_ids'])
                                      for field in manifest['coupled_fields']),
    }
    require(summary == manifest['summary'], 'Manifest summary differs: ' + str(summary))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        result = verify(json.loads(args.manifest.read_text()))
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(json.dumps({'verified': False, 'error': str(error)}, ensure_ascii=False))
        return 1
    print('Seifert readable table: ' + json.dumps(result, sort_keys=True) + '; verified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
