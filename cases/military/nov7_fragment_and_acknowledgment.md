# November 7 report fragments and a separate telegram acknowledgment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p151 A, PDF p154, is headed
`LP v NKJ (6.42 p.m., November 7th)` and `KR 1215 UKS 5 TLE`.
Only source-labeled parts **1 and 2** are established here. Parts 3–5
are not supplied or assembled from nearby messages. B is a separate
acknowledgment, with no established reply relationship to A.
All use the unchanged published partial **Nov7–9** key.

## p151 A1

The [source crop](../../experiments/nov7_fragments_and_council/sources/p151_A.png)
has **189 typed coordinates** against `1 TL RICHI-190`. The
[short-group detail](../../experiments/nov7_fragments_and_council/sources/p151_A1_short_group.png)
shows **AVVG**, four symbols. The following layers assume one missing
coordinate before that group: **?AVVG**. This is a conditional frame,
not a source-supplied loss position.

**Raw output — conditional 190-coordinate frame with one missing coordinate at the AVVG short group:**

```text
OHLXBPXXNACHRICHTVONABREISEDEUTSCHERWAFFENSTILLSTANDSKOMMISSIONHATANSCHEINENDGEM?LDETENSTUR3FSS
```

**Edited output — same conditional frame; one missing-coordinate fill and zero observed substitutions:**

```text
OHLXBPXXNACHRICHTVONABREISEDEUTSCHERWAFFENSTILLSTANDSKOMMISSIONHATANSCHEINENDGEMELDETENSTUR3FSS
```

The modeled missing coordinate at working index **55** is filled with D,
supplying E at plaintext position **80**. Its raw domain is **DEQTUX**.
The candidate fixes **95 / 95 positions** but retains the opaque ending
**STUR3FSS**; a fixed label is not necessarily an understood word.

**Readable German — spacing of an incomplete fragment, with the opaque closing retained:**

> OHL. BP. Nachricht von Abreise deutscher Waffenstillstandskommission
> hat anscheinend gemeldeten STUR3FSS

The predicate and closing are not reconstructed into a complete report.
The edition does not infer what effect the news of the commission's
departure had.

All five placements inside AVVG and all six coordinate values are
retained: **30 geometry-labeled witnesses**, **26 distinct complete
ciphertexts and plaintexts**. Requiring the lexical crib
**GEMELDETEN** at positions **77:87** leaves one candidate, the one above.
That uniqueness is conditional on both the one-loss model and the crib;
it is not an unconditional historical solution.

The later [p151/p157 copy comparison](armistice_departure_copy.md) supports
a separately priced A1 variant. Under the common-copy alignment, an
observed p157 coordinate supports p151 source index 142 `A` → `F`, giving
`STURZFSS` in place of `STUR3FSS`. The fuller `STURZDES` interpretation
still needs two additional p151 coordinate changes without observed p157
support. The truncated p157 source fixes **0/95 positions by itself** in
the declared frame; its copied prefix, competing alignments and conflicting
source choices remain explicit in the separate edition. The original
layers above retain their stated zero-observed-substitution candidate.

## p151 A2

The same source crop gives **186 valid coordinates** for
`2 TL RICHI-186`, fixing **93 / 93 positions**.

**Raw output — native 186-coordinate frame:**

```text
ANSCHEINENDXOMOLDOVAXUEBERGEGANGENERFEINDMARSCHIERTAUFXFEHERTEMPLOMXXARMEETRITTX8X11X0BMARSCH
```

**Edited output — one observed-coordinate substitution, with no fills:**

```text
ANSCHEINENDXOMOLDOVAXUEBERGEGANGENERFEINDMARSCHIERTAUFXFEHERTEMPLOMXXARMEETRITTX8X11XABMARSCH
```

Source **27 V→X** repairs `0BMARSCH` to `ABMARSCH`. No global numeral
relabeling follows, and the separate 8 and 11 remain literal.

