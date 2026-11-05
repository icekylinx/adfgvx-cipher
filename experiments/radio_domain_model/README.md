# A frozen radio-language model, with family-held-out controls

**A radio-specific objective helps one tested rank-search regime, but does
not reliably fix the short damaged-message regime.** This package supplies
the source-derived training snapshots, exact model construction and matched
controls needed to distinguish those results. No open-challenge candidate
trains the model, and no candidate from it is an accepted historical reading.

Prepared by **icekylinx and GPT-6 Astra Pro**. Source texts retain the prior
body and key credits in their original edition packages. Training material
includes explicitly costed editorial readings; it is not a collection of
independently proved transmitted plaintexts.

## 1. Freeze the families before testing the mixture

The first [dataset](dataset.json) has **45 training strings**, containing
5,045 characters including retained uncertainty markers and **4,634 usable
quadgrams**. A `?` ends a training span: no quadgram bridges it. The builder
excludes the entire six held-out message families, duplicate training strings,
additional exact 32-character overlaps, heavily damaged p68 procurement
readings, and late keys whose numerical labels have separate qualifications.

The six test families are the Dutch courier, oil/shipping inquiry, Mackensen
relay request, Polish appointment, crown finance, and Filittis permission.
Each synthetic loss control takes an 85-character known span, completes the
published partial square randomly, encrypts it, and deletes five uniformly sampled
distinct source positions. The known rank order and published square anchors
are given to the optimizer; the random completion, loss positions, fills and
plaintext are evaluation-only. The same frozen families support other cipher
conditions in the p73 and p170 packages; those are not independent historical
samples.

Each original dependency is hash-pinned. The Tiflis input is preserved in
[frozen_sources](frozen_sources) because the live source edition was later
extended with the missing preamble. New source editions are not silently
added to this training snapshot.

The radio component maps digits to one class, counts the 27-class quadgrams,
adds 0.01 to each possible cell and normalizes. It then distributes a class
probability uniformly across its specific digit spellings: a pattern with
`k` numeric positions assigns each spelling one `10^-k` share. This expanded
36-symbol distribution is mixed equally with the normalized, independently
built book distribution. The score is the base-10 logarithm of that mixture.
The book and radio components are different sources; the original book
quadgram and word-segmentation objectives share the same ten books.

## 2. Matched five-loss controls: no general improvement

The same seed and a 120-second blind budget are used for each book/radio pair.
Every received coordinate is preserved, and unfilled square cells remain a
permutation of the unused symbols. Correct characters are out of 85.

| Held-out source | Book objective | Radio mixture |
| --- | ---: | ---: |
| p92 A: courier | 81 | 81 |
| p84 A: oil inquiry | 82 | 79 |
| p190 D: relay request | 84 | 84 |
| p192 part 2: appointment | 85 | 85 |
| p205 A2: finance | 81 | 82 |
| p96 B: permission | 82 | 83 |
| **Exact texts** | **1 / 6** | **1 / 6** |

The sums are 495/510 and 494/510. This small fixed sample does not establish
an improvement. Several wrong strings score above their true texts, especially
in references and names. The book model's courier candidate changes the
number and the surname; the mixture likewise retains a wrong surname and
prefers letter-like reference fields. Even an unchanged-source round-trip
cannot authenticate those choices.

[loss_controls.json](loss_controls.json) contains every truth, selected result
reference, final event, seed and model hash. It records **632,810,000 completed
mutation proposals**. A proposal can be a no-op; this is not the total number
of all fitness calls. The first discovery of the best candidate and the actual
final proposal counter are separate fields.

The [p170 rank-search calibration](../p170_new_methods) uses the same held-out
families in a different task: 53 characters, no source loss, the full true
square supplied, and hidden column order at the correct width. The matched
radio mixture recovers 5/6 full texts versus 2/6 for the book model. The
remaining width-22 control fails under both; its better true score shows a
search failure. The [p73 fixed-rank hidden-square controls](../p73_new_methods)
recover neither fresh text exactly and still select wrong texts above truth.
The benefit is therefore specific to the observed search conditions.

## 3. Adaptive follow-up: score a single numeric class

After observing the first mixture's numerical-reference errors, a separate
objective was designed to treat all ten digit labels identically. This is
explicitly adaptive; the earlier six controls are development observations
for this follow-up.

Four further source families are removed from the training set before testing:
Kiel radio control, LP forwarding, Budapest telephone censorship, and naval
report administration. The resulting [class dataset](class_dataset.json) has
**37 training strings and 3,945 quadgrams**. The book probabilities are folded
into 27 classes, then mixed equally with the newly held-out radio component.
The 36/37-index binary tables are lookup adapters for a 27-class score; they
are not normalized probability distributions over 36 separate symbols.
Wildcard marginalization counts the numeric class once, not ten times.

| Additional held-out family | Folded book | Folded radio mixture |
| --- | ---: | ---: |
| Kiel radio control | 85 / 85 | 85 / 85 |
| LP forwarding | 85 / 85 | 85 / 85 |
| Budapest telephone | 82 / 85 | 83 / 85 |
| Naval reports | 82 / 85 | 82 / 85 |
| **Exact texts** | **2 / 4** | **2 / 4** |

These four selected spans contain no numeral, so their literal and
letter-or-digit-class accuracies coincide. They test ordinary wording under
the modified score, **not recovery of numerical fields**. The objective cannot
distinguish individual digit labels by construction. Wrong ordinary-word
candidates still outrank truth in the two failed families. The completed
matched runs account for **410,810,000 mutation proposals**.

## 4. Numerical fields: a separate fresh calibration

