#!/usr/bin/env python3
"""Independently reconcile the explicitly reviewed continuation source packages.

Read-only verification from literal inputs, input-declared frame operations and
per-record certificate ledgers. No repository cipher/verifier functions are
imported. The manifest defines a bounded set; it is not a claim that every later
continuation package is included.
Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'data/reviews/continuation_source_count_audit_20261103.json'
C = 'ADFGVX'
SYMBOLS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows_of(d):
    return d['records'] if 'records' in d else [d['record']]

def key_of(d, r):
    if 'key' in d:
        return d['key']
    keys = d['keys']
    if isinstance(keys, dict):
        return keys[r['key_id']]
    return next((k for k in keys if k['id'] == r['key_id']))

def grid_read_order(n, ranks):
    """Map each ragged row-major coordinate to its received-column index."""
    width = len(ranks)
    grid = [[None] * min(width, n - start) for start in range(0, n, width)]
    at = 0
    for col in sorted(range(width), key=lambda j: ranks[j]):
        for row in grid:
            if col < len(row):
                row[col] = at
                at += 1
    assert at == n
    return [i for row in grid for i in row]

def inspect(cipher, key):
    """Enumerate domains directly from pair masks and the partial square."""
    order = grid_read_order(len(cipher), key['column_rank_order'])
    missing = SYMBOLS - set(key['square'])
    positions = []
    for p in range(len(cipher) // 2):
        indices = order[2 * p:2 * p + 2]
        pair = ''.join((cipher[i] for i in indices))
        domain = set()
        for a in C if pair[0] == '?' else pair[:1]:
            for b in C if pair[1] == '?' else pair[1:]:
                label = key['square'][C.index(a) * 6 + C.index(b)]
                domain.update(missing if label == '?' else [label])
        domain = ''.join(sorted(domain))
        positions.append({'plaintext_index': p, 'model_indices': indices, 'pair': pair, 'domain': domain, 'raw': domain if len(domain) == 1 else '?'})
    return {'raw': ''.join((p['raw'] for p in positions)), 'fixed_positions': sum((len(p['domain']) == 1 for p in positions)), 'positions': positions, 'orphan_model_index': order[-1] if len(cipher) % 2 else None}

def transpose(coords, key):
    width = len(key['column_rank_order'])
    rows = [coords[start:start + width] for start in range(0, len(coords), width)]
    return ''.join((row[j] for j in sorted(range(width), key=lambda j: key['column_rank_order'][j]) for row in rows if j < len(row)))

def candidate_cipher(template, frame, key):
    """Encode only fixed target labels; leave '?' pairs unconstrained."""
    coords = ''
    for ch in template:
        if ch == '?':
            coords += '??'
        else:
            idx = key['square'].index(ch)
            coords += C[idx // 6] + C[idx % 6]
    wanted = transpose(coords, key)
    assert len(wanted) == len(frame)
    return ''.join((b if b in C else a for a, b in zip(frame, wanted)))

def frame_from_input(record, source, d):
    """Construct the primary map from declared source operations, not a certificate."""
    af = record.get('analysis_frame', {})
    excluded = set()
    insertions = {}
    linked = set()
    allowed_kinds = {None, 'single_surplus_group', 'single_missing_group', 'duplicate_ten_and_one_exclusion', 'one_parallel_coordinate_added', 'two_duplicate_groups_excluded_and_eleven_slots_added'}
    if af.get('kind') not in allowed_kinds:
        raise ValueError((record['id'], 'Unreviewed frame family', af.get('kind')))
    if af.get('kind') == 'two_duplicate_groups_excluded_and_eleven_slots_added':
        excluded = {i for start in af['primary_excluded_group_starts']
                    for i in range(start, start + 5)}
        one = af['single_gap_before_source_index']
        stage, origins = [], []
        for i in range(len(source) + 1):
            if i == one:
                stage.append('?')
                origins.append(None)
            if i < len(source) and i not in excluded:
                stage.append(source[i] if source[i] in C else '?')
                origins.append(i)
        a = af['first_five_gap_stage_boundary']
        b = af['second_five_gap_stage_boundary']
        assert 0 <= a <= b <= len(stage)
        frame = stage[:a] + ['?'] * 5 + stage[a:b] + ['?'] * 5 + stage[b:]
        mapping = origins[:a] + [None] * 5 + origins[a:b] + [None] * 5 + origins[b:]
        return ''.join(frame), mapping, sorted(excluded), []
    excluded.update(af.get('exclude_source_indices', []))
    excluded.update(af.get('excluded_source_indices', []))
    for a, b in af.get('exclude_half_open_source_ranges', []):
        excluded.update(range(a, b))
    if af.get('kind') == 'single_surplus_group':
        excluded.update(range(af['source_start'], af['source_start'] + af['excluded_slots']))
    for b in af.get('insert_unknown_at_source_boundaries', []):
        insertions.setdefault(b, []).append('?')
    if 'insert_unknown_at_source_boundary' in af:
        insertions.setdefault(af['insert_unknown_at_source_boundary'], []).append('?')
    if af.get('kind') == 'single_missing_group':
        insertions[af['source_boundary']] = ['?'] * af['inserted_slots']
    if af.get('kind') == 'one_parallel_coordinate_added':
        insertions[af['source_boundary']] = list(af['inserted_coordinates'])
        linked.add(af['source_boundary'])
        ref = d['parallel_reference']
        old = json.loads((ROOT / ref['path']).read_text())
        prior = next((x for x in old['records'] if x['id'] == ref['record_id']))
        assert prior['raw_source_compact'][af['parallel_coordinate_index']] == af['inserted_coordinates'] == 'A'
    assert all((0 <= i < len(source) for i in excluded))
    assert all((0 <= b <= len(source) for b in insertions))
    frame = []
    mapping = []
    linked_model = []
    for boundary in range(len(source) + 1):
        for val in insertions.get(boundary, []):
            if boundary in linked:
                linked_model.append(len(frame))
            frame.append(val)
            mapping.append(None)
        if boundary < len(source) and boundary not in excluded:
            frame.append(source[boundary] if source[boundary] in C else '?')
            mapping.append(boundary)
    return (''.join(frame), mapping, sorted(excluded), linked_model)

def build_audit(source_packages):
    """Recompute every record, then compare the generators' count fields."""
    assert source_packages and len(source_packages) == len(set(source_packages)), 'Package scope must be explicit and unique'
    assert all((isinstance(name, str) and name.replace('_', '').isalnum() for name in source_packages)), 'Invalid package identifier'
    records = []
    packages = []
    bindings = []
    globalkeys = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    for package in source_packages:
        base = ROOT / 'experiments' / package
        ip = base / 'inputs.json'
        cp = base / 'certificates.json'
        d = json.loads(ip.read_text())
        cert = json.loads(cp.read_text())
        start = len(records)
        assert cert['input_sha256'] == digest(ip), (package, 'input digest')
        bindings.append({'package': package, 'inputs_sha256': digest(ip), 'certificates_sha256': digest(cp)})
        crs = {r['id']: r for r in rows_of(cert)}
        for r in rows_of(d):
            rid = r['id']
            cr = crs[rid]
            key = key_of(d, r)
            assert key == globalkeys[key['id']], (rid, 'unchanged key')
            source = ''.join(''.join(r['source_rows']).split())
            assert len(source) == r['source_slots'], (rid, 'input source count')
            cs = cr['literal_source'] if 'literal_source' in cr else cr['native']['literal_source']
            assert source == cs, (rid, 'certificate source')
            valid = sum((ch in C for ch in source))
            masks = len(source) - valid
            for field in ['valid_coordinates', 'valid_source_coordinates']:
                if field in cr:
                    assert cr[field] == valid, (rid, field)
            frame, mapping, excluded, linked = frame_from_input(r, source, d)
            assert mapping == cr['model_to_source_indices'], (rid, 'independent frame mapping')
            retained = [i for i in mapping if i is not None]
            assert retained == sorted(set(retained))
            assert set(retained) | set(excluded) == set(range(len(source))) and (not set(retained) & set(excluded))
            for frame_field in ('ciphertext', 'ciphertext_with_unfilled_additions'):
                if frame_field in cr:
                    assert frame == cr[frame_field], (rid, 'independent raw frame')
            assert len(frame) % 2 == 0, (rid, 'modeled orphan')
            raw = inspect(frame, key)
            pureframe = ''.join(('?' if i is None else ch for ch, i in zip(frame, mapping)))
            pure = inspect(pureframe, key)
            assert raw['raw'] == r['expected_raw'] == cr['raw'], (rid, 'independent raw labels')
            assert raw['fixed_positions'] == cr['fixed_positions'], (rid, 'raw fixed count')
            for got, expected in zip(raw['positions'], cr['positions']):
                assert all((got[f] == expected[f] for f in ['plaintext_index', 'model_indices', 'pair', 'domain', 'raw'])), (rid, 'raw domain', got, expected)
                assert [mapping[i] for i in got['model_indices']] == expected['source_indices'], (rid, 'source-pair map')
            target = r.get('edited_output', r.get('readable_candidate'))
            assert isinstance(target, str)
            candidate = candidate_cipher(target, frame, key)
            ca = inspect(candidate, key)
            cc = cr['readable_candidate']
            if 'template' in cc:
                assert target == cc['template'], (rid, 'candidate template')
            else:
                assert cert['schema'] == 'adfgvx-conditional-two-duplicate-partial-certificate-v1', (rid, 'unreviewed candidate schema')
            assert candidate == cc['ciphertext'] and target == ca['raw'] == cc['raw'], (rid, 'independent partial re-encryption')
            assert ca['fixed_positions'] == cc['fixed_positions'], (rid, 'candidate fixed count')
            observed = []
            sourcefills = []
            insertedfills = []
            for i, (before, after, origin) in enumerate(zip(frame, candidate, mapping)):
                if before == after:
                    continue
                event = {'model_index': i, 'source_index': origin, 'before': before, 'after': after, 'literal_source_glyph': source[origin] if origin is not None else None}
                assert after in C, (rid, 'edited valid coordinate')
                if origin is None:
                    assert before == '?' and i not in linked, (rid, 'source-linked coordinate changed')
                    insertedfills.append(event)
                elif source[origin] in C:
                    assert before == source[origin]
                    observed.append(event)
                else:
                    assert before == '?'
                    sourcefills.append(event)
            assert [(x['model_index'], x['source_index'], x['before'], x['after']) for x in observed] == [(x['model_index'], x['source_index'], x['from'], x['to']) for x in cc['known_coordinate_substitutions']], (rid, 'substitution ledger')
            allfills = sorted(sourcefills + insertedfills, key=lambda x: x['model_index'])
            if 'erased_coordinate_fills' in cc:
                certificate_fills = cc['erased_coordinate_fills']
            else:
                assert cert['schema'] == 'adfgvx-conditional-two-duplicate-partial-certificate-v1' and not sourcefills, (rid, 'unreviewed fill schema')
                certificate_fills = cc['inserted_slot_fills']
            assert [(x['model_index'], x['source_index'], x['before'], x['after']) for x in allfills] == [(x['model_index'], x['source_index'], x['from'], x['to']) for x in certificate_fills], (rid, 'fill ledger')
            native = inspect(''.join((ch if ch in C else '?' for ch in source)), key)
            oi = native['orphan_model_index']
            orphan = None if oi is None else {'source_index': oi, 'literal_glyph': source[oi], 'analysis_coordinate': source[oi] if source[oi] in C else '?'}
            oldorphan = cr.get('native_orphan', cr.get('native', {}).get('orphan'))
            if oldorphan:
                assert orphan is not None and oldorphan['source_index'] == oi, (rid, 'native orphan')
            excluded_valid = sum((source[i] in C for i in excluded))
            excluded_masks = len(excluded) - excluded_valid
            unfilled_retained_masks = sum((origin is not None and source[origin] not in C and (candidate[i] == '?') for i, origin in enumerate(mapping)))
            unfilled_added = sum((origin is None and candidate[i] == '?' for i, origin in enumerate(mapping)))
            row = {
                'unfilled_inserted_slots': unfilled_added,
                'package': package,
                'id': rid,
                'source_slots': len(source),
                'valid_source_coordinates': valid,
                'source_masks': masks,
                'advertised_length': r['advertised_length'],
                'native_paired_positions': len(source) // 2,
                'native_orphan': orphan,
                'modeled_slots': len(frame),
                'plaintext_positions': len(frame) // 2,
                'raw_fixed_without_any_added_coordinate_values': pure['fixed_positions'],
                'displayed_raw_fixed_positions': raw['fixed_positions'],
                'candidate_fixed_positions': ca['fixed_positions'],
                'candidate_unresolved_positions': ca['raw'].count('?'),
                'observed_substitutions': len(observed),
                'source_mask_fills': len(sourcefills),
                'inserted_slot_fills': len(insertedfills),
                'source_linked_added_coordinates': len(linked),
                'inserted_slots': mapping.count(None),
                'excluded_source_slots': len(excluded),
                'excluded_valid_coordinates': excluded_valid,
                'excluded_masked_slots': excluded_masks,
                'unfilled_retained_source_masks': unfilled_retained_masks,
                'source_reorderings': 0,
                'source_substitution_events': observed,
                'source_mask_fill_events': sourcefills,
                'inserted_slot_fill_events': insertedfills,
                'source_exclusion_indices': excluded,
                'source_linked_added_model_indices': linked,
                'raw_stream': raw['raw'],
                'candidate_stream': ca['raw'],
            }
            assert row['modeled_slots'] == row['source_slots'] - row['excluded_source_slots'] + row['inserted_slots']
            assert row['source_masks'] == row['source_mask_fills'] + row['unfilled_retained_source_masks'] + row['excluded_masked_slots']
            assert row['inserted_slots'] == row['inserted_slot_fills'] + row['source_linked_added_coordinates'] + row['unfilled_inserted_slots']
            for field, actual in [('expected_substitutions', len(observed)), ('expected_observed_substitutions', len(observed)), ('expected_source_mask_fills', len(sourcefills)), ('expected_inserted_slot_fills', len(insertedfills)), ('expected_inserted_slots_unfilled', unfilled_added)]:
                if field in r:
                    assert r[field] == actual, (rid, field)
            records.append(row)
        subset = records[start:]
        summed = lambda f: sum((r[f] for r in subset))
        checks = {
            'physical_records': len(subset),
            'printed_source_slots': summed('source_slots'),
            'valid_source_coordinates': summed('valid_source_coordinates'),
            'modeled_coordinates': summed('modeled_slots'),
            'plaintext_positions': summed('plaintext_positions'),
            'baseline_fixed_positions': summed('displayed_raw_fixed_positions'),
            'candidate_fixed_positions': summed('candidate_fixed_positions'),
            'known_coordinate_substitutions': summed('observed_substitutions'),
            'source_or_model_erasure_fills': summed('source_mask_fills') + summed('inserted_slot_fills'),
            'source_mask_fills': summed('source_mask_fills'),
            'inserted_slot_fills': summed('inserted_slot_fills'),
            'source_linked_coordinate_additions': summed('source_linked_added_coordinates'),
            'inserted_slots': summed('inserted_slots'),
            'source_deletions': summed('excluded_source_slots'),
            'excluded_valid_source_coordinates': summed('excluded_valid_coordinates'),
            'excluded_source_mask_coordinates': summed('excluded_masked_slots'),
            'deleted_valid_source_coordinates': summed('excluded_valid_coordinates'),
            'deleted_masked_source_slots': summed('excluded_masked_slots'),
            'source_reorderings': 0,
        }
        checks['unfilled_source_mask_coordinates'] = summed('unfilled_retained_source_masks')
        checks['unfilled_retained_source_mask_coordinates'] = summed('unfilled_retained_source_masks')
        checks['unfilled_inserted_slots'] = summed('unfilled_inserted_slots')
        if 'unfilled_gap_fixed_positions' in cert['summary']:
            assert len(subset) == 1, (package, 'Review the scope of the singular unfilled-gap count')
            checks['unfilled_gap_fixed_positions'] = summed('raw_fixed_without_any_added_coordinate_values')
        for field, value in checks.items():
            if field in cert['summary']:
                assert value == cert['summary'][field], (package, field, value, cert['summary'][field])
        packages.append({
            'package': package,
            **{field: summed(field) for field in ['source_slots', 'valid_source_coordinates', 'source_masks', 'modeled_slots', 'plaintext_positions', 'raw_fixed_without_any_added_coordinate_values', 'displayed_raw_fixed_positions', 'candidate_fixed_positions', 'observed_substitutions', 'source_mask_fills', 'inserted_slot_fills', 'source_linked_added_coordinates', 'inserted_slots', 'unfilled_inserted_slots', 'excluded_source_slots', 'excluded_valid_coordinates', 'excluded_masked_slots']},
            'physical_records': len(subset),
            'summary_count_fields_checked': [field for field in checks if field in cert['summary']],
            'certificate_summary': cert['summary'],
            'generator_count_summary_matches_independent_calculation': True,
        })
    numeric_fields = [k for k, v in records[0].items() if isinstance(v, int) and k != 'advertised_length']
    totals = {k: sum((r[k] for r in records)) for k in numeric_fields}
    totals['physical_records'] = len(records)
    totals['source_packages'] = len(packages)
    totals['native_orphan_coordinates'] = sum((r['native_orphan'] is not None for r in records))
    assert totals['source_slots'] == 2 * totals['native_paired_positions'] + totals['native_orphan_coordinates']
    return {'totals': totals, 'package_totals': packages, 'records': records, 'input_bindings': bindings}

