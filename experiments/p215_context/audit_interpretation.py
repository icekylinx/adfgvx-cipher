#!/usr/bin/env python3
"""Locate every coordinate cost of selected p215 editorial readings.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
These are conditional interpretations, not newly observed plaintext letters.
"""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SYMBOLS = 'ADFGVX'

SEGMENTS = [
    ('mili5', 4, 'MILI5', 'Unexpanded identifier; L is allowed but not independently established.'),
    ('midi5', 4, 'MIDI5', 'Earlier shortened identifier; D needs one known-coordinate change.'),
    ('eilmeldg', 10, 'EILMELDG', 'Earlier editorial expansion; the raw prefix does not force this word.'),
    ('kertsch', 33, 'KERTSCH', 'Likely place name; the two erased letters permit T and H.'),
    ('ententeflotte', 47, 'ENTENTEFLOTTE', 'Plausible wording for the Entente fleet.'),
    ('zwodivisionen', 60, 'ZWODIVISIONEN', 'Plausible count and unit word; this does not identify the units.'),
    ('neuseelaender', 74, 'NEUSEELAENDER', 'Earlier reading; the nationality and any deployment remain uncorroborated.'),
    ('franzo', 95, 'FRANZO', 'Earlier abbreviated French nationality reading.'),
    ('nur_ohl', 106, 'NUROHL', 'Possible distribution restriction, not a recovered instruction.'),
    ('korps_kosch', 113, 'KORPSXKOSCH', 'New editorial lead: Corps Kosch, with an explicit separator.'),
    ('korpsfrisch', 113, 'KORPSFRISCH', 'Baertl comment39 reading, compared at the same position and length.'),
    ('body_with_kosch', 33,
     'KERTSCHXBRINGTENTENTEFLOTTEZWODIVISIONENXNEUSEELAENDERXENGLXUXFRANZOXMITXNUROHLXKORPSXKOSCHX',
     'Readable editorial segment; prefix and final reference remain unresolved. All costs are explicit.'),
]


