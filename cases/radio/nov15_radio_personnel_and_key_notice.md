# November 15: Warsaw radio personnel and a repeated key notice

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p197 preserves a two-part order concerning radio personnel in Warsaw
and a second physical witness of the [p189 C December-key notice](../context/p189_C.md).
All three records use the unchanged published **Nov13–15b** key. The first
part of the personnel order has a five-slot source deficit; its proposed
reconstruction is explicitly conditional. The complete second part directly
names **Posen** and reads **`IN MARSCH ZU SETZEN`**.

| Record | Printed source slots | Analysis-frame slots | Fixed raw positions | Observed substitutions | Source-mask fills | Inserted-slot fills |
|---|---:|---:|---:|---:|---:|---:|
| p197 A1 | 193 | 198, conditional gap | 93/99 | 1 | 1 | 5 |
| p197 A2 | 144 | 144, native | 68/72 | 0 | 0 | 0 |
| p197 B | 124 | 124, native | 60/62 | 3 | 0 | 0 |

The counts describe the stated frames and proposals, including unresolved
numerical labels. They do not count every displayed label as an independently
authenticated historical character. Period-key credit remains with George
Lasry and collaborators as recorded in [data/keys.json](../../data/keys.json).


**Reviewed source crops:** [p197_reviewed.png](../../experiments/nov15_radio_personnel_and_key_notice/sources/p197_reviewed.png) · [p189_reviewed.png](../../experiments/nov15_radio_personnel_and_key_notice/sources/p189_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p197 A1

[Reviewed source image — source-PDF reference](../../experiments/nov15_radio_personnel_and_key_notice/inputs.json).

**Source transcription — shared header and first-part length:**

```text
A) WAU v LP (03.55 p.m., November 15th)
14.50 2 TLE
1 TL RICHI-198
```

The five printed rows contain **193 slots**, including one dash in `VDVG-`,
against the advertised **198**. This edition keeps those 193 source slots
unchanged in the literal record. Its proposed analysis frame inserts **five
unknown slots at source boundary 165**, between the final row's `AFXFF` and
`GFVAX`. That location is an editorial hypothesis, not a printed gap mark.

**Raw output — conditional 198-slot frame with five added unknown slots; 93/99 fixed positions:**

```text
FESTUNGSFUNKAXWARSCHAUXDASGESAMTE?MBEREIC?DESGOUV?RNEMENT?WARSCHA?VERFUEGBAREFUN?ERPERSONALISTNMCHX
```

**Edited output — same conditional frame; one observed-coordinate substitution, one source-mask fill and five inserted-slot fills; 99/99 fixed positions:**

```text
FESTUNGSFUNKAXWARSCHAUXDASGESAMTEIMBEREICHDESGOUVERNEMENTSWARSCHAUVERFUEGBAREFUNKERPERSONALISTNACHX
```

The complete price, with zero-based source indices, is:

| Operation | Location | Proposed value |
|---|---|---|
| Observed-coordinate substitution | Source index 98 | `A → V`, giving `NACH` in place of raw `NMCH` |
| Source-mask fill | Printed dash at source index 134 | `D` |
| Five-slot insertion and fills | Source boundary 165 | `AAFFX` |

**Readable German — complete edited stream under the conditional gap model:**

> Festungsfunka Warschau. Das gesamte im Bereich des Gouvernements Warschau verfuegbare Funkerpersonal ist nach

`FESTUNGSFUNKA` is retained as transmitted. The sentence continues in the
native second part. That continuation independently gives the destination
and action, but does not supply every missing first-part letter.

### Comparison of the possible gap locations

For this exact 99-position candidate and the unchanged key, the verifier
compares **all 194 source boundaries** at which one five-coordinate gap
could be inserted. It prices only changes to observed coordinates in the
following column; the one printed-mask fill and five added-slot fills remain
separate in every comparison.

| Source boundary | Observed-coordinate substitutions |
|---:|---:|
| 163 | 2 |
| 164 | 2 |
| **165** | **1** |
| 166 | 2 |
| Every other boundary | At least 3 |

Boundary 165 is the unique minimum **for this candidate and this single-gap
family**. The [certificate](../../experiments/nov15_radio_personnel_and_key_notice/certificates.json)
retains all prices and the raw domains and edits for every frame within one
substitution of the minimum. The comparison does not prove unique historical
wording or exclude other damage mechanisms. The untouched 193-slot decode
and its unpaired final coordinate are retained separately in the certificate.

## p197 A2

**Source transcription — second-part label:**

```text
2 TL RICHI-144
```

**Raw output — native 144-slot frame; 68/72 fixed positions:**

```text
XFESTUNGSFUNKAXPOSENXINMARSCHZUSETZENXXINACHXFUNKLEITUNGHEIMATXNRX???6?5
```

**Readable German — complete raw stream, with spacing and punctuation only:**

> Festungsfunka Posen in Marsch zu setzen. I Nach Funkleitung Heimat Nr ???6?5.

No coordinate or key change is used. The literal sequence **`INACH`** is
shown as **`I Nach`**, without expanding it into an office or correcting it
into a different signature. The source's `VD AVD` is five printed
coordinates despite its internal space.

The final **`???6?5`** remains six output positions. The first, second and
fifth labels arise from three different unknown square cells; the second
and third positions use the **same** cell and must have the same value.
Each unknown cell has domain `{2, 3, 4, 7, 8, 9, Q, Y}` under the published
partial square, and different cells must remain distinct. This coupled
uncertainty is retained in the certificate; no historical reference number
is assigned.

## p197 B

**Source transcription — literal header:**

```text
B) NKJ v LP (04.24 p.m., November 15th)
10.00 (15/11)
RIZI-124-
```

The dash after the length label is outside the ciphertext. The visible
final group `XFXX` belongs to the 124-slot body; the earlier OCR omitted it.

**Raw output — native 124-slot frame; 60/62 fixed positions:**

```text
UNLOES?A?EHUNKSPRUECHENACHDEZEMBERSCHLUESSELENTZIFFERNXXIRRTUM
```

**Edited output — three observed-coordinate substitutions; no fills; 62/62 fixed positions:**

```text
UNLOESBAREFUNKSPRUECHENACHDEZEMBERSCHLUESSELENTZIFFERNXXIRRTUM
```

The changes are **source index 23 V→F**, **62 A→D**, and **93 F→G**. Unknown
square cells are not filled to make these words: the letters B and R already
occupy other cells, so the corresponding word proposals require coordinate
changes.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Unloesbare Funksprueche nach Dezemberschluessel entziffern. Irrtum.

### What the second copy supports

The independently inspected [p189 C source — source-PDF reference](../../experiments/nov15_radio_personnel_and_key_notice/inputs.json)
has the same 124-coordinate body except **source index 93**, where p189
prints **G** and p197 prints **F**. Their reception times differ; the common
internal `10.00` and November 15 date are preserved.

That single difference accounts for **B** versus an unknown at plaintext
index **6**. Thus p189's raw reading directly supports the proposed B in
p197. Both copies still have the unknown at plaintext index **8** and raw H
at index **10**. Neither copy independently supplies the proposed R or F at
those two positions. Their shared repairs are not promoted into independent
corroboration.

**`DEZEMBER`** and **`IRRTUM`** are directly decoded in both copies. The final
word is retained without deciding whether it corrects, cancels or otherwise
qualifies the preceding instruction.

## Verify

[Inputs and source transcriptions](../../experiments/nov15_radio_personnel_and_key_notice/inputs.json) ·
[Exact certificates](../../experiments/nov15_radio_personnel_and_key_notice/certificates.json) ·
[Reproduction notes](../../experiments/nov15_radio_personnel_and_key_notice/README.md).

```sh
python experiments/nov15_radio_personnel_and_key_notice/verify.py --verify
python experiments/nov15_radio_personnel_and_key_notice/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check reproduces both inspected crops and compares their
RGB pixels. The verifier also checks independent transposition offsets,
all 194 candidate-conditioned gap prices, the cross-copy coordinate
comparison, the complete readable-label mappings, and re-encryption using
one consistent global completion of the partial square. Those completion
witnesses are explicitly nonhistorical. Earlier repository and published-key
credits remain separate from the present source review.
