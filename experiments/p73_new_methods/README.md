# p73: source reuse, word scoring and substitution-invariant retrieval

**p73 still has no accepted plaintext.** This package makes three additional
methods reproducible: broader reuse of published square components, fixed-rank
recovery of a completely hidden square using a word objective, and retrieval of
possibly re-encrypted source texts through an optimal substitution assignment.
The fresh controls show why none of the resulting language-ranked strings is
promoted to a reading.

Prepared by **icekylinx and GPT-6 Astra Pro**. The positive source editions
recovered alongside this work are in the
[October Caucasus package](../october_caucasus/README.md) and the
[October staffing package](../october_staffing/README.md), with further
[source records from pp62–65](../october_requests/README.md). Those editions use an
earlier published key and retain the earlier Childs, Lasry, and
Lasry–Niebel–Kopal–Wacker credits. These method experiments do not establish a
new connection between their key and p73.

## Inputs and completed work

The historical target is the unchanged **178-slot p73 source frame**, with
**176 received coordinates and two erasures**. The header's 26 October /
8 November conflict remains unresolved. [inputs.json](inputs.json) snapshots the
target and 25 catalogued rank orders. This catalogue includes historical,
recovered and illustrative entries; it is not 25 independently dated historical
period keys. Complementing every rank, `r -> width+1-r`, supplies the reversed
column-readout hypothesis. All 50 resulting rank orders are distinct.

[completed_runs.json](completed_runs.json) is the authoritative ledger of
**completed** runs and counters. Each result suite contains its actual seeds,
inputs or input references, proposed square/ranks, source-compatible character
domains, budget and runtime. The ledger is updated only after a run finishes.
Runtime sums overlap where separate processes ran concurrently.

The final snapshot contains **255 completed new runs**, including all 50 blind
rank hypotheses and all 50 staged follow-ups. Their fixed-rank square-search
engines emitted **1,333,005,000 measured mutation proposals**. The configured slots of
the separate anchored-engine runs are not added to that measured count.

For the fixed-rank square-search engines, `best.proposals` is the counter at
discovery of the best candidate. It can be zero for a retained warm start even after a full
search. The separately stored `completed_proposals` comes from the **final
emitted row**; compressed original logs allow that count to be audited.
The verifier's legacy JSON field
`completed_fixed_square_proposals_checked_against_final_logs` follows the
`fixed_square*.cpp` filenames; it does not mean that the true square was supplied.
The older anchored engine exposes configured restart/iteration budgets instead
of an actual mutation counter, so its products are called **proposal slots**.

[prior_scope_inventory.json](prior_scope_inventory.json) separately preserves
35 earlier completed p73 square-reuse jobs: five nearby square families at
widths 16–22. Their original records and logs are compressed in the package.
The shared anchored-search README retains an earlier 2-of-70 snapshot across
two targets; it should not be read as the final runtime inventory. These 35
earlier p73 jobs are checked for source compatibility and excluded from every
new-campaign counter below.

## 1. Additional square-component and spacing searches

The expanded screen adds the complete **Nov19–21, Nov25–28 and Oct4–6 squares**
with arbitrary ranks at widths 16–24. These 27 settings completed 1,000 restarts
of 100,000 proposal slots each. The earlier 40-setting exploratory screen also
contains width 15 and the **partial** Aug8–9 square; the latter leaves its
unpublished cells free and must not be called a completely frozen square.

Six fresh controls use the correct frozen square, a random hidden rank order,
two adjacent erased source coordinates, and 89-character excerpts from the new
p70 source editions. They are synthetic re-encryption controls, not historical
attributions of those texts to the test keys.

| Square | Width 16 | Width 24 |
| --- | --- | --- |
| Nov19–21 | Exact ranks; 87/87 raw fixed letters | Exact ranks; 87/87 raw fixed letters |
| Nov25–28 | Exact ranks; 87/87 raw fixed letters | Failed; 2/87 raw fixed letters |
| Oct4–6 | Exact ranks; 87/87 raw fixed letters | Exact ranks; 87/87 raw fixed letters |

