#!/usr/bin/env python3
"""Price the conditional DES K.M. article while preserving the p72 A1 source.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from adfgvx.supplementary import calc as independent_calc
from experiments.romanian_pacification_consultation.verify import inspect, repair

CO = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(inp):
    baseline = inp['baseline']
    assert sha(ROOT / baseline['inputs']) == baseline['inputs_sha256']
    assert sha(ROOT / baseline['certificate']) == baseline['certificate_sha256']
    original, prior = load(ROOT / baseline['inputs']), load(ROOT / baseline['certificate'])
    record = next(r for r in original['records'] if r['id'] == baseline['record_id'])
    model = next(m for r in prior['records'] if r['id'] == baseline['record_id']
                 for m in r['models'] if m['id'] == baseline['model_id'])
    assert record['id'] == 'p72_A1' and baseline['model_id'] == 'printed_strikeout'
    key = original['key']
    registry = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Oct4-6')
    assert key['square'] == registry['square'] and key['column_rank_order'] == registry['column_rank_order']
    literal = record['literal_source']
    assert literal == re.sub('[()\\s]', '', ''.join(record['rows']))
    assert len(literal) == 203 and sum(c in CO for c in literal) == 202
    assert literal[136] == 'D' and literal[185] == 'U'
    assert record['layout_models'][0]['deletions'] == [[145, 170]]
    mapping = [i for i in range(203) if not 145 <= i < 170]
    assert mapping == model['layout_source_offsets']
    wire = ''.join(literal[i] if literal[i] in CO else '?' for i in mapping)
    assert wire == model['layout_ciphertext'] and len(wire) == record['advertised_length'] == 178
    native = inspect(wire, key, mapping)
    independent = independent_calc(wire, key)
    assert native['raw'] == independent['plaintext'] == inp['expected_raw'] == model['raw_plaintext']
    assert native['fixed_positions'] == 88
    assert [p['domain'] for p in native['positions']] == independent['plaintext_domains']
    assert inp['earlier_template'] == model['editorial_template'] == record['editorial_template']
    earlier = repair(inp['earlier_template'], wire, key, mapping, literal)
    assert len(earlier['known_coordinate_substitutions']) == 1 and not earlier['erased_coordinate_fills']
    assert [(e['source_index'], e['from'], e['to']) for e in earlier['known_coordinate_substitutions']] == [(125, 'F', 'V')]
    assert [(e['source_offset'], e['observed'], e['proposed']) for e in model['known_coordinate_substitutions']] == [(125, 'F', 'V')]
    assert model['erasure_fills'] == []
    template = list(inp['earlier_template'])
    for assignment in inp['assignments']:
        i = assignment['plaintext_index']
        assert template[i] == assignment['previous']
        template[i] = assignment['proposed']
    template = ''.join(template)
    assert template == inp['conditional_template']
    assert [(i, a, b) for i, (a, b) in enumerate(zip(inp['earlier_template'], template)) if a != b] == [
        (72, 'X', 'D'), (73, '?', 'E')]
    candidate = repair(template, wire, key, mapping, literal)
    assert candidate['fixed_positions'] == 89 and candidate['full_plaintext_reencryption_verified']
    assert [(e['source_index'], e['from'], e['to']) for e in candidate['known_coordinate_substitutions']] == [
        (125, 'F', 'V'), (136, 'D', 'G')]
    assert [(e['source_index'], e['printed'], e['to']) for e in candidate['erased_coordinate_fills']] == [(185, 'U', 'A')]
    assert independent_calc(candidate['ciphertext'], key)['plaintext'] == template
    assert encrypt(template, key['column_rank_order'], key['square']) == candidate['ciphertext']
    assert native['positions'][72]['pair'] == 'GD' and native['positions'][73]['pair'] == 'F?'
    assert native['positions'][73]['domain'] == '1EKLOS'
    witnesses, histogram = [], Counter()
    for first in ALPHABET:
        for second in native['positions'][73]['domain']:
            text = list(inp['earlier_template']); text[72:74] = [first, second]; text = ''.join(text)
            encoded = encrypt(text, key['column_rank_order'], key['square'])
            assert decrypt(encoded, key['column_rank_order'], key['square']) == text
            changes = [(mapping[i], a, b) for i, (a, b) in enumerate(zip(wire, encoded)) if a in CO and a != b]
            assert (125, 'F', 'V') in changes
            extra = [c for c in changes if c[0] != 125]
            assert set(i for i, _, _ in extra) <= set(native['positions'][72]['source_indices'])
            assert len(extra) in [0, 1, 2]
            histogram[len(extra)] += 1
            witnesses.append({'first_two_labels': first + second, 'local_text': text[72:79],
                              'additional_substitutions': [dict(source_index=i, before=a, after=b) for i, a, b in extra],
                              'source185_fill': encoded[mapping.index(185)],
                              'additional_observed_substitutions': len(extra),
                              'selected': text == template})
    assert len(witnesses) == 216 and dict(histogram) == {0: 6, 1: 60, 2: 150}
    assert sum(w['selected'] for w in witnesses) == 1
    case = (ROOT / inp['case']).read_text()
    section = case.split('### ' + inp['case_section'] + '\n', 1)[1].split('\n## ', 1)[0]
    assert re.findall(r'```text\n(.*?)\n```', section, re.S) == [template]
    quote = '\n'.join(line[2:] for line in section.splitlines() if line.startswith('> '))
    assert quote == inp['readable_german']
    assert re.sub('[^A-Z0-9?]', '', quote.upper()) == template.replace('X', '')
    return {'schema': 'adfgvx-p72-article-completion-certificate-v1', 'authors': inp['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'baseline': baseline,
            'summary': {'physical_records_added': 0, 'literal_source_slots': 203,
                        'source_instructed_strikeout_slots': 25, 'model_coordinates': 178,
                        'unchanged_raw_fixed_positions': 88, 'plaintext_positions': 89,
                        'earlier_edited_fixed_positions': 88, 'conditional_fixed_positions': 89,
                        'additional_observed_substitutions': 1, 'additional_invalid_glyph_fills': 1,
                        'total_observed_substitutions': 2, 'total_invalid_glyph_fills': 1,
                        'published_key_changed': False, 'source_frame_changed': False,
                        'exact_forward_witness_verified': True, 'local_label_candidates': 216,
                        'equally_priced_one_additional_substitution_candidates': 60},
            'literal_source': literal, 'model_to_source_indices': mapping,
            'native': native, 'earlier': earlier, 'conditional': candidate,
            'local_cost_census': {'additional_substitution_histogram': {str(k): histogram[k] for k in sorted(histogram)},
                                 'witnesses': witnesses}, 'limits': inp['limits'], 'credit': inp['credit']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    assert not (args.write and args.verify)
    inp = load(HERE / 'inputs.json'); certificate = build(inp)
    if args.write:
        (HERE / 'certificates.json').write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + '\n')
    else:
        assert certificate == load(HERE / 'certificates.json')
    evidence = verify_source_evidence(args.pdf, inp['source'], inp['source_images'], HERE)
    print(json.dumps({'verified': not args.write, **certificate['summary'],
                      'source_evidence': evidence['summary']}, indent=2))


if __name__ == '__main__':
    main()
