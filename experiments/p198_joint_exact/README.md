# Exact joint loss placement and plaintext completion

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result

The new decoder jointly chooses **all five missing-coordinate positions
and all five coordinate values**, keeping one concrete plaintext consistent
across every overlapping language-model window. For each fixed complete
square and transposition it solves the entire finite problem:

\[
\binom{170}{5}\,6^5=8,670,506,592,384
\]

loss-and-fill witnesses. Different witnesses can produce the same completed
ciphertext or plaintext; this count is not a count of distinct messages.
All four full runs enumerate 15,504 column allocations and reach at most
**16,807 active states** per layer, with no beam pruning.

The exact four-gram optimum is wrong on **both controls supplied with their
true complete keys**. This is useful evidence about the language objective:
more exhaustive search alone does not make its preferred text correct.

| Fixed-square case | Exact best loss positions | Inserted coordinates | Result |
| --- | --- | --- | --- |
| Synthetic CHI-Nov13, true key | `7,44,81,126,160` | `VADAV` | Four plaintext letters differ from truth. |
| Synthetic Nov13-15b, true key | `15,16,17,18,19` | `AFFFF` | Two plaintext letters differ from truth. |
| p198, frozen CHI-Nov13 completion | `16,18,88,96,169` | `AAXXA` | Unreadable model optimum; no historical reading accepted. |
| p198, frozen Nov13-15b completion | `28,45,86,128,149` | `XGXVF` | Unreadable model optimum; no historical reading accepted. |

All positions are zero-based in the hypothetical 170-coordinate ciphertext.
Every one of the 165 observed coordinates is preserved, in its original
relative order. The five added coordinates are model hypotheses.

The controls share this planted plaintext:

```text
DERSTABMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEWEITEREBEFEHLEUEBERMITTELN
```

The CHI-Nov13 optimum is:

```text
DERSTABGELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEREITEREBEFEHLESEKERMITTELN
```

The Nov13-15b optimum is:

```text
DERSTARMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBETTEWEITEREBEFEHLEUEBERMITTELN
```

Both wrong texts re-encrypt exactly to a five-loss completion of their
observed synthetic ciphertext. The truth was used only after optimization
for evaluation, not as a crib or part of the training corpus.

## Objective and score margins

The objective is the sum of the existing military model's original
float32 four-gram log frequencies. Each stored value is exactly
representable at scale `2^24`, so all sums, comparisons and tie decisions
use integers without floating-point accumulation drift. The displayed
mean divides the integer total by `82 * 2^24`.

This differs from the earlier [marginal-domain experiment](../p198_exact_sparse/README.md):
each inserted coordinate receives one concrete value used consistently
throughout the plaintext. The marginal objective averages alternatives
separately in each overlapping window.

| Fixed-square case | Joint optimum mean | Best concrete filling at marginal-optimal mask | Joint improvement over that filling |
| --- | ---: | ---: | ---: |
| Synthetic CHI-Nov13 | −4.160525508 | −4.160525508 | 0 |
| Synthetic Nov13-15b | −4.107718910 | −4.107718910 | 0 |
| p198 / CHI-Nov13 | −7.703862272 | −7.703862272 | 0 |
| p198 / Nov13-15b | −8.246209427 | −8.262625950 | +0.016416524 |

The common planted control text has mean **−4.224131232**. The two wrong
global optima exceed it by **+0.063605724** and **+0.116412323**, respectively,
or exactly **87,504,412** and **160,152,124** integer units. These are
objective preferences, not rounding effects. On Nov13-15b, a best filling
of the earlier marginal-optimal mask already obtains the same wrong
score; its different globally canonical mask is an alias at that score.

An independent Python finite-domain dynamic program computes the best
concrete filling of each marginal-optimal mask. It uses lexical plaintext
ties; the joint engine uses the witness tie order described below. Their
score comparison is valid even when those canonical witnesses differ.

