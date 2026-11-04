# Crown airlift to Kronstadt and Hermannstadt

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**A daily million crowns, delivered by air.** This three-part message of
10 November 1918 asks OHL for ordinary aircraft to bring cash alternately
to Kronstadt and Hermannstadt. Its interrupted final instruction asks for
small-denomination notes. A complete second copy now supplies the missing
ciphertext behind that instruction, leaving one explicitly priced word
repair.

The request concerns usable cash at a destination, not merely a monetary
total. Regular delivery, alternating landing places and small notes all
appear in the message. The [thirty-million-crown request of the previous day](nov9_crown_airlift_and_embassy.md)
and the [later reply about a shortage of banknotes](p205_A.md) place it in a
wider exchange about paying and purchasing during withdrawal. Their surviving
references do not establish that one proposed airlift replaced another.
None of these requests proves that a flight took place.

**Source:** Childs printed p174, PDF p177, A1–A3; header
`--- v ZO'N (07.24 p.m., November 10th); 17.50 3 TLE`.
**Source edition and comparison:** icekylinx and GPT-6 Astra Pro.

## Later complete-copy witness

The [complete p195 A2 witness](crown_banknote_completion.md) prints all
98 coordinates of the final instruction. It supplies the nineteen missing
tail slots and selects the end gap within the tested single-gap family.
Eleven of the twelve earlier word-based fills agree with it; one is contradicted.

The full copy still requires one observed-coordinate repair for SENDEN.
The receptions disagree at one prefix coordinate and carry different dates
and part numbers. The linked comparison retains these qualifications.

## p174 A1

**Readable German — first-part wording; the final ellipsis marks continuation in A2:**

> An OHL, Op. Kronenbedarf sehr dringend. Bitte täglich mit gewöhnlichem Flugzeug …

This intact first part states the urgency and proposes daily delivery by
ordinary aircraft. It prints the advertised 146 coordinates and gives
73 raw labels without a repair.

<details>
<summary>Source-exact first-part stream</summary>

**Raw output:**

```text
ANXOHLXOPXXKRONENBEDARFSEHRDRINGENDXBITTETAEGLICHMITGEWOEHNLICHEMFLUGZEUG
```

</details>

## p174 A2

**Readable German — second-part wording; the ellipses mark its joins with A1 and A3:**

> … eine Million Kronen abwechselnd nach Kronstadt u. Hermannstadt. Feldkriegskasse …

This is the amount and destination instruction: one million crowns,
alternately to the two named places. `Feldkriegskasse` remains the exact
office word at the part boundary; no missing verb or address is supplied.

<details>
<summary>Second-part streams and two explicit coordinate changes</summary>

**Raw output:**

```text
EINEMILLIONKRONENABWECHSWLNDNACHXKRONSTADTXUXHERMANNSTADTXFELDKR?EGSKASSE
```

**Edited output:**

```text
EINEMILLIONKRONENABWECHSELNDNACHXKRONSTADTXUXHERMANNSTADTXFELDKRIEGSKASSE
```

The source prints all 146 advertised slots. Observed source coordinate 103
changes D→X for `ABWECHSELND`; the invalid printed C at index 80 is filled
with D for the I in `FELDKRIEGSKASSE`. These zero-based changes cost one
observed-coordinate substitution and one printed-glyph fill. The frame and
published key are unchanged.

</details>

## p174 A3

The current copy-supported instruction is **in möglichst kleinen Scheinen
senden**: send the money in notes as small as possible. Its reference
`OKM1A4A11333OP` remains literal. Only 79 of the advertised 98 coordinates
survive in p174 itself; the complete evidence is in p195. The drawer below
preserves the earlier reconstruction as a historical comparison.

<details>
<summary>Earlier A3 reconstruction — superseded by the complete-copy evidence</summary>

The early edition modeled the advertised 98 slots by appending nineteen
unknown coordinates to the 79-coordinate source, after “Did not finish.”
It also restored the complete printed group GAVGX omitted by earlier OCR.

**Raw output — conditional 98-slot frame; nineteen absent tail coordinates left unknown:**

```text
INM???LICHS???EINEN???EINEN???DENLX???1A4A1????OP
```

**Edited output — same conditional 98-slot frame; proposed first 33 positions:**

```text
INMOEGLICHSTKLEINENSCHEINENSENDENLX???1A4A1????OP
```

**Readable German — proposed body excerpt under the incomplete-tail model:**

> In möglichst kleinen Scheinen senden …

The proposal filled twelve absent coordinates without changing an observed
p174 value; seven remained unknown. Its L after SENDEN and 1A4A1 labels were
retained. Three placements supported the same ordinary prefix:

| Gap before source index | Raw reading |
|---:|---|
| 77 | `INM???LICHS???EINEN???EINEN????ENLXO???A4A1????OP` |
| 78 | `INM???LICHS???EINEN???EINEN???DENLX????A4A1????OP` |
| 79 | `INM???LICHS???EINEN???EINEN???DENLX???1A4A1????OP` |

Boundary 79 was chosen from the printed interruption, before the complete
copy independently selected it within this gap family. The earlier fills
remained conjectures; the new witness subsequently contradicted one.

The original three-part package counted 371 native slots (370 valid
coordinates), 195 modeled plaintext positions, 175 fixed raw labels and
188 after its then-current proposals. These are historical package counts,
not the current cross-copy restoration total.

</details>

## Attribution and reproducibility

The unchanged Nov10–12 key is prior published work. **icekylinx and GPT-6
Astra Pro** contribute the inspected source edition and the later physical
copy comparison. The first two parts had already appeared as unreviewed
repository OCR candidates; their frozen records and original hashes remain
in the experiment. Bounded prior-work checks did not locate an explicit
published discussion of this message, without establishing universal priority.

The [original source package](../../experiments/crown_airlift/README.md)
keeps the early frame and repair audit. The [copy-retrieval package](../../experiments/retrieved_copy_editions/README.md)
records the stronger current source relationship. Both can be reproduced.

```bash
python experiments/crown_airlift/verify.py --verify
python experiments/crown_airlift/verify.py --verify --pdf /path/to/childs.pdf
```
