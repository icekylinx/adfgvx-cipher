# p228 B2 — Demobilization district and formations

[All cases](../README.md) · [The three-part Neuhof telegram](neuhof_demobilization.md) · [Reading conventions](../../docs/reading-conventions.md)

**Recovery and review: icekylinx and GPT-6 Astra Pro, 4 November 2026.**
Moving five printed mask slots exposes a substantial continuation of the
Neuhof demobilization instruction. The unchanged November 28–December 1 key
fixes **90/132 raw positions** in this conditional frame. The word proposal
fixes **121/132 positions**, comprising **95 proposed word positions** and
26 retained labels in other fields. Its five observed-coordinate substitutions
and 32 printed-mask fills are individually recorded.

Two shared-reference steps now extend that proposal to **125/132 positions**:
the first part supplies the order suffix and the first enclosure number.
Together with the later numeral interpretation, the latter passage reads
**Anlg. 1 u. 2**. Both steps use complete original donor pairs and add four
mask fills, with no additional observed-coordinate substitution.

The earlier edition proposed only the first 33 positions. This continuation
adds the phrases `DIE NACH ANLG`, `DES ERL`, `IM BEREICH DES STELLV`,
`DEMOBILMACHENDEN` and the suffix `FORMATIONEN`. The intervening command
designation and the prefix `???CK` remain unresolved.

## Readable fragments

**Conditional interpretation — readable German after the shared-reference and enclosure transfers, with the declared numeral interpretation; ellipses omit fields shown below:**

> An Strecke Hanau–Fulda demobil gemacht. Die nach Anlg. 1 u. 2 des Erl. […] im Bereich des stellv. […] demobilmachenden ???CKformationen […]

