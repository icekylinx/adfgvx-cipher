# Exact alignment of five scattered losses

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result

For a **fixed complete square and transposition**, the new dynamic program
finds the global optimum of the stated quadgram objective over every way
to insert five missing coordinates into p198's 165 received coordinates.
It covers all

\[
\binom{170}{5}=1,115,034,284
\]

loss masks by enumerating 15,504 per-column loss allocations and solving
each exactly. The four recorded 16-column runs reached at most **243
active states** per layer. There is no stochastic search or beam pruning.

| Fixed-square case | Exact best loss positions | Outcome |
| --- | --- | --- |
| Synthetic CHI-Nov13, true square supplied | `7, 44, 81, 126, 160` | The optimum is **wrong** at one otherwise fixed plaintext letter: 79/80 singleton positions agree with the planted text. |
| Synthetic Nov13-15b, true square supplied | `16, 17, 19, 20, 21` | A genuine alternate loss mask; all 80 singleton positions agree and the true plaintext still reproduces the received source. |
| p198, frozen CHI-Nov13 completion | `16, 18, 88, 96, 169` | Confirms the earlier heuristic's loss mask as a global optimum under this fixed completion and quantized objective; text remains unreadable. |
| p198, frozen Nov13-15b completion | `27, 46, 86, 128, 149` | Also confirms the earlier heuristic's geometry under its fixed completion; text remains unreadable. |

The first control is especially informative. Its actual last loss is at
158, but the **exact** optimum puts it at 160 and yields `…?EKERMITTELN`
where the planted text contains `…UEBERMITTELN`. This is a demonstrated
weakness of the marginal scoring objective under the true key. Running
the same optimizer longer cannot repair it. The score advantage is much
larger than the documented quantization error.

No historical p198 plaintext is accepted. The two historical complete
squares are explicitly frozen heuristic completions of partial recorded
keys. They are not newly established historical keys, and this experiment
does not bound other completions of those squares. Inputs and full
provenance are in [inputs.json](inputs.json); the complete exact records
and controls are in [results.json](results.json). The earlier stochastic
work is preserved in [the sparse-search collection](../open_targets/sparse_results.json).

## Objective and loss model

<a id="what-is-optimized"></a>

The source is assumed to have lost exactly five coordinate symbols, with
no substitutions, insertions, transposed groups, or changed key. Every
one of the 165 retained coordinates remains in its original relative
order. The nominal frame is therefore 170 coordinates, or 85 plaintext
positions. This is a hypothesis about the damage, not a proven description
of p198's transmission history.

A chosen loss mask supplies a padded ciphertext containing five `?`
positions. Untransposition under the fixed key gives known or partially
known coordinate pairs. With a complete square, each pair has one of
49 possible plaintext domains:

- 36 singleton cells when both coordinates are known.
- Six row domains and six column domains when one coordinate is lost.
- One 36-symbol domain when both are lost.

For each four-position window, the objective averages the base model's
frequency over the Cartesian product of those four domains, then takes
its base-ten logarithm. It is the same **mean-domain composite** used by
the earlier sparse-loss heuristic, subject to the explicit quantization
below. Missing-coordinate values are averaged, not chosen. Because
overlapping windows marginalize separately, this score is not a joint
likelihood for one globally filled plaintext.

The model is the existing hash-pinned military four-gram table, trained
on independent German books without the challenge plaintexts.
[Model provenance](../joint_search/models/provenance.json).

## Fixed marginal table and deterministic arithmetic

The `49^4 = 5,764,801` domain combinations are precomputed once for each
fixed square. The implementation first permutes the ordinary 36-symbol
frequency tensor into square-cell order, then applies a linear mean
transform along each of its four axes. This avoids repeated enumeration
of up to `6^5` coordinate alternatives in the search loop.

Each resulting log value is rounded once to float32 and stored in a
temporary 23 MB table. Its file hash is recorded. Those stored values are
represented **exactly** as integer multiples of `2^-24`; dynamic-program
sums and comparisons therefore have no floating-point accumulation or
tie drift. The precise optimum claim is for this quantized table.

The unrounded objective is checked separately with a Python Cartesian-
product implementation. For the inspected windows, rounding error is
bounded by `2^-21` per log value, approximately `0.000000477`. Mean-score
differences from the earlier heuristic are reported explicitly. A proof
for the quantized objective does not silently become a proof for every
possible floating-point implementation of the unrounded objective.

