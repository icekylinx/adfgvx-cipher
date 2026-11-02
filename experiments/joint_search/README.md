# Joint ADFGVX search: page 153

Authors: **icekylinx and GPT-6 Astra Pro**.

This small research suite attacks the two page 153 fragments jointly, with an
unknown substitution square and transposition. It records bounded searches,
positive controls, and failures. **A substantial partial reading of page 153
has now been recovered.** The [companion recovery package](../p153_recovery/README.md)
records the shared 18-column transposition, conservative 19-letter square,
remaining numeral ambiguity, and two explicit printed-coordinate anomalies.
It does not claim a complete solution or a complete historical square.
The received lengths are 132 and 108 coordinates, with 15 erased coordinates in
the second part. Source audit dates the intercept to November 8, 1918. A shared
key between the two parts is an attack hypothesis.

The code uses C11 with GCC/Clang builtins, plus Python 3.10+. GCC or Clang and `make` build the
solvers. NumPy is required only when rebuilding the large language models.
The package includes small profile/monogram statistics and source provenance;
it omits model binaries, downloaded books, executables and large candidate logs.

```sh
make
make check
python3 tools/build_models.py --cache work/corpus --output models
```

The builder verifies every downloaded book against its recorded SHA-256 before
training. If a source has changed, supply the recorded source version in the
cache. Model binaries are rebuilt deterministically and checked against the
published hashes. No attacked message, control plaintext, candidate or solved
1918 traffic enters these independent models. General German books have
weight 1; four wartime German books have weight 2. This domain adaptation was
motivated by control failures and is disclosed as an adaptive choice.

## Reproduce the segmentation stages

All ranks are **one-based transmission ranks indexed by physical column**.
All character positions and candidate ranks are zero-based. Ciphertext `?`
means exactly one erased coordinate; it is never an omitted-length gap.

For width 16, the column-height classes across the two messages are `(9,7)`,
`(8,7)` and `(8,6)`, with 4, 8 and 4 columns. There are 900,900 length-class
segmentations. The first command visits all of them and exactly optimizes two
additive matching surrogates. It retains 20,000 candidates from each ranking.

```sh
mkdir -p work
bin/segmentation_rank models/military_monograms.txt cases/p153_k16.in 20000 > work/ranking.jsonl
python3 tools/prepare_segments.py --ranking work/ranking.jsonl --output work/retained.segments
bin/segmentation_profile_batch models/profile.txt cases/p153_k16.in work/retained.segments 16 5 2000 2026110281 > work/pairings.jsonl
```

The two surrogates are a relaxed independent-letter upper bound and a
heuristic collision excess. The bound applies only to its IID relaxation,
which allows a separate square per pair and independently relaxed missing
coordinates. It does not bound a full language score. The collision statistic
is not a p-value. Neither surrogate enforces global square consistency.

The profile stage searches column pairings and orientations inside each fixed
segmentation. Its 5 restarts of 2000 proposals are stochastic. Every restart
randomizes the within-class assignments. Pair order is deferred.
An optional final argument `1` emits each restart's best pairing, allowing
distinct pairing basins to be retained instead of only one global winner.

To eliminate the surrogate-retention cutoff, generate all segmentations
directly. This still does not exhaust every pairing, ordering or square:

```sh
python3 tools/prepare_segments.py --all-width 16 --output work/all16.segments
bin/segmentation_profile_batch models/profile.txt cases/p153_k16.in work/all16.segments 16 5 2000 2026110297 > work/all16_pairings.jsonl
python3 tools/prepare_segments.py --all-width 18 --output work/all18.segments
bin/segmentation_profile_batch models/profile.txt cases/p153_k16.in work/all18.segments 18 10 5000 2026110293 > work/all18_pairings.jsonl
```

Width 18 has 18,564 segmentations: 6 columns of height `(8,6)` and 12 of `(7,6)`.
The same ciphertext input is valid; its final evaluation-mask line is ignored
by `segmentation_profile_batch`.

Width 14 has 210,210 segmentations. Its classes `(10,8)`, `(9,8)` and `(9,7)`
contain 6, 4 and 4 columns. The complete pass uses the same bounded pairing
budget as width 16:

```sh
python3 tools/prepare_segments.py --all-width 14 --output work/all14.segments
bin/segmentation_profile_batch models/profile.txt cases/p153_k16.in work/all14.segments 14 5 2000 2026110313 > work/all14_pairings.jsonl
```

