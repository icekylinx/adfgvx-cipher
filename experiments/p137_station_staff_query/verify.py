#!/usr/bin/env python3
"""Recompute p137 B's conditional staff query, all source maps and word prices.

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
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.check_reading_presentation import displays, expected_legend

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(rows):
    return ''.join(''.join(rows).split())


def inverse(length, ranks):
    """Independent physical-column offsets: interim index -> model index."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    heights = [length // width + (c < length % width) for c in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[c])
              for c in range(width)]
    result = [starts[i % width] + i // width for i in range(length)]
    assert sorted(result) == list(range(length))
    return result


def inspect(frame, key, mapping):
    order = inverse(len(frame), key['column_rank_order'])
    middle = ''.join(frame[j] for j in order)
    assert middle == untranspose(frame, key['column_rank_order'])
    positions = []
    for i in range(0, len(middle) - 1, 2):
        pair = middle[i:i + 2]
        domain = ''.join(sorted(key['square'][6*r+c]
                               for r in range(6) for c in range(6)
                               if pair[0] in ('?', C[r]) and pair[1] in ('?', C[c])))
        indices = order[i:i + 2]
        positions.append({'plaintext_index': i // 2, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices],
                          'domain': domain, 'raw': domain if len(domain) == 1 else '?'})
    raw = ''.join(p['raw'] for p in positions)
    assert raw == decrypt(frame, key['column_rank_order'], key['square'], allow_unpaired=True)
    if len(frame) % 2 == 0:
        assert [p['domain'] for p in positions] == plaintext_domains(frame, key['column_rank_order'], key['square'])
    orphan = None if len(frame) % 2 == 0 else {
        'interim_index': len(frame) - 1, 'model_index': order[-1],
        'source_index': mapping[order[-1]], 'coordinate': middle[-1]}
    return {'raw': raw, 'fixed_positions': sum(p['raw'] != '?' for p in positions),
            'positions': positions, 'unpaired_coordinate': orphan}


def masked_encryption(template, key):
    middle = ''.join('??' if ch == '?' else C[key['square'].index(ch)//6] + C[key['square'].index(ch)%6]
                     for ch in template)
    result = [''] * len(middle)
    for i, received in enumerate(inverse(len(middle), key['column_rank_order'])):
        result[received] = middle[i]
    return ''.join(result)


def move_map(length, start, destination):
    retained = [i for i in range(length) if not start <= i < start + 5]
    assert start % 5 == 0 and 0 <= start <= length - 5
    assert 0 <= destination <= len(retained)
    return retained[:destination] + list(range(start, start + 5)) + retained[destination:]


def full_scope(source, target):
    """Price every declared map using exact prefix/suffix mismatch sums.

    For a gap at g, the moved source prefix aligns to target[:g], and the
    suffix to target[g+3:]. A masked source or candidate coordinate costs 0.
    This is exact integer pricing, with no language scores or pruning.
    """
    histogram, ties = Counter(), []
    minimum, models = len(source) + 1, 0
    digest = hashlib.sha256()
    for start in range(0, len(source) - 4, 5):
        for destination in range(len(source) - 4):
            moved = ''.join(source[i] for i in move_map(len(source), start, destination))
            prefix, suffix = [0], [0] * (len(source) + 1)
            for i, char in enumerate(moved):
                prefix.append(prefix[-1] + (char in C and target[i] in C and char != target[i]))
            for i in range(len(source) - 1, -1, -1):
                suffix[i] = suffix[i+1] + (moved[i] in C and target[i+3] in C and moved[i] != target[i+3])
            costs = [prefix[g] + suffix[g] for g in range(len(source) + 1)]
            digest.update(bytes(costs))
            histogram.update(costs)
            for gap, cost in enumerate(costs):
                models += 1
                if cost < minimum:
                    minimum, ties = cost, []
                if cost == minimum:
                    ties.append([start, destination, gap])
    return {'models': models, 'minimum_observed_substitutions': minimum,
            'exact_minimum_maps': ties,
            'cost_histogram': {str(k): histogram[k] for k in sorted(histogram)},
            'all_costs_sha256': digest.hexdigest(),
            'digest_order': 'One unsigned-byte cost for each (start,destination,gap), ascending nested order.'}


def variant(source, key, template, start, destination, gap):
    moved = move_map(len(source), start, destination)
    mapping = moved[:gap] + [None] * 3 + moved[gap:]
    assert sorted(i for i in mapping if i is not None) == list(range(len(source)))
    frame = ''.join(source[i] if i is not None and source[i] in C else '?' for i in mapping)
    raw = inspect(frame, key, mapping)
    target = masked_encryption(template, key)
    edited = ''.join(a if b == '?' else b for a, b in zip(frame, target))
    result = inspect(edited, key, mapping)
    assert result['raw'] == template
    subs, masks, added = [], [], []
    for i, (before, after) in enumerate(zip(frame, edited)):
        if before == after:
            continue
        origin = mapping[i]
        event = {'model_index': i, 'source_index': origin,
                 'printed': None if origin is None else source[origin],
                 'from': before, 'to': after}
        (added if origin is None else masks if source[origin] not in C else subs).append(event)
    assert len(subs) == 3 and len(masks) == len(added) == 2
    assert edited.count('?') == 1 and edited[136] == '?'
    assert result['positions'][58]['domain'] == '036OQY'
    assert raw['fixed_positions'] == 64 and result['fixed_positions'] == 68
    proposal = {'template': template, 'ciphertext': edited, **result,
                'known_coordinate_substitutions': subs,
                'erased_coordinate_fills': masks + added,
                'source_mask_fills': masks, 'inserted_slot_fills': added,
                'full_plaintext_reencryption_verified': False,
                'published_key_changed': False}
    witnesses = []
    for label in result['positions'][58]['domain']:
        full = template[:58] + label + template[59:]
        encrypted = encrypt(full, key['column_rank_order'], key['square'])
        assert decrypt(encrypted, key['column_rank_order'], key['square']) == full
        assert all(a == '?' or a == b for a, b in zip(edited, encrypted))
        assert sum(source[origin] in C and source[origin] != encrypted[i]
                   for i, origin in enumerate(mapping) if origin is not None) == 3
        back = [''] * len(source)
        for i, origin in enumerate(mapping):
            if origin is not None:
                back[origin] = encrypted[i]
        assert all(back[e['source_index']] == e['to'] for e in subs + masks)
        witnesses.append({'plaintext_label_at_58': label, 'plaintext': full,
                          'ciphertext': encrypted, 'source_order_reencryption': ''.join(back),
                          'otherwise_unassigned_model_136': encrypted[136],
                          'auxiliary_only_not_in_primary_fill_count': True})
    return {'moved_group_source_start': start, 'move_destination_in_retained_stream': destination,
            'inserted_slot_boundary_in_moved_stream': gap,
            'model_to_source_indices': mapping, 'ciphertext': frame, **raw,
            'readable_candidate': proposal, 'full_completion_witnesses': witnesses}


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov4-6')
    assert len(key['square']) == len(set(key['square'])) == 36 and '?' not in key['square']
    for field in ['source_audit', 'prior_ocr']:
        assert sha(HERE / data[field]['path']) == data[field]['sha256']
    prior = data['prior_ocr']
    assert sha(ROOT / prior['origin']) == prior['origin_sha256']
    old = load(HERE / prior['path'])
    assert old == next(r for r in load(ROOT / prior['origin'])['blocks'] if r['id'] == old['id'])
    for name, digest in data['peer_evidence'].items():
        assert sha(HERE / name) == digest
    related = data['related_source']
    assert sha(ROOT / related['input_path']) == related['input_sha256']
    assert sha(ROOT / related['certificate_path']) == related['certificate_sha256']
    context = next(r for r in load(ROOT / related['certificate_path'])['records'] if r['id'] == related['record_id'])
    assert context['readable_candidate']['raw'] == related['edited']
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    record = data['records'][0]
    source = compact(record['source_rows'])
    audit = load(HERE / data['source_audit']['path'])
    assert source == audit['source_literal'] and record['source_rows'] == audit['source_rows']
    assert len(source) == 135 and sum(ch in C for ch in source) == 133
    assert [(i, ch) for i, ch in enumerate(source) if ch not in C] == [(133, '-'), (134, '-')]
    h = data['header']
    assert record['source_display'] == '\n'.join([h['received'], h['clear_continuation'], h['designator'],
                                                *record['source_rows'], *h['clear_footer']])
    template = record['readable_candidate']
    assert len(template) == 69 and template.count('?') == 1 and template[56:60] == '17?0'
    target = masked_encryption(template, key)
    peer = load(HERE / 'peer_input.json')
    assert target == peer['independently_masked_encoded_target']
    assert source == peer['source_record']['source_literal'] and key == peer['key']
    assert (HERE / 'peer_input.txt').read_text().split() == [source, target]
    scope = full_scope(source, target)
    assert scope['models'] == data['search_scope']['models'] == 481032
    assert scope['minimum_observed_substitutions'] == 3
    assert scope['exact_minimum_maps'] == data['search_scope']['exact_minima']
    peer_report = load(HERE / 'peer_audit.json')
    peer_lines = [list(map(int, line.split())) for line in (HERE / 'peer_result.txt').read_text().splitlines()]
    assert peer_lines == [[481032, 3, 5]] + scope['exact_minimum_maps']
    variants = [variant(source, key, template, *triple) for triple in scope['exact_minimum_maps']]
    for v, p in zip(variants, peer_report['all_ties']):
        assert v['raw'] == p['raw'] and v['readable_candidate']['raw'] == p['edited']
        assert v['model_to_source_indices'] == p['model_to_source_indices']
        assert v['readable_candidate']['positions'][58]['domain'] == p['time_unknown_at_58']['domain']
        actual = sorted((e['model_index'], e['source_index'], e['from'], e['to'])
                        for group in ['known_coordinate_substitutions', 'erased_coordinate_fills']
                        for e in v['readable_candidate'][group])
        expected = sorted((e['model_index'], e['source_index'], e['from'], e['to']) for e in p['source_events'])
        assert actual == expected
    primary = next(v for v in variants if v['move_destination_in_retained_stream'] == 105)
    assert primary['raw'] == record['expected_raw']
    proposal = primary['readable_candidate']
    assert [(e['source_index'], e['from'], e['to']) for e in proposal['known_coordinate_substitutions']] == [(130, 'V', 'F'), (131, 'D', 'G'), (132, 'F', 'X')]
    german = record['readable_german']
    assert re.sub('[^A-Z0-9?]', '', german.upper().replace('BESETZT?', 'BESETZT')) == template.replace('X', '')
    native = inspect(source.replace('-', '?'), key, list(range(len(source))))
    assert len(native['raw']) == 67 and native['unpaired_coordinate'] is not None
    path = ROOT / data['case']
    text = path.read_text()
    assert text.count(expected_legend(path)) == 1
    fences, quotes = displays(text)
    assert [f['role_from_caption'] for f in fences] == ['raw_output', 'edited_output', 'source_transcription']
    assert len(quotes) == 1 and quotes[0]['role_from_caption'] == 'readable_german'
    assert re.findall(r'```text\n(.*?)\n```', text, re.S) == [primary['raw'], template, record['source_display']]
    assert re.findall(r'^> (.*)$', text, re.M) == [german]
    return {'schema': 'adfgvx-p137-station-staff-query-certificate-v1',
            'project': data['project'], 'authors': data['authors'],
            'input_sha256': sha(HERE / 'inputs.json'), 'indexing': data['indexing'],
            'summary': {'physical_records': 1, 'printed_source_slots': 135,
                        'valid_source_coordinates': 133, 'source_mask_slots': 2,
                        'modeled_coordinates': 138, 'plaintext_positions': 69,
                        'baseline_fixed_positions': 64, 'candidate_fixed_positions': 68,
                        'known_coordinate_substitutions': 3, 'source_mask_fills': 2,
                        'inserted_slots': 3, 'inserted_slot_fills': 2,
                        'unfilled_inserted_slots': 1, 'excluded_source_slots': 0,
                        'source_group_moves': 1, 'moved_source_slots': 5,
                        'tied_minimum_maps': 5, 'exhaustively_compared_models': 481032,
                        'full_completion_witnesses': 30, 'published_key_changed': False},
            'records': [{'id': record['id'], 'key_id': key['id'], 'literal_source': source,
                         'literal_printed_rows': record['source_rows'], 'source_slots': 135,
                         'valid_coordinates': 133, **primary,
                         'readable_german': german, 'native_135_slot_diagnostic': native,
                         'all_tied_minimum_maps': variants,
                         'complete_fixed_candidate_cost_screen': scope}],
            'peer_result_sha256': sha(HERE / 'peer_audit.json'),
            'prior_credit': data['prior_credit'], 'limits': data['limits']}, evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result, evidence = build(args.pdf)
    if args.verify:
        assert result == load(HERE / 'certificates.json')
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, **result['summary'],
                      'source_evidence': evidence['summary']}, indent=2))
