# Anchored substitution-square search

Authors: **icekylinx and GPT-6 Astra Pro**.

This bounded experiment keeps the attested cells of a historical substitution
square fixed while searching an arbitrary column order and, where necessary,
completing the unknown square cells injectively. It tests component reuse for
pages 73 and 170. Reusing a square from another date is an attack hypothesis,
not a claim that it was the historical key.

**Only 2 of 70 planned historical cases completed. Neither produced an
accepted plaintext.** The historical run was interrupted to investigate the
independent page 153 discovery. The two completed cases are page 73 with the
28–31 October square at widths 16 and 17. No result is implied for the other
68 cases.

## Frozen inputs and controls

`data/cases.json` freezes the exact source-analysis ciphertext layer, partial
squares and evaluation-only control truth. The 70 historical cases are pages
73 and 170, five attested squares (28–31 October and 1–3, 4–6, 7–9 and
10–12 November), and widths 16 through 22. The input lengths are 178 and 106 coordinates;
page 73 has two declared erasures. No coordinate is deleted or rewritten.
An erasure occupies one slot; it does not represent an unknown-length gap.

The two invented controls have 89 and 53 plaintext characters, matching those
lengths. Their ciphertext lengths and erasure profiles match the historical
targets. The control plaintexts, true squares and true column orders are never
sent to the engine. They are used after fitting to assess recovery.

| Control | Restarts × proposal slots | Correct fully observed letters | Correct observed coordinates | Truth in every exact domain |
| --- | ---: | ---: | ---: | --- |
| 89 characters | 100 × 50,000 | 24 / 87 | 73 / 176 | No |
| 53 characters | 100 × 50,000 | 4 / 53 | 27 / 106 | No |
| 89 characters | 1,000 × 100,000 | 87 / 87 | 176 / 176 | Yes |
| 53 characters | 1,000 × 100,000 | 53 / 53 | 106 / 106 | Yes |

The stronger budget was chosen after observing the initial failures. These two
successful examples calibrate a bounded method; they do not establish a
recovery probability for historical messages. Every row, including both
failures, is retained in `data/result_snapshot.json`.

At the advertised historical budget, 70 cases would request 7,000,000,000
proposal slots. The two completed cases account for 200,000,000 slots. A slot
is not necessarily a distinct candidate or a completed evaluation: some moves
are skipped or repeat a state. The C engine also performs up to two greedy
pairwise-improvement passes after each restart, outside that proposal count.

## Objective and limits

The shared `anchored_joint` engine uses arbitrary column swaps, insertions,
reversals and pair exchanges, plus swaps among unanchored square cells.
Attested cells are immutable. Starts are randomized and selected restarts
perturb the current best state. This is stochastic optimization, not exhaustive
column-order enumeration.

The objective is a 37-symbol quadgram table, where the extra symbol is a
whole-letter wildcard. If one coordinate of a digraph is missing, ranking
marginalizes all 36 plaintext symbols and therefore discards the surviving
half-coordinate. The published result restores the exact six-cell domain
for such a position; fully missing digraphs have 36-cell domains. These exact
domains and a full re-encryption witness are arithmetic checks, not evidence
that a language-scoring candidate is the historical text.

The table comes from the independently built military model documented by
`experiments/joint_search/models/provenance.json`: six general German books,
four wartime books with weight 2, and three normalization streams weighted
5:3:1. No challenge plaintext or control is training data. The wildcard table
has SHA-256
`2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e`.
This package reuses that suite's engine, model builder and source provenance;
it does not duplicate books, binary models or C engines.

## Reproduction

Run from the repository root. Python 3.10+, a C11 compiler and `make` are needed.
NumPy is needed only to rebuild the shared wildcard model. The binary model
format requires a little-endian host with 32-bit IEEE floats.

```sh
make -C experiments/joint_search
python3 experiments/joint_search/tools/build_models.py --cache work/corpus --output work/joint_models
python3 experiments/anchored_search/verify_results.py
python3 experiments/anchored_search/run_anchored_squares.py --list
```

The small verifier checks the archived snapshot without an optimizer or any
language model. It independently recomputes the transposition, domains,
source-coordinate preservation and control recovery counts. It does not
recompute heuristic scores.

Reproduce each control budget in a separate output directory:

```sh
python3 experiments/anchored_search/run_anchored_squares.py --controls --model work/joint_models/german_military37_quad_marginal.bin --output work/anchored_control_small --restarts 100 --iterations 50000
python3 experiments/anchored_search/run_anchored_squares.py --controls --model work/joint_models/german_military37_quad_marginal.bin --output work/anchored_control_large --restarts 1000 --iterations 100000
```

Reproduce the two completed historical cases:

```sh
python3 experiments/anchored_search/run_anchored_squares.py --model work/joint_models/german_military37_quad_marginal.bin --output work/anchored_historical --limit 2
```

Omit `--limit 2` only to launch the entire planned 70-case experiment. Other
options are `--engine`, `--repository`, `--workers`, `--only` (a case-label glob)
and `--reverse`. Reversing changes execution order only; seeds and inputs stay
fixed. The default is one worker. Model paths in the C header cannot contain
whitespace. The CLI requires the pinned model hash and validates input lengths,
symbols, square injectivity, positive budgets and every completed result.

The seed is the first 15 hexadecimal digits of SHA-256 of the complete case
label. Existing output is resumed only after checking the input/budget/engine/
model/runner fingerprints and recomputing the saved arithmetic. An incompatible
record is rejected before replacing the run manifest. Use a separate directory
for a different budget or executable. A compiler change may change stochastic
trajectories; the archived executable hash is provenance, not a portability
requirement.

To refresh the snapshot from a directory containing completed records:

```sh
python3 experiments/anchored_search/refresh_results.py --results work/anchored_historical --output work/anchored_snapshot.json --interrupted
python3 experiments/anchored_search/verify_results.py --snapshot work/anchored_snapshot.json
```

A snapshot may contain all four control records together with historical
records, as the archived research directory did. The refresh helper counts
historical cases at the advertised budget only and rejects duplicate case
budgets. It never treats a partly written or missing result as complete.

`data/provenance.json` retains the original research driver's byte count and
SHA-256; `data/result_snapshot.json` records the exact two-case interruption.
Use the portable `run_anchored_squares.py` entry point, which adds validation
and resume checks while retaining the frozen inputs, label-derived seeds and
C search. The duplicate driver with obsolete workstation paths has been retired.
