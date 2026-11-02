#!/usr/bin/env python3
"""Reproduce the fixed p153 CHI-key search of extracted, unverified OCR blocks.

Only Python's standard library is required. Ranking is a retrieval aid. This
experiment cannot exclude companions hidden by unmodelled source errors.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parent
ALPHABET = 'ADFGVX'


def untranspose(ciphertext, ranks):
    rows, extra = divmod(len(ciphertext), len(ranks))
    lengths = [rows + (column < extra) for column in range(len(ranks))]
    columns = [''] * len(ranks)
    cursor = 0
    for column in sorted(range(len(ranks)), key=lambda i: ranks[i]):
        columns[column] = ciphertext[cursor:cursor + lengths[column]]
        cursor += lengths[column]
    return ''.join(columns[column][row]
                   for row in range(rows + 1)
                   for column in range(len(ranks))
                   if row < lengths[column])


def decrypt(ciphertext, ranks, square):
    intermediate = untranspose(ciphertext, ranks)
    plain = []
    for offset in range(0, len(intermediate) - 1, 2):
        a, b = intermediate[offset:offset + 2]
        plain.append('?' if '?' in (a, b) else
                     square[6 * ALPHABET.index(a) + ALPHABET.index(b)].lower())
    orphan = intermediate[-1] if len(intermediate) % 2 else None
    return ''.join(plain), orphan


def variants(block):
    """Explicit OCR geometry hypotheses; never source corrections.

    Preserve the raw groups first. Try uniform left/right alignment to five
    characters and an invalid-character-first truncation rule. For at most three
    four- or six-character nonfinal groups, also enumerate one unknown insertion
    or one OCR-character deletion. No arbitrary whole-group insertion is tried.
    """
    groups = block['groups']
    raw = ''.join(groups)
    yield raw, []
    for side in ('left', 'right', 'invalid-first'):
        fixed, changes = [], []
        for i, group in enumerate(groups):
            new = group
            if i < len(groups) - 1 and 3 <= len(group) <= 7 and len(group) != 5:
                if len(group) < 5:
                    padding = '?' * (5 - len(group))
                    new = padding + group if side == 'left' else group + padding
                else:
                    if side == 'invalid-first':
                        while len(new) > 5 and '?' in new:
                            position = new.index('?')
                            new = new[:position] + new[position + 1:]
                    new = new[-5:] if side == 'left' else new[:5]
                changes.append({'group': i + 1, 'ocr_group': group,
                                'layout_hypothesis': new, 'method': side})
            fixed.append(new)
        if changes:
            yield ''.join(fixed), changes
    choices, affected = [], 0
    for i, group in enumerate(groups):
        if i < len(groups) - 1 and len(group) == 4:
            options = [(group[:position] + '?' + group[position:],
                        {'group': i + 1, 'insert_unknown_at': position})
                       for position in range(5)]
            affected += 1
        elif i < len(groups) - 1 and len(group) == 6:
            options = [(group[:position] + group[position + 1:],
                        {'group': i + 1, 'delete_ocr_character_at': position})
                       for position in range(6)]
            affected += 1
        else:
            options = [(group, None)]
        choices.append(options)
    if 1 <= affected <= 3:
        seen = {raw}
        for combination in itertools.product(*choices):
            ciphertext = ''.join(item[0] for item in combination)
            if ciphertext not in seen:
                seen.add(ciphertext)
                yield ciphertext, [item[1] for item in combination
                                   if item[1] is not None]


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(all_output=None):
    data = json.loads((ROOT / 'inputs.json').read_text())
    config = json.loads((ROOT / 'config.json').read_text())
    ranking = json.loads((ROOT / 'ranking_weights.json').read_text())
    square = config['body_square']
    assert len(square) == 36
    assert sorted(config['rank']) == list(range(1, 19))
    known = [letter for letter in square if letter != '?']
    assert len(known) == len(set(known))
    models = [('body_only', square),
              ('body_plus_AF_X_hypothesis', square[:2] + 'X' + square[3:])]
    rows, tested = [], 0
    all_digest = hashlib.sha256()
    output_stream = open(all_output, 'w') if all_output else None
    try:
        for block in data['blocks']:
            best = None
            for ciphertext, edits in variants(block):
                assert all(char in ALPHABET + '?' for char in ciphertext)
                for model_name, model_square in models:
                    plain, orphan = decrypt(ciphertext, config['rank'], model_square)
                    tested += 1
                    grams = [plain[i:i+4] for i in range(len(plain)-3)
                             if '?' not in plain[i:i+4]]
                    known_count = len(plain) - plain.count('?')
                    score = (sum(ranking['weights'].get(gram, ranking['floor'])
                                 for gram in grams) / len(grams)) if grams else -999
                    row = {'id': block['id'],
                           'printed_page': block['printed_page'],
                           'pdf_page_1based': block['pdf_page_1based'],
                           'source_slots': sum(map(len, block['groups'])),
                           'model_slots': len(ciphertext),
                           'square_model': model_name,
                           'plaintext': plain,
                           'known_plaintext_slots': known_count,
                           'fully_observed_quadgrams': len(grams),
                           'score': score,
                           'group_layout_hypotheses': edits,
                           'ciphertext_hypothesis': ciphertext,
                           'unpaired_intermediate_coordinate': orphan}
                    line = json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n'
                    all_digest.update(line.encode())
                    if output_stream:
                        output_stream.write(line)
                    minimum = config['filter_for_ranked_candidate']
                    if known_count < minimum['minimum_known_plaintext_slots']:
                        continue
                    if len(grams) < minimum['minimum_fully_observed_quadgrams']:
                        continue
                    if best is None or score > best['score']:
                        best = row
            if best:
                rows.append(best)
    finally:
        if output_stream:
            output_stream.close()
    rows.sort(key=lambda row: -row['score'])
    controls = []
    for control in config['controls']:
        readings = {}
        for name, model_square in models:
            plain, orphan = decrypt(control['ciphertext'], config['rank'], model_square)
            readings[name] = {'plaintext': plain,
                              'known_plaintext_slots': len(plain) - plain.count('?'),
                              'unpaired_intermediate_coordinate': orphan}
        controls.append({'id': control['id'], 'readings': readings})
    return {'schema': 'adfgvx-fixed-p153-corpus-screen-result-v1',
            'input_sha256': digest_file(ROOT / 'inputs.json'),
            'ranking_weights_sha256': digest_file(ROOT / 'ranking_weights.json'),
            'config_sha256': digest_file(ROOT / 'config.json'),
            'blocks': len(data['blocks']),
            'fixed_key_layout_models': tested,
            'all_model_results_sha256': all_digest.hexdigest(),
            'ranked_block_count': len(rows),
            'controls': controls,
            'top_candidates': rows[:20],
            'nearby_pages_146_to_170': [row for row in rows
                                      if 146 <= row['printed_page'] <= 170],
            'interpretation': 'The two p153 controls are the only coherent matches identified by source review. Other high-scoring outputs remain gibberish. This OCR retrieval experiment cannot exclude a same-key companion obscured by unmodelled errors.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true',
                        help='Compare the deterministic summary with the included result.')
    parser.add_argument('--output', type=Path, help='Write the reproduced summary JSON.')
    parser.add_argument('--all-output', type=Path,
                        help='Optionally write every model result as JSON Lines.')
    args = parser.parse_args()
    result = run(args.all_output)
    if args.verify:
        expected = json.loads((ROOT / 'expected_summary.json').read_text())
        assert result == expected, 'The reproduced output differs from the included summary.'
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': bool(args.verify), 'blocks': result['blocks'],
                      'fixed_key_layout_models': result['fixed_key_layout_models'],
                      'all_model_results_sha256': result['all_model_results_sha256']}))
