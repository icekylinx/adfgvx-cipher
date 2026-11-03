# Equipment transfer east of the Rhine, with radio service maintained

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source recovery and edition: icekylinx and GPT-6 Astra Pro.**

This order directs equipment identified by the unexpanded label **`U.S.`**
to the nearest replacement unit east of the Rhine. It also requires wireless
station operation to be maintained. `U.S.` is preserved as a source label;
the text does not establish an American origin or a particular equipment type.

The source is Childs, *General Solution of the ADFGVX Cipher System*,
[printed p179 A, PDF p182](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view),
with this [visible header and ciphertext](../../experiments/november_armistice_orders/sources/p179_A.png):

**Source transcription — clear header and/or literal source record:**

```text
A) KS CZ FG v XF (20.07, November 11th)
RICHI-266
```

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

**Raw output — frame excluding the visibly cancelled duplicate group; exclusion priced separately:**

```text
DORTBEFINDXUXSXGERAETEZURNAECHSTENRECHTSRHEINXERSXABTLGXOCHAFKENXFU?OSTELLENB2TRIEBMUSSAUFRECHTERHA?TENBLEIBENXNACHRICHTENC0EF4B4??3?
```

Seven separately recorded observed-coordinate substitutions give:

**Edited output — same cancelled-group frame, followed by seven word repairs:**

```text
DORTBEFINDXUXSXGERAETEZURNAECHSTENRECHTSRHEINXERSXABTLGXSCHAFFENXFUNKSTELLENBETRIEBMUSSAUFRECHTERHALTENBLEIBENXNACHRICHTENCHEF4B4??3?
```

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
