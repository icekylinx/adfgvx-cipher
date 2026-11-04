# p137 B: station-staff query

Source review, recovery and verification: **icekylinx and GPT-6 Astra Pro**.
The unchanged **Nov4–6** key is credited to Lasry, Niebel, Kopal and Wacker
(2016), and Lasry's 2017 key list; its full provenance is frozen in
[`inputs.json`](inputs.json). The earlier unreviewed corpus OCR is frozen
in [`prior_ocr.json`](prior_ocr.json). This edition supplies a newly reviewed
source, conditional source map and readable query, rather than changing
the published key.

The [case](../../cases/pages/137.md#edition-cases-radio-p137-station-staff-query) asks whether the
station is still staffed by its former personnel and requests an answer
at the unresolved literal `17?0`, closing `EILVESE`.

## Source and conditional frame

Childs prints 135 cipher slots: 133 observed coordinates and two dashes,
against `RIZI-138`. The full header, clear continuation and footer are kept
outside the cipher body. The primary 138-slot model moves the final
five-slot group `VDF--`, source 130–134, to boundary 105 of the retained
130-slot stream, then appends three unknown coordinates. No source slot
is dropped or reused. The movement is conditional; the manuscript does
not mark it as a cancellation or correction.

| Primary layer | Fixed positions | Additional operations after the frame |
| --- | ---: | --- |
| Raw | 64/69 | None |
| Edited | 68/69 | Three observed substitutions, two printed-mask fills, two inserted-slot fills |

The minimum-price certificate considers each of 27 printed group starts,
131 destinations after removal and 136 boundaries for three contiguous
missing slots: **481,032** maps. For the fixed lexical proposal, exactly
five maps attain the three-substitution minimum: group 130, destination
103–107 and gap 135. All give the same edited stream. The primary 105
choice is a printed group/row boundary, not a uniquely proved position.
The certificate keeps every minimum, per-position domains, source maps
and separate repair ledgers. Its digest and histogram cover every price
in the declared finite scope, including unsuccessful maps.

One inserted coordinate stays unassigned. Under the unchanged complete,
injective square, plaintext position 58 has domain `036OQY`. All 30 full
completion witnesses (five maps times six labels) encrypt and decrypt
exactly and map back to the same three observed substitutions per map.
Those witnesses fill the last coordinate only to check compatibility;
the primary reading retains `17?0` and counts only two inserted-slot fills.
The native odd 135-slot diagnostic separately records its orphan coordinate.

The accepted p127 B1 old-personnel notice provides independently preserved
topical context. Its input and certificate hashes are pinned. Its LP/NKJ
header differs from this OSM/OUI route; no copy or proved reply relation
is claimed, and it supplies no coordinates or plaintext here.

## Reproduction

From the repository root, standard-library checks plus the repository's
cipher and presentation utilities:

```sh
python3 experiments/p137_station_staff_query/verify.py --verify
```

The verifier recomputes every map using prefix/suffix mismatch sums, checks
all five exact minima against the independent peer audit, prices every
change, verifies all 30 global-key witnesses, and checks the actual case
Markdown source, raw, edited and readable strings. The time-field question
mark survives German-display normalization; sentence punctuation is removed
separately.

An independent peer used column-bucket encoding, a standalone C++ integer
enumeration and a separately implemented ragged-column decoder, without
importing the package verifier or repository cipher. The frozen
[`peer_audit.json`](peer_audit.json), input, source and results preserve that
review. To rerun its finite pricing independently:

```sh
c++ -O2 -std=c++17 experiments/p137_station_staff_query/peer_price.cpp -o /tmp/adfgvx-p137-peer
/tmp/adfgvx-p137-peer experiments/p137_station_staff_query/peer_input.txt
```

The complete expected output is [`peer_result.txt`](peer_result.txt):
481032 models, minimum 3 and exactly five listed maps. Absolute scratch
paths in `peer_input.json` describe the peer's original source audit;
reproduction uses the frozen local inputs and does not open those paths.

## Original-source pixels

The source is [Childs's PDF, printed p137 / PDF page 140](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
`source_audit.json` preserves every reviewed glyph. `inputs.json` records
the original PDF size/SHA-256 and exact crop rectangle, page, `Matrix(4,4)`
recipe, dimensions and RGB digest. The newly made crop remains a local
review artifact; `external_pdf_reference` records its provenance without
requiring or opening a repository PNG.

Default verification checks metadata and cipher evidence, **not source
pixels**. With an independently obtained original PDF and PyMuPDF installed:

```sh
python3 experiments/p137_station_staff_query/verify.py --verify --pdf /path/to/childs.pdf
```

This additionally checks the PDF's exact bytes and re-renders the crop to
compare its RGB pixels. Both modes report what was actually checked.
These checks establish compatibility with the stated source model and
candidate, rather than unique historical wording or a proved fault mechanism.
