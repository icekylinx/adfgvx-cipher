#!/usr/bin/env python3
"""Recompute the conditional p215 A dispatch without a language model.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
All indices are zero based; ranges are half open.
"""
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
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_map(source, frame, mask_start=None):
    boundaries = frame['insert_unknown_before_source_indices']
    assert len(boundaries) == 2 and 155 <= boundaries[0] <= 159 and 184 <= boundaries[1] <= 188
    start = frame['move_printed_mask_source_start'] if mask_start is None else mask_start
    assert source[start:start + 5] == '-----'
    origins = []
    for i in range(len(source)):
        if i in boundaries:
            origins.append(None)
        origins.append(i)
    block = list(range(start, start + 5))
    at = origins.index(start)
    assert origins[at:at + 5] == block
    del origins[at:at + 5]
    destination = frame['insert_mask_block_at_shortened_frame_boundary']
    assert 0 <= destination <= len(origins) == 387
    origins[destination:destination] = block
    assert len(origins) == 392
    assert sorted(i for i in origins if i is not None) == list(range(390))
    # No observed coordinate, even its relative order, may be changed by this frame.
    assert [i for i in origins if i is not None and source[i] in C] == [
        i for i, c in enumerate(source) if c in C]
    return origins


def order(length, ranks):
    rows = [list(range(j, min(j + len(ranks), length)))
            for j in range(0, length, len(ranks))]
    transmitted = [row[col] for col in sorted(range(len(ranks)), key=lambda c: ranks[c])
                   for row in rows if col < len(row)]
    inverse = [None] * length
    for wire, intermediate in enumerate(transmitted):
        inverse[intermediate] = wire
    return transmitted, inverse


