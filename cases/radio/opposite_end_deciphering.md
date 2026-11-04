# “First half from the front, second half from the back”

The instruction says to decipher the first half from the front and the second half from the back. Two equally priced source variants preserve the same instruction and differ in the closing station label.

**Complete edition by printed page:** [p. 138](../pages/138.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p138 B gives a short operational instruction:

**Readable German — under the conditional final-X exclusion and stated word repairs:**

> Erste Hälfte von vorne, zweite Hälfte von hinten lösen. NKJ.

Its meaning is to solve or decipher the first half from the front and the
second half from the back. **The instructional body is shared by two equally
priced source variants.** The internal closing is `NKJ` in the preferred
variant and `NMJ` in the retained alternative. The separately printed
`NKJ 472` footer favors the former, without proving a unique geometry.

The edition is conditional: the source really contains **105 slots**, but
its readable body uses a 104-coordinate transposition with one extraneous
received coordinate separately retained. Two known-coordinate substitutions
and one invalid-glyph fill are also required. This is not an unchanged
ordinary-frame decryption.

## Exact source and dates

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p138, PDF p141](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [full page](../../experiments/bidirectional_deciphering/sources/childs_p138_full.png)
is headed **November 6**, but the [B reception line](../../experiments/bidirectional_deciphering/sources/childs_p138_B.png)
reads **00.15 November 5**:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
B) LP v NKJ (00.15 November 5th)
SSD ZU 14.10 (5)
RICHI-105
NKJ 472
```

</details>

The `TEILE`/`RICHI` labels are overprinted, and the original image is retained.
The date contradiction is not silently repaired. There are 21 complete
five-character cipher groups; the fourth glyph of group 2, `FAARG`, is a
printed `R` outside the ADFGVX alphabet. It remains an erasure in analysis.
The external `NKJ 472` footer is outside the 105-slot ciphertext.

## Raw readings and two surviving variants

Using all 105 slots in the unchanged published `Nov4-6` transposition gives
52 paired labels plus an unpaired `G`, and no readable body:

<details>
<summary>Raw decoded text</summary>

**Raw output — original odd frame; paired prefix is unreadable and an orphan coordinate remains:**

```text
EIM1VLM3LFT1VRF91R4KF19LW?HMYL4W9S3ML6NMJML1REELLTM2
```

</details>

Under the preferred conditional model, the **final received `X`, source
index 104**, is extraneous to a 104-coordinate cipher. Removing it for
transposition, while preserving it in the source witness, gives 51 fixed
labels out of 52:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional exclusion of final source 104 X:**

```text
ERSTEHAELFTEVONVORNEFFEIT?HAELFTEVONHINTENLOESENXNKJ
```

</details>

The proposal is:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same conditional final-X exclusion, with the stated repairs:**

```text
ERSTEHAELFTEVONVORNEZWEITEHAELFTEVONHINTENLOESENXNKJ
```

</details>

Removing the preceding received **`F`, source index 103**, instead gives:

<details>
<summary>Raw decoded text</summary>

**Raw output — alternate conditional exclusion of source 103 F:**

```text
ERSTEHAELFTEVONVORNEFFEIT?HAELFTEVONHINTENLOESENXNMJ
```

</details>

After the same repairs, its complete alternative is:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same alternate exclusion, with the stated repairs:**

```text
ERSTEHAELFTEVONVORNEZWEITEHAELFTEVONHINTENLOESENXNMJ
```

</details>

Both variants require exactly the same source edits:

| Source index, zero-based | Printed group / position, one-based | Change | Cost category |
| ---: | --- | --- | --- |
| 8 | 2 / 4 | printed `R` → `F` | One invalid-glyph fill |
| 76 | 16 / 2 | `V` → `F` | One known-coordinate substitution |
| 94 | 19 / 5 | `A` → `F` | One known-coordinate substitution |

The two substitutions restore `ZWEITE`; the fill supplies the missing `E`.
In addition, each variant separately charges **one extraneous transmitted
coordinate**, either the final `X` or the preceding `F`. Encoding either
52-character proposal, transposing at length 104, and reinserting its
unchanged extra coordinate produces **the same repaired 105-slot witness**.
Neither coordinate is silently deleted from the historical source.

The independently printed `NKJ 472` is evidence favoring the `NKJ` closing.
It is not part of the ciphertext or an additional coordinate repair. Calling
the final `X` intentional padding is a possible explanation, not an established
historical fact.

## What the bounded search actually found

The archived comparison evaluated every single-coordinate insertion or
removal at two stages: before untransposition in the received stream, or
after untransposition in the intermediate stream. It supplied the one
published key, tried all six values of the printed `R` erasure and every
inserted coordinate, and used two unchanged frozen language objectives.

This completed **8,892 candidate records and 17,784 model-score evaluations**
over 422 geometric locations. The count includes repeated fill-value
witnesses; it is not a count of unique plaintexts. Both objectives tied the
two raw endings `NMJ` and `NKJ` at their highest score. The source footer,
rather than the scorer, favors the latter.

For the retrospective fixed `NKJ`-ending template, index 104 uniquely
minimizes substitutions among the 105 received-coordinate removal positions.
That statement is **conditional on the chosen closing**. Index 103 remains
equally cheap under its own `NMJ`-ending proposal. All original candidates,
ties and earlier unsuccessful stage interpretations remain in the
[phase archive](../../experiments/bidirectional_deciphering/search/original_phase_screen.json).

## Relation to p132 B's 1410 (5) telegram

The [p132 B source edition](p132_radio_service.md#b-repeat-the-fourth-period-telegram-in-the-fifth)
contains this header:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
B) LP v NKJ (6.13 p.m., November 5th)
SSD EILT SOFORT LOESEN 1410 (5)
RIZI-155
```

