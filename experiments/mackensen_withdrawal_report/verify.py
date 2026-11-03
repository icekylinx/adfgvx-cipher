#!/usr/bin/env python3
"""Source, geometry and assembly audit for the November 3 thirteen-part report.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The historical decipherment and published reconstructed body retain their credits.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

CO = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse_order(length, ranks):
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (c < length % width) for c in range(width)]
    starts = [sum(heights[c] for c in range(width) if ranks[c] < ranks[col])
              for col in range(width)]
    order = [starts[i % width] + i // width for i in range(length)]
    assert sorted(order) == list(range(length))
    return order


def inspect(cipher, key, mapping):
    order = inverse_order(len(cipher), key['column_rank_order'])
    flat = ''.join(cipher[i] for i in order)
    assert flat == untranspose(cipher, key['column_rank_order'])
    square = key['square']
    positions = []
    for i in range(len(cipher) // 2):
        pair = flat[2*i:2*i+2]
        domain = ''.join(sorted(square[6*r+c] for r in range(6) for c in range(6)
                               if pair[0] in ('?', CO[r]) and pair[1] in ('?', CO[c])))
        indices = order[2*i:2*i+2]
        positions.append({'plaintext_position': i, 'pair': pair, 'domain': domain,
                          'raw_label': domain if len(domain) == 1 else '?',
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices]})
    raw = ''.join(p['raw_label'] for p in positions)
    assert raw == decrypt(cipher, key['column_rank_order'], square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, key['column_rank_order'], square)
    witness = cipher.replace('?', 'A')
    witness_text = decrypt(witness, key['column_rank_order'], square)
    assert encrypt(witness_text, key['column_rank_order'], square) == witness
    assert all(a == '?' or a == b for a, b in zip(cipher, witness))
    return {'raw': raw, 'fixed_positions': len(raw) - raw.count('?'), 'positions': positions,
            'arbitrary_completion_roundtrip': {'ciphertext': witness, 'plaintext': witness_text,
                                             'historical_claim': False}}


def stencil(text, key):
    square = key['square']
    flat = ''.join('??' if c == '?' else CO[square.index(c)//6] + CO[square.index(c) % 6]
                   for c in text)
    result = ['?'] * len(flat)
    for value, index in zip(flat, inverse_order(len(flat), key['column_rank_order'])):
        result[index] = value
    return ''.join(result)


def frame_for(record, gap=None):
    literal = ''.join(''.join(record['source_rows']).split())
    assert set(literal) <= set(CO + '-')
    cipher = literal.replace('-', '?')
    mapping = list(range(len(cipher)))
    model = record['frame_model']
    if model['added_coordinates']:
        g = model['source_gap_index'] if gap is None else gap
        count = model['added_coordinates']
        cipher = cipher[:g] + '?' * count + cipher[g:]
        mapping[g:g] = [None] * count
    assert len(cipher) == record['advertised_length']
    return literal, cipher, mapping


def record_certificate(record, key):
    if 'display_reading' in record:
        assert ''.join(record['display_reading'].split()) == record['editorial_plaintext']
    literal, cipher, mapping = frame_for(record)
    raw = inspect(cipher, key, mapping)
    assert raw['raw'] == record['expected_raw']
    text = record['editorial_plaintext']
    masked = stencil(text, key)
    assert len(masked) == len(cipher)
    repaired = ''.join(a if b == '?' else b for a, b in zip(cipher, masked))
    edition = inspect(repaired, key, mapping)
    assert edition['raw'] == text
    substitutions, source_fills, added_fills = [], [], []
    for i, (old, new) in enumerate(zip(cipher, repaired)):
        if old == new:
            continue
        source_index = mapping[i]
        event = {'model_index': i, 'source_index': source_index, 'from': old, 'to': new}
        target = substitutions if old != '?' else source_fills if source_index is not None else added_fills
        target.append(event)
    replay = list(cipher)
    for event in substitutions + source_fills + added_fills:
        replay[event['model_index']] = event['to']
    assert ''.join(replay) == repaired
    if '?' not in text:
        assert encrypt(text, key['column_rank_order'], key['square']) == repaired
    rare = [{'position': p['plaintext_position'], 'raw': p['raw_label'],
             'candidate': text[p['plaintext_position']], 'pair': p['pair'],
             'source_indices': p['source_indices']}
            for p in raw['positions'] if p['raw_label'].isdigit() or p['raw_label'] in 'JQY']
    return {'id': record['id'], 'message_part': record['message_part'],
            'literal_source': literal, 'source_slots': len(literal),
            'valid_source_coordinates': sum(c in CO for c in literal),
            'frame_model': record['frame_model'], 'analysis_frame': cipher,
            'model_to_source_indices': mapping, 'raw': raw,
            'edition': {'ciphertext': repaired, **edition},
            'known_coordinate_substitutions': substitutions,
            'source_mask_fills': source_fills, 'inserted_coordinate_fills': added_fills,
            'inserted_coordinates_left_unknown': sum(j is None and v == '?' for j, v in zip(mapping, repaired)),
            'source_masks_left_unknown': sum(j is not None and v == '?' for j, v in zip(mapping, repaired)),
            'raw_numeral_and_rare_label_inventory': rare,
            'source_deletions': 0, 'source_reordering': False, 'key_changed': False}


def gap_audit(record, spec, key):
    text = record['editorial_plaintext']
    assert text.count(spec['masked_text']) == 1
    masked = text.replace(spec['masked_text'], '?' * len(spec['masked_text']))
    targets = [stencil(t, key) for t in [text, masked]]
    literal = ''.join(''.join(record['source_rows']).split())
    rows = []
    for gap in range(len(literal) + 1):
        _, cipher, mapping = frame_for(record, gap)
        costs = [sum(a != '?' and b != '?' and a != b for a, b in zip(cipher, target))
                 for target in targets]
        rows.append({'gap': gap, 'full_substitutions': costs[0], 'masked_substitutions': costs[1]})
    scopes = []
    for field in ['full_substitutions', 'masked_substitutions']:
        minimum = min(r[field] for r in rows)
        minimizers = [r['gap'] for r in rows if r[field] == minimum]
        witnesses = []
        for gap in minimizers:
            _, cipher, mapping = frame_for(record, gap)
            witnesses.append({'gap': gap, 'raw': inspect(cipher, key, mapping)['raw']})
        scopes.append({'scope': field, 'minimum': minimum, 'all_minimizers': minimizers,
                       'cost_histogram': {str(k): v for k, v in sorted(Counter(r[field] for r in rows).items())},
                       'minimum_raw_witnesses': witnesses})
    group_rows = [r for r in rows if spec['printed_short_group_start'] <= r['gap'] <= spec['printed_short_group_end']]
    return {'id': record['id'], 'all_gap_comparisons': rows, 'scopes': scopes,
            'printed_short_group_gap_comparisons': group_rows,
            'masked_text': spec['masked_text'],
            'limit': 'Both stencils are retrospective editorial templates. Minimum cost does not authenticate missing-coordinate placement, mechanism, spelling or historical priority.'}


def build(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    assert sha(ROOT / 'data/keys.json') == inp['base_keys_sha256']
    actual = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys'] if k['id'] == inp['key']['id'])
    assert all(actual[k] == v for k, v in inp['key'].items())
    audit_path = HERE / 'independent_source_audit.json'
    assert sha(audit_path) == inp['independent_source_audit_sha256']
    source_audit = json.loads(audit_path.read_text())
    for row in source_audit['records']:
        original = next(r for r in inp['records'] if r['id'] == row['id'])
        assert ''.join(row['diplomatic_groups']) == ''.join(''.join(original['source_rows']).split())
        assert row['slots'] == sum(len(g) for g in row['diplomatic_groups'])
    for name, digest in source_audit['source_images'].items():
        assert sha(HERE / 'sources' / name) == digest
    for img in inp['source_images']:
        assert sha(HERE / img['path']) == img['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf) == inp['source']['pdf_sha256']
        doc = fitz.open(pdf)
        for img in inp['source_images']:
            # MuPDF can reuse a lower-resolution decoded image after an earlier
            # render of the same page. These separately reviewed detail crops
            # were generated from a fresh cache, which is explicit metadata.
            if img.get('fresh_render_cache'):
                fitz.TOOLS.store_shrink(100)
            p = doc[img['pdf_page_1based'] - 1]
            pix = p.get_pixmap(matrix=fitz.Matrix(img['render_scale'], img['render_scale']),
                              clip=fitz.Rect(*img['crop_pdf_points']), alpha=False)
            saved = Image.open(HERE / img['path']).convert('RGB')
            assert saved.size == (pix.width, pix.height) and saved.tobytes() == pix.samples
    records = [record_certificate(r, inp['key']) for r in inp['records']]
    by_id = {r['id']: r for r in records}
    parts = [r['message_part'] for r in records]
    assert parts == inp['assembly']['present_parts']
    assert set(range(1, 14)) - set(parts) == {2}
    assert by_id['p113_B9']['raw']['raw'] == by_id['p113_B9']['edition']['raw']
    assert by_id['p113_B9']['raw']['fixed_positions'] == 108
    assert not by_id['p113_B9']['known_coordinate_substitutions']
    assert not by_id['p115_A6']['known_coordinate_substitutions']
    last = by_id['p116_A13']
    assert last['source_slots'] == 160 and last['frame_model']['added_coordinates'] == 62
    assert last['raw']['fixed_positions'] == last['edition']['fixed_positions'] == 38
    assert last['raw']['raw'] == last['edition']['raw']
    assert not (last['known_coordinate_substitutions'] or last['source_mask_fills'] or last['inserted_coordinate_fills'])
    audits = [gap_audit(next(r for r in inp['records'] if r['id'] == a['id']), a, inp['key'])
              for a in inp['gap_audits']]
    assert audits[0]['scopes'][0]['minimum'] == 0
    assert audits[0]['scopes'][0]['all_minimizers'] == [102]
    assert audits[1]['scopes'][0]['minimum'] == 3
    assert audits[1]['scopes'][0]['all_minimizers'] == [141, 142, 143, 144]
    summary = {
        'physical_records': len(records), 'declared_message_parts': 13,
        'missing_part2_not_fabricated': True, 'raw_only_jammed_final_part': True,
        'printed_source_slots': sum(r['source_slots'] for r in records),
        'valid_source_coordinates': sum(r['valid_source_coordinates'] for r in records),
        'modeled_coordinates': sum(len(r['analysis_frame']) for r in records),
        'plaintext_positions': sum(len(r['raw']['raw']) for r in records),
        'baseline_fixed_positions': sum(r['raw']['fixed_positions'] for r in records),
        'candidate_fixed_positions': sum(r['edition']['fixed_positions'] for r in records),
        'known_coordinate_substitutions': sum(len(r['known_coordinate_substitutions']) for r in records),
        'source_mask_fills': sum(len(r['source_mask_fills']) for r in records),
        'inserted_coordinate_fills': sum(len(r['inserted_coordinate_fills']) for r in records),
        'inserted_coordinates_left_unknown': sum(r['inserted_coordinates_left_unknown'] for r in records),
        'source_masks_left_unknown': sum(r['source_masks_left_unknown'] for r in records),
        'source_deletions': 0, 'published_key_changed': False,
        'one_loss_gap_comparisons': sum(len(a['all_gap_comparisons']) for a in audits)}
    return {'schema': 'adfgvx-mackensen-withdrawal-source-certificate-v1',
            'authors': inp['authors'], 'inputs_sha256': sha(HERE / 'inputs.json'),
            'prior_ocr_sha256': sha(HERE / 'prior_ocr_candidates.json'),
            'summary': summary, 'records': records, 'gap_audits': audits,
            'assembly': inp['assembly'], 'prior_credit': inp['prior_credit']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    destination = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(destination.read_text()) == result, 'Certificate differs from independent recomputation'
    else:
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': args.pdf is not None,
                      **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