def build_geometry(certificate):
    source = certificate['source']['ciphertext']
    insertions = certificate['correction_geometry']['insertions']
    ranks = certificate['key']['column_rank_order']
    square = certificate['key']['square']
    received, source_map = [], []
    for offset in range(len(source) + 1):
        for insertion in insertions:
            if insertion['original_index'] == offset:
                received.extend('?' * insertion['count'])
                source_map.extend([None] * insertion['count'])
        if offset < len(source):
            received.append(source[offset])
            source_map.append(offset)
    # Assign received positions to the corresponding row-major coordinates.
    order = [i for column in sorted(range(len(ranks)), key=ranks.__getitem__)
             for i in range(column, len(received), len(ranks))]
    interim = [None] * len(received)
    interim_to_received = [None] * len(received)
    for received_index, interim_index in enumerate(order):
        interim[interim_index] = received[received_index]
        interim_to_received[interim_index] = received_index
    domains = []
    for start in range(0, len(interim), 2):
        observed = ''.join(interim[start:start+2])
        allowed = ''.join(sorted(char for cell, char in enumerate(square)
                                if all(a == '?' or a == b for a, b in
                                       zip(observed, SYMBOLS[cell//6] + SYMBOLS[cell%6]))))
        domains.append(allowed)
    raw = ''.join(chars if len(chars) == 1 else '?' for chars in domains)
    assert raw == certificate['constraints']['raw_partial_plaintext']
    assert ''.join(received) == certificate['constraints']['augmented_ciphertext']
    return received, source_map, interim, interim_to_received, domains, raw


def inspect_segment(name, start, proposal, note, certificate, geometry):
    received, source_map, interim, interim_to_received, domains, raw = geometry
    square = certificate['key']['square']
    assert start + len(proposal) <= len(domains)
    substitutions, fills, character_changes = [], [], []
    repaired_interim = interim.copy()
    for offset, proposed in enumerate(proposal):
        position = start + offset
        cell = square.index(proposed)
        proposed_pair = SYMBOLS[cell//6] + SYMBOLS[cell%6]
        if proposed not in domains[position]:
            character_changes.append({'plaintext_index': position,
                                      'baseline_allowed_characters': domains[position],
                                      'proposed_character': proposed})
        for half in range(2):
            interim_index = 2 * position + half
            repaired_interim[interim_index] = proposed_pair[half]
            index = interim_to_received[interim_index]
            record = {'plaintext_index': position, 'proposed_character': proposed,
                      'coordinate_half': half,
                      'augmented_ciphertext_index': index,
                      'original_ciphertext_index': source_map[index],
                      'observed': received[index], 'proposed': proposed_pair[half]}
            if received[index] == '?':
                fills.append(record)
            elif received[index] != proposed_pair[half]:
                substitutions.append(record)
    repaired_received = received.copy()
    for interim_index, char in enumerate(repaired_interim):
        repaired_received[interim_to_received[interim_index]] = char
    decoded = []
    for position in range(len(domains)):
        pair = repaired_interim[2*position:2*position+2]
        decoded.append('?' if '?' in pair else square[6*SYMBOLS.index(pair[0]) + SYMBOLS.index(pair[1])])
    expected = raw[:start] + proposal + raw[start+len(proposal):]
    assert ''.join(decoded) == expected
    assert sum(a != '?' and a != b for a, b in zip(received, repaired_received)) == len(substitutions)
    return {'id': name, 'plaintext_start': start, 'plaintext_end_exclusive': start + len(proposal),
            'raw_segment': raw[start:start+len(proposal)], 'proposal': proposal,
            'note': note, 'incompatible_plaintext_positions': character_changes,
            'known_coordinate_substitutions': substitutions,
            'erased_coordinate_fills': fills,
            'partially_reencrypted_ciphertext': ''.join(repaired_received),
            'raw_plaintext_after_declared_segment_repair': expected,
            'counts': {'plaintext_length': len(proposal),
                       'incompatible_plaintext_positions': len(character_changes),
                       'known_coordinate_substitutions': len(substitutions),
                       'erased_coordinate_fills': len(fills),
                       'source_erasure_fills': sum(row['original_ciphertext_index'] is not None for row in fills),
                       'inserted_gap_fills': sum(row['original_ciphertext_index'] is None for row in fills)}}


def build():
    path = ROOT / 'data/certificates/p215.json'
    certificate = json.loads(path.read_text())
    geometry = build_geometry(certificate)
    segments = [inspect_segment(*segment, certificate, geometry) for segment in SEGMENTS]
    by_id = {segment['id']: segment for segment in segments}
    assert by_id['korps_kosch']['counts']['known_coordinate_substitutions'] == 2
    assert by_id['korpsfrisch']['counts']['known_coordinate_substitutions'] == 5
    assert by_id['body_with_kosch']['counts']['known_coordinate_substitutions'] == 9
    assert [(row['original_ciphertext_index'], row['observed'], row['proposed'])
            for row in by_id['korps_kosch']['known_coordinate_substitutions']] == [(22, 'X', 'V'), (193, 'D', 'X')]
    return {'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
            'status': 'Conditional editorial interpretation; not an exact historical decryption.',
            'source_certificate': str(path.relative_to(ROOT)),
            'source_certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'index_convention': 'All character and coordinate indices are zero-based; end positions are exclusive.',
            'key': certificate['key'], 'geometry': certificate['correction_geometry'],
            'raw_partial_plaintext': geometry[-1], 'segments': segments,
            'limits': ['The geometry remains Norbert comment32\'s two missing five-coordinate groups.',
                       'History may favor an interpretation but supplies no missing ciphertext symbols.',
                       'The Kosch proposal contradicts two known source coordinates and is therefore an editorial repair.',
                       'The two source changes are on the printed page; both inserted-gap fills remain unobserved.',
                       'The present audit compares fixed positions and does not search alternate error geometries.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check the frozen output without rewriting it.')
    args = parser.parse_args()
    result = build()
    output = HERE / 'interpretation_costs.json'
    if args.check:
        assert json.loads(output.read_text()) == result
    else:
        output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({row['id']: row['counts'] for row in result['segments']}, indent=2))
