#!/usr/bin/env python3
"""Verify native Nov9 sources and acyclic cross-copy coordinate restoration.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import itertools
import json
import re
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect, repair
from experiments.arad_provisions_partial.verify import stage, framed

C = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal(record):
    return ''.join(''.join(record['source_rows']).split())


def fold(text):
    return ''.join(c for c in text.upper() if c in ALPHABET + '?').replace('X', '')


def origin_value(origin, sources):
    value = sources[origin['record_id']][origin['source_index']]
    assert value in C, origin
    return value


def complete_witness(cipher, key, template=None):
    witnesses = []
    missing = sorted(set(ALPHABET) - set(key['square']))
    holes = [i for i, c in enumerate(key['square']) if c == '?']
    assert len(missing) == len(holes) == 2
    for values in itertools.permutations(missing):
        square = list(key['square'])
        for i, value in zip(holes, values):
            square[i] = value
        square = ''.join(square)
        full = cipher.replace('?', 'A')
        text = decrypt(full, key['column_rank_order'], square)
        assert encrypt(text, key['column_rank_order'], square) == full
        if template is not None:
            assert all(a == '?' or a == b for a, b in zip(template, text))
        witnesses.append({'square': square, 'ciphertext': full, 'plaintext': text,
                          'reencryption_exact': True, 'historical_completion_claim': False})
    return witnesses


def check_case(data, results, p159):
    from data.reviews.check_reading_presentation import expected_legend
    path = ROOT / data['case']
    text = path.read_text()
    assert text.count(expected_legend(path)) == 1
    for record, result in zip(data['records'], results):
        heading = '## ' + record['id'].replace('_', ' ') + '\n'
        assert text.count(heading) == 1
        section = text.split(heading, 1)[1].split('\n## ', 1)[0]
        bodies = re.findall(r'```text\n(.*?)\n```', section, re.S)
        expected = ['\n'.join(record['source_rows']), result['raw']]
        if 'source_linked' in result:
            expected.append(result['source_linked']['raw'])
        expected.append(result['readable_candidate']['raw'])
        assert bodies == expected, record['id']
        assert re.findall(r'^> (.*)$', section, re.M) == [record['readable_german']]
        assert fold(record['readable_german']) == fold(result['readable_candidate']['raw'])
    section = text.split('## Arad cross-copy restoration\n', 1)[1].split('\n## ', 1)[0]
    assert re.findall(r'```text\n(.*?)\n```', section, re.S) == [p159['source_linked']['raw']]
    assert '124 to 135' in section and '11 originally missing coordinates' in section


def source_only_family(source, reference, reference_mapping, sources, key, expected_linked):
    """Price the entire earlier edit family using observed coordinates only.

    No plaintext, substitution square or word template enters the objective.
    Prefix sums price the three retained segments separated by two five-slot
    gaps. Equal retained stage strings transfer the whole table to all four
    choices of duplicated source-group origin.
    """
    assert len(source) == 271 and len(reference) == len(reference_mapping) == 272
    count = 0
    digest = hashlib.sha256()
    histogram = Counter()
    minimum = 10**6
    best = []
    stage_cache = {}
    for one in range(115, 120):
        st, _ = stage(source, [25, 80], one)
        text = ''.join(c for c, _, _ in st)
        n = len(text)
        assert n == 262
        stage_cache[one] = text
        costs, comparisons = {}, {}
        for shift in (0, 5, 10):
            pc, pn = [0], [0]
            for i, value in enumerate(text):
                other = reference[i + shift]
                observed = value in C and other in C
                pc.append(pc[-1] + int(observed and value != other))
                pn.append(pn[-1] + int(observed))
            costs[shift], comparisons[shift] = pc, pn
        for a in range(n + 1):
            for b in range(a, n + 1):
                price = costs[0][a] + costs[5][b] - costs[5][a] + costs[10][n] - costs[10][b]
                compared = comparisons[0][a] + comparisons[5][b] - comparisons[5][a] + comparisons[10][n] - comparisons[10][b]
                count += 1
                histogram[price] += 1
                digest.update(f'{one},{a},{b},{price},{compared}\n'.encode())
                if price < minimum:
                    minimum, best = price, []
                if price == minimum:
                    best.append((one, a, b, compared))
    assert count == 173580 and minimum == 5
    assert best == [(118, 15, 110, 258), (118, 16, 110, 258)]
    assert digest.hexdigest() == 'a46e3534617710c1a71f98d1785187efb3f7593ba9003c59fac43b33eb6e19eb'
    branches = list(itertools.product([25, 30], [80, 85]))
    branch_proof, maps = [], []
    for branch in branches:
        for one in range(115, 120):
            st, _ = stage(source, branch, one)
            assert ''.join(c for c, _, _ in st) == stage_cache[one]
        branch_proof.append({'excluded_group_starts':list(branch),
                             'all_five_stage_strings_equal_to_canonical':True})
        for one, a, b, compared in best:
            st, excluded = stage(source, branch, one)
            frame, mapping, tags = framed(st, a, b)
            pairs = [(i,x,y) for i,(x,y) in enumerate(zip(frame,reference)) if x in C and y in C]
            disagreements = [{'model_index':i,'p159_coordinate':x,'p168_coordinate':y} for i,x,y in pairs if x != y]
            assert len(pairs) == compared == 258 and len(disagreements) == minimum
            linked = list(frame)
            origins = []
            for i, value in enumerate(frame):
                if value != '?':
                    continue
                donor_index = reference_mapping[i]
                assert donor_index is not None and sources['p168_E'][donor_index] in C
                assert donor_index not in [201, 202]
                origin = {'record_id':'p168_E','source_index':donor_index}
                supplied = origin_value(origin, sources)
                linked[i] = supplied
                origins.append({'model_index':i,'coordinate':supplied,'origin':origin,'slot_kind':tags[i]})
            linked = ''.join(linked)
            assert len(origins) == 11 and linked == expected_linked
            decoded = inspect(linked, key, mapping)
            assert decoded['fixed_positions'] == 135 and decoded['raw'][96:101] == '80000'
            maps.append({'excluded_group_starts':list(branch),'excluded_source_indices':excluded,
                         'one_coordinate_source_boundary':one,'first_five_gap_stage_boundary':a,
                         'second_five_gap_stage_boundary':b,'known_coordinate_disagreements':minimum,
                         'observed_comparisons':compared,'model_to_source_indices':mapping,
                         'ciphertext_with_unfilled_additions':frame,'disagreements':disagreements,
                         'copied_coordinate_origins':origins,'source_linked_ciphertext_sha256':hashlib.sha256(linked.encode()).hexdigest(),
                         'source_linked_fixed_positions':135})
    assert len(maps) == 8 and count * len(branches) == 694320
    # Compare the separate, earlier word-conditioned minima after the new
    # source-only optimum has already been established over the whole family.
    old = load(ROOT / 'experiments/arad_provisions_partial/certificates.json')['fixed_partial_target_comparison']
    assert old['minimum'] == 6 and len(old['all_minimizing_source_maps']) == 64
    comparison = []
    for row in old['all_minimizing_source_maps']:
        st, _ = stage(source, row['excluded_group_starts'], row['one_coordinate_source_boundary'])
        frame, mapping, _ = framed(st, row['first_five_gap_stage_boundary'], row['second_five_gap_stage_boundary'])
        assert frame == row['ciphertext_with_unfilled_additions'] and mapping == row['model_to_source_indices']
        cost = sum(x in C and y in C and x != y for x,y in zip(frame,reference))
        comparison.append({'excluded_group_starts':row['excluded_group_starts'],
                           'one_coordinate_source_boundary':row['one_coordinate_source_boundary'],
                           'first_five_gap_stage_boundary':row['first_five_gap_stage_boundary'],
                           'second_five_gap_stage_boundary':row['second_five_gap_stage_boundary'],
                           'earlier_quantity_domain':row['quantity_position']['domain'],
                           'source_only_disagreements':cost,'survives_source_only_minimum':cost == minimum})
    assert sum(r['survives_source_only_minimum'] for r in comparison) == 8
    p_only = [r for r in comparison if r['earlier_quantity_domain'] == 'P']
    assert len(p_only) == 48 and not any(r['survives_source_only_minimum'] for r in p_only)
    return {'objective':'Mismatches only where both source-frame coordinates are originally observed; all three unobserved p168 coordinates remain unassigned. No plaintext template.',
            'family':'Exclude one of each printed VDAGG and FFXDF pair; place one short-group slot before source115..119 and two ordered five-slot gaps at every a<=b in the262-slot stage.',
            'canonical_source_models':count,'source_origin_models':count * len(branches),
            'minimum_known_coordinate_disagreements':minimum,'canonical_minima':[list(r) for r in best],
            'canonical_price_sha256':digest.hexdigest(),
            'digest_format':'UTF-8 one,a,b,cost,observed_comparisons\\n in ascending one,a,b order.',
            'price_histogram':{str(k):histogram[k] for k in sorted(histogram)},
            'duplicate_origin_equality':branch_proof,'minimizing_source_maps':maps,
            'distinct_source_linked_ciphertexts':1,'common_linked_ciphertext':expected_linked,
            'common_linked_plaintext':inspect(expected_linked,key,maps[0]['model_to_source_indices'])['raw'],
            'earlier_word_conditioned_comparison':{'word_price':6,'earlier_minima':64,'survivors_at_source_only_minimum':8,
                                                  'excluded_P0000_maps':48,'all_earlier_maps':comparison},
            'limit':'The finite source-edit family is explicit. Eight source-origin minima remain; this does not prove unrestricted historical uniqueness.'}


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    key = data['key']
    assert key == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov7-9')
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    assert sha(HERE / 'prior_snapshot.json') == data['prior_snapshot_sha256']
    prior = load(HERE / 'prior_snapshot.json')
    old159 = prior['p159_record']
    donor153 = prior['p153_B1_record']
    live159 = load(ROOT / 'experiments/arad_provisions_partial/inputs.json')['record']
    live153 = next(r for r in load(ROOT / 'experiments/nov7_danube_and_message_reports/inputs.json')['records'] if r['id'] == 'p153_B1')
    assert literal(old159) == literal(live159) and old159['analysis_frame'] == live159['analysis_frame']
    assert literal(donor153) == literal(live153)
    sources = {r['id']: literal(r) for r in data['records']}
    sources.update(p159_A=literal(old159), p153_B1=literal(donor153))
    out = []
    for r in data['records']:
        lit = sources[r['id']]
        assert len(lit) == r['source_slots']
        base = ''.join(c if c in C else '?' for c in lit)
        mapping = list(range(len(lit)))
        if r['id'] == 'p168_E':
            assert len(lit) == 271 and r['advertised_length'] == 272
            assert lit[50:54] == 'DDGX' and sources['p159_A'][50:55] == 'DDGGX'
            group_fits = []
            for boundary in range(50, 55):
                for ch in C:
                    group = lit[50:boundary] + ch + lit[boundary:54]
                    if group == sources['p159_A'][50:55]:
                        group_fits.append({'source_boundary': boundary, 'coordinate': ch})
            assert group_fits == [{'source_boundary':52,'coordinate':'G'}, {'source_boundary':53,'coordinate':'G'}]
            base = base[:52] + '?' + base[52:]
            mapping = mapping[:52] + [None] + mapping[52:]
        else:
            assert len(lit) == r['advertised_length']
        raw = inspect(base, key, mapping)
        assert raw['raw'] == r['expected_raw']
        candidate = repair(r['edited_output'], base, key, mapping, lit)
        assert len(candidate['known_coordinate_substitutions']) == r['expected_substitutions']
        assert len(candidate['erased_coordinate_fills']) == r['expected_erasure_fills']
        candidate['global_completion_witnesses'] = complete_witness(candidate['ciphertext'], key, candidate['raw'])
        result = {'id': r['id'], 'literal_source': lit, 'source_slots':len(lit),
                  'valid_source_coordinates':sum(c in C for c in lit), 'ciphertext':base,
                  'model_to_source_indices':mapping, **raw, 'readable_candidate':candidate,
                  'readable_german':r['readable_german']}
        if r['id'] == 'p164_C1':
            old = next(v for v in prior['p164_sources'] if v['id'] == r['id'])
            normalized = ''.join(c if c in C else '?' for c in old['raw_ciphertext'])
            assert [(i,a,b) for i,(a,b) in enumerate(zip(normalized,base)) if a != b] == [(148,'X','V')]
            assert old['plaintext'][110] == 'S' and raw['raw'][110] == 'E'
            don = inspect(sources['p153_B1'], key, list(range(len(sources['p153_B1']))))
            fills = [(59, donor153['expected_raw'].index('DONAU') + 4),
                     (112, donor153['expected_raw'].index('UEBSRSETZ') + 5)]
            template = list(raw['raw'])
            links = []
            for target_index, donor_index in fills:
                assert template[target_index] == '?'
                value = don['raw'][donor_index]
                assert value in raw['positions'][target_index]['domain']
                template[target_index] = value
                assert all(p is not None and sources['p153_B1'][p] in C for p in don['positions'][donor_index]['source_indices'])
                links.append({'target_plaintext_index':target_index, 'value':value,
                              'donor_record':'p153_B1', 'donor_plaintext_index':donor_index,
                              'donor_observed_pair':don['positions'][donor_index]})
            linked = repair(''.join(template), base, key, mapping, lit)
            assert not linked['known_coordinate_substitutions'] and len(linked['erased_coordinate_fills']) == 2
            assert raw['fixed_positions'] == 119 and linked['fixed_positions'] == 121
            result['source_linked'] = linked
            result['parallel_passage_mask_support'] = links
            supported = []
            for target_word, target_offset, donor_word, donor_offset in [('DONA?UEBER',6,'DONAUU3BER',6),('BELGRAD',5,'BELGR4D',5),('UEBER?ETZ',3,'UEBSRSETZ',3)]:
                ti=raw['raw'].index(target_word)+target_offset;di=don['raw'].index(donor_word)+donor_offset
                assert raw['positions'][ti]['raw'] == live153['edited_output'][di]
                assert don['raw'][di] != raw['raw'][ti]
                assert all(lit[j] in C for j in raw['positions'][ti]['source_indices'])
                supported.append({'target_p153_plaintext_index':di,'earlier_raw':don['raw'][di],
                                  'proposed':raw['raw'][ti],'p164_native_pair':raw['positions'][ti]})
            result['p153_word_repairs_supported_by_native_pairs'] = supported
            result['source_glyph_correction'] = data['source_glyph_correction']
        if r['id'] == 'p168_E':
            borrowed = [{'model_index':52,'origin':{'record_id':'p159_A','source_index':52}},
                        {'model_index':202,'origin':{'record_id':'p159_A','source_index':201}},
                        {'model_index':203,'origin':{'record_id':'p159_A','source_index':202}}]
            linked = list(base)
            for item in borrowed:
                assert linked[item['model_index']] == '?'
                item['coordinate'] = origin_value(item['origin'], sources)
                linked[item['model_index']] = item['coordinate']
            linked = ''.join(linked)
            analysis = inspect(linked,key,mapping)
            assert raw['fixed_positions'] == 132 and analysis['fixed_positions'] == 135
            result['source_linked'] = {'ciphertext':linked,**analysis,'copied_coordinate_origins':borrowed,
                                       'observed_coordinate_substitutions':0,'source_linked_additional_fixed_positions':3}
            result['short_group_exact_completion_witnesses'] = group_fits
            result['quantity_native_pair_witnesses'] = raw['positions'][96:101]
            assert raw['raw'][96:101] == '80000'
            for p in result['quantity_native_pair_witnesses']:
                assert all(i is not None and lit[i] in C for i in p['source_indices'])
        out.append(result)
    byid = {r['id']:r for r in out}
    # Every p159 lost-slot value comes from an original observed p168 coordinate,
    # avoiding the p168 gap and both p168 masks that borrow values from p159.
    spec = old159['analysis_frame']
    st, excluded = stage(sources['p159_A'],spec['primary_excluded_group_starts'],spec['single_gap_before_source_index'])
    oldbase, oldmap, tags = framed(st,spec['first_five_gap_stage_boundary'],spec['second_five_gap_stage_boundary'])
    oldraw = inspect(oldbase,key,oldmap)
    assert oldraw['raw'] == old159['expected_raw'] and oldraw['fixed_positions'] == 124
    e = byid['p168_E']; linked = list(oldbase); coordinate_links = []
    for model_index, coordinate in enumerate(oldbase):
        if coordinate != '?':
            continue
        donor_index = e['model_to_source_indices'][model_index]
        assert donor_index is not None and sources['p168_E'][donor_index] in C
        assert donor_index not in [201,202]
        origin = {'record_id':'p168_E','source_index':donor_index}
        value = origin_value(origin,sources)
        linked[model_index] = value
        coordinate_links.append({'model_index':model_index,'coordinate':value,'origin':origin,'slot_kind':tags[model_index]})
    assert len(coordinate_links) == 11
    linked=''.join(linked); oldlinked=inspect(linked,key,oldmap)
    assert oldlinked['fixed_positions'] == 135 and oldlinked['raw'][96:101] == '80000'
    oldcandidate=repair(e['readable_candidate']['raw'],oldbase,key,oldmap,sources['p159_A'])
    assert len(oldcandidate['known_coordinate_substitutions']) == 7
    assert len(oldcandidate['erased_coordinate_fills']) == 11
    assert all(oldcandidate['ciphertext'][item['model_index']] == item['coordinate']
               for item in coordinate_links)
    oldcandidate['global_completion_witnesses']=complete_witness(oldcandidate['ciphertext'],key,oldcandidate['raw'])
    p159={'id':'p159_A','primary_geometry':spec,'excluded_source_indices':excluded,
          'ciphertext_with_unfilled_additions':oldbase,'model_to_source_indices':oldmap,
          'source_only':oldraw,'source_linked':{'ciphertext':linked,**oldlinked},
          'copied_coordinate_origins':coordinate_links,'source_linked_additional_fixed_positions':11,
          'common_edited_candidate':oldcandidate}
    disagreements=[]
    for i,(a,b)in enumerate(zip(oldbase,e['ciphertext'])):
        if a in C and b in C and a!=b:
            disagreements.append({'model_index':i,'p159_source_index':oldmap[i],
                                  'p159_coordinate':a,'p168_source_index':e['model_to_source_indices'][i],
                                  'p168_coordinate':b})
    assert len(disagreements)==5
    p159['retained_observed_copy_disagreements']=disagreements
    source_family = source_only_family(sources['p159_A'], e['ciphertext'], e['model_to_source_indices'], sources, key, linked)
    joint=[]
    for a,b in zip(complete_witness(linked,key), complete_witness(e['source_linked']['ciphertext'],key)):
        assert a['square']==b['square'] and a['plaintext'][131]==b['plaintext'][131] in '56'
        assert a['plaintext'][96:101]==b['plaintext'][96:101]=='80000'
        joint.append({'square':a['square'],'p159_plaintext':a['plaintext'],'p168_plaintext':b['plaintext'],
                      'common_footer_label':a['plaintext'][131],'declared_linked_ciphertexts_reencrypt_exactly':True})
    check_case(data,out,p159)
    summary={'physical_records':2,'printed_source_slots':519,'modeled_coordinates':520,
             'plaintext_positions':260,'baseline_fixed_positions':251,
             'source_linked_fixed_positions':256,'candidate_fixed_positions':257,
             'known_coordinate_substitutions':8,'source_mask_fills':5,'inserted_slot_fills':1,
             'inserted_slots':1,'source_exclusions':0,'additional_p159_source_linked_positions':11}
    assert sum(r['source_slots'] for r in out)==summary['printed_source_slots']
    assert sum(len(r['raw']) for r in out)==summary['plaintext_positions']
    assert sum(r['fixed_positions'] for r in out)==summary['baseline_fixed_positions']
    assert sum(r['readable_candidate']['fixed_positions'] for r in out)==summary['candidate_fixed_positions']
    assert sum(len(r['readable_candidate']['known_coordinate_substitutions']) for r in out)==summary['known_coordinate_substitutions']
    fills=[event for r in out for event in r['readable_candidate']['erased_coordinate_fills']]
    assert sum(e['source_index'] is None for e in fills)==summary['inserted_slot_fills']
    assert sum(e['source_index'] is not None for e in fills)==summary['source_mask_fills']
    return {'schema':'adfgvx-nov8-remaining-source-certificate-v1','authors':data['authors'],
            'input_sha256':sha(HERE/'inputs.json'),'indexing':data['indexing'],
            'summary':summary,'records':out,'p159_source_collation':p159,'source_only_crosscopy_family':source_family,'joint_footer_witnesses':joint,
            'prior_credit':data['prior_credit'],'limits':data['limits']}, evidence


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--pdf',type=Path)
    args=parser.parse_args()
    result,evidence=build(args.pdf)
    path=HERE/'certificates.json'
    if args.verify:
        assert result==load(path)
    else:
        path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':args.verify,**result['summary'],'source_evidence':evidence['summary']},indent=2))
