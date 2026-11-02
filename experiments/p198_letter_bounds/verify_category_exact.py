#!/usr/bin/env python3
"""Independently recompute the p198 common-24 optimum by column-pair DPs.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Standard library only. No repository cipher functions, C++ engine, language
model, or recorded optimum is used to choose a score. The published result
is compared with the independently recomputed bound and explicit witnesses.
"""
from pathlib import Path
from functools import lru_cache
import argparse
import hashlib
import itertools
import json
import math
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
CATEGORY = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set('QY')
DEFAULT_OUTPUT = ROOT / 'data/reviews/p198_category_bounds_independent.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def encrypt(plaintext, ranks, square):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert sorted(ranks) == list(range(1, len(ranks)+1))
    stream = ''.join(COORDS[square.index(ch)//6]+COORDS[square.index(ch)%6] for ch in plaintext)
    return ''.join(stream[col::len(ranks)] for col in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def decode(ciphertext, ranks, square):
    assert len(ciphertext) % 2 == 0
    assert sorted(ranks) == list(range(1, len(ranks)+1))
    stream = [''] * len(ciphertext)
    at = 0
    for col in sorted(range(len(ranks)), key=lambda c: ranks[c]):
        for position in range(col, len(ciphertext), len(ranks)):
            stream[position] = ciphertext[at]
            at += 1
    return ''.join(square[6*COORDS.index(a)+COORDS.index(b)] for a, b in zip(stream[::2], stream[1::2]))


def fill_frame(source, losses, values):
    assert list(losses) == sorted(set(losses)) and len(losses) == len(values)
    assert set(values) <= set(COORDS)
    assert all(0 <= position < len(source)+len(losses) for position in losses)
    observed, inserted = iter(source), iter(values)
    return ''.join(next(inserted) if i in losses else next(observed) for i in range(len(source)+len(losses)))


def compositions(total, width, prefix=()):
    """All per-physical-column loss counts; invalid short columns are filtered."""
    if width == 1:
        yield prefix+(total,)
        return
    for value in range(total+1):
        yield from compositions(total-value, width-1, prefix+(value,))


def maximum_count(source, ranks, missing, cell_mask):
    """Exact additive maximum via independent adjacent physical column pairs.

    Once a loss allocation fixes each received column segment, its physical
    column pair has no interaction with the other pairs for this objective.
    Each local DP state is (row, left losses used, right losses used). It
    consumes each segment in order and considers every missing/present pair.
    Missing values can be maximized locally because they affect no other
    plaintext position. Summing the independent pair optima is therefore
    exact for this allocation. The outer loop covers every allocation.
    """
    nominal = len(source)+missing
    width = len(ranks)
    assert nominal % 2 == width % 2 == 0
    assert len(cell_mask) == 36 and set(cell_mask) <= {0, 1}
    assert sorted(ranks) == list(range(1, width+1))
    heights = [nominal//width+(col < nominal % width) for col in range(width)]
    assert all(heights[col] == heights[col+1] for col in range(0, width, 2))
    readout = sorted(range(width), key=lambda c: ranks[c])
    local_value = {}
    for left in range(7):
        for right in range(7):
            local_value[left, right] = max(
                cell_mask[6*a+b]
                for a in (range(6) if left == 6 else [left])
                for b in (range(6) if right == 6 else [right]))

    @lru_cache(None)
    def pair_best(left, right, height):
        left_losses = height-len(left)
        right_losses = height-len(right)
        layer = {(0, 0): 0}
        for row in range(height):
            following = {}
            for (left_used, right_used), value in layer.items():
                left_choices = []
                right_choices = []
                if row-left_used < len(left):
                    left_choices.append((left_used, left[row-left_used]))
                if left_used < left_losses:
                    left_choices.append((left_used+1, 6))
                if row-right_used < len(right):
                    right_choices.append((right_used, right[row-right_used]))
                if right_used < right_losses:
                    right_choices.append((right_used+1, 6))
                for next_left, left_symbol in left_choices:
                    for next_right, right_symbol in right_choices:
                        score = value+local_value[left_symbol, right_symbol]
                        state = (next_left, next_right)
                        if score > following.get(state, -1):
                            following[state] = score
            layer = following
        return layer[left_losses, right_losses]

    observed = tuple(COORDS.index(ch) for ch in source)
    best, tested, winning_allocations = -1, 0, 0
    for allocation in compositions(missing, width):
        if any(loss > height for loss, height in zip(allocation, heights)):
            continue
        segments = [None] * width
        at = 0
        for col in readout:
            length = heights[col]-allocation[col]
            segments[col] = observed[at:at+length]
            at += length
        assert at == len(source)
        value = sum(pair_best(segments[col], segments[col+1], heights[col]) for col in range(0, width, 2))
        if value > best:
            best, winning_allocations = value, 1
        elif value == best:
            winning_allocations += 1
        tested += 1
    cache = pair_best.cache_info()
    return dict(maximum_category_count=best, column_allocations=tested,
                maximizing_column_allocations=winning_allocations,
                pair_subproblems_solved=cache.misses, pair_cache_hits=cache.hits)


def witness(case, square, result):
    losses = result['missing_full_ciphertext_positions']
    values = result['filled_missing_coordinates']
    assert len(losses) == case['missing_count']
    full = fill_frame(case['observed_ciphertext'], losses, values)
    plaintext = decode(full, case['column_rank_order'], square)
    counts = dict(common24=sum(ch in CATEGORY for ch in plaintext),
                  Q=plaintext.count('Q'), Y=plaintext.count('Y'),
                  digits=sum(ch in '0123456789' for ch in plaintext))
    assert sum(counts.values()) == len(plaintext)
    assert counts['common24'] == result['target_category_count']
    assert encrypt(plaintext, case['column_rank_order'], square) == full
    assert ''.join(ch for i, ch in enumerate(full) if i not in losses) == case['observed_ciphertext']
    return dict(square=square, losses=losses, fill=values, plaintext=plaintext,
                counts=counts, retained_source_coordinates=len(case['observed_ciphertext']),
                reencryption_verified=True)


def small_controls(records):
    reports = []
    for record in records:
        case, square = record['case'], record['square']
        source, ranks, missing = case['observed_ciphertext'], case['column_rank_order'], case['missing_count']
        nominal = len(source)+missing
        mask = [int(ch in CATEGORY) for ch in square]
        maximum = maximum_count(source, ranks, missing, mask)
        complement = maximum_count(source, ranks, missing, [1-value for value in mask])
        bounds = {True: maximum['maximum_category_count'], False: nominal//2-complement['maximum_category_count']}
        best = {False: None, True: None}
        count = 0
        for losses in itertools.combinations(range(nominal), missing):
            for values in itertools.product(COORDS, repeat=missing):
                fill = ''.join(values)
                plaintext = decode(fill_frame(source, losses, fill), ranks, square)
                score = sum(ch in CATEGORY for ch in plaintext)
                for maximize in best:
                    candidate = (-score if maximize else score, losses, fill)
                    if best[maximize] is None or candidate < best[maximize]:
                        best[maximize] = candidate
                count += 1
        checks = []
        for check in record['checks']:
            reported = check['exact_search']
            maximize = reported['maximize_target_category']
            expected = best[maximize]
            score = -expected[0] if maximize else expected[0]
            assert score == bounds[maximize] == reported['target_category_count']
            assert list(expected[1]) == reported['missing_full_ciphertext_positions']
            assert expected[2] == reported['filled_missing_coordinates']
            witness(case, square, reported)
            checks.append(dict(maximize=maximize, exact_count=score,
                               canonical_loss_positions=list(expected[1]), canonical_fill=expected[2]))
        assert count == record['witnesses_enumerated']
        reports.append(dict(width=len(ranks), nominal_coordinates=nominal, missing=missing,
                            exhaustive_witnesses=count, both_signs_and_canonical_witnesses_agree=True,
                            checks=checks))
    assert sum(r['exhaustive_witnesses'] for r in reports) == 10188
    return reports


def audit():
    category_path = HERE / 'category_bounds.json'
    published = json.loads(category_path.read_text())
    input_path = ROOT / 'experiments/p198_exact_sparse/inputs.json'
    cases = json.loads(input_path.read_text())['cases']
    case = next(c for c in cases if c['id'] == 'p198_Nov13-15b')
    source, ranks, partial = case['observed_ciphertext'], case['column_rank_order'], case['partial_historical_square']
    keys = json.loads((ROOT / 'data/keys.json').read_text())['keys']
    key = next(k for k in keys if k['id'] == 'Nov13-15b')
    messages = json.loads((ROOT / 'data/messages.json').read_text())['messages']
    target = next(m for m in messages if m['id'] == 'p198')
    assert source == target['transcript']['analysis_ciphertext']
    assert partial == key['square'] == published['partial_square']
    assert ranks == key['column_rank_order']
    assert published['input_sha256'] == digest(input_path)
    assert set(ALPHABET)-set(partial) == set('QY234789')
    assert len(CATEGORY) == 24 and CATEGORY <= set(partial)
    assert set(published['target_category']) == CATEGORY
    mask = [int(ch in CATEGORY) for ch in partial]
    assert sum(mask) == 24 and all(ch != '?' or value == 0 for ch, value in zip(partial, mask))

    base_source = HERE / 'exact_letter_bounds.cpp'
    assert digest(base_source) == published['base_engine_sha256']
    generated = base_source.read_text()
    for change in published['declared_source_adaptations']:
        assert change['required_occurrences'] == generated.count(change['exact_original']) == 1
        generated = generated.replace(change['exact_original'], change['replacement'])
    generated_hash = hashlib.sha256(generated.encode()).hexdigest()
    assert generated_hash == published['generated_engine_sha256']

    controls = small_controls(published['controls']['records'])
    optimum = maximum_count(source, ranks, 5, mask)
    assert optimum['column_allocations'] == math.comb(20, 5) == 15504
    assert optimum['maximum_category_count'] == published['maximum_target24_positions'] == 75
    representative = published['representative_complete_square']
    assert all(a == '?' or a == b for a, b in zip(partial, representative))
    assert [int(ch in CATEGORY) for ch in representative] == mask
    attained = witness(case, representative, published['exact_search'])
    assert attained['counts'] == dict(common24=75, Q=0, Y=0, digits=10)
    positive_record = published['positive_control']
    positive = next(c for c in cases if c['id'] == positive_record['case_id'])
    positive_mask = [int(ch in CATEGORY) for ch in positive['fixed_complete_square']]
    positive_optimum = maximum_count(positive['observed_ciphertext'], positive['column_rank_order'], 5, positive_mask)
    assert positive_optimum['maximum_category_count'] == 85
    witness(positive, positive['fixed_complete_square'], positive_record['exact_search'])

    # A deliberately relaxed multiset shows why the fixed transposition matters.
    relaxed = 'E'*35+'P'*18+'B'*6+'H'*6+'A'*20
    histogram = {ch: 0 for ch in COORDS}
    for ch in relaxed:
        cell = partial.index(ch)
        histogram[COORDS[cell//6]] += 1
        histogram[COORDS[cell % 6]] += 1
    assert all(histogram[ch] == source.count(ch)+(5 if ch == 'V' else 0) for ch in COORDS)
    assert len(relaxed) == 85 and set(relaxed) <= CATEGORY

    paths = [category_path, input_path, base_source, Path(__file__).resolve()]
    return dict(schema='adfgvx-common24-independent-pair-dp-v1', project='ADFGVX Cipher',
                authors='icekylinx and GPT-6 Astra Pro', verified=True,
                input_hashes={str(p.relative_to(ROOT)): digest(p) for p in paths},
                category=''.join(ch for ch in ALPHABET if ch in CATEGORY),
                partial_square=partial, ranks=ranks, observed_ciphertext=source,
                observed_ciphertext_sha256=hashlib.sha256(source.encode()).hexdigest(),
                invariant_cell_mask=mask, complete_square_extensions_covered=math.factorial(8),
                independent_algorithm='Each fixed column-loss allocation determines received column segments. The additive objective separates into adjacent physical column pairs. Independent two-dimensional insertion-alignment DPs optimize each pair; summing their optima is exact for that allocation. All 15,504 allocations are enumerated.',
                category_invariance='Every unknown square cell contains Q, Y, or a digit and scores zero; all 40,320 complete-square extensions have the identical category mask.',
                generated_C_source_adaptations_hash_verified=generated_hash,
                C_engine_invoked=False, repository_cipher_functions_imported=False,
                small_exhaustive_controls=controls, total_small_witnesses=10188,
                historical_exact=optimum, reported_C_witness=attained,
                true_key_positive_control=positive_optimum,
                necessary_digits_plus_Q_plus_Y_minimum=10,
                attainable_digits_minimum_when_QY_absent=10,
                histogram_only_relaxation=dict(plaintext_multiset=dict(E=35, P=18, B=6, H=6, A=20),
                    completed_coordinate_counts=histogram, added_coordinates='VVVVV', common24_count=85,
                    interpretation='A multiset witness only, not a transposition/source witness. The ten-character obstruction depends on fixed rank order and loss geometry.'),
                limits=['The partial square, transposition, and exactly-five-loss model remain hypotheses.',
                        'The full category optimum is recomputed here, but no language plausibility or historical reading is asserted.',
                        'The independent DP checks count optima; canonical historical witness ordering is not needed for the bound.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--verify', action='store_true', help='Recompute and compare without rewriting the saved audit.')
    args = parser.parse_args()
    start = time.monotonic()
    result = audit()
    if args.verify:
        assert result == json.loads(args.output.read_text())
    else:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(verified=True, full_optimum_recomputed=True,
                          historical=result['historical_exact'],
                          small_exhaustive_witnesses=result['total_small_witnesses'],
                          QY_free_digits=result['attainable_digits_minimum_when_QY_absent'],
                          elapsed_seconds=time.monotonic()-start), indent=2))


if __name__ == '__main__':
    main()
