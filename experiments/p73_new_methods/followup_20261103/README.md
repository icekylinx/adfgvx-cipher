# p73: profile pairing and new-rank followup

**p73 remains unread.** This compact followup preserves a new source-preserving
method, its useful synthetic controls, and its bounded negative application.
It proposes no historical plaintext, key, date correction or catalogue change.

Prepared by **icekylinx and GPT-6 Astra Pro**, 3 November 2026. The earlier
Lasry–Schmeh challenge and the parent package's earlier work retain their
existing credits.

## Method and completed scope

The unchanged p73 frame has **178 slots: 176 observed coordinates and two
printed erasures at source indices 1 and 2**. Both October 26 and November 8
date layers remain as printed. No source position is inserted or excluded.

For each even width, enumerate every assignment of long/short transmitted
columns. A radio-derived sorted cell-frequency profile then ranks column
pairings without a supplied square. Retained distinct pairings are followed
by compatible pair-order enumeration and an annealed permutation of all
36 square symbols. The square and original keyword remain unknown.

| Width | Long/short source segmentations | Pairing seeds fitted to language |
| --- | ---: | ---: |
| 10 | 45 | 12 |
| 12 | 66 | 15 |
| 14 | 1,001 | 15 |
| 16 | 120 | 15 |
| Total | **1,232** | **57** |

Each target language fit used 60 restarts of 40,000 iterations. The 57 frozen
best states are diagnostics. The number of segmentations does not count
distinct complete keys, and stochastic pairing/square search is not exhaustive.
Seed deduplication used the unordered transmitted-column pair set. It did not
retain every long/short segmentation that could share that pair set.

## Related controls and exact witnesses

One freshly composed 89-position German control was re-encrypted with a
random hidden square and independently randomized ranks at four widths.
Both erasures were imposed in the p73 source positions. Selection used the
highest language score among the retained profile seeds; evaluation-only
true-rank sentinel runs are excluded from these four selections.

| Width | Literal positions correct / fixed | Complete truth compatible with all 176 observed coordinates |
| --- | ---: | --- |
| 10 | 86/87 | Yes; zero observed-coordinate changes |
| 12 | 79/87 | Yes; zero observed-coordinate changes |
| 14 | 82/87 | Yes; zero observed-coordinate changes |
| 16 | 65/87 | Yes; zero observed-coordinate changes |

The selected ranks recover the visible equality pattern. The complete global
square witnesses were constructed afterward using the known control truth.
Each injective square re-encrypts the full 89-position truth, agrees with every
observed coordinate including surviving half-pairs, and supplies only the two
printed-mask fills. These are arithmetic witnesses, not independently
recovered squares. Literal letter estimation and later word scoring still
make errors. The widths are related mechanism tests, not independent samples
or a general recovery-rate estimate.

The width-18 control retained incomplete pairings. Nested whole-square/order
refits after component-column changes also failed their controls and were not
applied historically. An alternative positive-count objective likewise failed
its control. Neither branch contributes a p73 reading.

## Expanded donor comparison

The new arbitrary ranks join published and reversed ranks in a **104-query**
screen: 103 historical queries and one positive control. The **944 donor
strings** include 293 curated source-only strings; other case fences can
include diagnostics. Their raw/editorial assumptions remain attached.
The input reuses 146 identical strings by reference to the parent's frozen
retrieval corpus, rather than duplicating those earlier inputs.

The exact assignment engine visits every relative offset with at least
60 known overlapping positions, yielding **94,795 reported query/donor
optima**. Best historical agreement is **31/61 = 50.82%**, or at most
**50.00%** in the curated source-only subset. The fresh control retrieves
87/87. No donor wording is accepted. The default verifier independently
checks 41 frozen leader/control assignments; the optional replay verifies
the entire output by its SHA-256. The 41 records comprise 20 overall leaders,
20 curated-subset leaders and one control, with overlap between the two lists.

## Verification and reproduction limits

```sh
python experiments/p73_new_methods/followup_20261103/verify.py
python experiments/p73_new_methods/followup_20261103/verify.py --recompute-donors
python experiments/p73_new_methods/followup_20261103/verify.py --recompute-profile 10
```

Default verification needs only Python's standard library. The two optional
replays also require `g++`. The donor replay uses the parent's unchanged
integer assignment engine. The profile replay uses the frozen means/variances
and included pairing engine; its byte comparison records the reference C++
run and can be sensitive to library-dependent ordering of equal-score ties.

**The complete stochastic search is not self-contained or claimed replayable
from this followup.** Its unbundled scratch 37-symbol model hashes to
`c7a114f115c707d665ce9884a9ed9814437e59d98b4ab0c0fe646bebfd95ad7d`;
the build provenance was not retained here. It is **different from** the
parent package's older `17688f91…` model. Substituting that older artifact
does not reproduce these runs. Language scores are recorded diagnostics,
not independently validated probabilities or historical evidence.

[inputs.json](inputs.json), [certificates.json](certificates.json) and
[scope.json](scope.json) retain the source frame, selected states, exact
control witnesses, budgets and limits. No model binaries, full search logs,
candidate clouds or duplicate earlier results are added.
