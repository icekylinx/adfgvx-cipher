# A repeated negotiation assessment and a departure-order reference

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The first two printed parts of a four-part heading repeat an assessment that participation in negotiations is pointless and state that earlier messages are dealt with by an order to depart. Both source bodies remain in their complete native frames. No missing later parts, numerical references or execution of the departure order are supplied from context.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p206 excerpt](../../experiments/nov18_negotiation_repetition/sources/p206_reviewed.png) · [Inputs](../../experiments/nov18_negotiation_repetition/inputs.json) · [Position and change certificates](../../experiments/nov18_negotiation_repetition/certificates.json)

The published `Nov16-18` key is unchanged. [Original OCR records](../../experiments/nov18_negotiation_repetition/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/nov18_negotiation_repetition/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p206 B1](#p206-b1) | 248 | 115 / 124 | 3 | 5 |
| [p206 B2](#p206-b2) | 236 | 113 / 118 | 2 | 0 |

## p206 B1

**Source transcription — header:** `B) ZÖN v OKM (08.14 p.m., November 18th); 1600 (11/18); 4 TEILE; 1 TL RICHI-[2-like]48`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ANXOKMXERBETENEWIEDERHODUNGHIESIGERRMX1XAX112??XGEHXOPXVOM?X11XTEWLNAHMEANV?RHAN?LUN?BNGE?AESS?ORTXRMX1?AX11222XOPXZWECKLOSX
```

**Edited output — 3 observed-coordinate substitutions and 5 source-mask fills; no insertion, deletion or reordering:**

```text
ANXOKMXERBETENEWIEDERHOLUNGHIESIGERRMX1XAX112??XGEHXOPXVOM?X11XTEILNAHMEANVERHANDLUNGENGEMAESSDORTXRMX1?AX11222XOPXZWECKLOSX
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> An OKM. Erbetene Wiederholung hiesiger RM 1 A 112?? GEH OP vom ? 11. Teilnahme an Verhandlungen gemaess dort RM 1?A 11222 OP zwecklos.

**Meaning:** The first part gives the requested repetition of a locally issued reference and states that participation in negotiations, according to the cited message, is pointless. The exact reference numbers, date-like labels and scope of those negotiations remain unresolved; the statement does not establish whether negotiations occurred.

**Editorial limits.**

- All 248 native source slots are retained, including the four dashes in A---- and two dashes in FVG--. Five dash values are supplied by the readable proposal and one reference-field dash stays unresolved.
- The header length digit is 2-like but imperfectly printed. The header is therefore transcribed RICHI-[2-like]48; the 248-slot body is counted independently from the source and does not erase the glyph qualification.
- WIEDERHODUNG to WIEDERHOLUNG, TEWLNAHME to TEILNAHME, and the incomplete VERHANDLUNGEN/GEMAESS/DORT wording have explicit costs: three observed substitutions and five dash fills in total.
- The four-part heading is retained. This edition covers the two printed parts shown here and supplies no missing part 3 or 4.
- The reference-field unknown at plaintext 103 is a printed dash under pair X?, with domain {A,C,K,M,O,X}; it cannot be a numeral, while X remains a possible separator label.
- B1 plaintext 45 and B2 plaintext 22 share square cell VA. B1 plaintext 46 and B2 plaintext 59/69 share GG. B1 plaintext 58 is GF; B2 plaintext 40 is GD and 41 is AF. These five distinct fully observed unknown square cells must take distinct labels from {0,3,4,5,6,7,8,9}; repeated cells must agree.

## p206 B2

**Source transcription — header:** `B) ZÖN v OKM (08.14 p.m., November 18th); 1600 (11/18); 4 TEILE; 2 TL RICHI-236`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
DORTIGEXNRXRMX1XAX1122?XOPXUNDRMX1XAX112??XOPXUNDRMX1UAX112?1XOPXVOMX?X11MDURCHDENHIWRGEGEBENENABMARSCHBEFEHLERLEDIGTX
```

**Edited output — 2 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
DORTIGEXNRXRMX1XAX1122?XOPXUNDRMX1XAX112??XOPXUNDRMX1UAX112?1XOPXVOMX?X11XDURCHDENHIERGEGEBENENABMARSCHBEFEHLERLEDIGTX
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Dortige Nr. RM 1 A 1122? OP und RM 1 A 112?? OP und RM 1UA 112?1 OP vom ? 11 durch den hier gegebenen Abmarschbefehl erledigt.

**Meaning:** The second part states that the cited messages have been dealt with by the order to depart issued locally. It records the order and its effect on the correspondence, not proof that the troops completed their departure. The literal 1UA reference and all unresolved number-like fields remain unchanged.

**Editorial limits.**

- All 236 native coordinates are visible, with no source erasures. The earlier OCR contains only 196 coordinates; restoring the omitted visible row is a source transcription correction, not a 40-coordinate historical insertion.
- The two word or separator proposals are HIWR to HIER and the M after the literal date-like 11 to separator X. Each costs one observed-coordinate substitution.
- 1UA is retained literally, despite the nearby repeated 1A reference pattern. No numerical field is repaired to match a presumed sequence.
- The five remaining ? positions arise from fully observed unknown square cells. The shared-cell and distinct-cell constraints are given with part 1 and enforced by a single injective completion witness.

## Coupled unresolved reference labels

Indices below are zero-based plaintext positions, matching the certificates. The fully observed unknown square cells share the unused label set `{0, 3, 4, 5, 6, 7, 8, 9}`. Repetitions of a cell must agree, while different cells must take different labels in one complete square.

| Cell or source uncertainty | Part 1 positions | Part 2 positions | Constraint |
| --- | --- | --- | --- |
| VA | 45 | 22 | Same unresolved digit in both parts |
| GG | 46 | 59, 69 | Same unresolved digit at all three positions |
| GF | 58 | — | A different unused digit |
| GD | — | 40 | A different unused digit |
| AF | — | 41 | A different unused digit |
| X? from the printed source dash | 103 | — | Domain `{A, C, K, M, O, X}`; no digit values are possible |

No reference number is completed independently of these constraints, and no repeated field supplies a historical digit value by itself. The preserved `1UA` spelling in part 2 is separate from those unresolved labels.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/nov18_negotiation_repetition/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
