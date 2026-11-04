#!/usr/bin/env python3
"""Recover BEVORSTEHEND and propagate the shared Y through the Kiev report.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_frame(literal, choices, duplicate):
    """Reconstruct all retained original positions before adding the gap."""
    removed = set()
    for choice, (first, second) in zip(choices, [(20, 25), (200, 205), (255, 260)]):
        if choice:
            start = second if choice == 1 else first
            removed.update(range(start, start + 5))
    if duplicate is not None:
        removed.update(range(duplicate, duplicate + 5))
    before = [i for i in range(85) if i not in removed]
    after = [i for i in range(85, len(literal)) if i not in removed]
    mapping = before + [None] * (294 - len(before) - len(after)) + after
    cipher = ''.join('?' if i is None else literal[i] for i in mapping)
    return cipher, mapping, sorted(removed)


def build(pdf=None, check_case=True):
    data = json.loads((HERE / 'kiev_completion_inputs.json').read_text())
    for path, sha in data['dependencies'].items():
        assert digest(ROOT / path) == sha, path
    source_dir = ROOT / data['source_package']
    source = load('kiev_completion_source', source_dir / 'verify.py')
    original, _ = source.build(pdf)
    assert original == json.loads((source_dir / 'certificates.json').read_text())
    manifest = json.loads((source_dir / 'inputs.json').read_text())
    names = load('kiev_completion_names', HERE / 'verify_names.py').build()
    assert names == json.loads((ROOT / data['shared_square_certificate']).read_text())
    reader = load('kiev_completion_reader', ROOT / 'experiments/nov25_letter_constraint/verify.py')
    partial = names['conditional_partial_square']
    baseline, ranks = manifest['key']['square'], manifest['key']['column_rank_order']
    literal, _, _ = source.parse_annotations(manifest['records'][0]['source_rows_annotated'])
    converted = ''.join('?' if c == '?' else partial[baseline.index(c)]
                        for c in manifest['primary_template'])
    models = []
    for choices, duplicate in itertools.product(itertools.product(range(3), repeat=3), [None, 0, 5]):
        native, mapping, excluded = independent_frame(literal, choices, duplicate)
        assert (native, mapping, excluded) == source.frame(literal, choices, duplicate)
        models.append((choices, duplicate, native, mapping, excluded))
    assert len(models) == 81
    scopes = {}
    for scope in data['scopes']:
        template = converted
        if scope['clause']:
            a, b = data['clause']['range']
            template = template[:a] + data['clause']['text'] + template[b:]
        for name in scope['names']:
            field = data['name_fields'][name]
            a, b = field['range']
            assert len(field['text']) == b - a
            template = template[:a] + field['text'] + template[b:]
        coords = ''.join('??' if c == '?' else reader.CO[partial.index(c) // 6] +
                         reader.CO[partial.index(c) % 6] for c in template)
        wanted = ''.join(coords[c::len(ranks)]
                         for c in sorted(range(len(ranks)), key=lambda c: ranks[c]))
        prices, candidates = [], []
        for choices, duplicate, native, mapping, excluded in models:
            edition = ''.join(b if b != '?' else a for a, b in zip(native, wanted))
            changes = [{'model_index': i, 'source_index': mapping[i], 'from': a, 'to': b,
                        'kind': 'inserted_fill' if a == '?' else 'observed_substitution'}
                       for i, (a, b) in enumerate(zip(native, edition)) if a != b]
            price = {
                'parenthetical_choices': list(choices), 'duplicate_excluded_start': duplicate,
                'observed_substitutions': sum(c['kind'] == 'observed_substitution' for c in changes),
                'inserted_fills': sum(c['kind'] == 'inserted_fill' for c in changes),
            }
            decoded = reader.read(edition, ranks, partial)
            assert all(a == '?' or a == b for a, b in zip(template, decoded['plaintext']))
            prices.append(price)
            candidates.append({
                **price, 'native_ciphertext': native, 'edition_ciphertext': edition,
                'frame_to_source_indices': mapping, 'excluded_source_indices': excluded,
                'conditional_plaintext': decoded['plaintext'], 'coordinate_changes': changes,
                'fixed_positions': sum(len(p['domain']) == 1 for p in decoded['positions']),
                'remaining_domains': [p for p in decoded['positions'] if len(p['domain']) != 1],
                'full_square_witness': reader.witness(edition, ranks, partial),
            })
        minimum = min(p['observed_substitutions'] for p in prices)
        minima = [r for r in candidates if r['observed_substitutions'] == minimum]
        choices = {tuple(r['parenthetical_choices']) for r in minima}
        assert choices == ({(2, 2, 0)} if scope['clause'] else {(1, 2, 0), (2, 2, 0)})
        assert {r['duplicate_excluded_start'] for r in minima} == {0, 5}
        assert len({r['inserted_fills'] for r in minima}) == 1
        assert len({r['fixed_positions'] for r in minima}) == 1
        summary = {
            'minimum_observed_substitutions': minimum, 'minimum_models': len(minima),
            'distinct_edited_streams': len({r['edition_ciphertext'] for r in minima}),
            'inserted_fills': minima[0]['inserted_fills'],
            'fixed_positions': minima[0]['fixed_positions'],
        }
        assert summary == scope['expected'], (scope['id'], summary)
        scopes[scope['id']] = {'conditional_template': template, 'summary': summary,
                               'all_geometry_prices': prices, 'all_minimum_models': minima}

    selected = next(r for r in scopes['clause']['all_minimum_models']
                    if r['duplicate_excluded_start'] == 0)
    mapping = selected['frame_to_source_indices']
    native = reader.read(selected['native_ciphertext'], ranks, partial)
    support = []
    for anchor in data['clause']['support']:
        p = native['positions'][anchor['plaintext_index']]
        assert p['pair'] == anchor['native_pair']
        assert p['frame_indices'] == anchor['model_indices']
        assert [mapping[i] for i in p['frame_indices']] == anchor['source_indices']
        assert anchor['value'] in p['domain']
        assert selected['conditional_plaintext'][anchor['plaintext_index']] == anchor['value']
        if 'fill' in anchor:
            i = anchor['fill']['model_index']
            assert mapping[i] is None and selected['native_ciphertext'][i] == '?'
            assert selected['edition_ciphertext'][i] == anchor['fill']['to']
        support.append({**p, 'source_indices': anchor['source_indices'], 'value': anchor['value']})
    y = data['shared_Y']
    pos = native['positions'][y['plaintext_index']]
    assert pos['pair'] == y['pair'] and pos['domain'] == 'Y'
    assert pos['frame_indices'] == y['model_indices']
    assert [mapping[i] for i in pos['frame_indices']] == y['source_indices']
    assert all(selected['native_ciphertext'][i] == selected['edition_ciphertext'][i]
               for i in pos['frame_indices'])
    assert selected['conditional_plaintext'][137:146] == y['conditional_signature']
    previous_signature = original['records'][0]['optional_name_candidates']['signature']
    removed = [{k: c[k] for k in ('source_index', 'from', 'to')}
               for c in previous_signature['known_coordinate_substitutions']
               if c['model_index'] in pos['frame_indices']]
    assert removed == y['removed_substitutions']
    combined = scopes['clause_all_names']['all_minimum_models'][0]
    remaining_repairs = {(c['source_index'], c['from'], c['to'])
                         for c in combined['coordinate_changes']
                         if c['kind'] == 'observed_substitution'}
    assert remaining_repairs == {(10, 'V', 'X'), (85, 'X', 'F'), (155, 'A', 'F')}
    source_summary = {
        'physical_records': 1, 'source_observations': len(literal),
        'modeled_coordinates': len(selected['native_ciphertext']),
        'excluded_observed_coordinates': len(selected['excluded_source_indices']),
        'added_unknown_slots': selected['native_ciphertext'].count('?'),
        'declared_source_models': len(models),
    }
    assert source_summary == data['expected_source']
    display = data['display']
    start, end = display['range']
    shown = scopes[display['scope']]['all_minimum_models'][0]['conditional_plaintext'][start:end]
    assert re.sub('[^A-Z0-9?]', '', display['german'].upper()) == shown.replace('X', '')
    if check_case:
        page = (ROOT / display['case']).read_text()
        assert display['german'] in page
        assert all('`' + f + '`' in page for f in display['fields'])
    return {
        'schema': 'adfgvx-kiev-clause-completion-certificate-v1',
        'authors': data['authors'], 'input_sha256': digest(HERE / 'kiev_completion_inputs.json'),
        'indexing': 'Zero-based plaintext, modeled-frame and original-source positions.',
        'source_summary': source_summary, 'conditional_square': partial,
        'clause_support': support, 'shared_Y_support': {**pos, 'source_indices': y['source_indices']},
        'removed_signature_substitutions': removed, 'scopes': scopes,
        'verified_display': display, 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'kiev_completion_certificate.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: s['summary'] for k, s in result['scopes'].items()}, indent=2))


if __name__ == '__main__':
    main()
