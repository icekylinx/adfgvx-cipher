#!/usr/bin/env python3
"""Replay a conditional p151/p157 copy relation without counting copied letters as raw.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
The original source editions are immutable dependencies, not revised inputs.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.romanian_pacification_consultation.verify import (
    C, inspect, permutation, repair, sha, verify_crops,
)


def frame(literal, prefix, boundaries):
    values, mapping = ['?'] * prefix, [None] * prefix
    for i in range(len(literal) + 1):
        if i in boundaries:
            values.append('?')
            mapping.append(None)
        if i < len(literal):
            values.append(literal[i] if literal[i] in C else '?')
            mapping.append(i)
    return ''.join(values), mapping


def costs(candidate, prefix):
    fills = candidate['erased_coordinate_fills']
    return {
        'observed_coordinate_substitutions': len(candidate['known_coordinate_substitutions']),
        'printed_mask_fills': sum(e['source_index'] is not None for e in fills),
        'missing_prefix_fills': sum(e['source_index'] is None and e['model_index'] < prefix for e in fills),
        'short_group_fills': sum(e['source_index'] is None and e['model_index'] >= prefix for e in fills),
    }


def compare(base, mapping, donor, donor_mapping, key):
    order = permutation(len(base), key['column_rank_order'])
    pair_for = {i: (j // 2, j % 2) for j, i in enumerate(order)}
    middle = ''.join(donor[i] for i in order)
    original = decrypt(donor, key['column_rank_order'], key['square'])
    agreements, conflicts = [], []
    for i, char in enumerate(base):
        if char not in C:
            continue
        if char == donor[i]:
            agreements.append({'model_index': i, 'p157_source_index': mapping[i],
                               'p151_source_index': donor_mapping[i], 'coordinate': char})
            continue
        plain_i, pair_offset = pair_for[i]
        altered = donor[:i] + char + donor[i + 1:]
        alternative = decrypt(altered, key['column_rank_order'], key['square'])
        assert [j for j, (a, b) in enumerate(zip(original, alternative)) if a != b] == [plain_i]
        pair = middle[2 * plain_i:2 * plain_i + 2]
        alt_pair = pair[:pair_offset] + char + pair[pair_offset + 1:]
        other_index = order[2 * plain_i + 1 - pair_offset]
        conflicts.append({
            'model_index': i, 'p157_source_index': mapping[i],
            'p151_source_index': donor_mapping[i],
            'p151_coordinate': donor[i], 'p157_coordinate': char,
            'other_p151_source_index': donor_mapping[other_index],
            'other_p151_coordinate': donor[other_index],
            'plaintext_index': plain_i, 'pair_coordinate_offset': pair_offset,
            'p151_pair': pair, 'p157_coordinate_with_other_p151_coordinate': alt_pair,
            'p151_label': original[plain_i], 'p157_label_with_other_p151_coordinate': alternative[plain_i],
        })
    return agreements, conflicts


def exact_runs(a, b, minimum):
    runs = []
    for i in range(len(a)):
        for j in range(len(b)):
            if i and j and a[i - 1] == b[j - 1] and a[i - 1] in C:
                continue
            n = 0
            while i + n < len(a) and j + n < len(b) and a[i + n] == b[j + n] and a[i + n] in C:
                n += 1
            if n >= minimum:
                runs.append({'p151_source_start': i, 'p157_source_start': j,
                             'length': n, 'literal': a[i:i + n]})
    return sorted(runs, key=lambda r: (-r['length'], r['p151_source_start'], r['p157_source_start']))


def build(pdf=None):
    data = json.loads((HERE / 'inputs.json').read_text())
    key = data['key']
    assert key == next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys'] if k['id'] == key['id'])
    for dependency in data['frozen_dependencies']:
        assert sha(ROOT / dependency['path']) == dependency['sha256'], dependency['path']
    for image in data['source_images']:
        assert sha(ROOT / image['path']) == image['sha256']
    if pdf:
        verify_crops(pdf, data['source'], data['source_images'], ROOT)

    earlier = json.loads((ROOT / data['independent_witness']['input_path']).read_text())
    old = next(r for r in earlier['records'] if r['id'] == 'p151_A1')
    witness = data['independent_witness']
    assert old['source_rows'] == witness['source_rows']
    donor_literal = ''.join(''.join(witness['source_rows']).split())
    assert len(donor_literal) == 189
    donor_base, donor_mapping = frame(donor_literal, 0, [55])
    donor_raw = inspect(donor_base, key, donor_mapping)
    assert donor_raw['raw'] == old['expected_raw'] == witness['prior_raw']
    prior = repair(witness['prior_readable_candidate'], donor_base, key, donor_mapping, donor_literal)
    assert prior['raw'] == old['readable_candidate']
    assert not prior['known_coordinate_substitutions']
    assert [(e['model_index'], e['to']) for e in prior['erased_coordinate_fills']] == [(55, 'D')]

    source = data['records'][0]
    literal = ''.join(''.join(source['source_rows']).split())
    previous_p157 = json.loads((ROOT / 'experiments/romanian_pacification_consultation/inputs.json').read_text())
    assert literal == previous_p157['contextual_unread_records'][0]['literal_source']
    assert len(literal) == 83 and sum(c in C for c in literal) == 78 and literal.count('-') == 5
    geometry = source['analysis_frame']
    assert literal[0:4] == 'XDDV' and literal[69:73] == 'XXXA'
    prefix = geometry['missing_prefix_slots']
    assert prefix == 105 and source['advertised_length'] is None
    primary_text = source['readable_candidate']
    assert primary_text == prior['raw'][:-8] + 'STURZFSS'

    alignments = []
    for first, second in itertools.product(geometry['first_short_group']['insertion_boundaries'],
                                            geometry['second_short_group']['insertion_boundaries']):
        base, mapping = frame(literal, prefix, [first, second])
        assert len(base) == geometry['length'] == 190
        raw = inspect(base, key, mapping)
        assert raw['fixed_positions'] == 0 and raw['raw'] == source['expected_raw']
        agreements, conflicts = compare(base, mapping, prior['ciphertext'], donor_mapping, key)
        candidate = repair(primary_text, base, key, mapping, literal)
        alignments.append({
            'insertion_boundaries': [first, second],
            'source_only_fixed_positions': raw['fixed_positions'],
            'observed_agreements_with_p151': len(agreements),
            'observed_conflicts_with_p151': len(conflicts),
            'conflicts': conflicts, 'primary_candidate_cost': costs(candidate, prefix),
            'short_group_fills': [e for e in candidate['erased_coordinate_fills']
                                  if e['source_index'] is None and e['model_index'] >= prefix],
        })
    minimum = min(a['observed_conflicts_with_p151'] for a in alignments)
    best = [a['insertion_boundaries'] for a in alignments if a['observed_conflicts_with_p151'] == minimum]
    assert minimum == 6 and best == [[3, 71], [3, 72], [4, 71], [4, 72]]
    assert min(a['primary_candidate_cost']['observed_coordinate_substitutions'] for a in alignments) == 5

    boundaries = geometry['primary_insertion_boundaries']
    assert boundaries == best[0]
    base, mapping = frame(literal, prefix, boundaries)
    raw = inspect(base, key, mapping)
    assert all('?' in point['pair'] for point in raw['positions'])
    candidate = repair(primary_text, base, key, mapping, literal)
    assert costs(candidate, prefix) == {
        'observed_coordinate_substitutions': 5, 'printed_mask_fills': 5,
        'missing_prefix_fills': 105, 'short_group_fills': 2,
    }
    agreements, conflicts = compare(base, mapping, prior['ciphertext'], donor_mapping, key)
    assert len(agreements) == 72 and len(conflicts) == 6
    assert [c['p157_source_index'] for c in conflicts] == [9, 10, 11, 12, 37, 71]

    # A source-choice family, not six independent claims of historical correction.
    alternatives = []
    for mask in range(1 << len(conflicts)):
        cipher = list(prior['ciphertext'])
        chosen = []
        for i, conflict in enumerate(conflicts):
            if mask & (1 << i):
                cipher[conflict['model_index']] = conflict['p157_coordinate']
                chosen.append(conflict['p157_source_index'])
        cipher = ''.join(cipher)
        plain = decrypt(cipher, key['column_rank_order'], key['square'])
        assert encrypt(plain, key['column_rank_order'], key['square']) == cipher
        donor_changes = sum(a in C and a != b for a, b in zip(donor_base, cipher))
        recipient_changes = sum(a in C and a != b for a, b in zip(base, cipher))
        assert donor_changes + recipient_changes == 6
        alternatives.append({'p157_coordinate_choices_at_source_indices': chosen,
                             'ciphertext': cipher, 'plaintext': plain,
                             'p151_observed_substitutions': donor_changes,
                             'p157_observed_substitutions': recipient_changes,
                             'combined_observed_substitutions': 6,
                             'roundtrip_verified': True})
    assert len({a['ciphertext'] for a in alternatives}) == 64
    selected = [a for a in alternatives if a['plaintext'] == primary_text]
    assert len(selected) == 1 and selected[0]['p157_coordinate_choices_at_source_indices'] == [37]

    # Copy fills produce a separate edited layer before any observed p157 repair.
    copied = ''.join(b if b in C else a for a, b in zip(prior['ciphertext'], base))
    copied_plain = decrypt(copied, key['column_rank_order'], key['square'])
    assert encrypt(copied_plain, key['column_rank_order'], key['square']) == copied
    assert copied_plain == 'OHLXBPHXNACHRICHBVONABREISSDEUTSCHERUAFFENSTILLSTANDSKOMMISSIONHATANSAHEINENDGEMELDETENSTURZFSS'
    fill_provenance = []
    for event in candidate['erased_coordinate_fills']:
        i = event['model_index']
        assert event['to'] == prior['ciphertext'][i]
        fill_provenance.append({**event, 'p151_source_index': donor_mapping[i],
                                'p151_basis': 'observed coordinate' if donor_mapping[i] is not None else 'prior conditional GEMELDETEN fill'})
    assert sum(e['p151_source_index'] is None for e in fill_provenance) == 1

    donor_primary = repair(primary_text, donor_base, key, donor_mapping, donor_literal)
    assert [(e['source_index'], e['from'], e['to']) for e in donor_primary['known_coordinate_substitutions']] == [(142, 'A', 'F')]
    changed = [i for i, (a, b) in enumerate(zip(prior['raw'], primary_text)) if a != b]
    assert changed == [91]
    z_support = next(c for c in conflicts if c['p157_source_index'] == 37)
    assert z_support['p151_pair'] == 'DA' and z_support['p157_coordinate_with_other_p151_coordinate'] == 'DF'
    assert z_support['p151_label'] == '3' and z_support['p157_label_with_other_p151_coordinate'] == 'Z'

    contextual_text = data['contextual_proposal']['plaintext']
    assert contextual_text == primary_text[:-8] + 'STURZDES'
    contextual_donor = repair(contextual_text, donor_base, key, donor_mapping, donor_literal)
    contextual_recipient = repair(contextual_text, base, key, mapping, literal)
    assert len(contextual_donor['known_coordinate_substitutions']) == 3
    assert costs(contextual_recipient, prefix) == costs(candidate, prefix)
    overrides = []
    for i, (a, b) in enumerate(zip(candidate['ciphertext'], contextual_recipient['ciphertext'])):
        if a != b:
            assert i < prefix and mapping[i] is None and donor_mapping[i] is not None
            overrides.append({'model_index': i, 'p151_source_index': donor_mapping[i],
                              'from': a, 'to': b, 'p157_source_index': None})
    assert overrides == [
        {'model_index': 46, 'p151_source_index': 46, 'from': 'X', 'to': 'V', 'p157_source_index': None},
        {'model_index': 104, 'p151_source_index': 103, 'from': 'X', 'to': 'V', 'p157_source_index': None},
    ]
    assert data['contextual_proposal']['continuation_reading'] == previous_p157['records'][0]['readable_candidate']

    display = re.sub('[^A-Z0-9]', '', source['readable_german'].upper())
    assert display == primary_text.replace('X', '')
    case = (ROOT / 'cases/military/armistice_departure_copy.md').read_text()
    assert '> ' + source['readable_german'] in case
    for stream in [raw['raw'], copied_plain, primary_text, contextual_text]:
        assert '```text\n' + stream + '\n```' in case

    runs = exact_runs(donor_literal, literal, 20)
    assert [(r['p151_source_start'], r['p157_source_start'], r['length']) for r in runs] == [(143, 38, 33), (118, 13, 24)]
    record = {
        'id': source['id'], 'literal_source': literal, 'source_slots': len(literal),
        'valid_source_coordinates': 78, 'ciphertext': base,
        'analysis_frame_slots': len(base), 'model_to_source_indices': mapping, **raw,
        'copy_assisted_output_before_observed_repairs': {'ciphertext': copied, 'plaintext': copied_plain,
                                                        'count_as_raw_fixed_positions': False},
        'readable_candidate': candidate, 'fill_provenance': fill_provenance,
        'readable_german': source['readable_german'], 'readable_mapping_verified': True,
    }
    summary = {
        'physical_records': 1, 'printed_source_slots': 83, 'valid_source_coordinates': 78,
        'modeled_coordinates': 190, 'plaintext_positions': 95,
        'baseline_fixed_positions': 0, 'candidate_fixed_positions': 95,
        'known_coordinate_substitutions': 5, 'source_or_model_erasure_fills': 112,
        'source_mask_fills': 5, 'inserted_slot_fills': 107,
        'missing_prefix_fills': 105, 'short_group_fills': 2,
        'source_deletions': 0, 'inserted_slots': 107, 'source_reorderings': 0,
        'published_key_changed': False, 'previously_cataloged_comparison_records_excluded': 1,
    }
    return {
        'schema': 'adfgvx-armistice-departure-copy-certificate-v1',
        'project': data['project'], 'authors': data['authors'], 'input_sha256': sha(HERE / 'inputs.json'),
        'indexing': 'All machine indices are zero-based.', 'summary': summary, 'records': [record],
        'long_exact_source_runs': runs, 'all_25_short_group_alignments': alignments,
        'minimum_observed_disagreement': minimum, 'all_minimum_alignment_boundaries': best,
        'primary_observed_agreements': agreements, 'primary_observed_conflicts': conflicts,
        'all_64_primary_frame_source_choice_witnesses': alternatives,
        'p151_comparison': {'raw': donor_raw, 'prior_candidate': prior,
                            'new_source_supported_proposal': donor_primary, 'z_coordinate_support': z_support},
        'contextual_STURZDES_proposal': {
            'p151_candidate': contextual_donor, 'p157_candidate': contextual_recipient,
            'additional_prefix_overrides_without_p157_observation': overrides,
            'historical_completion_claim': False,
        },
        'headers': data['headers'], 'prior_credit': data['prior_credit'], 'limits': data['limits'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
