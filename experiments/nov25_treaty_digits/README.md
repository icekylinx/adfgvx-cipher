# Article XII and two Nov25–28 numeral cells

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [Tiflis telegram](../../cases/caucasus/p218_A.md) paraphrases the
withdrawal condition in **Article XII** of the 11 November armistice.
Its received article-number pairs are `FX VG`, labelled `J1` by the
published Nov25–28 square. Interpreting these pairs as **1 and 2** restores
the reference without changing either pair. The earlier edition reached
the same article number through three coordinate substitutions.

This conditional interpretation extends the existing
[`VD=J` letter constraint](../nov25_letter_constraint/README.md) across its
complete snapshot of **23 reviewed records, 3,176 plaintext positions**.
The published key and source editions retain their original data and costs.

## Documentary identification and source cost

Article XII distinguishes withdrawal from former Russian territory by
making its timing depend on the Allies' assessment of the internal
situation. That distinctive condition appears in p218 A1–A2. It is printed
under XII in both the
[German text](https://germanhistorydocs.org/de/die-weimarer-republik-1918-1933/waffenstillstandsbedingungen-11-november-1918)
and the [U.S. diplomatic edition](https://history.state.gov/historicaldocuments/frus1919Parisv02/d1).
The historical identification already informed the earlier reading; the
new contribution is its use as a shared-square constraint.

| p218 A1 position | Received pair and source indices | Earlier numeral repair | Conditional treatment |
| --- | --- | --- | --- |
| 47 | `FX`, 64 and 163 | `FX→VG`, two coordinate changes | Keep `FX`; interpret as 1 |
| 48 | `VG`, 114 and 236 | `VG→VX`, one coordinate change | Keep `VG`; interpret as 2 |

All indices are zero-based. The missing `E` in received `RO?M` still needs
its earlier one-coordinate fill. A1 therefore costs **seven observed
changes and one fill**, down from ten changes and one fill. The complete
three-part reading costs **13 observed changes and three fills**, down
from 16 and three. Its opening raw-label reference `163` becomes `2??`;
the final two values remain unassigned.

## Consequences across the shared traffic

| Record | Received field | Conditional reading |
| --- | --- | --- |
| p219 A1 | `ETXINTENDXJJFIALA` | `ETXINTENDX11FIALA` |
| p219 B | `FELDINTENDXAXOXKXJJ` | `FELDINTENDXAXOXKX11` |
| p221 A6 | `JAJJ6J4` | `1A11?1?` |
| p222 A2 | `OHLXROEMXJAXJJ201XGEHXOPXX` | `OHLXROEMX1AX11??2XGEHXOPXX` |
| p223 A2 | `J1Y KRONEN FUER JYY LEI` | `12? KRONEN FUER 1?? LEI` |
| p224 C1 | `AOKJJ` | `AOK11` |

The three 11th-Army addresses are consistent consequences outside the
treaty passage. They are not additional assignments. The monetary
question marks in the two p223 A2 amounts all denote the same cell;
the result does not identify a complete exchange rate. The certificate
also records every affected reference position omitted from this short table.

The two pairs occur **38 times in the original streams**. Of these,
**35 survive as numeral interpretations** in the revised editions,
including the two article anchors. Three inconvenient uses remain visible:
`JNNEREN`, `MITGETEILJ` and `SOLLJE` become `1NNEREN`, `MITGETEIL1` and
`SOLL1E` in the raw conditional view. Their earlier ordinary-word repairs
remain unchanged. No new coordinate correction or erasure fill is added.

The prior 12 unassigned cells become ten. Their common remaining domain
is `03456789QY`, giving **10! = 3,628,800** globally bijective square
completions under the retained letter anchors and the two treaty-derived
assignments. This is an algebraic count, not a count of historically
plausible keys. Every occurrence of a cell must use the same value.

## A separate Breslau unit interpretation

A newly checked local decree places the **VI Army Corps deputy general
command in Breslau on 11 November 1918**. It appeared in *Der Gebirgsbote*,
no. 129, 13 November 1918, p1. The [institutional PDF](https://bibliotekacyfrowa.pl/Content/60534/PDF/directory.pdf),
[masthead](sources/gebirgsbote_1918_129_title.png) and
[decree](sources/breslau_vi_corps_nov11.png) supply a November witness for
the command previously documented from July 1917.

Identifying p224 C2's Breslau recipient with this command assigns `GA=6`.
This additional conditional layer fixes **three more received numeral
positions**: the corps number, p223 A3's first mark amount (`6?`), and
one position in its final departmental reference (`1??6X11X1?`). It adds
no source changes. The fourth raw occurrence is `BERLI7`; its previous
one-coordinate repair to `BERLIN` remains unchanged.

The resulting nine unknown cells have the common domain `0345789QY`,
giving **9! = 362,880** square completions. The
[separate certificate](breslau_certificate.json) retains the treaty-only
layer as its dependency. The contemporary decree supports the command's
location; it does not reproduce the personnel order or identify its officer.

## The Kiev report outside the original snapshot

The separately reviewed [p219 C report](../../cases/military/p219_kiev_unrest.md)
contains received `PEDF9?RA`. The existing `VD=J` assignment gives
`PEDFJ?RA` without source changes. Its optional `PETLJURA` proposal now
needs **two observed-coordinate substitutions and 18 inserted-slot fills**,
instead of four substitutions and 18 fills. The retained pair is supplied
by source 181 V and 212 D. The remaining corrections are source 10 V→X
and 155 A→F.

The [separate calculation](kiev_certificate.json) rechecks all 81 declared
source-annotation models under the shared partial square. Four models
still tie, and the opaque field still has two readings, now `6?` or `B?`.
The signature and other numerical fields remain unresolved. This is an
additional source outside the original 23-record snapshot; its positions
are not included in the 35-plus-three numeral totals above.

## Reproduce

```sh
python experiments/nov25_treaty_digits/verify.py --verify
python experiments/nov25_treaty_digits/verify_breslau.py --verify
python experiments/nov25_treaty_digits/verify_kiev.py --verify
```

The verifier checks the complete earlier dependency chain, independently
reads its source geometries, reverses only the three specified numeral
substitutions, inventories every original `FX`/`VG` occurrence, and
re-encrypts raw and revised views under one shared full-square witness.
Unassigned witness values are marked as arbitrary. It also checks the
live p218 German reading and every displayed case-field excerpt against
their coordinate-derived streams.

For pixel comparison with the complete historical PDF, pass
`--historical-pdf /path/to/gebirgsbote_1918_129.pdf` to `verify_breslau.py`.

Published key credit remains with **George Lasry, Ingo Niebel, Nils Kopal
and Arno Wacker**. The article identification and original source reading
precede this propagation; neither is recounted as a newly discovered
message.
