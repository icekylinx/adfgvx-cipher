# p201 B / p206 A — reporting orders linked by a shared reference

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case guide](../README.md) · [ADFGVX Cipher](../../README.md)

**Status:** Two complete multipart messages are assembled from the source:
a two-part reporting order on p201 and a three-part request for receipt
confirmation on p206. The unchanged published `Nov16-18` partial key fixes
**660 of 702 plaintext positions** from **1,404 source coordinate slots**.
Their matching number pattern and subject support a **conditional new digit
assignment, VA = 5**. The published square remains unchanged.
**Source assembly and analysis:** icekylinx and GPT-6 Astra Pro. Period-key
recovery retains [the catalogued attribution](../../data/keys.json).

## Reporting order on p201

**Readable German — body excerpt; the unresolved closing reference remains in the raw output below:**

> Erreichte Ziele regelmaessig hierher melden, desgl. wo u. wann ersten
> Teile voraussichtlich die deutsche Grenze erreichen werden, ob mit
> Bahn/Fussmarsch und welche Teile des sind. Empfang bestaetigen. OHL.

**Meaning:** Report reached positions regularly, and say where and when the
first units are expected to reach the German border, whether by rail or on
foot, and which units they are. Acknowledge receipt.

The source has the awkward `ERSTEN` and `DESSIND`; both are retained in the
German reading above. No final `N` is dropped to regularize the former.
The English translation conveys the sentence's apparent meaning
without claiming that its spelling is recovered differently. `WERD?N` is
shown as `werden` using one explicitly costed source-coordinate correction.

The full raw readings are:

**Raw output — two separately identified source parts:**

```text
p201 B1:
ERREICHTEZIELEREGELMAESSIGHIERHERMELDENDESGLXWOUXWANNERSTENTEILEVORAUSSICHTLICHDIEDEUTSCHEGRENZEERREICHEN

p201 B2:
WERD?NOBMITBAHNFUSSMARSCHUNDWELCHETEILEDESSINDEMPFANGBESTAETIGENXOHLXNMX1XAX11??2XGEHXOPX
```

The p201 [source crop](../../experiments/open_targets_continuation/sources/childs_p201_selected.png)
shows a **16 November** heading and receipt, while the clear internal origin
stamp says **`OHL OP 15/11`**:

**Source transcription — clear header and/or literal source record:**

```text
NKJ, UKS, RAT v LP (3.49 p.m., November 16th)
1205 (16) SSD OHL OP 15/11 OKM HERMANNSTADT 2 TLE (16)
1 TL: RICHI-210
2 TL: RICHI-178
```

All 388 printed coordinates are valid. In part 2, `WERD?N` uses the unknown
cell `GG` at its fifth letter; the established `E` is in `AG`. Source index
**169: G→A** restores `WERDEN`. Assigning that unknown cell to `E` instead
would violate the square's existing injectivity. The raw footer `NMX` and
the reference's two unknown digits are not normalized.

## The three-part confirmation request on p206

The later message asks OKM to confirm immediately whether seven earlier
orders arrived. It identifies the subject of each: the departure order,
reporting intentions, destructions, refusal to surrender weapons,
negotiations with Romania, the armistice, and reporting reached positions.
It then demands immediate reports of the divisions' locations and
acknowledgment of the present order.

The [p206 source](../../experiments/open_targets_continuation/sources/childs_p206_selected.png)
has an **18 November** heading and internal stamp but a **19 November** receipt:

**Source transcription — clear header and/or literal source record:**

```text
ZON v LP (06.28 a.m., November 19th)
2100 (11/18) 3 TEILE
1 TL: RICHI-368
2 TL: RICHI-400
3 TL: RICHI-248
```

The first OCR block ended after 40 coordinates, before the printed `RICHI`
label. Rejoining the two visually continuous source rows restores the
complete 368-slot first part. The third part has exactly its stated 248
slots; the earlier OCR's extra character is not part of the printed source.
These are transcription/layout corrections, not hypothetical historical
insertions or deletions.

