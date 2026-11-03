#!/usr/bin/env python3
"""Reconstruct Childs's twelve numbered teaching examples from exact source rows.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
The independent grid implementation preserves every source coordinate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SYMBOLS = 'ADFGVX'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_grid(length, ranks):
    """Fill complete/ragged columns in transmitted rank order, then read rows."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    rows, remaining = divmod(length, width)
    columns = [None] * width
    offset = 0
    for rank in range(1, width + 1):
        col = ranks.index(rank)
        height = rows + (col < remaining)
        columns[col] = list(range(offset, offset + height))
        offset += height
    assert offset == length
    order = [columns[c][r] for r in range(rows + bool(remaining))
             for c in range(width) if r < len(columns[c])]
    assert sorted(order) == list(range(length))
    return order


def decode(source, key):
    order = source_grid(len(source), key['column_rank_order'])
    intermediate = ''.join(source[i] for i in order)
    positions = []
    for i in range(len(source) // 2):
        pair = intermediate[2*i:2*i+2]
        cell = 6*SYMBOLS.index(pair[0]) + SYMBOLS.index(pair[1])
        positions.append({'plaintext_index': i, 'source_indices': order[2*i:2*i+2],
                          'coordinate_pair': pair, 'square_cell': cell,
                          'label': key['square'][cell]})
    return ''.join(p['label'] for p in positions), positions, order


def encode(plain, key):
    intermediate = ''.join(SYMBOLS[key['square'].index(c)//6] +
                           SYMBOLS[key['square'].index(c)%6] for c in plain)
    order = source_grid(len(intermediate), key['column_rank_order'])
    received = [None] * len(intermediate)
    for i, source_index in enumerate(order):
        received[source_index] = intermediate[i]
    assert all(c in SYMBOLS for c in received)
    return ''.join(received)


def authenticate_pdf(pdf, inp):
    if pdf is None:
        return {'mode': 'external_pdf_reference', 'pdf_file_checked': False,
                'pdf_pixels_checked': False, 'rendered_crops': 0}
    import fitz
    pdf = Path(pdf)
    assert pdf.stat().st_size == inp['source']['pdf_bytes']
    assert sha(pdf) == inp['source']['pdf_sha256']
    doc = fitz.open(pdf)
    for crop in inp['source_crops']:
        assert crop['storage'] == 'external_pdf_reference'
        scale = crop['render_scale']
        pix = doc[crop['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(crop['crop_pdf_points']))
        assert (pix.width, pix.height, pix.n) == (crop['width'], crop['height'], crop['channels'])
        assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']
    return {'mode': 'external_pdf_reference', 'pdf_file_checked': True,
            'pdf_pixels_checked': True, 'rendered_crops': len(inp['source_crops'])}


def build():
    inp = json.loads((HERE / 'inputs.json').read_text())
    assert inp['authors'] == 'icekylinx and GPT-6 Astra Pro'
    core = {'data/keys.json': '8902ab53ea0005370f5578a36e74cb8ef04d667cf5f714f93acfa7cd535e0dc1',
            'data/messages.json': '1e4013252eb54065435ae1591abea729df8e40e482a6fe57165b512a9ba9c373'}
    for path, digest in core.items():
        assert sha(ROOT / path) == digest
    key = inp['key']
    assert key == next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                       if k['id'] == 'Worked-example-VIKINGSCROWNHOTEL')
    assert len(key['column_rank_order']) == 17 and len(set(key['square'])) == 36
    readme = (HERE / 'README.md').read_text()
    records = []
    for record in inp['records']:
        literal = ''.join(''.join(record['source_rows']).split())
        assert len(literal) == record['printed_length'] and set(literal) <= set(SYMBOLS)
        assert len(literal) % 2 == 0
        plain, positions, mapping = decode(literal, key)
        assert plain == record['raw_plaintext']
        assert re.sub('[^A-Z0-9]', '', record['readable_english'].upper()) == plain
        assert '\n' + plain + '\n' in readme and '> ' + record['readable_english'] in readme
        witness = encode(plain, key)
        assert witness == literal
        records.append({'id': record['id'], 'printed_pages': record['printed_pages'],
                        'source_coordinates': len(literal), 'plaintext_positions': len(plain),
                        'raw_fixed_positions': len(plain), 'source_literal': literal,
                        'raw_plaintext': plain, 'readable_english': record['readable_english'],
                        'positions': positions, 'intermediate_to_source_indices': mapping,
                        'reencrypted_ciphertext': witness, 'exact_roundtrip': True,
                        'observed_substitutions': [], 'source_mask_fills': [],
                        'inserted_coordinates': [], 'excluded_coordinates': []})
    assert len(records) == 12 and len({r['id'] for r in records}) == 12
    by_id = {r['id']: r for r in records}
    proposals = []
    for proposal in inp['optional_editorial_proposals']:
        record = by_id[proposal['record']]
        before = record['raw_plaintext']
        at = proposal['plaintext_index']
        assert before[at] == proposal['from']
        after = before[:at] + proposal['to'] + before[at+1:]
        candidate = encode(after, key)
        changes = [[i, old, new] for i, (old, new) in enumerate(zip(record['source_literal'], candidate))
                   if old != new]
        assert changes == proposal['expected_source_changes']
        assert decode(candidate, key)[0] == after
        proposals.append({**proposal, 'complete_plaintext': after,
                          'reencrypted_ciphertext': candidate, 'source_changes': changes,
                          'observed_substitution_count': len(changes),
                          'selected_in_primary_edition': False})
    summary = {'instructional_examples': len(records),
               'printed_source_coordinates': sum(r['source_coordinates'] for r in records),
               'plaintext_positions': sum(r['plaintext_positions'] for r in records),
               'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in records),
               'primary_observed_substitutions': 0, 'primary_source_mask_fills': 0,
               'primary_insertions': 0, 'primary_exclusions': 0,
               'new_historical_log_sources': 0}
    assert summary['printed_source_coordinates'] == 2058
    assert summary['plaintext_positions'] == summary['raw_fixed_positions'] == 1029
    return {'schema': 'adfgvx-childs-instructional-certificate-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'),
            'indexing': 'All machine-readable indices are zero-based.',
            'summary': summary, 'records': records, 'optional_editorial_proposals': proposals,
            'core_files_unchanged': core, 'counting_limits': inp['counting_limits'],
            'source_authentication': 'Text-only PDF references; actual pixel checks require --pdf.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    certificate = build()
    path = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(path.read_text()) == certificate
    else:
        path.write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + '\n')
    evidence = authenticate_pdf(args.pdf, json.loads((HERE / 'inputs.json').read_text()))
    print(json.dumps({'verified': True, 'summary': certificate['summary'], 'source_check': evidence}, indent=2))


if __name__ == '__main__':
    main()
