# Constantinople addresses, signatures and receipt instructions

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** Three visible first parts, containing addresses, signatures and receipt instructions. Their headings announce two or three parts, but no missing continuation payload is claimed recovered here.

Source edition and verification: **icekylinx and GPT-6 Astra Pro**. The published Nov4–6 and Nov7–9 keys are credited to Lasry, Niebel, Kopal and Wacker and remain unchanged. Earlier unreviewed p147 C/p156 C address-and-signature readings are retained in the prior-work record; those fragments are not presented as newly discovered full message bodies.

## What the visible parts say

- **p147 C1:** To the German Embassy at Pera, with signature `STUMM`. The heading gives `YZ v LP`,08.19 a.m. on 7 November, `FUER YZ1450 (6/11) 2 TEILE`, and `1 TL RICHI-96`.
- **p148 B1:** To the Military Mission at `COSPOLI`, with reference labels, a signature for both parts `I.A. GROENER`, and an instruction for receipt to be acknowledged by an officer. The heading gives 08.40 a.m. on 7 November, `FUER YZ1135 (6/11) 3 TEILE`, and `1 TL RICHI-328`.
- **p156 C1:** German charge d'affaires at Constantinople, with raw signature `BUSSCHS`. The heading gives 06.03 a.m. on 8 November, `FUER YZ2030 (7/11) 2 TLE`, and `1 TL RICHI-102`.

`BUSSCHS` is not silently respelled or expanded to a named historical person. All numerical references remain the published-key labels. The source scan supplies only the first parts represented in this edition.

## Counts and source readings

| Record | Source slots | Raw fixed positions | Edited fixed positions | Observed-coordinate substitutions | Source fills |
|---|---:|---:|---:|---:|---:|
|p147_C1|96|48/48|48/48|0|0|
|p148_B1|328|163/164|163/164|2|0|
|p156_C1|102|51/51|51/51|0|0|

The physical-record total is **526 coordinate slots / 263 plaintext positions**. Raw fixed positions total 262; the edited layer fixes 262.

## p147 C1 — German Embassy at Pera and Stumm signature

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ANXDEUTSCHEBOTSCHAFTXPERAXXUNTERSCHRIFTXXSTUMMXX
```

</details>

## p148 B1 — Military Mission routing, Groener signature and officer receipt acknowledgement

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
ANXMILXMISSIONCOSPOLIXZUXRMX2XDXNRX755XXUNTERSCHRIFTFUERBEIUETLEXXIXAXGROENERXBXRM811193XGEHXPX?ZUSXOPXFUERXKOSPOLIXDOPPELPUNKTXEMPFANGSBESTAETIGUNGDURCHOFFZERBEEEN
```

**Edited output:**

```text
ANXMILXMISSIONCOSPOLIXZUXRMX2XDXNRX755XXUNTERSCHRIFTFUERBEIDETLEXXIXAXGROENERXBXRM811193XGEHXPX?ZUSXOPXFUERXKOSPOLIXDOPPELPUNKTXEMPFANGSBESTAETIGUNGDURCHOFFZERBETEN
```

</details>

## p156 C1 — German charge d’affaires at Constantinople and raw BUSSCHS signature

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DEUTSCHERGESCHAEFTSTRAEGERKONSTANTINOPELXXBUSSCHSXX
```

</details>

## The p148 source annotation and invalid glyph

The source visibly places an X above the F at coordinate 37. Applying that annotation produces the T in `ERBETEN`. The edition counts it as **one observed-coordinate substitution**, not zero-cost transcription. A separate ordinary-word repair changes `BEIUETLE` to `BEIDETLE` at coordinate 122; that also costs one observed substitution.

Coordinate 49 is printed as an L-shaped glyph outside the ADFGVX alphabet. It remains a source mask. The affected plaintext position 95 has exact domain **9EKVXZ**, so the reference is retained as `GEHXPX?ZUSXOP`. The edition does not infer a desired coordinate from that unclear field.

p147 C1 and p156 C1 need no source edits. None of these records has a coordinate insertion, deletion, reordering or key change, and none establishes the substance of its unlinked continuation parts.

## Evidence and reproduction

[The input record](../../experiments/constantinople_address_parts/inputs.json) preserves all manual rows, literal irregular glyphs, source headers and crop-rendering metadata. [The certificate](../../experiments/constantinople_address_parts/certificates.json) retains all coordinate changes, masks, symbol domains, digit/J/Q/Y labels and round trips. Global witnesses demonstrate consistency only; they do not recover a unique original.

[The README](../../experiments/constantinople_address_parts/README.md) provides portable verifier commands, including exact source-crop pixel regeneration from the pinned full scan. Prior candidates and specific earlier source editions are distinguished; the bounded literature check is not a universal priority claim.
