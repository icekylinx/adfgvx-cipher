# Exact crib consistency with source substitutions

**icekylinx and GPT-6 Astra Pro** · Apache-2.0

This package adds an exact, conditional consistency search for a supplied
partial or complete plaintext crib when **both the substitution square and
the column order are unknown**, and a declared number of observed source
coordinates may be wrong. Printed erasures keep their original positions.
The input width, source length, crib positions and substitution budget are
explicit; the search uses no language score or suggested period key.

The retained evidence consists of **nine exhaustive small rank-set oracles,
ten fresh hidden-key controls, and a replay of the existing p153 recovery**.
The p153 replay supplies the previously recovered sixty letters and retrieves
the already known two equivalent partial-key representations. It is a
post-discovery consistency check. This package claims no new historical
decipherment, date, serial number or original-challenge plaintext.

## Comparison with earlier implementations

<a id="what-is-new-here"></a>

The following comparison is limited to the cited repository implementations.

| Existing implementation | Relevant capability | Difference in this package |
| --- | --- | --- |
| [p153 exact crib](../p153_crib/README.md), [even widths](../p153_even_widths/README.md), [odd widths](../p153_odd_widths/README.md) | Unknown rank and square, with an unchanged first-part crib source; a second-part discrepancy is priced after the first fit. | A generic supplied crib can itself contain observed-coordinate substitutions, each charged during the rank-and-square search. |
| [p170 donor matching](../p170_new_methods/followup/README.md) | Unknown column order and up to two observed substitutions under supplied complete period squares, including clipped-source models. | The square is wholly unknown. The source here is a fixed, complete source frame, so the p170 clipping capability is not replicated. |
| [p73 substitution-invariant retrieval](../p73_new_methods/README.md) | An optimal substitution assignment for a supplied rank order. | Every column order at the declared width is searched together with the square and error positions. |

The component-variable representation follows the p153 odd-width work:
each known plaintext symbol has a square-row variable and a square-column
variable. The new implementation assigns the next transmitted chunk to an
unused physical column, generates its possible error-aware component
bindings, and maintains one global injective square. This also handles odd
widths, where a physical column can alternate between square-row and
square-column components.

[`inputs.json`](inputs.json) pins the relevant predecessor source files and the
existing p153 witness. The algorithm and verifier retain the earlier research
attribution through those dependencies. The new generic search, controls and
documentation are by **icekylinx and GPT-6 Astra Pro**.

## Model and completeness boundary

For a source of `N` slots and width `K`, physical column `j` has
`floor(N/K) + (j < N % K)` coordinates. Plaintext is encoded in ordinary
row-major coordinate order and columns are read in increasing rank order.
The source is the complete frame; it has even length, exactly twice the crib
length. A `?` in the source is one erased coordinate. A `?` in the crib is
one unspecified plaintext position. These are distinct kinds of unknown.

At each search step, every unused physical column can supply the next source
chunk. For that chunk, the solver considers every subset of valid coordinates
to ignore within the remaining error budget. Other observed coordinates
bind the corresponding known crib symbols' square components. Conflicting
bindings and collisions between two symbols in one square cell are rejected.
An augmenting-path matching checks that the partial map can extend to a full
36-cell bijection and supplies one concrete completion.

Every valid key at the declared width has a path through this enumeration:
its actual next column is among the choices, and its actual erroneous
positions are among the ignored subsets. Its consistent square survives
the component and injectivity checks. Local alternatives with identical
component bindings and the same ignored-coordinate count are merged; one
ignored-position mask is retained as a witness. This preserves existence and
the set of compatible rank orders. It does not enumerate every equivalent
error mask or every unconstrained full square.

Two necessary pruning bounds are also used. At most six distinct symbols can
share a square row or column. If assigned square components already require
more occurrences of a coordinate than the source observes, the sum of those
positive count deficits cannot exceed the allowed substitutions plus the
declared source erasures. Frequencies count only supplied crib symbols, so
unspecified plaintext positions cannot make this bound too restrictive.

