# An instruction to avoid fighting, with further orders to follow

The message instructs OKM, on the order of the authority labeled REICHSLEITG, to avoid any fighting, says compliance with demands labeled FRANZ is necessary, and promises further orders. FRANZ is read as an abbreviation for French in this context; the source does not spell that word out.

**Complete edition by printed page:** [p. 227](../pages/227.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

An instruction to OKM requires avoidance of all fighting, compliance with demands abbreviated FRANZ, and attention to further orders. A joint reading with p225 recovers JEDER from its original coordinate pair. Only the word repair ZT to ZU remains, reducing the cost from four observed-coordinate substitutions to two.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p227 excerpt](../../experiments/avoid_fighting_instruction/sources/p227_reviewed.png) · [Inputs](../../experiments/avoid_fighting_instruction/inputs.json) · [Position and change certificates](../../experiments/avoid_fighting_instruction/certificates.json)

The published `Nov28-Dec1` key is unchanged. [Original OCR records](../../experiments/avoid_fighting_instruction/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/avoid_fighting_instruction/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p227 D](#p227-d) | 272 | 136 / 136 | 4; **2 with shared J** | 0 |

## p227 D

**Source transcription — header:** `D) UKS v BSL (09.29 a.m., November 28th); KR 0912 (11/28); RICHI-272`

**Conditional interpretation — shared FA=J, with the two-coordinate ZT to ZU repair:**

> OKM. Auf Befehl der REICHSLEITG ist jeder Kampf zu vermeiden. Eingehen
> auf FRANZ Forderungen notwendig. Weitere Befehle folgen.
> OHL1A1136?GEH. OP2ANG.

The J at plaintext position 31 comes from the complete observed pair `FA`
at source positions 3 and 105. [p225 B2](regimental_journey_report.md#p225-b2)
provides a second native instance in `JEDE UNTERSTUETZUNG`.
The shared letter interpretation fixes **135/136 positions** in this message,
leaving the reference `1136?`; `FRANZ` remains abbreviated.
It extends the existing Nov28–Dec1 interpretation, including its historical
numeral assumptions. [Joint evidence and 24 square witnesses](../../experiments/late_november_joint_completion/README.md).

The subsequent [calendar and unit comparison](../../experiments/late_november_calendar_and_units/README.md)
also fixes the original `VG` pair in the reference as `7`:

| Field | After the shared J | After the unit interpretation |
|---|---|---|
| OHL reference | `1136?` | **11367** |

The conditional reading now fixes **136/136 positions**. Its two-coordinate
`ZT→ZU` repair is unchanged.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
OKMYAUFBEFEHLDERREICHSLEITGYIST1EDERKAMPFZTVERMEIDENYEINGEHENAUFFRANZYFORDERUNGENNOTWENDIGYWEITEREBEFEHLEFOLGENYYOHLXAXX280GEHYOPJANGYYY
```

**Edited output — earlier unchanged-key wording; 4 observed-coordinate substitutions:**

```text
OKMYAUFBEFEHLDERREICHSLEITGYISTJEDERKAMPFZUVERMEIDENYEINGEHENAUFFRANZYFORDERUNGENNOTWENDIGYWEITEREBEFEHLEFOLGENYYOHLXAXX280GEHYOPJANGYYY
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> OKM. Auf Befehl der REICHSLEITG ist jeder Kampf zu vermeiden. Eingehen auf FRANZ Forderungen notwendig. Weitere Befehle folgen. OHLXAXX280GEH. OPJANG.

**Meaning:** The message instructs OKM, on the order of the authority labeled REICHSLEITG, to avoid any fighting, says compliance with demands labeled FRANZ is necessary, and promises further orders. FRANZ is read as an abbreviation for French in this context; the source does not spell that word out. The message records an instruction, not proof that fighting stopped or that the demands were fulfilled.

**Editorial limits.**

- All 272 printed coordinates are present and legible, with no source erasures. The source photograph includes a complete group absent from the earlier OCR; restoring that visible group is a transcription correction, not an inserted historical coordinate.
- The high-resolution source reads FFFVD, including the third F with its middle bar. It is not treated as an invented missing coordinate or a T-shaped source mask.
- Under the published square, 1EDER to JEDER and ZT to ZU cost four substitutions. The shared FA=J interpretation removes the two J repairs; ZT to ZU still costs two. REICHSLEITG and FRANZ remain abbreviated.
- Y is the separator in this period key. The closing OHLXAXX280GEH and OPJANG are preserved literally; 280 is not turned into a calendar date or a reference number with an inferred format.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce the source edition with `python experiments/avoid_fighting_instruction/verify.py --verify` and the joint extension with `python experiments/late_november_joint_completion/verify.py --verify`. The source verifier accepts `--pdf /path/to/adfgvx-childs.pdf` for the original PDF and exact crop pixels.

</details>
<!-- CASE-EDITION:END -->
