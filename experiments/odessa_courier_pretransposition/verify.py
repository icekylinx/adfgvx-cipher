#!/usr/bin/env python3
"""Verify a conditional two-coordinate loss before the p201 C transposition.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, transpose, untranspose

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(rows):
    return ''.join(''.join(rows).split())


def order(n, ranks):
    columns = [[] for _ in ranks]
    offset = 0
    for col in sorted(range(len(ranks)), key=lambda i: ranks[i]):
        height = n // len(ranks) + (col < n % len(ranks))
        columns[col] = list(range(offset, offset + height))
        offset += height
    return [columns[c][r] for r in range((n + len(ranks) - 1) // len(ranks))
            for c in range(len(ranks)) if r < len(columns[c])]


def fractionate(plain, square):
    return ''.join('??' if c == '?' else C[square.index(c) // 6] + C[square.index(c) % 6]
                   for c in plain)


def read_fractionated(middle, square, mapping):
    assert len(middle) % 2 == 0 and len(middle) == len(mapping)
    unused = set(A) - set(square)
    positions = []
    for p in range(len(middle) // 2):
        pair = middle[2*p:2*p+2]
        cells = [6*r+c for r in range(6) for c in range(6)
                 if pair[0] in ('?', C[r]) and pair[1] in ('?', C[c])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        positions.append({'plaintext_index': p, 'pair': pair,
            'fractionation_indices': [2*p, 2*p+1],
            'received_source_indices': mapping[2*p:2*p+2],
            'domain': domain, 'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    return {'raw': raw, 'fixed_positions': len(raw) - raw.count('?'),
            'positions': positions}


def loss_map(received_order, gaps):
    it = iter(received_order)
    mapping = [None if i in gaps else next(it) for i in range(len(received_order) + len(gaps))]
    assert next(it, None) is None
    return mapping


def geometry_scan(middle, square, spans, selected):
    plain = ['?'] * 163
    for i in selected:
        span = spans[i]
        plain[span['start']:span['start']+len(span['text'])] = span['text']
    encoded = fractionate(''.join(plain), square)
    prefix = []
    for skipped in range(3):
        p = [0]
        for j, observed in enumerate(middle):
            target = encoded[j + skipped]
            p.append(p[-1] + int(observed != '?' and target != '?' and observed != target))
        prefix.append(p)
    best, minima = 999, []
    histogram = Counter()
    digest = hashlib.sha256()
    for first in range(325):
        for second in range(first+1, 326):
            cost = (prefix[0][first] + prefix[1][second-1] - prefix[1][first]
                    + prefix[2][324] - prefix[2][second-1])
            histogram[cost] += 1
            digest.update(f'{first},{second},{cost}\n'.encode())
            if cost < best:
                best, minima = cost, []
            if cost == best:
                minima.append([first, second])
    assert sum(histogram.values()) == 52975
    return {'plaintext_stencil': ''.join(plain), 'fractionation_stencil': encoded,
        'models_tested': 52975, 'minimum_observed_substitutions': best,
        'all_minimum_missing_fractionation_positions': minima,
        'all_placement_costs_sha256': digest.hexdigest(),
        'cost_histogram': {str(k): v for k, v in sorted(histogram.items())}}


def check_pdf(data, pdf):
    import fitz
    assert pdf.stat().st_size == data['source']['pdf_bytes']
    assert sha(pdf) == data['source']['pdf_sha256']
    doc = fitz.open(pdf)
    for crop in data['reviewed_source_crops']:
        pix = doc[crop['pdf_page_1based']-1].get_pixmap(
            matrix=fitz.Matrix(crop['render_scale'], crop['render_scale']),
            clip=fitz.Rect(*crop['crop_pdf_points']))
        assert [pix.width, pix.height, pix.n] == [crop['width'], crop['height'], crop['channels']]
        assert hashlib.sha256(pix.samples).hexdigest() == crop['rgb_sha256']


def build(pdf=None):
    data = json.loads((HERE / 'inputs.json').read_text())
    record, key = data['record'], data['key']
    assert data['authors'] == 'icekylinx and GPT-6 Astra Pro'
    assert key == next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                       if k['id'] == key['id'])
    for name, digest in data['prior_artifacts'].items():
        assert sha(HERE / name) == digest
    if pdf:
        check_pdf(data, pdf)
    source = compact(record['source_rows'])
    assert len(source) == record['source_slots'] == record['advertised_length'] == 324
    assert set(source) <= set(C) and source[50:55] == 'GXXDV'
    audit = json.loads((HERE / 'source_transcription_audit.json').read_text())
    assert audit['corrected_literal_source'] == source
    assert [(i, a, b) for i, (a, b) in enumerate(zip(audit['initial_literal_source'], source)) if a != b] == [(15, 'D', 'G')]
    assert record['overstrike_source_indices'] == [51, 52]
    ranks, square = key['column_rank_order'], key['square']
    received_order = order(324, ranks)
    middle = ''.join(source[i] for i in received_order)
    assert middle == untranspose(source, ranks) and transpose(middle, ranks) == source
    native = read_fractionated(middle, square, received_order)
    assert native['raw'] == decrypt(source, ranks, square)
    assert native['fixed_positions'] == 153
    conservative = ''.join('?' if i in (51, 52) else c for i, c in enumerate(source))
    conservative_middle = ''.join(conservative[i] for i in received_order)
    native_conservative = read_fractionated(conservative_middle, square, received_order)
    assert native_conservative['fixed_positions'] == 151

    scans = []
    for branch, raw_middle in [('visible_XX', middle), ('conservative_two_masks', conservative_middle)]:
        for scope in data['geometry_scopes']:
            result = geometry_scan(raw_middle, square, data['geometry_prefix_spans'], scope['span_indices'])
            assert result['minimum_observed_substitutions'] == 0
            expected_count = {'all_prefix': 2, 'without_odessa': 2,
                              'address_only': 522, 'without_courier': 32}[scope['id']]
            assert len(result['all_minimum_missing_fractionation_positions']) == expected_count
            if scope['id'] in ('all_prefix', 'without_odessa'):
                assert result['all_minimum_missing_fractionation_positions'] == [[36, 74], [37, 74]]
            scans.append({'glyph_branch': branch, 'scope': scope['id'], **result})

    branches = []
    for gaps in record['equivalent_missing_fractionated_positions']:
        mapping = loss_map(received_order, gaps)
        unfilled = ''.join('?' if i is None else source[i] for i in mapping)
        unfilled_reading = read_fractionated(unfilled, square, mapping)
        filled = list(unfilled)
        for i, value in zip(gaps, record['missing_values']):
            filled[i] = value
        filled = ''.join(filled)
        filled_reading = read_fractionated(filled, square, mapping)
        assert filled_reading['raw'] == record['expected_loss_frame_filled_raw']
        stencil = fractionate(record['edited_output'], square)
        edited = ''.join(a if b == '?' else b for a, b in zip(filled, stencil))
        events = [{'fractionation_index': j, 'received_source_index': mapping[j],
                   'from': a, 'to': b} for j, (a, b) in enumerate(zip(filled, edited)) if a != b]
        assert all(e['received_source_index'] is not None for e in events)
        assert sorted([e['received_source_index'], e['from'], e['to']] for e in events) == record['expected_received_substitutions']
        edited_reading = read_fractionated(edited, square, mapping)
        assert edited_reading['raw'] == record['edited_output']
        # The forward process removes the hypothesized losses BEFORE applying
        # the original 324-coordinate column permutation.
        shortened = ''.join(edited[j] for j in range(326) if j not in gaps)
        reconstructed_received = transpose(shortened, ranks)
        changes = [[i, a, b] for i, (a, b) in enumerate(zip(source, reconstructed_received)) if a != b]
        assert changes == record['expected_received_substitutions']
        assert transpose(''.join(filled[j] for j in range(326) if j not in gaps), ranks) == source
        assert [i for i in mapping if i is not None] == received_order
        assert sorted(i for i in mapping if i is not None) == list(range(324))
        sensitivity = ''.join('?' if origin in (51, 52) else edited[j]
                              for j, origin in enumerate(mapping))
        sensitivity_reading = read_fractionated(sensitivity, square, mapping)
        branches.append({'missing_fractionation_positions': gaps,
            'fractionation_to_received_source_indices': mapping,
            'unfilled_fractionation': unfilled, 'raw_unfilled': unfilled_reading,
            'added_fractionation_fills': [{'fractionation_index': i, 'value': c}
                                         for i, c in zip(gaps, record['missing_values'])],
            'filled_fractionation': filled, 'filled_raw': filled_reading,
            'observed_received_substitutions': events,
            'edited_fractionation': edited, 'edited': edited_reading,
            'reconstructed_received_ciphertext_after_observed_substitutions': reconstructed_received,
            'forward_error_model_roundtrip': True,
            'conservative_overstrike_edited': sensitivity_reading,
            'conservative_overstrike_extra_fills_if_XX_adopted': [
                {'received_source_index': 51, 'coordinate': 'X'},
                {'received_source_index': 52, 'coordinate': 'X'}]})
    primary = branches[0]
    assert branches[0]['filled_fractionation'] == branches[1]['filled_fractionation']
    assert branches[0]['edited_fractionation'] == branches[1]['edited_fractionation']
    assert primary['raw_unfilled']['fixed_positions'] == 157
    assert primary['filled_raw']['fixed_positions'] == 159
    assert primary['edited']['fixed_positions'] == 160
    assert primary['conservative_overstrike_edited']['fixed_positions'] == 158
    remaining = [p for p in primary['edited']['positions'] if p['raw'] == '?']
    assert [p['plaintext_index'] for p in remaining] == [152, 157, 161]
    assert [p['pair'] for p in remaining] == ['AF', 'GG', 'FD']
    assert all(p['domain'] == '03456789' for p in remaining)
    assert primary['edited']['raw'].endswith('ZT?NRX1?111?X')

    unknown = [i for i, c in enumerate(square) if c == '?']
    labels = sorted(set(A) - set(square))
    assert len(unknown) == len(labels) == 8
    digest = hashlib.sha256()
    witnesses = {}
    total = 0
    complete_middle = primary['edited_fractionation']
    for values in itertools.permutations(labels):
        full = list(square)
        for i, c in zip(unknown, values):
            full[i] = c
        full = ''.join(full)
        plain = ''.join(full[C.index(complete_middle[i])*6+C.index(complete_middle[i+1])]
                        for i in range(0, 326, 2))
        assert fractionate(plain, full) == complete_middle
        shortened = ''.join(complete_middle[i] for i in range(326) if i not in (36, 74))
        assert transpose(shortened, ranks) == primary['reconstructed_received_ciphertext_after_observed_substitutions']
        signature = ''.join(plain[i] for i in [152, 157, 161])
        assert len(set(signature)) == 3
        if signature not in witnesses:
            witnesses[signature] = {'reference_labels_152_157_161': signature,
                'complete_square': full, 'plaintext': plain,
                'historical_reference_assignment_claim': False}
        digest.update((full + '|' + plain + '\n').encode())
        total += 1
    assert total == 40320 and len(witnesses) == 336

    witness = json.loads((HERE / 'address_witness.json').read_text())
    live = json.loads((ROOT / witness['origin_path']).read_text())
    wr = next(r for r in live['records'] if r['id'] == witness['record']['id'])
    assert wr == witness['record']
    wc = compact(wr['source_rows'])
    wo = order(len(wc), ranks)
    wm = ''.join(wc[i] for i in wo)
    reading = read_fractionated(wm, square, wo)
    assert reading['raw'] == wr['expected_raw']
    spans = []
    address_at = reading['raw'].index('BEVOLLMAECHTIGTEN')
    for word, start in [('BEVOLLMAECHTIGTEN', address_at),
                        ('ODESSA', reading['raw'].index('ODESSA', address_at))]:
        assert reading['raw'][start:start+len(word)] == word
        positions = reading['positions'][start:start+len(word)]
        assert all(p['raw'] != '?' and '?' not in p['pair'] for p in positions)
        spans.append({'word': word, 'start': start, 'observed_pair_positions': positions})
    assert sha(HERE / witness['source_image']['path']) == witness['source_image']['sha256']

    case = (ROOT / data['case']).read_text()
    assert 'Literal header: `' + record['literal_header'] + '`.' in case
    assert '\n'.join(record['source_rows']) in case
    for plain in [native['raw'], primary['raw_unfilled']['raw'], primary['filled_raw']['raw'],
                  primary['edited']['raw'], primary['conservative_overstrike_edited']['raw']]:
        assert '\n```text\n' + plain + '\n```\n' in case
    assert '> ' + record['readable_german'] + '\n' in case
    folded = ''.join(c for c in record['readable_german'].upper() if c in A + '?')
    assert folded == record['edited_output'].replace('X', '')
    assert '324-coordinate transposition' in case and 'before transposition' in case
    return {'schema': 'adfgvx-odessa-courier-pretransposition-certificate-v1',
        'project': data['project'], 'authors': data['authors'],
        'input_sha256': sha(HERE / 'inputs.json'), 'indexing': 'All indices are zero-based.',
        'summary': {'physical_records': 1, 'printed_source_slots': 324,
            'valid_source_coordinates_primary_visible_glyphs': 324,
            'unambiguous_source_coordinates': 322,
            'received_transposition_coordinates': 324,
            'reconstructed_fractionation_coordinates': 326,
            'plaintext_positions': 163, 'native_fixed_positions': 153,
            'unfilled_loss_model_fixed_positions': 157,
            'filled_loss_model_fixed_positions': 159, 'candidate_fixed_positions': 160,
            'known_coordinate_substitutions': 4, 'added_fractionation_slots': 2,
            'added_fractionation_fills': 2, 'received_source_insertions': 0,
            'received_source_exclusions': 0, 'primary_source_mask_fills': 0,
            'conservative_overstrike_candidate_fixed_positions': 158,
            'published_key_changed': False},
        'source_crops_require_optional_pdf_for_pixel_verification': True,
        'record_id': record['id'], 'literal_header': record['literal_header'],
        'literal_source': source, 'literal_source_rows': record['source_rows'],
        'received_intermediate_to_source_indices': received_order,
        'native': native, 'native_conservative_overstrike': native_conservative,
        'geometry_scans': scans, 'all_primary_minimum_branches': branches,
        'remaining_reference_domains': remaining,
        'global_completion_check': {'full_square_assignments_checked': total,
            'distinct_reference_tuples': len(witnesses),
            'enumeration_sha256': digest.hexdigest(),
            'all_reference_tuple_witnesses': [witnesses[s] for s in sorted(witnesses)]},
        'independent_native_address_witness': {'record_id': wr['id'], 'spans': spans,
            'new_record_counted': False, 'identical_message_claim': False},
        'readable_german': record['readable_german'],
        'prior_credit': data['prior_credit'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify,
        'source_pixel_verification': 'passed' if args.pdf else 'not requested; requires --pdf',
        **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
