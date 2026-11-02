"""Verify explicit editorial proposals against the retained earlier repairs.

The candidate text is an interpretation, never a replacement source reading.
Every extra coordinate change is mapped through the prior repair and through
the columnar transposition. Offsets are zero based.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from . import cipher, prior

ROOT = Path(__file__).resolve().parent.parent


def edit_map(length, edits):
    """Map retained slots; length-changing replacement blocks remain unassigned."""
    result, cursor = [], 0
    for edit in sorted(edits, key=lambda e: (e['start'], e['end'])):
        start, end = edit['start'], edit['end']
        assert cursor <= start <= end <= length
        result.extend(range(cursor, start))
        if end - start == len(edit['inserted']):
            result.extend(range(start, end))
        else:
            result.extend([None] * len(edit['inserted']))
        cursor = end
    result.extend(range(cursor, length))
    return result


def audit(entry, record):
    source = entry['analysis_ciphertext']
    key = entry['key']
    variant = next(v for v in entry['verified_variants'] if v['id'] == record['baseline_variant'])
    base = prior.compute_variant(source, key, variant)
    assert base == variant['verification']
    candidate = record['compact_plaintext']
    assert len(candidate) == base['decoded_plaintext_length']
    assert not base['unpaired_intermediate_suffix']
    encoded = cipher.encode(candidate, key['square'])
    before = base['intermediate_stream_before_edits']
    after = base['intermediate_stream_after_edits']
    assert len(encoded) == len(after)
    after_to_before = edit_map(len(before), variant.get('intermediate_edits', []))
    corrected_to_source = edit_map(len(source), variant.get('ciphertext_edits', []))
    emitted = cipher.transposition_indices(len(before), key['column_rank_order'])
    before_to_corrected = {position: i for i, position in enumerate(emitted)}
    proposed_before = list(before)
    changes = []
    for index, (old, new) in enumerate(zip(after, encoded)):
        if old == new:
            continue
        original_intermediate = after_to_before[index]
        assert original_intermediate is not None
        corrected_index = before_to_corrected[original_intermediate]
        source_index = corrected_to_source[corrected_index]
        observed = source[source_index] if source_index is not None else None
        if observed is None:
            relation = 'earlier reconstructed block; no unique source-slot map'
        elif observed == '?':
            relation = 'earlier filled source erasure'
        elif observed != old:
            relation = 'earlier emended known source coordinate'
        else:
            relation = 'unchanged known source coordinate'
        changes.append({
            'plaintext_index': index // 2,
            'coordinate_in_pair': index % 2,
            'paired_stream_index': index,
            'pre_sender_repair_index': original_intermediate,
            'corrected_ciphertext_index': corrected_index,
            'source_index': source_index,
            'source_coordinate': observed,
            'baseline_coordinate': old,
            'proposed_coordinate': new,
            'source_relation': relation,
        })
        proposed_before[original_intermediate] = new
    proposed_before = ''.join(proposed_before)
    assert prior.apply_edits(proposed_before, variant.get('intermediate_edits', [])) == encoded
    proposed_ct = cipher.transpose(proposed_before, key['column_rank_order'])
    # Cross-check with the separate slice-based implementation in prior.py.
    assert proposed_ct == prior.transpose(proposed_before, key['column_rank_order'])
    assert cipher.untranspose(proposed_ct, key['column_rank_order']) == proposed_before
    assert cipher.decode(encoded, key['square']) == candidate
    assert len(changes) == sum(a != b for a, b in zip(base['corrected_ciphertext'], proposed_ct))
    plain_changes = [
        {'index': i, 'baseline': a, 'proposed': b}
        for i, (a, b) in enumerate(zip(base['raw_partial_plaintext'], candidate)) if a != b
    ]
    return {
        'analysis_source_sha256': hashlib.sha256(source.encode()).hexdigest(),
        'baseline_plaintext': base['raw_partial_plaintext'],
        'plaintext_length': len(candidate),
        'plaintext_changes': plain_changes,
        'extra_coordinate_changes': changes,
        'extra_coordinate_change_count': len(changes),
        'changes_at_unchanged_known_source_coordinates': sum(
            c['source_relation'] == 'unchanged known source coordinate' for c in changes),
        'changes_inside_earlier_reconstruction': sum(
            c['source_relation'] != 'unchanged known source coordinate' for c in changes),
        'proposed_corrected_ciphertext': proposed_ct,
        'prior_sender_error_model_retained': variant.get('intermediate_edits', []),
        'reencryption_verified': True,
    }


def verify(path=ROOT / 'data/certificates/editorial_readings.json'):
    document = json.loads(Path(path).read_text())
    entries = {m['id']: m for m in json.loads((ROOT / 'data/prior_readings.json').read_text())['messages']}
    result = []
    for record in document['readings']:
        actual = audit(entries[record['message_id']], record)
        assert actual == record['audit'], record['message_id']
        result.append({'message_id': record['message_id'],
                       'plaintext_changes': len(actual['plaintext_changes']),
                       'extra_coordinate_changes': actual['extra_coordinate_change_count'],
                       'historical_truth_asserted': False})
    return {'verified': True, 'scope': 'Explicit editorial changes, not new source-fixed plaintext',
            'readings': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', default=ROOT / 'data/certificates/editorial_readings.json')
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2))
