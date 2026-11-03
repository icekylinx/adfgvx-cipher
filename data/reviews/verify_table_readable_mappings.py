#!/usr/bin/env python3
"""Bind selected live table cells to their declared JSON evidence strings.

Reuses the reviewed table and bracket rules of the Seifert checker. Unmapped
rows are byte-preserved, not claimed as semantically verified. Source and
cipher authentication remain separate. Prepared by icekylinx and
GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import json
import sys

from verify_seifert_readable_table import (
    display_labels, read_section, require, sha, table_rows,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'data/reviews/transport_table_readable_mappings_20261103.json'


def at_path(value, path):
    for key in path:
        value = value[key]
    return value


def verify(manifest):
    evidence = {}
    for name, digest in manifest['evidence_files'].items():
        path = ROOT / name
        require(sha(path.read_bytes()) == digest, 'Protected evidence changed: ' + name)
        evidence[name] = json.loads(path.read_text())

    def source(reference):
        return at_path(evidence[reference['path']], reference['keys'])

    text = (ROOT / manifest['case_path']).read_text()
    rows = table_rows(read_section(text, manifest['section']), manifest)
    require([cells[0] for cells in rows] == manifest['ordered_source_cells'],
            'Table rows were added, removed or reordered')
    for note in manifest['required_case_notes']:
        require(note in text, 'Required local uncertainty explanation changed')
    mapped, total, unknowns = set(), 0, 0
    for row in manifest['rows']:
        index = row['table_row_index']
        require(index not in mapped, 'Repeated table-row mapping')
        mapped.add(index)
        cells = rows[index]
        require(cells[0] == row['source_cell'], row['id'] + ': source label changed')
        require(sha(cells[2].encode()) == row['qualification_sha256'],
                row['id'] + ': meaning or uncertainty qualification changed')
        raw = source(row['plaintext_source'])
        require(isinstance(raw, str), row['id'] + ': plaintext source is not a string')
        separator = row['separator_label']
        retained = row['retained_separator_positions']
        require(len(set(retained)) == len(retained)
                and all(raw[i] == separator for i in retained),
                row['id'] + ': invalid retained separator positions')
        expected = ''.join(char for i, char in enumerate(raw)
                           if char != separator or i in retained)
        labels = display_labels(cells[1], row)
        require(labels == expected, row['id'] + ': readable labels differ from evidence')
        require(len(labels) == row['mapped_positions']
                and labels.count('?') == row['unresolved_positions'],
                row['id'] + ': display-position count changed')
        for field in row['protected_fields']:
            require(field in labels and field in raw,
                    row['id'] + ': protected literal field changed')
        total += len(labels)
        unknowns += labels.count('?')
    preserved = set()
    for row in manifest['unmapped_rows_preserved']:
        index = row['table_row_index']
        require(index not in mapped and index not in preserved,
                'Repeated or conflicting preserved-row entry')
        preserved.add(index)
        require(sha(json.dumps(rows[index], ensure_ascii=False).encode())
                == row['cells_sha256'], 'Unmapped table row changed')
    require(mapped | preserved == set(range(len(rows))), 'Table row lacks a review role')

    for group in manifest['same_cell_groups']:
        positions = {item['plaintext_index']: item for item in source(group['positions_source'])}
        raw = source(group['plaintext_source'])
        for index in group['plaintext_indices']:
            point = positions[index]
            require(raw[index] == '?' and point['coordinate_pair'] == group['coordinate_pair']
                    and point['possible_characters'] == group['domain'],
                    'Shared unknown-cell relation changed')
        require(len(group['coordinate_pair']) == 2
                and set(group['coordinate_pair']) <= set('ADFGVX'),
                'A shared unknown cell must have two observed coordinates')
    for erasure in manifest['source_erasures']:
        literal = source(erasure['literal_source'])
        positions = {item['plaintext_index']: item
                     for item in source(erasure['positions_source'])}
        point = positions[erasure['plaintext_index']]
        require(literal[erasure['source_index']] == erasure['printed_glyph']
                and erasure['printed_glyph'] not in 'ADFGVX',
                'Declared invalid source glyph changed')
        require(point['coordinate_pair'] == erasure['coordinate_pair']
                and point['possible_characters'] == erasure['domain']
                and point['source_indices'] == erasure['source_indices']
                and point['coordinate_pair'][point['source_indices'].index(erasure['source_index'])] == '?',
                'Erased-source position or domain changed')
    summary = {
        'table_rows': len(rows),
        'exactly_mapped_rows': len(mapped),
        'other_rows_preserved': len(preserved),
        'mapped_nonseparator_positions': total,
        'unresolved_positions_in_display': unknowns,
        'same_cell_groups': len(manifest['same_cell_groups']),
        'distinct_shared_unknown_positions': sum(len(group['plaintext_indices'])
                                                for group in manifest['same_cell_groups']),
        'displayed_source_erasure_positions': len(manifest['source_erasures']),
    }
    require(summary == manifest['summary'], 'Manifest summary differs: ' + str(summary))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        result = verify(json.loads(args.manifest.read_text()))
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        print(json.dumps({'verified': False, 'error': str(error)}, ensure_ascii=False))
        return 1
    print('Live table mappings: ' + json.dumps(result, sort_keys=True) + '; verified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
