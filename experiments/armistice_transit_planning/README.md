# Armistice transit and withdrawal planning, pp125-126

Source edition and verification: **icekylinx and GPT-6 Astra Pro**.

This package edits a six-part report dated November 4, received November 5,
about reported armistice transit conditions and plans for the 11th Army.
It also preserves a separate adjacent receipt note. The
[reader edition](../../cases/military/armistice_transit_planning.md) explains
the bodies and their limits. All use the unchanged published `Nov4-6` key.

Six records have ordinary, exact-length cipher frames. The fifth part of
the report has **267 printed slots and a printed length of 267**. Its readable
opening and the opposite pairing phase of its ending motivate a separate
conditional model: one coordinate was omitted from the fractionated stream
before the original 267-slot transposition. This package does not silently
turn that transmitted frame into a 268-slot frame.

## Counts and status

| Record | Printed / source slots | Working plaintext positions | Fixed positions under stated geometry | Known-coordinate substitutions | Source-erasure fills | Conditional interim insertions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| p125 A1 | 244 / 244 | 122 | 122 | 0 | 0 | 0 |
| p125 A2 | 238 / 238 | 119 | 119 | 1 | 0 | 0 |
| p125 A3 | 200 / 200 | 100 | 100 | 1 | 0 | 0 |
| p125 A4 | 212 / 212 | 106 | 105 | 0 | 1 | 0 |
| p126 A5 | 267 / 267 | 134, conditional | 131, conditional | 4 | 2 | 1 |
| p126 A6 | 242 / 242 | 121 | 120 | 2 | 1 | 0 |
| p126 B | 134 / 134 | 67 | 67 | 2 | 0 | 0 |

The source has **1,537 slots, including 1,533 valid received coordinates**.
The six exact-frame records fix 633 of 635 positions; A5's conditional frame
fixes 131 of 134. A5's unmodified 267-slot frame is independently preserved:
it produces 133 paired positions and one final unpaired coordinate, with
an unreadable latter portion. These two A5 readings are not conflated.

The six-part report is based on terms learned from Hungarian newspapers and
asks for the actual agreement. Its assertions are not independently verified
historical armistice provisions. The damaged words and abbreviated grammar
remain visible, including `PUNKT`, `BESONDRER`, `DRINGD`, the `A` before
`SAEMTLICHEN`, and the elliptical `GEMELDETEN` clause. Numerical labels in
the ordinary exact frames and the stable A5 prefix are retained literally.

## Source and arithmetic verification

```sh
python experiments/armistice_transit_planning/verify.py --verify
python experiments/armistice_transit_planning/geometry_audit.py --verify
```

Both commands use Python's standard library. The first verifies bundled
source-image hashes, all manually transcribed rows and advertised lengths,
independent column-height inversion, plaintext domains, coordinate origins,
the exact repair/fill ledger and forward witnesses. It imports no repository
cipher implementation and uses the complete frozen key in `inputs.json`.

The optional PDF check additionally requires PyMuPDF and regenerates all
nine included page/detail images from their recorded rectangles and scales:

```sh
python experiments/armistice_transit_planning/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

PDF SHA-256:
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
Printed pp125-126 are PDF pp128-129. Image-file and uncompressed-pixel hashes
are in `inputs.json`. Both ordinary verification and the full PDF render
check passed when this package was prepared.

## The conditional A5 mechanism

1. Invert the original 267-slot transposition under the published ranks.
2. Insert an unknown coordinate at interim index 136, obtaining 268 coordinates.
3. Read 134 pairs under the unchanged square. This joins the readable opening
   to the readable tail, leaving three unknown plaintext positions.
4. The proposed edition fills the two printed dashes, fills the inserted
   interim coordinate with `F`, and makes four observed-coordinate substitutions.
5. To reproduce the source-shaped witness, fractionate the 134-character
   proposal, remove interim coordinate 136, then transpose the remaining
   267 coordinates using the original column geometry.

Every received coordinate retains its source index. There is no insertion
or deletion in the transmitted frame. `certificates.json` records `null` as
the source origin of the one proposed interim coordinate, while preserving
the exact original origins of all 267 received slots.

`geometry_audit.json` preserves **1,070 completed candidates**: at each of
the transmitted and interim stages, all 268 one-unknown insertions and all
267 single-coordinate deletions were evaluated. Both frozen language models
give their best interim-stage score to insertion positions 136 and 137;
the best transmitted-stage candidate is insertion position 235 and retains
the incoherent tail. The candidate strings and stage distinction are fully
reproducible without models.

For the explicitly retrospective proposed plaintext, all **268 interim
insertion placements** are independently priced. Position 136 is the unique
minimum with four substitutions, two source-erasure fills and one interim
insertion. This conditional template minimum is not an independent crib,
proof of a unique historical omission, or exclusion of more complex errors.

Optional score reproduction uses the frozen 37-symbol marginal models:

```sh
python experiments/armistice_transit_planning/geometry_audit.py --verify \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin
```

The model hashes are frozen in `geometry_audit.json`. Their construction
is documented in the [fixed-search model package](../fixed_search/README.md)
and [radio model package](../radio_domain_model/README.md). Full score
recomputation also passed. Without these arguments, the default audit checks
all strings and template costs but does not recompute stored model scores.
No models were tuned on this report.

## Credit

The period key is prior published work by **George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also reproduced in George Lasry's 2017 key comment linked in `inputs.json`.
The primary source is Childs's collected intercepts. Earlier unreviewed
OCR candidates and selected retrieval strings existed. No explicit p125/p126
body example was located in the bounded
[author-paper attribution audit](../p170_new_methods/lasry_attribution_audit.md).
That does not establish first-decipherment priority. The current contribution
is the manually checked source edition, exact arithmetic and repair ledgers,
and a clearly conditional analysis of the odd-frame pairing failure.
