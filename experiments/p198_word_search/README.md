# Word structure and joint five-loss search for p198

**p198 D remains open.** The new method jointly searches five missing source
coordinates, their values, and any unassigned square cells under a fixed
column order. Its language score adds explicit word segmentation and adjacent
word association to the existing book quadgrams. It recovers several planted
texts, but also prefers wrong numerical fields and wording to the truth.
None of its historical candidates is an accepted reading.

Prepared by **icekylinx and GPT-6 Astra Pro**. Historical keys and prior
recoveries retain their authorship in the key catalogue. The arbitrary full
squares in this package are source-compatible search states, not newly
identified historical keys.

## Source and search model

The historical input is exactly the 165-coordinate p198 D transcription in
[`data/messages.json`](../../data/messages.json). Every search preserves every
received coordinate in order, inserts exactly five coordinates, and therefore
models an 85-character plaintext. Loss positions range over all 170 full-frame
positions; no source coordinate is silently substituted or deleted. This is
a conditional five-loss model, not a proof of the original message length.

The recorded column order stays fixed within a job. Published square anchors
stay fixed; free cells form a permutation of the unused letters and digits.
The fully hidden-square branch retains the selected column order but hides
all 36 square cells. The late-key ordinary-letter variants deliberately mask
the raw numerical and rare-letter labels; their exact partial squares and
scope are recorded per job rather than merged into the published keys.

The engine uses simulated annealing with square swaps, coordinate-value
changes and loss-position moves. Most later restarts perturb the current best
state; other restarts begin anew. The experiment is finite and stochastic.
It does not repeat or replace the earlier exact fixed-key optimizations.

## The word objective

Ten hash-pinned public German books supply **1,091,203 weighted word tokens**
and **53,465 distinct words**. The six general-language books have weight 1;
the four wartime-history/memoir books have weight 2. The builder transliterates
umlauts and sharp s, extracts words of at most 32 letters, and records adjacent
word pairs within sentence/line boundaries. Pairs with weighted count at least 2
receive a nonnegative association bonus capped at 2.

A dynamic program finds the highest-scoring segmentation of a candidate.
Its word terms are base-10 unigram log frequencies. Adjacent recognized words
receive 0.65 times the capped association bonus. A single-character fallback
costs −3, except `X` costs −0.25; digit runs of length 1–10 cost −1 minus their
length. Fallbacks keep genuine garbles and unknown words feasible. They also
create identifiable failure modes, such as a lone digit sometimes beating
a true uncommon initial.

The combined score is the quadgram sum plus a selected weight times this
segmentation score. It is **not a calibrated probability**. The word and
quadgram components use the **same ten books**; agreement between them is
not independent language evidence. No attacked ciphertext, candidate or
control truth trains this original model.

The first pilot uses weight 1.5. Weight 2 was chosen adaptively after the old
Nov13b diagnostic still preferred `STAR`/`BETTE` to `STAB`/`BITTE`. The older
controls and their failures remain in the ledger; rerunning them at weight 2
does not make them fresh validation. The four later published-anchor control
bodies were fixed after that selection.

## Controls, with what the optimizer actually knows

All controls have 85 characters and five scattered missing coordinates.
Correct plaintext, losses and fills are evaluation-only. The two old diagnostic
runs start from an earlier quadgram optimum, **never from control truth**.
Their full seed states and reconstructed seed texts are preserved. Other
controls begin blindly.

| Control family | Square information | Budget per run | Correct characters |
|---|---|---:|---|
| Old diagnostic at weight 1.5, two keys | Full true square supplied; old quad optimum as seed | 300s | 85, 83 |
| Four new bodies at weight 1.5 | Full true square supplied | 600s | 81, 85, 85, 85 |
| Same old diagnostic at weight 2 | Same full squares and seed origins | 300s | 85, 84 |
| Same four bodies at weight 2 | Full true square supplied | 900s | 81, 85, 85, 85 |
| Four later bodies at weight 2 | Published anchors: one complete square and three partial squares | 900s | 85, 82, 85, 85 |
| Two of those later bodies, all cells hidden | No square anchors; correct ranks retained | 900s | 11, 85 |

