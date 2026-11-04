# Equipment transfer east of the Rhine, with radio service maintained

Equipment identified as U.S. is to be moved to the nearest replacement unit east of the Rhine. Wireless-station operations must continue; the source does not identify the equipment as American.

**Complete edition by printed page:** [p. 179](../pages/179.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source recovery and edition: icekylinx and GPT-6 Astra Pro.**

This order directs equipment identified by the unexpanded label **`U.S.`**
to the nearest replacement unit east of the Rhine. It also requires wireless
station operation to be maintained. `U.S.` is preserved as a source label;
the text does not establish an American origin or a particular equipment type.

The source is Childs, *General Solution of the ADFGVX Cipher System*,
[printed p179 A, PDF p182](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view),
with this [visible header and ciphertext](../../experiments/november_armistice_orders/sources/p179_A.png):

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
A) KS CZ FG v XF (20.07, November 11th)
RICHI-266
```

</details>

## Conditional shared digits

The equipment order gains the complete reference **4B49936**, fixing **133/133 labels**. Its existing five-coordinate printed cancellation and seven word substitutions retain their separate costs. The [joint reconstruction](../../experiments/nov10_joint_completion/README.md) combines the earlier Marineamt and formation interpretations with the army-number constraint and the mobilization decree; the reversed 7/9 assignment is retained there.

**Conditional interpretation — readable German under the joint square:**

> Dort befind. U S Geraete zur naechsten rechtsrhein. Ers. Abtlg. schaffen. Funkstellenbetrieb muss aufrechterhalten bleiben. Nachrichtenchef 4B49936.

<details>
<summary>Exact conditional labels</summary>

**Edited output — p179_A, conditional shared square; 133/133 fixed positions:**

```text
DORTBEFINDXUXSXGERAETEZURNAECHSTENRECHTSRHEINXERSXABTLGXSCHAFFENXFUNKSTELLENBETRIEBMUSSAUFRECHTERHALTENBLEIBENXNACHRICHTENCHEF4B49936
```

</details>


## A cancelled duplicate restores the printed frame length

The literal transcription contains **271 coordinates**. Source group 17,
at zero-based positions **80–84**, is visibly struck through. It reads
`ADADG`, exactly duplicating the immediately preceding group. Excluding the
marked copy gives the advertised **266-coordinate frame**.

The cancelled group remains in the literal transcript and in the source
image. Its exclusion counts as **five observed coordinates removed at the
printed cancellation**. It is not reported as a zero-edit source. A close
view of the damaged but readable `X` at source position 190 is also
[preserved](../../experiments/november_armistice_orders/sources/p179_A_glyph.png).

Under the unchanged published Nov10–12 square and ranks, the resulting raw
reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output — frame excluding the visibly cancelled duplicate group; exclusion priced separately:**

```text
DORTBEFINDXUXSXGERAETEZURNAECHSTENRECHTSRHEINXERSXABTLGXOCHAFKENXFU?OSTELLENB2TRIEBMUSSAUFRECHTERHA?TENBLEIBENXNACHRICHTENC0EF4B4??3?
```

</details>

Seven separately recorded observed-coordinate substitutions give:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same cancelled-group frame, followed by seven word repairs:**

```text
DORTBEFINDXUXSXGERAETEZURNAECHSTENRECHTSRHEINXERSXABTLGXSCHAFFENXFUNKSTELLENBETRIEBMUSSAUFRECHTERHALTENBLEIBENXNACHRICHTENCHEF4B4??3?
```

</details>

A readable expansion, with abbreviation completions in brackets, is:

**Readable German — after the cancelled-group exclusion and priced word repairs:**

> Dort befind[liche] U.S.-Geräte zur nächsten rechtsrhein[ischen]
> Ers[atz]abtlg. schaffen. Funkstellenbetrieb muss aufrechterhalten
> bleiben. Nachrichtenchef `4B4??3?`.

The three question marks in the closing `4B4??3?` are retained. They arise
from unassigned cells in the published partial square, not missing source
coordinates. The two ordinary-word question marks in the raw reading are
also partial-key outcomes; their editorial repairs change observed
coordinates, rather than filling the key with new letters.

The abbreviation `ABTLG` already includes its final G. The readable display
therefore retains that letter outside editorial brackets and preserves the
entire closing reference, including its fixed labels and three unknowns.

| Literal source slots | Analysis-frame slots | Raw fixed labels | Edition fixed labels | Observed coordinates excluded | Known-coordinate substitutions | Erasure fills |
|---:|---:|---:|---:|---:|---:|---:|
| 271 | 266 | 128 / 133 | 130 / 133 | 5 | 7 | 0 |

There are no added coordinates, block moves or baseline-key changes.
The [inputs](../../experiments/november_armistice_orders/inputs.json) and
[certificate](../../experiments/november_armistice_orders/certificates.json)
preserve both duplicate groups, the exact exclusion, every substitution,
raw domains and global re-encryption witnesses. Arbitrary completions are
marked as consistency examples, not original numerical readings.

The period key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**. The previous unreviewed OCR stream did not yield this coherent
body. The new contribution is the source reading and priced edition;
the bounded publication check is recorded without a universal priority claim.

The other source records on this page are covered in the
[armistice and leave case](../military/armistice_and_leave_orders.md).

```sh
python experiments/november_armistice_orders/verify.py --verify
```

</details>
<!-- CASE-EDITION:END -->
