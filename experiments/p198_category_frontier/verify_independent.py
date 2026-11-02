#!/usr/bin/env python3
"""Independently recompute every published p198 digit/QY Pareto frontier.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Standard library only. No primary optimizer or repository cipher arithmetic
is imported. This verifies full finite frontiers, not just their witnesses.
"""
from pathlib import Path
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
DEFAULT_OUTPUT = ROOT / 'data/reviews/p198_pareto_independent.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def undominated(points):
    """Keep all incomparable count pairs while minimizing both coordinates."""
    kept, least_qy = [], math.inf
    for digits, qy in sorted(set(points)):
        if qy < least_qy:
            kept.append((digits, qy))
            least_qy = qy
    return tuple(kept)


def combine(first, second):
    return undominated((a+c, b+d) for a, b in first for c, d in second)


def compositions(total, width, prefix=()):
    if width == 1:
        yield prefix+(total,)
        return
    for value in range(total+1):
        yield from compositions(total-value, width-1, prefix+(value,))


def geometry_pool(case):
    source = tuple(COORDS.index(ch) for ch in case['observed_ciphertext'])
    ranks, missing = case['column_rank_order'], case['missing_count']
    nominal, width = len(source)+missing, len(ranks)
    assert nominal % 2 == width % 2 == 0
    assert sorted(ranks) == list(range(1, width+1))
    heights = [nominal//width+(c < nominal % width) for c in range(width)]
    assert all(heights[c] == heights[c+1] for c in range(0, width, 2))
    readout = sorted(range(width), key=lambda c: ranks[c])
    unique, pair_problems, allocations = {}, [], []
    for losses in compositions(missing, width):
        if any(loss > height for loss, height in zip(losses, heights)):
            continue
        segments, at = [None]*width, 0
        for column in readout:
            size = heights[column]-losses[column]
            segments[column] = source[at:at+size]
            at += size
        assert at == len(source)
        indices = []
        for column in range(0, width, 2):
            problem = (segments[column], segments[column+1], heights[column])
            if problem not in unique:
                unique[problem] = len(pair_problems)
                pair_problems.append(problem)
            indices.append(unique[problem])
        allocations.append(tuple(indices))
    return pair_problems, allocations


def local_options(square):
    options = {}
    for left in range(7):
        for right in range(7):
            possibilities = []
            for a in (range(6) if left == 6 else [left]):
                for b in (range(6) if right == 6 else [right]):
                    char = square[6*a+b]
                    possibilities.append((int(char in '0123456789'), int(char in 'QY')))
            options[left, right] = undominated(possibilities)
    return options


def pair_frontier(left, right, height, options):
    """A separate vector-cost insertion-alignment DP for one column pair."""
    left_losses, right_losses = height-len(left), height-len(right)
    layer = {(0, 0): ((0, 0),)}
    for row in range(height):
        following = {}
        for (left_used, right_used), costs in layer.items():
            left_choices, right_choices = [], []
            if row-left_used < len(left):
                left_choices.append((left_used, left[row-left_used]))
            if left_used < left_losses:
                left_choices.append((left_used+1, 6))
            if row-right_used < len(right):
                right_choices.append((right_used, right[row-right_used]))
            if right_used < right_losses:
                right_choices.append((right_used+1, 6))
            for next_left, a in left_choices:
                for next_right, b in right_choices:
                    state = (next_left, next_right)
                    advanced = combine(costs, options[a, b])
                    following[state] = undominated(following.get(state, ())+advanced)
        layer = following
    return layer[left_losses, right_losses]


def membership_frontier(pool, square):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    problems, allocations = pool
    options = local_options(square)
    pair_answers = [pair_frontier(*problem, options) for problem in problems]
    frontier = ()
    for indices in allocations:
        combined = ((0, 0),)
        for index in indices:
            combined = combine(combined, pair_answers[index])
        frontier = undominated(frontier+combined)
    return frontier


def interim(ciphertext, ranks):
    values, source_index = ['']*len(ciphertext), 0
    for column in sorted(range(len(ranks)), key=lambda c: ranks[c]):
        for position in range(column, len(ciphertext), len(ranks)):
            values[position] = ciphertext[source_index]
            source_index += 1
    return ''.join(values)


def decode(ciphertext, ranks, square):
    values = interim(ciphertext, ranks)
    return ''.join(square[6*COORDS.index(a)+COORDS.index(b)] for a, b in zip(values[::2], values[1::2]))


def encrypt(plaintext, ranks, square):
    values = ''.join(COORDS[square.index(ch)//6]+COORDS[square.index(ch)%6] for ch in plaintext)
    return ''.join(values[c::len(ranks)] for c in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def fill_frame(source, losses, fill):
    assert list(losses) == sorted(set(losses)) and len(losses) == len(fill)
    assert set(fill) <= set(COORDS)
    assert all(0 <= i < len(source)+len(losses) for i in losses)
    observed, inserted = iter(source), iter(fill)
    return ''.join(next(inserted) if i in losses else next(observed) for i in range(len(source)+len(losses)))


def check_witness(case, row):
    square, ranks = row['representative_square'], case['column_rank_order']
    assert len(square) == 36 and set(square) == set(ALPHABET)
    losses, fill = row['loss_positions'], row['fill']
    assert len(losses) == case['missing_count']
    frame = fill_frame(case['observed_ciphertext'], losses, fill)
    assert frame == row['filled_ciphertext']
    plaintext = decode(frame, ranks, square)
    assert plaintext == row['plaintext_witness']
    counts = (sum(ch in '0123456789' for ch in plaintext), sum(ch in 'QY' for ch in plaintext))
    assert counts == (row['digits'], row['Q_or_Y'])
    assert len(plaintext)-sum(counts) == row['target24_letters']
    assert encrypt(plaintext, ranks, square) == frame
    assert ''.join(ch for i, ch in enumerate(frame) if i not in losses) == case['observed_ciphertext']
    assert row['source_coordinates_preserved'] == len(case['observed_ciphertext'])
    heights = [len(frame)//len(ranks)+(c < len(frame) % len(ranks)) for c in range(len(ranks))]
    allocation, at = [0]*len(ranks), 0
    for col in sorted(range(len(ranks)), key=lambda c: ranks[c]):
        allocation[col] = sum(at <= loss < at+heights[col] for loss in losses)
        at += heights[col]
    assert allocation == row['losses_per_physical_column']
    return counts


def small_exhaustive_checks(control_records, memberships):
    reports = []
    for record in control_records:
        case = record['case']
        source, ranks, missing = case['observed_ciphertext'], case['column_rank_order'], case['missing_count']
        nominal = len(source)+missing
        pool = geometry_pool(case)
        observed = [set() for _ in memberships]
        visited = 0
        for losses in itertools.combinations(range(nominal), missing):
            for values in itertools.product(COORDS, repeat=missing):
                frame = fill_frame(source, losses, ''.join(values))
                # Decode every representative independently. The source is tiny;
                # this avoids importing the primary cell-histogram control code.
                for index, member in enumerate(memberships):
                    text = decode(frame, ranks, member['representative_square'])
                    observed[index].add((sum(ch in '0123456789' for ch in text), sum(ch in 'QY' for ch in text)))
                visited += 1
        checks = []
        for index, (member, check) in enumerate(zip(memberships, record['checks'])):
            assert check['QY_cell_indices'] == member['QY_cell_indices']
            brute = undominated(observed[index])
            dynamic = membership_frontier(pool, member['representative_square'])
            assert brute == dynamic == tuple(map(tuple, check['frontier']))
            assert {check_witness(case, row) for row in check['witnesses']} == set(brute)
            checks.append(dict(QY_cell_indices=member['QY_cell_indices'], frontier=list(map(list, brute))))
        assert visited == record['loss_and_fill_witnesses_per_membership']
        assert visited*len(memberships) == record['total_membership_loss_fill_witnesses']
        reports.append(dict(width=len(ranks), nominal_coordinates=nominal, losses=missing,
                            memberships=len(memberships), loss_fill_witnesses_per_membership=visited,
                            membership_loss_fill_witnesses=visited*len(memberships),
                            maximum_frontier_size=max(len(c['frontier']) for c in checks), checks=checks))
    assert sum(r['membership_loss_fill_witnesses'] for r in reports) == 285264
    assert any(r['maximum_frontier_size'] >= 2 for r in reports)
    assert reports[0]['checks'][0]['frontier'] == [[1, 4], [2, 2]]
    return reports


def audit():
    result_path = HERE / 'results.json'
    published = json.loads(result_path.read_text())
    input_path = ROOT / 'experiments/p198_exact_sparse/inputs.json'
    case = next(c for c in json.loads(input_path.read_text())['cases'] if c['id'] == 'p198_Nov13-15b')
    partial = case['partial_historical_square']
    assert published['input_sha256'] == digest(input_path)
    assert published['algorithm_source_sha256'] == digest(HERE/'compute.py')
    assert published['partial_square'] == partial and published['column_rank_order'] == case['column_rank_order']
    unknown = [i for i, ch in enumerate(partial) if ch == '?']
    assert len(unknown) == 8 and set(ALPHABET)-set(partial) == set('QY234789')
    members = published['membership_results']
    assert [tuple(r['QY_cell_indices']) for r in members] == list(itertools.combinations(unknown, 2))
    assert len(members) == 28
    for member in members:
        square = member['representative_square']
        assert len(square) == 36 and set(square) == set(ALPHABET)
        assert all(a == '?' or a == b for a, b in zip(partial, square))
        assert [i for i, ch in enumerate(square) if ch in 'QY'] == member['QY_cell_indices']
    controls = small_exhaustive_checks(published['controls']['records'], members)
    pool = geometry_pool(case)
    assert len(pool[1]) == math.comb(20, 5) == 15504
    frontier, checks, witness_count = (), [], 0
    for member in members:
        found = membership_frontier(pool, member['representative_square'])
        received = tuple((r['digits'], r['Q_or_Y']) for r in member['frontier_witnesses'])
        assert found == received
        assert {check_witness(case, r) for r in member['frontier_witnesses']} == set(found)
        assert member['search_counts']['all_allocations_completed']
        assert member['search_counts']['allocations_completed'] == len(pool[1])
        frontier = undominated(frontier+found)
        witness_count += len(found)
        checks.append(dict(QY_cell_indices=member['QY_cell_indices'], frontier=list(map(list, found))))
    assert frontier == tuple(map(tuple, published['global_frontier_counts']))
    assert {check_witness(case, row) for row in published['global_frontier']} == set(frontier)
    bounds = [dict(QY_budget=budget, minimum_attainable_digits=min(d for d, q in frontier if q <= budget)) for budget in range(16)]
    assert bounds == published['bounds_with_at_most_QY']
    assert published['complete_square_extensions_covered'] == math.factorial(8) == 28*math.factorial(2)*math.factorial(6)
    assert published['all_memberships_and_allocations_completed']
    paths = [result_path, input_path, HERE/'compute.py', Path(__file__).resolve()]
    return dict(schema='adfgvx-independent-digit-QY-pareto-review-v1', project='ADFGVX Cipher',
                authors='icekylinx and GPT-6 Astra Pro', verified=True,
                input_hashes={str(p.relative_to(ROOT)): digest(p) for p in paths},
                source_coordinates_preserved=165, column_rank_order=case['column_rank_order'], partial_square=partial,
                complete_square_extensions_covered=math.factorial(8), membership_classes_recomputed=28,
                loss_allocations_per_membership=len(pool[1]), distinct_pair_problems_per_membership=len(pool[0]),
                independent_implementation='A separately written vector-cost pair alignment DP, with an explicit reusable geometry pool and direct nondominance operations; no primary optimizer or repository cipher arithmetic is imported.',
                exactness='For fixed column segments, each adjacent physical column pair has independent fill/loss choices and additive count costs. Dominated prefixes with the same consumed-source state can never improve a common continuation. Pair-frontier sums and unions over every allocation and membership preserve all globally nondominated pairs.',
                small_exhaustive_controls=controls,
                small_membership_loss_fill_witnesses=285264,
                incomparable_small_control_frontier=[[1, 4], [2, 2]],
                membership_frontiers=checks, historical_membership_frontier_witnesses_verified=witness_count,
                global_frontier=list(map(list, frontier)), global_frontier_witnesses_verified=len(frontier),
                bounds_with_at_most_QY= bounds,
                three_digit_minimum_QY=min(q for d, q in frontier if d == 3),
                zero_QY_minimum_digits=min(d for d, q in frontier if q == 0),
                limits=['Only the recorded partial square, transposition, and exactly-five-loss source model are covered.',
                        'A Pareto frontier contains nondominated count pairs, not every attainable count pair.',
                        'No historical digit/Q/Y count, readable plaintext, key acceptance, or key rejection is inferred.',
                        'Witnesses are checked for feasibility; no global lexical-canonical witness rule is asserted.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    result = audit()
    if args.verify:
        assert result == json.loads(args.output.read_text())
    else:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(verified=True, full_frontiers_recomputed=True,
                          memberships=result['membership_classes_recomputed'],
                          allocations_per_membership=result['loss_allocations_per_membership'],
                          small_exhaustive_witnesses=result['small_membership_loss_fill_witnesses'],
                          global_frontier=result['global_frontier'],
                          historical_membership_witnesses=result['historical_membership_frontier_witnesses_verified'],
                          elapsed_seconds=time.monotonic()-start), indent=2))


if __name__ == '__main__':
    main()
