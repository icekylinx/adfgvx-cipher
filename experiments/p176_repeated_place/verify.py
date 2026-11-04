#!/usr/bin/env python3
"""Audit a conditional repeated place in p176 A6 without changing source bits.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import permutations
import json
from math import prod
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(ref):
    path = ROOT / ref['path']
    assert sha(path) == ref['sha256'], ref['path']
    return path


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def independent_read(wire, ranks, square):
    """Use explicit column lengths and offsets, independently of inspect()."""
    n, width = len(wire), len(ranks)
    height, remainder = divmod(n, width)
    lengths = [height + int(i < remainder) for i in range(width)]
    offsets = [sum(lengths[j] for j in range(width) if ranks[j] < ranks[i])
               for i in range(width)]
    origins = [offsets[i % width] + i // width for i in range(n)]
    assert sorted(origins) == list(range(n))
    missing = set(A) - set(square)
    out = []
    for i in range(n // 2):
        a, b = origins[2*i:2*i+2]
        pair = wire[a] + wire[b]
        rows = [C.index(pair[0])] if pair[0] in C else range(6)
        cols = [C.index(pair[1])] if pair[1] in C else range(6)
        domain = set()
        for row in rows:
            for col in cols:
                char = square[6*row + col]
                domain.update(missing if char == '?' else char)
        dom = ''.join(sorted(domain))
        out.append({'plaintext_index': i, 'pair': pair,
                    'source_indices': [a, b], 'domain': dom,
                    'raw': dom if len(dom) == 1 else '?'})
    assert [p['domain'] for p in out] == plaintext_domains(wire, ranks, square)
    assert ''.join(p['raw'] for p in out) == decrypt(wire, ranks, square)
    return out


def independent_encrypt(plain, ranks, square):
    columns = [[] for _ in ranks]
    cursor = 0
    for char in plain:
        row, col = divmod(square.index(char), 6)
        for coord in (C[row], C[col]):
            columns[cursor % len(ranks)].append(coord)
            cursor += 1
    return ''.join(''.join(columns[ranks.index(rank)])
                   for rank in range(1, len(ranks) + 1))


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    base = load(checked(data['baseline_inputs']))
    old_cert = load(checked(data['baseline_certificate']))
    companion = load(checked(data['companion_inputs']))
    checked(data['existing_source_image'])
    record = next(r for r in base['records'] if r['id'] == data['record_id'])
    key = base['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys']
                       if k['id'] == 'Nov10-12')
    ranks, square = key['column_rank_order'], key['square']
    lit = literal(record)
    wire = lit.replace('-', '?')
    mapping = list(range(len(lit)))
    assert len(lit) == 160 and lit[:74].count('-') == 0 and lit[74:] == '-'*86
    raw = inspect(wire, key, mapping)
    raw_positions = independent_read(wire, ranks, square)
    assert raw['raw'] == record['expected_raw'] and raw['fixed_positions'] == 14
    for a, b in zip(raw['positions'], raw_positions):
        assert all(a[k] == b[k] for k in b)
    before = repair(record['readable_candidate'], wire, key, mapping, lit)
    assert before == old_cert['records'][0]['readable_candidate']
    assert before['fixed_positions'] == 48
    assert not before['known_coordinate_substitutions']
    assert len(before['erased_coordinate_fills']) == 44
    candidates = []
    definitions = [
        ('repeated_word_only', data['word_only_span'], 9, 12),
        ('left_separator_only', {'start': 28, 'stop': 29, 'text': 'X'}, 1, 1),
        ('right_separator_only', {'start': 40, 'stop': 41, 'text': 'X'}, 1, 2),
        ('repeated_place_with_separators', data['proposed_span'], 11, 15),
        ('nonrepeated_blankenburg', data['equal_price_nonrepetition'], 11, 15),
    ]
    for name, span, gain, cost in definitions:
        start, stop = span['start'], span['stop']
        assert stop-start == len(span['text'])
        text = before['raw'][:start] + span['text'] + before['raw'][stop:]
        edited = repair(text, wire, key, mapping, lit)
        assert not edited['known_coordinate_substitutions']
        assert edited['fixed_positions'] == 48+gain
        assert len(edited['erased_coordinate_fills']) == 44+cost
        assert edited['ciphertext'][:74] == lit[:74]
        assert edited['raw'][56:] == before['raw'][56:]
        added_fills = []
        for i, (a, b) in enumerate(zip(before['ciphertext'], edited['ciphertext'])):
            if a != b:
                assert a == '?' and lit[i] == '-' and b in C
                owner = next(p for p in raw_positions if i in p['source_indices'])
                added_fills.append({'source_index': i,
                                    'plaintext_index': owner['plaintext_index'],
                                    'from': a, 'to': b})
        assert len(added_fills) == cost
        newly_fixed = [i for i, (a, b) in enumerate(zip(before['raw'], edited['raw']))
                       if a == '?' and b != '?']
        assert len(newly_fixed) == gain
        wholly_unobserved = [i for i in newly_fixed if raw_positions[i]['pair'] == '??']
        candidates.append({'name': name, 'span': span, 'edited': edited,
                           'added_printed_mask_fills': added_fills,
                           'newly_fixed_positions': newly_fixed,
                           'newly_fixed_wholly_unobserved_positions': wholly_unobserved})
    primary = candidates[3]
    assert primary['edited']['ciphertext'].count('?') == 27
    assert primary['newly_fixed_wholly_unobserved_positions'] == [29, 32, 37, 40]
    assert candidates[0]['newly_fixed_wholly_unobserved_positions'] == [29, 32, 37]
    # The inherited dative N versus separator X remains a separate equal-price choice.
    text = primary['edited']['raw']
    nx = repair(text[:11] + 'X' + text[12:], wire, key, mapping, lit)
    assert not nx['known_coordinate_substitutions']
    assert len(nx['erased_coordinate_fills']) == 59 and nx['fixed_positions'] == 59
    assert [(i, a, b) for i, (a, b) in enumerate(zip(primary['edited']['ciphertext'], nx['ciphertext']))
            if a != b] == [(151, 'D', 'G')]
    # Compare the two *native* word spans, before either phrase is supplied.
    paired = []
    for i in range(11):
        a, b = raw_positions[17+i], raw_positions[29+i]
        domain = ''.join(sorted(set(a['domain']) & set(b['domain'])))
        assert domain and data['word_only_span']['text'][i] in domain
        paired.append({'word_index': i, 'first_native': a, 'second_native': b,
                       'intersection_under_partial_square': domain,
                       'proposed_letter': data['word_only_span']['text'][i],
                       'forced_given_repeated_word': len(domain) == 1})
    assert [(p['word_index'], p['intersection_under_partial_square']) for p in paired
            if p['forced_given_repeated_word']] == [(1,'L'),(2,'A'),(6,'N'),(9,'R'),(10,'G')]
    # Each complete square has six independent free word positions: 6^6 strings.
    # Partial-square unions are not multiplied: their digit choices are correlated.
    missing = sorted(set(A) - set(square))
    assert missing == list('56789') and square.count('?') == 5
    witnesses = []
    for digits in permutations(missing):
        it = iter(digits)
        completed = ''.join(next(it) if c == '?' else c for c in square)
        assert len(set(completed)) == 36
        positions = independent_read(wire, ranks, completed)
        domains = [''.join(sorted(set(positions[17+i]['domain']) & set(positions[29+i]['domain'])))
                   for i in range(11)]
        assert [len(d) for d in domains] == [6,1,1,6,6,6,1,6,6,1,1]
        assert prod(map(len, domains)) == 46656
        texts = {}
        for candidate in candidates + [{'name': 'inherited_X_at_11', 'edited': nx}]:
            ed = candidate['edited']
            full_wire = ed['ciphertext'].replace('?', 'A')
            plain = decrypt(full_wire, ranks, completed)
            assert encrypt(plain, ranks, completed) == full_wire
            assert independent_encrypt(plain, ranks, completed) == full_wire
            assert all(a == '?' or a == b for a, b in zip(ed['raw'], plain))
            assert full_wire[:74] == lit[:74]
            if candidate['name'] in ('repeated_place_with_separators', 'nonrepeated_blankenburg'):
                texts[candidate['name']] = plain
        witnesses.append({'square': completed, 'unknown_values_in_square_order': ''.join(digits),
                          'zero_error_common_strings_under_repetition': 46656,
                          'all_six_variant_roundtrips_verified': True,
                          'witness_plaintexts': texts})
    assert len(witnesses) == 120
    # A small native repeated-number witness comes from the same source assembly.
    context = data['native_repetition_context']
    rep = next(r for r in companion['records'] if r['id'] == context['record_id'])
    assert companion['assembly']['sequence'][0] == context['record_id']
    assert companion['assembly']['sequence'][-1] == 'p176_A6_unread'
    rep_wire = literal(rep).replace('-', '?')
    rep_read = independent_read(rep_wire, ranks, square)
    rep_raw = ''.join(p['raw'] for p in rep_read)
    assert rep_raw == rep['expected_raw']
    at = rep_raw.index(context['text'])
    context_positions = rep_read[at:at+len(context['text'])]
    assert all('?' not in p['pair'] for p in context_positions)
    displayed = re.findall(r'```text\n(.*?)\n```', (HERE/'README.md').read_text(), re.S)
    assert displayed == [raw['raw'], before['raw'], primary['edited']['raw']]
    evidence = verify_source_evidence(pdf, base['source'],
                                     [c for c in base['source_images'] if c['id'] == 'p176_A6'],
                                     ROOT / 'experiments/p176_coal_train_fragment')
    return {
        'schema': 'adfgvx-p176-repeated-place-certificate-v1',
        'authors': data['authors'], 'input_sha256': sha(HERE/'inputs.json'),
        'indexing': data['indexing'],
        'summary': {'physical_records': 1, 'new_physical_records': 0,
                    'source_slots': 160, 'observed_source_coordinates': 74,
                    'printed_source_masks': 86, 'native_raw_fixed_positions': 14,
                    'prior_edited_fixed_positions': 48, 'proposed_fixed_positions': 59,
                    'new_proposed_fixed_positions': 11,
                    'new_observed_substitutions': 0, 'new_printed_mask_fills': 15,
                    'full_candidate_observed_substitutions': 0,
                    'full_candidate_printed_mask_fills': 59,
                    'remaining_unfilled_masks': 27,
                    'new_wholly_unobserved_plaintext_positions': [29,32,37,40],
                    'source_slots_added_removed_or_reordered': 0,
                    'global_square_completions_checked': 120,
                    'variants_checked_per_completion': 6,
                    'historical_uniqueness_claim': False},
        'literal_source': lit, 'raw': raw, 'prior_edited': before,
        'candidates': candidates, 'inherited_equal_price_X_at_11': nx,
        'native_paired_word_intersections': paired,
        'repetition_assumption_limit': 'Equality of the two words is an explicit hypothesis. The native source forces five of eleven shared letters only after making that hypothesis. Each complete square still permits 46,656 common strings.',
        'same_message_repeated_number_witness': {'id': context['record_id'],
            'text': context['text'], 'start': at, 'positions': context_positions,
            'observed_substitutions': 0, 'printed_mask_fills': 0,
            'assembly': companion['assembly'], 'limit': context['claim']},
        'roundtrip_witnesses': witnesses,
        'roundtrip_limit': 'Every remaining coordinate mask is arbitrarily A only in these witnesses. Such fills do not enter the published proposal. The repeated-place and Blankenburg witnesses each use 27 arbitrary fills.',
        'limits': data['limits'],
    }, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result, evidence = build(args.pdf)
    out = HERE / 'certificates.json'
    if args.verify:
        assert result == load(out)
    else:
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
