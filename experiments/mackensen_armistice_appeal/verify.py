#!/usr/bin/env python3
"""Verify the six-part Mackensen armistice appeal and its conditional loss model.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The historical body identification and period key retain their prior credits.
"""
from array import array
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

CO = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def untranspose(cipher, ranks):
    """Allocate ranked column chunks, independently of the project cipher."""
    width, length = len(ranks), len(cipher)
    height, extra = divmod(length, width)
    stream, inverse = ['?'] * length, [None] * length
    cursor = 0
    for col in sorted(range(width), key=lambda c: ranks[c]):
        for row in range(height + (col < extra)):
            index = row * width + col
            stream[index], inverse[index] = cipher[cursor], cursor
            cursor += 1
    assert cursor == length
    return ''.join(stream), inverse


def encipher(text, ranks, square):
    flat = ''.join('??' if char == '?' else
                   CO[square.index(char) // 6] + CO[square.index(char) % 6]
                   for char in text)
    return ''.join(flat[col::len(ranks)]
                   for col in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def make_frame(literal, gaps=()):
    frame, origin = [], []
    for i in range(len(literal) + 1):
        for _ in range(gaps.count(i)):
            frame.extend('?' * 5)
            origin.extend([None] * 5)
        if i < len(literal):
            frame.append(literal[i] if literal[i] in CO else '?')
            origin.append(i)
    return ''.join(frame), origin


def inspect(record, key):
    ranks, square = key['column_rank_order'], key['square']
    literal = ''.join(''.join(record['source_rows']).split())
    gaps = record['frame_model'].get('source_gap_indices', [])
    frame, origin = make_frame(literal, gaps)
    assert len(frame) == record['advertised_length']
    stream, inverse = untranspose(frame, ranks)
    positions, raw = [], []
    for i in range(len(stream) // 2):
        pair = stream[2 * i:2 * i + 2]
        domain = ''.join(sorted(square[6 * a + b]
                                for a in range(6) for b in range(6)
                                if pair[0] in ('?', CO[a]) and pair[1] in ('?', CO[b])))
        char = domain if len(domain) == 1 else '?'
        indices = inverse[2 * i:2 * i + 2]
        raw.append(char)
        positions.append({'plaintext_position': i, 'source_pair': pair,
                          'base_domain': domain, 'base_symbol': char,
                          'working_coordinate_indices': indices,
                          'source_coordinate_indices': [origin[j] for j in indices]})
    raw = ''.join(raw)
    assert raw == record['expected_raw'] == decrypt(frame, ranks, square)
    assert [p['base_domain'] for p in positions] == plaintext_domains(frame, ranks, square)
    retransposed = ''.join(stream[col::len(ranks)]
                          for col in sorted(range(len(ranks)), key=lambda c: ranks[c]))
    assert retransposed == frame
    candidate = record['editorial_plaintext']
    target = encipher(candidate, ranks, square)
    assert len(candidate) == len(raw)
    assert target == encrypt(candidate, ranks, square)
    assert decrypt(target, ranks, square) == candidate
    owner = {j: p['plaintext_position'] for p in positions for j in p['working_coordinate_indices']}
    changes, erasures, added = [], [], []
    for i, (old, new) in enumerate(zip(frame, target)):
        entry = {'working_coordinate_index': i, 'source_index': origin[i],
                 'plaintext_position': owner[i], 'observed': old, 'proposed': new}
        if origin[i] is None:
            added.append(entry)
        elif old == '?':
            entry['printed'] = literal[origin[i]]
            erasures.append(entry)
        elif old != new:
            changes.append(entry)
    assert len(changes) == record['expected_known_substitutions']
    restored = list(frame)
    for edit in changes + erasures + added:
        restored[edit['working_coordinate_index']] = edit['proposed']
    assert ''.join(restored) == target
    labels = []
    for i, char in enumerate(raw):
        if char.isdigit() or char in 'JQY':
            p = positions[i]
            labels.append({'plaintext_position': i, 'raw_label': char,
                           'editorial_character': candidate[i],
                           'source_pair': p['source_pair'],
                           'source_indices': p['source_coordinate_indices'],
                           'coordinates_preserved': all(frame[j] == target[j]
                                                        for j in p['working_coordinate_indices']),
                           'raw_context': raw[max(0, i - 8):i + 9]})
    return {'id': record['id'], 'source_literal': literal, 'source_slots': len(literal),
            'valid_source_coordinates': sum(c in CO for c in literal),
            'frame_model': record['frame_model'], 'analysis_frame': frame,
            'modeled_coordinates': len(frame), 'raw_plaintext': raw,
            'plaintext_positions': len(raw), 'baseline_fixed_positions': len(raw) - raw.count('?'),
            'positions': positions, 'editorial_plaintext': candidate,
            'editorial_ciphertext': target, 'candidate_fixed_positions': len(candidate),
            'known_coordinate_substitutions': changes, 'printed_erasure_fills': erasures,
            'inserted_coordinate_fills': added, 'raw_numeral_and_rare_label_inventory': labels,
            'key_changed': False, 'source_deletions': 0, 'source_reordering': False}


def gap_audit(inputs, record):
    key = inputs['key']
    ranks, square = key['column_rank_order'], key['square']
    literal, candidate = record['source_literal'], record['editorial_plaintext']
    target = record['editorial_ciphertext']
    masked = list(candidate)
    for span in inputs['gap_audit']['masked_spans']:
        assert candidate[span['start']:span['end']] == span['text']
        masked[span['start']:span['end']] = '?' * (span['end'] - span['start'])
    masked_target = encipher(''.join(masked), ranks, square)
    source = ''.join(c if c in CO else '?' for c in literal)
    size = len(source)
    prefixes = []
    for goal in (target, masked_target):
        offsets = []
        for offset in (0, 5, 10):
            counts = [0]
            for i, char in enumerate(source):
                counts.append(counts[-1] + (char != '?' and goal[i + offset] != '?' and char != goal[i + offset]))
            offsets.append(counts)
        prefixes.append(offsets)
    rows = []
    for first in range(size + 1):
        for second in range(first, size + 1):
            prices = []
            frame, _ = make_frame(literal, [first, second])
            for goal, (a, b, c) in zip((target, masked_target), prefixes):
                price = a[first] + b[second] - b[first] + c[size] - c[second]
                # Independent full-string alignment verifies each prefix-sum price.
                assert price == sum(x != '?' and y != '?' and x != y for x, y in zip(frame, goal))
                prices.append(price)
            rows.append((first, second, *prices))
    expected = 'first_gap\tsecond_gap\tfull_substitutions\tmasked_substitutions\n'
    expected += ''.join('\t'.join(map(str, row)) + '\n' for row in rows)
    assert expected == (HERE / 'two_group_costs.tsv').read_text()
    scopes = []
    for column, name in ((2, 'full_retrospective_template'), (3, 'masked_retrospective_template')):
        minimum = min(r[column] for r in rows)
        fits = [[r[0], r[1]] for r in rows if r[column] == minimum]
        scopes.append({'scope': name, 'minimum_observed_substitutions': minimum,
                       'minimizing_gap_pairs': fits,
                       'cost_histogram': {str(cost): count for cost, count in sorted(Counter(r[column] for r in rows).items())}})
    ties = scopes[1]['minimizing_gap_pairs']
    tied_readings = []
    for gaps in ties:
        frame, _ = make_frame(literal, gaps)
        tied_readings.append({'gaps': gaps, 'raw': decrypt(frame, ranks, square)})
    common = ''.join(chars[0] if chars[0] != '?' and len(set(chars)) == 1 else '?'
                     for chars in zip(*(r['raw'] for r in tied_readings)))
    one_gap = [{'gap': r[0], 'full_substitutions': r[2], 'masked_substitutions': r[3]}
               for r in rows if r[0] == r[1]]
    assert len(rows) == 24976 and len(one_gap) == 223
    assert scopes[0]['minimizing_gap_pairs'] == [[0, 0]]
    assert scopes[1]['minimizing_gap_pairs'] == [[0, 0], [1, 1], [1, 2], [2, 2], [3, 3]]
    return {'two_group_comparisons': len(rows), 'contiguous_gap_comparisons': len(one_gap),
            'two_group_costs_sha256': sha(HERE / 'two_group_costs.tsv'), 'scopes': scopes,
            'contiguous_gaps': one_gap, 'masked_minimum_raw_readings': tied_readings,
            'masked_minimum_common_raw': common,
            'masked_minimum_common_fixed_positions': len(common) - common.count('?'),
            'inference_limit': 'All templates were constructed after inspection. Their minima do not independently authenticate the original wording, loss location or loss mechanism.'}


def check_scores(inputs, record, models):
    scores = json.loads((HERE / 'candidate_scores.json').read_text())
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?'
    literal = record['source_literal']
    key = inputs['key']
    assert len(scores['candidates']) == len(literal) + 1 == 223
    for row in scores['candidates']:
        frame, _ = make_frame(literal, [row['gap'], row['gap']])
        assert row['raw'] == decrypt(frame, key['column_rank_order'], key['square'])
    for name, path in models.items():
        if path is None:
            continue
        assert sha(path) == scores['model_sha256'][name]
        model = array('f')
        model.frombytes(path.read_bytes())
        if sys.byteorder != 'little':
            model.byteswap()
        assert len(model) == 37 ** 4
        for row in scores['candidates']:
            a = [alphabet.index(c) for c in row['raw']]
            total = sum(model[((a[i] * 37 + a[i + 1]) * 37 + a[i + 2]) * 37 + a[i + 3]]
                        for i in range(len(a) - 3)) / (len(a) - 3)
            assert abs(total - row[name]) < 1e-12
    return {name: max(scores['candidates'], key=lambda r: r[name])['gap'] for name in scores['model_sha256']}


def build(pdf=None, book_model=None, radio_model=None):
    inputs = json.loads((HERE / 'inputs.json').read_text())
    published = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                     if k['id'] == inputs['key']['id'])
    assert inputs['key'] == published
    assert len(set(published['square'])) == 36
    assert sha(HERE / 'prior_candidates.json') == inputs['prior_candidates_sha256']
    for name in ('candidate_scores', 'two_group_costs'):
        suffix = '.json' if name == 'candidate_scores' else '.tsv'
        assert sha(HERE / (name + suffix)) == inputs['gap_audit'][name + '_sha256']
    for item in inputs['source_images']:
        assert sha(HERE / item['path']) == item['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf) == inputs['source']['pdf_sha256']
        assert pdf.stat().st_size == inputs['source']['pdf_bytes']
        doc = fitz.open(pdf)
        for item in inputs['source_images']:
            scale = item['render_scale']
            pix = doc[item['pdf_page_1based'] - 1].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*item['crop_pdf_points']))
            image = Image.open(HERE / item['path']).convert('RGB')
            assert image.size == (pix.width, pix.height)
            assert image.tobytes() == pix.samples
    records = [inspect(r, inputs['key']) for r in inputs['records']]
    damaged = next(r for r in records if r['id'] == 'p221_A5')
    audit = gap_audit(inputs, damaged)
    leaders = check_scores(inputs, damaged, {'book': book_model, 'radio': radio_model})
    summary = {'physical_records': len(records)}
    for name in ('source_slots', 'valid_source_coordinates', 'modeled_coordinates', 'plaintext_positions', 'baseline_fixed_positions', 'candidate_fixed_positions'):
        summary[name] = sum(r[name] for r in records)
    for name in ('known_coordinate_substitutions', 'printed_erasure_fills', 'inserted_coordinate_fills'):
        summary[name] = sum(len(r[name]) for r in records)
    summary.update({'source_deletions': 0, 'published_key_changed': False,
                    'p221_A5_common_raw_positions_across_masked_minima': audit['masked_minimum_common_fixed_positions']})
    assert summary['source_slots'] == 1352 and summary['plaintext_positions'] == 681
    assert summary['known_coordinate_substitutions'] == 24
    assert summary['printed_erasure_fills'] == 4 and summary['inserted_coordinate_fills'] == 10
    return {'schema': 'adfgvx-mackensen-armistice-certificate-v1', 'authors': inputs['authors'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'prior_credit': inputs['prior_credit'],
            'summary': summary, 'records': records, 'gap_audit': audit,
            'candidate_finding_score_leaders': leaders,
            'limits': ['The six-part body had already been identified by Childs and summarized by Lasry et al.; this is a source edition, not a first decipherment.',
                       'The 232-coordinate fifth-part frame and its supplied ten-coordinate prefix are conditional. A masked retrospective comparison retains five alternatives.',
                       'Raw numeral and rare-letter labels remain distinct from historical numerical meanings. Every ordinary-word repair involving such a label is costed.',
                       'ERFOLT retains the apparent omitted G. No plaintext character is silently inserted into that complete received frame.',
                       'The proposed body distinguishes merely acknowledging receipt, disarmament by Hungary and forgoing internment; historical conclusions inherit the local repair and missing-prefix assumptions.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--book-model', type=Path)
    parser.add_argument('--radio-model', type=Path)
    args = parser.parse_args()
    result = build(args.pdf, args.book_model, args.radio_model)
    target = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
