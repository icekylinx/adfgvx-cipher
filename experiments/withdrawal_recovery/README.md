# Withdrawal-order fragments and a radio-station move

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Seven visually checked source records on Childs's printed pp163–164 preserve
1,581 coordinate slots. Six records can be read in explicit even-length frames;
their published 7–9 November key fixes 608 of 730 raw positions. The seventh is
an unnumbered, jammed, 121-coordinate fragment and receives no complete-message
decryption.

The source material concerns keeping Crajova and Bukarest occupied until the
last moment, a withdrawal in one move, the Bucharest garrison, Danube guard
boats, projected Scholtz and army headquarters movements, and a radio station's
onward march to Temesvar. The new work is a source edition and exact account of
its proposed repairs. It does not solve the open p170 A challenge.

## Source and reconstruction

| Record | Raw fixed positions | Known-coordinate substitutions | Erasure fills | Principal result |
| --- | ---: | ---: | ---: | --- |
| p163 A13 | 126/134 | 10 | 6 | Crajova and Bukarest to remain strongly occupied; opening unresolved; received 268 differs from header 278 |
| p163 A14 | 121/122 | 5 | 1 | Final evacuation in one move; the garrison clause continues into part 15 |
| p163 A15 | 36/117 | 2 | 63 | Explicitly conditional 91-position prefix joins the garrison to Generalkommando {5/6}3 and Scholtz; final 26 positions uncompleted |
| p163 unnumbered | — | — | — | Jammed fragment between parts 15 and 17; odd length 121, no full frame asserted |
| p163 A17 | 125/132 | 16 | 6 | Danube boats and projected Scholtz move to Calimanesti on 13 November |
| p163 A18 | 131/155 | 21 | 24 | Hermannstadt, Kronstadt and Sinaia headquarters movements; corps and date digits separately conditional |
| p164 B | 69/70 | 2 | 0 | Dismantle station, march to Temesvar, call again once established |

Every source glyph remains in `inputs.json`. The two edit columns describe the
reader's proposed edition, not alterations to the transcript. A raw fixed
position can contain a transmission garble; it is not automatically a correct
historical plaintext letter.

The part 15 prefix was reconstructed from its surviving half-coordinate domains
and the sentence crossing the part14 boundary. Its coherent proposed wording
is substantially more informative than the raw singleton string, but 63 filled
coordinates remain editorial choices. No uniqueness claim is made.

Part13 uses the 268 visible slots, with no ten-coordinate insertion to match the
278 header. The header discrepancy remains open. An unproved original-length
assumption must not be hidden by a fluent reconstructed ending.

## Shared digit inference

The already published historical layer in
[`military_context.json`](../p170_continuation/military_context.json) assigns
`VF=6`, `XA=5` under the 7–9 November square. This package propagates that same
assumption; `data/keys.json` is unchanged.

- Part15's unchanged `VF` cell gives corps 63.
- Part18's unchanged `XA` cell gives 15 November. Its proposed corps 63 also
  requires an explicit one-coordinate repair of raw `K` to cell `VF`.
- p164 B's unchanged `XA` cell gives 0500.

The inference also makes a raw garbled part17 position read `6`; the edition
independently proposes `X` there and counts its coordinate substitution. The
certificate includes this inconvenient consequence rather than selecting only
helpful propagated digits.

## Reproduce

```sh
python3 experiments/withdrawal_recovery/verify.py --verify
```

The verifier uses only the Python standard library. It reconstructs column
offsets independently, checks every raw domain against the separate project
reader, checks the printed-crop hashes, verifies every edited coordinate, and
builds global witnesses using one injective square. All fully determined
conditional editions re-encrypt exactly. The arbitrary remaining-coordinate
fills in a witness are expressly not proposed plaintext.

Add `--pdf /path/to/childs.pdf` to verify the complete inspected scan's hash.
The focused crops are retained in [`sources/`](sources/).

## Credit

The original intercepts are Childs's material. The period key retains the
attribution to George Lasry and colleagues recorded in `data/keys.json`.
The inspected author copy of Lasry, Niebel, Kopal and Wacker's 2017 paper does
not reproduce these p163/p164 B messages. This is a new repository edition,
with no claim that the messages were never read by historical or earlier
modern analysts. Retrieval, image review, reconstruction and verification here
are by **icekylinx and GPT-6 Astra Pro**.
