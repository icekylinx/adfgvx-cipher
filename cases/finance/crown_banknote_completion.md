# The interrupted banknote instruction: a complete later witness

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source comparison and edition: icekylinx and GPT-6 Astra Pro.**

The [earlier crown-airlift source edition](crown_airlift.md) preserved p174 A3
with 79 received coordinates, an advertised length of 98, and an explicit
“Did not finish” annotation. Its proposed ordinary words still left the
reference ending unresolved. A new literal-coordinate retrieval identified
**p195 A2**, which actually prints all **98 coordinates**.

The full witness gives this unchanged raw reading under the published
**Nov10–12** key:

**Raw output:**

```text
INMOEGLICHSTKLEINENSCHEINEN?ENDENXXOKM1A4A11333OP
```

The readable ordinary-language candidate is:

**Readable German — one-repair later witness; reference labels retained:**

> IN MOEGLICHST KLEINEN SCHEINEN SENDEN X X OKM1A4A11333OP

It asks for the money in as small denominations as possible. The literal
reference `OKM1A4A11333OP` is preserved; this edition does not turn its raw
labels into a newly established numerical date, message number or signature.

## What the second source establishes

The first 79 coordinates of p195 A2 agree with p174 A3 at **78 positions**.
Their sole disagreement is source index 65: the earlier copy has A, the
full witness has X. The earlier L after `SENDEN` becomes a second X if the
full witness's observed value is selected. This correction is supported by
a source value, not by silently assigning a new square cell.

The complete new source supplies the previously absent 19-coordinate tail:

**Source transcription — tail coordinates supplied by the complete witness:**

```text
AVDVVDFDAFXVADADXDA
```

All 80 placements of one contiguous 19-coordinate gap in the earlier
79-coordinate source were compared with this literal full witness.
**Boundary 79 is the unique minimum**, with the one observed-prefix
disagreement just described. The earlier word-only analysis had retained
three zero-substitution placements, 77–79. The new result uses a physical
copy to distinguish those geometries; it remains conditional on this
explicit single-gap family.

The earlier raw frame fixed 30 of 49 plaintext positions. Appending the
literal tail now fixes 48. It also lets us audit the twelve earlier
word-based coordinate fills: **eleven agree with the newly observed
coordinates; one does not**. The earlier evidence and costs remain unchanged
in their historical package.

## One ordinary word still requires a source repair

The unresolved first letter of `?ENDEN`, plaintext position 27, has the raw
square domain **`56789`**. S is already assigned elsewhere in the published
square, so this position cannot simply be relabelled S.

The `SENDEN` candidate changes **new-source index 95, X→D**. This is the one
new observed-coordinate word repair. It is also the coordinate where the
full witness contradicts an earlier conjectural fill. The candidate is
therefore not described as an unchanged 98-coordinate decipherment.
Of the nineteen final tail values in the edited common reading, eighteen
are copied literally and one is this separately priced correction.

## Preserve the conflicting headers

| Source | Page heading and receiving time | Reference and part marker | Observed slots |
|---|---|---|---:|
| p174 A3 | November 10; 7.24pm on November 10 | 17.50; third part of a three-part message | 79 |
| p195 A2 | November 15; 1.17am on November 15 | 1750; `2 TL` | 98 |

These are matching message fragments with different page dates and part
numbers. The source relationship does not establish which larger multipart
sequence was original, nor does it extend the Nov10–12 key's published
date range to all November 15 traffic.

## Source and exact verification

The [p195 page image](../../experiments/retrieved_copy_editions/sources/p195.png)
comes from Childs, *General Solution of the ADFGVX Cipher System*,
[complete scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [input rows](../../experiments/retrieved_copy_editions/inputs.json) and
[certificate](../../experiments/retrieved_copy_editions/certificates.json)
preserve every coordinate origin, all eighty gap costs, the disputed fill,
raw domains and explicit round-trip witnesses. Arbitrary completions used
to test partial-square consistency are not historical key assignments.

Only **p195 A2** is a new catalogue record. The prior p174 A3 is a contextual
witness and is not counted again. This new physical record has 49 positions,
48 raw fixed labels and 49 in the one-repair candidate; there are no source
erasures, coordinate insertions or deletions in its own 98-slot frame.

```sh
python experiments/retrieved_copy_editions/verify.py --verify
python experiments/retrieved_copy_editions/verify.py --verify --pdf /path/to/childs.pdf
```