**Readable German — spacing, punctuation and umlaut; the unfinished wording remains:**

> Anscheinend O MOLDOVA übergegangener Feind marschiert auf
> FEHERTEMPLOM. Armee tritt 8. 11. Abmarsch

The initial O is retained without geographical expansion. The ending is
not supplemented with “an,” a route, a time or a missing continuation.

## p151 B

The [separate source](../../experiments/nov7_fragments_and_council/sources/p151_B.png)
is headed `NKJ v UKS (11.30 p.m., November 7th)` and `AN LP 2150`.
Its **156 typed coordinates** match `RICHI-156`. Five additional
[handwritten glyphs](../../experiments/nov7_fragments_and_council/sources/p151_B_annotation.png)
read **VXXDV**, duplicating the immediately preceding typed group.
The combined visible layer has **161 slots** and is odd in length.

**Raw output — 156-coordinate typed source layer, with the five handwritten glyphs retained separately:**

```text
OXOXLXOPXDHRTIGESTELEGRAMMROEMX1ANOX11212OPXGEHXERHFLTENHOXKXMXOPXROEMX1A11302
```

**Edited output — same typed source layer; three observed-coordinate substitutions, with no fills:**

```text
OXHXLXOPXDORTIGESTELEGRAMMROEMX1ANOX11212OPXGEHXERHALTENHOXKXMXOPXROEMX1A11302
```

The changes are composite-source **0 F→V**, **40 V→F** and **115 X→D**.
They repair the first `O O L`, `DHRTIGES` and `ERHFLTEN`. The additional
H between ERHALTEN and O K M remains literal. Both layers have
**78 / 78 fixed positions**, and the complete edited candidate re-encrypts
exactly within the typed frame.

**Readable German — spacing and punctuation, with abbreviation labels retained:**

> O. H. L. Op. Dortiges Telegramm Röm. 1 A No. 11212 Op. Geh. erhalten.
> H. O. K. M. Op. Röm. 1 A 11302.

The acknowledgment refers to the literal number **11212**. This edition
does not establish which other surviving message, if any, it answers.

## Conditional interpretation and source-layer accounting

B's primary reading selects the typed source layer, mapping each working
coordinate to the complete visible composite. The handwriting's author
and purpose are not established. If all 161 visible glyphs are instead
treated as transmitted material, reaching the typed frame requires
**five slot deletions**, involving five known coordinates under the
primary D reading. That is a separate conditional transmission model,
not a free repair. A hypothetical handwritten D→O sensitivity leaves
four known coordinates and one non-coordinate mask in those excluded
slots; it does not affect the typed output. The enlarged crop supports
D, so the O variant is not presented as equally certified.

The old B OCR omitted typed **XXVGF** and the final D, misread one typed
X and masked a handwritten D and typed V. Its exact reconstruction is
frozen in the [OCR snapshot](../../experiments/nov7_fragments_and_council/ocr_snapshot.json)
and [certificate](../../experiments/nov7_fragments_and_council/certificates.json).
The historical typed-layer choice is kept separate from those OCR fixes.

These three physical records have **536 visible glyph slots including
five handwritten annotations**, **531 typed coordinates**, and **532
modeled coordinates**, with **266 plaintext positions**. The raw layers
fix **265 / 266** and the edited layers **266 / 266** under their stated
frames/layers. The primary cost is **four observed substitutions and one
missing-coordinate fill**. Neither unresolved key symbol 5 nor 6 is
assigned: all used pairs are already resolved by the published baseline.

Earlier A1/A2 body candidates, B's unread OCR and key provenance are
preserved; no historical first-solution claim is made. See the
[inputs](../../experiments/nov7_fragments_and_council/inputs.json),
[reproduction instructions](../../experiments/nov7_fragments_and_council/README.md)
and the separate [Soldiers Council notice](soldiers_council_surrender.md).
