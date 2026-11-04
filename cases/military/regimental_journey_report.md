# A regimental journey report with unresolved route and unit labels

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This two-part native report describes a journey and assistance received after minor interruptions. The route, date-like and unit labels remain in their exact source form. The five printed dashes in part 1 are explicit source erasures: four are supplied by priced wording proposals and one remains unresolved. The Nov28–Dec1 square uses Y as the separator; X inside the displayed labels stays literal.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p225 excerpt](../../experiments/regimental_journey_report/sources/p225_reviewed.png) · [Inputs](../../experiments/regimental_journey_report/inputs.json) · [Position and change certificates](../../experiments/regimental_journey_report/certificates.json) · [Reading conventions](../../docs/reading-conventions.md)

The published `Nov28-Dec1` key is unchanged. [Original OCR records](../../experiments/regimental_journey_report/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/regimental_journey_report/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p225 B1](#p225-b1) | 254 | 122 / 127 | 8 | 4 |
| [p225 B2](#p225-b2) | 212 | 106 / 106 | 2 | 0 |

## p225 B1

**Source transcription — header:** `B) ZON v UKS (01.17 a.m., November 29th); 1130 (11/28) (VON BSL); 1 TL RICHI-254`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ARMEE?KDOXXYY?EGIMENSSTABMIT2BAONJXUNDPEISENBAHLBUUCOMPYNACCFOLGENDJTRANMPYLANDWY1KXJSINDNAKHBEREITIGUNGLEI?HTERUNL?RBRECHU?GEN
```

**Edited output — 8 observed-coordinate substitutions and 4 source-mask fills; no insertion, deletion or reordering:**

```text
ARMEE?KDOXXYYREGIMENSSTABMIT2BAONJXUNDPEISENBAHNBAUCOMPYNACHFOLGENDJTRANSPYLANDWY1KXJSINDNACHBESEITIGUNGLEICHTERUNTERBRECHUNGEN
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> ARMEE?KDOXX. REGIMENSSTAB mit 2BAONJX und P Eisenbahnbaucomp. Nachfolgend J TRANSP. LANDW 1KXJ sind nach Beseitigung leichter Unterbrechungen

**Meaning:** The first part lists a regimental staff, battalion and railway-construction company fields, and a following transport. It says minor interruptions have been overcome and continues with the journey and arrival report in part 2. The opening command designation and unit or quantity labels remain unresolved.

**Editorial limits.**

- All 254 occupied source slots are retained. The source contains one complete group of five dashes; four of its values are supplied explicitly, while the remaining command-field erasure stays unknown.
- The raw ARMEE?KDOXX unknown has domain {4, 8, A, K, O, U}. It is not filled with a separator or a presumed army designation.
- REGIMENSSTAB is retained without inserting the absent T of a familiar spelling. The labels 2BAONJX, P, J TRANSP and LANDW 1KXJ are not converted into historical unit numbers or quantities.
- EISENBAHLBUUCOMP to EISENBAHNBAUCOMP, NACCFOLGEND to NACHFOLGEND, TRANMP to TRANSP, NAKH to NACH, BEREITIGUNG to BESEITIGUNG and UNL?RBRECHU?GEN to UNTERBRECHUNGEN are explicitly priced word proposals.
- The Nov28–Dec1 key uses Y as the separator label. X remains literal within fields, including KDOXX and 1KXJ.

## p225 B2

**Source transcription — header:** `B) ZON v UKS (01.17 a.m., November 29th); 1130 (11/28) (VON BSL); 2 TL RICHI-212`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
VONPOEST7ENYIYTRENCSENUEBERPUHOINSILEININDERNACHTAMJ0YEINGETROFFENY1EDEUNTERSTUETZUNGGEFUNDENYYRYIYRGTJXYY
```

**Edited output — 2 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
VONPOEST7ENYIYTRENCSENUEBERPUHOINSILEININDERNACHTAMJ0YEINGETROFFENYJEDEUNTERSTUETZUNGGEFUNDENYYRYIYRGTJXYY
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Von POEST7EN I TRENCSEN ueber PUHO in SILEIN in der Nacht am J0 eingetroffen. Jede Unterstuetzung gefunden. R I RGTJX.

**Meaning:** The continuation reports arrival in SILEIN during the night represented by J0, after a journey from the literal POEST7EN I TRENCSEN route field via PUHO, and says every assistance was received. The place spellings, date-like label and closing unit field are not silently normalized or independently identified.

**Editorial limits.**

- The native 212-coordinate second part has no source erasures or length changes. The sole word proposal 1EDE to JEDE costs two observed-coordinate substitutions.
- POEST7EN retains its numeral-like 7, and SILEIN retains the source-length spelling. Neither is silently converted into a presumed historical place name.
- J0, I and RGTJX remain literal. The body date-like label is not chosen from the November 29 interception header or the separate 11/28 originating line.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/regimental_journey_report/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
