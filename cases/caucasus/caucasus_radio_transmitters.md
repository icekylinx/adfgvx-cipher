# Caucasus delegation and radio transmitters at Tiflis

The message discusses tube radio transmitters at Tiflis and General von Kress.

**Complete edition by printed page:** [p. 88](../pages/088.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p88 A1/A2, PDF p91, form the two-part message headed
`NKJ v LP (05.56 a.m., November 2nd)` and
`FUER COS SSD BLITZ GR H Q 1330 (1.11) 2 TEILE`. Both parts use the
unchanged published **Nov1–3** key. The message discusses tube radio
transmitters at Tiflis and General von Kress. It does not establish that
the proposed transport actually took place.

## p88 A1

The [first-part crop](../../experiments/caucasus_radio_transmitters/sources/p88_A1.png)
contains **172 visible slots**, matching `1 TL RICHI-172`. Source slot
**57** contains a printed **Q** in `DVQXX`. It is masked as one invalid
coordinate, with no change to the frame.

<details>
<summary>Raw decoded text</summary>

**Raw output — native 172-coordinate frame:**

```text
DTSCHEKAUKASDELEGAXER?TTETRANSPORRTX800WATTROEHRENSENDTIFLISZURTAFUNKBERLINVERANLASSEN
```

</details>

**Readable German — spacing and punctuation, with the malformed words retained:**

> Dtsche. Kaukas. Delega. ER?TTE TRANSPORRT, 800 Watt Röhrensend.
> Tiflis zur TAFUNK Berlin veranlassen.

The verb-like field is incomplete. The message nevertheless preserves
`800 WATT ROEHRENSEND`, `TIFLIS`, `BERLIN` and `VERANLASSEN` directly.
**ZURTAFUNK** is displayed as “zur TAFUNK”; no institutional expansion of
TAFUNK is claimed.

The unknown plaintext position **21** has domain **248CIM**, not every
letter. Supplying an apparently obvious B would also require a change to
its other, observed coordinate. More broadly, normalizing the whole field
to `ERBITTETRANSPORT` requires **20 observed-coordinate substitutions plus
one fill** in this native frame. That expensive editorial possibility is
certified separately and **not adopted**. The main reading retains
**85 / 86 fixed positions**, including the doubled R in `TRANSPORRT`.

## p88 A2

The [second-part crop](../../experiments/caucasus_radio_transmitters/sources/p88_A2.png)
contains **134 visible slots**, matching `2 TL RICHI-134`. Source **53**
is a [y-like non-coordinate glyph](../../experiments/caucasus_radio_transmitters/sources/p88_A2_y_glyph.png),
recorded as Y in the literal transcript and masked without deleting it.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 134-coordinate typed frame:**

```text
UOBER1500WETTDOEHRENSENDVERFUEGTG?NERALVONKRESSXNACHCHEFRM4BX49523X
```

**Edited output — three observed-coordinate substitutions and one invalid-glyph fill:**

```text
UEBER1500WATTROEHRENSENDVERFUEGTGENERALVONKRESSXNACHCHEFRM4BX49523X
```

</details>

The changes are source **22 A→V**, **37 G→D**, **107 V→X**, and the
fill **53 Y→V**. The first three repair `UOBER`, `DOEHREN` and `WETT`;
the fill supplies E in `GENERAL`. The edited stream fixes **67 / 67
positions** and re-encrypts exactly.

**Readable German — spacing, punctuation and umlauts:**

> Über 1500 Watt Röhrensend. verfügt General von Kress.
> Nach Chef RM. 4. B. 49523.

The power, name and reference retain their literal values. No independent
biographical identity or expansion of the reference is inferred.

## Conditional interpretation and the supralinear source layer

The scan contains [four marks above typed coordinates](../../experiments/caucasus_radio_transmitters/sources/p88_A2_annotations.png).
Their author, date and purpose are unknown. Interpreting each as a
replacement of the aligned typed glyph gives the following independently
reproducible effects; all indices are zero-based.

| Source slot | Typed → aligned mark | Plaintext effect when applied alone |
|---|---|---|
| 107 | V → X | Position 10: `WETT` → `WATT` |
| 115 | G → F | Position 23: `SEND` → `SEN0` |
| 116 | F → A | Position 32: `G?NERAL` → `0?NERAL` |
| 119 | X → V | Position 61: `49523` → `M9523` |

<details>
<summary>Raw decoded text</summary>

**Raw output — all four aligned replacements, with the same native frame:**

```text
UOBER1500WATTDOEHRENSEN0VERFUEGT0?NERALVONKRESSXNACHCHEFRM4BXM9523X
```

</details>

The certificate retains **all 16 combinations** of these four source
choices. The primary edited candidate uses only the first annotation;
the other three effects are kept as source evidence rather than silently
accepted or suppressed. They are variants of the same physical A2
record, not extra recovered messages. No numerical relabeling follows.

Across both parts there are **306 visible slots**, **304 valid source
coordinates**, and **153 plaintext positions**. The typed layer fixes
**151 / 153** positions; the conservative edited layer fixes **152 / 153**.
The summary counts only three observed substitutions and one fill, with
one invalid source glyph still unresolved. It excludes the expensive A1
normalization and the alternative annotation layers. Six full A1
completion witnesses demonstrate the remaining ambiguity without naming
one as the historical text.

Both bodies already appeared in earlier unreviewed repository candidates.
Published key credit and the bounded prior-paper/comment check are kept
explicitly; this edition makes no historical first-solution claim. See
[inputs](../../experiments/caucasus_radio_transmitters/inputs.json),
[certificates](../../experiments/caucasus_radio_transmitters/certificates.json)
and [verification instructions](../../experiments/caucasus_radio_transmitters/README.md).

</details>
<!-- CASE-EDITION:END -->