</details>

The two records share the route **LP v NKJ**, the urgency label `SSD` and
the internal reference **1410 (5)**, with punctuation added in p138's
`ZU 14.10 (5)`. `ZU` explicitly introduces a reference to that time-stamped
message. These are concrete grounds for treating p138 as a likely related
instruction. They do not establish a reply in the reverse direction: the
printed route is the same in both. Nor is their chronological order fully
resolved, because p138's reception line and page heading conflict.

The preserved 622-block OCR-header inventory finds this time/day combination
only at p132 B and p138 B; another `1410` belongs to p177 with day `11/11`.
That is a bounded inventory of available OCR headers, not a universal
uniqueness claim about the original traffic.

### A precisely limited opposite-end interpretation

The p132 source has 155 intermediate coordinates after its original
transposition is undone. With an odd length, pairing from the front and
pairing from the back use opposite pair phases. A finite comparison tried
all **78** ways to join an initial run of forward labels to a final run of
backward labels, leaving exactly one intermediate coordinate unpaired.

| Leading labels read from front | Trailing labels read from back | Unpaired intermediate index | Known-coordinate substitutions for the prior p132 proposal |
| ---: | ---: | ---: | ---: |
| 27 | 50 | 54 | 3 |
| 28 | 49 | 56 | 3 |
| 38 | 39 | 76 | 20 |
| 39 | 38 | 78 | 22 |

The first two reproduce the earlier low-cost conditional p132 reading.
Their unpaired `V` belongs to the same run of four identical V coordinates
at indices **54–57** already retained in that edition. The literal balanced
halves, 38/39 or 39/38 labels, do **not** reproduce it at the same cost.

Thus the newly read instruction supports the general relevance of working
from opposite ends. A flexible split is algebraically the existing one-extra-
intermediate-coordinate model; it does not reduce that model's assumptions
or repair cost. The instruction does not explicitly identify intermediate
coordinates, a split point, or a mathematical procedure. **The p132 extra-V
interpretation remains conditional**, and none of these observations changes
the status of an unrelated challenge.

The two source models also act at different stages:

| Record | Conditional operation | Source-shaped forward witness |
| --- | --- | --- |
| p138 B | Exclude one received coordinate before 104-slot untransposition | Reinsert that same coordinate after transposition, preserving all 105 slots |
| p132 B | Exclude one intermediate V after 155-slot untransposition | Reinsert that V before transposition, preserving all 155 slots |

## Reproduce and attribution

The [inputs](../../experiments/bidirectional_deciphering/inputs.json),
[certificate](../../experiments/bidirectional_deciphering/certificates.json)
and [method package](../../experiments/bidirectional_deciphering/README.md)
preserve all source bytes, image hashes, both full variants and the 78 finite
comparisons. The p132 inputs and certificate are frozen snapshots; its older
record is not modified by this comparison.

```sh
python experiments/bidirectional_deciphering/verify.py --verify
python experiments/bidirectional_deciphering/phase_audit.py --verify
```

The unchanged period key is prior work by **George Lasry, Ingo Niebel, Nils
Kopal and Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also published in George Lasry's [2017-02-24 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR and insertion-only candidates existed. No explicit
p138 B body example was found in the bounded author-paper review; no universal
first-decipherment priority is claimed.

</details>
<!-- CASE-EDITION:END -->