The 5/6 recovery rate is evidence of useful search capability and an explicit
failure of uniform coverage. The p73 results are diagnostic candidates only.

Two further language models keep the same ten pinned German books but use
only joined text or only `X` between words. The 54 p73 settings use these two
models, the same three complete squares and widths 16–24, at 200 restarts of
50,000 slots. Matched spacing-specific controls recover 3/4 hidden rank orders:
joined-text width 24 fails at 13/87 fixed letters; joined-text width 16 and both
word-`X` controls recover 87/87. Model provenance and source hashes are retained
under [models](models).

## 2. A word objective with all 36 square cells hidden

The fixed-rank engine searches a complete permutation of the 36 plaintext
symbols and the two source erasure fills. Every observed coordinate is
preserved. There are no plaintext anchors. An arbitrary proposed square
necessarily yields some source-compatible text, so re-encryption is an
arithmetic check, not authentication of a historical square.

The language objective combines the book quadgram sum with twice
a trie-based word-segmentation score. Word-pair association bonuses are capped.
The exact lexicon builder and provenance are shared with
[p198_word_search](../p198_word_search). Both objectives use the **same ten
books**; they are not independent language models. No p73 candidate or control
text trains the original book or word model.

Three fresh controls use correct fixed ranks, a random hidden full square,
two known-position source erasures and 89-character source-edition excerpts.
The two blind methods each receive 120 seconds. The staged column receives an
**additional** 120 seconds starting from the quad-only result; it is not an
equal 120-second comparison.

| Control source | Quad only | Blind quad + word | Quad, then word |
| --- | ---: | ---: | ---: |
| p70 A1 |70/89 |81/89 |81/89 |
| p70 A2 |85/89 |24/89 |88/89 |
| p72 B |73/89 |84/89 |84/89 |

The p70 A2 blind word failure is an optimizer failure: a much better compatible
basin already exists. The staged result repairs nearly all of it. Its remaining
initial `M -> 5` is an **objective failure**: the fallback treatment of a lone
digit gives the wrong character exactly two score units over the true `M` at
weight 2. The p70 A1 and p72 B wrong candidates also outscore their true texts.
The model can recover ordinary wording while preferring wrong names,
abbreviations or numerals. Some excerpts end mid-word, which is retained as
part of the recorded control protocol.

The completed historical blind suite gives each rank hypothesis 120 seconds.
The completed staged suite gives 60 seconds from the best available compatible
seed: archived
quad-only candidates, with all 36 erasure-fill pairs enumerated, and any already
completed blind word candidate. Each result records exactly which seed was
used. The old and current p73 source strings were checked identical before an
archived seed was admitted. Availability of a blind result at the time of a
staged run is recorded rather than retroactively changed.

## 3. Frozen radio-domain objective: a limited follow-up

The team's [radio-domain model](../radio_domain_model) is a frozen 50:50
probability mixture of book quadgrams and source-edition radio quadgrams, with
uniform digit expansion in the radio component. This package neither retrains
nor tunes that mixture.

The first retrospective objective audit reused the three earlier p70/p72
controls. Their source families occur in the new training data, so that audit
is **not held-out validation**. It improves the ranking of several earlier
truths, but still prefers the wrong older p72 B candidate to the true text.

Two fresh 85-character controls instead use whole held-out source families,
random hidden squares, correct fixed ranks and two adjacent erasures. Book and
radio runs have identical seeds and 120-second budgets. These source families
also appear in other team calibration suites; the tests are different cipher
conditions, not independent historical samples.

| Held-out source | Book | Radio mixture | Radio score: truth / selected candidate |
| --- | ---: | ---: | --- |
| p84 B, shipping inquiry |80/85 |76/85 |−361.508 /−352.093 |
| p92 A, Dutch courier |78/85 |78/85 |−348.463 /−343.851 |