The supported input limits are `2 <= K <= 30`, an even `N <= 512`, at most
64 coordinates per physical column, and `0 <= E <= 7` observed substitutions.
The retained error controls cover budgets zero through two. Large widths,
weak cribs or larger error budgets can be computationally expensive.
Insertions, deletions, clipped ciphertext and shifted crib positions require
different explicit models; they are not silently absorbed into this one.

## Source witnesses and output counts

Every returned row contains a rank permutation, a bijective full square, a
complete arithmetic plaintext, the re-encrypted source frame, ignored source
indices, and the **actual** observed-coordinate substitutions. An ignored
coordinate can coincidentally equal the completed witness, so the ignored
count is an upper bound on actual changes. Both counts remain visible.

`partial_square` contains symbols whose two components were bound on that
search path. Other cells and unspecified crib positions are completed only
to demonstrate arithmetic consistency. Those arbitrary values are not
recovered historical letters. No input source file is rewritten.

Several search paths can return the same rank order, for example with
different nonredundant component bindings. The `solutions` counter therefore
counts returned witnesses, not distinct historical keys. The verifier
compares **sets of rank permutations** with the independent tiny oracle and
checks every returned witness by direct re-encryption.

The summary records both `projects` started and `completed_projects`, as well
as `complete` and `stop_reason`. A resource-limited last project is not counted
as completed. Wall-time and node budgets are polled periodically, so their
boundaries can be exceeded slightly before the stop is reported. A truncated
run cannot establish a no-solution result for its unfinished project.

## Retained checks

| Check | Supplied data and independently tested property |
| --- | --- |
| Nine tiny oracles | Widths 3–5; zero to two substitutions; complete and partial cribs; zero to two declared masks. Python enumerates every rank permutation and every allowed ignored-coordinate subset, then independently checks square matching. Its accepted rank set must equal the C++ result. Two fixtures have no compatible rank. |
| Three 53-character controls | Random hidden complete squares and ranks at widths 16, 17 and 18; one or two deliberately changed source coordinates; one partial crib. The true rank must be retrieved, with returned component bindings compatible with the planted square. |
| Seven 89-character controls | Random hidden complete squares and ranks at widths 16, 17, 18, 20, 21, 22 and 23; two deliberate observed-coordinate changes and source masks at positions 1 and 2; one partial crib. The same true-rank and source-witness checks apply. |
| Existing p153 first part | The supplied sixty-letter crib returns exactly the two previously certified width-18 rank representations and their nineteen-letter partial squares. It requires zero observed substitutions. |
| Existing p153 second-part prefix | Using each returned first-part key, the supplied ammunition-report prefix still requires the already documented `A -> X` changes at source positions 3 and 4. No footer or digit is completed as historical text. |
| Resource stop | A deliberately tiny node budget reports an incomplete project and zero completed projects. |

All control fixtures and the random-generation seed are retained in
`inputs.json`. Keys used to generate the synthetic sources are stored as
verification truth; the C++ process receives only each source, crib, width
and error budget. [`certificates.json`](certificates.json) keeps aggregate
oracle results and compact concrete witnesses. It contains no large donor
corpus or unsuccessful historical search campaign.

## Reproduction

From the repository root, with Python 3 and a C++17 compiler available:

```sh
python experiments/substitution_crib_csp/verify.py --verify
```

The verifier compiles the solver in a temporary directory, verifies pinned
dependencies, reruns every fixture, independently re-encrypts every result,
repeats all exhaustive tiny oracles, and compares the deterministic certificate.
`--write` regenerates that certificate after an intentional, reviewed change.

For a new, explicitly supplied crib pool:

```sh
g++ -std=c++17 -O2 experiments/substitution_crib_csp/search.cpp -o /tmp/adfgvx-crib
/tmp/adfgvx-crib source.txt cribs.txt 18 2 60 0 100
```

`source.txt` contains one unbroken string from `ADFGVX?`. Each line of
`cribs.txt` contains an identifier and a string from `A-Z`, `0-9`, `?` with
exactly half as many positions as the source. Identifiers use letters,
digits, underscore, hyphen or period. The final arguments above mean width
18, at most two observed substitutions, a 60-second budget, no node budget,
and a cap of 100 returned witnesses. A zero resource value removes that
particular cap. Output is one JSON object per line.
