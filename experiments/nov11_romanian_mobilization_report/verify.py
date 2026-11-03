#!/usr/bin/env python3
"""Verify the p180 B2 source, terminal-loss frame and partial word proposal.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from __future__ import annotations

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
from adfgvx.cipher import decrypt, encrypt, untranspose
from experiments.romanian_pacification_consultation.verify import (
    inspect, permutation, repair, verify_crops,
)

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_case(data, raw, candidate, native):
    case = (ROOT / data['case']).read_text()
    record = data['record']
    assert 'Literal header: `' + record['literal_header'] + '`.' in case
    assert '`01.02` and `04.02`' in case
    assert '(jammed to end)' in case
    assert '\n'.join(record['source_rows']) in case
    for stream in (raw['raw'], candidate['raw'], native['raw']):
        assert '\n```text\n' + stream + '\n```\n' in case
    assert '> ' + record['readable_german'] + '\n' in case
    folded = ''.join(c for c in record['readable_german'].upper() if c in A + '?')
    assert folded == candidate['raw'].replace('X', '')
    assert 'KRIEGSZUSAND' in case and 'ZIMNICA' in case
    assert 'same unknown square cell' in case


from adfgvx.source_evidence import verify_source_evidence

def build(pdf=None):
    data = json.loads((HERE / 'inputs.json').read_text())
    record, key = data['record'], data['key']
    assert data['authors'] == 'icekylinx and GPT-6 Astra Pro'
    current_key = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
                       if k['id'] == key['id'])
    assert key == current_key
    for name, digest in data['prior_artifacts'].items():
        assert sha(HERE / name) == digest
    source_evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    print(json.dumps({'source_evidence': source_evidence['summary']}))

    literal = ''.join(''.join(record['source_rows']).split())
    assert set(literal) <= set(C + '-')
    assert len(literal) == record['source_slots'] == 235
    assert sum(c in C for c in literal) == record['valid_source_coordinates'] == 233
    assert [i for i, c in enumerate(literal) if c == '-'] == [200, 201]
    native_cipher = literal.replace('-', '?')
    native_order = permutation(235, key['column_rank_order'])
    native_middle = ''.join(native_cipher[i] for i in native_order)
    assert native_middle == untranspose(native_cipher, key['column_rank_order'])
    native_raw = decrypt(native_cipher, key['column_rank_order'], key['square'], allow_unpaired=True)
    native = {'ciphertext': native_cipher, 'source_slots': 235,
              'paired_plaintext_positions': 117, 'raw': native_raw,
              'fixed_positions': sum(c != '?' for c in native_raw),
              'unpaired_intermediate_coordinate': {
                  'intermediate_index': 234, 'coordinate': native_middle[-1],
                  'source_index': native_order[-1]},
              'limit': 'Unchanged native odd-frame diagnostic, not a readable recovery.'}

    assert record['advertised_length'] == record['model_length'] == 240
    assert record['added_unknown_tail_coordinates'] == 5
    assert record['source_note'] == '(jammed to end)'
    base = native_cipher + '?' * 5
    mapping = list(range(235)) + [None] * 5
    raw = inspect(base, key, mapping)
    assert raw['raw'] == record['expected_raw'] and raw['fixed_positions'] == 110
    candidate = repair(record['edited_output'], base, key, mapping, literal)
    assert candidate['fixed_positions'] == 116
    substitutions = candidate['known_coordinate_substitutions']
    fills = candidate['erased_coordinate_fills']
    source_fills = [e for e in fills if e['source_index'] is not None]
    tail_fills = [e for e in fills if e['source_index'] is None]
    assert [(e['source_index'], e['from'], e['to']) for e in substitutions] == [
        (93, 'A', 'D'), (117, 'V', 'X'), (195, 'X', 'V'), (216, 'F', 'G')]
    assert [(e['source_index'], e['to']) for e in source_fills] == [(201, 'X')]
    assert [(e['model_index'], e['to']) for e in tail_fills] == [
        (236, 'D'), (237, 'G'), (238, 'A'), (239, 'D')]
    proposal_positions = set()
    for span in record['word_proposals']:
        start, word = span['start'], span['text']
        assert candidate['raw'][start:start + len(word)] == word
        proposal_positions.update(range(start, start + len(word)))
    # Number/date fields outside the six disclosed word proposals cannot change.
    for i, (before, after) in enumerate(zip(raw['raw'], candidate['raw'])):
        if i not in proposal_positions:
            assert before == after

    unresolved = [p for p in candidate['positions'] if p['raw'] == '?']
    assert [p['plaintext_index'] for p in unresolved] == [19, 44, 66, 83]
    assert [p['domain'] for p in unresolved] == [
        '56789', '3456789CLO', '56789', '156789ENVX']
    assert [p['pair'] for p in unresolved] == ['XA', '?A', 'XA', '?X']
    assert [i for i, c in enumerate(candidate['ciphertext']) if c == '?'] == [200, 235]

    # All full-square assignments and both six-way coordinate masks are retained.
    missing_cells = [i for i, c in enumerate(key['square']) if c == '?']
    missing_labels = ''.join(sorted(set(A) - set(key['square'])))
    assert len(missing_cells) == 5 and missing_labels == '56789'
    digest = hashlib.sha256()
    witnesses = {}
    completed_count = 0
    for labels in itertools.permutations(missing_labels):
        square = list(key['square'])
        for cell, label in zip(missing_cells, labels):
            square[cell] = label
        square = ''.join(square)
        for a, b in itertools.product(C, repeat=2):
            chars = list(candidate['ciphertext'])
            chars[200], chars[235] = a, b
            complete = ''.join(chars)
            plain = decrypt(complete, key['column_rank_order'], square)
            assert encrypt(plain, key['column_rank_order'], square) == complete
            assert all(fixed == '?' or fixed == actual
                       for fixed, actual in zip(candidate['raw'], plain))
            assert plain[19] == plain[66]
            if a == 'X':
                assert plain[44] == plain[19]
            if b == 'X':
                assert plain[83] in missing_labels and plain[83] != plain[19]
            signature = ''.join(plain[i] for i in [19, 44, 66, 83])
            if signature not in witnesses:
                witnesses[signature] = {'residual_labels_19_44_66_83': signature,
                    'complete_square': square, 'extra_source200_fill': a,
                    'extra_added235_fill': b, 'complete_ciphertext': complete,
                    'complete_plaintext': plain, 'historical_completion_claim': False}
            digest.update((square + '|' + a + b + '|' + complete + '|' + plain + '\n').encode())
            completed_count += 1
    assert completed_count == 4320 and len(witnesses) == 270
    for i, position in enumerate([19, 44, 66, 83]):
        observed = ''.join(sorted(set(s[i] for s in witnesses)))
        assert observed == candidate['positions'][position]['domain']

    prior = json.loads((HERE / 'prior_candidates.json').read_text())
    assert prior['source_transcription_artifact']['record'][2] == record['source_rows']
    for trial in prior['recomputed_prior_trials']:
        assert decrypt(trial['ciphertext'], key['column_rank_order'], key['square'],
                       allow_unpaired=len(trial['ciphertext']) % 2 != 0) == trial['raw']
    assert prior['recomputed_prior_trials'][2]['raw'] == raw['raw']
    check_case(data, raw, candidate, native)
    return {'schema': 'adfgvx-source-located-terminal-loss-certificate-v1',
        'project': data['project'], 'authors': data['authors'],
        'input_sha256': sha(HERE / 'inputs.json'), 'indexing': 'All indices are zero-based.',
        'summary': {'physical_records': 1, 'printed_source_slots': 235,
            'valid_source_coordinates': 233, 'modeled_coordinates': 240,
            'plaintext_positions': 120, 'baseline_fixed_positions': 110,
            'candidate_fixed_positions': 116, 'known_coordinate_substitutions': 4,
            'printed_mask_fills': 1, 'added_model_slots': 5,
            'added_slot_fills': 4, 'unfilled_source_masks': 1,
            'unfilled_added_slots': 1, 'source_exclusions': 0,
            'published_key_changed': False},
        'record_id': record['id'], 'literal_header': record['literal_header'],
        'header_hour_alternatives': record['header_hour_alternatives'],
        'literal_source': literal, 'literal_printed_rows': record['source_rows'],
        'source_note': record['source_note'], 'native_diagnostic': native,
        'model_to_source_indices': mapping, 'ciphertext': base, **raw,
        'readable_candidate': candidate, 'readable_german': record['readable_german'],
        'residual_positions': unresolved,
        'global_completion_check': {'square_assignments': 120,
            'source200_added235_coordinate_choices': 36,
            'exact_reencryption_witnesses_checked': completed_count,
            'enumeration_sha256': digest.hexdigest(),
            'distinct_residual_label_tuples': len(witnesses),
            'all_distinct_residual_tuple_witnesses': [witnesses[s] for s in sorted(witnesses)],
            'limit': 'Additional fills and full-square assignments are nonhistorical witnesses, not changes to the primary proposal.'},
        'prior_credit': data['prior_credit'], 'limits': data['limits']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    out = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(out.read_text())
    else:
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
