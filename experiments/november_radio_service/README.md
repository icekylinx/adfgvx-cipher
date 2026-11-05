# November radio service and document destruction

Prepared by **icekylinx and GPT-6 Astra Pro**. This source package contains
[three p132 records](../../pages/132.md#edition-cases-radio-p132-radio-service) and the separate
[p177 A destruction order](../../pages/177.md#edition-cases-radio-document-destruction).

The useful new geometry result is p132 B's genuine 155-slot frame. An
insertion-only search found its readable ending; manual source inspection
and a wider phase comparison support a **conditional extra-interim-V**
edition. Removing any one of four identical consecutive V coordinates
restores the 77-character wording about repeating a period's telegram and
sending five minutes of VVV beforehand. All four equivalent positions and
the original one-insertion candidates remain visible.

p177 A provides a contrasting source check: its earlier OCR extraction was
odd, but the source has an ordinary 186-slot frame, exactly as advertised.
It is not evidence of a historical phase error. Its readable destruction
order requires two coordinate substitutions under the unchanged partial key.

## Source accounting

| Record | Source slots | Raw fixed positions under stated geometry | Substitutions | Source-erasure fills | Additional qualification |
| --- | ---: | ---: | ---: | ---: | --- |
| p132 A | 242 | 120 / 121 | 6 | 1 | Addressee and general-name fields still unresolved |
| p132 B | 155 | 75 / 77, conditional | 3 | 2 | One extra interim V; four equivalent positions |
| p132 C | 198 | 99 / 99 | 0 | 0 | Raw abbreviations and numerical fields retained |
| p177 A | 186 | 92 / 93 | 2 | 0 | One raw unknown square label; no square assignment made |

The total is **781 printed slots and 778 valid received coordinates**,
11 observed-coordinate substitutions and three source-erasure fills.
The extra p132 B coordinate is charged separately. It is retained unchanged
in the full 155-slot forward witness, with each possible received origin
recorded. The three ordinary frames and the one conditional frame are
reported separately; their fixed-label counts do not imply that every raw
ordinary word is correct.

p132 A retains `KOSJOII`, `GENERALMAJRHYDEWALD` and `PAFR53540` without an
invented identity. p132 C retains `NACHCHE5` and every reference label.
p132 B explicitly repairs the raw word `FU1NFTER` to `FUENFTER` by one
coordinate substitution; this is not a reassignment of the square's `1`.
Its raw spelling and unchanged `5MIN` are separately preserved.

## Verification

```sh
python experiments/november_radio_service/verify.py --verify
python experiments/november_radio_service/geometry_audit.py --verify
```

The source verifier uses only Python's standard library. It implements
independent column-height inversion, retains marginal domains for the
conservative partial key, checks every image hash and source length, and
rebuilds every edit/fill ledger and forward witness. It verifies each of the
four equivalent p132 B positions separately. No shared cipher code or
external language model is needed by this default source check.

Optional source-PDF verification requires PyMuPDF and regenerates the six
images from their recorded rectangles and scales:

```sh
python experiments/november_radio_service/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

PDF SHA-256:
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
The page images, file hashes and raw-pixel hashes are frozen in `inputs.json`.
Both default verification and the full PDF check passed.

The geometry audit preserves **311 completed source candidates**: all 156
single interim insertions and 155 single interim removals in the manually
transcribed p132 B. It also prices the retrospective 77-character template
at every one of the 155 removal positions. The minimum is three substitutions
at positions 54–57; these four equal-V positions produce identical shortened
streams and the same full transmitted witness. This conditional minimum is
not an independent crib or proof of a unique historical mechanism.

To recompute the stored book and radio scores as well:

```sh
python experiments/november_radio_service/geometry_audit.py --verify \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin
```

Full score recomputation passed. Without model paths, the audit verifies all
strings, source witnesses and template costs but does not recompute the
stored heuristic scores.

## Bounded retrieval and its surviving record

The source lead came from **216 odd OCR blocks** between 55 and 700 slots.
For each, the existing best and runner-up key from the earlier frozen screen
were tried with both unchanged objectives and one interim insertion. All
**864 DP jobs completed**. They remain unreviewed retrieval candidates;
neither a readable fragment nor an improved model score establishes a source
reading. The already reviewed p126 A5 was also retrieved again, which is
reuse rather than new validation.

`retrieval/original_results.json` and `retrieval/original_driver.py` preserve
the exact original output and driver bytes. `selected_inputs.json` contains
the 216 input rows actually selected from the earlier screen, in original
order, and retains that full screen's original SHA-256. `provenance.json`
pins those assets, the frozen 25-key/model snapshot and the compiled engine
used. The default geometry audit checks every original retrieved candidate's
received-coordinate witness, not merely the selected p132 fragment.

The portable replay uses the separately frozen
[pretransposition-loss engine](../p198_pretransposition_loss/README.md):

```sh
python experiments/november_radio_service/retrieve_odd.py \
  --engine /path/to/interim_dp \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin \
  --output /tmp/odd-retrieval-replay.json
```

`--max-blocks 1` runs an explicit four-job interface smoke check; this path
was tested separately without overwriting the original ledger. The full
screen is intentionally bounded to two previously nominated keys per OCR
block. It is not a search over all possible keys or a negative exclusion.

## Attribution and limits

The published keys are credited to **George Lasry, Ingo Niebel, Nils Kopal
and Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
with full key provenance in `inputs.json`. Childs's collected intercepts are
the primary source. Earlier unreviewed OCR candidates existed. The bounded
author-paper check found no explicit p132 or p177 A body example; its separate
Eilvese/OUI discussion is credited as station context. No universal
first-decipherment claim is made.

This package distinguishes an ordinary OCR correction, a conservative partial
square, ordinary coordinate repairs, source-erasure fills, and a conditional
extra-coordinate mechanism. Exact re-encryption establishes their arithmetic
and stated prices. It does not establish the unique historical wording,
name, source of an error, or key assignment for any separate challenge.