Higher score is better. Both selected wrong strings beat the truth under the
radio objective. Therefore this calibration establishes no general advantage
for fully unknown-square p73 recovery. A limited four-rank application
(Oct4–6, Oct28–31, Nov7–9, and the recovered CHI-Nov8 rank order) completed
120 seconds per setting from compatible seeds. It supplied no accepted text;
no further model tuning follows from those outputs.

### A separate fixed-square, hidden-rank check

The later p170 calibration showed a benefit in a different regime, where the
complete true square was supplied. That motivated a narrow additional p73
branch using the same frozen radio model. Its protocol and gate were fixed
before its controls ran, in
[radio_rank_protocol.json](results/radio_rank_protocol.json).

Two 89-character controls use whole held-out source families, a supplied
complete square, random hidden ranks, and erased source positions 1 and 2.
They reuse source families seen in other calibration regimes; the new cipher
realizations are not independent historical samples. Each book/radio run gets
the same seed and **1,000 restarts × 100,000 proposal slots**, with no warm start.

| Control | Supplied square / width | Book | Radio mixture |
| --- | --- | --- | --- |
| p84 B, shipping inquiry | Oct4–6 / 22 | Exact ranks; 87/87 fixed positions | Exact ranks; 87/87 fixed positions |
| p92 A, Dutch courier | Nov25–28 / 23 | Exact ranks; 87/87 fixed positions | Exact ranks; 87/87 fixed positions |

The gate required both radio controls to recover the true ranks and all fixed
positions, retain the truth in every erasure domain, and have no lower total
accuracy than book. It passed. This establishes search capability on these
two controls; it does not establish a radio advantage over book here.

Only three predeclared historical square/native-width hypotheses followed:
**Oct4–6 / 22, Nov19–21 / 20, and Nov25–28 / 23**, at the same per-setting
budget. All three finished and supplied no accepted text. The
[gate record](results/radio_rank_gate.json),
[matched controls](results/radio_rank_controls.json), and
[historical results](results/radio_rank_p73.json) preserve the exact inputs,
seeds, source-compatible domains, models and configured slot budgets. These
are additional finite experiments, not exclusions of other ranks, widths,
squares or source layouts.

## 4. Find re-encrypted copies while allowing corruption

The retrieval engine does not need a known square. For a fixed rank order it
compares the resulting cell-label pattern with corpus plaintext at **every
relative offset having at least 60 known overlapping positions**. For each
alignment it builds a 36-by-36 contingency matrix and finds the exact
maximum-weight bijection. That yields the minimum number of plaintext
substitutions for that alignment. Missing coordinates remain wildcards;
insertions and deletions are outside this retrieval model.

The snapshotted corpus has 476 distinct strings: OCR-derived candidates plus
raw and editorial fields from explicitly selected source-edition packages.
Their provenance remains attached, including editorial assumptions. An
editorial corpus string is a retrieval hypothesis, not an independent witness.
Open-challenge language candidates are not corpus entries.

A final [source-snapshot audit](results/retrieval_provenance_audit.json)
records a provenance limitation: two earlier naval package files were edited
in place before their full JSON bytes were retained. Their original file-level
hashes therefore cannot be rechecked from the delivered snapshots. All 25
selected naval field references still match the current source edition exactly,
and their complete text remains frozen in `retrieval_inputs.json`, so retrieval
replay is intact. The earlier Tiflis input and certificate bytes are recoverable
exactly and identified separately. No missing original bytes or hashes were
silently reconstructed or replaced.

The experiment includes 50 p73 rank hypotheses, one frequency-preserving
shuffle of each, and two positive queries with five deliberately altered
positions. It produces 47,819 best query/corpus alignments.

