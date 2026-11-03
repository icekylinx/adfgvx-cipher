# Wishing to travel home and uncertainty over Baltic transport

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Two native source bodies need no coordinate repairs: one describes soldiers wishing to travel home without authorization; the other links transport difficulty to uncertainty in the Baltic Sea and begins an incomplete statement about Graf Goltz. The shared unknown GA cell remains globally coupled across their separate references. Missing context and abbreviated source spellings stay explicit.

Read the [complete source edition](../../cases/military/home_departures_baltic_transport.md).

## Exact scope

| Quantity | Count |
|---|---:|
| Physical source records | 2 |
| Printed source slots | 424 |
| Modeled plaintext positions | 212 |
| Fixed raw labels | 209 |
| Fixed edited labels | 209 |
| Observed-coordinate substitutions | 0 |
| Source-mask fills | 0 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

## Reproduce

```sh
python experiments/home_departures_baltic_transport/verify.py --verify
python experiments/home_departures_baltic_transport/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. All readable passages in this package are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
