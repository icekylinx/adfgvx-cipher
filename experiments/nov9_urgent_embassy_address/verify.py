#!/usr/bin/env python3
"""Verify p161 B1's native frame, source transcription corrections and display.

Prepared by icekylinx and GPT-6 Astra Pro. Standard library by default;
optional source-pixel reproduction requires PyMuPDF.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CO = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(source, key, full_square=None):
    ranks, square = key['column_rank_order'], full_square or key['square']
    width, n = len(ranks), len(source)
    mid, origins = [''] * n, [None] * n
    offset = 0
    for col in sorted(range(width), key=ranks.__getitem__):
        size = n // width + int(col < n % width)
        for row in range(size):
            mid[row * width + col] = source[offset + row]
            origins[row * width + col] = offset + row
        offset += size
    assert offset == n and n % 2 == 0
    positions = []
    for i in range(0, n, 2):
        pair = ''.join(mid[i:i + 2]); cells = []
        for row in range(6):
            for col in range(6):
                if (pair[0] not in CO or pair[0] == CO[row]) and (pair[1] not in CO or pair[1] == CO[col]):
                    cells.append(6 * row + col)
        domain = set()
        for cell in cells:
            domain.update(square[cell] if square[cell] != '?' else '56')
        domain = ''.join(sorted(domain))
        positions.append({'plaintext_index': i // 2, 'pair': pair, 'source_indices': origins[i:i + 2],
                          'square_cells': cells, 'domain': domain,
                          'label': domain if len(domain) == 1 else '?'})
    return ''.join(x['label'] for x in positions), positions


def encode(text, key, full_square=None):
    square, ranks = full_square or key['square'], key['column_rank_order']
    mid = ''.join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)
    return ''.join(mid[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text()); key = inp['key']
    assert key['id'] == 'Nov7-9'
    assert key['square'] == 'PRMYUW3LZGES8C71QOV29ITB40?KXH?AJNDF'
    assert sorted(key['column_rank_order']) == list(range(1, 21))
    assert sha(HERE / 'prior_evidence.json') == inp['prior_evidence_sha256']
    prior = json.loads((HERE / 'prior_evidence.json').read_text())
    doc = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        doc = fitz.open(pdf)
    for im in inp['source']['images']:
        assert sha(HERE / im['path']) == im['sha256']
        if doc is not None:
            fitz.TOOLS.store_shrink(100)
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(matrix=fitz.Matrix(im['scale'], im['scale']),
                                                        clip=fitz.Rect(im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    assert len(inp['records']) == 1
    r = inp['records'][0];source = ''.join(''.join(r['rows']).split())
    assert r['id'] == 'p161_B1' and source == r['literal_source']
    assert len(source) == r['advertised_length'] == 98 and set(source) <= set(CO)
    assert source[65:70] == 'DVGXV' and source[-3:] == 'AXA'
    raw, positions = decode(source, key)
    assert raw == r['expected_raw'] == r['editorial_text']
    assert raw == 'DEUTSCHEBOTSCHAFTCONSTANTINOPELDRINGENDXGEZXSTUMM'
    assert '?' not in raw and encode(raw, key) == source
    assert not r['coordinate_edits'] and not r['source_fills'] and not r['geometry_changes']
    assert all(d['square_cells'][0] not in [26, 30] for d in positions)
    for field in r['preserved_literal_fields']:
        assert field in raw
    initial = ''.join(''.join(prior['in_progress_manual_transcription']['rows']).split())
    assert len(initial) == 98
    diffs = [{'source_index': i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(initial, source)) if a != b]
    assert diffs == [{'source_index': 69, 'before': 'W', 'after': 'V'}, {'source_index': 96, 'before': 'A', 'after': 'X'}]
    intermediate = initial[:69] + 'V' + initial[70:]
    intermediate_raw = decode(intermediate, key)[0]
    assert intermediate_raw == 'DEUTSCHEBOTSCHAFTCONSTANTINOPELDRINGENUXGEZXSTUMM'
    assert [(i, a, b) for i, (a, b) in enumerate(zip(intermediate_raw, raw)) if a != b] == [(38, 'U', 'D')]
    normalized = ''.join(re.findall('[A-Z0-9?]', r['readable_german'].upper()))
    labels = [(i, c) for i, c in enumerate(raw) if c != 'X']
    assert normalized == ''.join(c for i, c in labels)
    assert '> ' + r['readable_german'] in (ROOT / r['readable_case_path']).read_text()
    mapping = [{'readable_normalized_index': j, 'raw_plaintext_index': i, 'label': c}
               for j, (i, c) in enumerate(labels)]
    witnesses = []
    for vf, xa in [('5', '6'), ('6', '5')]:
        square = list(key['square']);square[26] = vf;square[30] = xa;square = ''.join(square)
        assert len(set(square)) == 36
        assert decode(source, key, square)[0] == raw and encode(raw, key, square) == source
        witnesses.append({'assignments': {'VF': vf, 'XA': xa}, 'square': square,
                          'plaintext': raw, 'reencoded_ciphertext': source})
    return {'schema': 'adfgvx-nov9-urgent-embassy-address-certificates-v1', 'authors': inp['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'),
            'summary': {'physical_records': 1, 'literal_source_slots': 98, 'valid_source_coordinates': 98,
                        'working_frame_slots': 98, 'plaintext_positions': 49, 'raw_fixed_positions': 49,
                        'edited_fixed_positions': 49, 'observed_coordinate_substitutions': 0,
                        'source_mask_fills': 0, 'inserted_coordinates': 0, 'excluded_coordinates': 0,
                        'published_key_changes': 0, 'current_draft_transcription_corrections': 2,
                        'readable_non_x_labels': len(mapping)},
            'record': {'id': r['id'], 'raw_plaintext': raw, 'edited_plaintext': raw,
                       'positions': positions, 'reencoded_ciphertext': encode(raw, key),
                       'uses_unfilled_key_cells': False, 'readable_german': r['readable_german'],
                       'readable_non_x_mapping': mapping},
            'draft_transcription_diagnostics': {'initial_literal': initial, 'initial_raw': decode(initial, key)[0],
                                                'after_V_correction_literal': intermediate,
                                                'after_V_correction_raw': intermediate_raw,
                                                'after_AXA_source_review_raw': raw,
                                                'draft_coordinate_corrections': diffs,
                                                'historical_ciphertext_edits': []},
            'full_global_key_witnesses': witnesses,
            'date_evidence': {'receipt_header': 'November 8th', 'subsection_heading': '9th NOVEMBER, 1918.',
                              'internal_origin_field': '(9/11)', 'normalized_date': None},
            'limits': inp['limits']}


def main():
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('--verify', action='store_true');p.add_argument('--pdf', type=Path)
    args = p.parse_args();result = build(args.pdf)
    if args.verify:
        assert result == json.loads((HERE / 'certificates.json').read_text())
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': bool(args.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