The historical squares are two frozen heuristic completions of recorded
partial squares. They are not established full historical keys. These
optima do not bound other square completions, other transpositions, or
other kinds of transmission damage. Full inputs and their provenance
remain in [inputs.json](../p198_exact_sparse/inputs.json), linked to the
[earlier sparse-search records](../open_targets/sparse_results.json).
The independent training sources are recorded in the
[model provenance](../joint_search/models/provenance.json).

## Exact algorithm

For each distribution of five losses among the 16 physical columns,
the full column lengths and the numbers of retained coordinates fix the
source segment belonging to every column. The decoder then walks the
coordinate pairs in plaintext row order. At each column visit it either
consumes the next retained coordinate or spends an allocated loss. Each
loss branches over the six coordinates `ADFGVX`.

A state stores the number of losses used in each column and the last
three **concrete plaintext letters**. Two prefixes in the same state have
identical future source choices, remaining loss counts and language
context. Keeping their best integer score is exact. The witness carries
its loss-position mask and the inserted coordinate values in ciphertext
position order.

The canonical tie rule chooses the earliest increasing loss-position
list, then the earliest `ADFGVX`-ordered fill string. Prefix dominance is
compatible with that rule: two histories in the same state have equal
numbers of past losses. Adding the same future loss set preserves their
first differing mask position. If their masks coincide, inserting common
future values preserves their first differing fill. This remains true
when ciphertext readout places a future loss before an earlier row's
loss position.

Every complete witness belongs to one column allocation. Each allocation
is solved exactly, and the global best is selected across all 15,504.
A configured state-cap failure would abort rather than return a pruned
answer. All committed runs completed every allocation.

### Why the state count stays small

For the 16-column cases, the most recent six coordinates occupy distinct
columns. If a column has `l` allocated losses, a used-loss count of zero
fixes its recent coordinate; each positive used count admits at most
six coordinate values. The retained-coordinate case is already one of
those six values. Thus there are at most `1+6l` combinations for a recently
represented column, and fewer for a column outside the recent context.

Since the allocated counts sum to five,

\[
\prod_c(1+6l_c)\leq 7^{\sum_c l_c}=7^5=16,807.
\]

The original dense state array obtains this reduction by exact merging.
The same bound applies to a five-letter suffix when at least ten physical
columns are available, which motivates a separate six-gram calibration.
It does not justify an untested historical recovery claim.

## Validation

Three short examples are independently enumerated over every mask and
every coordinate filling:

| Width | Full coordinates | Losses | Witnesses enumerated |
| ---: | ---: | ---: | ---: |
| 4 | 12 | 1 | 72 |
| 6 | 14 | 2 | 3,276 |
| 16 | 20 | 2 | 6,840 |

Across all **10,188** enumerated witnesses, each exhaustive control's
optimum agrees with the dynamic program on score, mask and fill.
A constant-score table additionally makes all witnesses
tie and verifies the first mask `[0,1]` with fill `AA`.

For each full run, independent Python code constructs the completed
ciphertext, decrypts it, recomputes the integer score, re-encrypts the
plaintext, and removes the five inserted coordinates to recover the
observed source exactly. It also checks the prior marginal-mask optimum
with a separate finite-domain dynamic program. The complete results,
including conditional historical texts, are in [results.json](results.json).

## Reproduce

With Python, a C++17 compiler and the hash-pinned model available:

```sh
python3 experiments/p198_joint_exact/compute.py \
  --model /tmp/adfgvx-models/german_military36_quad.bin \
  --work-dir /tmp/adfgvx-joint-reproduce \
  --verify
```

This recompiles the engine, runs all exhaustive controls, reruns all four
full searches, verifies the winners, and compares the committed report.
Omit `--verify` to regenerate the report. Model files and executables
remain outside the repository. The engine also permits declared allocation
subsets for timing pilots; those results explicitly report
`all_allocations_completed: false` and are not global optima.

A fast check without model files or a compiler is also available:

```sh
python3 experiments/p198_joint_exact/verify_recorded.py
```

It verifies the recorded marginal and joint source witnesses, complete
keys, loss counts, column allocations, combinatorial space counts and
score/display arithmetic. It **does not rerun the optimizers or verify
model-table lookups**, so it is not an independent proof of optimality.
