# Page 153: exact component check at odd widths

Authors: **IceKylin and GPT-6 Astra**.

**The supplied sixty-letter first-part crib has no compatible key at widths
15, 17, 19, 21, 23 or 25.** All six searches completed. A width-18 overlap
reproduces the two equivalent partial keys from the separate even-width proof.
Combined, the two packages test every integer width from 14 through 26; only
width 18 fits this particular crib and unchanged first-part source.

This is post-discovery validation. The text was supplied after the blind search
found it. Other readings, lengths, widths, transposition geometries or source
repairs are not excluded. No date, order number, footer or complete square is
recovered by this calculation.

## Completed bounds

| Odd width | Long columns | Complete segmentations | Compatible partial keys |
| ---: | ---: | ---: | ---: |
| 15 | 12 | 455 | 0 |
| 17 | 13 | 2,380 | 0 |
| 19 | 18 | 19 | 0 |
| 21 | 6 | 54,264 | 0 |
| 23 | 17 | 100,947 | 0 |
| 25 | 7 | 480,700 | 0 |

All **638,765** odd-width column-length segmentations were visited. The
width-18 overlap separately visits 18,564 segmentations. No run reached its
90 CPU-second, 10,000,000-node or 1,000-solution cap. A segmentation is a
column-length layout, not a complete key. Every compatible column assignment
and injective square constraint is searched within it.

## Coordinate variables and row crossings

At odd width, consecutive digraph coordinates can cross a row boundary. It is
incorrect to treat the rectangle as fixed adjacent column pairs. This program
instead gives each known plaintext letter two variables: its square row and
its square column, each in `0..5`.

For every physical column, its row-major stream positions determine which
letter/component each received coordinate must represent. Every ciphertext
chunk of the correct height is considered for that column. A candidate is
rejected only if repeated instances of one component disagree or completed
letter cells cease to be injective. Backtracking assigns each chunk to one
physical column and extends the same global component map. Completed states
therefore describe exactly the permitted transpositions and partial squares.

The six first-part `?` positions impose no plaintext value. The nineteen known
letters constrain nineteen complete square cells. Unknown square cells remain
free, and the numeric-looking cells are not assigned historical digits.

The second part resets independently at 108 coordinates. Its column lengths
and offsets are recomputed for each returned rank order. The two coordinates
of a plaintext character may belong to different physical rows; each is mapped
with its own stream index. The second crib is evaluated only after a complete
first-crib key has been found and never prunes that search.

## Controls and independent checks

Each odd width has a fresh seeded square and rank permutation. The source has
the same fifteen-coordinate erasure interval as the historical second part,
plus two deliberate known-coordinate errors at positions 0 and 1. Every odd
control returns its true partial key and exactly those errors. The width-18
control returns the expected two equivalent representations. The adjacent-pair
transpose equivalence is not assumed for odd widths. A constant-letter false
crib supplies a negative control and returns no key.

`run_and_verify.py` independently reconstructs the full first and second
rectangles and reencrypts every returned key. The original width-18 proof and
the even-width package remain unchanged. `independent_python_check.py` supplies
an additional implementation using functional dictionary state rather than the
C solver's mutable row/column maps and rollback. Its published result files
state exactly which widths were exhaustively rerun.

## Reproduce

```sh
cc -O3 -std=c11 -Wall -Wextra -Werror enumerate_components.c -o /tmp/p153-components
python3 run_and_verify.py --engine /tmp/p153-components --output /tmp/p153-components-results
python3 independent_python_check.py --input historical_input.txt --c-results /tmp/p153-components-results --widths 15 17 19 --output /tmp/p153-python-small.json
```

The independent Python checker also accepts `--widths 18 21 23 25`; these
larger cases are slower in Python. The raw C interface is:

```text
enumerate_components INPUT WIDTH [CPU_SECONDS [MAX_NODES [MAX_SOLUTIONS]]]
```

Widths 14 through 26 are supported. Omitted or zero optional budgets mean
unlimited. An incomplete run explicitly records `complete: false` and a stop
reason. Published runs all record `complete: true`. CPU timings are incidental.

`results/verification.json` preserves the source/input hashes, all summaries,
control seeds, evaluation-only truths and outcomes. The JSONL results and
control input files are included. No executable, corpus or language model is
distributed. The conclusion remains conditional on the supplied first crib,
standard row-major coordinates followed by column readout, an injective square,
unchanged first-part source and independent resetting of the second rectangle.
