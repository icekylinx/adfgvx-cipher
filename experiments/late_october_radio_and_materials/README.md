# Late October radio service and Caucasus hide purchasing

Prepared by **icekylinx and GPT-6 Astra Pro**. This package makes a source
edition of eight physical records on Childs printed pp. 74–76 / PDF pp. 77–79.
The date heading is 28 October 1918; several printed reception times are
29 October. The unchanged published October 28–31 key is prior Lasry-team
work and is copied with its provenance in `inputs.json`.

The reader-facing cases are:

- [Late October radio service](../../cases/radio/late_october_radio_service.md):
  daily calls, a garbled CHI message, and a three-part routing query.
- [Caucasus hide purchasing](../../cases/finance/caucasus_hide_purchasing.md):
  exclusive purchasing, return of a signed contract, expense arrangements,
  and the instruction to report at Lederzentrale Magnus in Kiew.

## Scope and costs

| Physical source record | Typed slots | Fixed raw / total plaintext positions | Observed-coordinate substitutions | Printed-dash fills |
|---|---:|---:|---:|---:|
| p74 A | 154 | 77 / 77 | 1 | 0 |
| p74 B | 170 | 85 / 85 | 0 | 0 |
| p74 C1 | 148 | 44 / 74 | 0 | 30 |
| p74 C2 | 130 | 65 / 65 | 2 | 0 |
| p75 A3 | 154 | 77 / 77 | 2 | 0 |
| p75 B1 | 394 | 197 / 197 | 5 | 0 |
| p75 B2 | 204 | 102 / 102 | 0 | 0 |
| p76 A3 | 238 | 118 / 119 | 1 | 1 |
| **Total** | **1,592** | **765 / 796** | **11** | **31** |

There are 1,561 valid typed coordinate symbols. No coordinate is added to a
working typed frame; all advertised lengths agree with the typed frames.
The full published square is unchanged. Counts of fixed positions express
what a given key and frame determine, not an independent correctness score
for the words.

The **30 erased coordinates in p74 C1** support one explicit supplied
candidate, with no disagreement with any observed coordinate. That candidate
is conditional and is not claimed to be unique. Its irregular opening and
abbreviated `DRHTNETZ` / `AGESCHL` remain literal. The raw partial text,
all partial-cell domains, and every fill remain visible.

The raw numeral labels in `5ER` (p74 C2) and `3ORT` (p76 A3) become `DER`
and `DORT` through explicit coordinate substitutions. These are word repairs,
not changes to the key or to independent numerical fields. The verifier
checks the preserved literal reference fields separately.

## p76: typed layer, handwriting and the 258-slot diagnostic

The [annotation detail](sources/p76_A3_annotation_detail.png) distinguishes
238 typed slots from 20 handwritten slots. Under the primary reading, the
handwriting is `FXXFF FDGAD DDDDF AVVFA`, a duplicate of the next four typed
groups. The third handwritten glyph in `DDDDF` is D/O ambiguous at composite
index 87. The primary D transcription and the alternative noncoordinate O
are both retained, with complete diagnostic decodes. The typed-only reading
does not depend on that glyph.

The main typed-only frame excludes handwriting as a separate source layer.
If all 258 slots are instead hypothesized to be transmitted material,
recovering that frame requires excluding 20 slots: 20 observed coordinates
under D, or 19 observed coordinates plus one noncoordinate mask under O.
`inputs.json` explicitly prices that alternative. The package does not claim
a free 20-coordinate transmission deletion or establish who added the
handwriting.

The source therefore has 1,612 slots when the annotation is included, and
1,592 typed slots used in the eight working frames. The primary composite
transcription has 1,581 valid coordinates; the D/O alternative has 1,580.
The accepted typed frames have the same 1,561 valid coordinates either way.

## Reproduce

```sh
python3 experiments/late_october_radio_and_materials/verify.py --verify
python3 experiments/late_october_radio_and_materials/verify.py --verify --pdf /path/to/childs.pdf
```

The default verifier is standard library only. It independently implements
inverse transposition by sorting intermediate indices and forward encryption
by slicing original columns. It checks source rows, geometry maps, partial
pair domains, all word repairs, all printed-dash fills, preserved literal
fields, the two deliberately repaired numeral labels, image byte hashes and
the frozen certificate. It also checks that the D/O annotation alternative
leaves the typed-only source and reading unchanged.

`--pdf` additionally requires PyMuPDF. It checks the complete PDF hash and
re-renders all twelve saved images after clearing the image cache, comparing
the dimensions and exact pixel hashes. PDF SHA256:

```text
157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06
```

The source images include [p74](sources/p74_full.png),
[p75](sources/p75_full.png), [p76](sources/p76_full.png), eight record crops,
and the enlarged handwriting detail. Crop rectangles and scales are stored
in `inputs.json`.

## Prior work and limits

`prior_evidence.json` preserves every pp74–76 row from the earlier unreviewed
OCR screen, together with the original screen hash. That screen already
contained mostly readable p74 A/B and p75 A3 candidates. The complete source-
correct routing and purchasing parts, exact source-layer distinction and
coordinate repair ledger are the present additions. No universal first-
decipherment priority is asserted.

The source identifies names and reference strings under the published key;
it does not independently identify the full biographies or corporate
histories behind them. `WOLTERS` is retained without choosing whether its
last S is part of a surname or a grammatical ending. The reader pages
separate raw output, coordinate-priced edited output, readable German and
conditional interpretation, including the full p74 C1 fill candidate and
p76 source-layer alternative.
