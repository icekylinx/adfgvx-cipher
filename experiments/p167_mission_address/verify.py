#!/usr/bin/env python3
"""Verify the native p167 C1 service address and both global digit completions.

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


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov7-9')
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    old = data['prior_ocr']
    assert sha(HERE / old['path']) == old['sha256']
    assert sha(ROOT / old['origin']) == old['origin_sha256']
    prior = load(HERE / old['path'])
    assert prior == next(r for r in load(ROOT / old['origin'])['blocks'] if r['id'] == prior['id'])
    records = []
    for r in data['records']:
        literal = ''.join(''.join(r['source_rows']).split())
        assert len(literal) == r['source_slots'] == r['advertised_length'] == 132
        assert [(i, c) for i, c in enumerate(literal) if c not in C] == [(14, '-'), (90, 'Z')]
        frame = ''.join(c if c in C else '?' for c in literal)
        mapping = list(range(len(literal)))
        raw = inspect(frame, key, mapping)
        assert raw['raw'] == r['expected_raw'] and raw['fixed_positions'] == 61
        candidate = repair(r['readable_candidate'], frame, key, mapping, literal)
        assert candidate['fixed_positions'] == 63
        assert len(candidate['known_coordinate_substitutions']) == 6
        assert len(candidate['erased_coordinate_fills']) == 2
        assert [(e['source_index'], e['from'], e['to']) for e in candidate['known_coordinate_substitutions']] == [
            (20, 'D', 'X'), (23, 'D', 'X'), (83, 'V', 'D'), (84, 'D', 'X'),
            (114, 'V', 'X'), (126, 'X', 'D')]
        assert [(e['source_index'], e['to']) for e in candidate['erased_coordinate_fills']] == [(14, 'G'), (90, 'X')]
        for token in r['protected_fields']:
            assert token in raw['raw'] and token in candidate['raw']
        expected_unknowns = [(53, 'XA'), (61, 'VF'), (63, 'XA')]
        actual_unknowns = [(p['plaintext_index'], p['pair']) for p in candidate['positions'] if p['raw'] == '?']
        assert actual_unknowns == expected_unknowns
        assert all(p['domain'] == '56' for p in candidate['positions'] if p['raw'] == '?')
        unused = sorted(set(A) - set(key['square']))
        assert unused == ['5', '6'] and key['square'].count('?') == 2
        completions = []
        for values in itertools.permutations(unused):
            it = iter(values)
            square = ''.join(next(it) if c == '?' else c for c in key['square'])
            assert len(set(square)) == 36
            plaintext = decrypt(candidate['ciphertext'], key['column_rank_order'], square)
            assert encrypt(plaintext, key['column_rank_order'], square) == candidate['ciphertext']
            assert all(a == '?' or a == b for a, b in zip(candidate['raw'], plaintext))
            assert plaintext[53] == plaintext[63] and plaintext[61] != plaintext[63]
            completions.append({'square': square, 'plaintext': plaintext,
                                'alpha': plaintext[53], 'beta': plaintext[61],
                                'roem_field': plaintext[53], 'kr_field': plaintext[58:64],
                                'roundtrip_verified': True, 'historical_assignment_claim': False})
        assert {x['kr_field'] for x in completions} == {'130615', '130516'}
        optional = repair(r['optional_separator_candidate'], frame, key, mapping, literal)
        assert len(optional['known_coordinate_substitutions']) == 8
        assert len(optional['erased_coordinate_fills']) == 2
        assert [(i, a, b) for i, (a, b) in enumerate(zip(candidate['raw'], optional['raw'])) if a != b] == [(5, 'B', 'X')]
        extra = [e for e in optional['known_coordinate_substitutions']
                 if e['source_index'] not in {e['source_index'] for e in candidate['known_coordinate_substitutions']}]
        assert [(e['source_index'], e['from'], e['to']) for e in extra] == [(13, 'G', 'V'), (113, 'X', 'V')]
        assert re.sub('[^A-Z0-9?]', '', r['readable_german'].upper()) == candidate['raw'].replace('X', '')
        records.append({'id': r['id'], 'literal_source': literal, 'source_slots': len(literal),
                        'valid_source_coordinates': 130, 'ciphertext': frame,
                        'model_to_source_indices': mapping, **raw,
                        'readable_candidate': candidate, 'readable_german': r['readable_german'],
                        'global_completion_witnesses': completions,
                        'optional_separator_proposal': optional,
                        'optional_extra_observed_substitutions': extra})
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert [f['role_from_caption'] for f in fences] == ['raw_output', 'edited_output', 'source_transcription']
    assert len(quotes) == 1 and quotes[0]['role_from_caption'] == 'readable_german'
    assert re.findall(r'```text\n(.*?)\n```', text, re.S) == [records[0]['raw'], records[0]['readable_candidate']['raw'], '\n'.join(data['records'][0]['source_rows'])]
    assert re.findall(r'^> (.*)$', text, re.M) == [data['records'][0]['readable_german']]
    return {'schema': 'adfgvx-gap21-armistice-source-certificate-v1',
            'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
            'indexing': data['indexing'],
            'summary': {'physical_records': 1, 'printed_source_slots': 132,
                        'valid_source_coordinates': 130, 'modeled_coordinates': 132,
                        'plaintext_positions': 66, 'baseline_fixed_positions': 61,
                        'candidate_fixed_positions': 63, 'candidate_unknown_positions': 3,
                        'known_coordinate_substitutions': 6, 'source_mask_fills': 2,
                        'added_or_excluded_source_slots': 0,
                        'globally_consistent_square_completions': 2,
                        'optional_separator_total_observed_substitutions': 8,
                        'published_key_changed': False},
            'records': records, 'header': data['header'], 'prior_credit': data['prior_credit'],
            'limits': data['limits']}, evidence


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
