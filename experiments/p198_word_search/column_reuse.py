"""Exact donor-column permutation search with fixed deletion/edit budgets.

Physical columns are used exactly once. Observed source coordinates retain
order; substitutions are separately priced. This is a finite donor-family
arithmetic test, not a general decipherment or language model.
"""
from functools import lru_cache
from itertools import permutations, combinations, product
from pathlib import Path
import json
import sys
import time

CO = 'ADFGVX'


def columns(plain, square, width):
    loc = {c: i for i, c in enumerate(square)}
    mid = ''.join((CO[loc[c] // 6] + CO[loc[c] % 6] for c in plain))
    return [mid[c::width] for c in range(width)]


def match(cols, source, deletions, max_substitutions):
    """Return one exact witness with <= max_substitutions, or None."""
    width = len(cols)
    lengths = list(map(len, cols))
    total = sum(lengths)
    assert total - len(source) == deletions
    stats = {'states': 0, 'local_alignments': 0}
    length_cache = {0: 0}
    count_cache = {0: (0,) * 6}
    column_counts = [tuple((s.count(c) for c in CO)) for s in cols]
    total_counts = tuple((sum((v[i] for v in column_counts)) for i in range(6)))
    suffix_counts = [None] * (len(source) + 1)
    suffix_counts[-1] = (0,) * 6
    for p in range(len(source) - 1, -1, -1):
        v = list(suffix_counts[p + 1])
        v[CO.index(source[p])] += 1
        suffix_counts[p] = tuple(v)

    def used(mask):
        if mask not in length_cache:
            low = mask & -mask
            c = low.bit_length() - 1
            m = mask ^ low
            used(m)
            length_cache[mask] = length_cache[m] + lengths[c]
            count_cache[mask] = tuple(
                a + b for a, b in zip(count_cache[m], column_counts[c])
            )
        return (length_cache[mask], count_cache[mask])

    @lru_cache(None)
    def local(c, p):
        # Local paths delete donor coordinates and price source substitutions.
        s = cols[c]
        L = len(s)
        limit = min(L, len(source) - p)
        inf = max_substitutions + 1
        dp = [[inf] * (limit + 1) for _ in range(L + 1)]
        dp[0][0] = 0
        for i in range(1, L + 1):
            for j in range(max(0, i - deletions), min(i, limit) + 1):
                if i - 1 >= j:
                    dp[i][j] = dp[i - 1][j]
                if j:
                    dp[i][j] = min(
                        dp[i][j],
                        dp[i - 1][j - 1] + (s[i - 1] != source[p + j - 1]),
                    )
        stats['local_alignments'] += 1
        out = []
        for d in range(min(deletions, L) + 1):
            take = L - d
            if take > limit or dp[L][take] > max_substitutions:
                continue
            i, j = (L, take)
            lost = []
            edits = []
            while i:
                if (
                    j
                    and dp[i][j]
                    == dp[i - 1][j - 1] + (s[i - 1] != source[p + j - 1])
                ):
                    if s[i - 1] != source[p + j - 1]:
                        edits.append((p + j - 1, source[p + j - 1], s[i - 1]))
                    i -= 1
                    j -= 1
                else:
                    lost.append(i - 1)
                    i -= 1
            assert j == 0 and len(lost) == d and (len(edits) == dp[L][take])
            out.append(
                (d, dp[L][take], tuple(reversed(lost)), tuple(reversed(edits)))
            )
        return tuple(out)

    @lru_cache(None)
    def dp(mask, lost, budget):
        stats['states'] += 1
        length, counts = used(mask)
        p = length - lost
        if p > len(source):
            return None
        if (
            sum(
                max(suffix_counts[p][i] - (total_counts[i] - counts[i]), 0)
                for i in range(6)
            )
            > budget
        ):
            return None
        if mask == (1 << width) - 1:
            return () if lost == deletions and p == len(source) else None
        for c in range(width):
            if mask >> c & 1:
                continue
            for d, price, missing, changes in local(c, p):
                if lost + d > deletions or price > budget:
                    continue
                tail = dp(mask | 1 << c, lost + d, budget - price)
                if tail is not None:
                    return ((c, missing, changes),) + tail
        return None
    return (dp(0, 0, max_substitutions), stats)


def witness(plain, square, width, source, deletions, budget):
    cols = columns(plain, square, width)
    answer, stats = match(cols, source, deletions, budget)
    if answer is None:
        return (None, stats)
    rank = [0] * width
    full = ''
    loss = []
    edits = []
    for n, (c, missing, changes) in enumerate(answer):
        rank[c] = n + 1
        loss.extend((len(full) + j for j in missing))
        full += cols[c]
        edits.extend(changes)
    kept = ''.join((c for i, c in enumerate(full) if i not in loss))
    changes = [
        (i, a, b) for i, (a, b) in enumerate(zip(source, kept)) if a != b
    ]
    assert (
        len(loss) == deletions
        and changes == sorted(edits)
        and len(changes) <= budget
        and len(kept) == len(source)
    )
    return (
        {
            'plaintext': plain,
            'square': square,
            'ranks': rank,
            'loss_positions': loss,
            'loss_fill': ''.join(full[i] for i in loss),
            'full_ciphertext': full,
            'observed_substitutions': [
                {'source_index': i, 'from': a, 'to': b}
                for i, a, b in changes
            ],
            'observed_substitution_count': len(changes),
            'all_source_slots_retained_in_order': True,
        },
        stats,
    )


def tinycheck():
    results = []
    for cols in [['AADD', 'DADA', 'ADDD'], ['AADDA', 'DADA', 'ADDD']]:
        truths = set()
        for order in permutations(range(3)):
            full = ''.join((cols[c] for c in order))
            for lost in combinations(range(len(full)), 2):
                truths.add(''.join((c for i, c in enumerate(full) if i not in lost)))
        checked = 0
        for chars in product('AD', repeat=sum(map(len, cols)) - 2):
            source = ''.join(chars)
            price = min((sum((a != b for a, b in zip(source, t))) for t in truths))
            for budget in range(3):
                answer, _ = match(cols, source, 2, budget)
                assert (answer is not None) == (price <= budget)
            checked += 1
        results.append(
            {
                'column_lengths': list(map(len, cols)),
                'sources': checked,
                'budgets': [0, 1, 2],
                'all_results_match_independent_full_permutation_deletion_hamming_enumeration': True,
            }
        )
    return results


def compatible_squares(plain, partial_square, source, max_substitutions):
    """All relevant global completions passing the coordinate-count bound.

 Labels absent from plain have one representative unused completion: changing
 their assignment cannot alter this donor's physical column strings.
 """
    from collections import Counter
    A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    counts = Counter(plain)
    observed = [source.count(c) for c in CO]
    known = [0] * 6
    cells = []
    for i, ch in enumerate(partial_square):
        if ch == '?':
            cells.append(i)
        else:
            known[i // 6] += counts[ch]
            known[i % 6] += counts[ch]
    unused = [c for c in A if c not in partial_square]
    active = sorted((c for c in unused if counts[c]), key=lambda c: (-counts[c], c))
    answers = []

    def walk(at, available, hist, assignment):
        remaining = [counts[c] for c in active[at:]]
        # Both bounds relax the remaining global assignment, so are optimistic.
        if (
            sum(max(a - b, 0) for a, b in zip(observed, hist))
            > 2 * sum(remaining) + max_substitutions
        ):
            return
        maximum = []
        for j in range(6):
            weights = sorted(
                (int(i // 6 == j) + int(i % 6 == j) for i in available),
                reverse=True,
            )
            maximum.append(sum((a * b for a, b in zip(remaining, weights))))
        if (
            sum(max(a - b - c, 0) for a, b, c in zip(observed, hist, maximum))
            > max_substitutions
        ):
            return
        if at == len(active):
            price = sum((max(a - b, 0) for a, b in zip(observed, hist)))
            if price <= max_substitutions:
                square = list(partial_square)
                for ch, i in assignment.items():
                    square[i] = ch
                rest = iter((c for c in unused if c not in active))
                for i in cells:
                    if square[i] == '?':
                        square[i] = next(rest)
                answers.append((''.join(square), price))
            return
        ch = active[at]
        n = counts[ch]
        for i in available:
            h = hist[:]
            h[i // 6] += n
            h[i % 6] += n
            walk(at + 1, [x for x in available if x != i], h, {**assignment, ch: i})
    walk(0, cells, known, {})
    return answers


def replay(manifest, donors):
    windows = sorted(
        {
            row['text'][i:i + 85]
            for row in donors
            for i in range(len(row['text']) - 84)
        }
    )
    assert all(
        len(p) == 85 and set(p) <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        for p in windows
    )
    source = manifest['source']['ciphertext']
    budget = manifest['maximum_observed_substitutions']
    counts = {i: 0 for i in range(budget + 1)}
    hits = []
    states = alignments = 0
    for key in manifest['key_families']:
        for plain in windows:
            for square, minimum in compatible_squares(
                plain, key['square'], source, budget
            ):
                counts[minimum] += 1
                for cap in range(minimum, budget + 1):
                    answer, stats = witness(
                        plain,
                        square,
                        key['width'],
                        source,
                        manifest['coordinate_deletions'],
                        cap,
                    )
                    states += stats['states']
                    alignments += stats['local_alignments']
                    if answer is not None:
                        hits.append(
                            {
                                'key': key['id'],
                                'minimum_observed_substitution_budget': cap,
                                'witness': answer,
                            }
                        )
                        break
    return {
        'unique_source_donor_windows': len(windows),
        'histogram_candidates_by_minimum_coordinate_deficit': {
            str(k): v for k, v in counts.items()
        },
        'candidate_pairs': sum(counts.values()),
        'target_hits': hits,
        'dp_states': states,
        'local_alignments': alignments,
    }


def histogram_selftest():
    """Independent full-completion enumeration checks the histogram pruning."""
    from collections import Counter
    A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    plain = (
        'ANOKMXDERTRANSPORTISTAM18UM0700ANGEKOMMENX'
        'DIEWEITERFAHRTISTFUERDENABENDVORGESEHENXOKM'
    )
    square = A
    masked = set('AEN789Q')
    partial = ''.join(('?' if c in masked else c for c in square))
    cells = [i for i, c in enumerate(partial) if c == '?']
    unused = [c for c in A if c in masked]
    full = ''.join(columns(plain, square, 16))
    native = ''.join((c for i, c in enumerate(full) if i not in [3, 39, 78, 122, 161]))
    results = []
    for budget in range(3):
        source = list(native)
        for p in [12, 140][:budget]:
            source[p] = CO[(CO.index(source[p]) + 1) % 6]
        source = ''.join(source)
        expected = set()
        observed = Counter(source)
        for labels in permutations(unused):
            complete = list(partial)
            for i, c in zip(cells, labels):
                complete[i] = c
            complete = ''.join(complete)
            cols = columns(plain, complete, 16)
            counts = Counter(''.join(cols))
            price = sum((max(observed[c] - counts[c], 0) for c in CO))
            if price <= budget:
                expected.add(tuple(cols))
        found = {
            tuple(columns(plain, complete, 16))
            for complete, _ in compatible_squares(plain, partial, source, budget)
        }
        assert found == expected
        results.append(
            {
                'budget': budget,
                'complete_squares_enumerated': 5040,
                'distinct_compatible_donor_column_families': len(found),
            }
        )
    return results


if __name__ == '__main__':
    import argparse
    import hashlib
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--repo', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    if args.self_test:
        print(json.dumps(tinycheck(), indent=2))
        raise SystemExit(0)
    if not args.verify:
        parser.error('Choose --verify or --self-test')
    manifest = json.load(open(here / 'column_reuse_manifest.json'))
    assert (
        hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        == manifest['engine_sha256']
    )
    donorpath = here / manifest['donor_snapshot']['path']
    assert (
        hashlib.sha256(donorpath.read_bytes()).hexdigest()
        == manifest['donor_snapshot']['sha256']
    )
    donors = json.load(open(donorpath))
    assert len(donors) == manifest['source_donor_bodies']
    if args.repo:
        canonical = json.load(open(args.repo / 'data/messages.json'))['messages']
        record = next((x for x in canonical if x['id'] == 'p198'))
        assert (
            record['transcript']['raw_source_compact']
            == manifest['source']['ciphertext']
        )
        catalog_keys = json.load(open(args.repo / 'data/keys.json'))['keys']
        for key in manifest['key_families']:
            actual = next((x for x in catalog_keys if x['id'] == key['id']))
            assert (
                actual['square'] == key['square']
                and len(actual['column_rank_order']) == key['width']
            )
        for row in donors:
            for origin, path in row['origins']:
                value = json.load(open(args.repo / origin))
                for segment in path:
                    value = value[segment]
                assert value == row['text']
    result = replay(manifest, donors)
    assert result == manifest['source_donor_result']
    histogram_checks = histogram_selftest()
    assert histogram_checks == manifest['histogram_full_completion_checks']
    tiny = tinycheck()
    assert (
        sum(x['sources'] * len(x['budgets']) for x in tiny)
        == manifest['tiny_source_budget_tests']
    )
    fixtures = manifest['control_fixtures']
    run_count = 0
    for fixture in fixtures:
        for garbles in range(3):
            native = list(fixture['source'])
            for p in manifest['control_garble_indices'][:garbles]:
                native[p] = CO[(CO.index(native[p]) + 1) % 6]
            native = ''.join(native)
            answer = None
            for cap in range(garbles + 1):
                answer, _ = witness(
                    fixture['plaintext'],
                    fixture['square'],
                    fixture['width'],
                    native,
                    5,
                    cap,
                )
                if answer is not None:
                    break
            assert (
                answer is not None
                and answer['observed_substitution_count'] == garbles
            )
            if args.repo:
                sys.path.insert(0, str(args.repo))
                from adfgvx.cipher import encrypt
                assert (
                    encrypt(answer['plaintext'], answer['ranks'], answer['square'])
                    == answer['full_ciphertext']
                )
            run_count += 1
    assert run_count == manifest['positive_control_run_cases']
    print(
        json.dumps(
            {
                'verified': True,
                **result,
                'positive_control_run_cases': run_count,
                'distinct_control_texts': len({x['plaintext'] for x in fixtures}),
                'tiny_source_budget_tests': sum(x['sources'] * 3 for x in tiny),
                'histogram_full_completion_checks': histogram_checks,
            },
            indent=2,
        )
    )
