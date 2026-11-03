# Gomel route derailment and station-train forwarding

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Two source editions concern railway operations: a freight-train derailment blocking both tracks on the proposed Gomel–Bachmatsch route, and a message about forwarding a station train and construction train to Group Winterfeld. The wagon count, train labels, abbreviations and office references remain literal.

Read the [complete source edition](../../cases/military/nov7_derailment_and_trains.md).

## Exact scope

| Quantity | Count |
|---|---:|
| Physical source records | 2 |
| Printed source slots | 540 |
| Modeled plaintext positions | 270 |
| Fixed raw labels | 260 |
| Fixed edited labels | 265 |
| Observed-coordinate substitutions | 3 |
| Source-mask fills | 5 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/nov7_derailment_and_trains/verify.py --verify
python experiments/nov7_derailment_and_trains/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. All readable passages in this package are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
