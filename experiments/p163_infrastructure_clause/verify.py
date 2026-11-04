#!/usr/bin/env python3
"""Audit the conditional p163 unlabelled infrastructure clause.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import permutations
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair

C = 'ADFGVX'
A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(ref):
    path = ROOT / ref['path']
    assert sha(path) == ref['sha256'], ref['path']
    return path


def literal(record, field='source_rows'):
    value = record[field]
    return ''.join((''.join(value) if isinstance(value, list) else value).split())


def layout(length, ranks):
    """Independent ragged-column offsets, returning plaintext-half origins."""
    height, remainder = divmod(length, len(ranks))
    lengths = [height + int(i < remainder) for i in range(len(ranks))]
    offsets = [sum(lengths[j] for j in range(len(ranks)) if ranks[j] < ranks[i])
               for i in range(len(ranks))]
    origins = [offsets[i % len(ranks)] + i // len(ranks) for i in range(length)]
    assert sorted(origins) == list(range(length))
    return origins


def read(wire, key, mapping):
    square, ranks = key['square'], key['column_rank_order']
    origins = layout(len(wire), ranks)
    missing = set(A) - set(square)
    positions = []
    for i in range(len(wire)//2):
        indices = origins[2*i:2*i+2]
        pair = ''.join(wire[j] for j in indices)
        rows = [C.index(pair[0])] if pair[0] in C else range(6)
        cols = [C.index(pair[1])] if pair[1] in C else range(6)
        domain = set()
        for row in rows:
            for col in cols:
                char = square[6*row+col]
                domain.update(missing if char == '?' else char)
        dom = ''.join(sorted(domain))
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': indices,
                          'source_indices': [mapping[j] for j in indices],
                          'domain': dom, 'raw': dom if len(dom) == 1 else '?'})
    result = {'raw': ''.join(p['raw'] for p in positions),
              'fixed_positions': sum(len(p['domain']) == 1 for p in positions),
              'positions': positions}
    assert result == inspect(wire, key, mapping)
    assert result['raw'] == decrypt(wire, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(wire, ranks, square)
    return result


def pair(char, square):
    index = square.index(char)
    return C[index//6] + C[index % 6]


def independent_encrypt(text, ranks, square):
    columns = [[] for _ in ranks]
    cursor = 0
    for char in text:
        for coord in pair(char, square):
            columns[cursor % len(ranks)].append(coord)
            cursor += 1
    return ''.join(''.join(columns[ranks.index(rank)])
                   for rank in range(1, len(ranks)+1))


def completed_squares(square):
    missing = sorted(set(A) - set(square))
    assert missing == ['5', '6'] and square.count('?') == 2
    result = []
    for digits in permutations(missing):
        it = iter(digits)
        complete = ''.join(next(it) if c == '?' else c for c in square)
        assert len(set(complete)) == 36
        result.append(complete)
    return result


def variant(spec, source, key):
    n, prefix = spec['modeled_coordinates'], spec['leading_unknown_coordinates']
    assert n == prefix+len(source) and n % 2 == 0
    mapping = [None]*prefix + list(range(len(source)))
    wire = '?'*prefix + source
    raw = read(wire, key, mapping)
    assert raw['fixed_positions'] == 0
    start, text = spec['start'], spec['text']
    assert start+len(text) == n//2
    template = '?'*start + text
    common = repair(template, wire, key, mapping, source)
    assert not common['known_coordinate_substitutions']
    assert all(e['source_index'] is None for e in common['erased_coordinate_fills'])
    edited_wire = common['ciphertext']
    assert edited_wire[prefix:] == source
    after = read(edited_wire, key, mapping)
    assert after['raw'] == template and after['fixed_positions'] == len(text)
    assignments = []
    support = []
    for i, char in enumerate(text, start):
        before = raw['positions'][i]
        desired = pair(char, key['square'])
        halves = []
        for half, (model, origin, was, target) in enumerate(zip(
                before['model_indices'], before['source_indices'], before['pair'], desired)):
            if origin is not None:
                assert was == source[origin] == target
            else:
                assert was == '?'
                assignments.append({'model_index': model, 'source_index': None,
                                    'plaintext_index': i, 'half': half,
                                    'before': '?', 'after': target})
            halves.append({'half': half, 'model_index': model,
                           'source_index': origin, 'observed': origin is not None,
                           'source_value': None if origin is None else source[origin],
                           'proposed_value': target})
        support.append({'plaintext_index': i, 'proposed': char,
                        'native_pair': before['pair'], 'native_domain': before['domain'],
                        'observed_halves': sum(h['observed'] for h in halves),
                        'wholly_unobserved': all(not h['observed'] for h in halves),
                        'halves': halves})
    assignments.sort(key=lambda r: r['model_index'])
    assert len(assignments) == len(common['erased_coordinate_fills'])
    assert len({r['model_index'] for r in assignments}) == len(assignments)
    rebuilt = list(wire)
    for row in assignments:
        rebuilt[row['model_index']] = row['after']
    assert ''.join(rebuilt) == edited_wire
    witnesses = []
    for square in completed_squares(key['square']):
        full = edited_wire.replace('?', 'A')
        plain = decrypt(full, key['column_rank_order'], square)
        assert encrypt(plain, key['column_rank_order'], square) == full
        assert independent_encrypt(plain, key['column_rank_order'], square) == full
        assert full[prefix:] == source
        assert plain[start:] == text
        witnesses.append({'square': square, 'ciphertext': full, 'plaintext': plain,
                          'arbitrary_witness_only_added_coordinate_fills': edited_wire.count('?'),
                          'roundtrip_and_independent_column_encoder_verified': True,
                          'historical_completion_claim': False})
    edited = {'ciphertext': edited_wire, 'raw': after['raw'],
              'fixed_positions': after['fixed_positions'],
              'positions': after['positions'],
              'observed_coordinate_substitutions': [], 'printed_mask_fills': [],
              'inserted_slot_fills': assignments,
              'published_key_changed': False}
    return {'variant': spec, 'ciphertext': wire,
            'model_to_source_indices': mapping, **raw,
            'readable_candidate': edited, 'proposal_position_support': support,
            'summary': {'proposed_positions': len(text),
                        'observed_half_coordinates_preserved': sum(r['observed_halves'] for r in support),
                        'observed_coordinate_substitutions': 0,
                        'printed_mask_fills': 0,
                        'added_missing_coordinate_fills': len(assignments),
                        'remaining_added_unknown_coordinates': edited_wire.count('?'),
                        'wholly_unobserved_proposed_positions': [r['plaintext_index'] for r in support if r['wholly_unobserved']]},
            'global_square_witnesses': witnesses}


def geometry_audit(data, source, key):
    """Bounded exact suffix comparison; no language-model score is used."""
    bounds = data['suffix_geometry_audit']
    counts = {r['id']: 0 for r in data['variants']}
    hits = []
    for n in range(bounds['minimum_modeled_coordinates'], bounds['maximum_modeled_coordinates']+1, bounds['step']):
        prefix = n-len(source)
        wire = '?'*prefix+source
        origins = layout(n, key['column_rank_order'])
        for spec in data['variants']:
            text = spec['text']
            start = n//2-len(text)
            if start < 0:
                continue
            observed = mismatch = 0
            absent = []
            for i, char in enumerate(text, start):
                old = ''.join(wire[j] for j in origins[2*i:2*i+2])
                new = pair(char, key['square'])
                observed += sum(c in C for c in old)
                mismatch += sum(a in C and a != b for a, b in zip(old, new))
                if old == '??':
                    absent.append(i)
            counts[spec['id']] += 1
            if not mismatch:
                hits.append({'candidate_id': spec['id'], 'modeled_coordinates': n,
                             'leading_unknown_coordinates': prefix, 'start': start,
                             'observed_halves': observed,
                             'added_coordinate_fills': 2*len(text)-observed,
                             'wholly_unobserved_proposed_positions': absent,
                             'meets_reported_support_threshold': observed >= bounds['minimum_reported_observed_halves']})
    assert all(n == 440 for n in counts.values())
    assert {h['modeled_coordinates'] for h in hits if h['meets_reported_support_threshold']} == {284,286}
    return {'scope': bounds, 'tested_frames_per_candidate': counts,
            'all_zero_change_hits_including_low_support': hits,
            'limit': 'This compares only the stated candidate strings as suffixes in one-leading-loss frames. It does not establish either frame, exclude alternative wording, scan internal or trailing losses, or provide a uniqueness probability.'}


def build(pdf=None):
    data = load(HERE/'inputs.json')
    base = load(checked(data['baseline_inputs']))
    checked(data['baseline_certificate'])
    discovery = load(checked(data['discovery_metadata']))
    assert sha(HERE/'domain_words.cpp') == discovery['solver_source_sha256']
    keys = {k['id']: k for k in load(ROOT/'data/keys.json')['keys']}
    key = data['key']
    assert key == keys['Nov7-9']
    assert key['square'] == base['key']['square']
    assert key['column_rank_order'] == base['key']['column_rank_order']
    rec = data['records'][0]
    prior = next(r for r in base['records'] if r['id'] == rec['legacy_source_record_id'])
    assert rec['id'] == 'p163_A16' and rec['legacy_source_record_id'] == 'p163_A_unlabelled'
    assert rec['source_rows'] == prior['source_rows']
    assert rec['source_header'] == prior['source_header']
    source = literal(rec)
    assert len(source) == rec['source_slots'] == 121 and set(source) <= set(C)
    assert rec['printed_part_number'] is None and rec['advertised_length'] is None
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    variants = [variant(v, source, key) for v in data['variants']]
    by_id = {r['variant']['id']: r for r in variants}
    primary = by_id[rec['primary_variant_id']]
    assert primary['raw'] == rec['expected_raw'] == '?'*143
    assert primary['readable_candidate']['raw'] == rec['readable_candidate']
    assert primary['summary'] == {'proposed_positions':59,'observed_half_coordinates_preserved':53,
        'observed_coordinate_substitutions':0,'printed_mask_fills':0,'added_missing_coordinate_fills':65,
        'remaining_added_unknown_coordinates':100,'wholly_unobserved_proposed_positions':[92,102,112,122,132,142]}
    assert len(primary['readable_candidate']['raw'])-primary['readable_candidate']['fixed_positions'] == 84
    alternate = by_id['singular_separator_und']
    equivalence = []
    for a, b in zip(alternate['positions'], primary['positions']):
        assert a['pair'] == b['pair'] and a['domain'] == b['domain']
        assert a['source_indices'] == b['source_indices']
        equivalence.append({'plaintext_index': a['plaintext_index'],
                            'pair': a['pair'], 'source_indices': a['source_indices'],
                            'model_indices_284': a['model_indices'],
                            'model_indices_286': b['model_indices']})
    assert len(equivalence) == 142
    final = primary['positions'][-1]
    assert final['plaintext_index'] == 142 and final['pair'] == '??'
    assert final['model_indices'] == [14,157] and final['source_indices'] == [None,None]
    heading = by_id['plural_with_heading']
    assert heading['summary']['added_missing_coordinate_fills']-65 == 3
    assert heading['summary']['observed_half_coordinates_preserved']-53 == 1
    assert heading['summary']['wholly_unobserved_proposed_positions'] == [82,92,102,112,122,132,142]
    # Exact per-word support includes native half coordinates, not word frequencies.
    spans = [('WEGEN',84,89),('ZERSTOERUNG',89,100),('VON',100,103),
             ('EISENBAHNEN',103,114),('X',114,115),('STRASSEN',115,123),
             ('UND',123,126),('TELEPHON',126,134),('LEITUNGEN',134,143)]
    words = []
    for word, start, stop in spans:
        assert primary['readable_candidate']['raw'][start:stop] == word
        rows = [r for r in primary['proposal_position_support'] if start <= r['plaintext_index'] < stop]
        observed = sum(r['observed_halves'] for r in rows)
        words.append({'text':word,'start':start,'stop':stop,'observed_halves':observed,
                      'added_coordinate_fills':2*len(word)-observed,
                      'wholly_unobserved_positions':[r['plaintext_index'] for r in rows if r['wholly_unobserved']]})
    # A17 context is rebuilt and its inherited observed repair remains explicit.
    context = data['following_context']
    a17 = next(r for r in base['records'] if r['id'] == context['record_id'])
    lit17 = literal(a17);wire17 = lit17.replace('-','?')
    raw17 = read(wire17,key,list(range(len(wire17))))
    assert raw17['raw'][:17] == context['raw_opening']
    event = context['inherited_observed_change']
    assert lit17[event['source_index']] == event['from']
    edit17 = wire17[:event['source_index']]+event['to']+wire17[event['source_index']+1:]
    assert decrypt(edit17,key['column_rank_order'],key['square'])[:17] == context['earlier_edited_opening']
    assert raw17['positions'][4]['source_indices'] == [93,172]
    native = context['native_predicate_span']
    assert raw17['raw'][native['start']:native['stop']] == native['text']
    native_rows = raw17['positions'][native['start']:native['stop']]
    assert all('?' not in p['pair'] for p in native_rows)
    # Neighboring literal7 and9 support only the *optional* absent heading8.
    numbered = data['numbering_context']
    a15 = next(r for r in base['records'] if r['id'] == numbered['preceding_record'])
    wire15 = literal(a15).replace('-','?')
    raw15 = read(wire15,key,list(range(len(wire15))))
    seven = raw15['positions'][92]
    assert seven['raw'] == '7' and '?' not in seven['pair']
    heading_at = raw17['raw'].index(numbered['following_literal_heading'])
    nine = raw17['positions'][heading_at:heading_at+3]
    assert all('?' not in p['pair'] for p in nine)
    # Vocabulary witnesses must be complete original pairs in other records.
    donors = []
    for spec in data['native_word_witnesses']:
        inp = load(checked(spec['inputs']))
        donor = next(r for r in inp[spec['container']] if r['id'] == spec['record_id'])
        lit = literal(donor,spec['source_field'])
        assert set(lit) <= set(C+'-?')
        wire = lit.replace('-','?')
        reading = read(wire,keys[spec['key_id']],list(range(len(wire))))
        if spec.get('expected_raw_field'):
            assert reading['raw'] == donor[spec['expected_raw_field']]
        at = reading['raw'].index(spec['word'])
        positions = reading['positions'][at:at+len(spec['word'])]
        assert all('?' not in p['pair'] for p in positions)
        donors.append({'id':spec['id'],'record_id':spec['record_id'],'key_id':spec['key_id'],
                       'text':spec['word'],'start':at,'positions':positions,
                       'observed_coordinate_substitutions':0,'printed_mask_fills':0,
                       'scope':spec['scope']})
    # The generic primary-record fields support independent corpus quantification.
    primary_record = {'id':rec['id'],'legacy_source_record_id':rec['legacy_source_record_id'],
        'literal_source':source,'literal_printed_rows':rec['source_rows'],'source_slots':121,
        'valid_coordinates':121,'ciphertext':primary['ciphertext'],
        'model_to_source_indices':primary['model_to_source_indices'],
        'raw':primary['raw'],'fixed_positions':0,'positions':primary['positions'],
        'readable_candidate':primary['readable_candidate'],
        'readable_german':rec['readable_german'],'proposed_span':rec['proposed_span'],
        'proposal_position_support':primary['proposal_position_support']}
    # If README exists, its literal output displays must remain exact.
    readme = HERE/'README.md'
    if readme.exists():
        blocks = re.findall(r'```text\n(.*?)\n```',readme.read_text(),re.S)
        assert blocks == [primary['raw'],primary['readable_candidate']['raw'],'\n'.join(rec['source_rows'])]
    case_blocks = re.findall(r'```text\n(.*?)\n```',(ROOT/data['case']).read_text(),re.S)
    assert case_blocks == [primary['raw'],primary['readable_candidate']['raw'],'\n'.join(rec['source_rows'])]
    return {'schema':'adfgvx-p163-infrastructure-clause-certificate-v1',
        'authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':data['indexing'],
        'summary':{'physical_records':1,'native_source_slots':121,'valid_source_coordinates':121,
            'printed_source_masks':0,'modeled_coordinates':286,'added_unknown_prefix_coordinates':165,
            'source_coordinates_excluded_reordered_or_changed':0,'plaintext_positions':143,
            'raw_fixed_positions':0,'candidate_fixed_positions':59,'candidate_unknown_positions':84,
            'observed_coordinate_substitutions':0,'printed_mask_fills':0,
            'added_missing_coordinate_fills':65,'remaining_added_unknown_coordinates':100,
            'observed_half_coordinates_supporting_proposal':53,
            'wholly_unobserved_proposed_positions':[92,102,112,122,132,142],
            'full_length_established':False,'printed_part_number_established':False,
            'global_injective_square_completions_checked':2,'variants_checked':8,
            'historical_uniqueness_claim':False},
        'records':[primary_record],
        'priced_variants':variants,
        'per_word_half_coordinate_support':words,
        'exact_284_286_frame_equivalence':{'shared_plaintext_positions':142,
            'all_received_coordinate_ownerships_and_pairs_identical':True,
            'shared_positions':equivalence,'extra_286_position':final,
            'conclusion':'The received source cannot distinguish these two frames. The extra last letter in the 286-coordinate model is wholly unobserved.'},
        'bounded_suffix_geometry_audit':geometry_audit(data,source,key),
        'following_context':{**context,'raw_opening_positions':raw17['positions'][:17],
            'native_predicate_positions':native_rows},
        'numbering_context':{**numbered,'native_seven_position':seven,
            'native_nine_heading_positions':nine},
        'native_word_witnesses':donors,'limits':data['limits']},evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args()
    result,evidence = build(args.pdf)
    out = HERE/'certificates.json'
    if args.verify:
        assert result == load(out)
    else:
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary'],
                      'source_evidence':evidence['summary']},indent=2))
