# Radio notices, Tiflis personnel and internment on p230

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Four source-length telegrams on Childs p230 become complete literal readings under the published Nov28–Dec1 square. All 490 coordinates are preserved: no coordinate substitution, source-mask fill or frame change is needed. The source itself gives two first-group readings for C; both are retained.

Read the [complete source edition](../../cases/pages/230.md#edition-cases-radio-nov30-radio-personnel).

## Exact scope

| Quantity | Count |
| --- | ---: |
| Physical source records | 4 |
| Printed source slots | 490 |
| Modeled plaintext positions | 245 |
| Fixed raw labels | 245 |
| Fixed edited labels | 245 |
| Observed-coordinate substitutions | 0 |
| Source-mask fills | 0 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/nov30_radio_personnel/verify.py --verify
python experiments/nov30_radio_personnel/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. The seven readable passages across these two packages are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are preserved separately. This is a source edition and explicit repair review, not a claim of universal first-decipherment priority.
