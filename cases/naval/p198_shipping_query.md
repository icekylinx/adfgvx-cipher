# p198 A — Prices and freight for wheat delivered to Poti

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Conditional recovery: icekylinx and GPT-6 Astra Pro.** Source-defined group
repairs and the registered **Nov7–9 key** recover a shipping-price query from
the irregular transmission on printed p198. The 244-slot model fixes
**111/122 raw positions**; five observed-coordinate substitutions and seven
fills give **118/122**.

## p198 A

**Readable German — conditional word edition; received spelling, names and quantity retained:**

> Drahtet Kaufpreis, Schiffsfracht, Transporversicherung fuer Ende Sept. mit Dampfer ??PASIA und IBALIA Poti gelieferte 11??0K Pud Weizen.

The query asks for the purchase price, ship freight and transport insurance
for wheat delivered to Poti at the end of September. `TRANSPOR` lacks the T
of ordinary German *Transport*; the readable text preserves that spelling.
The steamer labels and `11??0K` quantity are retained exactly. No vessel
identity or numerical tonnage is supplied.

This is section **A**. The original p198 challenge is section **D** and has
its own separate status.

## Source-defined frame

The source advertises `RICHI-244` but prints **247 glyph slots**. Its first
two groups have six glyphs (`XADTAF`, `AATAGV`), `XGAX` has four, and the
ending contains six coordinates. The annotation says **Very irregular spark**.
All eight noncoordinate letters and both dashes remain in the literal source.

The selected conditional model excludes source indices **4, 8, 245 and 246**,
then inserts one unknown coordinate before original source index **92**.
Thus it excludes three observed coordinates and one invalid T, adds one
unknown slot, and retains all other source slots in order. The frame has
244 slots and uses the unchanged registered Nov7–9 square and ranks.

**Raw output — conditional 244-slot frame; every printed mask and inserted slot unassigned:**

```text
DRAHT?TKAUFPREISS?HIFFSFRAC0TTRA?SP?RVERSICH?RUNGFUEYENDESEPTX?GTDAMPFER??PASIAUNDIBALIAPOTIXIELIEFERTEX11??0KXPUDWEIZE?XX
```

**Edited output — same frame; five observed substitutions, six printed-mask fills and one inserted-slot fill:**

```text
DRAHTETKAUFPREISSCHIFFSFRACHTTRANSPORVERSICHERUNGFUERENDESEPTXMITDAMPFER??PASIAUNDIBALIAPOTIXGELIEFERTEX11??0KXPUDWEIZENXX
```

The word corrections repair `FRAC0T`, `FUEY`, `?GT` and `IELIEFERTE`.
The numeral label `0` is changed only within the explicitly repaired word;
the separate `0` in the quantity remains unchanged.

Two source glyphs at indices 49 and 192 are C-like rather than clearly barred
G. The primary transcription preserves both as literal C and treats them as
masks. The ordinary word `WEIZEN` supplies one fill; the corresponding vessel
letter remains unknown. All four C/G combinations are checked separately.
Reading source 192 as G would give `?TPASIA`, but that alternative is not
silently selected in the primary edition.

## Four tied source maps

Every choice of one exclusion in each initial six-glyph group, one insertion
boundary in `XGAX`, and two exclusions in the final six coordinates is
checked: **2,700 maps**. The word template has four minima at five observed
substitutions. All exclude source 4 and the final 245–246, insert before 92,
and exclude one source position from `{6, 7, 8, 9}`.

All four give the same displayed raw and edited labels. The selected map
excludes only three observed coordinates; the others exclude four. Their
uncertainty differs: the initial `?` of `??PASIA` lies in `MPRUWY` for the
selected map, but one tied map permits any square label. These alternatives
are retained rather than choosing a vessel name. The enumeration prices this
declared template and does not prove a unique historical error mechanism.

The two quantity positions are also linked. One is an unassigned VF square
cell with labels `{5, 6}`; the other depends on a surviving printed mask and
the same globally injective square. There are **12 joint quantity strings**,
not 14 independent marginal combinations. With the selected first-two-label
name domains they produce **432 complete roundtrip witnesses**, all retained in the
certificate. None is selected as the historical quantity.

## Original source and attribution

Childs, printed p198 / PDF p201; `A) IWE v KI (17.21 p.m., November 15th)`;
`VON POT AN IWE SS 18.06 WIR GEN TRA`; `RICHI-244`.
The page heading and reception date remain **15 November**. Nov7–9 is the
registered key identifier that decrypts this body, not a replacement date.

[Original PDF](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
· [Edition and verification](../../experiments/p198_shipping_query/README.md)
· [Complete certificate](../../experiments/p198_shipping_query/certificates.json).

**Source transcription — all 247 glyph slots, including invalid letters and masks:**

```text
XADTAF AATAGV DAVUV GXDAG XDUDN DXUAX XXDDF DVGVD
XAXVX VGCXV XXXVG VXGVV XXXAD AGDXG AVVAA XXGDV
AXGGA VGGAA XGAX DFAGD FAADX DGGVG DXVVG VADAX
DVDDX GDG-- GVVVV XXDXV VVGVD VVVXD DVVDX GGFGV
GDAVG VADVG XDAXD GVVDV GVAVV DXDVD DCGGV XGXDA
GXFGD VAFVX DXDVV DDDGV AGGAX AXAFD VXXVG DDDAX
AXVDX X
```

The key retains the published Lasry–Niebel–Kopal–Wacker work and Lasry's
2017 list. The earlier repository OCR block remains preserved as provenance;
the source transcription, conditional frame and readable recovery here are
by **icekylinx and GPT-6 Astra Pro**.
