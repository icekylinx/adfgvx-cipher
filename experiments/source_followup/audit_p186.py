#!/usr/bin/env python3
"""Independent arithmetic for the previously reported p186/p187 parallel.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The source is transcribed from the scan, not reconstructed from the desired text.
Only Python's standard library is needed.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parents[2]
COORDS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COMMENT53 = ('https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/'
             'the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-'
             'from-world-war-1/?all=1#comment-878079')


def mapping(length, ranks):
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    return [i for rank in range(1, width + 1)
            for i in range(ranks.index(rank), length, width)]


def inspect(raw, key):
    raw = ''.join(raw.split())
    text = ''.join(c if c in COORDS else '?' for c in raw)
    positions = mapping(len(text), key['column_rank_order'])
    intermediate = [''] * len(text)
    source_index = [None] * len(text)
    for i, target in enumerate(positions):
        intermediate[target] = text[i]
        source_index[target] = i
    assert len(intermediate) % 2 == 0
    square = key['square']
    unused = set(ALPHABET) - set(square)
    letters, domains, pairs, sources = [], [], [], []
    for offset in range(0, len(text), 2):
        pair = ''.join(intermediate[offset:offset+2])
        rows = range(6) if pair[0] == '?' else [COORDS.index(pair[0])]
        cols = range(6) if pair[1] == '?' else [COORDS.index(pair[1])]
        possible = set()
        for r in rows:
            for c in cols:
                value = square[6*r+c]
                possible.update(unused if value == '?' else value)
        domains.append(''.join(sorted(possible)))
        pairs.append(pair)
        sources.append(source_index[offset:offset+2])
        if '?' in pair:
            letters.append('?')
        else:
            letters.append(square[6*COORDS.index(pair[0])+COORDS.index(pair[1])])
    roundtrip = ''.join(intermediate[i] for i in positions)
    assert roundtrip == text
    for i, value in enumerate(letters):
        if value != '?':
            cell = square.index(value)
            assert COORDS[cell//6] + COORDS[cell%6] == pairs[i]
    return {'raw_source_grouped': raw, 'analysis_ciphertext': text,
            'source_slots': len(text),
            'known_coordinates': sum(c in COORDS for c in raw),
            'nonalphabetic_source_positions': [{'index': i, 'literal': c}
                                              for i, c in enumerate(raw) if c not in COORDS],
            'raw_plaintext': ''.join(letters), 'fixed_plaintext_positions': len(letters)-letters.count('?'),
            'plaintext_domains': domains, 'coordinate_pairs': pairs,
            'source_indices_per_plaintext_position': sources,
            'coordinate_reencryption': roundtrip,
            'coordinate_roundtrip_exact': True,
            'every_known_plaintext_pair_reencodes_exactly': True}


def encode(text, key):
    square = key['square']
    intermediate = ''.join(COORDS[square.index(c)//6] + COORDS[square.index(c)%6]
                           for c in text)
    return ''.join(intermediate[i] for i in mapping(len(intermediate), key['column_rank_order']))


def trial_suffix_equality(left_pairs, right_pairs, left_key, right_key, deletion, erased_value):
    """Check a stated deletion model under injective extensions of both squares.

    The only erased pair in this suffix has its first coordinate D observed;
    its six possible decoded letters all already occur in the attested square.
    All other uncertain suffix positions are fixed, distinct square-cell labels.
    """
    unknown_domains = {}
    def atoms(pairs, key, prefix):
        result = []
        for pair in pairs:
            if '?' in pair:
                assert pair == 'D?'
                result.append(('constant', erased_value))
            else:
                cell = 6*COORDS.index(pair[0])+COORDS.index(pair[1])
                value = key['square'][cell]
                if value != '?':
                    result.append(('constant', value))
                else:
                    label = prefix + ':' + pair
                    unknown_domains[label] = set(ALPHABET) - set(key['square'])
                    result.append(('variable', label))
        return result
    a = atoms(left_pairs, left_key, 'p186')
    b = atoms(right_pairs, right_key, 'p187')
    a = a[:deletion] + a[deletion+1:]
    assert len(a) == len(b)
    parent = {v: v for v in unknown_domains}
    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]
    constants = []
    for x, y in zip(a, b):
        if x[0] == y[0] == 'constant':
            if x[1] != y[1]:
                return False
        elif x[0] == y[0] == 'variable':
            parent[find(x[1])] = find(y[1])
        else:
            variable, constant = (x, y) if x[0] == 'variable' else (y, x)
            constants.append((variable[1], constant[1]))
    domains = {}
    members = {}
    for v, domain in unknown_domains.items():
        r = find(v)
        domains[r] = domains.get(r, set(ALPHABET)) & domain
        members.setdefault(r, []).append(v)
    for v, value in constants:
        domains[find(v)] &= {value}
    if any(not d for d in domains.values()):
        return False
    for variables in members.values():
        key_names = [v.split(':')[0] for v in variables]
        if len(key_names) != len(set(key_names)):
            return False
    order = sorted(domains, key=lambda v: len(domains[v]))
    used = {'p186': set(), 'p187': set()}
    def search(index):
        if index == len(order):
            return True
        v = order[index]
        key_names = [m.split(':')[0] for m in members[v]]
        for letter in sorted(domains[v]):
            if any(letter in used[k] for k in key_names):
                continue
            for k in key_names:
                used[k].add(letter)
            if search(index+1):
                return True
            for k in key_names:
                used[k].remove(letter)
        return False
    return search(0)


def build():
    keys = {x['id']: x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    messages = {x['id']: x for x in json.loads((ROOT/'data/messages.json').read_text())['messages']}
    key = keys['Nov13-15b']
    chi = keys['CHI-Nov13']
    baseline_path = ROOT/'data/reviews/p186_chi_parallel.json'
    baseline = {r['id']: r for r in json.loads(baseline_path.read_text())}
    conservative = {name: ''.join(r['ciphertext_grouped'].split()) for name, r in baseline.items()}
    # The scan's M-like/overstruck and Y-like glyphs are not silently accepted as V.
    a2 = list(conservative['p186_A2'])
    a2[20], a2[29] = 'M', 'Y'
    conservative['p186_A2'] = ''.join(a2)
    source = {name: inspect(raw, key) for name, raw in conservative.items()}
    target = {name: inspect(messages[name]['transcript']['analysis_ciphertext'], chi)
              for name in ['p187', 'p187b']}
    full_a1 = ('RUSSISCHENUNDPOLNHEEREVERKEHRVOLLERFASSENWICHTIGESBESONDAUSPOLN'
               'VERKEHRUEBEROHLSTATION')
    encoded = encode(full_a1, key)
    observed = source['p186_A1']['analysis_ciphertext']
    assert len(encoded) == len(observed)
    assert all(a == '?' or a == b for a, b in zip(observed, encoded))
    fills = [{'source_index': i, 'value': b} for i, (a, b) in enumerate(zip(observed, encoded)) if a == '?']
    # Compare exact source-backed word normalizations, without assigning new cells.
    supported = []
    for name, proposed in [
        ('p187', target['p187']['raw_plaintext'].replace('RUSSISCHET', 'RUSSISCHEN')),
        ('p187b', target['p187b']['raw_plaintext'].replace('NITHTARBEICET', 'NICHTARBEITET')),
    ]:
        raw = target[name]['raw_plaintext']
        edits = []
        for i, (old, new) in enumerate(zip(raw, proposed)):
            if old == new:
                continue
            cell = chi['square'].index(new)
            pair = COORDS[cell//6] + COORDS[cell%6]
            for half in range(2):
                if pair[half] != target[name]['coordinate_pairs'][i][half]:
                    edits.append({'source_index': target[name]['source_indices_per_plaintext_position'][i][half],
                                  'from': target[name]['coordinate_pairs'][i][half], 'to': pair[half],
                                  'plaintext_index': i, 'plaintext_from': old, 'plaintext_to': new})
        supported.append({'case': name, 'proposed_partial_plaintext': proposed,
                          'basis': 'The corresponding p186 words have these known square labels; source edits remain a hypothesis.',
                          'known_coordinate_changes': sorted(edits, key=lambda x: x['source_index'])})
    left = source['p186_A2']['coordinate_pairs'][78:]
    right = target['p187b']['coordinate_pairs'][63:]
    assert len(left) == 9 and len(right) == 8
    assert trial_suffix_equality(left, left[:-1], key, key, 8, 'X')
    conflict_control = left[:-1].copy()
    conflict_control[0] = 'DD'
    assert not trial_suffix_equality(left, conflict_control, key, key, 8, 'X')
    possibilities = list(source['p186_A2']['plaintext_domains'][79])
    assert possibilities == list('015FPX')
    ending_trials = []
    for deletion in range(9):
        values = [v for v in possibilities
                  if trial_suffix_equality(left, right, key, chi, deletion, v)]
        ending_trials.append({'deleted_p186_suffix_position': deletion,
                              'p186_plaintext_index': 78+deletion,
                              'compatible_erased_pair_values': values,
                              'injective_square_completion_exists': bool(values)})
    assert not any(row['injective_square_completion_exists'] for row in ending_trials)
    return {
        'format_version': 1, 'project': 'ADFGVX Cipher', 'authors': ['icekylinx', 'GPT-6 Astra Pro'],
        'source': {'printed_page': 186, 'pdf_page_1based': 189, 'section': 'A',
                   'url': 'https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view',
                   'header_literal': 'SU v LP (06.33 a.m., November 13th); 20.50 (13/11); 2 TLE',
                   'advertised_part_lengths': [170, 174],
                   'visual_review': 'Full page and enlarged source crop inspected. M-like/overstruck and Y-like A2 glyphs are masked in the conservative layer, not silently accepted as V.'},
        'prior_credit': {'relationship': 'Norbert, 2017-05-03, comment 53', 'url': COMMENT53,
                         'earlier_reading': 'Norbert says p186 had already been deciphered by the Lasry team; this review makes no first-reading claim.',
                         'current_contribution': 'Explicit source transcription, coordinate audit, word comparison and suffix-identity obstruction.'},
        'key_ids': [key['id'], chi['id']],
        'existing_source_record': {'path': 'data/reviews/p186_chi_parallel.json',
                                   'sha256': hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
                                   'p186_A1_independent_visual_transcription': 'Agrees exactly.',
                                   'p186_A2_conservative_differences': [
                                       {'source_index': 20, 'existing_value': 'V', 'visual_description': 'M-like or overstruck glyph', 'analysis_value': '?'},
                                       {'source_index': 29, 'existing_value': 'V', 'visual_description': 'Y-like glyph', 'analysis_value': '?'}]},
        'conservative_p186_A2': {k: source['p186_A2'][k] for k in
                                ['raw_plaintext', 'source_slots', 'known_coordinates',
                                 'fixed_plaintext_positions', 'coordinate_roundtrip_exact',
                                 'every_known_plaintext_pair_reencodes_exactly']},
        'p186_A1_conditional_erasure_fills': {'plaintext': full_a1, 'known_coordinate_changes': 0,
                                            'erasure_fills': fills, 'ciphertext': encoded,
                                            'support': 'The three restored letters occur in the corresponding p187 wording. Their transfer assumes this local word correspondence.'},
        'source_supported_word_proposals': supported,
        'suffix_comparison': {'p186_A2_start_plaintext_index': 78, 'p187b_start_plaintext_index': 63,
                              'p186_pairs': left, 'p187b_pairs': right,
                              'p186_partial_suffix': source['p186_A2']['raw_plaintext'][78:],
                              'p187b_partial_suffix': target['p187b']['raw_plaintext'][63:],
                              'model': 'Align after the shared NACHCHEF; delete exactly one of the nine p186 suffix characters; preserve every other source constraint and both injective partial squares.',
                              'all_deletion_trials': ending_trials,
                              'result': 'No compatible completion. The two suffixes cannot be equated in this model, so p186 numeral 1 cannot simply be copied into p187b unknown cells.',
                              'short_proof': [
                                  'Deleting suffix position 0 or 1 puts the known p186 numeral 1 against the known p187 separator X at position 1.',
                                  'Deleting position 2 makes the two occurrences of p187 cell VA at positions 5 and 7 equal the distinct known p186 characters 1 and X.',
                                  'Deleting any position 3 through 8 makes the first and third p187 suffix positions, both cell VD, equal p186 cell FV and its known numeral 1. FV cannot encode 1 because the same p186 square already assigns 1 to DD.'
                              ],
                              'positive_and_negative_controls_passed': True,
                              'limit': 'This does not rule out other alignments, additional reception errors, different references or other relationships.'},
        'summary': {'source_coordinates': 344, 'source_known_coordinates': 339,
                    'source_plaintext_positions': 172,
                    'source_fixed_plaintext_positions': sum(r['fixed_plaintext_positions'] for r in source.values()),
                    'p187_unknown_cells_newly_assigned': 0},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('p186_source_and_suffix_delta.json'))
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.verify:
        assert result == json.loads(args.output.read_text())
    else:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['summary']))
