# Urgent shipping capacity and probable reliance on sea transport

The surviving second part urgently requests shipping capacity for personnel and horses. The paired capacity labels are repeated in the source.

**Complete edition by printed page:** [p. 218](../pages/218.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The surviving second and third parts request urgent shipping capacity and say that all troops will probably need sea transport. The source explicitly marks the first part missing. Repeated capacity labels, differing command fields and the unresolved source-mask position remain literal.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p218 excerpt](../../experiments/urgent_shipping_space/sources/p218_reviewed.png) · [Inputs](../../experiments/urgent_shipping_space/inputs.json) · [Position and change certificates](../../experiments/urgent_shipping_space/certificates.json)

The published `Nov25-28` key is unchanged. [Original OCR records](../../experiments/urgent_shipping_space/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/urgent_shipping_space/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p218 B2](#p218-b2) | 188 | 94 / 94 | 1 | 0 |
| [p218 B3](#p218-b3) | 200 | 99 / 100 | 0 | 0 |

## p218 B2

**Source transcription — header:** `B) KOW v RVA (01.36 a.m., November 26th); KR AN LP 2100 (11/25) 3 TLE; (1 TL missing); 2 TL RICHI-188`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
SOFORTIGESEGDUNGVONSCHIFFSRAUMFUERJ3YYYMANN3YYYPFERDEXJ3YYYMANN3YYYPFERDEXRTVLDRINGENDGEBOTENX
```

**Edited output — 1 observed-coordinate substitution and 0 source-mask fills; no insertion, deletion or reordering:**

```text
SOFORTIGESENDUNGVONSCHIFFSRAUMFUERJ3YYYMANN3YYYPFERDEXJ3YYYMANN3YYYPFERDEXRTVLDRINGENDGEBOTENX
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Sofortige Sendung von Schiffsraum fuer J3YYY Mann 3YYY Pferde. J3YYY Mann 3YYY Pferde. RTVL dringend geboten.

**Meaning:** The surviving second part urgently requests shipping capacity for personnel and horses. The paired capacity labels are repeated in the source. J3YYY, 3YYY and RTVL remain literal; no numerical total or port identification is imposed.

**Editorial limits.**

- The source explicitly says “1 TL missing.” This edition starts with the complete native 188-coordinate second part and supplies no missing first body.
- SEGDUNG to SENDUNG is one observed-coordinate substitution. All source coordinates remain in native order.
- Both repetitions of J3YYY MANN 3YYY PFERDE remain in the exact stream and readable passage. They are not silently converted to familiar decimal numbers or counted as separate telegrams.
- RTVL is not expanded into a named port or headquarters. The printed interception date November 26 and originating line 11/25 remain separate.

## p218 B3

**Source transcription — header:** `B) KOW v RVA (01.36 a.m., November 26th); KR AN LP 2100 (11/25) 3 TLE; 3 TL RICHI-200`

<details>
<summary>Raw decoded text</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
DAWAHRSCHEINLICHALLETRUPPENAUFSEETRANSPORTANGEWIESENXGENXKDOX?XBXVX72XGENXKDOXZXBXNX72XJAXNR42XJ2GEH
```

</details>

**Readable German — exact nonseparator labels of the unchanged raw output:**

> Da wahrscheinlich alle Truppen auf Seetransport angewiesen. Gen. Kdo. ? B V 72. Gen. Kdo. Z B N 72. JAXNR42XJ2GEH.

**Meaning:** The third part explains that all troops will probably depend on sea transport. Its command and reference fields remain literal. This is a stated expectation and an urgent request for capacity, not proof that ships were supplied or the troops transported.

**Editorial limits.**

- The native 200-coordinate body contains one printed dash in -AGXG. It remains masked and unfilled; no observed coordinate changes.
- The remaining source-mask position has domain {3, D, F, M, T, X}. A familiar abbreviation is not forced into that field.
- The two command fields retain their different V and N labels, the repeated 72, and the complete footer JAXNR42XJ2GEH. No historical unit identity or numbered reference is inferred.

## Meaning without converting the labels

The request concerns transport capacity for men and horses, and the following explanation expects general reliance on sea transport. It does not establish that transport was supplied. Both repetitions of `J3YYY MANN 3YYY PFERDE` are retained. A familiar-looking decimal conversion is not silently applied to the J/Y labels, and RTVL is not expanded to a particular port.

The third-part unknown is a printed source erasure under an otherwise fixed square, with domain `{3, D, F, M, T, X}`. The second command field retains N where the first has V. Both details remain visible rather than being normalized to a standard command abbreviation.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/urgent_shipping_space/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.

</details>
<!-- CASE-EDITION:END -->
