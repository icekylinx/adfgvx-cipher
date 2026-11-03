# November 11: Romanian mobilization and a crossing report

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

The surviving second part on printed page 180 reports mobilization and a crossing. Its last line is followed by **“(jammed to end)”**. The source contains **235 printed slots**, including two dashes, under a **RICHI-240** header. Keeping every printed slot and appending five unknown coordinates produces a conditional 240-coordinate frame with **110 of 120 plaintext positions fixed** under the unchanged published Nov10–12 key.

Six narrow word proposals raise that count to **116 of 120**. They cost **four observed-coordinate substitutions, one printed-mask fill and four fills of added tail slots**. The remaining source dash, first added tail slot and two linked occurrences of an unknown square cell stay unresolved. Date-like fields, the shortened **KRIEGSZUSAND** and the literal **ZIMNICA** are preserved. This is a partial source edition of one surviving part; the absent first part and a unique original transmission are not reconstructed.

Research and editorial work: **icekylinx and GPT-6 Astra Pro**. The period key is credited to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, with its publication details retained in [inputs.json](../../experiments/nov11_romanian_mobilization_report/inputs.json). Earlier local native and terminal-mask trials already exposed this lead. Their transcription and reproducible outputs are retained in [prior_candidates.json](../../experiments/nov11_romanian_mobilization_report/prior_candidates.json); this edition does not claim first-decipherment priority.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## p180 B2

Literal header: `B) LP v ZON (0[1/4].02 p.m. November 11th); -----; 2 TL RICHI-240`.

The damaged hour glyph remains ambiguous between `01.02` and `04.02`. The older OCR reads 01.02. An enlarged comparison with the same page’s clear 4 in the D1 header does not decisively exclude either reading. The complete alternatives are `B) LP v ZON (01.02 p.m. November 11th); -----; 2 TL RICHI-240` and `B) LP v ZON (04.02 p.m. November 11th); -----; 2 TL RICHI-240`. Neither is selected by the body’s date or hour fields.

[Printed page 180, B2 and its terminal-jamming note — source-PDF reference](../../experiments/nov11_romanian_mobilization_report/inputs.json)

[The neighboring D1 header used only for glyph comparison — source-PDF reference](../../experiments/nov11_romanian_mobilization_report/inputs.json) is not a second recovered body in this edition.

**Source transcription — all 235 native printed slots, including both dashes:**

```text
GVGDA GAAFD GXGVA XVXAX ADXFX XGXGX GDXXG XDDXG
AAVVV VFXXD XGXFD XDVXV GVAGA GFGAV AADFF DAAXX
XXDGG XXADG AFDAA AAAGD GAADX VDDDX FDXAD XFVAX
ADAAV XDDAV DAADA DAAAG ADXAD AGFVA GFXXV XFDXX
DGFDD FAGDX DVGVX XVGXF XAXDV AGXDX XDDFG XGGDA
--AVG GAVAV XDXFX XFFFF XVGXV AGXVG GVGAD
```

Source note immediately below the body: `(jammed to end)`.

The printed 2 TL identifies this as a second part. No first-part body is present under this reception header on page 180. All five-character groups remain intact and in order; the final line has seven groups. Source dashes occupy indices **200 and 201**. All indices in this edition are zero-based.

## Source frame and raw evidence

The native 235-slot stream is odd. Its unchanged-key diagnostic has 117 complete pairs and leaves the coordinate **G at source index 146** unpaired in the intermediate stream. It is retained below so the readable 240-slot model cannot be mistaken for the direct native result.

**Raw output — native 235-slot diagnostic, with the unpaired coordinate recorded separately:**

```text
HR?GO4?MAKDHNKE2GLN?P4??RUYGXKENOBGC?141UND4XAXDA1GXL1A1ETN?I?MUG1FE113VKRGX?NJFSAXD?01DTX4Q1RW?ENAJQF1DNDE1XR12TUHNJ
```

The 240-slot model appends unknowns at model indices **235–239**. Every earlier model index maps to the identically numbered printed slot. The five-slot shortfall and the explicit terminal-jamming note motivate this position. They do not prove that an interior loss is impossible, and no exhaustive search for a unique loss geometry is claimed.

**Raw output — unchanged Nov10–12 key in the conditional 240-slot terminal-loss frame:**

```text
RUMA?NXMOBILMACHUNG?X11XA1GEORDNETXX1XTAG10X?1LXKRIE?FZUSAND10X1TX?UHRABENDSXFEIND1?X11XTUR?UMAGUR2?EZIMNIC?UEBERGE?ETZT
```

The words MOBILMACHUNG, TAG, UHRABENDS and FEIND are already fixed in this frame. Parts of ANGEORDNET and the two place-like sequences need explicit changes or fills. The numerical labels remain outputs of the published partial square, not independently established calendar dates.

## Priced word proposal

**Edited output — 4 observed-coordinate substitutions, 1 printed-mask fill and 4 added-tail fills:**

```text
RUMAENXMOBILMACHUNG?X11XANGEORDNETXX1XTAG10X?1LXKRIEGSZUSAND10X1TX?UHRABENDSXFEIND1?X11XTURNUMAGURELEZIMNICAUEBERGESETZT
```

