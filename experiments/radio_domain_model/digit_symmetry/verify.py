#!/usr/bin/env python3
"""Certify digit-permutation orbits of eight fixed recorded control candidates.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Standard library only. No model, partial square, search row or ledger is changed.
"""
from __future__ import annotations

import argparse
from array import array
import hashlib
from itertools import permutations
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
DIGITS = '0123456789'
COORDS = 'ADFGVX'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value):
    return hashlib.sha256(value.encode('ascii')).hexdigest()


def classes(text):
    return ''.join('#' if c in DIGITS else c for c in text)


def encrypt(plaintext, ranks, square):
    """Independent rowwise fractionation followed by ranked column readout."""
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert sorted(ranks) == list(range(1, len(ranks)+1))
    lookup = {symbol: COORDS[i//6]+COORDS[i%6] for i, symbol in enumerate(square)}
    middle = ''.join(lookup[c] for c in plaintext)
    return ''.join(middle[col::len(ranks)] for col in sorted(range(len(ranks)), key=ranks.__getitem__))


def decrypt(cipher, ranks, square):
    width = len(ranks)
    heights = [len(cipher)//width + (i < len(cipher)%width) for i in range(width)]
    columns = [None]*width
    offset = 0
    for column in sorted(range(width), key=ranks.__getitem__):
        columns[column] = cipher[offset:offset+heights[column]]
        offset += heights[column]
    assert offset == len(cipher)
    middle = ''.join(columns[i%width][i//width] for i in range(len(cipher)))
    assert len(middle)%2 == 0
    return ''.join(square[6*COORDS.index(middle[i])+COORDS.index(middle[i+1])]
                   for i in range(0, len(middle), 2))


def check_witness(candidate, control):
    partial, ranks = control['partial_square'], control['column_rank_order']
    square, plaintext = candidate['square'], candidate['plaintext']
    loss, fill = candidate['loss'], candidate['fill']
    assert len(partial) == len(square) == 36
    assert len(set(partial.replace('?', ''))) == len(partial.replace('?', ''))
    assert all(a == '?' or a == b for a, b in zip(partial, square))
    assert loss == sorted(set(loss)) and len(loss) == len(fill) == 5
    full = encrypt(plaintext, ranks, square)
    assert len(full) == 170 and len(plaintext) == 85
    assert decrypt(full, ranks, square) == plaintext
    assert ''.join(full[i] for i in loss) == fill
    assert ''.join(c for i, c in enumerate(full) if i not in loss) == control['received_ciphertext']
    return full


def permute_text(text, mapping):
    return ''.join(mapping.get(c, c) for c in text)


def transformed(candidate, mapping):
    return {**candidate,
            'square': permute_text(candidate['square'], mapping),
            'plaintext': permute_text(candidate['plaintext'], mapping)}


def truth_orbit(candidate_text, truth, unused):
    """A literal target is in the orbit iff a partial bijection on U exists."""
    forward, backward, conflicts = {}, {}, []
    for i, (a, b) in enumerate(zip(candidate_text, truth)):
        if a not in unused:
            if a != b:
                conflicts.append({'kind':'fixed_symbol_mismatch', 'position':i,
                                  'candidate':a, 'truth':b})
            continue
        if b not in unused:
            conflicts.append({'kind':'target_not_permutable', 'position':i,
                              'candidate':a, 'truth':b})
            continue
        if a in forward and forward[a][0] != b:
            prior_b, prior_i = forward[a]
            conflicts.append({'kind':'same_candidate_digit_different_truth_digits',
                              'candidate_digit':a, 'positions':[prior_i, i],
                              'truth_digits':[prior_b, b]})
        else:
            forward.setdefault(a, (b, i))
        if b in backward and backward[b][0] != a:
            prior_a, prior_i = backward[b]
            conflicts.append({'kind':'different_candidate_digits_same_truth_digit',
                              'truth_digit':b, 'positions':[prior_i, i],
                              'candidate_digits':[prior_a, a]})
        else:
            backward.setdefault(b, (a, i))
    same_class = classes(candidate_text) == classes(truth)
    compatible = not conflicts
    result = {'same_digit_class_text_as_truth':same_class,
              'truth_in_fixed_candidate_plaintext_orbit':compatible,
              'literal_matches':sum(a == b for a,b in zip(candidate_text, truth)),
              'class_matches':sum(a == b for a,b in zip(classes(candidate_text), classes(truth))),
              'length':len(truth),
              'all_compatibility_conflicts':conflicts}
    if compatible:
        used = {a:v[0] for a,v in forward.items()}
        remaining_sources = sorted(set(unused)-set(used))
        remaining_targets = sorted(set(unused)-set(used.values()))
        extension = {**used, **dict(zip(remaining_sources, remaining_targets))}
        assert permute_text(candidate_text, extension) == truth
        result.update({'required_used_digit_map':used,
                       'example_full_digit_permutation':extension,
                       'full_digit_permutations_yielding_truth':math.factorial(len(remaining_sources))})
    elif same_class:
        equality = [c for c in conflicts if c['kind']=='same_candidate_digit_different_truth_digits']
        result['explicit_equality_conflict'] = equality[0] if equality else conflicts[0]
    return result


def orbit_certificate(row, control, enumerate_limit):
    candidate = row['best_candidate']
    assert candidate['word_weight'] == candidate['word_sum'] == 0
    assert candidate['score'] == candidate['quad_sum']
    full = check_witness(candidate, control)
    assert check_witness(row['final_event'], control) == full
    assert row['truth_seeded'] is False
    unused = ''.join(d for d in DIGITS if d not in control['partial_square'])
    present = ''.join(d for d in unused if d in candidate['plaintext'])
    k, r = len(unused), len(present)
    square_count = math.factorial(k)
    stabilizer_count = math.factorial(k-r)
    plaintext_count = square_count//stabilizer_count
    assert all(control['partial_square'][candidate['square'].index(d)] == '?' for d in unused)
    base_class = classes(candidate['plaintext'])
    generators = []
    for a,b in zip(unused, unused[1:]):
        changed = transformed(candidate, {a:b,b:a})
        assert check_witness(changed, control) == full
        assert classes(changed['plaintext']) == base_class
        assert changed['loss'] == candidate['loss'] and changed['fill'] == candidate['fill']
        generators.append({'swap':[a,b], 'square':changed['square'],
                           'plaintext':changed['plaintext'], 'ciphertext_unchanged':True,
                           'loss_and_fill_unchanged':True, 'class_text_unchanged':True})
    assert len(generators) == max(0,k-1)
    proof_checks = {'adjacent_transposition_generators_checked':len(generators),
                    'all_generators':generators}
    if k <= enumerate_limit:
        seen_squares, seen_plaintexts = set(), set()
        orbit_hash = hashlib.sha256()
        total = 0
        for permutation in permutations(unused):
            mapping = dict(zip(unused, permutation))
            changed = transformed(candidate, mapping)
            assert check_witness(changed, control) == full
            assert classes(changed['plaintext']) == base_class
            seen_squares.add(changed['square'])
            seen_plaintexts.add(changed['plaintext'])
            orbit_hash.update((changed['square']+'\n'+changed['plaintext']+'\n').encode('ascii'))
            total += 1
        assert total == len(seen_squares) == square_count
        assert len(seen_plaintexts) == plaintext_count
        proof_checks['full_enumeration'] = {'performed':True, 'permutations_checked':total,
                                            'distinct_complete_squares':len(seen_squares),
                                            'distinct_literal_plaintexts':len(seen_plaintexts),
                                            'lexicographic_permutation_stream_sha256':orbit_hash.hexdigest()}
    else:
        proof_checks['full_enumeration'] = {'performed':False, 'permutations_checked':0,
                                            'reason':'The exact count follows from the free square action and plaintext stabilizer; only a generating set is explicitly checked.'}
    comparison = truth_orbit(candidate['plaintext'], control['truth'], unused)
    assert comparison['literal_matches'] == row['correct_characters']
    assert comparison['class_matches'] == row['digit_class_accuracy']
    assert not row['exact_plaintext']
    if comparison['truth_in_fixed_candidate_plaintext_orbit']:
        truth_variant = transformed(candidate, comparison['example_full_digit_permutation'])
        assert check_witness(truth_variant, control) == full
        comparison['example_truth_square_in_this_orbit'] = truth_variant['square']
        comparison['example_truth_square_equals_original_truth_square'] = truth_variant['square'] == control['square']
    return {'result_id':row['id'], 'control_id':row['control_id'], 'model':row['model'],
            'fixed_column_rank_order':control['column_rank_order'],
            'fixed_loss_positions':candidate['loss'], 'fixed_coordinate_fill':candidate['fill'],
            'base_square':candidate['square'], 'base_plaintext':candidate['plaintext'],
            'complete_ciphertext':full, 'complete_ciphertext_sha256':text_sha(full),
            'received_ciphertext_sha256':text_sha(control['received_ciphertext']),
            'anchored_digits':''.join(d for d in DIGITS if d in control['partial_square']),
            'permutable_unanchored_digits':unused, 'k':k,
            'permutable_digits_occurring_in_candidate_plaintext':present, 'r':r,
            'distinct_complete_squares_in_this_digit_orbit':square_count,
            'plaintext_stabilizer_permutations':stabilizer_count,
            'distinct_literal_plaintexts_in_this_digit_orbit':plaintext_count,
            'fixed_digit_class_plaintext':base_class,
            'proof_checks':proof_checks, 'truth_comparison':comparison}


def build():
    inputs = json.loads((HERE/'inputs.json').read_text())
    assert inputs['authors'] == 'icekylinx and GPT-6 Astra Pro'
    for item in inputs['source_files']:
        assert sha(HERE/item['path']) == item['sha256']
    original_data = json.loads((HERE/'../numeric_dataset.json').read_text())
    original_report = json.loads((HERE/'../numeric_loss_controls.json').read_text())
    assert inputs['controls'] == original_data['controls']
    assert inputs['rows'] == [r for r in original_report['results'] if r['model'] in inputs['model_files']]
    assert len(inputs['controls']) == 4 and len(inputs['rows']) == 8
    assert original_report['dataset_sha256'] == sha(HERE/'../numeric_dataset.json')
    assert original_report['word_weight'] == 0 and original_report['truth_used_as_seed'] is False
    for name, info in inputs['model_files'].items():
        assert info['sha256'] == original_report['model_sha256'][name]
    assert inputs['enumerate_all_permutations_when_k_at_most'] == 6
    controls = {c['id']:c for c in inputs['controls']}
    for c in controls.values():
        truth = {'square':c['square'], 'plaintext':c['truth'], 'loss':c['loss_positions'], 'fill':c['fill']}
        assert check_witness(truth, c) == c['full_ciphertext']
        assert classes(c['truth']) == c['truth_classes']
    rows = [orbit_certificate(row, controls[row['control_id']], 6) for row in inputs['rows']]
    expected = [(10,9,3628800,3628800),(10,9,3628800,3628800),
                (6,4,720,360),(6,5,720,720),(5,4,120,120),(5,4,120,120),(2,2,2,2),(2,2,2,2)]
    assert [(r['k'],r['r'],r['distinct_complete_squares_in_this_digit_orbit'],
             r['distinct_literal_plaintexts_in_this_digit_orbit']) for r in rows] == expected
    perfect_class = [r for r in rows if r['truth_comparison']['same_digit_class_text_as_truth']]
    assert len(perfect_class) == 3
    assert [r['truth_comparison']['truth_in_fixed_candidate_plaintext_orbit'] for r in perfect_class] == [False, False, True]
    assert sum(r['proof_checks']['full_enumeration']['permutations_checked'] for r in rows) == 1684
    assert sum(r['proof_checks']['adjacent_transposition_generators_checked'] for r in rows) == 38
    return {'schema':'adfgvx-fixed-candidate-digit-symmetry-certificate-v1',
            'authors':inputs['authors'], 'input_sha256':sha(HERE/'inputs.json'),
            'indexing':'All positions are zero-based.',
            'counting_scope':'Exact orbit of each frozen candidate under permutations of unanchored digits; other possible letter placements or loss frames are outside this count.',
            'theorem':{'square_orbit':'k!', 'literal_plaintext_orbit':'k!/(k-r)!',
                       'plaintext_stabilizer':'(k-r)!',
                       'ciphertext':'Joint label permutation preserves each coordinate pair, hence full transposed ciphertext, loss projection and coordinate fill.',
                       'objective':'Each digit maps to the same class; any objective factoring through this class string is unchanged. The recorded objectives have word_weight=0.'},
            'summary':{'recorded_candidates':8,'truth_class_exact_but_literal_wrong':3,
                       'class_exact_rows_with_truth_in_fixed_plaintext_orbit':1,
                       'class_exact_rows_with_digit_equality_conflicts':2,
                       'fully_enumerated_rows':6,'total_small_orbit_permutations_checked':1684,
                       'generator_checks_across_all_rows':38,
                       'ten_factorial_orbits_fully_enumerated':0,
                       'historical_digit_assignments':0},
            'rows':rows,
            'limits':['Counts are exact per recorded candidate orbit, not totals over every possible full-square completion or loss geometry.',
                      'The eight rows are separate optimization outcomes; their orbit sizes must not be added as if their unions were disjoint.',
                      'An 85/85 class match need not preserve the true digit-equality pattern; the two CHI rows demonstrate this explicitly.',
                      'These invented controls establish an identifiability limit of the declared objective, not any historical numerical value.']}


def binary_checks(model_directory, result):
    """Check all 36^4 adapter entries, then candidate/generator score invariance."""
    inputs = json.loads((HERE/'inputs.json').read_text())
    tables, reports = {}, []
    for model, info in inputs['model_files'].items():
        path = model_directory/info['filename']
        assert sha(path) == info['sha256']
        raw = path.read_bytes()
        assert len(raw) == 4*36**4
        bits, values = array('I'), array('f')
        assert bits.itemsize == values.itemsize == 4
        bits.frombytes(raw); values.frombytes(raw)
        if sys.byteorder != 'little':
            bits.byteswap(); values.byteswap()
        assert all(math.isfinite(value) for value in values)
        checked = 0
        for a in range(36):
            for b in range(36):
                for c in range(36):
                    prefix = ((a*36+b)*36+c)*36
                    representative = ((min(a,26)*36+min(b,26))*36+min(c,26))*36
                    for d in range(36):
                        assert bits[prefix+d] == bits[representative+min(d,26)]
                        checked += 1
        assert checked == 36**4
        tables[model] = values
        reports.append({'model':model,'filename':info['filename'],'sha256':info['sha256'],
                        'exact_bitwise_adapter_entries_checked':checked,
                        'collapsed_classes':27,'all_entries_factor_through_digit_class':True})
    def score(text, table):
        values = [ALPHABET.index(c) for c in text]
        return sum(table[((a*36+b)*36+c)*36+d]
                   for a,b,c,d in zip(values,values[1:],values[2:],values[3:]))
    row_scores = []
    original = {r['id']:r for r in inputs['rows']}
    controls = {c['id']:c for c in inputs['controls']}
    for row in result['rows']:
        table = tables[row['model']]
        value = score(row['base_plaintext'], table)
        assert abs(value-original[row['result_id']]['best_candidate']['score']) < 1e-6
        truth_value = score(controls[row['control_id']]['truth'], table)
        assert abs(truth_value-original[row['result_id']]['truth_score']) < 1e-6
        for witness in row['proof_checks']['all_generators']:
            assert score(witness['plaintext'], table) == value
        if row['truth_comparison']['same_digit_class_text_as_truth']:
            assert truth_value == value
        row_scores.append({'result_id':row['result_id'],'exact_candidate_score':value,
                           'exact_truth_score':truth_value,
                           'generator_scores_exactly_equal':True})
    return {'schema':'adfgvx-digit-class-adapter-check-v1',
            'authors':'icekylinx and GPT-6 Astra Pro',
            'certificate_sha256':sha(HERE/'certificate.json'),
            'model_checks':reports,'row_scores':row_scores,
            'total_adapter_entries_checked':2*36**4,
            'total_generator_score_checks':38}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='Write the frozen derived certificate; otherwise verify it.')
    parser.add_argument('--models',type=Path,help='Optional directory of the unchanged class binary lookup tables.')
    args = parser.parse_args()
    result = build()
    target = HERE/'certificate.json'
    if args.write:
        target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    else:
        assert result == json.loads(target.read_text())
    binary = None
    if args.models:
        binary = binary_checks(args.models,result)
        path = HERE/'binary_table_check.json'
        if args.write:
            path.write_text(json.dumps(binary,indent=2,ensure_ascii=False)+'\n')
        else:
            assert binary == json.loads(path.read_text())
    print(json.dumps({'verified':not args.write,**result['summary'],
                      'binary_adapter_entries_checked_this_run':binary['total_adapter_entries_checked'] if binary else 0},indent=2))


if __name__ == '__main__':
    main()
