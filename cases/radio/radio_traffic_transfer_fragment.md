# A radio-traffic transfer in a surviving second part

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A surviving second part reports that DNZW takes over radio traffic and gives further call-name and place-like fields. The source expressly marks the first part missing. One coordinate correction and three printed-dash fills give a readable proposal, while the leading character and exact identity of several labels remain unresolved.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p226 excerpt](../../experiments/radio_traffic_transfer_fragment/sources/p226_reviewed.png) · [Inputs](../../experiments/radio_traffic_transfer_fragment/inputs.json) · [Position and change certificates](../../experiments/radio_traffic_transfer_fragment/certificates.json)

The published `Nov28-Dec1` key is unchanged. [Original OCR records](../../experiments/radio_traffic_transfer_fragment/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/radio_traffic_transfer_fragment/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p226 A2](#p226-a2) | 186 | 89 / 93 | 1 | 3 |

## p226 A2

**Source transcription — header:** `A) BSL v UKS (10.27 p.m., November 30th); 1700 (11/29); (1st Tl Missing); 2 TL RICHI-186`

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
?DEZGROSSW0RDEINYYDNZWUEBERNIMMTVERKAHRFUEROKMSCHWEREX9RUFZYNATANADOLFUR?UL?YINGRO?SVARDEINYY
```

**Edited output — 1 observed-coordinate substitution and 3 source-mask fills; no insertion, deletion or reordering:**

```text
?DEZGROSSW0RDEINYYDNZWUEBERNIMMTVERKEHRFUEROKMSCHWEREX9RUFZYNATANADOLFURSULAYINGROSSVARDEINYY
```

**Readable German — exact nonseparator labels of the edited output:**

> ?DEZ GROSSW0RDEIN. DNZW uebernimmt Verkehr fuer OKM SCHWEREX9 RUFZ: Natan Adolf Ursula in GROSSVARDEIN.

**Meaning:** The surviving second part states that DNZW takes over communications traffic for OKM, followed by the literal field SCHWEREX9 and RUFZ, then the proposed spoken-name sequence Natan Adolf Ursula and a place-like label. RUFZ may abbreviate Rufzeichen, or call sign. The missing first part and the exact identity of DNZW, the station and the location are not reconstructed.

**Editorial limits.**

- The source explicitly says the first part is missing. This is an edition of the complete native 186-slot second part, not a reconstruction of the missing first part.
- Four printed dashes remain occupied source positions. Three are filled in the proposals UR?UL? to URSULA and GRO?SVARDEIN to GROSSVARDEIN. The initial ? is retained with domain {1, 3, D, I, N, U}.
- The only observed-coordinate word change is VERKAHR to VERKEHR. Natan Adolf Ursula is an explicit source-mask completion proposal, not an independently identified person or station.
- GROSSW0RDEIN keeps the numeral 0 and W in the first place-like field; GROSSVARDEIN keeps V in the second. Neither field is silently normalized to a modern or historical place name.
- The initial ?DEZ is not assigned a particular December date. The interception header and separate 11/29 originating line do not select that character.
- Y is the separator label. X and 9 inside SCHWEREX9 remain literal; DNZW and RUFZ are not expanded in the exact readable quotation.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/radio_traffic_transfer_fragment/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
