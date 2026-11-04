# Further p170 recovery methods and their controls

**p170 A remains open.** These bounded experiments extend the square-reuse
search, test a frozen radio-language objective, and transfer a source-layout
fault found in another telegram. None produces an accepted p170 plaintext.
Every returned candidate, failed control, known-cell constraint and completed
budget is retained. The work is by **icekylinx and GPT-6 Astra Pro**; prior key,
source and body credits remain in the referenced repository records.

Throughout, square anchors retain their recorded baseline symbol labels.
The optional numeral and rare-letter interpretations in
[late_key_interpretation](../late_key_interpretation/) are not imposed on any
search here. In particular, a complete recorded late-period square need not
settle the original meanings of every numeral or rare symbol.

The source is the unchanged 106-coordinate transcription in
[`data/messages.json`](../../data/messages.json). Its SHA-256 is
`2cdf18dd71917e53d68f1271f1c297a28a40c65dda2285d05eeb726f9b1ae753`.
The count 106 is handwritten; no typed transmitted length, surviving call
signs or part number establishes that this is a complete transmission. These
rank-search experiments nevertheless use a complete 106-coordinate frame as
an explicit working model. They do not test source loss or truncation.

## 1. Reuse other recorded squares while hiding column order

The [prior runtime inventory](prior_scope_inventory.json) records 35 completed
nearby-period jobs and 13 earlier CHI-Nov8 jobs, separately from this campaign.
The shared [anchored-search report](../anchored_search/) freezes an earlier
2/70 snapshot; its planned-case count should not be mistaken for completed
p170 work. The large fixed-key truncation scan has its own
[report](../known_key/P170_TRUNCATION_NOTE.md). This branch adds 18 recorded
square anchors that the nearby-period rank searches did not cover.
Known square cells are fixed; only unassigned cells are permuted
injectively, together with a freely searched column order. The optimizer
receives no candidate plaintext.

The frozen [inputs](cross_period_inputs.json) define 234 potential cases.
**Only the first 54 were requested:** each anchor at its recorded width, one
column shorter and one longer. The wider list of widths 12–24 was not run.
Additional-period and instructional squares are comparison anchors, not
evidence that their historical dates apply to p170.

| Square anchor | Widths in the 54-job campaign |
| --- | --- |
| Sep19–21; Oct4–6 | 21, 22, 23 |
| Nov13–15a; Nov19–21; Aug8–9 | 19, 20, 21 |
| Nov13–15b; Nov28–Dec1; CHI-Nov13; Jul18 | 15, 16, 17 |
| Nov16–18; Aug3; TRUPPENVERSCHIEBUNG-2026-reported | 18, 19, 20 |
| Nov22–24 | 21, 22, 23 |
| Nov25–28 | 22, 23, 24 |
| Jul22 | 20, 21, 22 |
| Aug20 | 14, 15, 16 |
| NSA-undated-CHI-example-18 | 17, 18, 19 |
| Worked-example-VIKINGSCROWNHOTEL | 16, 17, 18 |

Before the historical trials, six fresh controls used two newly composed
53-character bodies, four complete and two partial squares, and hidden
random column orders. All six received 1,000 restarts of 100,000 loop slots.
The planted plaintexts and ranks were evaluation-only.

| Control | Width | Initially correct characters | Stronger selected repeat |
| --- | ---: | ---: | ---: |
| Sep19–21, prose | 18 | 53/53, exact ranks | — |
| Oct4–6, prose | 22 | 53/53, exact ranks | — |
| Nov19–21, numeric text | 17 | 53/53, exact ranks | — |
| Nov28–Dec1, numeric text | 20 | 2/53 | 53/53, exact ranks |
| Jul18, partial square, prose | 16 | 53/53, exact ranks | — |
| Nov13–15a, partial square, numeric text | 21 | 5/53 | 2/53 |

The two failures were then selected for independent-seed repeats with 5,000
restarts each. One recovered the exact result; the other still failed. This
adaptive repeat is not a fresh six-control success rate. These small, related
mechanism controls do not estimate a general recovery probability. A failure
does not exclude the associated historical key or width.

[`cross_period_results.json`](cross_period_results.json) preserves the initial
six controls, both stronger repeats and the 54 historical results. The
original engine did not count fitness calls. Its legacy field named
`configured_proposal_slots` means completed configured loop slots: 600 million
for the initial controls, 1 billion for the repeats and 5.4 billion for the
historical jobs. Same-cell proposals can skip evaluation; transposition
proposals can repeat a state; polishing adds calls. These figures must not
be described as distinct states or exact fitness-call totals.

## 2. Matched full-square controls for the frozen radio objective

The [radio-domain model package](../radio_domain_model/) freezes 45 training
strings and 4,634 usable quadgrams from source editions outside six held-out
families. Digits collapse into one class in the radio component and are then
expanded uniformly. The radio and independently built book probabilities
are mixed equally. Editorial assumptions and earlier body credits remain
attached to those source editions. No p170 candidate trains the model.

