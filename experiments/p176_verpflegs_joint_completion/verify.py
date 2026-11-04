#!/usr/bin/env python3
"""Verify the optional A5 VERPFLEGSZ completion, retaining prior A5/A6 layers.

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


def load(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def literal(r):
    return ''.join(''.join(r['source_rows']).split())


def without_later_conditional_digits(text):
    """Validate the later C2 edition before comparing the frozen A5 displays."""
    certificate = ROOT / 'experiments/nov10_joint_completion/certificates.json'
    assert sha(certificate) == '8aabd2291564ec7edff555b30230e704a083edc3da4deaae8174faff16a457af'
    joint = load(certificate)
    c2 = next(r for r in joint['records'] if r['id'] == 'p175_C2')
    assert c2['fixed_after'] == c2['positions'] == 104
    assert c2['additional_observed_substitutions'] == c2['additional_source_fills'] == 0
    sections = list(re.finditer(r'^## Conditional shared digits\n.*?(?=^## |\Z)', text, re.M | re.S))
    assert len(sections) == 1
    section = sections[0]
    # Bind the complete new interpretation, caveats, quotation and evidence
    # drawer; arbitrary displays cannot be hidden under this later heading.
    assert hashlib.sha256(section.group().encode()).hexdigest() == '4edba39a7cc94f48b9b3b2ed6fe064e68b9429dab2feeb3c491f2959c8ce7930'
    assert re.findall(r'```text\n(.*?)\n```', section.group(), re.S) == [c2['selected_plaintext']]
    return text[:section.start()] + text[section.end():]


def build(pdf=None):
    d = load(HERE / 'inputs.json')
    k = d['key']
    assert k == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov10-12')
    evidence = verify_source_evidence(pdf, d['source'], d['source_images'], HERE)
    assert sha(HERE / d['context_snapshot']['path']) == d['context_snapshot']['sha256']
    snap = load(HERE / d['context_snapshot']['path'])
    for name in ['A5', 'A6']:
        assert sha(ROOT / snap[name + '_origin']) == snap[name + '_origin_sha256']
    r = d['records'][0]
    s = literal(r)
    assert s == literal(snap['prior_A5_record']) and len(s) == 168
    assert s.count('-') == 5 and s[50:55] == '-----'
    frame = s.replace('-', '?')
    mp = list(range(168))
    raw = inspect(frame, k, mp)
    assert raw['raw'] == r['expected_raw'] and raw['fixed_positions'] == 79
    prior = repair(snap['prior_A5_record']['readable_candidate'], frame, k, mp, s)
    assert prior['fixed_positions'] == 83
    assert prior['positions'][78]['pair'] == '?G'
    assert prior['positions'][78]['domain'] == '56789JQSUZ'
    assert prior['positions'][78]['source_indices'] == [50, 136]
    candidate = repair(r['readable_candidate'], frame, k, mp, s)
    assert candidate['fixed_positions'] == 84 and candidate['full_plaintext_reencryption_verified']
    assert len(candidate['known_coordinate_substitutions']) == 3
    assert len(candidate['erased_coordinate_fills']) == 5
    assert candidate['known_coordinate_substitutions'] == prior['known_coordinate_substitutions']
    assert [(i, a, b) for i, (a, b) in enumerate(zip(prior['ciphertext'], candidate['ciphertext'])) if a != b] == [(50, '?', 'D')]
    assert [(i, a, b) for i, (a, b) in enumerate(zip(prior['raw'], candidate['raw'])) if a != b] == [(78, '?', 'S')]
    assert candidate['positions'][78]['pair'] == 'DG'
    assert re.sub('[^A-Z0-9?]', '', r['readable_german'].upper()) == candidate['raw'].replace('X', '')
    a6 = snap['A6_record']
    a6s = literal(a6)
    a6candidate = repair(a6['readable_candidate'], a6s.replace('-', '?'), k, list(range(160)), a6s)
    assert not a6candidate['known_coordinate_substitutions'] and len(a6candidate['erased_coordinate_fills']) == 44
    assert a6candidate['fixed_positions'] == 48
    assert a6candidate['raw'].startswith('KOHLENZUEGENUEBERKLAUSENBURG')
    assert a6candidate['raw'][41:56] == 'GERECHNETWERDEN'
    witnesses = []
    for values in itertools.permutations('56789'):
        it = iter(values)
        square = ''.join(next(it) if ch == '?' else ch for ch in k['square'])
        assert len(set(square)) == 36
        assert encrypt(candidate['raw'], k['column_rank_order'], square) == candidate['ciphertext']
        assert decrypt(candidate['ciphertext'], k['column_rank_order'], square) == candidate['raw']
        witnesses.append({'unknown_cell_assignment_in_square_order': ''.join(values), 'roundtrip_verified': True})
    assert len(witnesses) == 120
    text = (ROOT / d['case']).read_text()
    assert text.count(expected_legend(ROOT / d['case'])) == 1
    prior_displays = d['prior_case_displays']
    assert sha(HERE / prior_displays['path']) == prior_displays['sha256']
    old_displays = load(HERE / prior_displays['path'])
    section = text.split('## Optional VERPFLEGSZ completion\n', 1)[1].split('\n## ', 1)[0]
    fences, quotes = displays(section)
    assert [f['role_from_caption'] for f in fences] == ['edited_output'] and not quotes
    assert re.findall(r'```text\n(.*?)\n```', section, re.S) == [candidate['raw']]
    new_display = re.findall(r'```[^\n]*\n.*?\n```', section, re.S)
    prior_text = without_later_conditional_digits(text)
    all_displays = re.findall(r'```[^\n]*\n.*?\n```', prior_text, re.S)
    assert [f for f in all_displays if f not in new_display] == old_displays['fenced_displays']
    assert re.findall(r'^> .*$', prior_text, re.M) == old_displays['quoted_lines']
    assert raw['raw'] in text and prior['raw'] in text
    return {'schema': 'adfgvx-p176-verpflegs-joint-certificate-v1', 'authors': d['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': d['indexing'],
            'summary': {'physical_records': 1, 'printed_source_slots': 168,
                'valid_source_coordinates': 163, 'modeled_coordinates': 168,
                'plaintext_positions': 84, 'baseline_fixed_positions': 79,
                'prior_candidate_fixed_positions': 83, 'candidate_fixed_positions': 84,
                'known_coordinate_substitutions': 3, 'source_mask_fills': 5,
                'incremental_observed_substitutions': 0, 'incremental_source_mask_fills': 1,
                'added_or_excluded_source_slots': 0, 'published_key_changed': False,
                'global_square_completions_checked': 120},
            'records': [{'id': r['id'], 'literal_source': s, 'source_slots': 168,
                'valid_coordinates': 163, 'ciphertext': frame, 'model_to_source_indices': mp,
                **raw, 'prior_candidate': prior, 'readable_candidate': candidate,
                'readable_german': r['readable_german'], 'global_roundtrip_witnesses': witnesses}],
            'A6_context_excluded_from_summary': a6candidate,
            'limits': d['limits'], 'prior_credit': d['prior_credit']}, evidence


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    args = p.parse_args()
    result, evidence = build(args.pdf)
    if args.verify:
        assert result == load(HERE / 'certificates.json')
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary'], 'source_evidence': evidence['summary']}, indent=2))
