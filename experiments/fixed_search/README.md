# Fixed-permutation and coordinate-geometry experiments

This package makes four bounded research branches reproducible. **No historical
plaintext from these search branches has been accepted.** A high language score
and a mathematically valid fitted square do not establish the historical key.
The later source-based p152 and p189 findings are separate from these searches.

## What was searched

| Branch | Exact configured cases | Objective and scope |
| --- | ---: | --- |
| Fixed transposition | 144 | Eight separate targets and one p153 joint target, each under 16 recorded rank families; unknown bijective square; general German quadgrams. |
| Dictionary permutations | 1,352 | Deduplicated p73/p170 rank candidates selected independently of a square, then fitted with an unknown bijective square and military German quadgrams over the complete observed coordinate domains. |
| p198 group-gap refinement | 136 | Four rank families × 34 positions for one missing five-coordinate group; unknown bijective square; 30% four-gram and 70% six-gram composite score. There are 102 warm starts and 34 cold starts. |
| Coordinate/geometry screen | 20,666,880 evaluations | 23 partly or fully known squares, all 720 common permutations of the six coordinate labels, both coordinate-pair orientations, and deduplicated rank/readout conventions. Includes a synthetic control. |

The first two fit branches request 1,000 restarts × 60,000 proposal slots per
case. The gap branch requests 120 × 100,000. A proposal may be skipped or repeat
a previously visited state, so these are **configured proposal slots**, not
counts of distinct keys. `data/completion_snapshot.json` distinguishes completed
unique records from the full planned budget and records its capture time.

### Input layers and limits

`data/input_layers.json` preserves the exact inputs of the earlier run and
compares them with the source-audited transcript. The fixed branch masks p152
positions 29 and 69. Its p189 input retains six legacy glyph interpretations
that the later source audit treats as uncertain. Its p176b input uses the 220
received coordinates without the previously published twenty-slot restoration.

The archived fixed branch maps a partly erased coordinate pair to a whole-cell
wildcard, losing its known half for scoring. For odd-length p198, it pairs only
the first 164 untransposed coordinates and explicitly records the abandoned
last coordinate. This is a diagnostic of a damaged input, **not an ordinary
complete-message decryption**. The ordinary decoder and both later domain
solvers reject odd coordinate streams. The joint p153 case resets transposition
between its 132- and 108-coordinate parts and separates their cell strings with
four artificial wildcards; it does not transpose a combined rectangle.

The dictionary and gap fits keep every observed coordinate, including the known
half of a partly erased pair. A four- or six-letter window sums model mass over
the permitted cells. The overlapping-window objective is a composite score,
not an exact sequence likelihood or a confidence estimate. Unknown source
coordinates are not filled in their printed candidates.

The gap refinement uses CHI-Nov13, Nov13–15b, Nov13–15a and Nov28–Dec1. The prior
quad-only search used Nov16–18 instead of Nov28–Dec1. Consequently only the
three overlapping families supply warm starts. Their exact 102 initial squares
and prior-record hashes are preserved in `data/p198_warm_starts.json`; all 34
Nov28–Dec1 cases start without a supplied square. This corrects an earlier
research bookkeeping assumption that all 136 refinements were warm-started.

The geometry screen tests normal and inverse ranks, a physical-column mirror,
ascending/descending column readout, and reversal inside each column. Equivalent
index maps are deduplicated. A common coordinate-label permutation acts on both
coordinates; independent row/column permutations are outside this screen. Its
unknown windows receive the recorded constant −7.4. The count includes 39 input
variants: four unchanged targets, 34 p198 group-gap variants, and one synthetic
control. A negative result does not exclude other ranks, squares or damage.

## Build and inspect

Python 3.10 or newer and a C11 compiler on a little-endian system are needed. NumPy is needed only by the
coordinate/geometry screen. Generated executables, books, wordlists and binary
models are not distributed in this package.

```sh
make
python tools/verify_inputs.py
python src/run_fixed_transposition.py --list
python src/run_dictionary_permutation_fits.py --list --limit 5
python src/run_gap_domain_refinement.py --list
```

The archived C sources are preserved unchanged. The wrapper validates their
alphabets, budgets, complete square seeds and model hashes before fitting.
The legacy `subsolve` does not always record its starting state before a swap;
a very small test budget can therefore produce no incumbent. The wrapper reports
that outcome explicitly. It does not change the archived stochastic trajectory.

## Models and shared caches

`data/model_provenance.json` gives every source URL, byte hash, mixture weight,
normalization rule and expected output hash. The general model uses six German
Project Gutenberg books. Book 6099, present in the initial ID list, is actually
French and is excluded. The military model adds four independently sourced
German wartime books at twice the general-book weight. No challenge plaintext,
candidate or newly decrypted parallel was inserted into either model.

Three textual conventions receive weights 5:3:1: joined letters/digits,
sentence-boundary `X`, and word-boundary `X`. German umlauts are expanded to
`AE/OE/UE`, and sharp-s to `SS`. These conventions and the military adaptation
are model choices, not inferences about the encipherer's exact wording.

Reuse a single cache shared with other experiment packages:

```sh
python tools/build_models.py --kind all \
  --corpus-directory /path/to/general-books \
  --corpus-directory /path/to/military-books \
  --output /path/to/shared-models
```