The four additional source spans above contain no digits. To avoid treating
that success as evidence for numeral recovery, four new, deliberately numerical
telegram-like texts were authored after the model settings were frozen. They
are synthetic controls, not historical readings. Each has 85 characters,
a random completion of its published partial square, and five scattered losses.
All four objectives use the same seed for a given control and 120 seconds.
The Nov13b control additionally supplies the separately stated FX=Y condition.

The cells below show **literal agreement / agreement after folding all digits
to one class**, each out of 85:

| Authored control | Book | Radio mixture | Folded book | Folded radio |
| --- | ---: | ---: | ---: | ---: |
| Train, dates and departure times | 71 / 83 | 71 / 81 | 70 / 85 | 70 / 85 |
| Marineamt, ship and payment | 80 / 85 | 78 / 82 | 80 / 85 | 78 / 83 |
| Radio wavelength and listening times | 75 / 81 | 75 / 80 | 74 / 80 | 77 / 81 |
| Order number, time and companies | 81 / 82 | 81 / 82 | 82 / 84 | 84 / 84 |
| **Exact literal texts** | **0 / 4** | **0 / 4** | **0 / 4** | **0 / 4** |
| **Exact class texts** | **1 / 4** | **0 / 4** | **2 / 4** | **1 / 4** |

The folded score recovers two class sequences under the book objective,
but class agreement does not establish the numeric equality pattern or the
digit labels. Other failed controls
still contain ordinary-word errors that score above truth. The mixture does
not establish an advantage in this sample. The completed 16 runs use
**732,130,000 mutation proposals**. The [dataset](numeric_dataset.json) freezes
the authored strings and truth-generation seeds; [results](numeric_loss_controls.json)
retain every candidate, truth score, final counter and original log hash.

The [exact digit-symmetry audit](digit_symmetry/README.md) now distinguishes
those two limitations. Keeping a recorded candidate's letters, ranks, losses
and fills fixed, permuting its `k` unanchored digits gives exactly `k!` complete
squares and `k! / (k-r)!` literal texts, where `r` such digits occur in the text.
The Nov13b folded-book candidate has **360** such literal texts, including the
truth. Both CHI candidates instead have **3,628,800** literal texts in their
respective orbits, yet neither orbit contains the true text: each repeats one
digit at two positions where the truth has different digits. Their perfect
85/85 class agreement therefore hides a wrong equality pattern as well as
unresolved labels. The proof, small-orbit enumeration and complete bitwise
check of both class lookup tables are separate from stochastic search.

## 5. Conditional p198 follow-up

Four additional blind 1,800-second jobs preserve all 165 received coordinates
and infer exactly five missing positions and their coordinate values. Three use the Nov13b partial square
with **FX=Y** from the separate [Tydelski identity hypothesis](../contextual_key_constraints/README.md):
the book-plus-word score at weight 2, the expanded radio mixture, and the
single-numeric-class mixture. The fourth uses the CHI-Nov13 partial square
and the class mixture, without transferring the Y condition.

All four completed jobs remain unreadable. Their arbitrary square completions,
losses, fills, scores and final counters are in
[conditional_targets.json](conditional_targets.json). They account for
**2,190,795,000 mutation proposals**; this is separate from the control totals
and from the older word-engine campaign. No sampled candidate is accepted,
and these finite searches do not exclude either historical key hypothesis.

## Reproduce and verify

The default verifier uses only Python's standard library. It regenerates
the frozen dataset selections and numerical controls, checks source dependencies and independently
re-encrypts every archived result:

```sh
python experiments/radio_domain_model/verify.py
python experiments/radio_domain_model/digit_symmetry/verify.py
```

Rebuild the models with NumPy; the recorded environment used NumPy 2.3.5:

```sh
python experiments/radio_domain_model/build.py --verify-dataset \
  --book-quad /path/to/german_military36_quad.bin --output /tmp/radio-model
python experiments/radio_domain_model/build_class_model.py --verify-dataset \
  --book-quad /path/to/german_military36_quad.bin --output /tmp/radio-model
python experiments/radio_domain_model/verify.py --models /tmp/radio-model \
  --book-quad /path/to/german_military36_quad.bin
```

Optional model verification recomputes both true and selected-candidate
scores. All model SHA-256 values are in the two provenance files. The source
engine is the word-loss engine with the unused lexical score skipped at
weight zero; its input geometry and mutation rules are unchanged.

```sh
g++ -O3 -std=c++17 experiments/radio_domain_model/quad_loss.cpp -o /tmp/quad-loss
python experiments/radio_domain_model/run_loss_control.py \
  --variant 36 --control 0 --model radio --engine /tmp/quad-loss \
  --quad /tmp/radio-model/radio_book36_quad.bin \
  --lexicon /path/to/lexicon.txt --output /tmp/radio-control-replay
```

The lexical file is loaded by this engine interface but unused at zero word
weight. Reproduction uses the recorded seed; hardware-dependent wall-clock
budgets may reach different proposal totals. The archived source witnesses
and their objective values have deterministic independent verification.

For a numerical control use `--variant numeric --control 0` and one of
`--model book`, `radio`, `book_class`, or `radio_class`, with the matching
frozen table. The [independent audit](independent/README.md) separately rebuilds
all six radio/class tables and checks the word-score implementation and the
original completed-run logs; its initial 30-case snapshot is preserved.

To replay one conditional target under its recorded model and seed:

```sh
python experiments/radio_domain_model/run_conditional_target.py \
  --case Nov13-15b_radio_class --engine /tmp/quad-loss \
  --quad /tmp/radio-model/radio_book_class36_quad.bin \
  --lexicon /path/to/lexicon.txt --output /tmp/conditional-p198-replay
```

Add `--lexicon /path/to/lexicon.txt` to the verifier command to recompute the
conditional word objective as well as the supplied quadgram models.
