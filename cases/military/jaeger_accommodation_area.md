# A Jaeger division's accommodation area near Huy

The report gives an accommodation area for a German Jaeger division south of Huy. A separately priced place-name correction identifies Vierset-Barse, supported by a historical caption; the joint numeral interpretation gives correspondence from AOK 18 to AOK 17.

**Complete edition by printed page:** [p. 183](../pages/183.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This message reports an accommodation area for a German Jaeger division near Huy. A prewar illustrated guide supplies the spelling **Vierset-Barse**, supporting one correction in its place list. The complete source body matches its advertised 230 slots, with no change to its frame.

## Vierset-Barse in the accommodation list

The received `VIERSWT X BARSE` is proposed as **VIERSET X BARSE**. A plate in
*Huy-pittoresque*, dated about 1885–1890 by the Rijksmuseum, prints the caption
**CHATEAU DE VIERSET-BARSE**. The two fields can therefore be read together as
the place-name **Vierset-Barse**. The intervening X remains the transmitted
separator; the hyphen belongs to the readable display.

The correction costs **one additional observed substitution**, source **170 D→X**.
It changes plaintext position 88 from W to E (`VD→VX`) and leaves the other
114 labels untouched. Including the earlier JAEGER repair and two dash fills,
this place-name layer costs **two substitutions and two source-mask fills**.
It adds no fixed positions: the corrected letter was already a known W.

**Readable German — place-name correction, with the published partial square:**

> An AOK 1?. Zu dort 11140 OP. Unterbringungsraum DT JAEGER DIV 13?11: MARCHE, SUEDL HUY, VIERSET-BARSE, SOHEIT. AOK 1? 1 AM.

<details>
<summary>Exact place-name proposal</summary>

**Edited output — 2 observed-coordinate substitutions and 2 source-mask fills:**

```text
ANXAOKX1?XZUXDORTX11140XOPXUNTERBRINGUNGSRAUMXDTXJAEGERXDIVX13?11XMARCHEXSUEDLXHUYXVIERSETXBARSEXSOHEITXAOKX1?X1XAM
```

</details>

The [source plate and exact check](../../experiments/p183_vierset_place/README.md)
support this spelling independently of the conditional numeral interpretation
below. MARCHE, SOHEIT and the intermediate reference remain unchanged.

## Conditional shared digits

The accommodation report gains **AOK 17** at the opening and **AOK 18** at the close, reaching **115/115 labels** under the shared interpretation. The intermediate field becomes the literal **13711**. Its 7 is coupled to AOK 17 and is not replaced by a separator. The earlier JAEGER repair and two source-mask fills are retained. The [joint reconstruction](../../experiments/nov10_joint_completion/README.md) combines the earlier Marineamt and formation interpretations with the army-number constraint and the mobilization decree; the reversed 7/9 assignment is retained there.

**Conditional interpretation — readable German under the joint square:**

> An AOK 17. Zu dort 11140 OP. Unterbringungsraum DT JAEGER DIV 13711: MARCHE, SUEDL HUY, VIERSWT, BARSE, SOHEIT. AOK 18 1 AM.

<details>
<summary>Exact conditional labels</summary>

**Edited output — p183_F, conditional shared square; 115/115 fixed positions:**

```text
ANXAOKX17XZUXDORTX11140XOPXUNTERBRINGUNGSRAUMXDTXJAEGERXDIVX13711XMARCHEXSUEDLXHUYXVIERSWTXBARSEXSOHEITXAOKX18X1XAM
```

</details>


## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p183 excerpt](../../experiments/jaeger_accommodation_area/sources/p183_reviewed.png) · [Inputs](../../experiments/jaeger_accommodation_area/inputs.json) · [Position and change certificates](../../experiments/jaeger_accommodation_area/certificates.json)

The published `Nov10-12` key is unchanged. [Original OCR records](../../experiments/jaeger_accommodation_area/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/jaeger_accommodation_area/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p183 F](#p183-f) | 230 | 110 / 115 | 1 | 2 |

## p183 F

**Source transcription — header:** `F) -- v -- (14.05 p.m., November 12th); 12.10; RICHI-230`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ANXAOKX1?XZUXDORTX11140XOPXUNTERBRINGUNGSRAUMXDTXJAEGE1XDIVX13?11XMARC?EXSUEDL?HUYXVIERSWTXBARSEXSOHEITXAOKX1?X1XAM
```

**Edited output — 1 observed-coordinate substitution and 2 source-mask fills; no insertion, deletion or reordering:**

```text
ANXAOKX1?XZUXDORTX11140XOPXUNTERBRINGUNGSRAUMXDTXJAEGERXDIVX13?11XMARCHEXSUEDLXHUYXVIERSWTXBARSEXSOHEITXAOKX1?X1XAM
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> An AOK 1?. Zu dort 11140 OP. Unterbringungsraum DT JAEGER DIV 13?11: MARCHE, SUEDL HUY, VIERSWT, BARSE, SOHEIT. AOK 1? 1 AM.

**Meaning of this earlier layer:** The message reports an accommodation area for a German Jaeger division, followed by a partially unresolved label and a list of place-like fields. SUEDL HUY means south of Huy. This layer preserves VIERSWT, BARSE and the three unresolved numeral positions; the place-name correction and shared digits are presented separately above.

**Editorial limits.**

- The native body has all 230 printed slots, including two printed dashes in XF--F. No source coordinate is inserted, excluded or reordered.
- The single observed-coordinate proposal JAEGE1 to JAEGER is priced. The two dash fills propose MARC?E to MARCHE and SUEDL?HUY to SUEDLXHUY. These supply readable words and a separator without changing the key.
- VIERSWT and SOHEIT remain literal in this earlier layer. The Vierset proposal above carries its additional substitution explicitly.
- The unknown at plaintext index 8 in the opening AOK1? and at 62 in 13?11 comes from the same fully observed GF square cell. Those two occurrences must take the same digit from {5,6,7,8,9}.
- The final AOK1? unknown at plaintext index 109 is a different fully observed XG square cell and must take a different member of {5,6,7,8,9}. No choice is made merely to make the two AOK labels agree.
- The header retains the literal 14.05 p.m. and 12.10. Neither is used to resolve the date-like or reference labels inside the body.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/jaeger_accommodation_area/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.

</details>
<!-- CASE-EDITION:END -->
