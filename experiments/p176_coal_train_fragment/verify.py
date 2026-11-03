#!/usr/bin/env python3
"""Audit the contextual p176 A6 partial proposal without changing source bits.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def independent_encrypt(plain, ranks, square):
    """Construct actual column lists; do not use cipher/transposition helpers."""
    columns = [[] for _ in ranks]
    stream = []
    for ch in plain:
        row, col = divmod(square.index(ch), 6)
        stream.extend([C[row], C[col]])
    for i, coord in enumerate(stream):
        columns[i % len(ranks)].append(coord)
    return ''.join(''.join(columns[ranks.index(rank)])
                   for rank in range(1, len(ranks) + 1))


def fold(text):
    text = text.upper().replace('Ä', 'AE').replace('Ö', 'OE').replace('Ü', 'UE')
    return re.sub('[^A-Z0-9?]', '', text)


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov10-12')
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    snapshot = data['context_snapshot']
    assert sha(HERE / snapshot['path']) == snapshot['sha256']
    context = load(HERE / snapshot['path'])
    for prefix in ['input', 'certificate']:
        assert sha(ROOT / context[prefix + '_origin']) == context[prefix + '_origin_sha256']
    old = load(ROOT / context['input_origin'])
    assert context['prior_A6_contextual_unread_record'] == next(r for r in old['contextual_unread_records'] if r['id'] == 'p176_A6')
    c5 = context['prior_A5_input_record']
    assert c5 == next(r for r in old['records'] if r['id'] == 'p176_A5')
    lit5 = literal(c5)
    raw5 = inspect(lit5.replace('-', '?'), key, list(range(len(lit5))))
    assert raw5['raw'] == c5['expected_raw'] and raw5['fixed_positions'] == 79
    edit5 = repair(c5['readable_candidate'], lit5.replace('-', '?'), key, list(range(len(lit5))), lit5)
    assert {k: v for k, v in edit5.items() if k != 'positions'} == context['prior_A5_candidate']
    assert edit5['fixed_positions'] == 83 and len(edit5['known_coordinate_substitutions']) == 3
    assert len(edit5['erased_coordinate_fills']) == 4 and edit5['raw'].endswith('VERPFLEG?ZXUND')
    assert [(e['source_index'], e['from'], e['to']) for e in edit5['known_coordinate_substitutions']] == [(58, 'G', 'F'), (108, 'X', 'D'), (120, 'A', 'D')]
    assert [(e['source_index'], e['to']) for e in edit5['erased_coordinate_fills']] == [(51, 'F'), (52, 'G'), (53, 'D'), (54, 'A')]
    assert context['assembly']['sequence'][-2:] == ['p176_A5', 'p176_A6_unread']
    records = []
    for r in data['records']:
        lit = literal(r)
        assert lit == literal(context['prior_A6_contextual_unread_record'])
        assert len(lit) == r['source_slots'] == r['advertised_length'] == 160
        assert set(lit) <= set(C + '-') and lit[:74].count('-') == 0 and lit[74:] == '-' * 86
        frame = lit.replace('-', '?')
        mapping = list(range(160))
        raw = inspect(frame, key, mapping)
        assert raw['raw'] == r['expected_raw'] and raw['fixed_positions'] == 14
        candidate = repair(r['readable_candidate'], frame, key, mapping, lit)
        assert candidate['fixed_positions'] == 48 and candidate['raw'].count('?') == 32
        assert not candidate['known_coordinate_substitutions'] and len(candidate['erased_coordinate_fills']) == 44
        assert sum(ch == '?' for ch in candidate['ciphertext']) == 42
        assert all(a == b for a, b in zip(lit[:74], candidate['ciphertext'][:74]))
        for begin, end in r['retained_intervals']:
            assert candidate['raw'][begin:end] == raw['raw'][begin:end]
        for span in r['proposed_spans']:
            assert candidate['raw'][span['start']:span['stop']] == span['text']
        assert fold(r['readable_german'].replace('[…]', '')) == ''.join(s['text'] for s in r['proposed_spans'])
        alternative_text = candidate['raw'][:11] + 'X' + candidate['raw'][12:]
        alternative = repair(alternative_text, frame, key, mapping, lit)
        assert alternative['fixed_positions'] == 48 and not alternative['known_coordinate_substitutions']
        assert len(alternative['erased_coordinate_fills']) == 44
        assert [(i, a, b) for i, (a, b) in enumerate(zip(candidate['ciphertext'], alternative['ciphertext'])) if a != b] == [(151, 'D', 'G')]
        # Full completions prove compatibility, not historical wording. The
        # remaining 42 coordinate masks are arbitrarily A in every witness.
        unfilled = [i for i, ch in enumerate(candidate['ciphertext']) if ch == '?']
        witness_cipher = candidate['ciphertext'].replace('?', 'A')
        assert len(unfilled) == 42 and all(lit[i] == '-' for i in unfilled)
        unused = sorted(set(A) - set(key['square']))
        assert unused == list('56789') and key['square'].count('?') == 5
        witnesses = []
        for values in itertools.permutations(unused):
            it = iter(values)
            square = ''.join(next(it) if ch == '?' else ch for ch in key['square'])
            assert len(set(square)) == 36
            plaintext = decrypt(witness_cipher, key['column_rank_order'], square)
            assert encrypt(plaintext, key['column_rank_order'], square) == witness_cipher
            assert independent_encrypt(plaintext, key['column_rank_order'], square) == witness_cipher
            assert all(a == '?' or a == b for a, b in zip(candidate['raw'], plaintext))
            assert all(a not in C or a == b for a, b in zip(lit, witness_cipher))
            witnesses.append({'square': square, 'unknown_cell_values_in_square_order': ''.join(values),
                              'plaintext': plaintext, 'roundtrip_verified': True,
                              'independent_column_encoder_verified': True,
                              'historical_completion_claim': False})
        assert len(witnesses) == 120
        records.append({'id': r['id'], 'literal_source': lit, 'literal_printed_rows': r['source_rows'],
                        'source_slots': 160, 'valid_coordinates': 74,
                        'ciphertext': frame, 'model_to_source_indices': mapping, **raw,
                        'readable_candidate': candidate, 'readable_german': r['readable_german'],
                        'retained_intervals': r['retained_intervals'], 'proposed_spans': r['proposed_spans'],
                        'equal_price_X_alternative_at_11': alternative,
                        'remaining_source_mask_indices': unfilled,
                        'full_completion_witness_ciphertext': witness_cipher,
                        'witness_only_coordinate_fills': [{'source_index': i, 'to': 'A'} for i in unfilled],
                        'global_square_completion_witnesses': witnesses,
                        'witness_limit': 'The 42 extra A assignments occur only in constructed witnesses; they do not fill the published partial candidate or select historical text.'})
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert [f['role_from_caption'] for f in fences] == ['raw_output', 'edited_output', 'earlier_attributed_reading', 'source_transcription']
    assert len(quotes) == 1 and quotes[0]['role_from_caption'] == 'readable_german'
    assert re.findall(r'```text\n(.*?)\n```', text, re.S) == [records[0]['raw'], records[0]['readable_candidate']['raw'], edit5['raw'], '\n'.join(data['records'][0]['source_rows'])]
    assert re.findall(r'^> (.*)$', text, re.M) == [data['records'][0]['readable_german']]
    return {'schema': 'adfgvx-p176-coal-train-fragment-certificate-v1',
            'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': data['indexing'],
            'summary': {'physical_records': 1, 'printed_source_slots': 160,
                        'valid_source_coordinates': 74, 'printed_source_masks': 86,
                        'modeled_coordinates': 160, 'plaintext_positions': 80,
                        'baseline_fixed_positions': 14, 'candidate_fixed_positions': 48,
                        'candidate_unknown_positions': 32, 'known_coordinate_substitutions': 0,
                        'source_mask_fills': 44, 'remaining_unfilled_source_masks': 42,
                        'added_or_excluded_source_slots': 0, 'published_key_changed': False,
                        'global_injective_square_completions_checked': 120,
                        'full_source_retaining_roundtrip_witnesses': 120,
                        'witness_only_mask_fills_per_completion': 42,
                        'historical_uniqueness_claim': False},
            'records': records,
            'context_A5_excluded_from_new_record_counts': {'id': 'p176_A5', 'source_slots': 168,
                'baseline': raw5, 'candidate': edit5, 'prior_credit': data['prior_credit']['A5_context_and_source_review']},
            'header': data['header'], 'prior_credit': data['prior_credit'], 'limits': data['limits']}, evidence


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
    print(json.dumps({'verified': args.verify, **result['summary'], 'source_evidence': evidence['summary']}, indent=2))
