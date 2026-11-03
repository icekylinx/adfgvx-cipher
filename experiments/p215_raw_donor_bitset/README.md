# Exact raw-domain copy scope for p215 B3

Prepared by **icekylinx and GPT-6 Astra Pro**, 4 November 2026.

This research checkpoint closes a previously capped donor scope. All **62
literal-label windows and 62 widened-label windows are infeasible**, with
zero capped branches at a 25-million-node limit per branch. It supplies no
new plaintext; p215 B3 remains unread. [Recorded results](result_summary.json)
include branch node counts and the control outcome.

The target retains all 219 printed slots: 200 observations and 19 masks.
The model has 234 coordinates, every permutation of 22 physical columns,
and exactly 15 additional transmitted-coordinate losses. It uses the
published Nov22–24 numeric+J+Y conjunction: 28 anchored square cells and
every one of the remaining **8! = 40,320 injective completions**.

The donor is p219 C under two distinct conditional raw-domain models.
Each excludes 15 of 284 observed coordinates and inserts 25 unassigned
coordinates, retaining 269 observations in a 294-slot frame. No word fills
or name repairs are used. These streams represent the four tied minimum
ownership maps; the **other 77 source geometries are outside this scope**.
Each 147-position donor supplies all 31 windows of length 117.

The widened run preserves every original domain label. Where a domain
meets `0123456789JQY`, it unions the entire 13-label set into that domain.
Independent expansion is a safe superset of global donor relabelings
within that set. Its infeasibility excludes those relabelings too. It
does not cover arbitrary changes to the anchored ordinary-letter set.

## Method and controls

One bitset indexes complete shared squares. For each of 49 observed
row/column patterns, a domain permits the union of compatible squares;
intersections across positions retain one globally consistent square.
Exact search jointly chooses the column order and lost transmitted slots.
Printed masks consume source slots and remain distinct from new losses.
For even width, only observations in unfinished adjacent column pairs
need remain in the memo context; cached key sets are exact.

All **89 independent exhaustive miniature oracles** agree with the engine,
including a case that permits local cell choices but forbids a shared
injective square. The full-size unhinted control recovers its exact column
order, complete square and all 15 loss positions in 1,361 nodes. Its
arbitrary witness matches 116/117 planted labels; one masked position
retains a domain alternative.

## Replay

Python 3.10 or later; standard library only. Generate bulky inputs and
outputs outside the checkout. Source pixels are not authenticated here.

```sh
python verify_controls.py
python prepare.py --output /tmp/p215-bitset --repo /path/to/adfgvx-cipher
python run_scope.py /tmp/p215-bitset/literal62.json --workers 3 \
  --output /tmp/p215-bitset/literal-results.json
python run_scope.py /tmp/p215-bitset/relaxed62.json --workers 3 \
  --output /tmp/p215-bitset/relaxed-results.json
```

Omit `--repo` to generate from the compact frozen transcriptions alone.
With it, all four published input hashes must match. The recorded literal
run used 263,313,458 nodes; the widened run used 471,233,163. Timings depend
on hardware and concurrency. A capped result is never an exclusion.

Historical source: J. Rives Childs, *General Solution of the ADFGVX Cipher
System*. Period-key credit remains with George Lasry, Ingo Niebel, Nils
Kopal and Arno Wacker (2016), and Lasry's 2017 list. The source decisions
and prior qualifications remain in the pinned repository packages named
in [frozen inputs](frozen_inputs.json). The lost older 57-branch cap list
was not recovered; all 62 reconstructed raw windows were recomputed.
