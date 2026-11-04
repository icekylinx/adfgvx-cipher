# Withdrawal from Hungarian and South Slav territory, and a night report

The surviving parts say German troops will leave Hungarian and South Slav territory as soon as possible, and that the army begins its march on the stated November date. A separate short night report is preserved alongside them.

**Complete edition by printed page:** [p. 117](../pages/117.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Prepared by **icekylinx and GPT-6 Astra Pro**.

The p117 C material comprises explicitly marked third and fourth parts
under `UKS v ZOEN`, time 1030, received at 5.25 p.m. on November 3. Earlier
parts are not identified here. The adjacent D item is a separate short
report, with an unknown sender and a November 4 receipt line.

## p117 C3

<details>
<summary>Raw decoded text</summary>

**Raw output — native source frame**

```text
DEUTSCHETRUPPENWERDENSOBALDALSMOEGLICHUNGARISCHENUNDSUEDSLAVISCHENBODENVERLASSEN
```

</details>

**Edited output:** identical to the raw output under the stated frame; no additional letter repair.

Price: 0 observed-coordinate substitutions, 0 source-mask fills.

**Readable German — based on the raw output**

> Deutsche Truppen werden sobald als moeglich ungarischen und suedslavischen Boden verlassen.

The source actually contains 160 coordinates. The older 159-slot OCR frame
missed a printed symbol. Correct source transcription therefore restores
the coherent 80-position statement without adding a historical coordinate
or changing any received coordinate.

## p117 C4

The printed length is 112, while the page actually contains **117** coordinates.
The following reading is **conditional** on excluding five transmitted
coordinates. The complete literal source remains in the input record.

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional five-coordinate exclusion**

```text
ARMEETRITTXVIERTEN11MARSCHXRUMAENIENANXAXOXK11XEINSA7029
```

</details>

**Edited output:** identical to the raw output under the stated frame; no additional letter repair.

Price: 0 observed-coordinate substitutions, 0 source-mask fills, and **five observed coordinates excluded from the conditional frame**.

**Readable German — conditional on the same five-coordinate exclusion**

> Armee tritt vierten11 Marsch Rumaenien an. A.O.K.11. `EINSA7029`.

The unusual `VIERTEN11` wording and complete reference are retained. A
particular calendar rendering or the missing preposition needed for smoother
German is not supplied. The readable text preserves the source's telegram
style; it is not an independently recovered full original sentence.

**Frame alternatives.** All 113 contiguous five-coordinate exclusions are
priced against the explicit 56-position candidate. Starts **16–22** each need
zero observed-coordinate substitutions and produce one identical completed
ciphertext. Presentation uses start 20, the printed fifth group `VDGDX`,
because it follows the displayed group boundary. That choice does not make
the historical location unique.

Allowing any five source positions to be excluded yields **14** zero-substitution
layouts for the same fixed candidate. An exact dynamic program retains every
state, path count and minimum layout. Six independent small brute-force
checks cover 66 complete layouts and agree with the dynamic result. These
are proofs about the specified template and model, not proofs that the
actual transmission contained an extra group.

The exploratory language screen reconstructed 230 candidates: all 117
single-coordinate and 113 five-coordinate exclusions at the transmitted
stage. Its archived scores can be recomputed from the frozen model. No
claim is made about untested stages, keys or other corruption mechanisms.

## p117 D

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native source frame**

```text
OXKXMXXNACHTRUHOGVERLAUFENXXOXKX11
```

**Edited output**

```text
OXKXMXXNACHTRUHIGVERLAUFENXXOXKX11
```

</details>

Price: 1 observed-coordinate substitution, 0 source-mask fills.

**Readable German — based on the edited output**

> O.K.M. Nacht ruhig verlaufen. O.K.11.

One coordinate repairs `RUHOG`→`RUHIG`. The 68-coordinate source has no
printed erasure or length defect. The sender remains unknown; the header's
`2045 1 TL UND7 TL 0705 (3)` is retained as source metadata, without supplying
any unseen parts. Its final `FVGVA` group ends in a visible A, as the enlarged
source image shows.

## Evidence and reproduction

The published Nov1–3 square and ranks retain the credit of George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker. The earlier unreviewed OCR candidates
are preserved separately. These are source editions and conditional frame
analyses, without a first historical decipherment claim.

[Literal rows and source images](../../experiments/nov3_medical_radio_withdrawal/inputs.json),
[domains, origins and exact repair certificate](../../experiments/nov3_medical_radio_withdrawal/certificates.json),
and [full method and verification commands](../../experiments/nov3_medical_radio_withdrawal/README.md).

</details>
<!-- CASE-EDITION:END -->
