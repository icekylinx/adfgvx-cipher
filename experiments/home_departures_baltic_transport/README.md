# Wishing to travel home and uncertainty over Baltic transport

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Two native source bodies describe soldiers wishing to travel home without authorization and transport difficulty linked to uncertainty in the Baltic Sea. The second begins an incomplete statement about Graf Goltz. One damaged source glyph in that body is retained as unknown; its unchanged edited reading requires one explicit source-mask fill. The shared unknown GA cell remains globally coupled across their separate references. Missing context and abbreviated source spellings stay explicit.

Read the [complete source edition](../../cases/pages/186.md#edition-cases-military-home-departures-baltic-transport).

## Exact scope

| Quantity | Count |
|---|---:|
| Physical source records | 2 |
| Printed source slots | 424 |
| Unambiguous printed coordinates | 423 |
| Modeled plaintext positions | 212 |
| Fixed raw labels | 208 |
| Fixed edited labels | 209 |
| Observed-coordinate substitutions | 0 |
| Source-mask fills | 1 |
| Insertions, deletions or reordering | 0 |

These counts describe the exact stated key and native frame; they do not count historical numeral identifications. Printed source variants are alternatives within one physical record, not extra records. The complete source text, masks, row boundaries, headers and unchanged keys are in [inputs.json](inputs.json); every coordinate and plaintext position is replayed in [certificates.json](certificates.json).

The [damaged glyph at p186 C1 source index 110](sources/p186_C1_damaged_glyph.png) has an attached lower-right diagonal and cannot safely be transcribed as an observed F. The main source uses `?FAFF`, yielding 88 fixed raw positions out of 91. Filling that slot with F supplies the E in `GEN` at plaintext index 61 and retains the previous edited reading. An explicit F sensitivity branch reproduces the former 89-position, zero-fill result as an assumption excluded from observed-source totals. This correction records uncertainty; it is not a repair-cost reduction or a new plaintext recovery.

## Reproduce

```sh
python experiments/home_departures_baltic_transport/verify.py --verify
python experiments/home_departures_baltic_transport/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verification requires only the standard library and existing repository helpers. Optional PDF verification uses PyMuPDF and Pillow to check the original PDF hash and compare all delivered crop pixels. All readable passages in this package are checked against their literal nonseparator labels; no missing letter is supplied as formatting.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
