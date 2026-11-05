# Coordinate loss before transposition: source diagnostic and p198

Prepared by **icekylinx and GPT-6 Astra Pro**. **p198 remains open.**

The [p126 A5 source edition](../../pages/125.md#edition-cases-military-armistice-transit-planning-a5-conditional-recovery-of-the-odd-frame)
motivates a distinct error mechanism: a coordinate may have disappeared
from the fractionated stream **before** the sender transposed it. The
source has a printed and observed length of 267, a readable opening and a
readable ending under the opposite pairing phase. A conditional one-coordinate
interim insertion joins those portions. This experiment tests that mechanism
on p198's 165 received coordinates and advertised length of 170.

This differs from the earlier p198 searches: those insert five coordinates
into a 170-slot transmitted ciphertext before undoing its transposition.
Here the original **165-slot** ciphertext is untransposed first, and five
coordinates are inserted into its intermediate stream. A forward witness
removes those five intermediate coordinates and then transposes the remaining
165. All received coordinates and their original rank geometry survive.

## Frozen protocol and completed work

`inputs.json` was fixed before inspecting the new target outputs. It contains
the exact p198 source, all 25 catalogued key records, the control fixtures,
planted damage, model hashes and the calibration gate. The key list includes
dated period keys, partial historical keys, an instructional example and
later recoveries. These additional cases are explicit comparisons; their
inclusion is not evidence for their historical use on p198.

The unchanged book and radio 37-symbol marginal quadgram tables are the two
objectives. No retraining, mixture change, weight tuning or word-score selection
was performed. The radio model includes the existing book component, so
agreement between the objectives is not independent language evidence.

| Completed stage | Actual scope |
| --- | --- |
| Initial contiguous geometry screen | 25 keys × 166 interim placements = 4,150 partial-label candidates; 8,300 scores |
| Fresh controls | 3 source bodies × 3 planted loss patterns × 2 objectives = 18 DP jobs |
| Reused p126 A5 diagnostic | 2 DP jobs |
| Historical arbitrary-five-loss search | 25 fixed key records × 2 objectives = 50 DP jobs |
| Independent small exhaustive validation | 6 cases; 9,672 full loss/fill witnesses enumerated separately |

All **70 principal DP jobs completed**, with zero pending jobs. Their actual
counters are **182,964,558 expanded states** and **1,428,164,910 evaluated
transitions**. These are operations recorded by the completed engine runs;
they are not counts of distinct full plaintexts or explicitly visited complete
loss-and-fill witnesses. The six tiny validation invocations are separate
from these 70 principal jobs and their counters.

The historical 50-job portion accounts for 137,008,046 expanded states and
1,079,388,614 transitions. The 20 control/diagnostic jobs account for
45,956,512 states and 348,776,296 transitions. Original compact output logs
are preserved under `results/logs`, with their hashes in the stage ledgers.
No in-progress incumbent was collected as a completed result.

## Dynamic-programming objective

<a id="what-the-exact-dp-optimizes"></a>

For a fixed supplied square and rank order, let `t` be the number of completed
plaintext pairs and `g` the number of inserted interim coordinates already
used. The number of consumed observations is then exactly `2*t - g`.
The DP state retains `(t, g, h)`, where `h` is the previous three plaintext
labels needed by the quadgram score.

Each next pair has four possible forms:

| Pair form | Observed coordinates consumed | Inserted coordinates used |
| --- | ---: | ---: |
| Both coordinates observed | 2 | 0 |
| First observed, second inserted | 1 | 1 |
| First inserted, second observed | 1 | 1 |
| Both inserted | 0 | 2 |

Inserted coordinates range over all six symbols. An explicit `?` in a received
diagnostic is a source erasure: it consumes an observed slot while allowing
any coordinate value, and does not count as a lost position. Historical p198
has no such received erasure.

The transition score depends only on the state and the next label. Merging
paths with the same state therefore retains the exact best future score
under this objective. Back-pointers preserve one maximizing complete interim
stream and loss mask. The final state uses exactly the specified number of
insertions and consumes every received coordinate. Equal-score alignment
aliases need not have the originally planted mask.

**Partial squares remain partial.** A cell whose published label is unknown
emits `?`; no unused letter or digit is assigned to it. The exact optimum is
then for this conservative partial-label objective, not for jointly optimized
global square completions. The source witness still specifies coordinate
cells and preserves every known square anchor. Missing cells retain their
unassigned status and global bijection requirement.

Scores obtained with different amounts of unknown information cannot rank
historical keys reliably. The entirely unknown `NSA-June1-CHI-21` example
illustrates the problem: its output is 85 question marks, and the marginal
quadgram sum is zero. That result carries no plaintext information and is
never treated as a leading recovery.

## Calibration: strengths and failures

The three fresh 85-character source prefixes are p125 A1, p133 A3 and p130 A1.
Their exact original certificate bytes are preserved in `frozen_sources`.
Each prefix is absent as a complete string from the frozen radio training
records. They were selected after the model was frozen, and neither their
plaintext nor their planted masks are passed to the executable. **The full
true square and true rank order are supplied** in these controls.

The deterministic damage patterns are one lost coordinate, five contiguous
lost coordinates, and five scattered lost coordinates. The arbitrary-loss DP
searches the wider family for every five-loss test; it is not told that a
particular planted mask happened to be contiguous.

The following cells show positional agreement out of 85. Parentheses show
ordinary character edit distance, which also captures shifted passages:

| Fresh body and damage | Book | Radio |
| --- | ---: | ---: |
| p125 A1, one loss | 85 (0) | 85 (0) |
| p125 A1, five contiguous | 16 (7) | 77 (4) |
| p125 A1, five scattered | 81 (4) | 85 (0) |
| p133 A3, one loss | 84 (1) | 84 (1) |
| p133 A3, five contiguous | 23 (6) | 10 (5) |
| p133 A3, five scattered | 85 (0) | 85 (0) |
| p130 A1, one loss | 82 (3) | 82 (3) |
| p130 A1, five contiguous | 48 (15) | 72 (8) |
| p130 A1, five scattered | 77 (8) | 78 (7) |

This is **5 exact texts in 18 run observations on three bodies**. It is not
18 independent validation samples. The frozen gate required at least one
fresh five-loss exact recovery under either objective; it passed on p125 A1
under radio and p133 A3 under both objectives. All failed cases remain in the
ledger. No further objective changes followed their inspection.

Every one of the **13 failed controls has a feasible wrong candidate that
scores strictly above the true text**. Independent score recomputation confirms
that these are objective failures, not unexplored better truth states. In
the one-loss p133 control, both models prefer `UNGOETIG` to the true
`UNNOETIG`. In the numerical p130 control, even one lost coordinate lets the
objective prefer `ZURATER46873` over the true `ZURM2NR46873`. The digits and
abbreviations cannot be certified from language rank.

Some low positional agreement counts arise from a short insertion/deletion
shift in an otherwise similar long passage. That is why `review.json` reports
both positional agreement and Levenshtein distance rather than describing
those candidates as wholly unrelated text.

The **reused** p126 A5 diagnostic is successful under both objectives: each
recovers all 134 labels of the already proposed conditional target and picks
interim insertion 136. That target retains its four observed-coordinate
garbles; the DP is not permitted to repair them. The two source dashes are
filled. This reproduces the conditional mechanism without supplying the
proposed plaintext to the optimizer, but it is not a fresh control or an
independent proof of the historical omission.

## Historical result and limits

The 4,150 initial contiguous placements and the subsequent 50 arbitrary-loss
DP results produce **no accepted p198 plaintext**. Full outputs and loss masks
are retained in `results/contiguous.json` and `results/historical.json`.
Some partial-key outputs contain short word-like fragments among many unknown
labels; none establishes a readable message or key.

The initial screen inserts five **unknown** coordinates and ranks the resulting
partial labels. It does not jointly optimize those five values. The later DP
does optimize their coordinate values, while still preserving unassigned
square labels. Neither stage changes received coordinates, varies the supplied
rank order, recovers an unknown square, or excludes other damage mechanisms.
The control failures limit interpretation of a language optimum even with
a complete, correct key.

## Verification and reproduction

Default independent verification uses only Python's standard library:

```sh
python experiments/p198_pretransposition_loss/verify.py --verify
```

It checks the 70 original logs and hashes, exact source-preserving forward
witnesses, every control truth and comparison, all 4,150 contiguous strings,
the calibration gate, source-fixture snapshots and actual completed counters.
It also rebuilds a deterministic synthetic score table and independently
enumerates all 9,672 tiny witnesses to check the stored DP optima. It does not
need a compiled executable or external book files. It does not recompute the
book/radio scores unless their paths are supplied:

```sh
python experiments/p198_pretransposition_loss/verify.py --verify \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin
```

Both default verification and complete score recomputation passed. The model
builders and provenance remain in the shared
[fixed-search](../fixed_search/README.md) and
[radio-model](../radio_domain_model/README.md) packages.

To rerun the optimizer, compile the C++17 engine on a little-endian machine
and select an empty output directory. Original logs cannot be overwritten:

```sh
c++ -O3 -std=c++17 experiments/p198_pretransposition_loss/interim_dp.cpp -o /tmp/interim_dp

python experiments/p198_pretransposition_loss/run.py --stage controls \
  --engine /tmp/interim_dp \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin \
  --output /tmp/interim-reproduction

python experiments/p198_pretransposition_loss/run.py --stage contiguous \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin \
  --output /tmp/interim-reproduction

python experiments/p198_pretransposition_loss/run.py --stage historical \
  --engine /tmp/interim_dp \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin \
  --output /tmp/interim-reproduction
```

The historical stage verifies the frozen control gate before running.
The separate executable-versus-enumeration check needs no external model:

```sh
python experiments/p198_pretransposition_loss/validate_dp.py --verify --engine /tmp/interim_dp
```

Historical key and body credits remain in the frozen source records and their
original editions. This package claims a new explicitly defined damage-model
test and reproducible arithmetic; it makes no new historical plaintext claim.
