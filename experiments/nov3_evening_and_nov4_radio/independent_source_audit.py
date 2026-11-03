#!/usr/bin/env python3
"""Independent p111/p112 source, copy and conditional-geometry audit.

Prepared by icekylinx and GPT-6 Astra Pro. No imports from the reviewed
verifier, shared cipher implementation or search engine. Standard library.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path

CO = 'ADFGVX'
MANUAL_ROWS = {'p112_A1': ['VAGDG VAVVA VDAVA VXAVF XAVFA XGAFV XVVGD GAAVA', 'DDDGG GGVGV AAXXV GAXAA AAAVV GXGVA DAAFG GVVDV', 'DGGGG XGCXV VXDAF DDGGA AFFVX DXADF DADXX FDGGA', 'XVVDD AXVFD ADFAG DAXAG VXDDD DFVGX GFDDV GXXGV', 'FAGDA AARVA DDAVD VDVDG DAGGD GAGGX XVGXX ADGAV', 'AX'], 'p112_A2': ['GDDGG FADGD XDDGG AXVVG GGFFD ADFXF DDFXD XDAAG', 'DGDGV GXADX AXDFA XDXXG FVAGD GAXDV DVGAG VADVG', 'VGXGV XGGVD AVDGG DVFGV ADVGV FXADG VGXGX GAGVV', 'DGDAD GDFDA DVFVV GAXXV GAFXA GAXXX GGVDG -----', '----- ----- ----- XXGVA XFAVF XXFAG GVFDF FXGVA', 'AVFVG DVGFD GXGVG VFF'], 'p112_A3': ['XDDDX DGGFF XAVXD DGAGA DXGVA ADXGD VAXXA -----', 'FFDAD XADFX XXDFV FAGAX DDVVF FDDXV DXXVG XDFRD', 'AVDVV XGDXA FVAFX FVGSX DXFXD DDF'], 'p112_B': ['AGXAD VXDVD GFFFG DAVAV FAADV AVGGA FAFDX DAXAA', 'AVXFX XAXFD GFFAF AAGGF AVVFV VXAXD XVVXA AXFFX', 'XFAXX GVAXV XXFGX XXADA AXXDD XAXGX XXFXV XFAVV', 'XDFAA AAXFF VFGVX AXFFF FAXAA FAVGX GXAFX XGFAV', 'GXDAF DFFXF XAXAD XVFVX XXFDF FVA'], 'p112_C': ['FVAXX DVAX FXGVV VAAFV AGFF VXFDV VVXVX ADAFG', 'VDFVX XXGDX XGGXX XFADV VVXDG FFGVD FFADX AVAXA', 'XAFXF XVXGF AAAXD FGXAA XAFGX AXGVA XX'], 'p112_D': ['AFXVX DFXVF VXDFA AXXXA FGVVF XGAAA XVDDX VXFGV', 'XVFXV XADDF XXDGA VG-AV FGFFA FGADG FAVVX XAAXA', '-VAXX XXVAG AFDVA XDXAX FFXGA GDFXV VGAGV FVDXX', 'VAXFG FGDXF XFAFG AVGGA XXFFA XAFVF GVFAV FXAFA', 'XADXV AAXFA FGXVF DXADX AFDAA XAVGV FGXVX AVGDA', 'FGXGD AFAAV DAAAG FDGFA XFFXX AXAVX'], 'p111_A1': ['VAGDG VAVVA VDAVA VXAVF XAVFA XGAFV XVVGD GAAVA', 'DDDGG GGVGV AAXXV GAXAA AAAVV GXGVA DAAFG GVVDV', 'DGGGG XGGXV ----- ----- ----- DXADF DADXX FDGGX', 'XVVDD AXVFD ADFAG DAXAG VXDDD DFVGX GFDDV GXXGV', 'FAGDA AAFVA DDAVD VDVDG DAGGD GAGGX XVGXX ADGGV', 'AX']}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten(rows):
    return ''.join(''.join(rows).split())


def decode(source, key):
    ranks, square = key['column_rank_order'], key['square']
    width = len(ranks)
    columns, origin_columns, offset = {}, {}, 0
    for col in sorted(range(width), key=ranks.__getitem__):
        count = (len(source) - col + width - 1) // width
        columns[col] = source[offset:offset + count]
        origin_columns[col] = list(range(offset, offset + count))
        offset += count
    middle = ''.join(columns[i % width][i // width] for i in range(len(source)))
    origins = [origin_columns[i % width][i // width] for i in range(len(source))]
    domains = []
    for i in range(0, len(middle), 2):
        pair = middle[i:i + 2]
        domain = ''.join(square[6 * r + c] for r in range(6) for c in range(6)
                         if (pair[0] not in CO or pair[0] == CO[r])
                         and (pair[1] not in CO or pair[1] == CO[c]))
        domains.append(domain)
    return {'plaintext': ''.join(d if len(d) == 1 else '?' for d in domains),
            'domains': domains, 'interim': middle, 'interim_source_indices': origins,
            'fixed_positions': sum(len(d) == 1 for d in domains), 'plaintext_positions': len(domains)}


def encrypt_template(text, key):
    square, ranks = key['square'], key['column_rank_order']
    middle = ''.join('??' if c == '?' else CO[square.index(c) // 6] + CO[square.index(c) % 6]
                     for c in text)
    ordering = sorted(range(len(middle)), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))
    return ''.join(middle[i] for i in ordering)


def price(record, key, text):
    target = encrypt_template(text, key)
    mapping = record['model_to_source_indices']
    source = record['analysis_source']
    framed = ''.join('?' if i is None else source[i] for i in mapping)
    assert len(target) == len(framed)
    working = list(framed)
    ledger = {'known_coordinate_substitutions': [], 'source_mask_fills': [], 'missing_coordinate_fills': []}
    for i, (before, after) in enumerate(zip(framed, target)):
        if after not in CO or before == after:
            continue
        item = {'model_index': i, 'source_index': mapping[i], 'before': before, 'after': after}
        if mapping[i] is None:
            ledger['missing_coordinate_fills'].append(item)
        elif before not in CO:
            ledger['source_mask_fills'].append(item)
        else:
            ledger['known_coordinate_substitutions'].append(item)
        working[i] = after
    return {'framed_source': framed, 'target_constraints': target,
            'cost': {k: len(v) for k, v in ledger.items()}, 'changes': ledger,
            'edited_frame': ''.join(working), 'edited_reading': decode(''.join(working), key)}


def c_geometry(record, key, certificate):
    source = record['analysis_source']
    assert len(source) == 110 and len(record['editorial_text']) == 61
    target = encrypt_template(record['editorial_text'], key)
    histogram, minimum, minima, distinct = Counter(), 999, [], set()
    evaluated = 0
    for first in range(5, 10):
        for second in range(19, 24):
            base = list(range(first)) + [None] + list(range(first, second)) + [None] + list(range(second, 110))
            assert len(base) == 112
            for left in range(113):
                for right in range(left, 113):
                    mapping = base[:left] + [None] * 5 + base[left:right] + [None] * 5 + base[right:]
                    inserted = tuple(i for i, original in enumerate(mapping) if original is None)
                    distinct.add(inserted)
                    mismatch = sum(target[j] in CO and source[original] != target[j]
                                   for j, original in enumerate(mapping) if original is not None)
                    histogram[mismatch] += 1
                    evaluated += 1
                    if mismatch < minimum:
                        minimum, minima = mismatch, []
                    if mismatch == minimum:
                        minima.append({'parameters': [first, second, left, right], 'inserted_model_indices': list(inserted)})
    bounded = certificate['bounded_family']
    assert evaluated == bounded.get('completed_parameter_configurations', bounded.get('completed_layouts')) == 161025
    if 'distinct_source_origin_layouts' in bounded:
        assert len(distinct) == bounded['distinct_source_origin_layouts']
    assert dict(histogram) == {int(k): v for k, v in bounded['cost_histogram'].items()}
    assert minimum == bounded['minimum_observed_substitutions'] == 1
    assert minima == bounded['all_minimum_layouts']
    # Independent bottom-up suffix DP: i source symbols and j missing target
    # symbols already consumed. Every one of (110+1)*(12+1) states is visited.
    n, missing = len(source), len(target) - len(source)
    best = [[10**9] * (missing + 1) for _ in range(n + 1)]
    counts = [[0] * (missing + 1) for _ in range(n + 1)]
    states = keep_transitions = missing_transitions = 0
    for i in range(n, -1, -1):
        for j in range(missing, -1, -1):
            states += 1
            if i == n and j == missing:
                best[i][j], counts[i][j] = 0, 1
                continue
            options = []
            if i < n:
                mismatch = int(target[i + j] in CO and source[i] != target[i + j])
                options.append((mismatch + best[i + 1][j], counts[i + 1][j]))
                keep_transitions += 1
            if j < missing:
                options.append((best[i][j + 1], counts[i][j + 1]))
                missing_transitions += 1
            best[i][j] = min(x[0] for x in options)
            counts[i][j] = sum(x[1] for x in options if x[0] == best[i][j])
    def enumerate_minima(i, j, inserted):
        if i == n and j == missing:
            return [inserted]
        out = []
        if i < n:
            mismatch = int(target[i + j] in CO and source[i] != target[i + j])
            if mismatch + best[i + 1][j] == best[i][j]:
                out += enumerate_minima(i + 1, j, inserted)
        if j < missing and best[i][j + 1] == best[i][j]:
            out += enumerate_minima(i, j + 1, inserted + [i + j])
        return out
    all_minima = enumerate_minima(0, 0, [])
    arbitrary = certificate['arbitrary_twelve_missing_coordinates']
    assert best[0][0] == arbitrary['minimum_observed_substitutions'] == 1
    assert counts[0][0] == len(all_minima) == arbitrary['optimal_layout_count'] == 8
    assert sorted(all_minima) == sorted(arbitrary['all_optimal_inserted_model_indices'])
    assert states == arbitrary['visited_dp_states'] == 1443
    return {'target': record['editorial_text'], 'source_slots': n, 'target_slots': len(target),
            'bounded_parameter_layouts_evaluated': evaluated,
            'distinct_source_origin_layouts': len(distinct),
            'parameter_layout_duplicate_count': evaluated - len(distinct),
            'cost_histogram': {str(k): histogram[k] for k in sorted(histogram)},
            'minimum_observed_substitutions': minimum, 'all_bounded_minima': minima,
            'arbitrary_missing_coordinate_minimum': best[0][0],
            'arbitrary_missing_coordinate_optima': all_minima,
            'measured_dp': {'states': states, 'keep_transitions': keep_transitions, 'missing_transitions': missing_transitions},
            'scope': 'Retrospective fixed-template source alignment; no free-wording or historical-mechanism uniqueness.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('independent_source_audit.json'))
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--geometry-only', action='store_true')
    args = parser.parse_args()
    path = args.repo / 'experiments/nov3_evening_and_nov4_radio'
    inp = json.loads((path / 'inputs.json').read_text())
    cert = json.loads((path / 'certificates.json').read_text())
    assert cert['inputs_sha256'] == sha(path / 'inputs.json')
    keys = {k['id']: k for k in inp['keys']}
    records = {r['id']: r for r in inp['records']}
    certificates = {r['id']: r for r in cert['records']}
    geometry = c_geometry(records['p112_C'], keys[records['p112_C']['key_id']], cert['conditional_C_geometry'])
    if args.geometry_only:
        print(json.dumps({k: v for k, v in geometry.items() if k not in ['cost_histogram', 'arbitrary_missing_coordinate_optima']}, indent=2))
        return
    checked = []
    for id, record in records.items():
        assert record['rows'] == MANUAL_ROWS[id]
        literal = flatten(MANUAL_ROWS[id])
        assert literal == record['literal_source']
        assert ''.join(c if c in CO else '?' for c in literal) == record['analysis_source']
        mapping = record['model_to_source_indices']
        assert [i for i in mapping if i is not None] == list(range(len(literal)))
        key = keys[record['key_id']]
        priced = price(record, key, record['editorial_text'])
        raw = decode(priced['framed_source'], key)
        assert raw['plaintext'] == record['expected_raw'] == certificates[id]['raw_reading']['plaintext']
        assert raw['interim_source_indices'] == certificates[id]['raw_reading']['interim_source_indices']
        assert [set(d) for d in raw['domains']] == [set(d) for d in certificates[id]['raw_reading']['domains']]
        assert priced['edited_reading']['plaintext'] == record['editorial_text'] == certificates[id]['edited_reading']['plaintext']
        assert priced['cost'] == record['expected_cost'] == certificates[id]['cost']
        assert [set(d) for d in priced['edited_reading']['domains']] == [set(d) for d in certificates[id]['edited_reading']['domains']]
        checked.append({'id': id, 'source_slots': len(literal), 'valid_source_coordinates': sum(c in CO for c in literal),
                        'model_slots': len(mapping), 'inserted_coordinates': mapping.count(None),
                        'raw': raw['plaintext'], 'edited': record['editorial_text'],
                        'raw_fixed_positions': raw['fixed_positions'], 'edited_fixed_positions': priced['edited_reading']['fixed_positions'],
                        'cost': priced['cost'], 'changes': priced['changes']})
    first, second = records['p111_A1']['analysis_source'], records['p112_A1']['analysis_source']
    conflicts = [i for i, (a, b) in enumerate(zip(first, second)) if a in CO and b in CO and a != b]
    fills = [i for i, (a, b) in enumerate(zip(first, second)) if (a in CO) != (b in CO)]
    same = sum(a in CO and b in CO and a == b for a, b in zip(first, second))
    assert conflicts == [119, 198] and len(fills) == 17 and same == 183
    copy_candidates = []
    for choices in itertools.product(*[(first[i], second[i]) for i in conflicts]):
        common = [a if a in CO else b for a, b in zip(first, second)]
        for i, choice in zip(conflicts, choices):
            common[i] = choice
        common = ''.join(common)
        costs = [sum(a in CO and a != b for a, b in zip(source, common)) for source in [first, second]]
        copy_candidates.append({'conflict_choices': list(choices), 'plaintext': decode(common, keys['Nov1-3'])['plaintext'],
                                'ciphertext': common, 'observed_substitution_costs': costs})
    assert copy_candidates == cert['copy_audit']['all_minimum_common_streams']
    assert all(sum(c['observed_substitution_costs']) == 2 for c in copy_candidates)
    a2 = records['p112_A2']
    alternatives = []
    for word in ['FAHRZEUG', 'FLUGZEUG']:
        text = a2['editorial_text'].replace('FLUGZEUG', word).replace('FAHRZEUG', word)
        priced = price(a2, keys[a2['key_id']], text)
        assert priced['edited_reading']['plaintext'] == text
        alternatives.append({'word': word, 'template': text, 'cost': priced['cost'], 'changes': priced['changes']})
    assert [a['cost']['known_coordinate_substitutions'] for a in alternatives] == [6, 10]
    assert all(a['cost']['source_mask_fills'] == 18 for a in alternatives)
    total = {'physical_records': len(checked), 'source_slots': sum(r['source_slots'] for r in checked),
             'valid_source_coordinates': sum(r['valid_source_coordinates'] for r in checked),
             'analysis_frame_slots': sum(r['model_slots'] for r in checked),
             'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in checked),
             'edited_fixed_positions': sum(r['edited_fixed_positions'] for r in checked),
             'known_coordinate_substitutions': sum(r['cost']['known_coordinate_substitutions'] for r in checked),
             'source_mask_fills': sum(r['cost']['source_mask_fills'] for r in checked),
             'missing_coordinate_fills': sum(r['cost']['missing_coordinate_fills'] for r in checked)}
    assert all(cert['summary'][k] == v for k, v in total.items())
    out = {'schema': 'adfgvx-nov3-evening-independent-audit-v1', 'authors': ['icekylinx', 'GPT-6 Astra Pro'],
           'inputs_sha256': sha(path / 'inputs.json'), 'certificates_sha256': sha(path / 'certificates.json'),
           'source_images_reviewed': [{'path': str((path / 'sources' / name).relative_to(args.repo)), 'sha256': sha(path / 'sources' / name)}
                                      for name in ['p111_A1_detail.png', 'p112_A_detail.png', 'p112_C_detail.png', 'p112_full.png', 'p112_D_detail.png']],
           'manual_source_rows': MANUAL_ROWS, 'records': checked, 'summary': total,
           'source_copy_check': {'same_valid_coordinates': same, 'complementary_erasure_positions': fills,
                                 'observed_conflicts': conflicts, 'all_four_minimum_common_streams': copy_candidates},
           'A2_word_alternatives': alternatives, 'C_geometry': geometry,
           'findings': ['All seven source row transcriptions agree with independent visual reading.',
                        'The copies supply seventeen missing coordinate values but retain two observed conflicts; all four equal-combined-cost common streams survive.',
                        'FAHRZEUG uses six observed substitutions versus ten for FLUGZEUG, with eighteen equal source-mask fills and the same two unresolved date positions.',
                        'C contains110 observed coordinates and advertises122. DVAX and AGFF are visibly four-character groups; no printed marker establishes a missing ten-coordinate prefix.',
                        'The chosen C geometry retains all observed coordinates, adds12 model slots, fills11, and leaves the ?400 field unresolved.',
                        'A3 repeated TLICH and4X4?X4X11, A1 repeated219219/5353, and D closingBVNXBEIBVGX7OSPOLIX? remain literal.'],
           'limits': ['Fixed-template alignment costs are retrospective compatibility results, not unique language or historical mechanism proofs.',
                      'Source copies are two physical witnesses; their exact transmission lineage is not proved by textual agreement alone.'],
           'verified': True}
    if args.verify:
        assert out == json.loads(args.output.read_text())
    else:
        args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'verified': True, 'summary': total,
                      'C_parameter_layouts': geometry['bounded_parameter_layouts_evaluated'],
                      'C_distinct_source_origin_layouts': geometry['distinct_source_origin_layouts'],
                      'C_arbitrary_minima': len(geometry['arbitrary_missing_coordinate_optima']),
                      'A2_costs': {a['word']: a['cost'] for a in alternatives}}, indent=2))


if __name__ == '__main__':
    main()