## Exact row dynamic programming

For a 16-column, 170-coordinate frame, ten columns have length 11 and six
have length 10. Assign the five losses among those physical columns.
There are

\[
\binom{16+5-1}{5}=15,504
\]

such allocations. Once an allocation is fixed, each received column's
length and boundaries are known: it contains its full length minus its
allocated loss count. Thus the 165-symbol source is split into fixed
column segments for that allocation.

The algorithm visits coordinate pairs in plaintext row order. At each
column visit, it may consume the next received coordinate or record a
loss, provided the allocated counts permit that choice. A state stores:

1. How many losses have already been used in every column, encoded in
   mixed radix.
2. The last three plaintext-domain identifiers, sufficient to score the
   next quadgram.
3. The best integer score and a canonical loss-position witness.

Two prefixes reaching the same state have the same future observed
coordinates, remaining loss counts, and language context. Only their
best score is needed. Equal scores retain the lexicographically earliest
sorted loss-position list. Adding a common future set of positions
preserves this order, so the tie rule also respects prefix dominance.

Each complete loss mask belongs to exactly one column allocation. The
global best across all exact allocation solutions is therefore the
global best across all `C(170,5)` masks. A state-cap violation would abort
the search; it never trims states or returns an approximate result.

The observed small state count has a structural reason. With a width
of at least six, the last three plaintext pairs visit distinct columns.
For a column allocated `l` losses, its used count and whether its most
recent relevant coordinate was lost admit at most `2l+1` combinations.
Their product is at most `3^5 = 243` for five losses. The recent domain
sequence is determined by those choices and the fixed column segments.
The implementation uses a general suffix representation and obtains
this reduction through exact state merging.

## Controls and independent checks

Three small cases are solved both by the dynamic program and by explicit
enumeration of **every** loss mask:

| Width | Nominal coordinates | Losses | Masks independently enumerated |
| ---: | ---: | ---: | ---: |
| 4 | 24 | 2 | 276 |
| 6 | 26 | 2 | 325 |
| 16 | 24 | 2 | 276 |

All 877 comparisons agree on the exact best integer score and canonical
loss mask. The 16-column control has a short final row, exercising
unequal column lengths. Every control window is also checked against
the independent direct marginal scorer. A constant-score table makes
all masks tie and verifies that the canonical first mask is `[0,1]`.

For each full 170-coordinate run, the winner is independently
untransposed and rescored. Choosing any representative from its
plaintext domains re-encrypts to a ciphertext that preserves all 165
received coordinates. The result contains all domains, the padded
ciphertext, exact geometry counts, table hashes, score checks, and
the control truth comparison. It never assigns a missing coordinate
value merely to make the partial text readable.

The known synthetic plaintext and planted loss locations are used only
after optimization for evaluation. The synthetic runs deliberately
supply their complete true square, so they test the alignment objective
and optimizer rather than unknown-key recovery.

## Reproduce

Only Python's standard library, the repository's cipher implementation,
a C++17 compiler, and the existing base model are needed:

```sh
python3 experiments/p198_exact_sparse/compute.py \
  --model /tmp/adfgvx-models/german_military36_quad.bin \
  --work-dir /tmp/adfgvx-exact-sparse-reproduce \
  --verify
```

The command recompiles the engine, checks the frozen inputs against the
earlier sparse-search collection, rebuilds all marginal tables, reruns
the exhaustive small controls, searches all four full cases, verifies
the source witnesses, and compares the complete result. Omit `--verify`
to regenerate [results.json](results.json). Large tables, executables,
and intermediate files stay in the selected temporary directory.

The C++ entry points also support a declared subset of column allocations
for performance pilots. Such output is marked `all_allocations_completed:
false`; it cannot be reported as a global optimum. All committed full
results have that field set to `true`.

## Research consequence

The historical hypotheses remain open because a fixed heuristic square
and a particular five-loss model are only a narrow portion of the real
uncertainty. Within those two fixed hypotheses, further stochastic
movement of the loss positions cannot improve the quantized objective.
The failing true-key control points to the next constructive comparison:
optimize a single concrete plaintext jointly over loss positions and
the values of the five missing coordinates, instead of averaging each
quadgram independently.
