# Kiew morning report and pioneer-park loading request

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Prepared by **icekylinx and GPT-6 Astra Pro**.

These are two separate messages on Childs p110, both marked NKJ v LP and
forwarded for UKS on November 3. They are not assembled into one telegram.
Both use the unchanged published Nov1–3 square and ranks.

## Morning report

### p110 B

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
OXKXMACKENSENXXMORGENMELDU?GXVX3X11X18XNICHTSN?UESXXHRGXKIEWXROMX1AX6915X18
```

**Edited output:**

```text
OXKXMACKENSENXXMORGENMELDUNGXVX3X11X18XNICHTSNEUESXXHRGXKIEWXROMX1AX6915X18
```

</details>

Cost: **0 observed-coordinate substitutions** and **2 source-mask fills**. Source length and transposition are unchanged.

The message addresses Mackensen and reports `NICHTS NEUES`—nothing new—in
the morning report of `3X11X18`. The Kiew/office/reference ending remains
literal. Two printed glyphs at source indices 67 and 104 are C-shaped;
they are preserved as C in the diplomatic transcript and treated as masks
in the arithmetic. Filling the two word positions gives `MORGENMELDUNG`
and `NICHTSNEUES` without changing an observed coordinate. Independent enlarged-glyph review identifies source 62 as G in `VAGGF`;
its coordinate pair directly supplies the final reference digit5. The raw
reference `6915` is preserved as a published-square label sequence, without
a new historical numerical assignment. [The independent glyph audit](../../experiments/nov3_radio_and_pioneer/source_glyph_audit.json) retains the rejected preliminary C reading and the comparison crops.

## Pioneer-park request

### p110 C

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
ANDENSTABSOFFIZIERDERPIONIEREDESXAXOXKXSCHOLTVXXPIONPARKKAMPX13XFIEGTBEI26X10INXPETREXVERLADEBEREITERBITTEPARKNUM2ERDES1AGGONGESTELLUNGVERANLASSETDASONSTJINFORTKOMMENUNMOEGLICHXXBAYXPIONXPARKXKOMPX13
```

**Edited output:**

```text
ANDENSTABSOFFIZIERDERPIONIEREDESXAXOXKXSCHOLTZXXPIONPARKKOMPX13XLIEGTBEI26X10INXPETREXVERLADEBEREITERBITTEPARKNUMMERDESWAGGONGESTELLUNGVERANLASSENDASONSTEINFORTKOMMENUNMOEGLICHXXBAYXPIONXPARKXKOMPX13
```

</details>

Cost: **8 observed-coordinate substitutions** and **0 source-mask fills**. Source length and transposition are unchanged.

The request addresses the staff officer of pioneers of Army Command Scholtz.
It says that a pioneer-park company is ready for loading at the literal
place field `PETRE` and requests wagon provision, without which onward
movement is impossible. These are readings of the message, not confirmation
that the shipment occurred or a new identification of the place.

Seven equal-length word/name repairs cost eight observed-coordinate changes:
`SCHOLTV`→`SCHOLTZ`, `PARKKAMP`→`PARKKOMP`, `FIEGT`→`LIEGT`,
`NUM2ER`→`NUMMER`, `1AGGON`→`WAGGON`, `VERANLASSET`→`VERANLASSEN`,
and `SONSTJIN`→`SONSTEIN`. The two numerical-looking symbols repaired inside
words are local edits; they do not relabel those square cells elsewhere.

The awkward `BEI26X10`, `ERBITTEPARKNUMMERDES` and the unit labels `13`
are retained. A precise intended date or a smoother grammatical sentence
is not imposed. The source has exactly **398 coordinates**. Earlier OCR
had 399 because it inserted a spurious V at source boundary 277 and also
masked two visible letters. Restoring the literal source frame is not an
original-message deletion or an erasure fill.

## Notation and evidence

The fixed-width strings preserve every plaintext position. `?` means one
unresolved position, `X` is a literal decoded symbol that may serve as a
separator, and digits retain the published square's labels. Word spacing,
calendar values and numerical identities are not silently inferred. A source
mask fill is separate from a change to an observed ADFGVX coordinate.

[Source rows and image metadata](../../experiments/nov3_radio_and_pioneer/inputs.json),
[coordinate and domain certificate](../../experiments/nov3_radio_and_pioneer/certificates.json),
and [method, prior credit and reproduction](../../experiments/nov3_radio_and_pioneer/README.md).
