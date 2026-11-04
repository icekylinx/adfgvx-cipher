# Return to a replacement unit on medical grounds

The two p104 C parts report being sent to a replacement unit for specialist medical treatment and recovery.

**Complete edition by printed page:** [p. 104](../pages/104.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

The two p104 C parts report being sent to a replacement unit for specialist
medical treatment and recovery. The literal closing contains both
`RETTERL` and `KETTERL`, followed by `LTN`; neither spelling is silently
replaced by the other. The office-like field `DTSCHXSTAAT` remains unresolved.

Part 1 has a visibly short cipher group and remains conditional on one
missing transmitted coordinate. Part 2 has an ordinary complete frame.
Together the edition requires four known-coordinate substitutions and the
one separately charged insertion. No square label changes.

## Source and header

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p104, PDF p107](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [full page](../../experiments/inventory_and_medical_return/sources/childs_p104_full.png)
places these parts under a November 2 heading. Their reception line says
November 4:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
C) POT v NKJ (9.10 a.m., November 4th)
FÜR POT FÜR HAFENKDTR 1135 (2) 2 TLE
1 TL RICHI-228
2 TL RICHI-140
```

</details>

The unchanged published `Nov1-3` key applies. The heading, internal day `(2)`
and later reception date are preserved without renaming the key period.

## C1: one coordinate missing from the source frame

The [first-part crop](../../experiments/inventory_and_medical_return/sources/childs_p104_C1.png)
contains **227 valid coordinates**, although its label says 228. Group 34,
row 5/group 2, is visibly only **`GAGA`**, beginning at zero-based source
index 165. This is not merely an odd OCR extraction: the four-character
group is present in the image.

The unmodified 227-slot frame gives an unreadable 113-position string plus
an unpaired coordinate; that result is preserved in the certificate. Under
the conditional 228-slot model, inserting an unknown coordinate at index
168 gives 113 fixed labels out of 114:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional insertion at source index 168:**

```text
W?RDEHEUTEAUFGRUNDAERZTLXGUTACHTJDSEITENSSCHWARZMEERSTELLEDTSCHXSTAATZUSPEZIALAERZTLXBEHADDLUNGUXWIEDERHERSTELLUNG
```

</details>

Inserting `A` and applying three source-coordinate substitutions gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same conditional missing-slot frame, with A supplied and three substitutions:**

```text
WURDEHEUTEAUFGRUNDAERZTLXGUTACHTENSEITENSSCHWARZMEERSTELLEDTSCHXSTAATZUSPEZIALAERZTLXBEHANDLUNGUXWIEDERHERSTELLUNG
```

</details>

The phrase continues directly into part 2. It says that action was taken
today on the basis of a medical opinion from the `SCHWARZMEERSTELLE`
followed by the literal `DTSCHXSTAAT` field, for specialist medical treatment
and restoration of health. This edition does not turn `STAAT` into `STAB`
or assign a specific institutional identity.

### Equal-A insertion ambiguity

All **228** possible insertion positions were priced against the later
114-character template. The minimum is three observed-coordinate
substitutions, reached at positions **168, 169 and 170**, always with a
missing `A`. The three choices produce **one identical completed cipher
stream and one identical repaired received witness**.

Positions 168 and 169 lie within or at the end of the visibly short `GAGA`
group. Position 170 is just beyond it, after the first `A` of the next
printed group. It remains an arithmetic equivalent because the completed
stream contains three consecutive A coordinates there; it is not an
independently witnessed location of the source gap.

| Proposed insertion index | Where the unknown label appears before filling | Relationship to the short group |
| ---: | --- | --- |
| 168 | `W?RDE` | Within `GAGA` |
| 169 | `A?FGRUND` | At the end of `GAGA` |
| 170 | `AE?ZTL` | Just beyond the printed short group |

The certificate preserves all three mappings from observed coordinates to
plaintext. The template was chosen after reading the message; this pricing
is not an independently supplied crib or proof of a uniquely placed loss.

## C2: completion of the sentence and the literal closing

The [second-part crop](../../experiments/inventory_and_medical_return/sources/childs_p104_C2.png)
has exactly 140 valid coordinates and 70 fixed raw labels:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DERGESUNDHEITZUMERSATZTRUPPJNTEILINMARSHGESETZTXXRETTERLXKETTERLXLTNXX
```

</details>

One known-coordinate substitution gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
DERGESUNDHEITZUMERSATZTRUPPENTEILINMARSHGESETZTXXRETTERLXKETTERLXLTNXX
```

</details>

Together the parts report being sent to the replacement unit for specialist
treatment and recovery. The source spells the phrase `IN MARSH GESETZT`;
no extra plaintext `C` is inserted to make modern `MARSCH`. Both name tokens
in `RETTERL KETTERL LTN` remain literal. The text supports a lieutenant's
medical-return report, not a unique historical identification from a repaired
surname.

## Costs and reproduction

All indices below refer to the **original received source**, before the
missing C1 coordinate is reconstructed. Printed group numbers and positions
are counted separately within each part.

| Part | Source index | Printed group / position | Change | Effect |
| --- | ---: | --- | --- | --- |
| C1 | 194 | 40 / 1 | `A` → `G` | `J` → `E` in `GUTACHTEN` |
| C1 | 200 | 41 / 2 | `A` → `G` | `BEHADDLUNG` → `BEHANDLUNG` |
| C1 | 218 | 44 / 5 | `A` → `G` | Final `D` → `N` in `GUTACHTEN` |
| C2 | 61 | 13 / 2 | `A` → `G` | `TRUPPJNTEIL` → `TRUPPENTEIL` |

The extra reconstructed `A` in C1 is charged as one **missing transmitted
coordinate**, not as a source-glyph fill. There are no unreadable coordinates
in either observed body. The [inputs](../../experiments/inventory_and_medical_return/inputs.json)
and [certificates](../../experiments/inventory_and_medical_return/certificates.json)
preserve every original group, raw domain, insertion alternative, edit and
full/received forward witness.

```sh
python experiments/inventory_and_medical_return/verify.py --verify
```

The period key is prior work by **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also reproduced in Lasry's 2017 key comment. Earlier unreviewed OCR candidates
existed. No universal first-decipherment claim is made from the bounded
author-paper review. The conditional reconstruction certifies its arithmetic
and repair cost, while the source gap and unresolved words remain explicit.

</details>
<!-- CASE-EDITION:END -->
