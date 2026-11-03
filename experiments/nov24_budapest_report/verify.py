#!/usr/bin/env python3
"""Verify p217 B2's complete native stream and exact teleprinter sentence.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import difflib
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
from experiments.romanian_pacification_consultation.verify import inspect


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def fold(text):
    return re.sub('[^A-Z0-9?]', '', text.upper())


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov22-24')
    assert len(set(key['square'])) == 36
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    prior = data['prior_candidates']
    assert sha(HERE / prior['path']) == prior['sha256']
    assert sha(ROOT / prior['source_path']) == prior['source_sha256']
    snapshots = load(HERE / prior['path'])
    assert snapshots == [r for r in load(ROOT / prior['source_path'])['unreviewed_cache_candidates']
                         if r['block'] == 'p217_ocr_block7']
    records = []
    for r in data['records']:
        source = ''.join(''.join(r['source_rows']).split())
        assert len(source) == r['source_slots'] == r['advertised_length'] == 176
        assert set(source) <= set('ADFGVX')
        mapping = list(range(len(source)))
        raw = inspect(source, key, mapping)
        assert raw['raw'] == r['expected_raw']
        assert raw['fixed_positions'] == len(raw['raw']) == 88
        assert decrypt(source, key['column_rank_order'], key['square']) == raw['raw']
        assert encrypt(raw['raw'], key['column_rank_order'], key['square']) == source
        span = r['readable_span']
        assert (span['start'], span['end']) == (29, 80)
        assert fold(span['german']) == raw['raw'][span['start']:span['end']]
        assert all(token in raw['raw'] for token in r['protected_fields'])
        case_path = ROOT / data['case']
        case_text = case_path.read_text()
        assert case_text.count(expected_legend(case_path)) == 1
        fences, quotes = displays(case_text)
        assert len(fences) == 2 and len(quotes) == 1
        assert [f['role_from_caption'] for f in fences] == ['raw_output', 'source_transcription']
        assert quotes[0]['role_from_caption'] == 'readable_german'
        fenced_bodies = re.findall(r'```text\n(.*?)\n```', case_text, re.S)
        assert fenced_bodies[0] == raw['raw']
        assert ''.join(fenced_bodies[1].split()) == source
        displayed_quote = re.findall(r'^> (.*)$', case_text, re.M)
        assert displayed_quote == [span['german']]

        old = snapshots[0]
        assert old['key'] == key['id']
        assert decrypt(old['ciphertext'], key['column_rank_order'], key['square']) == old['plaintext']
        ops = [list(op) for op in difflib.SequenceMatcher(None, old['ciphertext'], source, autojunk=False).get_opcodes()]
        rebuilt = ''.join(old['ciphertext'][i:j] if tag == 'equal' else source[u:v]
                          for tag, i, j, u, v in ops)
        assert rebuilt == source
        records.append({'id': r['id'], 'literal_source': source,
                        'ciphertext': source, 'source_slots': len(source),
                        'model_to_source_indices': mapping, **raw,
                        'ordinary_reencryption_exact': True,
                        'observed_coordinate_substitutions': [], 'source_mask_fills': [],
                        'readable_span': {**span, 'plaintext': fold(span['german']),
                                          'position_ledger': raw['positions'][29:80]},
                        'earlier_ocr': {'ciphertext': old['ciphertext'], 'plaintext': old['plaintext'],
                                       'alignment_opcodes': ops,
                                       'known_labels_before_source_review': len(old['plaintext']) - old['plaintext'].count('?')}})
    first = data['unaccepted_first_part']
    literal = ''.join(''.join(first['source_rows']).split())
    assert len(literal) == first['source_slots'] == 204 and set(literal) <= set('ADFGVX-')
    baseline = inspect(literal.replace('-', '?'), key, list(range(len(literal))))
    assert baseline['raw'] == first['expected_raw_native']
    assert literal[45:50] == literal[50:55] == 'FXXXF'
    return {'schema': 'adfgvx-nov24-budapest-report-certificate-v1',
            'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
            'summary': {'physical_records': 1, 'printed_source_slots': 176,
                        'plaintext_positions': 88, 'fixed_raw_positions': 88,
                        'readable_quoted_positions': 51, 'observed_coordinate_substitutions': 0,
                        'source_mask_fills': 0, 'added_or_excluded_source_slots': 0},
            'records': records,
            'unaccepted_first_part_diagnostic': {'id': first['id'], 'literal_source': literal,
                                               'native_baseline': baseline,
                                               'status': first['status']},
            'prior_credit': data['prior_credit']}, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    certificate, evidence = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert certificate == load(path)
    else:
        path.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
