# Native restoration of the p151 E2 operations-map fragment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source restoration and verification: icekylinx and GPT-6 Astra Pro.**

The [complete case](../../cases/radio/nov9_operations_map_sheets.md) gives
the four reading layers, exact coordinate changes and the coupled numerical
alternatives. This package restores the **224 actually printed slots** from
an earlier 225-slot OCR record. The difference is OCR group 16 `GGVVXX`
versus the visible five-coordinate `GGVVX`; no manuscript coordinate is
excluded.

The unchanged Nov7–9 key yields 108/112 fixed raw labels. Two observed
substitutions and two source-mask fills yield 110/112 fixed edited labels.
The two remaining positions are cells VF and XA, which take 5/6 in opposite
orders under one injective square. The footer remains `1D70??`.

## Source evidence and files

[inputs.json](inputs.json) retains the complete grouped manuscript
transcription, header, published key, source PDF digest and the exact
reviewed crop specification. [ocr_snapshot.json](ocr_snapshot.json)
retains the earlier digital evidence, and [certificates.json](certificates.json)
contains the native arithmetic, source maps, all changes and both global
completion witnesses. [catalog_proposal.json](catalog_proposal.json) is
only a proposed new entry for this one physical source; no global catalogue
is edited by this package.

The complete page and the E2 crop were visually inspected. This package
includes the reviewed crop linked below. Its source is PDF page 154, rectangle
`[65,695,495,790]` points, rendered at scale 4. The expected pixel digest was
computed from that inspected render. Readers can reproduce it directly
from the pinned source PDF.

## Reproduction and limits

```sh
python experiments/nov9_operations_map_sheets/verify.py --verify
python experiments/nov9_operations_map_sheets/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

Default verification uses the standard library and repository files. It
explicitly reports the pixel check as skipped without `--pdf`. The optional
PDF check requires PyMuPDF and compares the regenerated dimensions and RGB
bytes' digest with the actually reviewed render. It does not silently claim
a pixel check when the PDF is unavailable.

The source has no asserted structural repair, and all 222 valid coordinates
remain in native order. Two of them are explicitly changed by the optional
word edition. The uncertain place letters are lexical proposals within
surviving half-pair domains. No first part, exact administrative reference,
unit interpretation or successful map shipment is supplied.

Historical source and published-key credits, earlier OCR provenance and
all limitations are retained in the inputs and the complete case.

**Reviewed source crops:** [p151_reviewed.png](sources/p151_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
