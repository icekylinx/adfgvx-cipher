#!/usr/bin/env python3
"""Reproduce the square-independent seven-target contact/coincidence diagnosis.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from math import factorial
from pathlib import Path
import random
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, transposition_indices
from adfgvx.source_evidence import verify_source_evidence
C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()


def normalize(source):
    return ''.join(c if c in C else '?' for c in source)


def original_rows(record):
    return ''.join(''.join(record.get('source_rows',record.get('rows',''))).split())


def origins(n, ranks):
    """Independent column-offset construction; output is native wire ownership."""
    height, extra = divmod(n,len(ranks))
    lengths = [height+int(i < extra) for i in range(len(ranks))]
    offset = [sum(lengths[j] for j in range(len(ranks)) if ranks[j] < rank)
              for rank in ranks]
    out = [offset[i % len(ranks)]+i//len(ranks) for i in range(n)]
    assert sorted(out) == list(range(n))
    assert out == list(np.argsort(transposition_indices(n,ranks)))
    return out


def statistics(source, maps):
    """Exact integer cell-contact counts; unknown halves never become letters."""
    values = np.array([C.index(c) if c in C else 6 for c in source]+[6],dtype=np.int8)
    mid = values[maps]
    pairs = 7*mid[:,::2]+mid[:,1::2]
    labels = 49*np.arange(len(maps))[:,None]+pairs
    counts = np.bincount(labels.ravel(),minlength=49*len(maps)).reshape(-1,7,7)[:,:6,:6]
    n = counts.sum((1,2)); nn = n*(n-1)
    cell = (counts*(counts-1)).sum((1,2))
    row = counts.sum(2); col = counts.sum(1)
    row_equal = (row*(row-1)).sum(1); col_equal = (col*(col-1)).sum(1)
    numerator = cell*nn-row_equal*col_equal
    denominator = nn*nn
    scores = np.divide(numerator,denominator,out=np.full(len(maps),-np.inf),where=denominator > 0)
    return counts,n,cell,row_equal,col_equal,numerator,denominator,scores


def row(a, i, with_counts=False):
    counts,n,cell,rows,cols,numerators,denominators,scores = a
    result = {'complete_observed_pairs':int(n[i]),
              'cell_equal_ordered_pairs':int(cell[i]),
              'row_equal_ordered_pairs':int(rows[i]),
              'column_equal_ordered_pairs':int(cols[i]),
              'excess_numerator':int(numerators[i]),
              'excess_denominator':int(denominators[i]),
              'excess_cell_ic':None if not denominators[i] else round(float(scores[i]),12)}
    if with_counts:
        result['cell_counts'] = counts[i].tolist()
    return result


def maximum(a):
    candidates = np.flatnonzero(a[-1] == a[-1].max()).tolist()
    assert candidates and np.isfinite(a[-1][candidates[0]])
    winner = max(candidates,key=lambda i:Fraction(int(a[5][i]),int(a[6][i])))
    tied = [i for i in candidates if int(a[5][i])*int(a[6][winner]) == int(a[5][winner])*int(a[6][i])]
    return winner,tied


def model_family(record, keys):
    source = record['analysis_source']; n = len(source)
    maps, descriptions = [], []
    if record['id'] == 'p198':
        assert n == 165
        for key in keys:
            inv = np.array(origins(170,key['column_rank_order']))
            for gap in range(166):
                owner = np.where(inv < gap,inv,np.where(inv < gap+5,n,inv-5))
                assert sorted(i for i in owner.tolist() if i != n) == list(range(n))
                maps.append(owner)
                descriptions.append({'key_id':key['id'],'modeled_coordinates':170,'gap_before_source':gap})
    else:
        assert n % 2 == 0
        for key in keys:
            maps.append(origins(n,key['column_rank_order']))
            descriptions.append({'key_id':key['id'],'modeled_coordinates':n,'gap_before_source':None})
    return np.array(maps,dtype=np.int16),descriptions


def shuffle_source(source, rng):
    chars = [c for c in source if c in C]
    rng.shuffle(chars); it = iter(chars)
    result = ''.join(next(it) if c in C else '?' for c in source)
    assert Counter(result) == Counter(source)
    assert [i for i,c in enumerate(result) if c == '?'] == [i for i,c in enumerate(source) if c == '?']
    return result


def diagnose(record, keys, seed, samples):
    source = record['analysis_source']; maps,models = model_family(record,keys)
    a = statistics(source,maps); winner,tied = maximum(a)
    if record['id'] == 'p198':
        retained = []
        for start in range(0,len(models),166):
            local = tuple(x[start:start+166] for x in a)
            at, _ = maximum(local); retained.append(start+at)
        assert len(models) == 4150
    else:
        retained = list(range(len(models))); assert len(models) == 25
    order = sorted(retained,key=lambda i:Fraction(int(a[5][i]),int(a[6][i])),reverse=True)
    rng = random.Random(seed); maxima = []; source_hash = hashlib.sha256()
    for _ in range(samples):
        shuffled = shuffle_source(source,rng); source_hash.update((shuffled+'\n').encode())
        b = statistics(shuffled,maps); at, _ = maximum(b)
        maxima.append([int(b[5][at]),int(b[6][at]),at])
    exceed = sum(num*int(a[6][winner]) >= int(a[5][winner])*den for num,den,_ in maxima)
    exact_table = [[int(a[j][i]) for j in range(1,7)] for i in range(len(models))]
    result = {'id':record['id'],'source_slots':len(source),
              'coordinate_histogram':{c:source.count(c) for c in C+'?'},
              'declared_models_evaluated':len(models),'complete_integer_table_sha256':digest(exact_table),
              'leader':{'model':models[winner],**row(a,winner,True)},
              'all_tied_leading_models':[models[i] for i in tied],
              'rank_vector_summaries':[{'model':models[i],**row(a,i)} for i in order],
              'matched_shuffles':{'count':samples,'seed':seed,
                  'all_generated_source_streams_sha256':source_hash.hexdigest(),
                  'maxima_at_least_observed_maximum':exceed,
                  'maxima_columns':['excess_numerator','excess_denominator','first_best_model_index'],
                  'maxima':maxima,
                  'every_shuffle_evaluates_all_declared_models':True}}
    if 'key_id' in record:
        at = next(i for i,m in enumerate(models) if m['key_id'] == record['key_id'])
        result['known_native_rank_key'] = record['key_id']
        result['known_native_key_rank'] = order.index(at)+1
        result['known_native_key_statistics'] = row(a,at,True)
        assert result['known_native_key_rank'] == 1
    return result


def scalar_counts(source, ranks):
    """Independent chunk/row reconstruction used only by the tiny oracle."""
    columns = {}; offset = 0; n = len(source)
    for c in sorted(range(len(ranks)),key=lambda i:ranks[i]):
        size = len(range(c,n,len(ranks)))
        columns[c] = source[offset:offset+size]; offset += size
    mid = ''.join(columns[i % len(ranks)][i//len(ranks)] for i in range(n))
    cells = [[0]*6 for _ in C]
    for i in range(0,n,2):
        if all(c in C for c in mid[i:i+2]):
            cells[C.index(mid[i])][C.index(mid[i+1])] += 1
    return cells


def oracle():
    ranks = list(permutations([1,2,3])); maps = np.array([origins(6,list(r)) for r in ranks])
    checked = 0
    for values in product('AD?',repeat=6):
        source = ''.join(values); actual = statistics(source,maps)
        for i, rank in enumerate(ranks):
            expected = scalar_counts(source,rank)
            assert actual[0][i].tolist() == expected
            n = sum(map(sum,expected)); c = sum(v*(v-1) for line in expected for v in line)
            rs = [sum(line) for line in expected]; cs = [sum(line[j] for line in expected) for j in range(6)]
            rp = sum(v*(v-1) for v in rs); cp = sum(v*(v-1) for v in cs)
            assert int(actual[5][i]) == c*n*(n-1)-rp*cp
            assert int(actual[6][i]) == (n*(n-1))**2
            checked += 1
    assert checked == 4374
    return {'exhaustive_tiny_source_rank_checks':checked,
            'scope':'All3^6 strings over A,D,? and all6 permutations of three columns; integer contact counts and statistic checked by independent chunk/row reconstruction.'}


def pair_order_audit(spec, source, key):
    n = spec['modeled_coordinates']; ranks = key['column_rank_order']; k = len(ranks)
    assert n == len(source) == 206 and k == 22
    height,extra = divmod(n,k); assert extra % 2 == 0
    long,short = extra//2,(k-extra)//2
    assert (long,short) == (4,7)
    count = 2*factorial(long)*factorial(short)
    assert count == spec['distinct_same_statistic_rank_vectors'] == 241920
    base = statistics(source,np.array([origins(n,ranks)]))
    rng = random.Random(spec['examples_seed']); examples = []
    for _ in range(spec['random_examples']):
        left = list(range(long)); right = list(range(long,k//2)); rng.shuffle(left);rng.shuffle(right)
        for transpose in [False,True]:
            pair_order = left+right
            permutation = [2*j+h for j in pair_order for h in ([1,0] if transpose else [0,1])]
            changed = [ranks[i] for i in permutation]
            result = statistics(source,np.array([origins(n,changed)]))
            assert result[0][0].tolist() == (base[0][0].T if transpose else base[0][0]).tolist()
            assert row(result,0) == row(base,0) or (
                transpose and result[3][0] == base[4][0] and result[4][0] == base[3][0]
                and result[5][0] == base[5][0] and result[6][0] == base[6][0])
            examples.append({'ranks':changed,'global_half_swap':transpose,'cell_counts_sha256':digest(result[0][0].tolist())})
    return {'height':height,'long_pair_columns':long,'short_pair_columns':short,
            'distinct_rank_vectors_in_proved_invariance_family':count,
            'checked_examples':examples,
            'proof':'Permuting whole adjacent column pairs within a shared height class permutes plaintext pair positions without changing the cell multiset. Swapping both columns in every pair transposes the cell table and swaps its marginal tables. Both operations preserve the stated statistic. They preserve all original source coordinates and printed mask slots.'}


def p194_observability(record, keys, spec):
    source = record['analysis_source']; assert len(source) == 45 and '?' not in source
    rows = []
    for key in keys:
        for start in spec['source_start_positions']:
            owner = [len(source)]*214
            owner[start:start+45] = range(45)
            inv = origins(214,key['column_rank_order'])
            mapping = [owner[i] for i in inv]
            counts = [sum(i != 45 for i in mapping[j:j+2]) for j in range(0,214,2)]
            rows.append({'key_id':key['id'],'source_start':start,
                         'fully_observed_pairs':counts.count(2),'half_observed_pairs':counts.count(1),
                         'wholly_unobserved_pairs':counts.count(0),
                         'pretransposition_source_owners_sha256':digest([None if i == 45 else i for i in mapping])})
    nearby = [r for r in rows if r['key_id'] in spec['near_period_keys']]
    assert len(nearby) == 10 and all((r['fully_observed_pairs'],r['half_observed_pairs'],r['wholly_unobserved_pairs']) == (0,45,62) for r in nearby)
    assert len(rows) == 50
    return {'id':record['id'],'source_slots':45,'coordinate_histogram':{c:source.count(c) for c in C},
            'modeled_coordinates':214,'added_unknown_coordinates':169,
            'prefix_and_suffix_models':rows,'near_period_models':nearby,
            'coincidence_score_reported_for_near_period_models':False,
            'reason':'No complete observed pair exists in these ten declared near-period prefix/suffix models. Half-coordinates still constrain letter domains; they are not plaintext labels. The original location of the fragment is not established.'}


def build(pdf=None):
    data = load(HERE/'inputs.json')
    assert [r['id'] for r in data['targets']] == ['p73','p170','p198','p70_B1','p127_B2','p145_A','p194_D1']
    assert [r['id'] for r in data['native_controls']] == ['p127_B1','p145_B1','p145_B3','p72_A3','p194_C','p194_E']
    protocol = data['shuffle_protocol']
    assert protocol['samples_per_body'] == 128 and protocol['seed_base'] == 7052816
    assert protocol['ordered_body_ids'] == [r['id'] for r in data['targets'][:-1]+data['native_controls']]
    assert data['p198_family'] == {'modeled_coordinates':170,'added_unknown_coordinates':5,'gap_positions':list(range(166)),'contiguous_loss_established':False}
    assert data['p194_family']['source_start_positions'] == [0,169]
    assert data['p194_family']['added_unknown_coordinates'] == 169
    assert data['p194_family']['placement_established'] is False
    assert data['pair_order_invariance'] == {'source_id':'p70_B1','key_id':'Oct4-6',
        'modeled_coordinates':206,'long_pair_columns':4,'short_pair_columns':7,
        'distinct_same_statistic_rank_vectors':241920,'examples_seed':706194,'random_examples':32}
    assert data['p194_family']['modeled_coordinates'] == 214 and data['p194_family']['received_coordinates'] == 45
    assert data['p194_family']['near_period_keys'] == ['Nov13-15a','Nov13-15b','CHI-Nov13','Nov16-18','CHI-Nov8-2026-recovery']
    canonical_keys = {k['id']:k for k in load(ROOT/'data/keys.json')['keys']}
    keys = data['rank_hypotheses']; assert len(keys) == len({k['id'] for k in keys}) == 25
    for key in keys:
        assert key['column_rank_order'] == canonical_keys[key['id']]['column_rank_order']
    for r in data['targets']:
        assert r['encryption_date_established'] is False
        assert r['family'] == ('five_consecutive_losses' if r['id'] == 'p198' else
            'prefix_and_suffix_observability' if r['id'] == 'p194_D1' else 'literal_complete_frame')
        binding = r['source_binding']; original = next(x for x in load(ROOT/binding['path'])[binding['collection']] if x['id'] == r['id'])
        if binding['collection'] == 'messages':
            literal = original['transcript']['raw_source_compact']; analysis = original['transcript']['analysis_ciphertext']
            header = original['source']['header_transcription']; page = original['source']['printed_page']; advertised = original['source']['advertised_length']
        else:
            literal = original_rows(original); analysis = normalize(literal)
            header = original['header_transcription']; page = original['printed_page']; advertised = original['advertised_length']
        assert (r['literal_source'],r['analysis_source'],r['header'],r['printed_page'],r['advertised_length']) == (literal,analysis,header,page,advertised)
    control_raw = []
    for r in data['native_controls']:
        ref = r['source_binding']; path = ROOT/ref['path']; assert sha(path) == ref['sha256']
        original_input = load(path); original = next(x for x in original_input['records'] if x['id'] == r['id'])
        source = normalize(original.get('analysis_source',original_rows(original)))
        assert source == r['analysis_source'] and r['native_no_candidate_edits'] is True and r['frame'] == 'literal_source_length'
        key_id = original.get('key_id',original_input.get('key',{}).get('id'))
        assert key_id == r['key_id']; key = canonical_keys[key_id]
        raw = decrypt(source,key['column_rank_order'],key['square'])
        if 'expected_raw' in original:
            assert raw == original['expected_raw']
        control_raw.append({'id':r['id'],'key_id':key_id,'literal_keyed_raw':raw,
                            'received_source_repaired':False,'purpose':'Previously source-reviewed native body used only to check rank diagnosis; no reading or square is fitted here.'})
    results = [diagnose(r,keys,protocol['seed_base']+i,128)
               for i,r in enumerate(data['targets'][:-1]+data['native_controls'])]
    assert len(results) == 12
    assert [r['matched_shuffles']['maxima_at_least_observed_maximum'] for r in results] == [22,73,38,61,44,109,0,0,2,0,0,0]
    p194 = p194_observability(data['targets'][-1],keys,data['p194_family'])
    p70 = next(r['analysis_source'] for r in data['targets'] if r['id'] == 'p70_B1')
    invariance = pair_order_audit(data['pair_order_invariance'],p70,canonical_keys['Oct4-6'])
    evidence = verify_source_evidence(pdf,data['source'],data['source_images'],HERE)
    return {'schema':'adfgvx-open-target-contact-certificate-v1','authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),
            'summary':{'open_targets':7,'native_control_bodies':6,'rank_hypotheses':25,
                       'ranked_target_families':6,'p194_observability_models':50,
                       'p198_contiguous_loss_models':4150,'shuffled_sources_per_ranked_body':128,
                       'shuffled_source_families':1536,'native_controls_ranking_known_key_first':6,
                       'new_plaintext_positions':0,'accepted_open_target_keys':0,'source_repairs':0,
                       'historical_uniqueness_probability':None},
            'diagnoses':results,'p194_observability':p194,'native_control_raw':control_raw,
            'pair_order_invariance':invariance,'small_exhaustive_oracle':oracle(),
            'limits':data['limits']},evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args = parser.parse_args(); result,evidence = build(args.pdf)
    path = HERE/'certificates.json'
    if args.verify:
        assert result == load(path)
    else:
        path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary'],'source_evidence':evidence['summary']},indent=2))
