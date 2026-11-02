#!/usr/bin/env python3
"""Propagate independently declared late-period label hypotheses.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The earlier literal transcripts, keys and editorial costs remain unchanged.
This verifier supplies a separate partial-square interpretation and a globally
consistent roundtrip witness; it never fills a key by reading one target word.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

CO = 'ADFGVX'
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
DEPENDENCIES = [
    'data/certificates/p215.json',
    'experiments/operational_recovery/inputs.json',
    'experiments/open_targets_continuation/inputs.json',
    'experiments/corpus_extension/certificates.json',
]


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def clean(text):
    return ''.join(c if c in CO else '?' for c in text)


def interpreted_squares(base, definition):
    """Clear all unproved labels before assigning one injective partial map."""
    ambiguous = definition['ambiguous_baseline_labels']
    assert set(ambiguous) <= set(base)
    square = ['?' if c in ambiguous else c for c in base]
    assignments = {}
    result = []
    for layer in definition['layers']:
        for old, new in layer['assignments'].items():
            assert old in ambiguous and old not in assignments
            assert new in AL and new not in square
            square[base.index(old)] = new
            assignments[old] = new
        value = ''.join(square)
        assert len(value) == 36
        assert len(set(value) - {'?'}) == 36 - value.count('?')
        result.append(dict(id=layer['id'], square=value,
                           assignments=dict(assignments),
                           remaining_symbols=''.join(sorted(set(AL)-set(value)))))
    return result


def independent_read(source, ranks, square, source_map):
    """Construct physical column offsets without importing untranspose."""
    n, width = len(source), len(ranks)
    assert n % 2 == 0 and sorted(ranks) == list(range(1, width+1))
    heights = [n//width + (c < n % width) for c in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[c])
              for c in range(width)]
    indices = [starts[p % width]+p//width for p in range(n)]
    assert sorted(indices) == list(range(n))
    unused = set(AL)-set(square)
    positions = []
    for i in range(n//2):
        pair_indices = indices[2*i:2*i+2]
        pair = ''.join(source[j] for j in pair_indices)
        cells = [a*6+b for a in range(6) for b in range(6)
                 if pair[0] in ('?', CO[a]) and pair[1] in ('?', CO[b])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        positions.append(dict(plaintext_index=i, pair=pair,
                              source_indices=[source_map[j] for j in pair_indices],
                              domain=''.join(sorted(domain))))
    raw = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in positions)
    assert raw == decrypt(source, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(source, ranks, square)
    return raw, positions


def records():
    p215 = read(DEPENDENCIES[0])
    source = p215['source']['ciphertext']
    frame, mapping = [], []
    for index in range(len(source)+1):
        for insertion in p215['correction_geometry']['insertions']:
            if index == insertion['original_index']:
                frame.extend('?'*insertion['count'])
                mapping.extend([None]*insertion['count'])
        if index < len(source):
            frame.append(source[index])
            mapping.append(index)
    assert ''.join(frame) == p215['constraints']['augmented_ciphertext']
    yield dict(id='p215_norbert32', key_id='Nov22-24', cipher=''.join(frame),
               source_map=mapping, original=source, baseline=p215['constraints']['raw_partial_plaintext'],
               interpretation='Norbert 2017 two-gap geometry; no new source repair',
               source_coordinate_edits=[])
    earlier = read(DEPENDENCIES[2])
    record = next(r for r in earlier['messages'] if r['id'] == 'p214_B')
    literal = ''.join(''.join(record['source_rows']).split())
    source = clean(literal)
    yield dict(id=record['id'], key_id=record['key_id'], cipher=source,
               source_map=list(range(len(source))), original=source,
               baseline=record['expected_raw'], source_coordinate_edits=[],
               interpretation='Unchanged source; earlier quotation repairs are not applied here')
    extension = read(DEPENDENCIES[3])
    keys = read(DEPENDENCIES[1])['keys']
    for record in extension['records']:
        if record['id'] not in ('p227_B', 'p226_B2'):
            continue
        assert record['model']['kind'] == 'identity'
        source = clean(record['literal'])
        common = dict(key_id=record['key_id'], source_map=list(range(len(source))),
                      original=source)
        yield dict(id=record['id']+'_raw', cipher=source, baseline=record['raw'],
                   source_coordinate_edits=[], interpretation='Unchanged source', **common)
        proposal = next(p for p in record['editorial_candidates'] if p['id'] == 'readable')
        key = keys[record['key_id']]
        encoded = encrypt(proposal['plaintext'], key['column_rank_order'], key['square'])
        edits = [dict(source_index=i, before=a, after=b)
                 for i, (a,b) in enumerate(zip(source, encoded)) if a != b]
        expected = [dict(source_index=e['source_index'], before=e['from'], after=e['to'])
                    for e in proposal['known_coordinate_substitutions']]
        assert edits == expected
        assert not proposal['source_erasure_fills'] and not proposal['model_inserted_slot_fills']
        yield dict(id=record['id']+'_earlier_word_repairs', cipher=encoded,
                   baseline=proposal['plaintext'], source_coordinate_edits=edits,
                   interpretation='Only the previously certified ordinary-word repairs', **common)


def build():
    inputs = read(DEPENDENCIES[1])
    squares = {name: interpreted_squares(inputs['keys'][name]['square'], definition)
               for name, definition in inputs['interpretation_layers'].items()}
    results = []
    for record in records():
        key = inputs['keys'][record['key_id']]
        ranks = key['column_rank_order']
        baseline, _ = independent_read(record['cipher'], ranks, key['square'], record['source_map'])
        assert baseline == record['baseline']
        interpretations = []
        for layer in squares[record['key_id']]:
            raw, positions = independent_read(record['cipher'], ranks, layer['square'], record['source_map'])
            events = []
            for p in positions:
                if '?' in p['pair']:
                    continue
                cell = 6*CO.index(p['pair'][0])+CO.index(p['pair'][1])
                old = key['square'][cell]
                if old in layer['assignments']:
                    assert p['domain'] == layer['assignments'][old]
                    events.append(dict(**p, baseline_label=old))
            unused = iter(sorted(set(AL)-set(layer['square'])))
            completion = ''.join(next(unused) if c == '?' else c for c in layer['square'])
            assert set(completion) == set(AL)
            filled = record['cipher'].replace('?', 'A')
            text = decrypt(filled, ranks, completion)
            assert encrypt(text, ranks, completion) == filled
            assert all(c in p['domain'] for c,p in zip(text,positions))
            assert all(a == '?' or a == b for a,b in zip(record['cipher'],filled))
            interpretations.append(dict(layer=layer['id'], square=layer['square'],
                conditional_plaintext=raw, fixed_positions=sum(c!='?' for c in raw),
                propagated_assignments=events,
                witness=dict(square=completion,filled_ciphertext=filled,plaintext=text,
                             is_proposed_historical_reading=False)))
        results.append(dict(id=record['id'], key_id=record['key_id'],
                            interpretation=record['interpretation'],
                            source_coordinate_edits=record['source_coordinate_edits'],
                            baseline=baseline, interpretations=interpretations))
    indexed={r['id']:r for r in results}
    assert indexed['p215_norbert32']['interpretations'][0]['conditional_plaintext'][-4:] == '?1?6'
    assert 'AOK11' in indexed['p214_B']['interpretations'][0]['conditional_plaintext']
    assert indexed['p227_B_earlier_word_repairs']['interpretations'][-1]['conditional_plaintext'] == (
        'BITTEFUNKSPRUECHEAN11XARMEEUNDUNTERSTELLTEFORMATIONENUNMITTELBARANZOENGEBENX')
    # The two unresolved footer cells are distinct, so their labels cannot be
    # chosen independently with repetition. Exhibit every ordered assignment.
    target = next(r for r in records() if r['id'] == 'p215_norbert32')
    layer = squares['Nov22-24'][0]
    base = inputs['keys']['Nov22-24']['square']
    ranks = inputs['keys']['Nov22-24']['column_rank_order']
    _, positions = independent_read(target['cipher'], ranks, layer['square'], target['source_map'])
    assert all('?' not in p['pair'] and None not in p['source_indices'] for p in positions[-4:])
    footer_values = []
    for a,b in itertools.permutations(layer['remaining_symbols'],2):
        candidate = list(layer['square'])
        candidate[base.index('3')], candidate[base.index('5')] = a,b
        unused = iter(sorted(set(AL)-set(candidate)))
        candidate = ''.join(next(unused) if c == '?' else c for c in candidate)
        filled = target['cipher'].replace('?','A')
        text = decrypt(filled,ranks,candidate)
        assert text[-4:] == a+'1'+b+'6'
        assert encrypt(text,ranks,candidate) == filled
        footer_values.append(text[-4:])
    assert len(footer_values) == len(set(footer_values)) == 90
    numeric = [x for x in footer_values if x.isdecimal()]
    assert len(numeric) == 42
    footer = dict(pattern='a1b6', a_and_b_domain=layer['remaining_symbols'],
                  distinct_a_and_b=True, source_positions=positions[-4:],
                  all_90_assignments_have_global_source_preserving_witnesses=True,
                  possible_values=footer_values,
                  additional_all_four_characters_are_digits_assumption=dict(
                      possible_values=numeric, count=len(numeric), leading_zero_allowed=True))
    return dict(schema='adfgvx-late-key-propagation-v1', authors='icekylinx and GPT-6 Astra Pro',
                indexing='Zero-based plaintext and source indices; null is an earlier inserted gap.',
                dependency_sha256={p:sha(p) for p in DEPENDENCIES},
                conditional_squares=squares, records=results, p215_footer=footer,
                limits=[
                    'Historical formation identifications and lexical/separator assumptions remain optional.',
                    'The earlier published key files and raw source transcripts are unchanged.',
                    'Cleared labels share one global unused-symbol pool; per-position domains are not independent.',
                    'A witness is one arbitrary consistent square/erasure completion, not recovered historical text.',
                    'The p215 gap geometry and all unresolved source coordinates remain exactly as before.',
                ])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    result=build(); path=HERE/'certificate.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result,indent=2)+'\n')
    for row in result['records']:
        print(row['id'], row['interpretations'][-1]['conditional_plaintext'])
    print('All propagated partial-square domains and global roundtrip witnesses agree.')


if __name__=='__main__':
    main()
