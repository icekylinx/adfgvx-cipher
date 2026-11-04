#!/usr/bin/env python3
"""Reproduce p225 erasure fills and the shared late-November FA=J proposal."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

CO = 'ADFGVX'
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def read(path):
    return json.loads((ROOT / path).read_text())


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def clean(source):
    return ''.join(c if c in CO else '?' for c in source)


def positions(source, ranks, square):
    n, width = len(source), len(ranks)
    heights = [n // width + (c < n % width) for c in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[c])
              for c in range(width)]
    order = [starts[p % width] + p // width for p in range(n)]
    assert sorted(order) == list(range(n))
    unused = set(AL) - set(square)
    result = []
    for p in range(n // 2):
        indices = order[2*p:2*p+2]
        pair = ''.join(source[i] for i in indices)
        values = set()
        for a, b in itertools.product(range(6), repeat=2):
            if pair[0] not in ('?', CO[a]) or pair[1] not in ('?', CO[b]):
                continue
            ch = square[6*a+b]
            values.update(unused if ch == '?' else ch)
        result.append({'plaintext_index': p, 'source_indices': indices,
                       'pair': pair, 'domain': ''.join(sorted(values))})
    raw = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in result)
    assert raw == decrypt(source, ranks, square)
    assert [p['domain'] for p in result] == plaintext_domains(source, ranks, square)
    return raw, result


def edit_words(source, ranks, square, specs):
    """Price named words only; leave other cells and all other source slots alone."""
    raw, ps = positions(clean(source), ranks, square)
    target = list(clean(source))
    for start, text in specs:
        for p, ch in enumerate(text, start):
            cell = square.index(ch)
            for i, value in zip(ps[p]['source_indices'], (CO[cell // 6], CO[cell % 6])):
                target[i] = value
    target = ''.join(target)
    changes = [{'source_index': i, 'from': a, 'to': b}
               for i, (a, b) in enumerate(zip(source, target)) if a in CO and a != b]
    fills = [{'source_index': i, 'literal': a, 'to': b}
             for i, (a, b) in enumerate(zip(source, target)) if a not in CO and b in CO]
    return target, changes, fills


def completions(square):
    cells = [i for i, c in enumerate(square) if c == '?']
    remaining = sorted(set(AL) - set(square))
    assert len(cells) == len(remaining)
    for values in itertools.permutations(remaining):
        full = list(square)
        for i, v in zip(cells, values):
            full[i] = v
        yield ''.join(full)


def check_readable(spec, plaintext):
    page = (ROOT / spec['case_path']).read_text()
    quotes = [' '.join(line[2:] for line in m[0].splitlines())
              for m in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', page, re.M)]
    assert spec['readable_german'] in quotes
    labels = re.sub('[^A-Z0-9?]', '', spec['readable_german'].upper())
    assert labels == plaintext.replace(spec['separator'], '')


def build():
    inputs = json.loads((HERE / 'inputs.json').read_text())
    for path, digest in inputs['dependencies'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == inputs['key_id'])
    base, ranks = key['square'], key['column_rank_order']

    service = inputs['service_completion']
    record = next(r for r in read(service['inputs'])['records'] if r['id'] == service['id'])
    source = literal(record)
    raw, ps = positions(clean(source), ranks, base)
    assert raw == record['expected_model_raw'] and len(source) == 232
    filled = list(raw)
    supports = []
    for fill in service['fills']:
        p, ch = fill['plaintext_index'], fill['symbol']
        assert raw[p] == '?' and ch in ps[p]['domain'] and ps[p]['pair'].count('?') == 1
        filled[p] = ch
        supports.append({**fill, **ps[p]})
    filled = ''.join(filled)
    assert filled == service['expected_filled']
    filled_cipher, changes, fills = edit_words(source, ranks, base, [(0, filled)])
    assert not changes and len(fills) == 6
    assert sum(x['literal'] == '-' for x in fills) == 5
    assert sum(x['literal'] == 'R' for x in fills) == 1
    assert encrypt(filled, ranks, base) == filled_cipher
    word = filled
    for replacement in service['word_replacements']:
        assert word.count(replacement['old']) == 1
        word = word.replace(replacement['old'], replacement['new'])
    assert word == service['expected_word']
    word_cipher, word_changes, word_fills = edit_words(source, ranks, base, [(0, word)])
    assert len(word_changes) == 2 and word_fills == fills
    assert encrypt(word, ranks, base) == word_cipher
    check_readable(service, word)
    service_result = {
        'id': service['id'], 'literal': source, 'raw': raw,
        'raw_fixed': len(raw) - raw.count('?'), 'positions': len(raw),
        'fill_support': supports, 'filled_plaintext': filled,
        'source_mask_fills': fills, 'filled_ciphertext': filled_cipher,
        'filled_fixed': len(filled), 'filled_observed_substitutions': changes,
        'word_plaintext': word, 'word_observed_substitutions': word_changes,
        'word_ciphertext': word_cipher, 'word_fixed': len(word),
        'readable_german': service['readable_german'],
        'published_key_changed': False,
    }

    joint = inputs['shared_J']
    prior = read('experiments/late_key_interpretation/certificate.json')['conditional_squares'][key['id']][-1]
    assert prior['id'] == joint['prior_layer'] and prior['square'] == joint['prior_square']
    assert prior['remaining_symbols'] == joint['prior_unused_symbols']
    cell = base.index(joint['baseline_label'])
    assert CO[cell // 6] + CO[cell % 6] == joint['coordinate_pair']
    assert prior['square'][cell] == '?' and joint['proposed_symbol'] not in prior['square']
    new = list(prior['square'])
    new[cell] = joint['proposed_symbol']
    new = ''.join(new)
    assert new == joint['new_square'] and ''.join(sorted(set(AL)-set(new))) == joint['remaining_symbols']
    full_squares = list(completions(new))
    assert len(list(completions(prior['square']))) == 120 and len(full_squares) == 24
    results = []
    for donor in joint['witnesses']:
        rec = next(r for r in read(donor['inputs'])['records'] if r['id'] == donor['id'])
        src = literal(rec)
        assert all(c in CO for c in src)
        baseline, bp = positions(src, ranks, base)
        assert baseline == rec['expected_raw']
        at, text = donor['word_start'], donor['proposed_word']
        assert baseline[at:at+len(text)] == donor['native_word']
        old_cipher, old_changes, old_fills = edit_words(src, ranks, base, [(at, text)])
        assert len(old_changes) == 2 and not old_fills
        before, _ = positions(src, ranks, prior['square'])
        after, np = positions(src, ranks, new)
        support = np[donor['plaintext_index']]
        assert support['pair'] == 'FA' and support['domain'] == 'J'
        assert after[at:at+len(text)] == text
        specs = [(at, text)]
        for replacement in donor['remaining_word_repairs']:
            assert baseline.count(replacement['old']) == 1
            specs.append((baseline.index(replacement['old']), replacement['new']))
        repaired, new_changes, new_fills = edit_words(src, ranks, new, specs)
        assert not new_fills
        old_repaired, all_old_changes, _ = edit_words(src, ranks, base, specs)
        assert len(all_old_changes) == len(new_changes) + 2
        conditional_word, _ = positions(repaired, ranks, new)
        check_readable(donor, conditional_word)
        witnesses = []
        for square in full_squares:
            native_text = decrypt(src, ranks, square)
            edited_text = decrypt(repaired, ranks, square)
            assert native_text[at:at+len(text)] == text
            assert encrypt(native_text, ranks, square) == src
            assert encrypt(edited_text, ranks, square) == repaired
            assert all(a == '?' or a == b for a, b in zip(conditional_word, edited_text))
            witnesses.append({'remaining_assignment': {CO[i//6]+CO[i%6]: square[i]
                              for i, c in enumerate(new) if c == '?'},
                              'native_plaintext': native_text,
                              'edited_plaintext': edited_text})
        results.append({
            'id': donor['id'], 'source_slots': len(src), 'literal': src,
            'baseline': baseline, 'prior_interpreted': before,
            'new_interpreted': after, 'word_interpreted': conditional_word,
            'fixed_before_J': len(before)-before.count('?'),
            'fixed_after_J': len(after)-after.count('?'),
            'original_pair_support': support,
            'baseline_J_repairs': old_changes,
            'baseline_all_word_repairs': all_old_changes,
            'new_word_repairs': new_changes, 'new_ciphertext': repaired,
            'global_witness_count': len(witnesses), 'global_witnesses': witnesses,
            'readable_german': donor['readable_german'],
        })
    assert sum(len(r['baseline_all_word_repairs']) for r in results) == 6
    assert sum(len(r['new_word_repairs']) for r in results) == 2
    return {'schema': 'adfgvx-late-november-joint-certificate-v1',
            'authors': inputs['authors'], 'input_sha256': hashlib.sha256((HERE/'inputs.json').read_bytes()).hexdigest(),
            'indexing': 'Zero-based source and plaintext positions.',
            'service_completion': service_result,
            'shared_J': {'prior_square': prior['square'], 'square': new,
                         'remaining_symbols': joint['remaining_symbols'],
                         'prior_global_assignments': 120, 'global_assignments': 24,
                         'records': results},
            'limits': inputs['limits']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    destination = HERE / 'certificates.json'
    if args.verify:
        assert json.loads(destination.read_text()) == result
    else:
        destination.write_text(json.dumps(result, indent=2) + '\n')
    print('p225 A: 110 → 116/116; six source fills, zero observed changes; two separately priced word repairs.')
    print('p225 B2 + p227 D: shared original FA=J; observed word-repair cost 6 → 2; 24 joint square witnesses.')


if __name__ == '__main__':
    main()
