# Mackensen armistice appeal: six-part source edition

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

The [readable edition](../../cases/pages/220.md#edition-cases-military-mackensen-armistice-appeal)
covers Childs p220 C1–C4 and p221 A5–A6. The body had already been identified
by Childs and summarized by Lasry, Niebel, Kopal and Wacker in 2016. The
published Nov25–28 key is used unchanged.

This package restores two observed final groups omitted by OCR, records
all 1,352 received slots, and makes the fifth part's ten-coordinate
shortfall explicit. Its representative frame has 667/681 fixed raw-label
positions. The complete same-length editorial candidate uses 24 observed
substitutions, four printed-erasure fills and ten inserted-coordinate fills.
No source coordinates are deleted or rearranged.

## Source and evidence files

| File | What it preserves |
| --- | --- |
| [inputs.json](inputs.json) | Literal rows, unchanged key, source headers, crop geometry, raw/candidate texts, prior attribution and model assumptions |
| [certificates.json](certificates.json) | Every plaintext position and source pair, exact edits, numerical/rare-letter inventory, all contiguous-gap costs and retained two-group minima |
| [two_group_costs.tsv](two_group_costs.tsv) | All 24,976 ordered two-five-coordinate-gap comparisons against the full and masked retrospective templates |
| [candidate_scores.json](candidate_scores.json) | All 223 contiguous-gap raw readings, earlier book/radio ranking scores and pinned model hashes |
| [prior_candidates.json](prior_candidates.json) | Six earlier unreviewed OCR-derived records and their original-file digest |
| [sources/p220_C.png](sources/p220_C.png), [sources/p221_A.png](sources/p221_A.png) | Source sections containing all six parts and their repeated headers |

The source PDF is pinned by SHA-256
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
The optional PDF check regenerates both crops at their recorded scale and
compares every RGB pixel. The basic verifier checks delivered image hashes
without requiring the large PDF or image libraries.

## Conditional geometry

A5 advertises 232 coordinates but prints 222, including three dashes.
The representative inserts two missing five-coordinate groups at the start.
The full retrospective wording selects that placement at six substitutions.
Masking its opening, `INTERNIERUNG` and `KARPATHEN` leaves five minima:
`(0,0), (1,1), (1,2), (2,2), (3,3)`. The five raw readings share 100/116 fixed
positions. The same masks leave four contiguous-ten-gap minima.

Both the full and masked templates were prepared after reading candidates.
They measure costs; they do not supply independent historical evidence.
The language models rank the leading gap first, but that ranking is not a
proof of loss mechanism. All source/model alternatives in the declared
search spaces can be reproduced from the retained rows.

The verifier uses ranked column-chunk allocation independently of the
project cipher, then checks the project implementation's raw domains,
encryption and decryption. It independently verifies every two-group cost
both with prefix sums and with full-string alignment. No additional search
budget or heuristic success is implied by these deterministic checks.

## Reproduce

```sh
python experiments/mackensen_armistice_appeal/verify.py --verify
python experiments/mackensen_armistice_appeal/verify.py --verify --pdf /path/to/childs.pdf
python experiments/mackensen_armistice_appeal/verify.py --verify --book-model /path/to/german_military37_quad_marginal.bin --radio-model /path/to/radio_book37_quad_marginal.bin
```

The first command uses the standard library. The PDF option needs PyMuPDF
and Pillow; model-score replay uses standard-library float arrays. Original
reference labels, the received `ERFOLT` spelling, prior body credit and the
source/paper time discrepancy remain explicit throughout.
