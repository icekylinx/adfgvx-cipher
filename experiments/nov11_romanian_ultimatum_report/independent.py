#!/usr/bin/env python3
"""Independent ragged-column check of the p180 D1 reconstruction.

No project cipher, transposition or geometry helper is imported.
ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = 'ADFGVX'


def build():
    audit = json.loads((HERE / 'source_audit.json').read_text())
    source = ''.join(''.join(audit['rows']).split())
    data = json.loads((HERE / 'inputs.json').read_text())
    candidate = data['records'][0]['readable_candidate']
    key = next(k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']
               if k['id'] == 'Nov10-12')
    ranks, square = key['column_rank_order'], key['square']
    width = len(ranks)
    coordinates = ''.join(C[square.index(c) // 6] + C[square.index(c) % 6] for c in candidate)
    encoded = ''.join(coordinates[c::width] for c in sorted(range(width), key=lambda c: ranks[c]))

    def decode(frame):
        intermediate = [''] * len(frame)
        at = 0
        for column in sorted(range(width), key=lambda c: ranks[c]):
            for position in range(column, len(frame), width):
                intermediate[position] = frame[at]
                at += 1
        result = ''
        for i in range(0, len(intermediate), 2):
            a, b = intermediate[i:i + 2]
            result += square[C.index(a) * 6 + C.index(b)] if a in C and b in C else '?'
        return result

    simple_costs = [sum(a in C and a != b for a, b in zip(source[:i] + source[i + 1:], encoded))
                    for i in range(len(source))]
    minimum = None
    best = []
    tested = 0
    for duplicate in [125, 130]:
        for tail in [195, 196]:
            excluded = set(range(duplicate, duplicate + 5)) | {tail}
            origins = [i for i in range(len(source)) if i not in excluded]
            assert len(origins) == 191
            for boundary in range(len(origins) + 1):
                tested += 1
                mapping = origins[:boundary] + [None] * 5 + origins[boundary:]
                frame = ''.join(source[i] if i is not None and source[i] in C else '?' for i in mapping)
                changes = [{'source_index': i, 'from': source[i], 'to': encoded[j]}
                           for j, i in enumerate(mapping)
                           if i is not None and source[i] in C and source[i] != encoded[j]]
                cost = len(changes)
                if minimum is None or cost < minimum:
                    minimum, best = cost, []
                if cost != minimum:
                    continue
                raw = decode(frame)
                best.append({'duplicate_start': duplicate, 'excluded_final_A': tail,
                             'gap_boundary_in_retained_stream': boundary,
                             'before_original_source_index': origins[boundary] if boundary < len(origins) else None,
                             'mapping_sha256': hashlib.sha256(json.dumps(mapping, separators=(',', ':')).encode()).hexdigest(),
                             'raw': raw, 'fixed_positions': len(raw) - raw.count('?'),
                             'observed_coordinate_substitutions': changes,
                             'source_mask_fills': sum(i is not None and source[i] not in C for i in mapping),
                             'inserted_slot_fills': mapping.count(None)})
    assert tested == 768 and minimum == 2 and len(best) == 8
    assert {r['gap_boundary_in_retained_stream'] for r in best} == {145, 146}
    assert all(r['fixed_positions'] == (85 if r['gap_boundary_in_retained_stream'] == 145 else 84) for r in best)
    assert all(r['source_mask_fills'] == 10 and r['inserted_slot_fills'] == 5 for r in best)
    assert min(simple_costs) == 17
    return {'schema': 'adfgvx-p180-independent-candidate-check-v1',
            'authors': data['authors'], 'candidate': candidate,
            'native_slots': len(source), 'native_valid_coordinates': sum(c in C for c in source),
            'tested_maps': tested, 'minimum_observed_substitutions': minimum,
            'minimum_maps': best,
            'single_exclusion_only': {'tested_maps': len(simple_costs), 'minimum_observed_substitutions': min(simple_costs),
                                      'minimum_excluded_indices': [i for i, c in enumerate(simple_costs) if c == min(simple_costs)]}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    destination = HERE / 'independent.json'
    if args.verify:
        assert result == json.loads(destination.read_text())
    else:
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'tested_maps': result['tested_maps'],
                      'minimum_observed_substitutions': result['minimum_observed_substitutions'],
                      'minimum_maps': len(result['minimum_maps'])}, indent=2))
