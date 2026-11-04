# Two-part discharge instruction naming Rudolf twice

The military mission is asked to release the man written Rudolf Rudolf, attached to the German Embassy, from military service. The two parts join across the phrase “aus Militärdienst.”.

**Complete edition by printed page:** [p. 108](../pages/108.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p108 B1/B2, PDF p111, are headed
`OSM v LP (9.25 p.m., November 2nd)` and `1710 (2/11) 2 TEILE`.
The consecutive part labels and the split **AUS / MILITAERDIENST**
connect the two parts. Both use the unchanged published **Nov1–3** key.
The separate p108 A naval inquiry is not part of this assembly.

## p108 B1

The [first part](../../experiments/p108_naval_and_personnel/sources/p108_B1.png)
contains **130 valid coordinates**, matching `1 TL RICHI-130`.
It fixes **65 / 65 plaintext positions** without repairs.

<details>
<summary>Raw decoded text</summary>

**Raw output — native 130-coordinate frame:**

```text
MILITAERMISSXBITTEGEFRXRUDOLFRUDOLFZUGETDERDEUTSCHBOTSCHSOFORTAUS
```

</details>

**Readable German — spacing, punctuation and umlaut:**

> Militärmiss. Bitte Gefr. Rudolf Rudolf, zuget. der deutsch. Botsch.,
> sofort aus

The sentence continues with **MILITAERDIENST** in part 2. The two
occurrences of **RUDOLF** remain as transmitted; they are not silently
collapsed or assigned to independently identified first and family names.
The abbreviations **GEFR**, **ZUGET**, **DEUTSCH BOTSCH** remain abbreviated
in the readable layer.

## p108 B2

The [second part](../../experiments/p108_naval_and_personnel/sources/p108_B2.png)
has **135 visible coordinates**, although its heading says
`2 TL RICHI-136`. The first row's fifth group is **DAGD**, with four
symbols. The following raw and edited layers use the explicitly
conditional model of one missing coordinate after its initial D:
**D?AGD**. The scan identifies the short group, but does not specify that
exact internal loss position.

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional 136-coordinate frame with one missing coordinate inside DAGD:**

```text
MILITAERDIENSTENTLASSENDEUTSCHEBOTSCHBENACHRNACHRICHXNACHCHEF2BO52?X
```

</details>

**Readable German — spacing, punctuation and umlaut, with the unresolved reference retained:**

> Militärdienst entlassen. Deutsche Botsch. benachr. Nachrich.
> Nach Chef 2 BO 52?.

The two parts request immediate discharge from military service and
embassy notification. They do not certify that those actions happened.
The consecutive **BENACHR / NACHRICH / NACHCHEF** fields remain separate;
no missing word or expansion is supplied to make the closing smoother.

## Conditional interpretation and every short-group placement

All five insertion positions inside **DAGD** are retained. The following
costs refer to a separately disclosed diagnostic constraint: preserve the
selected readable prefix through `NACHCHEF2BO52`, while leaving each
alternative's final reference label as found. This is a lexical constraint,
not independent ciphertext proof of the loss geometry.

| Group model | Observed substitutions for the stated prefix | Missing-coordinate fills | Resulting reference |
|---|---:|---:|---|
| `?DAGD` | 0 | 1 | `2BO522X` |
| `D?AGD` | 0 | 0 | `2BO52?X` |
| `DA?GD` | 0 | 1 | `2BO520X` |
| `DAG?D` | 1 | 1 | `2BO520X` |
| `DAGD?` | 2 | 1 | `2BO520X` |

The diagnostic fills and substitutions in this table are **not adopted
or included in the primary repair count**. The primary frame retains
**67 / 68 fixed positions**. Its unknown plaintext position **66** has
pair **F?** and domain **027GQT**, supplied by source index **35** and the
missing coordinate. Even a decimal-only assumption leaves **0, 2 or 7**;
no digit is chosen.

The verifier enumerates all **30 geometry-labeled completions** of the
five group models and six coordinate values. They produce **26 distinct
complete ciphertexts and plaintexts**. Applying the stated readable-prefix
constraint leaves six distinct completions, precisely the six completions
of **D?AGD**. The filled `?DAGD` and `DA?GD` alternatives duplicate two of
those complete ciphertexts, with reference endings **522** and **520**.
This finite audit preserves the ambiguity instead of presenting one
reference number as solved. Every complete witness re-encrypts exactly.

B1/B2 together contain **265 visible coordinates**, **266 modeled
coordinates** and **132 / 133 fixed plaintext positions under the stated
frames**. The primary layers use no observed substitutions and no fills.
The two bodies already appeared in earlier unreviewed repository
candidates; this edition supplies source layout, complete geometry
accounting and exact reproduction, with published key credit retained.
It makes no historical first-solution claim. See
[inputs](../../experiments/p108_naval_and_personnel/inputs.json),
[certificates](../../experiments/p108_naval_and_personnel/certificates.json)
and [reproduction instructions](../../experiments/p108_naval_and_personnel/README.md).

</details>
<!-- CASE-EDITION:END -->
