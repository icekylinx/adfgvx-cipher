# Radio reception instructions and a brief no-events report

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The two-part p224 A telegram asks for experienced listeners, clear transmission and a suitable reception wavelength. The separate p224 B report states that nothing special has happened. This edition preserves the source-length spellings SICERES and MORENMELDUNG and the date-like field 17XJJ.

Read the [complete source edition](../../pages/224.md#edition-cases-radio-nov27-receiving-instructions).

## Exact scope

| Quantity | Count |
| --- | ---: |
| Physical source records | 3 |
| Printed source slots | 506 |
| Modeled plaintext positions | 253 |
| Fixed raw labels | 250 |
| Fixed edited labels | 253 |
| Observed-coordinate substitutions | 14 |
| Source-mask fills | 3 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/nov27_receiving_instructions/verify.py --verify
python experiments/nov27_receiving_instructions/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. The seven readable passages across these two packages are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are preserved separately. This is a source edition and explicit repair review, not a claim of universal first-decipherment priority.