| Query group | Best recorded agreement | Meaning |
| --- | --- | --- |
| p73 rank hypotheses |31/62 = 50.00% | No plausible duplicate identified |
| Frequency-preserving shuffles |32/63 = 50.79% | Finite comparison, not a p-value |
| p80/p81 positive family |85/89 on a full known match | Correct family retrieved despite imposed errors |
| p205 positive family |84/89 | Correct text retrieved despite imposed errors |

The p80/p81 family also has a partial raw match at 83/86, a higher fraction
because of its erasures. Five changed query characters do not necessarily
force five disagreements under a free bijection: a changed symbol occurring
only once can be absorbed by another assignment. The control therefore checks
retrieval of the right source family rather than an assumed error count.

The Python verifier independently solves **all 47,819 reported assignments**
with SciPy's assignment implementation and checks the group maxima. An
optional deterministic replay repeats the full C++ offset search. The shuffled
sample is finite and frequency-preserving only; it is not a significance test
or an exclusion of other keys, corpora, layouts or cipher conventions.

## 5. Profile pairing and new arbitrary ranks: 3 November follow-up

The [compact follow-up](followup_20261103/README.md) adds 1,232 source
segmentations, 57 private-square/pair-order fits, and 94,795 exact donor
comparison optima. Four related hidden-key controls admit complete global
square witnesses with zero changes to all 176 observed coordinates, while
the literal square estimates still confuse letters. No p73 reading is accepted.

Its standard-library verifier checks the source/control witnesses and 41
donor leaders; optional replay checks the complete donor screen. The stochastic
search used a different, unbundled scratch model whose build provenance was
not retained. The follow-up states that reproduction limit explicitly.

## Reproduce and verify

From the repository root:

```sh
python experiments/p73_new_methods/verify.py
python experiments/p73_new_methods/verify.py --recompute-retrieval
```

The first command independently checks every archived source-coordinate
witness, control accuracy, final proposal counter, source identity and
reported substitution assignment. The second also reruns every retrieval
offset. Neither command authenticates a language-ranked historical candidate.

For a standard-library-only check, including Python 3.10:

```sh
python experiments/p73_new_methods/verify.py --skip-assignment
```

This keeps source witnesses, controls, final counters, prior-run records,
retrieval inputs and overlap counts checked, while explicitly reporting zero
independently recomputed assignment optima. The full default check additionally
needs NumPy and SciPy, pinned in the root [REQUIREMENTS.txt](../../REQUIREMENTS.txt).
CI runs the standard-library mode on Python 3.10 and 3.13 and the full
assignment check on 3.13. `--recompute-retrieval` also needs a C++17 compiler.

Measured local timings and the exact checked snapshot are recorded in
[ci_runtime_observation.json](results/ci_runtime_observation.json). These
measurements were taken during concurrent research processes on Python 3.12;
they are observations, not a guarantee for other machines.

Rebuild the pinned book and word models using their shared packages. The two
spacing variants can be regenerated with:

```sh
python experiments/p73_new_methods/build_spacing_models.py \
  --cache /path/to/pinned-books --output /path/to/spacing-models
```

Replay a completed stochastic setting by its `run_id`, for example:

```sh
python experiments/p73_new_methods/reproduce.py \
  --suite word_blind --run Nov7-9 \
  --quad /path/to/german_military36_quad.bin \
  --lexicon /path/to/lexicon.txt --output /tmp/p73-replay.json
```

Model hashes are checked before replay. Optional budget overrides are recorded
by the resulting run. Six tiny explicit-budget
[interface checks](results/replay_interface_checks.json) cover the blind,
warm-start and frozen-square engines, including separate book and radio model
selection. They are excluded from the campaign ledger. Runtime-limited searches
may complete different numbers
of proposals on different machines even with the same seed; deterministic
verification of the archived witnesses does not have that limitation. The
source code, full final logs and complete retrieval inputs are retained;
compiled binaries and large learned tables are reproducible external files.
