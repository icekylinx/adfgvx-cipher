# Warsaw station report: conditional recovery of a missing row

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

This package source-reviews p204 C2 and constructs a conditional continuation of the native [part 1](../../cases/pages/204.md#edition-cases-radio-nov16-18-command-inquiries-p204-c1). The [readable case](../../cases/pages/204.md#edition-cases-radio-warsaw-station-missing-row) keeps the native and conditional frames separate.

## Positive result

The source prints 242 slots against an advertised length of 282. A hypothetical 40-slot gap before the terminal `GX` supports a 141-position text about equipment not yet received from home, a Monday-evening handover to the Poles, and WAU personnel transfers. The displayed proposal has 137 fixed labels, requires zero observed-coordinate changes, and fills 36 of the added 40 slots. All 242 original coordinates survive in exact source order.

This is a conditional reconstruction with explicit lost-row and word-completion assumptions. The source does not visibly authenticate where the loss occurred. No final destination, unit identifier or uncommon abbreviation is silently completed.

## Exact bounds

| Quantity | Primary conditional model |
| --- | ---: |
| Physical source records | 1 |
| Printed source slots | 242 |
| Advertised / modeled coordinates | 282 |
| Raw fixed positions | 101 / 141 |
| Edited fixed positions | 137 / 141 |
| Observed-coordinate substitutions | 0 |
| Source-mask fills | 0 |
| Inserted slots | 40 |
| Inserted-slot fills | 36 |
| Remaining inserted masks | 4 |

All 243 contiguous-gap starts are checked against the disclosed template. Three give zero observed changes: starts 240, 241 and 242. Only 240 lies on a five-coordinate group boundary; starts 241 and 242 remain valid coordinate-level alternatives and are not suppressed. Their counts are alternatives for the same physical source, not extra recovered records.

The expected substantive middle wording is stable across these three conditional branches, while the final opaque fields differ. The independent p204 A handover message supplies context only; it is not a ciphertext-completion witness.

## Reproduce

```sh
python experiments/warsaw_station_missing_row/verify.py --verify
python experiments/warsaw_station_missing_row/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Verification checks the unchanged published key, exact source count, all placement costs, source-order preservation, each inserted fill, all readable nonseparator labels and complete global re-encryption witnesses. Optional PDF verification checks the source digest and every delivered crop pixel.

Published Nov16–18 key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016); George Lasry (2017 key list). Earlier unreviewed OCR candidates are preserved. New source review and conditional reconstruction: icekylinx and GPT-6 Astra Pro.
