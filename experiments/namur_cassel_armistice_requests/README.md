# Namur arrival, Cassel transport and armistice-information requests

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

These four surviving source bodies report an arrival at Namur, direct prompt transport arrangements to Cassel, and request the local armistice conditions again. The Namur telegram explicitly lacks its second part; its first and third parts are presented without bridging that gap. Literal office labels, an opaque transport field and source-length spellings remain visible.

Read the [complete source edition](../../cases/military/namur_cassel_armistice_requests.md).

## Exact scope

| Quantity | Count |
|---|---:|
| Physical source records | 4 |
| Printed source slots | 658 |
| Modeled plaintext positions | 329 |
| Fixed raw labels | 326 |
| Fixed edited labels | 328 |
| Observed-coordinate substitutions | 7 |
| Source-mask fills | 1 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/namur_cassel_armistice_requests/verify.py --verify
python experiments/namur_cassel_armistice_requests/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. All readable passages in this package are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
