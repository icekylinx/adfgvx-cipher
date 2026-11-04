<a id="the-interrupted-banknote-instruction-a-complete-later-witness"></a>

# The small-note instruction: the complete banknote witness

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**The interrupted instruction can now be checked against a complete copy.**
Childs p195 A2 contains all 98 coordinates corresponding to the 79-coordinate
p174 A3 fragment. It confirms the request for small banknotes at the end of
the [daily crown-airlift message](crown_airlift.md), while exposing one
incorrect earlier word-based fill.

**Readable German — one-repair later witness; reference labels retained:**

> IN MOEGLICHST KLEINEN SCHEINEN SENDEN X X OKM1A4A11333OP

The practical concern is the form in which the money should arrive: notes
small enough to use. The earlier parts request one million crowns each day,
alternately to Kronstadt and Hermannstadt. This closing instruction refines
that request; it does not report receipt of the cash. The reference
`OKM1A4A11333OP` remains literal rather than becoming an inferred date,
message number or signature.

**Edition and source comparison:** icekylinx and GPT-6 Astra Pro.
The unchanged published key is **Nov10–12**.

## What the second source establishes

The two records share 78 of their first 79 observed coordinates. The single
disagreement is at zero-based index 65: p174 has A and p195 has X. Selecting
the complete copy’s X changes the earlier L after `SENDEN` into a second X.
That is an observed difference between sources, not a change to the key.

The full copy supplies all nineteen previously absent tail coordinates.
It raises the source-linked reading of the earlier frame from 30 to 48
fixed positions out of 49. Of the twelve coordinates once supplied from
word expectations, eleven agree with the newly observed source and one
does not. The recovered copy both strengthens and corrects the reconstruction.

<details>
<summary>Unchanged raw stream, literal tail and gap comparison</summary>

**Raw output:**

```text
INMOEGLICHSTKLEINENSCHEINEN?ENDENXXOKM1A4A11333OP
```

**Source transcription — tail coordinates supplied by the complete witness:**

```text
AVDVVDFDAFXVADADXDA
```

All eighty placements of one contiguous nineteen-coordinate gap were
compared against the full literal source. Boundary 79 is the unique minimum,
with the one observed-prefix disagreement described above. The older
word-only comparison had retained boundaries 77–79. This distinction comes
from physical source evidence; uniqueness remains scoped to that declared
single-gap family.

</details>

## One ordinary word still requires a source repair

The raw first label of `?ENDEN`, at plaintext position 27, has the published
square domain **56789**. S is already assigned to another cell. Reading
`SENDEN` therefore requires the explicit observed-coordinate change
**p195 source 95, X→D**; the question mark cannot simply be renamed S.

This is also where the full copy contradicts an earlier conjectural fill.
The common edited tail retains eighteen source values literally and changes
one. The p195 record has no printed erasures and needs no added, removed or
reordered coordinate. Its own 49-position frame has 48 raw fixed labels and
49 in the one-repair proposal.

## Preserve the conflicting headers

| Source | Page heading and receiving time | Reference and part marker | Observed slots |
|---|---|---|---:|
| p174 A3 | November 10; 7.24pm on November 10 | 17.50; third part of a three-part message | 79 |
| p195 A2 | November 15; 1.17am on November 15 | 1750; `2 TL` | 98 |

The sources match closely but carry different dates and part numbers. Their
relationship does not establish which larger multipart sequence was original,
or extend the key’s published date range to every November 15 message.

## Source and exact verification

The [p195 image](../../experiments/retrieved_copy_editions/sources/p195.png)
is from Childs, *General Solution of the ADFGVX Cipher System*,
[scanned volume](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [inputs](../../experiments/retrieved_copy_editions/inputs.json) and
[certificate](../../experiments/retrieved_copy_editions/certificates.json)
retain the original-coordinate comparison, all eighty gap costs, the
contradicted fill, raw domains and exact re-encryption witnesses. Arbitrary
completions used to check partial-square consistency are not historical key
assignments.

p195 A2 and p174 A3 each have one catalogue entry as separate physical
sources. Their common wording does not create another record.

Only **p195 A2** is a new catalogue record. The prior p174 A3 is a contextual
witness and is not counted again. This new physical record has 49 positions,
48 raw fixed labels and 49 in the one-repair candidate; there are no source
erasures, coordinate insertions or deletions in its own 98-slot frame.

```sh
python experiments/retrieved_copy_editions/verify.py --verify
python experiments/retrieved_copy_editions/verify.py --verify --pdf /path/to/childs.pdf
```