For these six 53-character controls, **the full true square is supplied**;
only column order is hidden. Both models receive the same per-family seed,
1,000 restarts and 100,000 slots per restart. No true rank or plaintext enters
the optimizer. This isolates the rank-search/model interaction from square
completion, and is easier than historical jobs with partial square anchors.

| Held-out family | Width | Book: correct characters | Radio mixture: correct characters |
| --- | ---: | ---: | ---: |
| p92 A, Dutch courier | 16 | 53/53 | 53/53 |
| p84 A, oil inquiry | 16 | 1/53 | 53/53 |
| p190 D, relay request | 19 | 1/53 | 53/53 |
| p192 part 2, appointment | 20 | 4/53 | 53/53 |
| p205 A2, finance | 20 | 53/53 | 53/53 |
| p96 B, Filittis permission | 22 | 6/53 | 1/53 |
| **Exact texts and ranks** | | **2/6** | **5/6** |

In every failed full-square job, the true plaintext scores above the returned
candidate. The remaining radio failure is therefore a search failure under
this budget, not an objective preference for the wrong full plaintext. Its
true score is −5.055297332; the returned score is −5.153025565, a gap of
0.097728233. The improvement on five controls does not establish reliable
recovery for width 22, partial squares, damaged sources or other text families.
The same held-out families used elsewhere are not independent new historical
samples.

[`radio_rank_results.json`](radio_rank_results.json) is frozen and its hash is
pinned by the subsequent historical input. All 12 jobs completed, recording
1,200,000,000 annealing fitness calls, 2,118,195 polishing calls and 12,000
initial evaluations: **1,202,130,195 total fitness calls**.

## 3. A bounded historical radio campaign

After that calibration, the [historical settings](radio_historical_inputs.json)
were frozen for four anchors: Nov7–9, Nov4–6, Nov10–12, and the separately
attributed CHI-Nov8-2026-recovery square. Each uses widths 16–22, with every
observed p170 coordinate and every previously known square cell unchanged.
No additional digit relabeling, plaintext crib or source correction is used.

All **28 jobs** completed at 1,000 restarts × 100,000 slots. The
[complete results](radio_historical_results.json) contain:

| Recorded quantity | Count |
| --- | ---: |
| Completed restarts | 28,000 |
| Annealing loop slots | 2,800,000,000 |
| Annealing fitness calls | 2,693,773,478 |
| Polishing fitness calls | 6,335,421 |
| Initial evaluations | 28,000 |
| **Total fitness calls** | **2,700,136,899** |
| Accepted p170 plaintexts | **0** |

The [instrumented C source](counted_anchored_joint.c) adds counters to the
existing optimizer without changing random-number calls, mutations, scores or
acceptance decisions. A small matched run produced byte-identical improving
checkpoint output with the original engine. Counts represent evaluations,
including repeated states; they are not an exhaustive key-space measure.

The highest-scoring returned text is still incoherent. A round-trip validates
the arithmetic of a returned square and rank order; it does not identify the
original message. The verifier also records how many plaintext positions are
fixed by the original partial square at each returned rank order, separating
those positions from letters supplied by the searched completion.

## 4. Transfer the independently observed single-group displacement

The [p191 boots-request edition](../boots_request/) identifies a displaced
five-coordinate printed group under a fixed published key. That positive
source-layout result motivates this separate, bounded p170 screen. It does
not imply that p170 has the same fault.

For p170's 21 complete groups, move any one full group to another position,
or keep the original order. The final one-coordinate tail remains fixed.
There are **421 operation descriptions and 401 distinct frames**. All 24
informative recorded square/rank pairs are held fixed; the all-unknown NSA
June key supplies no useful fixed-square test and is excluded explicitly.
Known square cells remain fixed and unknown cells remain `?` when scoring.

Both models score all frames: **9,624 historical frames per model, 19,248
historical score evaluations in total**. The six control/model pairs add
2,406 evaluations. The [results](group_move_results.json) retain
each key/model's three leaders, their operation aliases and raw fixed-letter
counts. A separate globally injective completion witness proves arithmetic
compatibility but is neither scored nor accepted as a historical reading.

Three matched controls include fresh radio prose, fresh supply prose, and
the first 53 characters of the independently edited p200 A source. Book
ranking selects all three true frames; radio ranking selects two. In the
failed radio supply control, truth is third:

| Candidate | Fixed characters | Radio score |
| --- | ---: | ---: |
| True supply-control frame | 53/53 | −4.306179214 |
| Incorrect leader | 48/53 | −4.162675924 |

The wrong leader is
`MERPFLEG??GREICHTNURNOMH??SMORGENXNACH?CIUBDRINGENDXX`.
The 37-symbol table marginalizes a `?` by summing compatible probability
mass. A less informative partial text can therefore score higher than a
fully determined true text. This bias is visible even within one fixed key;
raw scores across different partial squares are still less comparable.
The rank searches in sections 1–3 score complete candidate squares and do
not introduce those wildcard characters into their unchanged-source texts.

No group-move candidate is accepted. The exhaustive statement applies only
to this finite move set and the fixed recorded keys, not to arbitrary source
damage, column orders or new square completions.

