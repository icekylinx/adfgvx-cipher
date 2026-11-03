# An instruction to avoid fighting, with further orders to follow

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A fully preserved native ciphertext directs that fighting be avoided and states that further instructions will follow. Four coordinate substitutions supply two word proposals; every abbreviated authority, demand and closing reference label stays visible. The account distinguishes the order from evidence that it was carried out.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p227 excerpt](../../experiments/avoid_fighting_instruction/sources/p227_reviewed.png) · [Inputs](../../experiments/avoid_fighting_instruction/inputs.json) · [Position and change certificates](../../experiments/avoid_fighting_instruction/certificates.json)

The published `Nov28-Dec1` key is unchanged. [Original OCR records](../../experiments/avoid_fighting_instruction/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/avoid_fighting_instruction/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p227 D](#p227-d) | 272 | 136 / 136 | 4 | 0 |

## p227 D

**Source transcription — header:** `D) UKS v BSL (09.29 a.m., November 28th); KR 0912 (11/28); RICHI-272`

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
OKMYAUFBEFEHLDERREICHSLEITGYIST1EDERKAMPFZTVERMEIDENYEINGEHENAUFFRANZYFORDERUNGENNOTWENDIGYWEITEREBEFEHLEFOLGENYYOHLXAXX280GEHYOPJANGYYY
```

**Edited output — 4 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
OKMYAUFBEFEHLDERREICHSLEITGYISTJEDERKAMPFZUVERMEIDENYEINGEHENAUFFRANZYFORDERUNGENNOTWENDIGYWEITEREBEFEHLEFOLGENYYOHLXAXX280GEHYOPJANGYYY
```

**Readable German — exact nonseparator labels of the edited output:**

> OKM. Auf Befehl der REICHSLEITG ist jeder Kampf zu vermeiden. Eingehen auf FRANZ Forderungen notwendig. Weitere Befehle folgen. OHLXAXX280GEH. OPJANG.

**Meaning:** The message instructs OKM, on the order of the authority labeled REICHSLEITG, to avoid any fighting, says compliance with demands labeled FRANZ is necessary, and promises further orders. FRANZ is read as an abbreviation for French in this context; the source does not spell that word out. The message records an instruction, not proof that fighting stopped or that the demands were fulfilled.

**Editorial limits.**

- All 272 printed coordinates are present and legible, with no source erasures. The source photograph includes a complete group absent from the earlier OCR; restoring that visible group is a transcription correction, not an inserted historical coordinate.
- The high-resolution source reads FFFVD, including the third F with its middle bar. It is not treated as an invented missing coordinate or a T-shaped source mask.
- The wording proposals 1EDER to JEDER and ZT to ZU cost four observed-coordinate substitutions in total. REICHSLEITG and FRANZ remain abbreviated.
- Y is the separator in this period key. The closing OHLXAXX280GEH and OPJANG are preserved literally; 280 is not turned into a calendar date or a reference number with an inferred format.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/avoid_fighting_instruction/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