**Readable German — the complete edited stream, with spacing and punctuation only:**

> Rumaen. Mobilmachung ? 11 angeordnet. 1. Tag 10 ?1L. Kriegszusand 10 1T ? Uhr abends. Feind 1? 11 Turnumagurele Zimnica uebergesetzt.

**Conditional interpretation — partial report and unresolved fields:**

The proposed wording concerns Romanian mobilization, an order, a state of war and an enemy crossing. TURNUMAGURELE and ZIMNICA are the exact candidate letter sequences. No modern place spelling is inserted. KRIEGSZUSAND retains the missing T of the resulting stream; replacing it by the standard KRIEGSZUSTAND would add a plaintext position and is outside this frame. The fields following MOBILMACHUNG, TAG, KRIEGSZUSAND and FEIND remain literal, including ? 11, 10 ?1L, 10 1T ? and 1? 11. A specific mobilization date, declaration time or crossing date is not selected.

| Proposed span | Plaintext start | Observed changes | Printed-mask fills | Added-tail fills |
| --- | ---: | ---: | ---: | ---: |
| RUMAEN | 0 | 1 | 0 | 0 |
| ANGEORDNET | 24 | 1 | 0 | 0 |
| KRIEGSZUSAND | 48 | 1 | 1 | 0 |
| TURNUMAGURELE | 88 | 1 | 0 | 2 |
| ZIMNICA | 101 | 0 | 0 | 1 |
| UEBERGESETZT | 108 | 0 | 0 | 1 |
| **Total** | | **4** | **1** | **4** |

The substitutions within A1GEORDNET and MAGUR2 replace the literal raw labels 1 and 2 only in those disclosed word proposals. The separate number/date fields are unchanged. The precise coordinate ledger is:

| Model index | Printed source index | Before | After | Cost class |
| ---: | ---: | :---: | :---: | --- |
| 93 | 93 | A | D | Observed-coordinate substitution |
| 117 | 117 | V | X | Observed-coordinate substitution |
| 195 | 195 | X | V | Observed-coordinate substitution |
| 216 | 216 | F | G | Observed-coordinate substitution |
| 201 | 201 | source dash | X | Printed-mask fill |
| 236 | absent | unknown | D | Added-tail fill |
| 237 | absent | unknown | G | Added-tail fill |
| 238 | absent | unknown | A | Added-tail fill |
| 239 | absent | unknown | D | Added-tail fill |

There are **five added coordinates** in the frame, even though the proposal fills only four. Model index 235 remains unknown. The unchanged source dash at index 200 also remains unknown. No printed coordinate is excluded.

## Coupled residual possibilities

| Plaintext index | Coordinate pair | Exact remaining domain | Coordinate source |
| ---: | :---: | --- | --- |
| 19 | XA | 5, 6, 7, 8, 9 | Printed source 227,77 |
| 44 | ?A | 3, 4, 5, 6, 7, 8, 9, C, L, O | Source dash 200 and printed source 20 |
| 66 | XA | 5, 6, 7, 8, 9 | Printed source 38,113 |
| 83 | ?X | 1, 5, 6, 7, 8, 9, E, N, V, X | Added model slot 235 and printed source 85 |

Positions **19 and 66 use the same unknown square cell** and must have the same label. They cannot independently be assigned different dates or hours. If source dash 200 is completed as X, position 44 also uses that same XA cell. If added slot 235 is completed as X, position 83 uses XX, whose label must differ from XA under a one-to-one square completion.

The verifier checks all **120 assignments** of the five missing square labels and all **36 coordinate completions** of source 200 and model 235: **4,320 exact full re-encryptions**. They yield **270 distinct residual label tuples** at positions 19,44,66,83. One complete witness for every tuple is retained in the certificate. Those additional fills demonstrate the alternatives; none is adopted into the displayed proposal.

## Evidence and reproduction

| Quantity | Count |
| --- | ---: |
| Physical source records | 1 |
| Native printed slots | 235 |
| Valid printed coordinates | 233 |
| Printed masks | 2 |
| Added tail slots | 5 |
| Modeled coordinates / plaintext positions | 240 / 120 |
| Raw fixed / edited fixed positions | 110 / 116 |
| Observed substitutions | 4 |
| Printed-mask fills / added-tail fills | 1 / 4 |
| Source exclusions | 0 |

The frozen OCR divided this body into separate 40-slot and 196-slot blocks. Those earlier blocks are preserved in [ocr_snapshot.json](../../experiments/nov11_romanian_mobilization_report/ocr_snapshot.json); they are not silently treated as two physical messages. The reviewed source body has 235 slots.

The [portable verifier](../../experiments/nov11_romanian_mobilization_report/verify.py) checks source-image hashes and RGB bytes, the optional original-PDF rendering, the unchanged key, every source/model index, all coordinate repairs, the live case’s literal header and complete displays, preservation of date-like fields, and the coupled completion witnesses. [certificates.json](../../experiments/nov11_romanian_mobilization_report/certificates.json) retains all domains and exact ledgers.

```sh
python experiments/nov11_romanian_mobilization_report/verify.py --verify
python experiments/nov11_romanian_mobilization_report/verify.py --verify --pdf /path/to/childs.pdf
```