def analyze(cipher, key, origins):
    _, inverse = order(len(cipher), key['column_rank_order'])
    positions = []
    for p in range(len(cipher) // 2):
        indices = inverse[2 * p:2 * p + 2]
        pair = ''.join(cipher[i] for i in indices)
        domain = sorted({key['square'][6 * C.index(a) + C.index(b)]
                         for a in (C if pair[0] == '?' else pair[0])
                         for b in (C if pair[1] == '?' else pair[1])})
        positions.append(dict(plaintext_index=p, model_indices=indices,
                              source_indices=[origins[i] for i in indices],
                              pair=pair, domain=''.join(domain),
                              raw=domain[0] if len(domain) == 1 else '?'))
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(cipher, key['column_rank_order'], key['square'])
    return dict(raw=raw, fixed_positions=len(raw) - raw.count('?'), positions=positions)


def witness(cipher, key):
    full = cipher.replace('?', 'A')
    plaintext = decrypt(full, key['column_rank_order'], key['square'])
    assert encrypt(plaintext, key['column_rank_order'], key['square']) == full
    return dict(ciphertext=full, plaintext=plaintext,
                unknown_coordinate_choice='A solely for a complete roundtrip witness',
                historical_fill_claim=False)


def edited_layer(template, cipher, source, origins, key):
    assert len(template) == len(cipher) // 2
    interim = ''.join('??' if c == '?' else
                      C[key['square'].index(c) // 6] + C[key['square'].index(c) % 6]
                      for c in template)
    emit, _ = order(len(cipher), key['column_rank_order'])
    desired = ''.join(interim[i] for i in emit)
    result = ''.join(a if b == '?' else b for a, b in zip(cipher, desired))
    substitutions, printed, inserted = [], [], []
    for i, (a, b) in enumerate(zip(cipher, result)):
        if a == b:
            continue
        origin = origins[i]
        change = dict(model_index=i, source_index=origin, before=a, after=b,
                      literal_source_glyph=None if origin is None else source[origin])
        (substitutions if a in C else inserted if origin is None else printed).append(change)
    analyzed = analyze(result, key, origins)
    assert analyzed['raw'] == template
    # Raw domains already carry the unchanged coordinate-origin map. The edited
    # ciphertext and explicit change ledger suffice to recompute every new domain.
    return dict(ciphertext=result, raw=analyzed['raw'], fixed_positions=analyzed['fixed_positions'],
                observed_coordinate_substitutions=substitutions,
                printed_mask_fills=printed, inserted_slot_fills=inserted,
                full_roundtrip_witness=witness(result, key))


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov22-24')
    record = data['records'][0]
    audit = next(r for r in load(ROOT / 'data/reviews/source_gap_audit_20261103.json')['records']
                 if r['id'] == record['id'])
    assert record['source_rows'] == audit['source_rows']
    assert record['header_transcription'] == audit['header_transcription']
    source = ''.join(''.join(record['source_rows']).split())
    assert hashlib.sha256(source.encode()).hexdigest() == audit['literal_sha256']
    assert len(source) == 390 and sum(c in C for c in source) == 372
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    editions = []
    for model in record['models']:
        origins = source_map(source, model['frame'])
        cipher = ''.join(source[i] if i is not None and source[i] in C else '?' for i in origins)
        raw = analyze(cipher, key, origins)
        assert raw['raw'] == model['expected_raw']
        aliases = []
        for start in range(195, 204):
            alias = source_map(source, model['frame'], start)
            assert ''.join(source[i] if i is not None and source[i] in C else '?' for i in alias) == cipher
            aliases.append(dict(moved_printed_mask_source_range=[start, start + 5],
                                mapping_sha256=hashlib.sha256(json.dumps(alias, separators=(',', ':')).encode()).hexdigest()))
        row = dict(id=model['id'], frame=model['frame'], ciphertext=cipher,
                   model_to_source_indices=origins, **raw,
                   observationally_equivalent_mask_ownerships=aliases,
                   full_roundtrip_witness=witness(cipher, key))
        if model.get('word_proposal'):
            row['readable_candidate'] = edited_layer(model['word_proposal'], cipher, source, origins, key)
            layer = row['readable_candidate']
            expected_counts = model['expected_word_prices']
            actual_counts = dict(fixed_positions=layer['fixed_positions'],
                                 observed_substitutions=len(layer['observed_coordinate_substitutions']),
                                 printed_mask_fills=len(layer['printed_mask_fills']),
                                 inserted_slot_fills=len(layer['inserted_slot_fills']))
            assert actual_counts == expected_counts
            gained = [i for i, (a, b) in enumerate(zip(raw['raw'], layer['raw'])) if a == '?' and b != '?']
            assert all(sum(c in C for c in raw['positions'][i]['pair']) == 1 for i in gained)
            row['new_word_positions_with_one_observed_half'] = gained
            # Filled AFFFA and VVDGA have repeated-letter insertion aliases.
            # These identities do not multiply the text or establish unique gaps.
            alias_hashes = []
            for a in [156, 157, 158]:
                for b in [184, 185]:
                    for start in range(195, 204):
                        alternative = dict(model['frame'], insert_unknown_before_source_indices=[a, b])
                        mp = source_map(source, alternative, start)
                        wire = ''.join(source[i] if i is not None and source[i] in C else '?' for i in mp)
                        candidate = edited_layer(model['word_proposal'], wire, source, mp, key)
                        assert candidate['ciphertext'] == layer['ciphertext']
                        assert len(candidate['observed_coordinate_substitutions']) == actual_counts['observed_substitutions']
                        assert len(candidate['printed_mask_fills']) == actual_counts['printed_mask_fills']
                        assert len(candidate['inserted_slot_fills']) == actual_counts['inserted_slot_fills']
                        alias_hashes.append(hashlib.sha256(json.dumps(mp, separators=(',', ':')).encode()).hexdigest())
            assert len(set(alias_hashes)) == 54
            row['word_layer_ownership_aliases'] = dict(
                count=54, first_insert_boundaries=[156, 157, 158], second_insert_boundaries=[184, 185],
                moved_mask_source_starts=list(range(195, 204)), mapping_sha256s=alias_hashes,
                completed_ciphertext_sha256=hashlib.sha256(layer['ciphertext'].encode()).hexdigest(),
                limit='Conditional on this word proposal; one corrected ciphertext, not54 independent readings.')
        editions.append(row)
    primary = next(r for r in editions if r['id'] == record['primary_model_id'])
    # The primary raw stream, not a language-filled witness, is the census contract.
    primary_record = dict(primary, id=record['id'], model_id=primary['id'], literal_source=source)
    summary = dict(physical_sources=1, literal_source_slots=390, observed_source_coordinates=372,
                   printed_masks=18, frame_slots=392, plaintext_positions=196,
                   inserted_unknown_slots=2, relocated_printed_mask_slots=5,
                   excluded_source_slots=0, excluded_observed_coordinates=0,
                   raw_source_substitutions=0, observed_coordinate_order_preserved=True,
                   primary_fixed_raw_positions=primary['fixed_positions'],
                   primary_model_id=primary['id'])
    if 'readable_candidate' in primary:
        candidate = primary['readable_candidate']
        summary.update(primary_edited_fixed_positions=candidate['fixed_positions'],
                       primary_edited_observed_substitutions=len(candidate['observed_coordinate_substitutions']),
                       primary_printed_mask_fills=len(candidate['printed_mask_fills']),
                       primary_inserted_slot_fills=len(candidate['inserted_slot_fills']))
    common = None
    if all('readable_candidate' in row for row in editions):
        texts = [row['readable_candidate']['raw'] for row in editions]
        common = ''.join(chars[0] if len(set(chars)) == 1 else '?' for chars in zip(*texts))
        assert common == data['common_word_reading']
        assert len(common) - common.count('?') == 192
        summary.update(common_word_fixed_positions=192, common_unknown_positions=[44, 45, 66, 67])
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert all(x['role_from_caption'] is not None for x in fences + quotes)
    bodies = re.findall(r'```text\n(.*?)\n```', text, re.S)
    assert primary['raw'] in bodies
    assert '\n'.join(record['source_rows']) in bodies
    if 'readable_candidate' in primary:
        assert primary['readable_candidate']['raw'] in bodies
        assert data['primary_readable_german'] in text
        visible = re.sub('[^A-Z0-9?]', '', data['primary_readable_german'].upper())
        assert visible == primary['readable_candidate']['raw'].replace('X', '')
    return dict(schema='adfgvx-p215-breslau-dispatch-certificate-v1',
                authors=data['authors'], input_sha256=sha(HERE / 'inputs.json'),
                indexing='All indices are zero based; ranges are half open.',
                summary=summary, records=[primary_record],
                alternative_models=[row for row in editions if row['id'] != primary['id']],
                common_word_reading=common), evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result, evidence = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert load(path) == result, 'Certificate differs; inspect the change before regeneration'
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(verified=True, **result['summary'], source_evidence=evidence), indent=2))


if __name__ == '__main__':
    main()