def first_difference(expected, actual, path='expected'):
    if type(expected) is not type(actual):
        return f'{path}: type changed from {type(expected).__name__} to {type(actual).__name__}'
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            return f'{path}: fields differ; missing={sorted(expected.keys() - actual.keys())}, added={sorted(actual.keys() - expected.keys())}'
        for key in expected:
            mismatch = first_difference(expected[key], actual[key], f'{path}.{key}')
            if mismatch:
                return mismatch
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            return f'{path}: list length {len(expected)} != {len(actual)}'
        for index, (left, right) in enumerate(zip(expected, actual)):
            mismatch = first_difference(left, right, f'{path}[{index}]')
            if mismatch:
                return mismatch
    elif expected != actual:
        return f'{path}: expected {expected!r}, recomputed {actual!r}'
    return None

def verify_manifest(manifest):
    assert manifest['schema'] == 'adfgvx-continuation-source-count-audit-v1', 'Unreviewed manifest schema'
    actual = build_audit(manifest['source_packages'])
    difference = first_difference(manifest['expected'], actual)
    assert difference is None, difference
    return actual

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT, help='Explicitly reviewed package list, bindings and expected ledgers')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--verify', action='store_true', help='Check the frozen audit (default; read-only)')
    modes.add_argument('--emit', action='store_true', help='Print independently computed ledgers for review; never overwrite the manifest')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        if args.emit:
            actual = build_audit(manifest['source_packages'])
            print(json.dumps(actual, indent=2, ensure_ascii=False))
        else:
            actual = verify_manifest(manifest)
            print(json.dumps({'verified': True, **actual['totals']}, indent=2))
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as error:
        print(json.dumps({'verified': False, 'error': str(error)}, ensure_ascii=False))
        return 1
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