The [column-family follow-up](followup/README.md) tests known source-derived
donor bodies while allowing arbitrary column order and missing outer columns.
Its coupled-domain branch preserves partial donors' original half-coordinates.
Exact and damaged source controls pass; no p170 donor match is found within
the frozen bounds.

## Verify or replay

The default verifier needs only the Python standard library and this
repository. It independently reconstructs physical columns, re-encrypts
every archived search result, checks fixed cells, input and runner hashes,
control accuracy, recorded budgets, group geometry and witness distinctions:

```sh
python experiments/p170_new_methods/verify.py
```

Supplying the two pinned binary models also recomputes scores and the entire
finite group-move ranking, including ties. This optional full ranking uses
NumPy through the original runner:

```sh
python experiments/p170_new_methods/verify.py \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin
```

The model hashes are in [radio_rank_inputs.json](radio_rank_inputs.json).
Rebuild the book models using
[`joint_search/tools/build_models.py`](../joint_search/tools/build_models.py)
and its hash-pinned public-book cache; build the radio mixture using
[`radio_domain_model/build.py`](../radio_domain_model/build.py). Model paths
in the original runtime records are provenance, not required storage paths.

To replay a single expensive search with explicit paths:

```sh
cc -O3 -std=c11 -Wall -Wextra \
  experiments/p170_new_methods/counted_anchored_joint.c \
  -lm -o /tmp/p170-counted-anchored-joint
python experiments/p170_new_methods/replay.py --list
python experiments/p170_new_methods/replay.py \
  --campaign radio_rank \
  --job radio_holdout_0_p92_A__radio_mixture \
  --engine /tmp/p170-counted-anchored-joint \
  --model /path/to/radio_book37_quad_marginal.bin \
  --output /tmp/p170-replay
```

The replay reports binary identity, selected-candidate equality and, where
originally recorded, counter equality. Compiler and floating-point changes
may affect stochastic search trajectories. The independent arithmetic and
score checks do not depend on reproducing those trajectories. The C engine
uses little-endian IEEE float32 model files and a model path without whitespace.

The original batch runners remain unchanged so their recorded hashes stay
valid. [`collect_results.py`](collect_results.py) assembles completed runtime
records and checks the improving-checkpoint logs before archiving their
hashes and counts; it refuses incomplete campaigns. Full runtime checkpoint
logs are not required for the offline arithmetic verifier.

### Audit the original runtime logs from the delivery ZIP

[`audit_original_logs.py`](audit_original_logs.py) separately checks the original
102 JSONL logs and their complete result sidecars against the frozen records.
It needs only the Python standard library. It independently re-encrypts every
logged incumbent, checks supplied square anchors, verifies both original binary
and source identities, and checks the instrumented counter arithmetic. It reads
the binaries without executing them and does not repeat any search.

From the extracted `adfgvx-cipher/` directory, run this exact command:

```sh
python experiments/p170_new_methods/audit_original_logs.py \
  --cross-period-logs reproduction-assets/p170-book-run \
  --radio-rank-logs reproduction-assets/p170-matched-rank-controls \
  --radio-historical-logs reproduction-assets/p170-radio-historical \
  --original-engine reproduction-assets/p170-engines/anchored_joint \
  --counted-engine reproduction-assets/p170-engines/counted_anchored_joint \
  --output /tmp/p170-original-log-audit.json
```

All five asset paths and the report path are explicit CLI arguments, so another
layout can use the same script. Repository inputs derive from the script's
location, and their frozen SHA-256 values are checked without requiring Git.
The report's `repository_commit` is optional metadata and may be null outside
a checkout; `--source-commit` can supply a known commit label. No original
workspace path is required. A mismatch produces a nonzero exit status and a
JSON failure report.

The original-asset audit checks **102 final incumbents, 102 entire sidecars and
761 logged incumbents**. Only **90 logs** have pre-existing SHA-256 pins in the
committed `runtime_log_inventory`. The other **12 radio-rank control logs** were
first hashed in the final original-log audit; their final states and complete
sidecars match the frozen records, but this does not create an earlier hash
inventory retrospectively.

The **40 instrumented sidecars** contain **3,902,267,094 fitness calls**, including
**601,058,006 book-objective calls** and **3,301,209,088 radio-mixture calls**.
Those counters were captured from the engine's stderr after successful
completion. The separate original stderr bytes were not retained; this audit
checks the preserved parsed counters and their arithmetic, without independently
recounting those historical calls. JSONL files contain improving candidates,
not terminal counters. The **7,000,000,000 slots** for the **62 uninstrumented
book jobs** remain configured loop slots, not measured fitness calls or counts
of distinct states. These limits remain explicit in every audit report.

## Attribution audit

The separate [Lasry paper audit](lasry_attribution_audit.md) and its
[machine-readable table](lasry_attribution_audit.json) identify earlier body
readings, header examples and key-only references. They are a frozen snapshot
made before the resulting catalog-credit corrections, not a report of the
current catalog's omissions. An absent explicit body reference does not
establish first-publication priority for a new source edition.
