"""Exact checks for the p109 parallel and p146 duplicate-group repair.

Readable interpretations remain conditional. Received transcripts are never
overwritten. This module checks the quantitative claims against the stored
sources and the previously published keys.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from . import cipher, prior

ROOT = Path(__file__).resolve().parent.parent


def load_inputs():
    entries = {m['id']: m for m in json.loads((ROOT / 'data/prior_readings.json').read_text())['messages']}
    readings = {m['message_id']: m for m in json.loads((ROOT / 'data/certificates/editorial_readings.json').read_text())['readings']}
    return entries, readings


def p146_analysis():
    entries, readings = load_inputs()
    entry = entries['p146']
    source, key = entry['analysis_ciphertext'], entry['key']
    assert source[220:225] == source[225:230] == 'XAAXV'
    variants = []
    for fill in ['?????', 'AAXAA']:
        edits = [
            {'start': 45, 'end': 45, 'removed': '', 'inserted': fill},
            {'start': 225, 'end': 230, 'removed': 'XAAXV', 'inserted': ''},
        ]
        actual = prior.compute_variant(source, key, {'ciphertext_edits': edits})
        assert cipher.plaintext_domains(actual['corrected_ciphertext'], key['column_rank_order'], key['square']) == actual['plaintext_domains']
        assert actual['corrected_ciphertext'] == source[:45] + fill + source[45:225] + source[230:]
        assert len(actual['corrected_ciphertext']) == len(source) == 244
        assert actual['coordinate_transposition_roundtrip']
        variants.append({'id': 'unfilled' if fill[0] == '?' else 'readable_hypothesis',
                         'edits': edits, 'analysis': actual})
    assert variants[1]['analysis']['raw_partial_plaintext'] == readings['p146']['compact_plaintext']
    # Deleting either of the two indistinguishable printed groups gives the same stream.
    assert source[:220] + source[225:] == source[:225] + source[230:]
    candidate = variants[1]['analysis']['raw_partial_plaintext']
    encoded = cipher.encrypt(candidate, key['column_rank_order'], key['square'])
    assert encoded == variants[1]['analysis']['corrected_ciphertext']
    # Exhaust every single five-coordinate deletion and five-coordinate insertion
    # for this particular complete candidate, allowing nongroup boundaries too.
    fits = []
    for deletion in range(len(source) - 4):
        retained = source[:deletion] + source[deletion + 5:]
        for insertion in range(len(retained) + 1):
            if encoded[:insertion] == retained[:insertion] and encoded[insertion + 5:] == retained[insertion:]:
                fits.append({'deletion_start_in_source': deletion,
                             'insertion_start_in_retained_stream': insertion,
                             'inserted_coordinates': encoded[insertion:insertion + 5]})
    domains = variants[0]['analysis']['plaintext_domains']
    ambiguous = [{'plaintext_index': i, 'allowed_characters': d} for i, d in enumerate(domains) if len(d) > 1]
    return {
        'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
        'source_slots': len(source), 'source_known_coordinates': sum(c in cipher.SYMBOLS for c in source),
        'identical_printed_groups': {'first_start': 220, 'second_start': 225, 'group': 'XAAXV'},
        'representative_inserted_unknown_group_start': 45,
        'retained_known_coordinates': 239,
        'substitutions_to_retained_coordinates': 0,
        'unfilled_plaintext': variants[0]['analysis']['raw_partial_plaintext'],
        'fixed_plaintext_positions': sum(len(d) == 1 for d in domains),
        'plaintext_positions': len(domains),
        'unresolved_domains': ambiguous,
        'compatible_plaintexts_at_representative_geometry': math.prod(map(len, domains)),
        'variants': variants,
        'all_insertion_deletion_fits_for_readable_hypothesis': fits,
        'group_boundary_fits': [f for f in fits if f['deletion_start_in_source'] % 5 == 0 and f['insertion_start_in_retained_stream'] % 5 == 0],
    }


def p109_analysis(source_b):
    entries, readings = load_inputs()
    entry = entries['p109']
    key = entry['key']
    source_d = entry['analysis_ciphertext']
    d_variant = next(v for v in entry['verified_variants'] if v['id'] == 'norbert18')
    b = prior.compute_variant(source_b, key, {})
    d = prior.compute_variant(source_d, key, d_variant)
    assert len(source_b) == len(d['corrected_ciphertext']) == 248
    assert b['plaintext_domains'] == cipher.plaintext_domains(source_b, key['column_rank_order'], key['square'])
    candidate = readings['p109']['compact_plaintext']
    encoded = cipher.encrypt(candidate, key['column_rank_order'], key['square'])
    comparisons = []
    for label, result in [('p109_B', b), ('p109_D_after_Norbert18', d)]:
        ct = result['corrected_ciphertext']
        diffs = [{'index': i, 'observed': a, 'proposed': z}
                 for i, (a, z) in enumerate(zip(ct, encoded)) if a in cipher.SYMBOLS and a != z]
        comparisons.append({'source': label, 'known_coordinate_disagreements_with_candidate': diffs,
                            'count': len(diffs)})
    # At a fixed plaintext slot, all candidate characters are compared with both
    # known coordinate pairs. Missing coordinates contribute no mismatch cost.
    domains, conflicts, minima = [], [], []
    for i, char in enumerate(candidate):
        pairs = [r['intermediate_stream_after_edits'][2*i:2*i+2] for r in (b, d)]
        costs = {}
        for letter in key['square']:
            code = cipher.encode(letter, key['square'])
            costs[letter] = sum(x != y for pair in pairs for x, y in zip(pair, code) if x in cipher.SYMBOLS)
        minimum = min(costs.values())
        best = ''.join(sorted(letter for letter, cost in costs.items() if cost == minimum))
        minima.append(minimum)
        domains.append({'plaintext_index': i, 'pair_B': pairs[0], 'pair_D': pairs[1],
                        'minimum_cost': minimum, 'minimum_cost_characters': best,
                        'readable_candidate_character': char, 'readable_candidate_cost': costs[char]})
        if costs[char] > minimum:
            conflicts.append({'plaintext_index': i, 'proposed': char, 'minimum_cost_characters': best,
                              'extra_substitutions': costs[char] - minimum})
    return {
        'source_B_sha256': hashlib.sha256(source_b.encode()).hexdigest(),
        'source_B_analysis': b,
        'source_D_reference': {'message': 'p109', 'variant': 'norbert18'},
        'known_coordinate_agreements': sum(a == z and a in cipher.SYMBOLS for a, z in zip(source_b, d['corrected_ciphertext'])),
        'known_coordinate_disagreements': sum(a != z and a in cipher.SYMBOLS for a, z in zip(source_b, d['corrected_ciphertext'])),
        'source_B_erasure_indices': [i for i, c in enumerate(source_b) if c == '?'],
        'candidate_comparisons': comparisons,
        'common_plaintext_model': {
            'assumption': 'Both witnesses are readings of one 124-position plaintext after the named earlier D repair; source timings and different endings are not independently resolved.',
            'minimum_total_known_coordinate_substitutions': sum(minima),
            'readable_candidate_total_known_coordinate_substitutions': sum(row['count'] for row in comparisons),
            'positions_outside_minimum_cost_domains': conflicts,
            'domains': domains,
            'candidate_is_source_fixed': False,
        },
    }


def verify():
    p146 = json.loads((ROOT / 'data/certificates/p146_duplicate_group.json').read_text())
    actual146 = p146_analysis()
    assert p146['analysis'] == actual146
    p109 = json.loads((ROOT / 'data/certificates/p109_parallel.json').read_text())
    assert ''.join(p109['source_B']['ciphertext_grouped'].split()).replace('-', '?') == p109['source_B']['ciphertext']
    actual109 = p109_analysis(p109['source_B']['ciphertext'])
    assert p109['analysis'] == actual109
    context = json.loads((ROOT / 'experiments/source_followup/source_context.json').read_text())
    keys = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    checked_context = []
    for record in context['records']:
        key = keys[record['key_id']]
        source = ''.join(record['raw_source_grouped'].split())
        normalized = ''.join(c if c in cipher.SYMBOLS else '?' for c in source)
        analysis = record['arithmetic']
        assert normalized == analysis['analysis_ciphertext']
        assert cipher.decrypt(normalized, key['column_rank_order'], key['square']) == analysis['raw_plaintext']
        assert cipher.plaintext_domains(normalized, key['column_rank_order'], key['square']) == analysis['plaintext_domains']
        if analysis['ordinary_complete_reencryption_exact']:
            assert cipher.encrypt(analysis['raw_plaintext'], key['column_rank_order'], key['square']) == normalized
        checked_context.append(record['id'])
    return {'verified': True,
            'additional_source_context_checked': checked_context,
            'p146': {'retained_known_coordinates': actual146['retained_known_coordinates'],
                     'known_coordinate_substitutions': 0,
                     'fixed_positions_before_fills': actual146['fixed_plaintext_positions'],
                     'conditional_candidate_alignment_count': len(actual146['all_insertion_deletion_fits_for_readable_hypothesis'])},
            'p109': {'parallel_known_agreements': actual109['known_coordinate_agreements'],
                     'parallel_known_disagreements': actual109['known_coordinate_disagreements'],
                     'readable_text_status': 'Explicit conditional editorial interpretation'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(verify(), indent=2))
