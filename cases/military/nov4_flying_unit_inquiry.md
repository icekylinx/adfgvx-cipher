# Flying units: should they depart or remain?

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p124 section B contains a short inquiry about whether flying units
should leave or remain. The source prints **183 slots**, including **25
masked coordinates**, against an advertised **184**. A visibly short
four-slot group constrains the proposed missing coordinate, and a conditional
184-slot frame yields **92 plaintext positions, 67 fixed raw**.

The edited reading repairs ordinary words in the body while leaving the
entire opening reference untouched. It has **83/92 fixed positions** and
requires **2 observed-coordinate substitutions, 16 source-mask fills and 1
inserted-slot fill**. The published **Nov4–6** key stays unchanged. The two
equally priced local gap positions are both retained.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## p124 B

[Reviewed source image — source-PDF reference](../../experiments/nov4_flying_unit_inquiry/inputs.json).

**Source transcription — header:**

```text
Page heading: 4th NOVEMBER, 1918.
B) UKH v ZON (4.41 a.m., November ---)
RICHI-184
```

The intercept's day is missing and remains missing. The November 4 page
heading is a separate source layer. The [literal input](../../experiments/nov4_flying_unit_inquiry/inputs.json)
preserves every dash and the invalid printed `U` in `GXXGU`.

The short **XFVV** group occupies source indices **15–18**. The displayed
frame inserts an unknown coordinate at **source boundary 17**, before
original source index 17. No source slot is removed or reordered.

**Raw output — conditional 184-slot frame, boundary 17; 67/92 fixed positions:**

```text
??ERX?K??1?2??OP??ICHT?E??T?ENDLI??XXSOLLEN?LI?GERA??EI?UNG?N?B?LIEGENX?DERHIERRLEIBENXFRAGE
```

**Edited output — the same conditional frame; 2 observed-coordinate substitutions, 16 source-mask fills and 1 added-slot fill; 83/92 fixed positions:**

```text
??ERX?K??1?2??OP?NICHTVERSTAENDLICHXXSOLLENFLIEGERABTEILUNGENABFLIEGENXODERHIERBLEIBENXFRAGE
```

**Readable German — complete edited stream; the opening token stays literal:**

> ??ERX?K??1?2??OP?. Nicht verstaendlich. Sollen Fliegerabteilungen abfliegen oder hierbleiben. Frage.

The initial **17 positions** are unchanged, including **nine unresolved
positions** and the labels **1** and **2**. No addressee, serial or office is
inferred from that fragment. The literal word **Frage** stays visible at
the end; it is not silently replaced by punctuation.

**Meaning:** The proposed body says that a communication is not understood
and asks whether flying units should depart by air or remain here. It does
not identify the units or establish that either action occurred. These are
explicit word restorations from a damaged source, not a complete recovery
of its opening reference.

## Repair account

The two changes to observed coordinates, using zero-based original source
indices, are **14 G→D** and **171 A→G**. The latter repairs raw
`HIERRLEIBEN` to proposed `HIERBLEIBEN`; the former helps supply `B` in
`FLIEGERABTEILUNGEN` at a position whose other coordinate was already masked.

| Kind | Original source indices and supplied values |
| --- | --- |
| Observed-coordinate substitutions | 14 G→D; 171 A→G |
| Printed-mask fills | 7→A; 23→F; 33→F; 58 U→A; 66→X; 67→G; 68→A; 88→G; 102→A; 103→G; 135→X; 146→A; 147→V; 170→G; 175→A; 176→X |
| Added-slot fill | F at source boundary 17, model index 17 |
| Unfilled printed masks | 9, retained in the opening fragment |

All listed mask fills except source 58 fill printed dashes. Source 58 is the
invalid printed `U`, retained literally in the source transcript. The
certificate records each event with its original glyph, source index,
model index and resulting plaintext domain. Filling remaining masks with a
mechanical value produces a complete re-encryption witness, explicitly
marked **nonhistorical**; it does not supply the opening reference.

## Both local gap minima

The verifier compares all five insertion boundaries within or at the edges
of the visibly four-slot group, against the same partial edited template:

| Source boundary | Observed substitutions | Printed-mask fills | Added-slot fills |
| ---: | ---: | ---: | ---: |
| 15 | 3 | 16 | 1 |
| 16 | 2 | 16 | 1 |
| 17 | 2 | 16 | 1 |
| 18 | 3 | 16 | 1 |
| 19 | 3 | 16 | 1 |

Boundaries **16 and 17 tie**. Both add F next to the already printed F,
producing the same edited ciphertext group **XFFVV** and the same edited
plaintext. Their unfilled raw frames differ because the unknown slot lies
on opposite sides of the observed F.

**Raw output — equally priced boundary-16 alternative; 67/92 fixed positions:**

```text
??ERX?K??1?2??OP??ICHT?E??T?ENDLI??XXSOLLEN?LI?GER???EI?UNGEN?B?LIEGENX?DERHIERRLEIBENXFRAGE
```

The displayed boundary-17 frame is a presentation choice. The certificate
preserves both mappings and all five price comparisons. The comparison is
limited to this stated short-group family and fixed body proposal; it
neither proves a unique historical reading nor identifies the historical
stage at which the coordinate was lost.

## Source restoration, attribution and reproduction

Earlier repository OCR contained **178 slots**: it omitted the printed
last-row `---AV` group and misread or masked several observed coordinates.
The reviewed **183-slot transcription** restores those actual source marks.
Those machine-input corrections are separate from the one missing
coordinate hypothesized in `XFVV`.

J. Rives Childs's scan is the historical source. The period-key work of
George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, Lasry's 2017 key list,
and earlier repository work retain their credit. The frozen earlier OCR
and recomputed unchanged-key output are available in
[prior candidates](../../experiments/nov4_flying_unit_inquiry/prior_candidates.json).
No first-decipherment priority is claimed.

[Inputs](../../experiments/nov4_flying_unit_inquiry/inputs.json),
[certificates](../../experiments/nov4_flying_unit_inquiry/certificates.json),
and [reproduction instructions](../../experiments/nov4_flying_unit_inquiry/README.md)
include every raw domain, both minimal source mappings, all repair events,
the unresolved prefix and source-image pixel verification.
