# The Namur order: two witnesses for Staedt and Weiher

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source reconciliation and edition: icekylinx and GPT-6 Astra Pro.**

Two closely related transmissions instruct **Hauptmann Staedt in Namur**
to contact `HPT V. WEIHER` at an Etappen inspection. The latter is to receive
a detailed order by `11 VORM`; the message is signed `MJR KROEGER`.
The witnesses together support this 126-position reading:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — joint witness reconstruction under the stated same-message model:**

```text
HPTMANNSTAEDTNAMURXXBITTESICHMITHPTVXXWEIHERETAPPENINSP1INVERBINDUNGSETZENDERBIS11VORMAUSFUEHRLICHENBEFEHLBEKOMMTXXMJRKROEGERX
```

</details>

The anomalous **`INSP1IN`** and literal **`HPTVXX`** are retained. The
edition does not silently replace the `1` with a separator or insert letters
into the title abbreviation. The source spelling `STAEDT` is retained
without a new biographical identification.

## The two physical sources

Both are in Childs, *General Solution of the ADFGVX Cipher System*,
[complete scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view),
and use the unchanged published **Nov10–12** square and ranks.

| Witness | Source | Header | Received slots |
|---|---|---|---:|
| p171 C | [Printed p171, PDF p174](../../experiments/namur_order_witnesses/sources/p171_C.png) | `--- v SY (7.26 p.m., November 10th); 1800; RICHI-252` | 252, including four printed dashes |
| p172 E | [Printed p172, PDF p175](../../experiments/namur_order_witnesses/sources/p172_E.png) | `SY v MAX (7.21 p.m., November 10th); RICHI----; (J'md)` before the received groups | 242, all valid coordinates |

The receiving time on E is five minutes earlier than C's. The edition
preserves both timestamps and does not infer an actual relay sequence.
The p171 page heading is November 9, while C's own receiving timestamp
explicitly says November 10.

C's direct reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
HPTMDNNSTAEDTNAMQRXXBITTESICHMITHPTVXXWEGHERE?AB?ENINSP1?NVERBINDUNGSETZENDE4BIS11VORMAUSFUEHRLICHENBQFE?LBEKOMMTXXMJRKROEGERX
```

</details>

E's earlier OCR stream had only 235 positions and did not yield this
coherent body. Visual retranscription supplies its actual **242 received
coordinates**. Under the same-message model, E is missing ten leading
coordinates, giving this direct reading in a 252-coordinate frame:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional same-message 252-slot frame with ten absent leading coordinates:**

```text
HPTMANN?1AEDTNA?URXXBIT?ESICHJI?HPTVXXW?IHERETA?PENINSP?I?VERBI?DUNGSET?ENDERBI?11VORMAUSFUEHRLICHENBEFEHLBEKOMMRXXPJRKROEGERX
```

</details>

The ten-coordinate leading loss is inferred from the relationship between
the witnesses; E does not display a legible total length or explicitly
count a ten-coordinate gap. It remains a stated model assumption.

## Why the alignment is useful

Aligning E's first received coordinate with C source index **10** compares
**238 jointly observed coordinates**: **227 agree** and **11 conflict**.
E supplies observed values for all four printed dashes in C, while C
supplies E's ten modeled missing leading values:

<details>
<summary>Literal source transcription</summary>

**Source transcription — ten leading coordinates supplied by the other witness:**

```text
DGAAV FADFD
```

</details>

This offset is the unique highest agreement fraction among the **87 relative
offsets with at least 200 jointly observed coordinate pairs**. The comparison
uses ciphertext values, without a language score. It is a finite alignment
check, not a statistical significance claim or a global exclusion of every
possible original length.

The name correction **`WEGHER→WEIHER`** is supported by an observed coordinate
in E, rather than merely by the familiarity of a surname. Conversely, C
supplies correct-looking word and name values where E has other errors.
Lasry et al.'s separate discussion of the neighboring p172 C/p175 A family
also mentions von Weiher; that is retained as prior context, not used to
claim a new identification of the officer in these two witnesses.

## Exact reconciliation cost, with the alternatives retained

For two aligned streams to represent one common ciphertext, at least one
observed coordinate must change at each of the **11 conflicts**. The
selected readable body needs exactly **six substitutions in C and five in
E**, meeting that lower bound. Four printed-dash fills in C and ten modeled
prefix fills in E are separately accounted for.

Every coordinate value in the selected common ciphertext is **observed in
at least one witness**. No new coordinate value is supplied solely from a
word guess. The evidence for its plaintext pairs is:

| Complete coordinate pair supporting a selected character | Positions |
|---|---:|
| Observed in both witnesses | 102 |
| Observed only in C | 14 |
| Observed only in E | 9 |
| One coordinate supplied by each witness | 1 |
| **Total** | **126** |

The mixed pair is the first `P` in `ETAPPEN`, plaintext position **47**:
C supplies working coordinate 5 and E supplies working coordinate 52.
Thus **125 of 126 whole pairs** are directly observed in one of the two
sources, and the remaining pair is covered coordinate by coordinate.

Minimum cost does not establish a unique original reading. Each conflicting
coordinate has two source-supported choices, yielding **2¹¹ = 2,048**
minimum-cost common coordinate streams under this fixed alignment. The
verifier enumerates all of them, checks the same total cost, and records
their ordered digest. The complete conflict table and selected choice bits
make every alternative reproducible. The readable body is an editorial
choice within that set, with `INSP1IN` left unrepaired.

| Witness | Literal source slots | Analysis-frame slots | Raw fixed labels | Edition labels | Known-coordinate substitutions | Printed fills | Modeled-prefix fills |
|---|---:|---:|---:|---:|---:|---:|---:|
| p171 C | 252 | 252 | 122 / 126 | 126 / 126 | 6 | 4 | 0 |
| p172 E | 242 | 252 | 115 / 126 | 126 / 126 | 5 | 0 | 10 |
| **Total** | **494** | **504** | **237 / 252** | **252 / 252** | **11** | **4** | **10** |

These are two physical witnesses of **one 126-position body**, not two
independent bodies totaling 252 distinct characters. There is no deletion,
source reordering or baseline-key change.

## Attribution and reproduction

The period key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**. C already appeared as an unreviewed OCR-derived candidate.
The new contribution is the exact source review of both witnesses, the
recovery of E's actual received stream, the joint reconstruction and its
complete repair accounting. The bounded publication check is documented;
no universal decipherment-priority claim is made.

The [inputs](../../experiments/namur_order_witnesses/inputs.json) preserve
all source rows and headers. The
[certificate](../../experiments/namur_order_witnesses/certificates.json)
contains all 87 alignment comparisons, all 11 coordinate conflicts,
character-by-character support, repairs, raw domains and global round-trip
witnesses. Arbitrary key/erasure witnesses certify consistency only.

```sh
python experiments/namur_order_witnesses/verify.py --verify
```

The optional `--pdf` argument verifies the pinned scan and independently
regenerates both source-crop images for pixel comparison.
