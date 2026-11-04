# OKM availability through an incompletely identified radio route

The proposed reading addresses OHL and OKM and reports that OKM can be reached via the literal address AOK1? through FXT. The last address character and FXT are not expanded into a unit identity or named station.

**Complete edition by printed page:** [p. 180](../pages/180.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This short native body reports a communication route to OKM. Its readable wording is an explicitly priced proposal, while AOK1? and FXT remain literal. The unresolved address character is a source erasure with both numerical and alphabetic possibilities.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p180 excerpt](../../experiments/okm_radio_route/sources/p180_reviewed.png) · [Inputs](../../experiments/okm_radio_route/inputs.json) · [Position and change certificates](../../experiments/okm_radio_route/certificates.json)

The published `Nov10-12` key is unchanged. [Original OCR records](../../experiments/okm_radio_route/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/okm_radio_route/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p180 C](#p180-c) | 86 | 42 / 43 | 6 | 0 |

## p180 C

**Source transcription — header:** `C) LP-vZON (----- November 11th); 24.00; RIZI-86`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ANOHLXOKMXOKMUEBERAOK1?XSUBCHFXTXEHREACHHAR
```

**Edited output — 6 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
ANOHLXOKMXOKMUEBERAOK1?XDURCHFXTXERREICHBAR
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> An OHL. OKM. OKM ueber AOK1? durch FXT erreichbar.

**Meaning:** The proposed reading addresses OHL and OKM and reports that OKM can be reached via the literal address AOK1? through FXT. The last address character and FXT are not expanded into a unit identity or named station.

**Editorial limits.**

- All 86 occupied source slots are retained in native order. The O-like glyph in FAXOX is masked and remains unfilled.
- SUBCH to DURCH and EHREACHHAR to ERREICHBAR cost six observed-coordinate substitutions in total. The exact raw layer remains available; the familiar wording is not represented as an unedited source reading.
- The unresolved source position in AOK1? has domain {1, 4, A, R, T, U}. It is not necessarily a numerical digit, and the edition does not choose a standard army designation.
- FXT remains a literal routing label. The missing interception-time field and separate printed 24.00 line are retained without chronological normalization.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/okm_radio_route/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.

</details>
<!-- CASE-EDITION:END -->
