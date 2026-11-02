# p191 A: boots and clothing for Oderberg

**Moving one printed five-coordinate group restores the second part of
this supply request.** With four further known-coordinate substitutions
across both parts and twelve printed-dash fills, the edition fixes **196
of 200 plaintext positions**. The corps symbol, two quantity symbols,
and one connective remain unresolved. No square assignment is added.

The request is addressed to a deputy corps command at Breslau. It asks
for boots and heavy clothing, initially for Oderberg, to be made available
on call with advance notice, and requests a wire/radio reply. The repaired
signature is `A.O.K.11`. The exact unit and quantity fields are not
replaced with historically plausible guesses.

Published period key: **George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker**. Source transcription, group-displacement identification,
explicit repairs and certificate: **icekylinx and GPT-6 Astra Pro**.
The author paper was checked for explicit body attribution; no p191
body reference was located. This is not a first historical decipherment
priority claim.

## Source and fixed-length editions

The [source crop](sources/childs_p191_A.png) is Childs printed p191 / PDF
p194. The page heading is **14 November 1918**, while the intercept
header retains its uncertain day:
`LP v ZÖN (06.16 p.m., November ?); 2301 (11/14) 2 TLE`.
Neither the page heading nor the origin field silently replaces that
question mark. Part lengths are 214 and 186 coordinate slots, matching
the literal source exactly.

### Part 1

Untouched source reading:

```text
SELLVXGENXKOMX?XAXKXBRESLAUXXBITTEWEGEND?INGENDERNOTLAGEINBEKLEIDUNGX?0?0?PAARS1IEFELZUNAECHSTNACHXODERBERG
```

Proposed edition:

```text
SELLVXGENXKOMX?XAXKXBRESLAUXXBITTEWEGENDRINGENDERNOTLAGEINBEKLEIDUNGX?0?0XPAARSTIEFELZUNAECHSTNACHXODERBERG
```

`SELLV` is retained literally. Expanding it as *stellvertretendes* in
readable prose is editorial; no `T` is inserted into the cryptographic
edition. The proposal fixes 104/107 positions, changing source coordinate
104 from `D` to `X` for `STIEFEL`, coordinate 140 from `V` to `G` for
`DRINGENDER`, and filling the printed dash at coordinate 63 with `D` for
the separator after the quantity. Coordinates here are one-based.

The remaining unit symbol and the two quantity symbols occupy different
unknown square cells, `GD`, `FV`, and `XX`. Each has the published-key
domain `{2,3,4,7,8,9,Q,Y}`; their assignments must be distinct. The edition
does not select numeric values or change the established digit cells.

### Part 2

Untouched source reading:

```text
UFTERAORVELDUHGMFJST?R?EPPEKLE?DN6AUFA?R?IBERE?T5KELLE??A?RAHT??CNUNKA?T?URTER?E?ENXXA?OEJX1?
```

Moving printed group **12**, `AXFVA`, immediately before printed group
**8**, without changing any coordinate value, gives:

```text
UNTERVORMELDUNGMITST?R?ERBEKLE?DNGAUFA?RUFBERE?TSTELLE??XDRAHT??XFUNKA?TWORTER?ETENXXA?O5KX1?
```

The proposed edition then reads:

```text
UNTERVORMELDUNGMITSTARKERBEKLEIDNGAUFABRUFBEREITSTELLENXXDRAHTX?XFUNKANTWORTERBETENXXAXOXKX11
```

This needs only **two** known-coordinate substitutions, both `F → V`
at original coordinates **127** and **130**, and **eleven** of the
twelve printed-dash fills. The substitutions restore the separator in
`A.O.K.11` and `STARKER`, respectively; the fills supply the erased letters.
The original `BEKLEIDNG` spelling remains; no `U` is inserted.

The remaining connective, plaintext position **64**, retains its entire
domain `{0,2,3,4,7,8,9,O,Q,U,W,Y}`. `O` and `U` could support readable
abbreviations for *oder* and *und*, but neither is chosen. The certificate
provides a globally consistent pair of message witnesses for **every**
domain value, using the same completed square for both parts. Witness
digits are not proposed unit numbers or quantities.

## Selecting the group geometry without the footer

The initial clue was that nineteen ordinary-word coordinate repairs all
fell within one short contiguous source stretch. A local exploratory
group-permutation check exposed the displaced `AXFVA` group. We then
froze **77 ordinary plaintext positions**, excluding the entire
eight-position footer, the uncertain adjective span, and the connective.
No name, unit number or quantity enters the objective.

The completed check evaluates the identity and **every** move of one
complete five-coordinate group among the 37 complete groups, leaving
the one-coordinate tail fixed: **1,333 operation descriptions** and
**1,297 distinct candidate streams**. The cost is the number of observed
coordinates contradicting the frozen ordinary-word mask; erased source
slots do not incur a mismatch cost.

| Source-order model | Ordinary-word coordinate disagreements |
|---|---:|
| Untouched printed order | 19 |
| Group 12 moved before group 8 | **0** |

There is **one distinct global minimizer** within this stated move
family. All minimizing operations are preserved in the geometry
certificate; none is discarded by a footer or numeric preference.

This is a **posthoc, fixed-text consistency comparison**. The ordinary
word anchors came from the damaged message and exploratory analysis.
The unique minimum does not prove every possible German text or every
possible source-error mechanism has been considered.

## Fresh damaged control

The inputs freeze a newly composed 93-character control: 85 ordinary
prose characters and an eight-character synthetic footer. It uses the
same ranks, message length, twelve erased coordinate positions, group
displacement, and 77-position scoring-mask shape. The footer is excluded.
Its arbitrary completed square is used only to construct the synthetic
control and makes no historical digit claim.

The same complete enumeration recovers its true source order as the
unique zero-disagreement candidate. This checks implementation and
sensitivity to this particular group-displacement family. One control
does not establish a general decipherment success rate.

## Accounting and reproduction

| Measure | Part 1 | Part 2 | Total |
|---|---:|---:|---:|
| Source coordinate slots | 214 | 186 | 400 |
| Printed erased slots | 1 | 12 | 13 |
| Untouched raw fixed positions | 102/107 | 76/93 | 178/200 |
| Fixed positions after group move only | 102/107 | 80/93 | 182/200 |
| Proposed fixed positions | 104/107 | 92/93 | **196/200** |
| Full-group moves | 0 | 1 | 1 |
| Known-coordinate substitutions | 2 | 2 | 4 |
| Printed-dash fills | 1 | 11 | 12 |
| Inserted/deleted coordinates | 0/0 | 0/0 | 0/0 |

```sh
python experiments/boots_request/geometry.py --verify
python experiments/boots_request/verify.py --verify \
  --pdf /tmp/adfgvx-childs.pdf
```

`inputs.json` contains the literal source rows, exact group operation,
ordinary-word mask, proposed text and fresh control. The geometry
certificate retains all minima and a digest of all candidate costs.
The source certificate retains the untouched and reordered readings,
every repair in original printed coordinates, and joint bijective-square
witnesses. Re-encryption establishes the stated conditional consistency
and edit costs; it does not establish the historical cause of the group
displacement or remove the four unresolved plaintext positions.
