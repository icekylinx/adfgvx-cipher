# Model-free letter-count bounds for a partial square

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result and its limited implication

Under the recorded Nov13-15b transposition and partial square, p198 can
contain **at most 82 ordinary letters among its 85 plaintext positions**
if exactly five coordinates were deleted from the 170-coordinate frame.
Thus every source-compatible completion in this family contains at least
**three digits**. The minimum attainable ordinary-letter count is **44**,
equivalently a maximum of 41 digits. Both extrema have explicit witnesses.

This is a modest necessary constraint, not a rejection of the key.
The historical message's digit count is unknown, and three or more digits
could be entirely legitimate. The maximum-count witness is unreadable;
having many letters does not make it plausible German. No historical
plaintext is accepted.

The calculation uses **no language model, frequency prior, corpus or
p-value**. It covers all **8! = 40,320** completions of the partial square,
all **C(170,5) = 1,115,034,284** five-loss geometries, and every coordinate
filling at those losses. Every one of the 165 observed coordinates remains
unchanged and in its original relative order.

| Fixed-key family | Attainable minimum letters | Attainable maximum letters | Implication |
| --- | ---: | ---: | --- |
| p198, all Nov13-15b partial-square extensions | 44 | 82 | At least three digits under this specific key/damage hypothesis. |
| Synthetic CHI-Nov13, supplied true complete square | 49 | 85 | The all-letter planted plaintext remains feasible. |
| Synthetic Nov13-15b, supplied true complete square | 58 | 85 | The all-letter planted plaintext remains feasible. |

These are extrema. The report does not claim that every integer count
between the extrema has been separately exhibited. The synthetic controls
supply their true complete keys to check the source-loss procedure, not
to test unknown-key recovery.

## Exhausting square completions without choosing arbitrary digits

The recorded partial square is:

```text
H??BMUF15PX0DJLR????S6VONKZ?AWITEGC?
```

Its eight unknown cells contain the letters `Q`, `Y` and the digits
`2`, `3`, `4`, `7`, `8`, `9`. For a count of ordinary letters, only the
choice of which two cells contain letters matters. There are

\[
\binom{8}{2}=28
\]

such membership assignments. Within an assignment, the `2!` permutations
of the letters and `6!` permutations of the digits leave every count
unchanged. One representative complete square therefore suffices for
each assignment, while still covering all `28 × 2! × 6! = 8!` completions.
Letter/digit membership is fixed per cell throughout the whole message;
it is not chosen independently for each occurrence.

The eight unknown square-cell indices are `1,2,16,17,18,19,27,35`, numbered
from zero in row-major order. The maximum of 82 letters occurs when cells
`16` and `35` contain the two remaining letters. One representative is:

```text
H23BMUF15PX0DJLRQ478S6VONKZ9AWITEGCY
```

With losses at ciphertext positions `66,88,101,107,167` and inserted
coordinates `AFFAA`, its completed plaintext contains 82 letters and three
digits. The record includes its exact ciphertext and plaintext solely
as a feasibility witness. Swapping `Q` and `Y` or permuting the remaining
digits does not change this count.

All 28 separate membership results, including both extremizing witnesses,
are in [results.json](results.json). The shared source inputs and frozen
key provenance are in [inputs.json](../p198_exact_sparse/inputs.json) and
the [earlier sparse-search records](../open_targets/sparse_results.json).

## Exact source-preserving dynamic program

As in the [joint language decoder](../p198_joint_exact/README.md), the
algorithm enumerates the 15,504 allocations of five losses among the
16 physical columns. An allocation fixes every received column's source
segment. A row walk then consumes the next source coordinate or spends
one of that column's allocated losses.

The count objective has no language context. The state needs only the
number of losses already used in each column. Its total size is bounded
by

\[
\prod_c(l_c+1)\leq 2^{\sum_c l_c}=2^5=32.
\]

For each coordinate pair, the engine considers all legal lost/present
choices. Given those choices, it can immediately choose the coordinate
values that maximize or minimize that pair's letter indicator. These
values do not affect any other plaintext position, so this local reduction
is exact. A precomputed table also selects the canonical local fill in
ciphertext readout order, which may differ from plaintext pair order.

Two prefixes with the same used-loss state have exactly the same future
source choices. The best signed count dominates the other prefix. Ties
use the earliest increasing loss-position list, followed by the earliest
`ADFGVX` fill in that position order. Adding common future loss positions
and values preserves the ordering. This is the same tie argument used
by the independently reviewed joint decoder.

Each full witness belongs to exactly one loss allocation and one
letter/digit membership assignment. Taking the best and worst values
across all of them gives the attainable extrema over the entire declared
partial-key family. No beam pruning or probabilistic sampling is used.

## Validation and reproduction

Small controls use widths 4, 6 and 16, one or two lost coordinates, and
a partial square with two possible letter/digit membership assignments.
Independent Python enumeration visits **20,376** membership/loss/fill
witnesses. For each of the six control settings, both the minimum and
maximum agree with the dynamic program on count, loss mask and fill.
The controls include unequal column lengths and ties between many
count-equivalent candidates.

Every full reported witness is independently decrypted, recounted,
re-encrypted and checked against all retained source coordinates.
The two full true-key controls both attain their planted all-letter
count of 85. The planted text is used only for this post-search check.

Python's standard library, the repository's cipher implementation and
a C++17 compiler are sufficient; no model download is needed:

```sh
python3 experiments/p198_letter_bounds/compute.py \
  --work-dir /tmp/adfgvx-letter-bounds-reproduce \
  --verify
```

This recompiles the engine, reruns the exhaustive controls and all full
membership searches, independently checks the witnesses, and compares
the stored result. Omit `--verify` to regenerate the report.

A faster recorded-witness check is available for routine CI:

```sh
python3 experiments/p198_letter_bounds/verify_recorded.py
```

That command verifies complete-square membership coverage, both sets of
recorded extrema, ciphertext preservation, count arithmetic and file
hashes. It does not rerun the optimization and therefore does not by
itself prove that no better count exists.
