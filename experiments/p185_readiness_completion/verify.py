#!/usr/bin/env python3
"""Check the p185 D truck and readiness clause against the original coordinates."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

CO = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def read(path):
    return json.loads((ROOT / path).read_text())


def source_order(length, ranks):
    """Original wire position for each position before transposition."""
    width = len(ranks)
    rows, extra = divmod(length, width)
    answer = [None] * length
    offset = 0
    for column in sorted(range(width), key=lambda c: ranks[c]):
        for row in range(rows + (column < extra)):
            answer[row * width + column] = offset
            offset += 1
    assert sorted(answer) == list(range(length))
    return answer


def inspect(wire, square, ranks, mapping):
    order = source_order(len(wire), ranks)
    spare = set(ALPHABET) - set(square)
    text, positions = [], []
    for at in range(0, len(wire), 2):
        indices = order[at:at + 2]
        pair = ''.join(wire[i] for i in indices)
        domain = set()
        for first in CO if pair[0] == '?' else pair[0]:
            for second in CO if pair[1] == '?' else pair[1]:
                label = square[6 * CO.index(first) + CO.index(second)]
                domain.update(spare if label == '?' else label)
        label = next(iter(domain)) if len(domain) == 1 else '?'
        text.append(label)
        positions.append({'plaintext_index': at // 2, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[i] for i in indices],
                          'label': label, 'domain': ''.join(sorted(domain))})
    text = ''.join(text)
    assert text == decrypt(wire, ranks, square)
    return text, positions


def frame(source, gap):
    mapping = list(range(gap)) + [None] * 5 + list(range(gap, len(source)))
    wire = ''.join(source[i] if i is not None and source[i] in CO else '?'
                   for i in mapping)
    return wire, mapping


def price(wire, mapping, stencil, square, ranks):
    _, positions = inspect(wire, square, ranks, mapping)
    changes, fills = [], []
    for label, position in zip(stencil, positions):
        if label == '?':
            continue
        cell = square.index(label)
        pair = CO[cell // 6] + CO[cell % 6]
        for model_index, expected in zip(position['model_indices'], pair):
            observed = wire[model_index]
            if observed == expected:
                continue
            entry = {'plaintext_index': position['plaintext_index'],
                     'source_index': mapping[model_index],
                     'model_index': model_index,
                     'before': observed, 'after': expected}
            (fills if observed == '?' else changes).append(entry)
    return changes, fills


def native_word(wire, mapping, square, ranks, word, record):
    text, positions = inspect(wire, square, ranks, mapping)
    start = text.index(word)
    support = positions[start:start + len(word)]
    assert all('?' not in p['pair'] and None not in p['source_indices']
               and p['domain'] == ch for p, ch in zip(support, word))
    return {'record': record, 'word': word, 'raw_reading': text,
            'plaintext_start': start, 'native_positions': support}


def build():
    spec = read('experiments/p185_readiness_completion/inputs.json')
    for path, digest in spec['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    old = read(spec['source_certificate'])
    source = old['source']['ciphertext']
    assert source == ''.join(old['source']['ciphertext_grouped'].split())
    assert len(source) == 193 and source[159] == 'Y'
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == spec['key_id'])
    square, ranks = key['square'], key['column_rank_order']
    wire, mapping = frame(source, spec['retained_gap'])
    assert wire == old['selected_geometry']['corrected_ciphertext']
    assert mapping == old['selected_geometry']['corrected_to_source_index']
    raw, positions = inspect(wire, square, ranks, mapping)
    assert raw == spec['expected_raw']
    target = list(raw)
    for phrase in spec['phrases']:
        a = phrase['start']
        b = a + len(phrase['before'])
        assert raw[a:b] == phrase['before']
        assert len(phrase['before']) == len(phrase['after'])
        target[a:b] = phrase['after']
    target = ''.join(target)
    assert target == spec['expected_edition']
    changes, fills = price(wire, mapping, target, square, ranks)
    actual_changes = sorted(({'source_index': c['source_index'],
                              'before': c['before'], 'after': c['after']}
                             for c in changes), key=lambda c: c['source_index'])
    assert actual_changes == spec['source_substitutions']
    assert len(changes) == 3 and len(fills) == 3
    assert [{'source_index': c['source_index'], 'literal': source[c['source_index']],
             'after': c['after']} for c in fills if c['source_index'] is not None] == spec['printed_glyph_fills']
    assert [{'model_index': c['model_index'], 'after': c['after']}
            for c in fills if c['source_index'] is None] == spec['inserted_slot_fills']
    edited = list(wire)
    for c in changes + fills:
        edited[c['model_index']] = c['after']
    edited = ''.join(edited)
    text, edited_positions = inspect(edited, square, ranks, mapping)
    assert text == target
    assert (len(raw) - raw.count('?'), len(text) - text.count('?')) == (91, 95)
    gains = [{**p, 'before': raw[p['plaintext_index']]}
             for p in edited_positions if raw[p['plaintext_index']] == '?' and p['label'] != '?']
    assert [p['plaintext_index'] for p in gains] == [22, 25, 49, 57]

    # The ordinary-word screen excludes the header, opening designation,
    # four numerical labels, closing command and signature.
    stencil = spec['body_stencil']
    assert len(stencil) == 99 and stencil[33:37] == '????'
    trials = []
    for gap in range(len(source) + 1):
        candidate, source_map = frame(source, gap)
        observed_changes, supplied = price(candidate, source_map, stencil, square, ranks)
        trials.append({'gap': gap, 'observed_substitutions': len(observed_changes),
                       'printed_glyph_fills': sum(c['source_index'] is not None for c in supplied),
                       'inserted_slot_fills': sum(c['source_index'] is None for c in supplied)})
    minimum = min(t['observed_substitutions'] for t in trials)
    minima = [t for t in trials if t['observed_substitutions'] == minimum]
    assert minimum == spec['expected_body_minimum']
    assert [t['gap'] for t in minima] == spec['expected_tied_gaps']

    # Native vocabulary witnesses under the same published key. They are not
    # treated as duplicate receptions of the target sentence.
    context = {r['source']['id']: r['source'] for r in old['direct_transport_context']}
    donors = []
    for rid, word in [('p198_C', 'LASTAUTO'), ('p196_B', 'BEREIT')]:
        donor = context[rid]
        literal = donor['raw_literal']
        native = ''.join(c if c in CO else '?' for c in literal)
        donors.append(native_word(native, list(range(len(native))), square, ranks, word, rid))
    departure = next(r for r in read('experiments/nov14_15_departure_and_supper/certificates.json')['records']
                     if r['id'] == 'p193_C')
    original = next(r for r in read('experiments/nov14_15_departure_and_supper/inputs.json')['records']
                    if r['id'] == 'p193_C')
    literal = ''.join(''.join(original['source_rows']).split())
    assert literal == departure['literal_source']
    native = ''.join(c if c in CO else '?' for c in literal)
    donors.append(native_word(native, list(range(len(native))), square, ranks, 'ABMARSCH', 'p193_C'))

    # A full injective square and arbitrary values for the three untouched
    # inserted coordinates provide a single compatibility witness.
    spare = iter(sorted(set(ALPHABET) - set(square)))
    full_square = ''.join(next(spare) if c == '?' else c for c in square)
    witness_wire = edited.replace('?', 'A')
    witness_text = decrypt(witness_wire, ranks, full_square)
    assert all(a == '?' or a == b for a, b in zip(target, witness_text))
    assert encrypt(witness_text, ranks, full_square) == witness_wire

    case = (ROOT / spec['case']).read_text()
    assert spec['readable_excerpt'] in case
    excerpt_labels = re.sub('[^A-Z0-9]', '', spec['readable_excerpt'].upper())
    assert excerpt_labels == (target[8:65] + target[92:]).replace('X', '')
    return {'schema': 'adfgvx-p185-readiness-v1', 'authors': spec['authors'],
            'input_sha256': hashlib.sha256((HERE / 'inputs.json').read_bytes()).hexdigest(),
            'indexing': 'Zero-based source, model and plaintext positions.',
            'record': spec['record'], 'published_key_id': spec['key_id'],
            'source': source, 'retained_gap': spec['retained_gap'],
            'model_to_source_indices': mapping, 'raw': raw, 'edition': text,
            'edition_ciphertext': edited, 'positions': 99, 'fixed_before': 91,
            'fixed_after': 95, 'source_substitutions': changes,
            'coordinate_fills': fills, 'new_fixed_positions': gains,
            'unresolved_positions': [p for p in edited_positions if p['label'] == '?'],
            'native_vocabulary_witnesses': donors,
            'gap_screen': {'stencil': stencil, 'minimum_observed_substitutions': minimum,
                           'retained_minima': minima, 'all_194_gaps': trials},
            'compatibility_witness': {'square': full_square, 'ciphertext': witness_wire,
                                      'plaintext': witness_text,
                                      'arbitrary_completions_are_not_readings': True},
            'source_visual_review': spec['source_visual_review'],
            'readable_excerpt': spec['readable_excerpt'], 'limits': spec['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('p185 D: LASTAUTOS / ABMARSCHBEREITSEIN; 91 -> 95/99; '
          '3 substitutions, 1 printed-glyph fill, 2 missing-slot fills; gaps52–55 retained.')


if __name__ == '__main__':
    main()
