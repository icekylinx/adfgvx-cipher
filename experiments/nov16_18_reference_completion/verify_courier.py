#!/usr/bin/env python3
"""Propagate existing FD=8 / VA=5 through the p201 C courier-loss models.

Prepared by icekylinx and GPT-6 Astra Pro. No new square assignment or repair.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def read(path):
    return json.loads((ROOT / path).read_text())


def fractionate(text, square):
    return ''.join(CO[square.index(c)//6] + CO[square.index(c)%6] for c in text)


def read_fractionation(stream, square):
    unused = set(ALPHABET) - set(square)
    positions = []
    for p in range(len(stream)//2):
        pair = stream[2*p:2*p+2]
        domain = set()
        for cell in range(36):
            coords = CO[cell//6] + CO[cell%6]
            if all(a == '?' or a == b for a, b in zip(pair, coords)):
                domain.update(unused if square[cell] == '?' else square[cell])
        positions.append({'plaintext_index': p, 'pair': pair,
                          'domain': ''.join(sorted(domain))})
    text = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in positions)
    return text, positions


def build(case_text=None):
    data = json.loads((HERE / 'courier_inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    source_input = read(data['source_inputs'])
    prior = read(data['source_certificate'])
    layer = read(data['conditional_layer_certificate'])['conditional_key_layer']
    record, key = source_input['record'], source_input['key']
    assert record['id'] == data['record'] == 'p201_C'
    assert key == next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov16-18')
    base, square, ranks = key['square'], layer['conditional_square'], key['column_rank_order']
    assert [(CO[i//6]+CO[i%6], a, b) for i, (a, b) in enumerate(zip(base, square))
            if a != b] == [('FD', '?', '8'), ('VA', '?', '5')]
    assert [a['id'] for a in layer['assumptions']] == ['nov16_fd_8', 'nov16_va_5']
    source = ''.join(''.join(record['source_rows']).split())
    assert len(source) == 324 and source == prior['literal_source']
    transposition_order = [j for c in sorted(range(len(ranks)), key=ranks.__getitem__)
                           for j in range(c, 324, len(ranks))]
    received_order = [transposition_order.index(j) for j in range(324)]
    assert received_order == prior['received_intermediate_to_source_indices']

    def transpose324(stream):
        assert len(stream) == 324
        return ''.join(stream[i] for i in transposition_order)

    def forward(stream, gaps):
        assert len(stream) == 326
        return transpose324(''.join(c for i, c in enumerate(stream) if i not in gaps))

    expected_received = list(source)
    for i, old, new in record['expected_received_substitutions']:
        assert source[i] == old
        expected_received[i] = new
    expected_received = ''.join(expected_received)
    branches = []
    assert record['equivalent_missing_fractionated_positions'] == [[36, 74], [37, 74]]
    for gaps in record['equivalent_missing_fractionated_positions']:
        old_branch = next(b for b in prior['all_primary_minimum_branches']
                          if b['missing_fractionation_positions'] == gaps)
        iterator = iter(received_order)
        mapping = [None if j in gaps else next(iterator) for j in range(326)]
        assert next(iterator, None) is None
        assert mapping == old_branch['fractionation_to_received_source_indices']
        stream = ['?' if i is None else source[i] for i in mapping]
        assert ''.join(stream) == old_branch['unfilled_fractionation']
        for j, c in zip(gaps, record['missing_values']):
            stream[j] = c
        assert ''.join(stream) == old_branch['filled_fractionation']
        for source_index, old, new in record['expected_received_substitutions']:
            j = mapping.index(source_index)
            assert stream[j] == old
            stream[j] = new
        stream = ''.join(stream)
        assert stream == old_branch['edited_fractionation']
        earlier, _ = read_fractionation(stream, base)
        current, positions = read_fractionation(stream, square)
        assert earlier == record['edited_output']
        assert current == data['expected']
        assert [p for p, (a, b) in enumerate(zip(earlier, current)) if a != b] == [161]
        assert mapping[322:324] == [187, 289]
        assert source[187] + source[289] == 'FD' and current[161] == '8'
        remaining = [p for p in positions if len(p['domain']) != 1]
        assert [(p['plaintext_index'], p['pair'], p['domain']) for p in remaining] == [
            (152, 'AF', '034679'), (157, 'GG', '034679')]
        for p in remaining:
            p['received_source_indices'] = mapping[2*p['plaintext_index']:2*p['plaintext_index']+2]
        conservative = ''.join('?' if i in record['overstrike_source_indices'] else stream[j]
                               for j, i in enumerate(mapping))
        old_conservative, _ = read_fractionation(conservative, base)
        new_conservative, conservative_positions = read_fractionation(conservative, square)
        assert old_conservative == old_branch['conservative_overstrike_edited']['raw']
        assert len(earlier)-earlier.count('?') == 160
        assert len(current)-current.count('?') == 161
        assert len(old_conservative)-old_conservative.count('?') == 158
        assert len(new_conservative)-new_conservative.count('?') == 159
        assert forward(stream, gaps) == expected_received
        branches.append({'missing_fractionation_positions': gaps,
                         'fractionation_to_received_source_indices': mapping,
                         'earlier_edition': earlier, 'interpreted_edition': current,
                         'edited_fractionation': stream,
                         'conservative_interpretation': new_conservative,
                         'remaining_reference_domains': remaining,
                         'conservative_remaining_domains': [p for p in conservative_positions if len(p['domain']) != 1]})
    assert branches[0]['interpreted_edition'] == branches[1]['interpreted_edition']
    assert branches[0]['edited_fractionation'] == branches[1]['edited_fractionation']
    unused = sorted(set(ALPHABET)-set(square))
    holes = [i for i, c in enumerate(square) if c == '?']
    assert unused == list('034679') and len(holes) == 6
    witnesses, digest = {}, hashlib.sha256()
    squares, roundtrips = 0, 0
    for values in itertools.permutations(unused):
        full = list(square)
        for i, c in zip(holes, values):
            full[i] = c
        full = ''.join(full)
        for branch in branches:
            stream = branch['edited_fractionation']
            text, _ = read_fractionation(stream, full)
            assert '?' not in text
            assert all(a == '?' or a == b for a, b in zip(branch['interpreted_edition'], text))
            assert fractionate(text, full) == stream
            assert forward(fractionate(text, full), branch['missing_fractionation_positions']) == expected_received
            assert text[161] == '8'
            pair = text[152] + text[157]
            assert len(set(pair)) == 2 and set(pair) <= set('034679')
            witnesses.setdefault(pair, {'reference_labels_152_157_161': pair+'8',
                                        'complete_square': full, 'plaintext': text,
                                        'arbitrary_completion_not_historical_number': True})
            digest.update((str(branch['missing_fractionation_positions'])+'|'+full+'|'+text+'\n').encode())
            roundtrips += 1
        squares += 1
    assert squares == 720 and roundtrips == 1440 and len(witnesses) == 30
    # All 36 possible readings of the two retained source masks preserve FD.
    mask_checks = 0
    sample_square = next(iter(witnesses.values()))['complete_square']
    for branch in branches:
        for mask_values in itertools.product(CO, repeat=2):
            stream = list(branch['edited_fractionation'])
            for source_index, c in zip(record['overstrike_source_indices'], mask_values):
                stream[branch['fractionation_to_received_source_indices'].index(source_index)] = c
            stream = ''.join(stream)
            text, _ = read_fractionation(stream, sample_square)
            assert text[161] == '8' and fractionate(text, sample_square) == stream
            received = forward(stream, branch['missing_fractionation_positions'])
            assert all(received[i] == c for i, c in enumerate(expected_received)
                       if i not in record['overstrike_source_indices'])
            mask_checks += 1
    assert mask_checks == 72
    folded = ''.join(c for c in data['german'].upper() if c in ALPHABET+'?')
    assert folded == data['expected'].replace('X', '')
    case_text = (ROOT/data['case']).read_text() if case_text is None else case_text
    assert '> '+data['german']+'\n' in case_text
    return {'schema': 'adfgvx-nov16-18-courier-propagation-v1', 'authors': data['authors'],
            'input_sha256': hashlib.sha256((HERE/'courier_inputs.json').read_bytes()).hexdigest(),
            'indexing': 'Zero-based plaintext, fractionation and received-source indices.',
            'record': data['record'], 'conditional_square': square,
            'inherited_assumptions': layer['assumptions'],
            'native_new_position': {'plaintext_index': 161, 'pair': 'FD', 'value': '8',
                                    'received_source_indices': [187, 289], 'received_coordinates': ['F', 'D']},
            'positions': 163, 'fixed_before': 160, 'fixed_after': 161,
            'conservative_fixed_before': 158, 'conservative_fixed_after': 159,
            'retained_observed_substitutions': record['expected_received_substitutions'],
            'retained_added_fractionation_fills': 2, 'additional_observed_substitutions': 0,
            'additional_mask_or_fractionation_fills': 0,
            'received_transposition_length': 324, 'reconstructed_fractionation_length': 326,
            'literal_received_source': source, 'edited_received_ciphertext': expected_received,
            'branches': branches, 'complete_squares_checked': squares,
            'forward_roundtrips_checked': roundtrips, 'distinct_reference_tuples': len(witnesses),
            'all_reference_witnesses': [witnesses[p] for p in sorted(witnesses)],
            'full_square_witnesses_sha256': digest.hexdigest(),
            'two_mask_combinations_per_geometry': 36, 'two_mask_witness_checks': mask_checks,
            'german': data['german'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build()
    if args.pdf:
        sys.path.insert(0, str(ROOT))
        from experiments.odessa_courier_pretransposition.verify import check_pdf
        data = json.loads((HERE/'courier_inputs.json').read_text())
        check_pdf(read(data['source_inputs']), args.pdf)
    path = HERE/'courier_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print('p201 C: native FD=8 adds one footer position, 160->161/163; '
          '720 squares / 30 reference tuples; both loss maps and all glyph-mask combinations checked; '
          'no additional source edits or fills.')


if __name__ == '__main__':
    main()