## Fit a square and resolve pair order

```sh
python3 tools/refine_candidate.py --case p153 --candidates work/pairings.jsonl --rank 0 --models models --output work/refined.json
```

The helper selects a profile candidate, fits an unknown square, then jointly
optimizes square, pair order and pair orientations. It finishes with a
fixed-transposition exact-coordinate refinement: every half-erased digraph
permits precisely six square cells, and every fully erased digraph permits 36.
Four- and six-gram windows never cross message boundaries. The mixed score is
a composite language objective; it is not a posterior or a plaintext proof.

The optional `--component-columns` step sits between pair fitting and exact
coordinate refinement. It allows individual columns to move within the same
height class, using the pair-stage square as a warm start.
This can repair a wrong pairing while preserving the declared segmentation.
It uses 100 restarts of 100,000 proposals by default, followed by the same exact
coordinate refinement:

```sh
python3 tools/refine_candidate.py --case p153 --candidates work/all18_pairings.jsonl --rank 0 --component-columns --models models --output work/component_refined.json
```

Control keys and plaintexts in `cases/cases.json` are used only after fitting
for evaluation and reencryption. A high-scoring historical string is never
promoted to a decryption certificate by this helper.
The separate segmentation-ranking diagnostic receives the control's true
length-class masks solely to report their ranks. Those masks do not affect
candidate enumeration, scoring, retention or the subsequent fit.

## Solver input formats

| Program | Input |
| --- | --- |
| `segmentation_rank` | Arguments: monogram text file, ciphertext input, retained count. The input file contains two ciphertext strings followed by two evaluation masks for the four longest and four shortest K16 columns; use `0 0` for a historical target. |
| `segmentation_profile_batch` | Arguments: profile text, ciphertext input, segments file, even width, restarts, iterations, seed, optional emit-restarts flag. Segments file: count, then one row per segmentation with two long-column masks and the width's column ranks. |
| `subsolve_marginal` | Arguments: 37^4 float32 model, cell stream, restarts, iterations, seed, optional square. Cell indices 0..35 are encoded as `A..Z0..9`; `?` is unknown and `\|` is a message boundary. |
| `pair_marginal` | Standard input: model path, even width, restarts, iterations, seed, message count; then a 36-character initial square or 36 question marks; ranks; ciphertexts. Pair identities are fixed, while order, orientation and square may change. |
| `joint_rectangle_warm` | Same header and complete-square convention as `pair_marginal`. Individual component columns may move within a shared height class; the length-class segmentation remains fixed. |
| `anchored_joint` | Same header, followed by a 36-cell partial square, ranks or all-zero ranks, and ciphertexts. Known square cells remain fixed. |
| `joint_domain_subsolve6` | Arguments: 36^4 quad model, sparse six-gram model, six-gram weight, already-untransposed coordinate streams separated by `\|`, restarts, iterations, seed, optional complete square. |
| `pair_order_rank` | Arguments: profile text, two-message/pairing input, retained count, optional second-message pair-column offset. Input: two 132/108-coordinate ciphertexts and 18 ranks describing a fixed pairing. Enumerates every compatible pair order and relative orientation; it does not fit a square. |

Every ciphertext message must have even length. A separate explicit error
model is required for odd input. Square letters use `A..Z0..9`, with `?` only
for declared unknown cells. A complete square is injective.
Binary model readers assume a little-endian host with 32-bit IEEE floats.
Model paths in standard-input headers must not contain whitespace.

The CHI anchor example is in `cases/p153_anchored_k16.in`. Its 22 fixed cells
come from the independently audited November 13 CHI solution. **Reuse on
November 8 is only a secondary hypothesis**; this anchored search is not a
source-established constraint on the target.

```sh
bin/anchored_joint < cases/p153_anchored_k16.in > work/anchored.jsonl
```

## Engine versions and archived traces

The canonical engines reject malformed supplied squares and nonpositive
budgets, and record each initial state before attempting a proposal. These
checks fix concrete issues found during independent review. A substitution
seed may contain `?` placeholders; they are completed for initialization and
are not immutable anchors. The pair solver accepts a complete square or
exactly 36 question marks. The exact-coordinate solver requires a complete
optional square.