| Part | Source slots | Directly fixed plaintext | Separately proposed body repairs |
| --- | ---: | ---: | --- |
| A1 | 368 | 175/184 | Two erasure fills in `BETR` and `BEFEHL`. |
| A2 | 400 | 179/200 | Six erasure fills in words/separators; one erased coordinate in a number remains unresolved. |
| A3 | 248 | 115/124 | Four erasure fills; two known-coordinate substitutions for `DMR→DER` and `EXPFANG→EMPFANG`. |

The first part retains an overtyped, unclear coordinate as `?`; visible dashes
remain erasures. The third part's repeated `BEFEHLSBEFEHLS` is retained rather
than silently shortened. Its final reference begins with a directly decoded
`J`; this is not replaced with a guessed `1`.

## The shared reference and conditional digit 5

The p201 order ends with the number `11??2`. The seventh p206 reference also
has `11??2`, followed by the subject `BEFEHL ERREICHTE ZIELE MELDEN`.
Their number is identical at the square-cell level:

| Position in five-character reference | p201 B2 digraph | p206 A2 digraph | Published-key reading |
| ---: | :---: | :---: | :---: |
| 0 | VX | VX | 1 |
| 1 | VX | VX | 1 |
| 2 | FA | FA | ? |
| 3 | VV | VV | ? |
| 4 | DV | DV | 2 |

The unknown number positions are therefore shared variables, not four
independent guesses. The matching body subject further supports identifying
the seventh reference with the p201 order.

The referenced date on p206 is `1{VA}.11`. If the clear p201 origin stamp
`OHL OP 15/11` is the date of that same order, **VA must contain 5**.
This assigns zero-based square cell **24**. It changes no source coordinate
and is independent of the [p204 calendar inference](../radio/p204_A.md).

The link remains conditional on the identification of the order and the
correct copying of its date and reference. An equal partly unknown number
alone would not prove that two documents concern the same order; the matching
subject and explicit source date are why the inference is recorded here.
No unrestricted completion of the remaining square cells is claimed.

## Reference list under the two explicit inferences

The following display applies **VA = 5** from the order link and **FD = 8**
from p204's Monday date. Other unknown cells and erasures stay unknown:

| Reference | Conditional number | Conditional date | Directly readable subject |
| ---: | --- | --- | --- |
| 1 | `11212` | `?.11` | `ABMARSCHBEFEHL` — departure order |
| 2 | `1125?` | `?.11` | `BEFEHL ABSICHTEN ZU MELDEN` — report intentions |
| 3 | `11?2?` | `8.11` | `ZERSTOERUNGEN` — destructions |
| 4 | `11???` | `8.11` | `ABLEHNUNG DER WAFFENABGABE` — refusal to surrender weapons |
| 5 | `11???` | `8.11` | `VERHANDLUNGEN MIT RUMAENIEN` — negotiations with Romania |
| 6 | `11???` | `1?.11` | `WAFFENSTILLSTAND` — armistice |
| 7 | `11??2` | `15.11` | `BEFEHL ERREICHTE ZIELE MELDEN` — report reached positions |

The date order in this list is not used as an additional constraint. The
other serial numbers are not forced into an assumed numerical sequence.

Across p204 and the three p206 parts, the two assignments jointly add **seven
fixed positions** under the stated assumptions. They also fix exactly one
position in the separately audited [p205 financial message](../finance/p205_A.md):
part A4's plaintext index **86** becomes `5`, turning `NRX1???STRICH11` into
`NRX1??5STRICH11`. The p205 source package and base reading remain unchanged.
Its other unknown reference cells then share the remaining digit domain
`034679`; they are not independently chosen.

## Verify

The [input package](../../experiments/open_targets_continuation/inputs.json)
contains every source row and historical assumption. The
[certificate](../../experiments/open_targets_continuation/certificates.json)
checks both number patterns cell by cell, all source-to-plaintext offsets,
each editorial cost and every consequence of the conditional square.

```sh
python3 experiments/open_targets_continuation/verify.py --verify
```

This is an edition and a qualified key inference by **icekylinx and GPT-6 Astra Pro**,
using the published period key. No first-decipherment priority is claimed for
these supplementary messages.
