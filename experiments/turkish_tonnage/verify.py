#!/usr/bin/env python3
"""Verify the three-part Turkish-tonnage sale instruction and all source repairs.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No published substitution square or numerical label is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permutation(length, ranks):
    """Independent column-offset inverse: interim index -> model index."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (i < length % width) for i in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[i])
              for i in range(width)]
    order = [starts[i % width] + i // width for i in range(length)]
    assert sorted(order) == list(range(length))
    return order


def inspect(cipher, key, mapping):
    square, ranks = key['square'], key['column_rank_order']
    assert len(cipher) % 2 == 0 and len(mapping) == len(cipher)
    order = permutation(len(cipher), ranks)
    middle = ''.join(cipher[j] for j in order)
    assert middle == untranspose(cipher, ranks)
    unused = set(A) - set(square)
    positions = []
    for i in range(len(cipher) // 2):
        pair = middle[2*i:2*i+2]
        cells = [6*r+c for r in range(6) for c in range(6)
                 if pair[0] in ('?', C[r]) and pair[1] in ('?', C[c])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        indices = order[2*i:2*i+2]
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices],
                          'domain': domain,
                          'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    return {'raw': raw, 'fixed_positions': sum(p['raw'] != '?' for p in positions),
            'positions': positions}


def masked_encryption(template, key):
    square = key['square']
    middle = ''.join('??' if ch == '?' else C[square.index(ch)//6] + C[square.index(ch) % 6]
                     for ch in template)
    target = [None] * len(middle)
    for ch, i in zip(middle, permutation(len(middle), key['column_rank_order'])):
        target[i] = ch
    return ''.join(target)


def repair(template, base, key, mapping, literal):
    assert len(template)*2 == len(base)
    stencil = masked_encryption(template, key)
    target = ''.join(a if b == '?' else b for a, b in zip(base, stencil))
    result = inspect(target, key, mapping)
    assert result['raw'] == template
    substitutions, fills = [], []
    for i, (a, b) in enumerate(zip(base, target)):
        if a == b:
            continue
        source_i = mapping[i]
        event = {'model_index': i, 'source_index': source_i,
                 'printed': literal[source_i] if source_i is not None else None,
                 'from': a, 'to': b}
        (fills if a == '?' else substitutions).append(event)
    rebuilt = list(base)
    for event in substitutions + fills:
        rebuilt[event['model_index']] = event['to']
    assert ''.join(rebuilt) == target
    if '?' not in template:
        assert target == encrypt(template, key['column_rank_order'], key['square'])
    return {'template': template, 'ciphertext': target,
            'known_coordinate_substitutions': substitutions,
            'erased_coordinate_fills': fills,
            'full_plaintext_reencryption_verified': '?' not in template,
            'published_key_changed': False, **result}


def model(source, gap=None):
    literal = ''.join(''.join(source['source_rows']).split())
    cipher = ''.join(c if c in C else '?' for c in literal)
    mapping = list(range(len(cipher)))
    if source['model']['kind'] == 'single_missing_coordinate':
        gap = source['model']['representative_source_boundary'] if gap is None else gap
        cipher = cipher[:gap] + '?' + cipher[gap:]
        mapping = mapping[:gap] + [None] + mapping[gap:]
    return literal, cipher, mapping


def geometry_screen(source, key):
    literal = ''.join(''.join(source['source_rows']).split())
    stencil = masked_encryption(source['readable_candidate'], key)
    assert len(literal) == 295 and len(stencil) == 296 and '?' not in literal
    assert literal[230:234] == 'GDXV'
    trials = []
    for gap in range(len(literal)+1):
        cipher = literal[:gap] + '?' + literal[gap:]
        cost = sum(a != '?' and b != '?' and a != b for a, b in zip(cipher, stencil))
        trials.append({'source_boundary': gap, 'known_coordinate_substitutions': cost})
    minimum = min(t['known_coordinate_substitutions'] for t in trials)
    tied = [t['source_boundary'] for t in trials if t['known_coordinate_substitutions'] == minimum]
    assert minimum == 2 and tied == source['model']['all_tied_source_boundaries'] == [232, 233]
    views = []
    for gap in tied:
        literal, cipher, mapping = model(source, gap)
        views.append({'source_boundary': gap, 'ciphertext': cipher,
                      'model_to_source_indices': mapping, **inspect(cipher, key, mapping),
                      'readable_candidate': repair(source['readable_candidate'], cipher, key, mapping, literal)})
    assert views[0]['readable_candidate']['ciphertext'] == views[1]['readable_candidate']['ciphertext']
    assert all(v['readable_candidate']['erased_coordinate_fills'][0]['to'] == 'X' for v in views)
    return {'method': 'All single-loss boundaries, with the fixed ordinary-word candidate used uniformly.',
            'boundary_count': len(trials), 'all_costs': trials,
            'minimum_known_coordinate_substitutions': minimum,
            'all_tied_source_boundaries': tied,
            'source_group': {'literal': 'GDXV', 'start': 230, 'end_exclusive': 234},
            'both_candidates_produce_identical_ciphertext': True,
            'unique_loss_boundary_claimed': False, 'all_tied_views': views}


def conditional_impact(inputs, records, screen):
    dependency = inputs['conditional_key_layer']
    path = ROOT/dependency['path']
    assert sha(path) == dependency['sha256']
    prior = json.loads(path.read_text())['conditional_office_prefix_layers']['Nov10-12_layer']
    assert prior['assignments'] == dependency['assignment'] == {'XX': '6'}
    baseline = inputs['key']
    changed = {**baseline, 'square': baseline['square'][:-1] + '6'}
    assert baseline['square'][-1] == '?' and '6' not in baseline['square']
    variants = []
    for record in records:
        views = screen['all_tied_views'] if record['id'] == 'p177_B2' else [record]
        for view in views:
            for label, cipher in [('source_model', view['ciphertext']),
                                  ('readable_candidate', view['readable_candidate']['ciphertext'])]:
                mapping = view['model_to_source_indices']
                before = inspect(cipher, baseline, mapping)
                after = inspect(cipher, changed, mapping)
                domains = [{'plaintext_index': i, 'pair': a['pair'], 'source_indices': a['source_indices'],
                            'before': a['domain'], 'after': b['domain']}
                           for i, (a, b) in enumerate(zip(before['positions'], after['positions']))
                           if a['domain'] != b['domain']]
                raw = [{'plaintext_index': i, 'pair': before['positions'][i]['pair'],
                        'source_indices': before['positions'][i]['source_indices'], 'before': a, 'after': b}
                       for i, (a, b) in enumerate(zip(before['raw'], after['raw'])) if a != b]
                if '?' not in after['raw']:
                    assert encrypt(after['raw'], changed['column_rank_order'], changed['square']) == cipher
                variants.append({'record': record['id'], 'variant': label,
                                 'source_boundary': view.get('source_boundary'),
                                 'raw_before': before['raw'], 'raw_after': after['raw'],
                                 'newly_fixed_raw_positions': raw,
                                 'all_changed_marginal_domains': domains,
                                 'all_remaining_uncertain_positions': [p for p in after['positions'] if p['raw'] == '?'],
                                 'full_reencryption_if_fully_known': '?' not in after['raw']})
    source_fixed = sorted({(v['record'], p['plaintext_index']) for v in variants
                           if v['variant'] == 'source_model' for p in v['newly_fixed_raw_positions']})
    candidate_fixed = sorted({(v['record'], p['plaintext_index']) for v in variants
                              if v['variant'] == 'readable_candidate' for p in v['newly_fixed_raw_positions']})
    assert source_fixed == [('p177_B1', 20), ('p177_B2', 139), ('p177_B3', 180), ('p177_B3', 184)]
    assert candidate_fixed == [('p177_B1', 20), ('p177_B3', 180), ('p177_B3', 184)]
    return {'dependency': dependency, 'key_id': baseline['id'], 'assignments': {'XX': '6'},
            'conditional_square': changed['square'], 'physical_records_checked': 3,
            'variants_checked': len(variants), 'all_variant_results': variants,
            'newly_fixed_physical_source_positions': [list(p) for p in source_fixed],
            'newly_fixed_physical_candidate_positions': [list(p) for p in candidate_fixed],
            'inconvenient_source_occurrence': 'p177 B2 position 139 changes V?RKAUFEN to V6RKAUFEN under XX=6; the separately priced ordinary-word repair changes that observed pair to E instead.',
            'published_key_changed': False,
            'interpretive_limit': 'The reference/date values follow the prior conditional key hypothesis. Their plausibility is not an independent proof of that hypothesis. Ordinary-word occurrences of other unknown cells remain garbles and are repaired separately.'}


def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    current = {k['id']: k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    assert key == current[key['id']]
    for source in inputs['source_images']:
        assert sha(HERE/source['path']) == source['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        assert sha(pdf) == inputs['source']['pdf_sha256']
        doc = fitz.open(pdf)
        for source in inputs['source_images']:
            pix = doc[source['pdf_page_1based']-1].get_pixmap(
                matrix=fitz.Matrix(source['render_scale'], source['render_scale']),
                clip=fitz.Rect(*source['crop_pdf_points']))
            im = Image.open(HERE/source['path']).convert('RGB')
            assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples
    records = []
    for source in inputs['records']:
        literal, cipher, mapping = model(source)
        assert len(literal) == source['source_slots']
        assert len(cipher) == source['advertised_length']
        raw = inspect(cipher, key, mapping)
        assert raw['raw'] == source['expected_raw']
        records.append({'id': source['id'], 'literal_source': literal,
                        'source_slots': len(literal), 'valid_coordinates': sum(c in C for c in literal),
                        'ciphertext': cipher, 'model_to_source_indices': mapping, **raw,
                        'readable_candidate': repair(source['readable_candidate'], cipher, key, mapping, literal)})
    screen = geometry_screen(inputs['records'][1], key)
    assert screen['all_tied_views'][0]['raw'] == records[1]['raw']
    assert [r['fixed_positions'] for r in records] == [161, 146, 183]
    assert [r['readable_candidate']['fixed_positions'] for r in records] == [164, 148, 184]
    third = records[2]
    price_start = third['raw'].index('1200MARK')
    price_positions = third['positions'][price_start:price_start+8]
    assert all('?' not in p['pair'] for p in price_positions)
    assert all(third['ciphertext'][i] == third['readable_candidate']['ciphertext'][i]
               for p in price_positions for i in p['source_indices'])
    return {'schema': 'adfgvx-turkish-tonnage-certificate-v1',
            'project': inputs['project'], 'authors': inputs['authors'],
            'input_sha256': sha(HERE/'inputs.json'), 'indexing': 'All indices are zero-based.',
            'summary': {'physical_records': len(records),
                        'printed_source_slots': sum(r['source_slots'] for r in records),
                        'valid_source_coordinates': sum(r['valid_coordinates'] for r in records),
                        'modeled_coordinates': sum(len(r['ciphertext']) for r in records),
                        'plaintext_positions': sum(len(r['raw']) for r in records),
                        'baseline_fixed_positions': sum(r['fixed_positions'] for r in records),
                        'readable_candidate_fixed_positions': sum(r['readable_candidate']['fixed_positions'] for r in records)},
            'records': records, 'p177_B2_geometry': screen,
            'price_witness': {'record': 'p177_B3', 'directly_observed': '1200MARK',
                              'positions': price_positions,
                              'second_price_limit': 'TAUSEN? is raw; the final D in TAUSEND requires one observed-coordinate change. The edition does not disguise that repair as a numerical key fill.'},
            'conditional_Nov10_XX6_propagation': conditional_impact(inputs, records, screen),
            'prior_attribution_check': inputs['prior_attribution_check'],
            'limits': ['The three-part instruction is distinct from the Corcovado messages.',
                       'Raw KERKIJRA and KEHKYRA are preserved; only the latter receives a separately priced same-length KERKYRA proposal.',
                       'The two B2 loss positions are genuinely tied and give identical corrected ciphertext.',
                       'The p177 page heading is November 11, its reception header is November 12, and its internal origin is November 11; all are preserved.',
                       'The conditional office key hypothesis is propagated to every source and candidate variant, including garbled ordinary words and all reference/date occurrences.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
