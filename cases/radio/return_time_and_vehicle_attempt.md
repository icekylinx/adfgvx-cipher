# An expected return and an attempt to obtain a vehicle

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Two complete short native bodies report an expected return and discuss obtaining a vehicle. The first is unchanged; the second has four explicitly priced coordinate substitutions. The incomplete spelling RUECKUNFT, the literal 0100 field and the elliptical sense of VERSUCHEN remain visible.


**Reviewed source crops:** [p182_reviewed.png](../../experiments/return_time_and_vehicle_attempt/sources/p182_reviewed.png) · [p189_reviewed.png](../../experiments/return_time_and_vehicle_attempt/sources/p189_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p182 excerpt — source-PDF reference](../../experiments/return_time_and_vehicle_attempt/inputs.json) · [Reviewed p189 excerpt — source-PDF reference](../../experiments/return_time_and_vehicle_attempt/inputs.json) · [Inputs](../../experiments/return_time_and_vehicle_attempt/inputs.json) · [Position and change certificates](../../experiments/return_time_and_vehicle_attempt/certificates.json)

The published `Nov10-12` and `Nov13-15b` keys are unchanged. [Original OCR records](../../experiments/return_time_and_vehicle_attempt/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/return_time_and_vehicle_attempt/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p182 B](#p182-b) | 62 | 31 / 31 | 0 | 0 |
| [p189 B](#p189-b) | 70 | 35 / 35 | 4 | 0 |

## p182 B

**Source transcription — header:** `B) CM v CZ (20.45 p.m., November 12th); 20.20; RIZI-62`

<details>
<summary>Raw decoded text</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
RUECKUNFTVORAUSSICHTLICH0100XSX
```

</details>

**Readable German — exact nonseparator labels of the unchanged raw output:**

> RUECKUNFT voraussichtlich 0100. S.

**Meaning:** The sender reports an expected return at the literal label 0100. The closing S is not expanded, and this record does not itself identify the returning person or establish a complete itinerary.

**Editorial limits.**

- All 62 printed coordinates decode directly, with no source erasures, substitutions or frame changes. The following CM UM is printed transmission control outside the body.
- RUECKUNFT is retained with only the one K visible in the decoded stream; the standard spelling Rueckkunft would require an extra plaintext letter and is not silently inserted.
- 0100 is preserved as four literal labels. Its interpretation as a time is contextual; the body does not specify a time zone or independently identify the date.
- The neighboring Seifert service exchange does not establish that the abbreviated S here is a particular person.

## p189 B

**Source transcription — header:** `B) CM v CZ (10.10 a.m., November 14th); RIZI-70`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
VERSUCHENI6GENDECNEIWWGENZUBEKOMMEN
```

**Edited output — 4 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
VERSUCHENIRGENDEINENWAGENZUBEKOMMEN
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Versuchen, irgendeinen Wagen zu bekommen.

**Meaning:** The message concerns trying to obtain a vehicle or wagon. The terse infinitive form alone does not securely distinguish a request to try from a report of an attempt, and Wagen does not by itself identify a specific car or railway wagon.

**Editorial limits.**

- All 70 native coordinates are retained and valid. High-resolution inspection reads the last group of the first row as FGXAV, including a clear X; the earlier low-resolution Y-like impression is not retained as a fictitious source erasure.
- The ordinary-word proposal costs four observed-coordinate substitutions. The literal 6 in I6GENDE… is changed only through an explicit coordinate repair, not through a global reinterpretation of the numeral label.
- The edition does not identify a vehicle, promise that one was obtained, or infer a connection to another service message merely from the word Wagen.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/return_time_and_vehicle_attempt/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
