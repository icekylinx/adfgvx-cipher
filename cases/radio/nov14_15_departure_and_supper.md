# Postponed departure, a supper query and a farewell

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Three separate service messages retain their complete native source frames: a postponed departure with reassurance, a proposed warm supper and headcount enquiry, and a short farewell. Source-transcription corrections recover the positions omitted by earlier OCR; ordinary-word repairs, printed-dash fills and literal abbreviations remain explicit.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p193 excerpt](../../experiments/nov14_15_departure_and_supper/sources/p193_reviewed.png) · [Reviewed p196 excerpt](../../experiments/nov14_15_departure_and_supper/sources/p196_reviewed.png) · [Inputs](../../experiments/nov14_15_departure_and_supper/inputs.json) · [Position and change certificates](../../experiments/nov14_15_departure_and_supper/certificates.json)

The published `Nov13-15b` key is unchanged. [Original OCR records](../../experiments/nov14_15_departure_and_supper/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/nov14_15_departure_and_supper/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p193 C](#p193-c) | 212 | 104 / 106 | 3 | 2 |
| [p193 D](#p193-d) | 82 | 40 / 41 | 4 | 0 |
| [p196 A](#p196-a) | 74 | 37 / 37 | 0 | 0 |

## p193 C

**Source transcription — header:** `C) --- v CM (1.15 p.m., November 14th); RIZI-212`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ABMARSCHVERSCHOBENKEIN6RUNDZURBEUNRUHIGUNGABMERFOLGTSPA5TERINVEREINBARTERWCISEDHFNBLEIBTBET?BEREITX?EIFERT
```

**Edited output — 3 observed-coordinate substitutions and 2 source-mask fills; no insertion, deletion or reordering:**

```text
ABMARSCHVERSCHOBENKEINGRUNDZURBEUNRUHIGUNGABMERFOLGTSPAETERINVEREINBARTERWEISEDHFNBLEIBTBETRBEREITXSEIFERT
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Abmarsch verschoben. Kein Grund zur Beunruhigung. Abm. erfolgt spaeter in vereinbarter Weise. DHFN bleibt BETR bereit. Seifert.

**Meaning:** The message reports that departure has been postponed, says there is no cause for alarm, and states that departure will occur later as agreed. The closing readiness phrase is retained as DHFN bleibt BETR bereit; the edition does not identify DHFN as a particular place or silently expand BETR.

**Editorial limits.**

- The source prints 210 valid coordinates followed by two distinct dashes. Together these are 212 occupied slots, exactly matching the header. The older OCR omitted the two dashes; restoring their positions is a source-transcription correction, not insertion of hypothetical missing ciphertext.
- 6RUND → GRUND, SPA5TER → SPAETER and WCISE → WEISE require three observed-coordinate substitutions. The printed dashes at indices 210 and 211 are explicitly filled with F and G. They supply the R of BETR and the initial S of SEIFERT under the fixed frame.
- ABM is retained as an abbreviation. DHFN and BETR are literal labels, without geographical identification or a hidden expansion in the readable stream.
- The source reports a postponement and a future intention; it does not establish that the later departure occurred.

## p193 D

**Source transcription — header:** `D) CZ v CM (1.10 p.m., November 14th); RIZI-82`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
WOLLGNWALMESA?ENDBRXBEREITENVWIEVXKOEPFEX
```

**Edited output — 4 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
WOLLENWARMESABENDBRXBEREITENXWIEVXKOEPFEX
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Wollen warmes Abendbr. bereiten. Wiev. Koepfe.

**Meaning:** The proposed wording says the sender intends to prepare a warm evening meal and asks how many people there are. Abendbr. and Wiev. remain abbreviated in the quoted stream. The message does not record a supplied headcount or confirm that the meal was prepared.

**Editorial limits.**

- All 82 source coordinates are printed and retained. The earlier OCR block had only 76 coordinates; the corrected native transcription contains the complete second row and final VG.
- WOLLGN → WOLLEN, WALMES → WARMES, A?ENDBR → ABENDBR and the V following BEREITEN → separator X cost four observed-coordinate substitutions in total. No source glyph is erased or filled.
- The raw question mark comes from an unassigned square cell even though its two source coordinates are known. The proposed B therefore requires an observed-coordinate change to a known B pair; it is not a free square completion or erasure fill.
- ABENDBR and WIEV are retained literally. The natural evening-meal and headcount interpretation is attached to the explicitly repaired candidate, not presented as an unchanged raw sentence.
- This is a separate source record five minutes before the neighbouring C reception. No response relationship or combined message is assumed.

## p196 A

**Source transcription — header:** `A) CZ v CM (15.22 p.m., November 15th); 16.15; RIZI-74`

<details>
<summary>Raw decoded text</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ABFAHRXWIEDERSEHENXGRUESSEKRAMMXOPITZ
```

</details>

**Readable German — exact nonseparator labels of the unchanged raw output:**

> ABFAHR. Wiedersehen. Gruesse, Kramm. Opitz.

**Meaning:** The short unedited reading contains a departure-related opening, farewell, greetings and the names or signature labels Kramm and Opitz. It does not establish either person’s identity or assign their exact sender/addressee roles.

**Editorial limits.**

- All 74 valid source coordinates decrypt directly to 37 fixed raw labels. No observed-coordinate substitution, source fill, missing slot or frame change is used.
- The source gives ABFAHR without a final T. That shortened form is preserved in both raw and readable output; no letter is silently inserted to produce ABFAHRT.
- The header retains its anomalous 15.22 p.m. expression and separate 16.15 line. They are not normalized into a reconstructed chronology.
- KRAMM and OPITZ remain literal labels; neighbouring service traffic does not by itself identify their full names or this message’s exact historical itinerary.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/nov14_15_departure_and_supper/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
