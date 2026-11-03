#!/usr/bin/env python3
"""Check the separately optional p127 B1 OSM field without changing its baseline.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt, decrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair
from data.reviews.check_reading_presentation import displays, expected_legend


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(pdf=None, hopman_image=None):
    data = load(HERE / 'osmanie_field.json')
    for name, digest in data['dependencies'].items():
        assert sha(HERE / name) == digest
    old_input = load(HERE / 'inputs.json')
    source_record = next(r for r in old_input['records'] if r['id'] == data['record_id'])
    old_cert = next(r for r in load(HERE / 'certificates.json')['records']
                    if r['id'] == data['record_id'])
    key = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == data['key_id'])
    assert key == next(k for k in old_input['keys'] if k['id'] == data['key_id'])
    assert len(set(key['square'])) == len(key['square']) == 36
    literal = ''.join(''.join(source_record['source_rows']).split())
    frame = literal.replace('-', '?')
    mapping = list(range(len(frame)))
    baseline = inspect(frame, key, mapping)
    assert baseline['raw'] == old_cert['raw'] and baseline['fixed_positions'] == 76
    prior = old_cert['readable_candidate']
    assert prior['raw'] == data['existing_candidate'] == source_record['readable_candidate']
    field = baseline['positions'][66]
    assert field['source_indices'] == [44, 111] and field['pair'] == 'X?'
    assert field['domain'] == data['field']['domain'] == '4CMNST'
    assert literal[44] == 'X' and literal[111] == '-'
    candidate = repair(data['optional_candidate'], frame, key, mapping, literal)
    assert candidate['fixed_positions'] == 80 and candidate['raw'][64:67] == 'OSM'
    assert candidate['raw'].replace('OSM', 'OS?') == prior['raw']
    assert candidate['positions'][66]['pair'] == 'XF'
    changes = [(i, a, b) for i, (a, b) in enumerate(zip(prior['ciphertext'], candidate['ciphertext'])) if a != b]
    assert changes == [(111, '?', 'F')]
    assert candidate['known_coordinate_substitutions'] == prior['known_coordinate_substitutions']
    fills = candidate['erased_coordinate_fills']
    assert len(candidate['known_coordinate_substitutions']) == 1 and len(fills) == 4
    assert [(e['source_index'], e['to']) for e in fills] == [(55, 'A'), (93, 'D'), (94, 'A'), (111, 'F')]
    assert [e for e in fills if e['source_index'] != 111] == prior['erased_coordinate_fills']
    assert encrypt(candidate['raw'], key['column_rank_order'], key['square']) == candidate['ciphertext']
    assert decrypt(candidate['ciphertext'], key['column_rank_order'], key['square']) == candidate['raw']
    assert 'WENNNICTMEHR' in candidate['raw']
    german = data['optional_readable_german']
    assert re.sub('[^A-Z0-9?]', '', german.upper()) == candidate['raw'].replace('X', '')
    case = ROOT / data['case']
    text = case.read_text()
    assert text.count(expected_legend(case)) == 1
    fences, quotes = displays(text)
    assert [f['role_from_caption'] for f in fences] == ['raw_output', 'edited_output', 'edited_output']
    assert [q['role_from_caption'] for q in quotes] == ['readable_german', 'readable_german']
    assert re.findall(r'```text\n(.*?)\n```', text, re.S) == [baseline['raw'], prior['raw'], candidate['raw']]
    assert re.findall(r'^> (.*)$', text, re.M) == [source_record['readable_german'], german]
    assert data['documentary_reference']['short_quote'] in text
    assert '4th NOVEMBER, 1918' in text and 'November 5th' in text
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    ref = data['documentary_reference']
    documentary = {'image_supplied': hopman_image is not None,
                   'encoded_bytes_checked': False, 'rgb_pixels_checked': False,
                   'manual_visual_review_recorded': True,
                   'scope': 'The visual reading is recorded separately; file/pixel checks do not automatically authenticate a historical interpretation.'}
    if hopman_image is not None:
        assert hopman_image.stat().st_size == ref['image_bytes'] and sha(hopman_image) == ref['image_sha256']
        from PIL import Image
        with Image.open(hopman_image) as image:
            rgb = image.convert('RGB')
            assert rgb.size == (ref['width'], ref['height'])
            assert hashlib.sha256(rgb.tobytes()).hexdigest() == ref['rgb_sha256']
        documentary.update(encoded_bytes_checked=True, rgb_pixels_checked=True)
    certificate = {'schema': 'adfgvx-p127-osmanie-field-certificate-v1', 'authors': data['authors'],
                   'input_sha256': sha(HERE / 'osmanie_field.json'),
                   'physical_body_added': False, 'key_changed': False,
                   'source_dates': data['source_dates'],
                   'baseline_raw': baseline['raw'], 'existing_candidate': prior['raw'],
                   'native_fixed_positions': 76, 'existing_candidate_fixed_positions': 79,
                   'optional_candidate_fixed_positions': 80, 'plaintext_positions': 80,
                   'additional_observed_substitutions': 0, 'additional_source_mask_fills': 1,
                   'total_observed_substitutions': 1, 'total_source_mask_fills': 4,
                   'field_source_evidence': field,
                   'optional_candidate': {k: v for k, v in candidate.items()
                                          if k != 'positions'},
                   'readable_german': german, 'documentary_reference': ref,
                   'published_call_sign_mapping': data['published_call_sign_mapping'],
                   'limits': data['limits']}
    return certificate, evidence, documentary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--hopman-image', type=Path)
    args = parser.parse_args()
    assert not (args.verify and args.write)
    result, evidence, documentary = build(args.pdf, args.hopman_image)
    target = HERE / 'osmanie_field_certificate.json'
    if args.write:
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    else:
        assert result == load(target)
    print(json.dumps({'verified': not args.write,
                      'physical_body_added': False, 'optional_fixed_positions': 80,
                      'additional_source_mask_fills': 1,
                      'source_evidence': evidence['summary'],
                      'documentary_evidence': documentary}, indent=2))