The earlier fixed-pair search traces use the archived engine version recorded
in `repro/archived_engine_manifest.json`. Recording an initial
incumbent can alter subsequent stochastic trajectories, so the corrected
engines are not claimed to reproduce every older best-score line byte for
byte. `repro/restore_archived_engines.patch` restores the four archived source
snapshots inside a separate copy; all four restored source hashes were checked.
The supplied reencryption certificates can be verified independently of any
optimizer replay.
The later `joint_rectangle_warm` experiment uses a separate corrected engine;
its source hash is recorded with its calibration results. It does not overwrite
the earlier component-column or fixed-pair search traces.

## What the controls establish

At the specified width 16, the surrogate rankings followed by profile and
language fitting recover all 105 fully observed plaintext characters in both
same-length controls. Their true segmentations rank 0 and 4 after the profile
stage. No true segmentation, pairing or square is used to generate or score
the attack candidates; the supplied diagnostic masks only measure recall.
The original control reencrypts all 225 received coordinates with an equivalent
globally transposed square. The fresh wildcard-stage control fails one
surviving coordinate even though all 105 fully observed letters are correct;
that failure remains in `results/control_certificates.json`. Exact-domain
refinements are separate records: both now reencrypt all 225 observed coordinates
correctly. Their keys and plaintexts were used only for this final evaluation.
Unobserved square cells and erased ciphertext coordinates remain undetermined.
The exact-refinement wrapper now chooses the highest objective among all ten
control candidates. `results/control_selection_audit.json` verifies that this
selects the same archived inputs as an earlier redundant success filter; no
control outcome or optimizer input changed when that filter was removed.

At width 18, both control segmentations rank first across all 18,564 choices.
One best pairing contains all 9 true pairs, while the other contains 7/9 because
a false pairing scores better. Segmentation recall and plaintext recovery must
therefore be reported separately. Retaining twenty distinct pairings per
segmentation includes both true pairings, yet the fixed-pair language stage
still fails both controls. Their true plaintexts score above the false search
incumbents, demonstrating an optimizer failure under this objective.

The subsequent full component-column warm stage recovers all 105 fully observed
letters in both controls. The original already matches all 225 coordinates;
the fresh wildcard candidate has a surviving-coordinate mismatch at position
102 of part 2. Exact-coordinate refinement preserves that fresh-control failure:
the K in `FUNKSTELLE` is only partly observed, and the language objective weakly
prefers another column for K. A separate diagnostic enumerates all placements
of K among cells unused by fully observed letters. Two placements satisfy the
complete control, but their slightly lower scores are not a blind recovery.
This limitation is retained in `results/fresh_k18_half_coordinate_diagnostic.json`.

```sh
python3 tools/diagnose_half_coordinate.py --models models --output work/half_coordinate_diagnostic.json
```

The bounded historical component-column follow-up is motivated by recovery of
both transpositions and all fully observed characters, with the remaining
half-coordinate failure explicitly retained. It does not rely on a claim of
complete control recovery. Calibration and follow-up scope are recorded in
`results/component_column_calibration.json`.
All twenty candidates per control receive the same budget, and the final
candidate is selected by objective without consulting control truth.

At width 14, the control segmentations rank 4 and 1 among all 210,210 choices,
with every true unordered pair recovered in both. The bounded top-ten language
fits recover both controls and reencrypt all 225 observed coordinates. The
successful candidates also have the highest objective in their respective
shortlists. These tests reuse the same two calibration texts with new withheld
keys; they are not an unbiased sample of historical radiograms.

One further diagnostic enumerates all 256 relative pair orientations and 4320
compatible orders for a fixed K18 pairing: 1,105,920 choices. It ranks cell
bigram coincidence, trigram coincidence, and a profile composite. Even with
the correct pairing, the original control's true key falls below the top 2000
in every ranking. The fresh oracle-pairing control ranks 1259 by bigram
coincidence and 589 by the profile composite. This pruning method was therefore
not expanded into a historical search. Its explicit negative result is in
`results/pair_order_diagnostic.json`.

```sh
bin/pair_order_rank models/profile.txt cases/pair_order_original_control.in 2000 > work/order_diagnostic.jsonl
```

`results/summary.json` and `results/language_stages.json` record completed budgets
and current outcomes. Proposal counts include no-op proposals and are not CPU
time measurements.
`results/segmentation16_ranking.json` and `results/segmentation18.json` give
exact ranking and scope details. The source and algorithm notes in
`PROVENANCE.md` separate prior art from this implementation.