These are **18 run-level observations on nine distinct plaintext bodies**,
with repeated keys/texts and adaptive reuse. They are not 18 independent
validation samples. Twelve runs recover the full text. An independent Python
score review classifies five failures as **wrong incumbent outranks truth**
and one as **search failed to reach the better truth**.

The published-anchor numerical control is especially clear: its 82/85 result
recovers the wording while changing company 3 to 2, day 17 to 18 and time 0800 to 0300.
Those changes are globally consistent with a different square completion and
score better under the model. A successful source roundtrip therefore cannot
identify those numbers. The fully hidden-square failure recovers only 11/85
characters despite a superior true score; it demonstrates search incompleteness
in that harder regime.

[`objective_review.json`](objective_review.json) records the independently
recomputed true/candidate scores, class agreement and diagnosis for every
control. [`records.json`](records.json) contains the complete inputs,
evaluation-only truths, selected and final events, and original log hashes.

## Historical scope and completed counters

The completed campaign contains **49 jobs: 18 control runs and 31 historical
searches**, with **zero pending jobs**. The initial pilot tests the CHI-Nov13
and Nov13b partial-square
hypotheses for 2,400 seconds each. The adaptive branch repeats them for 3,600
seconds and tests both with all square cells hidden for 5,400 seconds. The
broader branch tests 25 additional recorded-key or explicitly masked variants
for 1,200 seconds each. These catalogued keys include instructional and later
recovered examples; their inclusion is a comparison, not historical dating
evidence for p198.

The final ledger records **2,055,765,000 completed mutation proposals**.
It distinguishes **declared**, **completed** and **pending** cases. Collection
admits a result only after its process exits
successfully and writes a completion record. An in-progress best candidate
never counts as a completed job. The final event supplies actual completed
mutation proposals and restart counts; the earlier event at which the best
candidate was discovered is retained separately.

One mutation proposal may leave the state unchanged, and the engine also
evaluates initial states and output checkpoints. Proposal counts are neither
distinct-key counts nor all fitness calls. Wall-clock budgets mean a different
machine may complete a different number of proposals with the same seed.
The ledger and verifier report the exact completed total without projecting
unfinished budgets. No historical plaintext is accepted.

The separate [radio-domain package](../radio_domain_model/README.md) tests
source-derived language statistics, digit-class scoring and the conditional
FX=Y hypothesis. Its calls and controls have separate counters and cannot be
added as independent validation samples when they reuse a text family.

## Verify and reproduce

The default verifier uses only Python's standard library. It independently
constructs the column transposition, checks injective square completion,
reencrypts every candidate and truth, and verifies that removing only the
recorded losses recovers the exact received input.

```sh
python experiments/p198_word_search/verify.py
python experiments/p198_word_search/verify.py \
  --quad /path/to/german_military36_quad.bin --lexicon /path/to/lexicon.txt
python experiments/p198_word_search/score_review.py --check \
  --quad /path/to/german_military36_quad.bin --lexicon /path/to/lexicon.txt
```

Rebuild the word data from the ten hash-pinned book files. The builder checks
the resulting lexicon against its frozen SHA-256:

```sh
python experiments/p198_word_search/build_lexicon.py \
  --cache /path/to/pinned-books --output /tmp/word-model
g++ -O3 -std=c++17 experiments/p198_word_search/word_loss.cpp -o /tmp/word-loss
python experiments/p198_word_search/run_case.py \
  --case broad_partial/control_partial_1_Nov13-15b \
  --engine /tmp/word-loss --quad /path/to/german_military36_quad.bin \
  --lexicon /tmp/word-model/lexicon.txt --output /tmp/word-replay
```

Use the validated Python runner for external inputs to this frozen experimental
engine. It checks rank permutations, unique fixed square labels, coordinate
alphabet and model identity before launching. The engine source is preserved
exactly as run, with a separate source hash; later interface validation does
not retroactively change that provenance.

The [independent implementation audit](../radio_domain_model/independent/README.md)
uses backward memoized substring segmentation instead of the engine's forward
trie dynamic program, checks original completion logs and binary identity,
and rebuilds the radio/class tables separately. It preserves its original
30-case snapshot so a later expanded ledger cannot silently replace an audit
that covered fewer completed runs.
