# Von Schorlemer: demobilization work inquiry and reply

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

A clear-address request on p122 and an encrypted reply on p155 form a source-linked exchange about von Schorlemer's availability for demobilization work. The earlier request asks whether he can be released to the Trade Ministry; the later administrative-staff reply says he cannot currently be spared. Both native frames and every repair remain explicit. The later reply supports the name and topic; the 33 supplied mask values in the first request remain editorial proposals.

Read the [complete source edition](../../cases/pages/122.md#edition-cases-people-schorlemer-demobilization-inquiry).

## Exact scope

| Quantity | Count |
|---|---:|
| Physical source records | 2 |
| Printed source slots | 412 |
| Modeled plaintext positions | 206 |
| Fixed raw labels | 169 |
| Fixed edited labels | 206 |
| Observed-coordinate substitutions | 8 |
| Source-mask fills | 37 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/schorlemer_demobilization_inquiry/verify.py --verify
python experiments/schorlemer_demobilization_inquiry/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. All readable passages in this package are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
