#!/usr/bin/env python3
"""Verify the Hungary transport warning, exact missing group and unchanged reference domains.

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


def verify_crops(pdf, expected, crops, relative_to):
    import fitz
    from PIL import Image
    assert pdf.stat().st_size == expected['pdf_bytes']
    assert sha(pdf) == expected['pdf_sha256']
    doc = fitz.open(pdf)
    for crop in crops:
        rect = crop.get('crop_pdf_points', crop.get('clip_points'))
        scale = crop.get('render_scale', crop.get('scale'))
        pix = doc[crop['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*rect))
        im = Image.open(relative_to/crop['path']).convert('RGB')
        assert im.size == (pix.width, pix.height) and im.tobytes() == pix.samples



def build(pdf=None):
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    key = inputs['key']
    assert key == next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']
                       if k['id'] == key['id'])
    for crop in inputs['source_images']:
        assert sha(HERE/crop['path']) == crop['sha256']
    if pdf:
        verify_crops(pdf, inputs['source'], inputs['source_images'], HERE)
    records = []
    for source in inputs['records']:
        literal = ''.join(''.join(source['source_rows']).split())
        assert set(literal) <= set(C)
        assert len(literal) == source['source_slots']
        mapping = list(range(len(literal)))
        cipher = literal
        if source['model']['kind'] == 'single_missing_group':
            gap = source['model']['gap_before_source_index']
            count = source['model']['missing_coordinates']
            mapping = mapping[:gap] + [None]*count + mapping[gap:]
            cipher = literal[:gap] + '?'*count + literal[gap:]
        assert len(cipher) == source['advertised_length']
        raw = inspect(cipher, key, mapping)
        assert raw['raw'] == source['expected_raw']
        candidate = repair(source['readable_candidate'], cipher, key, mapping, literal)
        records.append({'id': source['id'], 'literal_source': literal,
                        'source_slots': len(literal), 'valid_source_coordinates': len(literal),
                        'ciphertext': cipher, 'model_to_source_indices': mapping,
                        **raw, 'readable_candidate': candidate})
    by_id = {r['id']: r for r in records}
    assert [r['source_slots'] for r in records] == [146,187,110,136,190,108]
    assert [len(r['raw']) for r in records] == [73,96,55,68,95,54]
    assert [r['fixed_positions'] for r in records] == [73,91,40,68,94,39]
    assert [len(r['readable_candidate']['known_coordinate_substitutions']) for r in records] == [0,0,0,0,2,0]
    assert [len(r['readable_candidate']['erased_coordinate_fills']) for r in records] == [0,5,0,0,0,0]
    alignment = inputs['cross_copy_alignment']
    left, right = by_id[alignment['left_record']], by_id[alignment['right_record']]
    assert len(left['raw']) == alignment['left_length']
    assert len(right['raw']) == alignment['right_length']
    mask = ['?'] * len(left['raw'])
    matched = []
    for l, r, size in alignment['matching_ranges_left_start_right_start_length']:
        for offset in range(size):
            lp, rp = l+offset, r+offset
            assert right['raw'][rp] != '?' and mask[lp] == '?'
            mask[lp] = right['raw'][rp]
            matched.append({'left_index': lp, 'right_index': rp,
                            'right_raw_witness': right['positions'][rp],
                            'left_candidate': left['readable_candidate']['positions'][lp]})
            assert left['readable_candidate']['raw'][lp] == right['raw'][rp]
    assert len(matched) == 92
    assert [i for i, ch in enumerate(mask) if ch == '?'] == alignment['excluded_left_positions']
    assert sorted(set(range(len(right['raw'])))-{p['right_index'] for p in matched}) == alignment['unused_right_positions']
    mask = ''.join(mask)
    stencil = masked_encryption(mask, key)
    literal = left['literal_source']
    scores = []
    for gap in range(len(literal)+1):
        model = literal[:gap] + '?????' + literal[gap:]
        mismatch = [i for i, (a,b) in enumerate(zip(model,stencil))
                    if a != '?' and b != '?' and a != b]
        scores.append({'gap_before_source_index': gap,
                       'observed_coordinate_substitutions': len(mismatch),
                       'mismatching_model_indices': mismatch})
    best = min(s['observed_coordinate_substitutions'] for s in scores)
    winners = [s['gap_before_source_index'] for s in scores
               if s['observed_coordinate_substitutions'] == best]
    assert best == 0 and winners == [35]
    assert len(scores) == 188 and stencil[35:40] == 'DXDVA'
    # Derive the missing group from the independent C2 mask alone. Neither of
    # the later C2 repairs (positions 5 and 90) can influence the gap screen.
    derived = literal[:35] + stencil[35:40] + literal[35:]
    assert derived == left['readable_candidate']['ciphertext']
    assert derived[:35] + derived[40:] == literal
    assert decrypt(derived,key['column_rank_order'],key['square']) == left['readable_candidate']['raw']
    restored = []
    for match in matched:
        i = match['left_index']
        if left['raw'][i] == '?':
            restored.append({'left_index': i, 'right_index': match['right_index'],
                             'before': left['positions'][i],
                             'after': left['readable_candidate']['positions'][i],
                             'independent_right_raw_witness': match['right_raw_witness']})
    assert [p['left_index'] for p in restored] == [8,18,28,79,89]
    assert ''.join(p['after']['raw'] for p in restored) == 'TAHSX'
    reverse_support = []
    for lp,rp in [(5,5),(90,90)]:
        assert lp in alignment['excluded_left_positions']
        assert left['raw'][lp] == right['readable_candidate']['raw'][rp]
        assert left['positions'][lp] == left['readable_candidate']['positions'][lp]
        assert all(i is not None for i in left['positions'][lp]['source_indices'])
        assert right['raw'][rp] != right['readable_candidate']['raw'][rp]
        reverse_support.append({'left_unchanged_raw_witness': left['positions'][lp],
                                'right_before': right['positions'][rp],
                                'right_after': right['readable_candidate']['positions'][rp],
                                'excluded_from_gap_selection': True})
    assert [e['source_index'] for e in right['readable_candidate']['known_coordinate_substitutions']] == [75,86]
    unknown_word = right['positions'][45]
    assert unknown_word['pair'] == 'DX' and unknown_word['domain'] == '0123456789QY'
    assert unknown_word == right['readable_candidate']['positions'][45]
    assert unknown_word['source_indices'] == [90,137]

    b3,c3 = by_id['p184_B3'],by_id['p184_C3']
    assert [p['pair'] for p in b3['positions'][:54]] == [p['pair'] for p in c3['positions']]
    assert untranspose(b3['literal_source'],key['column_rank_order'])[:-2] == untranspose(c3['literal_source'],key['column_rank_order'])
    assert b3['raw'][-1] == 'X' and len(b3['raw']) == len(c3['raw'])+1
    footer_pairs = [{'plaintext_index': i, 'left': b3['positions'][i], 'right': c3['positions'][i]}
                    for i in range(54)]
    unknown_footer = [p for p in footer_pairs if p['left']['raw'] == '?']
    assert len(unknown_footer) == 15
    assert all(p['left']['domain'] == p['right']['domain'] == '0123456789QY'
               for p in unknown_footer)
    inventory = [{'record': r['id'], 'variant': variant, 'raw': reading['raw'],
                  'all_unresolved_positions': [p for p in reading['positions'] if p['raw'] == '?'],
                  'all_numeral_and_JQY_occurrences': [p for p in reading['positions']
                                                    if p['raw'] in '0123456789JQY']}
                 for r in records for variant,reading in [('source_model',r),('readable_candidate',r['readable_candidate'])]]
    assert sum(len(r['raw'])-r['readable_candidate']['fixed_positions'] for r in records) == 31
    return {'schema':'adfgvx-hungary-transport-warning-certificate-v1',
            'project':inputs['project'],'authors':inputs['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':'All indices are zero-based.',
            'summary':{'physical_records':6,'printed_source_slots':877,
                       'valid_source_coordinates':877,'modeled_coordinates':882,
                       'plaintext_positions':441,'baseline_fixed_positions':405,
                       'candidate_fixed_positions':410,'known_coordinate_substitutions':2,
                       'printed_erasure_fills':0,'missing_coordinate_fills':5,
                       'source_deletions':0,'remaining_unresolved_positions':31,
                       'published_key_changed':False},
            'records':records,
            'independent_missing_group_certificate':{
                'model':'One contiguous group of five missing source coordinates; advertised length 192.',
                'mask_from_uncorrected_C2':mask,'matched_position_count':92,
                'alignment':alignment,'matched_positions':matched,
                'all_gap_scores':scores,'minimum_observed_coordinate_changes':best,
                'all_best_gaps':winners,'missing_group':'DXDVA',
                'derived_only_from_mask_ciphertext':derived,
                'all_observed_B2_coordinates_unchanged':True,
                'restored_plaintext_positions':restored,
                'reverse_C2_word_repair_witnesses':reverse_support,
                'uniqueness_scope':'Exactly one zero-cost position among 188 single contiguous five-coordinate-gap models for this fixed alignment; not an unconstrained reconstruction theorem.'},
            'footer_exact_pair_prefix':{'left_record':'p184_B3','right_record':'p184_C3',
                                       'matching_positions':54,'all_pair_witnesses':footer_pairs,
                                       'unknown_positions_still_unassigned':unknown_footer,
                                       'additional_left_terminal':'X'},
            'unresolved_extra_word_position':unknown_word,
            'complete_raw_label_and_domain_inventory':inventory,
            'prior_attribution_check':inputs['prior_attribution_check'],
            'limits':['The warning states a risk of loss in Hungary; this edition does not establish that every transport was in fact lost.',
                      'The different address lengths and received misspellings remain explicit. The complete messages are not assumed byte-identical.',
                      'The printed a.m. receipt times conflict with 13.40 origin on the same date; no date or time is changed.',
                      'The unknown reference labels are unchanged despite exact pair equality. C2 retains an extra unresolved position in HE?REIN.',
                      'Source transcription and missing-group reconstruction are not a claim of first historical decipherment.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    target = HERE/'certificates.json'
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary']},indent=2))


if __name__ == '__main__':
    main()