The wording concerns formations undergoing demobilization within a deputy
command's district and refers to two enclosures and an order. The incomplete
compound ending in `FORMATIONEN` does not identify a specific formation type.
The [third part](neuhof_demobilization.md#b3-routing-to-neuhof) continues with
`DESFELDHEERES` and directs the relevant items toward Neuhof. The new fragment
helps connect the instruction's two previously readable ends; it does not
supply the remaining reference values or establish that the order was executed.

## Source and frame

Childs, printed p228 / PDF p231, section B2, `2 TL RICHI-264`, under
`30th NOVEMBER, 1918.` The parent header reads
`B) ZON v BSL (01.33 a.m., December 1st); NO 152 1512 3 TLE`.
The body contains exactly **264 slots: 221 observed coordinates and 43 dashes**.

<details>
<summary>Literal source transcription</summary>

**Source transcription — unchanged 264-slot body:**

```text
XFXDD VAVXV AXDVX FXVVA FGXVV VGFVG VDVDA GVFDF
AGAVX XAGDD FGFAA GAXXV ADDFG FGVFX VVGGG FDGAV
XGVXD DXXFA AXFGV XDVGD DAGGV FAAAX FDAGV VDDGV
GVGGA FFDGA -AVVG FGVFG DVXAG XFXGG GFGFG ADXFV
DDVFV G-DAF GXFXX GGVFV FVGVD -GDXG FF--- -----
----- ----- ----- ----- DFGFF VAAVX XGFFD FGFFV
XAVAA FVDXX FF--- ----- ----
```

</details>

All indices are zero based, with end-exclusive ranges. Remove the existing
five printed masks at source[195:200], then insert them at boundary246 of
the shortened 259-slot stream. They occupy model[246:251]. No source slot
is dropped or added; all 221 observed coordinates retain their values and
relative order.

This is a conditional placement of a printed mask group, not an OCR correction.
Any five contiguous masks starting at source192 through215 give the same
ciphertext: 24 different mask-identity maps are preserved. The printed page
does not independently select the new location or any one of those identities.

## Raw and edited output

<details>
<summary>Source and cipher evidence</summary>

**Raw output — mask relocation, unchanged published key; 90/132 fixed positions; no observed substitutions or fills:**

```text
A?ST??CKEHAN??FULDAD??OBILGED??HTDIB??CHANLG??UJDESE??Y2680Y??GEHY0Y??MBEREI??DESSTE???YYKDO???MX4AK???OBILM???ENDEN???CKF?????I4NE?
```

**Edited output — same frame; five observed substitutions and 32 printed-mask fills; 121/132 fixed positions:**

```text
ANSTRECKEHANAUFULDADEMOBILGEMACHTDIENACHANLG??UJDESERLY2680Y??GEHY0Y?IMBEREICHDESSTELLVYYKDO???MX4AKDEMOBILMACHENDEN???CKFORMATIONEN
```

</details>

| Source index | Printed | Proposed | Word position |
|---:|:---:|:---:|---|
| 148 | G | D | `O` in `FORMATIONEN` |
| 179 | V | D | `A` in `DEMOBILMACHENDEN` |
| 181 | V | F | `M` in `FORMATIONEN` |
| 240 | X | V | `E` in `DIE` |
| 251 | F | X | `M` in the opening `GEMACHT` |

The 32 fills fix 31 previously unresolved positions. **Position4, R in
STRECKE, has both coordinates missing** and consumes two printed-mask fills;
it lies inside the previously proposed opening. Every one of the **22 newly
fixed tail-word positions** has one observed half-coordinate. The other five
repairs change observed values and remain separate from the fills.

The 11 unresolved positions are **44,45,60,61,68,92,93,94,116,117,118**.
The three positions before `CKFORMATIONEN` are deliberately unfilled.
The known numeral labels, `Y` labels and `X4AK` field are not assigned
historical numbers by this edition. A complete arbitrary re-encryption
witness checks the arithmetic without claiming the remaining erased values.

## Comparison and reproducibility

| Frame and proposal | Raw fixed | Edited fixed | Observed substitutions | Printed-mask fills | Proposed word positions |
|---|---:|---:|---:|---:|---:|
| Earlier native frame, opening only | 89/132 | 99/132 | 5 | 10 | 33 |
| Relocated frame, same opening only | 90/132 | 99/132 | 1 | 10 | 33 |
| Relocated frame, new word spans | 90/132 | 121/132 | 5 | 32 | 95 |

The earlier edition and its literal displays remain available. The improved
opening price is a useful check independent of the newly proposed tail words;
it does not prove unique historical geometry. Blind mask-placement searches
and fresh source-shaped controls are described in the
[recovery package](../../experiments/p228_demobilization_fragment/README.md).

[Inputs](../../experiments/p228_demobilization_fragment/inputs.json) and
[certificates](../../experiments/p228_demobilization_fragment/certificates.json)
retain every coordinate origin, word span, repair, remaining domain and
mask-ownership alias. The original PDF and the previously published source
crop have matching authenticated pixels; no new source image is duplicated.

**Reproduction command — verifies the unchanged source, frame, prices and complete witnesses:**

```sh
python experiments/p228_demobilization_fragment/verify.py --verify
```

## Shared reference and enclosure witnesses

The first part has the fully observed reference fragment `P680YX4GEH`;
B2 has `2680Y??GEH`. If these denote the same order-reference field,
B1 supplies the two missing labels `X4` at B2 positions 60–61. The
[separate certificate](../../experiments/p228_demobilization_fragment/reference_witness.json)
records the original donor pairs `GX` and `GD`, fills source255 with `G`
and source210 with `D`, and verifies both parts under the same unchanged key.
This optional layer reaches **123/132 fixed positions**, with **34 printed-mask
fills and the same five observed substitutions**. The primary layer stays at
121/132. The observed `P` versus `2` disagreement is retained; neither label
receives a numerical interpretation. These are separate parts with a proposed
shared reference, not duplicate receptions. Reproduce with
`python experiments/p228_demobilization_fragment/verify_reference.py --verify`.

The first part also has the fully observed `ANLGYX`. Its two final pairs,
`AX` and `GX`, fit B2's `ANLG??UJ` at positions 44–45. Transferring them fills
source253 with `A` and source208 with `X`, producing `ANLGYXUJ`. This
**enclosure extension fixes 125/132 positions**, with five observed
substitutions and 36 mask fills in total. Positions 68, 92–94 and 116–118
remain unresolved.

Under the [shared calendar and unit interpretation](../../experiments/late_november_calendar_and_units/README.md),
the enclosure field reads `ANLGX1U2`, and B2's order reference reads
`3067X18GEH`. B1 has `P067X18GEH`; that initial P/3 disagreement remains.

<details>
<summary>Combined conditional reading</summary>

**Edited output — mask relocation, five observed substitutions, 36 printed-mask fills and the shared numeral interpretation:**

```text
ANSTRECKEHANAUFULDADEMOBILGEMACHTDIENACHANLGX1U2DESERLX3067X18GEHX7X?IMBEREICHDESSTELLVXXKDO???M18AKDEMOBILMACHENDEN???CKFORMATIONEN
```

The verifier checks both original donor pairs, every added fill, the displayed
word spans and complete witnesses under both remaining square assignments.

</details>

Historical ciphertext: **J. Rives Childs**. Published period key:
**George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**. The earlier Neuhof
source edition and its attribution are preserved. Mask-frame recovery,
continuation and independent review: **icekylinx and GPT-6 Astra Pro**.
