# Page 153: exact first-crib validation across even widths

Authors: **IceKylin and GPT-6 Astra**.

**Among even widths 14, 16, 18, 20, 22, 24 and 26, only width 18 can encode the
specified sixty first-part letters while preserving its 132 source coordinates.**
It has the same two equivalent partial-key representations as the earlier
width-18 check. Both imply the same two second-part source disagreements,
indices 3 and 4, `A` to `X`, for the proposed 42-letter body.

This is an exact post-discovery consistency check using the recovered text as
a crib. It is not another blind attack, does not assign the six date/number
positions, and does not exclude other widths, corruption models or readings.
The original width-18 proof package is unchanged.

## Complete historical enumeration

| Width | Long columns in 132-slot rectangle | Complete segmentations | Partial-key representations |
| ---: | ---: | ---: | ---: |
| 14 | 6 | 3,003 | 0 |
| 16 | 4 | 1,820 | 0 |
| 18 | 6 | 18,564 | 2, equivalent |
| 20 | 12 | 125,970 | 0 |
| 22 | 0 | 1 | 0 |
| 24 | 12 | 2,704,156 | 0 |
| 26 | 2 | 325 | 0 |

All **2,853,839** segmentations were enumerated. No time, node or solution cap
was reached. Segmentations are column-length layouts, not individual complete
keys. The search also considers every compatible ordered column pairing and
enforces a single injective substitution mapping across all crib positions.

The input is the unchanged 66-position first crib and 132 coordinates, followed
by the proposed 42-letter second crib and 108 source slots. The six first-crib
question marks are unconstrained, not digit guesses. The second crib is used
only to evaluate keys after the first-crib search has finished selecting them.
The nineteen letter assignments leave seventeen square cells unassigned.

## Generic rectangle geometry

For an even width `K`, the first rectangle has `132 % K` long columns. That
remainder is even, so each adjacent physical column pair has equal heights.
The program enumerates all choices of long chunks in transmission order and
all compatible ordered pairs. Repeated crib letters must repeat each of their
two coordinate components. Applying that necessary filter early removes
impossible columns without removing a valid key. Global backtracking then
checks the shared injective letter-to-cell map and uses each transmitted chunk
exactly once.

The second part resets independently at 108 coordinates. Its offsets are
recomputed from `108 / K` and `108 % K` for every returned rank order. No
six-row shortcut is used for widths other than 18. Independent Python
re-encryption checks every returned key and every reported contradiction.

## Independent exclusions without the C solver

`check_exclusions.py` supplies a separate, smaller proof for the other six
widths. For widths 14, 16 and 20, a necessary physical-column repetition pattern
matches **no contiguous substring anywhere in the received source**. At width
24, its pattern matches only one substring, although two distinct columns are
required. This relaxed substring test already excludes every possible
segmentation at those widths.

For width 22, the only segmentation fails a repeated-letter column condition.
For width 26, the script checks all 325 segmentations and records one failed
column-pair condition for each. No substitution fitting or heuristic score is
used in these exclusions. The exact witness list is in
`independent_exclusion_proof.json`.

## Controls and reproduction

Each of the seven widths has a fresh seeded complete square and column order,
using the same first-crib structure and source erasure profile. The generated
second part contains two deliberate known-coordinate errors, at indices 0 and
1. Every control exhaustively returns its true key and the globally transposed
equivalent, with exactly those two errors. These controls test all seven reset
geometries, including ragged second rectangles. Truth is used only to generate
and verify them.

Run inside this directory:

```sh
cc -O3 -std=c11 -Wall -Wextra -Werror enumerate_even.c -o /tmp/p153-even
python3 run_and_verify.py --engine /tmp/p153-even --output /tmp/p153-even-results
python3 check_exclusions.py --output /tmp/p153-even-exclusions.json
```

The raw C interface is:

```text
enumerate_even INPUT WIDTH [CPU_SECONDS [MAX_NODES [MAX_SOLUTIONS]]]
```

Zero or omitted optional budgets mean unlimited. Published runs used 240 CPU
seconds, 100,000,000 recursive nodes and 1,000 returned solutions per case; none
was reached. An interrupted enumeration explicitly reports `complete: false`
and a stop reason. A no-solution summary uses a null minimum mismatch count.
CPU timings are incidental and need not reproduce exactly.

`results/verification.json` records the exact source/input hashes, all seven
historical summaries and all seven control seeds, truths and outcomes. The
JSONL results and frozen control input files permit independent inspection.
No executable, language model or corpus is distributed here.

The conclusion remains conditional on the sixty-letter first crib, the tested
even widths, ordinary row-major input and column readout, per-part resetting,
an injective 36-cell square, and the unchanged first-part ciphertext. The two
second-part A glyphs stay literal source evidence; the calculation does not
identify the historical cause of their disagreement with the proposed wording.
