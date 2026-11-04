# p167 D — Captain and replacement-detachment dispatch fragment

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Partial word proposal and source review: icekylinx and GPT-6 Astra Pro.**
The fragment concerns a captain's dispatch to a replacement detachment.
The established word layer reads `HPTM`, the title ending `CHEF`, `WIRD`,
and `ERSATZABTLG ABBEFOERDERT`, followed by `NACHCHEF`. An additional name
proposal reads **Zimmermann**, supported by another telegram that names a
captain in the radio service. The full title, destination and footer remain
unread.

## Conditional name proposal

**Readable German — optional Zimmermann reading; unread fields remain omitted:**

> Hptm. Zimmermann […] Chef wird […] Ersatzabtlg abbefoerdert. Nachchef […]

The raw ten-letter field `LIMMER2ANG` can be read as **ZIMMERMANN** at four
additional observed-coordinate substitutions. A separate radio-service
telegram, [p121 B1](../radio/nov4_repetition_and_connections.md#p121-b1),
directly reads `HPTM ZIMMERMANN` while asking about the Bucharest–Constanza
connection. Its complete observed pairs support the proposed name and
rank; they do not establish that both messages concern the same officer.

The new name layer extends the interpreted spans from 45 to 55 positions.
It retains all six unknown positions, the opaque `KODESEL` and title fields,
and the uncompleted destination and footer. The omitted intervals are
15–30, 39–53 and 86–94; no given name or biographical identity is supplied.

<details>
<summary>Name proposal and exact source cost</summary>

**Edited output — optional ZIMMERMANN proposal; 14 observed substitutions, 2 source-mask fills and 2 added-slot fills; 89/95 fixed labels:**

```text
HPTMXZIMMERMANNKODESELXFESDEILOCHEFWIRDN0?HRA2T11?RK?RERSATZABTLGABBEFOERDERTXNACHCHEFT1B?7?17?
```

| Original source index | Additional observed change | Name repair |
| ---: | --- | --- |
| 160 | `D`→`F` | Initial `L`→`Z` |
| 57, 132 | `G`→`A`, `D`→`F` | `2`→`M` |
| 66 | `D`→`X` | Final `G`→`N` |

The four changes have the same positions and cost in all six retained
frames. Repricing all 125 permitted short-group layouts with the added name
span leaves the same six minima, now at 14 substitutions. The new name
does not favor a particular missing-coordinate placement.

</details>

## p167 D

**Readable German — three proposed spans; each omission retains an unread field:**

> Hptm. […] Chef wird […] Ersatzabtlg abbefoerdert. Nachchef […]

The omissions cover positions **5–30**, **39–53** and **86–94** respectively.
`Chef` is the ending of the unidentified title-like `FESDEILO…` field.
The fragment mentions a captain and dispatch in connection with a replacement
detachment; the full destination and the person's identity remain unread.
`NACHCHEF` is retained as the proposed closing designation.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 190-slot frame with three added unknowns, unchanged Nov7–9 key; 84/95 fixed positions:**

```text
H?TMXLIMMER2ANGKODESELXFESDEILO?HEFWIRDN0?HRA2T11?RK?RZRLATZRBTLGJBBEAFE?DERF??ACHCHEFT1B?7?17?
```

**Edited output — partial word proposal in the same frame; ten observed substitutions, two source-mask fills and two added-slot fills; 89/95 fixed labels:**

```text
HPTMXLIMMER2ANGKODESELXFESDEILOCHEFWIRDN0?HRA2T11?RK?RERSATZABTLGABBEFOERDERTXNACHCHEFT1B?7?17?
```

</details>

All output outside the proposed spans stays exactly raw. In particular,
`LIMMER2ANG`, `KODESEL`, `FESDEILO` and the garbled destination/reference
fields are preserved. The 89 fixed labels include those opaque fields;
they are not 89 independently read historical characters.

## Source frame and exact price

The body has **187 native slots**, including the invalid printed `C` and `W`
and two dashes; **183** slots are valid coordinates. The header advertises
**190**. Three groups contain four glyphs: `DFGX`, `VVGD` and `WVDG`.
Inserting one unknown at each group's five possible boundaries gives
**125** source-retaining models.

For the stated word spans, all 125 models are priced exactly. **Six** tie
at ten observed substitutions. Their insertion boundaries are
`[35,59,100]`, `[35,59,101]`, `[36,59,100]`, `[36,59,101]`,
`[37,59,100]` and `[37,59,101]`, measured before original source slots.
Two require four supplied unknown values rather than five. The displayed
primary is the first of those two, **[36,59,100]**. This selection is
conditioned on the word proposal, not proof of historical gap locations.
No source slot is deleted, moved or copied.

| Change class | Exact primary events, zero-based |
|---|---|
| Observed substitutions | Source 34 D→X, 52 A→X, 53 X→F, 56 D→A, 82 X→G, 117 D→X, 119 X→V, 126 F→V, 158 F→V, 166 F→D |
| Existing source-mask fills | Invalid `C` at source 91→G; dash at source 131→A |
| Added-slot fills | Model 60→F and 102→D |
| Remaining unknown coordinates | Added model 36; invalid `W` at source 98; dash at source 130 |

The six unresolved plaintext positions are **41, 49, 52, 89, 91 and 94**.
Positions 41 and 91 share square cell `VF`; position 49 uses `XA`, the
opposite digit in `{5,6}`. The three remaining coordinate masks impose
additional coupled domains. All **432** complete square/mask assignments
for the primary are enumerated and exactly re-encrypted; no one completion
is selected. The certificate retains the alternative maps and their full
compatibility witnesses too.

## Source and credit

Childs, printed p167 / PDF p170, section D. The header reads
`NKJ v LP (03.23 a.m., November 10th)` and
`(RAT) SSD BLITZBLUECHER (9/11) 2245; RICHI-190`.
The original `(9/11)` corrects the earlier unreviewed OCR's `(8/11)`.

<details>
<summary>Literal source transcription</summary>

**Source transcription — all 187 native slots; C, W and both dashes remain literal:**

```text
GXVVV AGAFF AXDAF XGVFD VDAGA XAXVX DGAFD DFGX
VDDDV XFVAD FVAAX FFDGD VVGD VVVDD XXDDD DVGFX
GGDGX GFVGV GVVCX VDVXX WVDG XDVXD DDXDF GXVGV
DXXVV GVXDF GVV-- DDDFG XVXFA XXDAA DXVFF VVDGD
XFGDG XXDDF DXDDD XXDXX FADGX FGDXG
```

</details>

[Original PDF, p170](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
· [Reproduction and provenance](../../experiments/p167_captain_dispatch_fragment/README.md)
· [Full source-map and repair certificate](../../experiments/p167_captain_dispatch_fragment/certificates.json).

The period key retains Lasry, Niebel, Kopal and Wacker's credit, and Lasry's
2017 key-list provenance. The earlier OCR is preserved separately. The
source review and limited dispatch-word proposal are by
**icekylinx and GPT-6 Astra Pro**.
