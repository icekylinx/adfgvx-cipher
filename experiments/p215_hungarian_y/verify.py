#!/usr/bin/env python3
"""Optional shared DD=Y constraint and original p215 closing witnesses.

icekylinx and GPT-6 Astra Pro. No baseline key or source value is changed.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains
from adfgvx.source_evidence import verify_source_evidence
CO = 'ADFGVX'
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def inspect(cipher, ranks, square, mapping):
    n, width = len(cipher), len(ranks)
    assert n % 2 == 0 and len(mapping) == n
    heights = [n // width + (c < n % width) for c in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[c])
              for c in range(width)]
    indices = [starts[p % width] + p // width for p in range(n)]
    assert sorted(indices) == list(range(n))
    unused = set(AL) - set(square)
    positions = []
    for i in range(n // 2):
        model_indices = indices[2*i:2*i+2]
        pair = ''.join(cipher[j] for j in model_indices)
        values = set()
        for row in range(6):
            for col in range(6):
                if pair[0] in ('?', CO[row]) and pair[1] in ('?', CO[col]):
                    value = square[6*row+col]
                    values.update(unused if value == '?' else value)
        domain = ''.join(sorted(values))
        positions.append({'plaintext_index': i, 'pair': pair,
                          'model_indices': model_indices,
                          'source_indices': [mapping[j] for j in model_indices],
                          'domain': domain})
    raw = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in positions)
    assert raw == decrypt(cipher, ranks, square)
    assert [p['domain'] for p in positions] == plaintext_domains(cipher, ranks, square)
    return raw, positions


def partial(base, ambiguous, assignments):
    result = ['?' if c in ambiguous else c for c in base]
    for old, new in assignments.items():
        assert old in ambiguous and new in AL and new not in result
        result[base.index(old)] = new
    result = ''.join(result)
    assert len(set(result) - {'?'}) == 36 - result.count('?')
    return result


def complete(square, overrides=None):
    result = list(square)
    for index, value in (overrides or {}).items():
        assert result[index] == '?' and value not in result
        result[index] = value
    unused = iter(sorted(set(AL) - set(result)))
    result = ''.join(next(unused) if c == '?' else c for c in result)
    assert set(result) == set(AL) and len(result) == 36
    return result


def witness(cipher, ranks, square):
    filled = cipher.replace('?', 'A')
    text = decrypt(filled, ranks, square)
    assert encrypt(text, ranks, square) == filled
    assert all(a == '?' or a == b for a, b in zip(cipher, filled))
    return {'square': square, 'filled_ciphertext': filled, 'plaintext': text,
            'is_proposed_historical_reading': False}


def price(source, edited):
    assert len(source) == len(edited)
    substitutions, fills = [], []
    for i, (old, new) in enumerate(zip(source, edited)):
        if old == new:
            continue
        event = {'source_index': i, 'before': old, 'after': new}
        (fills if old == '?' else substitutions).append(event)
    return {'observed_substitutions': substitutions, 'source_mask_fills': fills,
            'observed_substitution_count': len(substitutions), 'mask_fill_count': len(fills)}


def normalize_place(text):
    text = text.upper().replace('Ö', 'OE').replace('Ő', 'OE').replace('Ü', 'UE').replace('Ű', 'UE')
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if 'A' <= c <= 'Z')


def build():
    inputs = load(HERE / 'inputs.json')
    for name, expected in inputs['dependency_sha256'].items():
        assert sha(ROOT / name) == expected, name
    assert sha(HERE / 'known_body_inventory.json') == inputs['known_inventory_sha256']
    key = inputs['key']
    current = next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == key['id'])
    for name in ('coordinate_order', 'column_rank_order', 'square'):
        assert current[name] == key[name]
    base, ranks = key['square'], key['column_rank_order']
    numeric = inputs['prior_numeric_assignments']
    definitions = {'prior_numeric_only': dict(numeric),
                   'prior_numeric_plus_J': dict(numeric, **{'9': 'J'}),
                   'prior_numeric_plus_Y': dict(numeric, **{'4': 'Y'}),
                   'prior_numeric_plus_J_and_Y': dict(numeric, **{'9': 'J', '4': 'Y'})}
    squares = {name: partial(base, inputs['ambiguous_baseline_labels'], assignments)
               for name, assignments in definitions.items()}
    results, occurrences, physical = [], [], set()
    for record in inputs['records']:
        cipher, mapping = record['ciphertext'], record['model_to_source_indices']
        raw, positions = inspect(cipher, ranks, base, mapping)
        assert raw == record['expected_baseline'], (record['physical_record'], record['variant'])
        interpretations = {}
        for name, square in squares.items():
            text, projected = inspect(cipher, ranks, square, mapping)
            win = witness(cipher, ranks, complete(square))
            assert all(c in p['domain'] for c, p in zip(win['plaintext'], projected))
            interpretations[name] = {'square': square, 'conditional_plaintext': text,
                                     'fixed_positions': sum(c != '?' for c in text),
                                     'witness': win}
        if record['is_primary_raw']:
            assert record['physical_record'] not in physical
            physical.add(record['physical_record'])
            for p in positions:
                if raw[p['plaintext_index']] == '4':
                    assert p['pair'] == 'DD' and None not in p['source_indices']
                    occurrences.append(dict(physical_record=record['physical_record'], **p,
                        baseline_context=raw[max(0,p['plaintext_index']-12):p['plaintext_index']+13]))
        results.append({'physical_record': record['physical_record'], 'variant': record['variant'],
                        'is_primary_raw': record['is_primary_raw'], 'baseline_plaintext': raw,
                        'interpretations': interpretations})
    assert len(physical) == 26
    inventory = load(HERE / 'known_body_inventory.json')
    assert len(inventory['bodies']) == 25
    assert {r['id'] for r in inventory['bodies']} == physical - {'p215'}
    for item in inventory['bodies']:
        primary = next(r for r in results if r['physical_record'] == item['id'] and r['is_primary_raw'])
        assert primary['baseline_plaintext'] in [v['raw'] for v in item['variants']]
    assert len(occurrences) == 9
    assert {p['physical_record'] for p in occurrences} == {'p213_A2','p215_B2','p217_A3','p215'}
    support = {}
    for rid, expected_positions in [('p217_A3',[57]), ('p215_B2',[105,112])]:
        source = next(r for r in inputs['records'] if r['physical_record'] == rid and r['is_primary_raw'])
        raw, pos = inspect(source['ciphertext'], ranks, base, source['model_to_source_indices'])
        links = [pos[i] for i in expected_positions]
        assert all(p['pair'] == 'DD' and None not in p['source_indices'] for p in links)
        support[rid] = links
    assert support['p217_A3'][0]['source_indices'] == [139,222]
    assert [p['source_indices'] for p in support['p215_B2']] == [[268,23],[187,296]]
    primary217 = next(r for r in results if r['physical_record'] == 'p217_A3' and r['is_primary_raw'])
    assert primary217['interpretations']['prior_numeric_plus_J_and_Y']['conditional_plaintext'][52:60] == 'POESTYEN'
    b2primary = next(r for r in results if r['physical_record'] == 'p215_B2' and r['variant'] == 'inherited_13_mask_fill_primary')
    b2text = b2primary['interpretations']['prior_numeric_plus_J_and_Y']['conditional_plaintext']
    assert 'NAGYBANHEGYES' in b2text
    assert all(value in b2text for value in ['VASARHE1Y','VASARTELY','BATTREYA'])
    reval = next(r for r in results if r['physical_record'] == 'p213_A2' and r['is_primary_raw'])
    assert 'BACYLON' in reval['interpretations']['prior_numeric_plus_J_and_Y']['conditional_plaintext']
    target = next(r for r in inputs['records'] if r['physical_record'] == 'p215' and r['is_primary_raw'])
    assert len(target['ciphertext']) == 258 and target['ciphertext'].count('?') == 21
    footer = {}
    old90 = load(ROOT/'experiments/late_key_interpretation/certificate.json')['p215_footer']['possible_values']
    for name, square in squares.items():
        text, pos = inspect(target['ciphertext'], ranks, square, target['model_to_source_indices'])
        tail = pos[-4:]
        assert [p['pair'] for p in tail] == ['FD','FA','XD','AV']
        assert tail[1]['domain'] == '1' and tail[3]['domain'] == '6'
        assert tail[0]['domain'] == tail[2]['domain']
        allowed = tail[0]['domain']
        values, witnesses = [], []
        for a,b in itertools.permutations(allowed,2):
            fullkey = complete(square, {base.index('3'):a, base.index('5'):b})
            win = witness(target['ciphertext'], ranks, fullkey)
            value = a+'1'+b+'6'
            assert win['plaintext'][-4:] == value
            # A single global square must also preserve every certified source model.
            checks = []
            for record in inputs['records']:
                w = witness(record['ciphertext'], ranks, fullkey)
                checks.append(hashlib.sha256((record['physical_record']+'\n'+record['variant']+'\n'+w['plaintext']).encode()).hexdigest())
            win['global_cohort_plaintext_digest'] = hashlib.sha256(('\n'.join(checks)+'\n').encode()).hexdigest()
            values.append(value);witnesses.append(win)
        assert values == sorted(values)
        footer[name] = {'pattern':'a1b6','a_and_b_domain':allowed,'distinct_a_and_b':True,
                        'count':len(values),'possible_values':values,
                        'all_numeric_values':[v for v in values if v.isdigit()],
                        'source_positions':tail,'witnesses':witnesses}
        assert len(footer[name]['all_numeric_values']) == 42
    assert footer['prior_numeric_only']['possible_values'] == old90
    assert [footer[n]['count'] for n in definitions] == [90,72,72,56]
    joint = footer['prior_numeric_plus_J_and_Y']['possible_values']
    assert set(joint) == set(footer['prior_numeric_plus_J']['possible_values']) & set(footer['prior_numeric_plus_Y']['possible_values'])
    assert all('J' not in v and 'Y' not in v for v in joint)
    geo = inputs['geography_comparison']
    frozen_b2 = next(r for r in load(ROOT/'experiments/southern_hungary_positions_part2/certificates.json')['records']
                     if r['id'] == 'p215_B2')
    frozen_geo = frozen_b2['geographical_alternative']
    assert geo['original_source_ciphertext'] == frozen_b2['ciphertext']
    assert geo['original_baseline_geographical_template'] == frozen_geo['template']
    assert geo['original_baseline_geographical_ciphertext'] == frozen_geo['ciphertext']
    old_geo, old_geo_positions = inspect(frozen_geo['ciphertext'], ranks, base, list(range(300)))
    assert old_geo == frozen_geo['template']
    y_positions = geo['Y_plaintext_positions']
    assert y_positions == [36,75,105,112,122]
    expected_cipher = list(frozen_geo['ciphertext'])
    original_b2, original_b2_positions = inspect(frozen_b2['ciphertext'], ranks, base, list(range(300)))
    for index in y_positions:
        assert old_geo[index] == 'Y' and original_b2[index] == '4'
        assert original_b2_positions[index]['pair'] == 'DD'
        for model_index in original_b2_positions[index]['model_indices']:
            expected_cipher[model_index] = 'D'
    assert ''.join(expected_cipher) == geo['new_shared_Y_ciphertext']
    new_geo, new_geo_positions = inspect(geo['new_shared_Y_ciphertext'], ranks,
                                         squares['prior_numeric_plus_J_and_Y'], list(range(300)))
    expected_letters = []
    for index, value in enumerate(old_geo):
        expected_letters.append('Y' if index in y_positions else '?' if value == '?' else
                                squares['prior_numeric_plus_J_and_Y'][base.index(value)])
    assert new_geo == ''.join(expected_letters)
    assert old_geo[1] == 'Y' and new_geo[1] == '1'
    assert all(new_geo_positions[index]['pair'] == 'DD' and new_geo[index] == 'Y'
               for index in y_positions)
    for word in ['HODMEZOEXVASARHELY','OROSHAZA','NAGYBANHEGYES','BATTONYA','MEZOEKOVACSHAZA']:
        assert word in new_geo
    full_geo_witness = witness(geo['new_shared_Y_ciphertext'], ranks,
                               complete(squares['prior_numeric_plus_J_and_Y']))
    assert all(letter == '?' or letter == value for letter, value in
               zip(new_geo, full_geo_witness['plaintext']))
    before = price(geo['original_source_ciphertext'],geo['original_baseline_geographical_ciphertext'])
    after = price(geo['original_source_ciphertext'],geo['new_shared_Y_ciphertext'])
    assert (before['observed_substitution_count'],before['mask_fill_count']) == (18,14)
    assert (after['observed_substitution_count'],after['mask_fill_count']) == (8,14)
    assert before['source_mask_fills'] == after['source_mask_fills']
    assert all(event in before['observed_substitutions'] for event in after['observed_substitutions'])
    # No unpriced identity normalization: these five Y cells only revert to observed DD.
    reverted = [i for i,(a,b) in enumerate(zip(geo['original_baseline_geographical_ciphertext'],geo['new_shared_Y_ciphertext'])) if a!=b]
    assert len(reverted) == 10 and all(geo['original_source_ciphertext'][i] == geo['new_shared_Y_ciphertext'][i] for i in reverted)
    return {'schema':'adfgvx-p215-shared-hungarian-y-certificate-v1','authors':inputs['authors'],
            'inputs_sha256':sha(HERE/'inputs.json'),'conditional_squares':squares,
            'summary':{'certified_physical_bodies':26,'other_body_inventory':25,
                       'source_and_editorial_variants':len(results),'primary_observed_DD_positions':9,
                       'new_observed_coordinate_edits_for_key_interpretation':0,
                       'baseline_key_changed':False,'original_p215_unknown_coordinates':21,
                       'footer_stage_counts':[90,72,72,56],'all_numeric_count_each_stage':42},
            'source_cell_support':support,'all_primary_raw_4_occurrences':occurrences,
            'records':results,'p215_footer':footer,
            'adverse_fields':{'p215_B2_inherited_primary_under_joint':b2text,
               'p213_A2_under_joint':reval['interpretations']['prior_numeric_plus_J_and_Y']['conditional_plaintext'],
               'inherited_J_adverse_name':'NIKOLA3EW in p216 A2 is not silently changed to NIKOLAJEW; FD cannot also be J when GD is J.'},
            'optional_geography_repricing':{'before':before,'after':after,
                'old_baseline_template':old_geo,'new_joint_conditional_plaintext':new_geo,
                'new_geographical_Y_positions':[new_geo_positions[i] for i in y_positions],
                'global_key_witness':full_geo_witness,
                'reverted_to_original_DD_source_indices':reverted},
            'limits':inputs['limits']}


def verify_markdown(certificate):
    import re
    text=(HERE/'README.md').read_text()
    fences=re.findall(r'```text\n(.*?)\n```',text,re.S)
    target=next(r for r in certificate['records'] if r['physical_record']=='p215' and r['is_primary_raw'])
    expected=[target['baseline_plaintext'],target['interpretations']['prior_numeric_plus_J_and_Y']['conditional_plaintext']]
    assert fences == expected, 'README raw/conditional text differs from the exact certificate'
    for n in ['90','72','56','42','8','14']:
        assert n in text
    assert 'not a recovered serial number' in text


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify',action='store_true')
    p.add_argument('--write',action='store_true')
    p.add_argument('--pdf',type=Path)
    p.add_argument('--directory-1913-pdf',type=Path)
    p.add_argument('--yearbook-pdf',type=Path)
    args=p.parse_args()
    certificate=build()
    if args.write:
        (HERE/'certificates.json').write_text(json.dumps(certificate,indent=2)+'\n')
    else:
        assert load(HERE/'certificates.json') == certificate
    inputs=load(HERE/'inputs.json')
    source_report=verify_source_evidence(args.pdf,inputs['source'],inputs['source_images'],HERE)
    references=[]
    for ref,provided in zip(inputs['primary_place_references'],[args.directory_1913_pdf,args.yearbook_pdf]):
        report=verify_source_evidence(provided,ref,[ref['source_image']],HERE)
        if provided:
            import fitz
            with fitz.open(provided) as d:
                text=d[ref['pdf_page_1based']-1].get_text()
                assert ref['short_quote'] in text
                assert normalize_place(ref['short_quote'].split('(')[0]) == ref['cipher_spelling_for_comparison']
        references.append({'reference':ref['id'],'checks':report['summary']})
    if args.verify:
        verify_markdown(certificate)
    print(json.dumps({'verified':True,**certificate['summary'],'source_evidence':source_report['summary'],
                      'primary_references':references},indent=2))


if __name__=='__main__':
    main()
