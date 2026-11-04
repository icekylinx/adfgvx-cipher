#!/usr/bin/env python3
"""Audit the conditional p137 A6 publicity fragment and adverse alternatives.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains
from adfgvx.source_evidence import verify_source_evidence
from experiments.p163_infrastructure_clause.verify import read, layout, pair, independent_encrypt

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


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def proposal(source, key, n, template, ident, full=False):
    prefix = n-len(source)
    assert prefix >= 0 and n % 2 == 0 and len(template) == n//2
    mapping = [None]*prefix+list(range(len(source)))
    wire = '?'*prefix+source.replace('-', '?')
    raw = read(wire, key, mapping)
    assert raw['fixed_positions'] == 0
    edited = list(wire)
    substitutions, printed_fills, added_fills, support = [], [], [], []
    for i, char in enumerate(template):
        if char == '?':
            continue
        before = raw['positions'][i]
        target = pair(char, key['square'])
        halves = []
        for half, (model, origin, old, new) in enumerate(zip(
                before['model_indices'], before['source_indices'], before['pair'], target)):
            entry = {'model_index': model, 'source_index': origin,
                     'plaintext_index': i, 'half': half, 'before': old, 'after': new}
            if old != new:
                if old in C:
                    substitutions.append(entry)
                elif origin is None:
                    added_fills.append(entry)
                else:
                    printed_fills.append(entry)
            edited[model] = new
            halves.append({'half': half, 'model_index': model, 'source_index': origin,
                           'observed': old in C, 'source_value': None if origin is None else source[origin],
                           'proposed_value': new})
        support.append({'plaintext_index': i, 'proposed': char,
                        'native_pair': before['pair'], 'native_domain': before['domain'],
                        'observed_halves': sum(h['observed'] for h in halves),
                        'wholly_unobserved': all(not h['observed'] for h in halves),
                        'halves': halves})
    edited = ''.join(edited)
    after = read(edited, key, mapping)
    assert after['raw'] == template
    for ledger in (substitutions, printed_fills, added_fills):
        ledger.sort(key=lambda r: r['model_index'])
        assert len({r['model_index'] for r in ledger}) == len(ledger)
    rebuilt = list(wire)
    for row in substitutions+printed_fills+added_fills:
        assert rebuilt[row['model_index']] == row['before']
        rebuilt[row['model_index']] = row['after']
    assert ''.join(rebuilt) == edited
    witness = edited.replace('?', 'A')
    witness_plain = decrypt(witness, key['column_rank_order'], key['square'])
    assert encrypt(witness_plain, key['column_rank_order'], key['square']) == witness
    assert independent_encrypt(witness_plain, key['column_rank_order'], key['square']) == witness
    assert all(c == '?' or c == d for c, d in zip(template, witness_plain))
    native_changes = {r['source_index'] for r in substitutions}
    assert all(c not in C or i in native_changes or witness[prefix+i] == c for i, c in enumerate(source))
    result = {'id': ident, 'modeled_coordinates': n, 'leading_unknown_coordinates': prefix,
              'ciphertext': wire, 'model_to_source_indices': mapping,
              'raw': raw['raw'], 'fixed_positions': raw['fixed_positions'],
              'readable_candidate': {'ciphertext': edited, 'raw': template,
                  'fixed_positions': after['fixed_positions'],
                  'observed_coordinate_substitutions': substitutions,
                  'printed_mask_fills': printed_fills, 'inserted_slot_fills': added_fills,
                  'published_key_changed': False},
              'proposal_position_support': support,
              'summary': {'proposed_positions': len(support),
                  'observed_half_coordinates_preserved': sum(r['observed_halves'] for r in support)-len(substitutions),
                  'observed_coordinate_substitutions': len(substitutions),
                  'printed_mask_fills': len(printed_fills),
                  'added_missing_coordinate_fills': len(added_fills),
                  'remaining_added_unknown_coordinates': edited[:prefix].count('?'),
                  'remaining_printed_masks': edited[prefix:].count('?'),
                  'wholly_unobserved_proposed_positions': [r['plaintext_index'] for r in support if r['wholly_unobserved']]},
              'forward_witness': {'ciphertext': witness, 'plaintext': witness_plain,
                  'ciphertext_sha256': hashlib.sha256(witness.encode()).hexdigest(),
                  'remaining_unknowns_arbitrarily_filled_with': 'A',
                  'roundtrip_and_independent_column_encoder_verified': True,
                  'historical_completion_claim': False}}
    if full:
        result['positions'] = raw['positions']
        result['readable_candidate']['positions'] = after['positions']
    return result


def geometry_audit(data, source, key):
    scope = data['geometry_audit']
    pattern = scope['pattern']
    wanted = ''.join(pair(c, key['square']) if c != '?' else '??' for c in pattern)
    assigned = [(i, c) for i, c in enumerate(wanted) if c != '?']
    tested = eligible = 0
    hits = []
    for n in range(scope['minimum'], scope['maximum']+1, scope['step']):
        wire = '?'*(n-len(source))+source.replace('-', '?')
        mid = ''.join(wire[j] for j in layout(n, key['column_rank_order']))
        for start in range(n//2-len(pattern)+1):
            tested += 1
            sample = mid[2*start:2*(start+len(pattern))]
            observed = sum(sample[i] in C for i, _ in assigned)
            if observed < scope['minimum_observed_halves']:
                continue
            eligible += 1
            changes = sum(sample[i] in C and sample[i] != c for i, c in assigned)
            if changes <= 1:
                hits.append({'modeled_coordinates': n, 'leading_unknown_coordinates': n-len(source),
                             'start': start, 'assigned_positions': 25,
                             'observed_halves': observed, 'observed_changes': changes})
    assert tested == 106953 and eligible == 3724
    assert [(h['modeled_coordinates'], h['start'], h['observed_changes']) for h in hits] == [(254,13,0),(256,13,0),(258,13,0)]
    return {'scope': scope, 'placements_tested': tested,
            'placements_meeting_support_threshold': eligible,
            'all_zero_or_one_change_hits_at_threshold': hits,
            'limit': 'Only these 25 already-proposed labels, their 39-position span and this one-leading-loss family are tested. Lower-support placements, other words, longer frames and internal or trailing loss models are not excluded.'}


def discovery_audit(data, source, keys):
    d = load(checked(data['discovery_metadata']))
    checked(d['solver']); checked(d['solver_oracle']); checked(d['lexicon']['provenance'])
    assert d['full_length_family'] == {'minimum':74,'maximum':600,'step':2,'frames':264}
    assert d['parameters'] == {'fallback_score':-3,'bigram_weight':0.65,'separator_X_score':-0.25}
    assert len(d['families']) == 13 and d['shuffle_seed'] == 1370418
    rng = random.Random(d['shuffle_seed'])
    target = d['families'][0]
    assert target['id'] == 'target' and target['source_literal'] == source
    result = []
    for index, f in enumerate(d['families']):
        assert len(f['source_literal']) == 74
        assert [i for i, c in enumerate(f['source_literal']) if c not in C] == [25,26,27]
        rows = f['scores_by_length']
        assert [n for n, _ in rows] == list(range(74,602,2))
        winner = max(rows, key=lambda row: row[1])
        assert winner == [f['best_length'], f['best_score']]
        registered = keys[f['key_id']]
        assert f['ranks'] == registered['column_rank_order']
        unused = iter(sorted(set(A)-set(registered['square'])))
        representative = ''.join(next(unused) if c == '?' else c for c in registered['square'])
        assert f['square'] == representative and len(set(f['square'])) == 36
        if f['kind'] == 'full_family_shuffle':
            chars = [c for c in source if c in C]; rng.shuffle(chars); it = iter(chars)
            expected = ''.join(next(it) if c in C else '-' for c in source)
            assert f['source_literal'] == expected and Counter(chars) == Counter(c for c in source if c in C)
            assert 1 <= index <= 8 and f['best_score'] < target['best_score']
        elif f['kind'] == 'wrong_period_key':
            assert 9 <= index <= 11 and f['source_literal'] == source
            assert f['best_score'] < target['best_score']
        elif f['kind'] == 'fresh_authored_positive':
            assert index == 12 and f['authored_not_historical']
            full = independent_encrypt(f['authored_plaintext'], f['ranks'], f['square'])
            suffix = list(full[-74:])
            for i in [25,26,27]: suffix[i] = '-'
            assert ''.join(suffix) == f['source_literal']
            assert f['true_length'] == f['best_length'] == 254
            assert sum(a == b for a, b in zip(f['authored_plaintext'], f['diagnostic_best_plaintext'])) == f['exact_plaintext_agreement'] == 54
        else:
            assert index == 0 and f['kind'] == 'received_source' and f['best_length'] == 254
        wire = '?'*(f['best_length']-74)+f['source_literal'].replace('-', '?')
        domains = plaintext_domains(wire, f['ranks'], f['square'])
        assert len(f['diagnostic_best_plaintext']) == len(domains)
        assert all(c in domain for c, domain in zip(f['diagnostic_best_plaintext'], domains))
        assert f['diagnostic_best_segmentation'].replace(' ', '') == f['diagnostic_best_plaintext']
        result.append({'id':f['id'],'frames':len(rows),'best_length':f['best_length'],'best_score':f['best_score']})
    return {'families':result,'total_declared_frame_scores':3432,
            'source_generation_and_selected_best_native_compatibility_checked':True,
            'word_model_scores_recomputed_by_default_verifier':False,
            'optional_exact_replay':'python experiments/p137_publicity_fragment/replay_discovery.py --lexicon /path/to/lexicon.txt',
            'authored_positive_correct_labels':54,'authored_positive_total_labels':127,
            'historical_uniqueness_probability':None,'limits':d['limits']}


def build(pdf=None):
    data = load(HERE/'inputs.json')
    base = load(checked(data['baseline_inputs'])); checked(data['baseline_certificate'])
    checked(data['arithmetic_dependency'])
    keys = {k['id']:k for k in load(ROOT/'data/keys.json')['keys']}
    key = data['key']; assert key == keys['Nov4-6'] == base['key']
    rec, = data['records']; assert rec['id'] == 'p137_A6'
    assert data['equivalent_model_lengths'] == [254,256,258]
    assert data['full_clause_alternatives'] == [
        {'id':f'{adverb.lower()}_{verb.lower()}', 'start':13,
         'text':'DEROEFFENTLICHKEIT'+adverb+verb+'BLEIBEN'}
        for adverb in ['NICHT','IMMER','LANGE'] for verb in ['VERBORGEN','VERGOENNT']]
    assert data['article_alternatives'] == ['DER','DEN','DEM','DIE']
    assert data['optional_von'] == {'start':124,'text':'VON','included_in_primary':False}
    assert data['unresolved_semantic_spans'] == [
        {'start':31,'stop':36,'equal_price_examples':['NICHT','IMMER','LANGE']},
        {'start':36,'stop':45,'equal_price_examples':['VERBORGEN','VERGOENNT']}]
    assert rec['model'] == {'kind':'unknown_leading_interference','modeled_coordinates':254,
                            'leading_unknown_coordinates':180,'full_length_established':False}
    assert rec['proposed_spans'] == [
        {'start':13,'stop':31,'text':'DEROEFFENTLICHKEIT'},
        {'start':45,'stop':52,'text':'BLEIBEN'}]
    assert (rec['printed_page'],rec['pdf_page_1based'],rec['source_section'],
            rec['message_part'],rec['message_total_parts'],rec['source_image_id']) == (137,140,'A6',6,8,'p137_A6_source')
    assert rec['literal_source_slots'] == 74 and rec['valid_source_coordinates'] == 71
    assert rec['printed_mask_indices'] == [25,26,27]
    assert data['geometry_audit'] == {'minimum':74,'maximum':1000,'step':2,'all_offsets':True,
                                    'pattern':'DEROEFFENTLICHKEIT'+'?'*14+'BLEIBEN',
                                    'minimum_observed_halves':15}
    assert data['source'] == base['source']
    crop, = data['source_images']
    assert (crop['id'],crop['path'],crop['printed_page'],crop['pdf_page_1based'],
            crop['crop_pdf_points'],crop['render_scale']) == ('p137_A6_source','sources/p137_a6.png',137,140,[55,430,506,478],4)
    source = literal(rec); assert len(source) == 74 and sum(c in C for c in source) == 71
    assert [i for i,c in enumerate(source) if c not in C] == [25,26,27] and set(source) == set(C+'-')
    old = next(r for r in base['contextual_unread_records'] if r['id'] == rec['id'])
    assert [s.replace('{INTERFERENCE_1} ', '') for s in old['source_rows']] == rec['source_rows']
    assert old['advertised_length'] is None and rec['advertised_length'] is None
    assert all(rec[field] == old[field] for field in ['printed_page','pdf_page_1based',
        'source_section','message_part','message_total_parts'])
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    template = rec['readable_candidate']
    assert template == '?'*13+'DEROEFFENTLICHKEIT'+'?'*14+'BLEIBEN'+'?'*75
    primary = proposal(source,key,254,template,'primary_254',full=True)
    assert primary['raw'] == rec['expected_raw'] == '?'*127
    s = primary['summary']
    assert (s['proposed_positions'],s['observed_half_coordinates_preserved'],s['added_missing_coordinate_fills']) == (25,15,35)
    assert s['observed_coordinate_substitutions'] == s['printed_mask_fills'] == 0
    assert s['remaining_added_unknown_coordinates'] == 145 and s['remaining_printed_masks'] == 3
    assert s['wholly_unobserved_proposed_positions'] == [15,17,19,22,25,26,29,46,49,51]
    assert primary['forward_witness']['ciphertext_sha256'] == '26df2229bca588c8e21ce1952856315f6e351715da0196f96c66c346f02ee737'
    equivalents = []
    common_projection = [p['source_indices'] for p in primary['positions']]
    for n in data['equivalent_model_lengths']:
        p = proposal(source,key,n,template+'?'*((n-254)//2),f'primary_{n}',full=True)
        assert [r['source_indices'] for r in p['positions'][:127]] == common_projection
        assert [r['pair'] for r in p['positions'][:127]] == [r['pair'] for r in primary['positions']]
        assert all(r['source_indices'] == [None,None] for r in p['positions'][127:])
        assert p['summary'] == {**s, 'remaining_added_unknown_coordinates': n-74-35}
        equivalents.append({'modeled_coordinates':n,'leading_unknown_coordinates':n-74,
                            'plaintext_positions':n//2,'raw_fixed_positions':0,
                            'candidate_fixed_positions':25,'candidate_unknown_positions':n//2-25,
                            'summary':p['summary'],'extra_wholly_unobserved_positions':p['positions'][127:],
                            'forward_witness':p['forward_witness']})
    variants = []
    for spec in data['full_clause_alternatives']:
        assert spec['start'] == 13 and len(spec['text']) == 39
        p = proposal(source,key,254,'?'*13+spec['text']+'?'*75,spec['id'])
        assert (p['summary']['proposed_positions'],p['summary']['observed_half_coordinates_preserved'],p['summary']['added_missing_coordinate_fills']) == (39,23,55)
        assert p['summary']['observed_coordinate_substitutions'] == p['summary']['printed_mask_fills'] == 0
        assert len(p['summary']['wholly_unobserved_proposed_positions']) == 16
        variants.append(p)
    assert len(variants) == 6
    articles = [proposal(source,key,254,'?'*13+word+'?'*111,'article_'+word.lower()) for word in data['article_alternatives']]
    assert [p['summary']['observed_coordinate_substitutions'] for p in articles] == [0,0,0,1]
    optional = proposal(source,key,254,'?'*124+'VON','optional_von')
    assert (optional['summary']['proposed_positions'],optional['summary']['observed_half_coordinates_preserved'],optional['summary']['added_missing_coordinate_fills']) == (3,2,4)
    assert optional['summary']['wholly_unobserved_proposed_positions'] == [124]
    context = data['following_part_context']
    assert context['record_id'] == 'p129_A7'
    assert context['native_prefix'] == 'ALLGEMEINERHIERNICHTBEKANNTERPOLITISCHERLAGE'
    assert context['association'] == base['proposed_cross_page_assembly']
    a7 = next(r for r in base['records'] if r['id'] == context['record_id'])
    a7_source = literal(a7); a7_read = read(a7_source.replace('-','?'),key,list(range(len(a7_source))))
    prefix = context['native_prefix']; assert a7_read['raw'].startswith(prefix)
    native_context = a7_read['positions'][:len(prefix)]
    assert all(all(c in C for c in p['pair']) for p in native_context)
    donor_spec = data['native_vocabulary_witness']
    assert donor_spec['record_id'] == 'p163_A14' and donor_spec['start'] == 0 and donor_spec['text'] == 'BLEIBEN'
    donor_input = load(checked(donor_spec['inputs']))
    donor = next(r for r in donor_input['records'] if r['id'] == donor_spec['record_id'])
    donor_source = literal(donor)
    donor_read = read(donor_source.replace('-','?'),keys['Nov7-9'],list(range(len(donor_source))))
    donor_positions = donor_read['positions'][:7]
    assert donor_read['raw'].startswith(donor_spec['text']) and all(all(c in C for c in p['pair']) for p in donor_positions)
    words = []
    for start, stop, word in [(13,16,'DER'),(16,31,'OEFFENTLICHKEIT'),(45,52,'BLEIBEN')]:
        rows = [p for p in primary['proposal_position_support'] if start <= p['plaintext_index'] < stop]
        observed = sum(p['observed_halves'] for p in rows)
        words.append({'word':word,'start':start,'stop':stop,'observed_halves':observed,
                      'added_coordinate_fills':2*len(rows)-observed,
                      'wholly_unobserved_positions':[p['plaintext_index'] for p in rows if p['wholly_unobserved']]})
    for path in [ROOT/data['case'], HERE/'README.md']:
        if path.exists():
            blocks = re.findall(r'```text\n(.*?)\n```',path.read_text(),re.S)
            assert blocks == [primary['raw'],template,'\n'.join(rec['source_rows'])], str(path)
    record = {'id':rec['id'],'literal_source':source,'literal_printed_rows':rec['source_rows'],
              'source_slots':74,'valid_coordinates':71,'ciphertext':primary['ciphertext'],
              'model_to_source_indices':primary['model_to_source_indices'],'raw':primary['raw'],
              'fixed_positions':0,'positions':primary['positions'],
              'readable_candidate':primary['readable_candidate'],
              'proposal_position_support':primary['proposal_position_support'],
              'forward_witness':primary['forward_witness']}
    return {'schema':'adfgvx-p137-publicity-fragment-certificate-v1','authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':data['indexing'],
            'summary':{'physical_records':1,'native_source_slots':74,'valid_source_coordinates':71,
                       'printed_source_masks':3,'modeled_coordinates':254,'added_unknown_prefix_coordinates':180,
                       'source_coordinates_excluded_reordered_or_changed':0,'plaintext_positions':127,
                       'raw_fixed_positions':0,'candidate_fixed_positions':25,'candidate_unknown_positions':102,
                       'observed_coordinate_substitutions':0,'printed_mask_fills':0,
                       'added_missing_coordinate_fills':35,'remaining_added_unknown_coordinates':145,
                       'remaining_printed_source_masks':3,'observed_half_coordinates_supporting_proposal':15,
                       'wholly_unobserved_proposed_positions':s['wholly_unobserved_proposed_positions'],
                       'full_length_established':False,'historical_uniqueness_claim':False},
            'records':[record],'per_word_half_coordinate_support':words,
            'equivalent_frames':{'frames':equivalents,'shared_plaintext_positions':127,
                'all_received_coordinate_ownerships_and_pairs_identical':True,
                'shared_pretransposition_source_ownerships':[v for p in common_projection for v in p],
                'conclusion':'The full received-source projection is identical. The source cannot distinguish these three total lengths.'},
            'full_clause_alternatives':variants,'local_article_alternatives':articles,
            'optional_von_excluded_from_primary':optional,
            'bounded_sparse_pattern_geometry_audit':geometry_audit(data,source,key),
            'following_part_context':{**context,'native_prefix_positions':native_context},
            'native_word_witness':{**donor_spec,'positions':donor_positions},
            'discovery_audit':discovery_audit(data,source,keys),'limits':data['limits']},evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args()
    result,evidence = build(args.pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert result == load(path)
    else:
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary'],'source_evidence':evidence['summary']},indent=2))
