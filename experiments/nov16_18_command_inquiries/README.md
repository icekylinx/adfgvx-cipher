# Armistice acknowledgments, personnel and Warsaw radio inquiries

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Seven native source records cover an armistice-receipt query, nightly radio listening, an inquiry for Captain von Borries, the location of the Warsaw general government, and radio equipment and personnel. Two previously OCR-damaged short messages become clear when their actually printed final groups are restored. All unresolved fields and missing-letter spellings remain explicit.

Read the [complete source edition](../../cases/radio/nov16_18_command_inquiries.md).

## Exact scope

| Quantity | Count |
|---|---:|
| Physical source records | 7 |
| Printed source slots | 1070 |
| Modeled plaintext positions | 535 |
| Fixed raw labels | 517 |
| Fixed edited labels | 526 |
| Observed-coordinate substitutions | 9 |
| Source-mask fills | 5 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/nov16_18_command_inquiries/verify.py --verify
python experiments/nov16_18_command_inquiries/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. All seven readable passages are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are preserved separately. This is a source edition and explicit repair review, not a claim of universal first-decipherment priority.
