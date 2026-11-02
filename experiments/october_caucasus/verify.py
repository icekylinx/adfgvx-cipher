#!/usr/bin/env python3
"""Source-preserving October editions; icekylinx and GPT-6 Astra Pro.

Rebuilds letter domains and explicit editorial repair certificates by an
independent column-offset inverse, then compares it with adfgvx.cipher.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

COORD = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def raw_coordinates(record):
    literal = ''.join(' '.join(record['rows']).split()).replace('(', '').replace(')', '')
    assert literal == record['literal_source']
    masked = ''.join(c if c in COORD else '?' for c in literal)
    assert masked == record['analysis_source']
    return literal, masked


def apply_layout(source, model):
    excluded = set()
    for lo, hi in model['deletions']:
        assert 0 <= lo < hi <= len(source)
        assert not (excluded & set(range(lo, hi)))
        excluded.update(range(lo, hi))
    insertions = {}
    for insertion in model['insertions']:
        position = insertion['before_source']
        assert 0 <= position <= len(source) and position not in insertions
        assert insertion['symbols'] and set(insertion['symbols']) <= set(COORD + '?')
        insertions[position] = insertion['symbols']
    chars, origins = [], []
    for i in range(len(source) + 1):
        for c in insertions.get(i, ''):
            chars.append(c)
            origins.append(None)
        if i < len(source) and i not in excluded:
            chars.append(source[i])
            origins.append(i)
    return ''.join(chars), origins


def inverse_offsets(ciphertext, ranks):
    """Map each interim coordinate to its ciphertext offset independently."""
    width, length = len(ranks), len(ciphertext)
    assert sorted(ranks) == list(range(1, width + 1))
    assert length % 2 == 0
    heights = [length // width + (c < length % width) for c in range(width)]
    bases = []
    for c in range(width):
        bases.append(sum(heights[d] for d in range(width) if ranks[d] < ranks[c]))
    offsets = [bases[i % width] + i // width for i in range(length)]
    assert sorted(offsets) == list(range(length))
    return offsets


def decode_model(record, model, key):
    _, source = raw_coordinates(record)
    ciphertext, origins = apply_layout(source, model)
    offsets = inverse_offsets(ciphertext, key['column_rank_order'])
    stream = ''.join(ciphertext[i] for i in offsets)
    assert stream == untranspose(ciphertext, key['column_rank_order'])
    square = key['square']
    domains, pairs = [], []
    for i in range(0, len(stream), 2):
        pair = stream[i:i + 2]
        rows = [COORD.index(pair[0])] if pair[0] in COORD else range(6)
        columns = [COORD.index(pair[1])] if pair[1] in COORD else range(6)
        domains.append(''.join(sorted(square[6*r+c] for r in rows for c in columns)))
        pairs.append({'pair': pair, 'layout_offsets': offsets[i:i+2],
                      'source_offsets': [origins[j] for j in offsets[i:i+2]]})
    assert domains == plaintext_domains(ciphertext, key['column_rank_order'], square)
    raw = ''.join(d if len(d) == 1 else '?' for d in domains)
    assert raw == decrypt(ciphertext, key['column_rank_order'], square)
    proposal = record['editorial_template']
    assert len(proposal) == len(domains) and set(proposal) <= set(ALPHABET + '?')
    # A complete witness fills only otherwise unconstrained erasures with A.
    # This arbitrary filler is never presented as recovered plaintext.
    witness = list(ciphertext.replace('?', 'A'))
    edits, fills = [], []
    for position, char in enumerate(proposal):
        if char == '?':
            continue
        cell = square.index(char)
        expected_pair = COORD[cell // 6] + COORD[cell % 6]
        for half, expected in enumerate(expected_pair):
            offset = offsets[2*position + half]
            observed = ciphertext[offset]
            item = {'layout_offset': offset, 'source_offset': origins[offset],
                    'plaintext_position': position, 'observed': observed,
                    'proposed': expected}
            if observed == '?':
                fills.append(item)
            elif observed != expected:
                edits.append(item)
            witness[offset] = expected
    witness = ''.join(witness)
    witness_plaintext = decrypt(witness, key['column_rank_order'], square)
    assert encrypt(witness_plaintext, key['column_rank_order'], square) == witness
    assert all(a == '?' or a == b for a, b in zip(proposal, witness_plaintext))
    changed = {x['layout_offset'] for x in edits + fills}
    assert all(a == b or a == '?' or i in changed for i, (a, b) in enumerate(zip(ciphertext, witness)))
    # Modelled omissions, source erasures and asserted substitutions are distinct.
    return {'id': model['id'], 'layout_length': len(ciphertext),
            'layout_ciphertext': ciphertext, 'layout_source_offsets': origins,
            'raw_plaintext': raw, 'fixed_positions': sum(len(d) == 1 for d in domains),
            'plaintext_positions': len(domains), 'domains': domains, 'pairs': pairs,
            'deleted_source_slots': sum(hi-lo for lo, hi in model['deletions']),
            'inserted_slots': sum(len(x['symbols']) for x in model['insertions']),
            'editorial_template': proposal, 'known_coordinate_substitutions': edits,
            'erasure_fills': fills,
            'editorial_counts': {'substitutions': len(edits), 'fills': len(fills)},
            'arithmetic_witness_ciphertext': witness,
            'arithmetic_witness_plaintext': witness_plaintext,
            'witness_warning': 'Unasserted erased slots use arbitrary A coordinates only for the roundtrip check.'}


def rebuild(inputs):
    key = inputs['key']
    assert sorted(key['square']) == sorted(ALPHABET)
    current = next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys'] if k['id'] == key['id'])
    assert current == key, 'Published key snapshot changed'
    for crop in inputs['source']['images']:
        assert digest(HERE/crop['path']) == crop['sha256'], crop['path']
    records = []
    for record in inputs['records']:
        literal, source = raw_coordinates(record)
        models = [decode_model(record, model, key) for model in record['layout_models']]
        length = models[0]['plaintext_positions']
        assert all(m['plaintext_positions'] == length for m in models)
        union = [''.join(sorted(set().union(*(set(m['domains'][i]) for m in models))))
                 for i in range(length)]
        common = ''.join(d if len(d) == 1 else '?' for d in union)
        best_cost = min(m['editorial_counts']['substitutions'] for m in models)
        best_models = [m['id'] for m in models if m['editorial_counts']['substitutions'] == best_cost]
        records.append({'id': record['id'], 'source_slots': len(source),
                        'known_source_coordinates': sum(c in COORD for c in source),
                        'source_erased_slots': source.count('?'),
                        'advertised_length': record['advertised_length'],
                        'models': models, 'all_model_union_domains': union,
                        'all_model_common_template': common,
                        'all_model_common_fixed_positions': sum(len(d) == 1 for d in union),
                        'minimum_editorial_known_substitutions': best_cost,
                        'minimum_cost_model_ids': best_models})
    by_id = {r['id']: r for r in records}
    # The strikeout is an exact repeated 25-coordinate run.
    s = next(r for r in inputs['records'] if r['id'] == 'p72_A1')['analysis_source']
    assert s[120:145] == s[145:170]
    # The unmarked repeated p72 run has one invalid source letter, no
    # contradictory pair of known coordinates.
    r = next(r for r in inputs['records'] if r['id'] == 'p72_A2')
    a, b = r['analysis_source'][110:135], r['analysis_source'][135:160]
    assert len(a) == len(b) == 25
    assert sum(x != y for x, y in zip(a, b)) == 1
    assert all(x == y or '?' in (x,y) for x,y in zip(a,b))
    # Two independent exact five-coordinate repeats, not arbitrary score-led cuts.
    s = next(r for r in inputs['records'] if r['id'] == 'p70_A1')['analysis_source']
    assert s[235:240] == s[240:245] == 'AAAAA'
    assert s[275:280] == s[280:285] == 'DAAGG'
    assert len({m['layout_ciphertext'] for m in by_id['p70_A1']['models']}) == 1
    # Check short source groups and every declared one-slot placement.
    s = next(r for r in inputs['records'] if r['id'] == 'p69_B1')['analysis_source']
    assert s[300:304] == 'VXFX'
    s = next(r for r in inputs['records'] if r['id'] == 'p69_B2')['analysis_source']
    assert s[45:49] == 'XFFF'
    for message_id, boundaries in [('p69_B1',range(300,305)),('p69_B2',range(45,50))]:
        r = next(r for r in inputs['records'] if r['id'] == message_id)
        assert [m['insertions'][0]['before_source'] for m in r['layout_models']] == list(boundaries)
    unresolved = []
    for r in inputs.get('unresolved_continuations', []):
        source = ''.join(' '.join(r['rows']).split())
        assert source == r['literal_source'] and set(source) <= set(COORD)
        assert len(source) < r['advertised_length']
        padded = source + '?' * (r['advertised_length'] - len(source))
        domains = plaintext_domains(padded, key['column_rank_order'], key['square'])
        unresolved.append({'id': r['id'], 'surviving_slots': len(source),
            'hypothesis': 'Unobserved suffix padded to the advertised length.',
            'added_erased_slots': padded.count('?'), 'domains': domains,
            'fixed_plaintext_positions': sum(len(d) == 1 for d in domains),
            'accepted_plaintext': None})
    assert len(unresolved) == 1 and unresolved[0]['id'] == 'p71_A2'
    assert unresolved[0]['surviving_slots'] == 85
    assert unresolved[0]['added_erased_slots'] == 107
    assert unresolved[0]['fixed_plaintext_positions'] == 0
    return {'schema': 'adfgvx-october-caucasus-certificate-v1',
            'prepared_by': inputs['prepared_by'],
            'inputs_sha256': digest(HERE/'inputs.json'),
            'source_slots_total': sum(r['source_slots'] for r in records),
            'records': records, 'unresolved_continuations': unresolved}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE/'inputs.json').read_text())
    if args.pdf:
        assert digest(args.pdf) == inputs['source']['pdf_sha256']
    result = rebuild(inputs)
    destination = HERE/'certificates.json'
    if args.verify:
        assert json.loads(destination.read_text()) == result, 'Certificate mismatch'
    else:
        destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    for record in result['records']:
        print(record['id'], 'raw common', record['all_model_common_fixed_positions'],
              '/', len(record['all_model_common_template']),
              'editorial minimum substitutions', record['minimum_editorial_known_substitutions'],
              'models', len(record['models']))
    print('Verified' if args.verify else 'Wrote', len(result['records']), 'source records;',
          result['source_slots_total'], 'literal slots')


if __name__ == '__main__':
    main()