To retrieve the public source books into a new cache, use `--download
--cache-directory /path/to/shared-books` instead. A changed source hash stops
the rebuild. The builder requires the final model hashes to match the archived
tables. No binary model is needed merely to inspect inputs or refresh budgets.

## Run selected fits

All commands default to one worker. Use `--only` with a case-label glob,
`--limit`, `--reverse`, `--restarts` and `--iterations` to make the experiment
scope explicit. Canonical seeds are derived from the case label; `--seed-offset`
creates a new deterministic run. Existing results are resumed only when their
entire recipe fingerprint matches.

```sh
python src/run_fixed_transposition.py \
  --model /path/to/shared-models/german36_quad.bin \
  --only 'p170__*' --output work/fixed

python src/run_dictionary_permutation_fits.py \
  --model /path/to/shared-models/german_military36_quad.bin \
  --only 'p73__*' --output work/dictionary

python src/run_gap_domain_refinement.py \
  --model /path/to/shared-models/german_military36_quad.bin \
  --six-model /path/to/shared-models/german_military36_sixgram.bin \
  --only 'p198__CHI-Nov13__*' --output work/gaps

python src/coordinate_geometry_screen.py \
  --repository data/geometry_repository \
  --model /path/to/shared-models/german_military36_quad.bin \
  --output work/coordinate_geometry.json
```

The geometry fixture freezes the input keys and transcripts of the recorded
screen. Pointing `--repository` at an updated publication repository creates a
new input layer; record that distinction when comparing outputs.

## Dictionary selection

The raw list comes from `enz/german-wordlist`; its source, license and content
hashes are recorded in `data/wordlist_provenance.json` and `data/WORDLIST_COPYING`.
Normalization generates both expanded and unaccented umlaut spellings, retains
uppercase A–Z at lengths 8–40, deduplicates and sorts. It produces 724,720 words
whose actual maximum length is 25. Seventeen recorded context words and the
explicit control keyword `TRUPPENVERSCHIEBUNG` are added. That control is an
implementation check, not evidence of dictionary coverage.

The selector scores substitution-invariant coincidence and frequency profiles.
For each observed width and objective it retains the best 300 words, then the
best 20 distinct stable rank permutations. Tied repeated keyword letters are
ranked left to right. Each target contributes 720 selection records; deduplication
across objectives leaves 1,352 fitting cases in total. The profiles use 10,800
independent samples from the six general German books. The p73 profile places
one or two erased plaintext cells uniformly, an approximation to its unknown
transposition mask.

The normalized list, both profiles and all selected rank records can be rebuilt:

```sh
python tools/dictionary_pipeline.py normalize --raw /path/to/raw-words \
  --output /path/to/shared-normalized-words.txt
python tools/dictionary_pipeline.py profiles \
  --corpus-directory /path/to/general-books --output work/profiles
python tools/dictionary_pipeline.py select \
  --words /path/to/shared-normalized-words.txt --output work/selection
```

## Refresh and provenance

**Historical refresh command, before candidate-export cleanup:**

```sh
python tools/refresh_results.py --research-results /path/to/root_attack/results \
  --output data/completion_snapshot.json \
  --candidates-output data/best_fits.json
```

For current use, omit `--candidates-output` when refreshing the completion ledger,
or export candidates with `--candidates-output /tmp/adfgvx-fixed/best_fits.json`.

The refresh reads completed result records, rechecks their input arithmetic and
canonical seed/budget, and counts each case once. Partial trace files are listed
separately. Summed per-case wall seconds are not elapsed project duration.
The optional candidate export belongs in a temporary working directory. The
1,632 unaccepted per-case fits are no longer distributed; the compact completion
ledger retains the completed-case hashes, budgets and leading diagnostics.

`repro/source_manifest.json` preserves the original driver, C source and
executable hashes. Portable orchestration lives in `src/`, with model and
selection tools in `tools/`; duplicate workstation drivers have been retired.
Both coordinate-domain C engines rebuild byte for byte identically to their
archived executables. The older `subsolve36` executable has a different binary
hash from the fresh build of the retained `subsolve.c`; deterministic fixture
and archived-case comparisons are recorded separately in `repro/`. Matching a
tested trace is narrower than proving binary equivalence for every input.
The tested compiler/platform is recorded in `repro/toolchain.json`; differences
in floating-point libraries or compiler behavior can change stochastic traces
on other platforms even when the input model hashes match.

The portable builders were actually run against the recorded cached sources:
all three binary-model hashes, both 10,800-sample profiles, the 724,720-word
normalization, and all 1,440 dictionary selection records reproduced exactly.
The recorded legacy fixed-search case also reproduced its full 1,000 × 60,000
trace byte for byte. The tiny portable CLI checks exercise valid output, input
arithmetic, identical-recipe resume and rejection of changed-recipe reuse.
These checks validate reproducibility; they are not new historical decryptions.

The later anchored-square/arbitrary-column branch has a different search space
and is outside these four counters. It should receive its own frozen inputs,
model provenance and completed-case ledger when imported.

`MANIFEST.json` lists the distributable files. Generated `bin`, `work`, cache,
model and Python cache files are excluded.

After refreshing a record, update this package's file inventory with
`python tools/write_manifest.py`. Import only the listed files.
