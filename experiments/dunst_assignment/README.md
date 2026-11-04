# Major Dunst: cancellation of the Turkey assignment

Prepared by **icekylinx and GPT-6 Astra Pro**. The
[reader case](../../cases/pages/095.md#edition-cases-people-dunst-assignment) presents two numbered
parts on Childs printed p95 / PDF page 98, headed 1 November 1918. Their shared
header reads `OSM v LP (5.22 p.m., November 1st)`,
`SSD GRHQU (1/11)0400 2 TEILE`.

The text cancels the assignment of Major `DUNST` to Turkey and the military
mission. The earlier date `DEZEMBERX2X1917`, order `AXKXOX26X10X18` and
reference `92527` are literal labels under the unchanged published November
1–3 key. They are not inferred from a biography or reassigned square digits.

| Record | Literal displayed slots | Valid coordinate letters | Working slots | Fixed raw / total positions | Observed substitutions |
| --- | ---: | ---: | ---: | ---: | ---: |
| p95 A1 | 283 | 282 | 282 | 141 / 141 | 3 |
| p95 A2 | 464 | 464 | 464 | 232 / 232 | 1 |
| **Total** | **747** | **746** | **746** | **373 / 373** | **4** |

No valid observed coordinate is deleted, no source erasure is filled, no
coordinate is inserted, and no key cell or rank is changed. The first frame
explicitly excludes one **prefixed noncoordinate dash**, discussed below.
Raw labels `1` and `7` in `KONST1NTINOPEL` and `R7S` are changed only through
the listed word repairs. Every historical numerical field remains unchanged.

## First-part prefixed mark

The [detail image](sources/p95_A1_prefix.png) preserves `-DGDGX`. The complete
five-coordinate group `DGDGX` is aligned with the following first groups;
the dash is immediately to its left. The 282 valid coordinate letters match
`RICHI-282`. The source does not explain that dash.

The working interpretation excludes source mark 0, retaining all 282 valid
letters. The input and certificate preserve the complete 283-slot string,
its raw paired prefix and its unpaired coordinate. A conditional model is
therefore visible even though no observed coordinate is changed by this
boundary choice.

A retrospective fixed-target check evaluates all 283 one-slot exclusions.
Indices 0 and 1 have zero known-coordinate disagreement with the accepted
raw stream. Index 0 excludes only the prefixed dash. Index 1 instead deletes
an observed D and fills the retained dash with D. The certificate prices
those costs separately. It does not equate them, claim a unique historical
mechanism, or describe this finite consistency check as blind recovery.

## Reproduce

```sh
python3 experiments/dunst_assignment/verify.py --verify
python3 experiments/dunst_assignment/verify.py --verify --pdf /path/to/childs.pdf
```

The default verifier needs only the standard library. It verifies the exact
source rows, both source layers, all coordinate origins, raw decodes,
independent forward encryption, four word repairs, preserved fields and
numeral positions, the complete 283-placement consistency ledger, and all
saved image and prior-evidence byte hashes. It compares the recomputed result
with `certificates.json`.

The optional PDF check requires PyMuPDF and verifies the full PDF hash plus
five exact pixel hashes after re-rendering the recorded rectangles/scales
with a cleared image cache. PDF SHA256:

```text
157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06
```

[Full page](sources/p95_full.png) · [A1](sources/p95_A1.png) ·
[A2](sources/p95_A2.png) · [A1 prefix](sources/p95_A1_prefix.png) ·
[A2 last row](sources/p95_A2_last_row.png).

## Prior work and reading limits

The period key is prior Lasry-team work, with provenance retained in
`inputs.json`. The prior OCR snapshot contains 243/424-slot frames beginning
at the second typed row. Those unreviewed candidates did not recover these
bodies. Manual transcription corrects the OCR; it does not infer a historical
insertion for each omitted OCR row.

`BEORDRT` stays unchanged in the raw and edited streams. The reader-facing
`beord[e]rt` explicitly marks a prose-only completion. The readable layer also
marks the expansion of `MILIT`; it does not silently add decrypted letters.
The source supports the named officer and the cancellation message, not a
separate identification of his full biography. No universal first-decipherment
priority is claimed.
