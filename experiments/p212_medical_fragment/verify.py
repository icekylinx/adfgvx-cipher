#!/usr/bin/env python3
"""Independent source/coordinate verifier. icekylinx and GPT-6 Astra Pro."""
from pathlib import Path
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDINATES = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def layout(length, ranks):
    """Ciphertext index at each untransposed coordinate index."""
    columns = {}
    cursor = 0
    for rank in sorted(ranks):
        column = ranks.index(rank)
        size = len(range(column, length, len(ranks)))
        columns[column] = list(range(cursor, cursor + size))
        cursor += size
    result = [columns[i % len(ranks)][i // len(ranks)] for i in range(length)]
    assert sorted(result) == list(range(length))
    return result


def decode(ciphertext, ranks, square):
    permutation = layout(len(ciphertext), ranks)
    interim = ''.join(ciphertext[index] for index in permutation)
    domains = []
    for i in range(0, len(interim), 2):
        first, second = interim[i:i + 2]
        allowed = [square[6 * row + column]
                   for row in range(6) for column in range(6)
                   if (first == '?' or first == COORDINATES[row])
                   and (second == '?' or second == COORDINATES[column])]
        domains.append(''.join(sorted(allowed)))
    return interim, domains, ''.join(d if len(d) == 1 else '?' for d in domains)


def encrypt(plaintext, ranks, square):
    interim = ''.join(COORDINATES[square.index(c) // 6]
                      + COORDINATES[square.index(c) % 6] for c in plaintext)
    return ''.join(interim[ranks.index(rank)::len(ranks)] for rank in sorted(ranks))


def verify(pdf=None):
    inputs = json.loads((HERE / 'inputs.json').read_text())
    certificate = json.loads((HERE / 'certificates.json').read_text())
    assert certificate['input_sha256'] == sha256(HERE / 'inputs.json')
    for dependency in inputs['dependencies']:
        assert sha256(ROOT / dependency['path']) == dependency['sha256']
    record = certificate['record']
    source = ''.join(''.join(inputs['record']['source_rows']).split())
    assert source == record['literal_source']
    assert len(source) == 197 and set(source) <= set(COORDINATES)
    key = inputs['key']
    registered = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                      if k['id'] == key['id'])
    assert key == registered
    square, ranks = key['square'], key['column_rank_order']
    assert set(square) == set(ALPHABET) and len(square) == 36
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    frame = '?' * 105 + source
    assert record['ciphertext'] == frame
    assert record['model_to_source_indices'] == [None] * 105 + list(range(197))
    interim, domains, raw = decode(frame, ranks, square)
    assert interim == record['raw_interim']
    assert domains == record['raw_domains'] and raw == record['raw']
    assert len(domains) == 151 and raw.count('?') == 105
    counts = {observed: sum(pair.count('?') == 2 - observed
                           for pair in (interim[i:i + 2] for i in range(0, 302, 2)))
              for observed in (0, 1, 2)}
    assert counts == {0: 0, 1: 105, 2: 46}
    assert certificate['frame_geometry'] == {
        'full_observed_pairs': 46, 'one_observed_half_pairs': 105,
        'zero_observed_half_pairs': 0}
    permutation = layout(302, ranks)
    primary_frame = list(frame)
    fills = []
    selected_positions = []
    for span in inputs['lexical_spans']:
        for position, character in enumerate(span['text'], span['start']):
            assert character in domains[position]
            selected_positions.append(position)
            cell = square.index(character)
            for side, value in enumerate((COORDINATES[cell // 6], COORDINATES[cell % 6])):
                model_index = permutation[2 * position + side]
                if primary_frame[model_index] == '?':
                    assert model_index < 105
                    fills.append({'model_index': model_index, 'source_index': None,
                                  'plaintext_index': position, 'pair_side': side,
                                  'from': '?', 'to': value, 'selected_label': character})
                    primary_frame[model_index] = value
                else:
                    assert primary_frame[model_index] == value
    assert len(selected_positions) == len(set(selected_positions)) == 121
    primary_frame = ''.join(primary_frame)
    primary = record['primary']
    _, primary_domains, primary_raw = decode(primary_frame, ranks, square)
    assert primary_frame == primary['ciphertext']
    assert primary_frame[105:] == source
    assert primary_domains == primary['domains'] and primary_raw == primary['raw']
    assert sorted(fills, key=lambda x: x['model_index']) == primary['inserted_coordinate_fills']
    assert len(fills) == 83
    unresolved = [i for i, c in enumerate(primary_raw) if c == '?']
    assert unresolved == primary['unresolved_plaintext_positions'] and len(unresolved) == 22
    unassigned = [i for i, c in enumerate(primary_frame) if c == '?']
    assert unassigned == primary['unassigned_inserted_model_indices'] and len(unassigned) == 22
    assert primary['observed_coordinate_substitutions'] == primary['source_mask_fills'] == []
    for i, position in enumerate(record['positions']):
        model_indices = permutation[2 * i:2 * i + 2]
        expected = {'plaintext_index': i, 'pair': interim[2 * i:2 * i + 2],
                    'model_indices': model_indices,
                    'source_indices': [m - 105 if m >= 105 else None for m in model_indices],
                    'domain': domains[i], 'raw': raw[i], 'primary': primary_raw[i]}
        assert position == expected
        if raw[i] != '?':
            assert raw[i] == primary_raw[i]
    assert len(record['positions']) == 151
    witness = certificate['exact_reencryption_witness']
    assert witness['ciphertext'] == primary_frame.replace('?', 'A')
    assert encrypt(witness['plaintext'], ranks, square) == witness['ciphertext']
    assert witness['ciphertext'][105:] == source
    summary = certificate['summary']
    assert summary == {
        'source_records': 1, 'source_slots': 197, 'valid_source_coordinates': 197,
        'analysis_frame_slots': 302, 'plaintext_positions': 151,
        'raw_fixed_positions': 46, 'primary_fixed_positions': 129,
        'observed_coordinate_substitutions': 0, 'source_mask_fills': 0,
        'inserted_slots': 105, 'inserted_slot_fills': 83,
        'unassigned_inserted_slots': 22, 'excluded_source_slots': 0,
        'reordered_source_slots': 0}
    controls = inputs['evidence']['length_retrieval_controls']
    assert [c['true_total_rank'] for c in controls] == [1, 1, 2]
    for control in controls:
        full = encrypt(control['truth'], control['ranks'], control['completed_square'])
        assert len(full) == control['total']
        assert full[-197:] == control['source']
        original_key = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                            if k['id'] == control['key'])
        assert all(c not in ALPHABET or c == d
                   for c, d in zip(original_key['square'], control['completed_square']))
    control = inputs['evidence']['structural_302_control']
    assert encrypt(control['truth'], ranks, square)[-197:] == control['source']
    ci, cd, cr = decode('?' * 105 + control['source'], ranks, square)
    assert len(cr) == 151 and cr.count('?') == 105
    assert all(character in domain for character, domain in zip(control['truth'], cd))
    assert all(ci[i:i + 2].count('?') <= 1 for i in range(0, 302, 2))
    retrieval = inputs['evidence']['retrieval']
    assert retrieval['total_frames'] == 25 * len(range(198, 701, 2)) == 6300
    assert [x['length'] for x in retrieval['nearby_lengths']] == list(range(298, 309, 2))
    for item in retrieval['nearby_lengths']:
        _, nd, nr = decode('?' * (item['length'] - 197) + source, ranks, square)
        assert len(nr) - nr.count('?') == item['fixed_labels']
    shuffled = inputs['evidence']['shuffled_comparison']
    assert len(shuffled['best_scores']) == len(shuffled['at302_scores']) == shuffled['count'] == 100
    assert max(shuffled['best_scores']) == shuffled['maximum_shuffled_best']
    assert sum(s >= retrieval['actual_score'] for s in shuffled['best_scores']) == shuffled['greater_or_equal_actual'] == 0
    case = (ROOT / inputs['case_path']).read_text()
    assert re.findall(r'```text\n(.*?)\n```', case, re.S) == [
        '\n'.join(inputs['record']['source_rows']), raw, primary_raw]
    german = inputs['readable_german_excerpt']
    assert certificate['readable_german_excerpt'] == german
    assert re.findall(r'^> (.*)$', case, re.M) == [german]
    assert re.sub('[^A-Z0-9]', '', german.upper()) == ''.join(
        span['text'] for span in inputs['lexical_spans']).replace('X', '')
    for span in inputs['lexical_spans']:
        end = span['start'] + len(span['text'])
        assert f"| {span['start']}–{end} | `{span['text']}` |" in case
    for row in [
        '| Fixed raw / edited positions | 46 / 129 |',
        '| Proposed lexical positions / other retained raw labels | 121 / 8 |',
        '| Added prefix slots / filled / unassigned | 105 / 83 / 22 |',
        '| Observed substitutions, printed-mask fills, exclusions or reorderings | 0 |']:
        assert row in case
    if pdf is not None:
        import fitz
        from PIL import Image, ImageChops
        import io
        assert Path(pdf).stat().st_size == inputs['source']['pdf_bytes']
        assert sha256(pdf) == inputs['source']['pdf_sha256']
        reference = inputs['source_reference']
        existing = ROOT / reference['existing_local_crop']
        assert sha256(existing) == reference['existing_crop_sha256']
        with fitz.open(pdf) as document:
            scale = reference['render_scale']
            pixmap = document[reference['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*reference['crop_pdf_points']))
            rendered = Image.open(io.BytesIO(pixmap.tobytes('png'))).convert('RGB')
            archived = Image.open(existing).convert('RGB')
            assert rendered.size == archived.size
            assert ImageChops.difference(rendered, archived).getbbox() is None
    print('Verified p212 A4: 197 unchanged observations; raw 46/151; primary 129/151; '
          '83 inserted-half fills; 22 unresolved positions. Language scores are frozen diagnostics.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    verify(args.pdf)
