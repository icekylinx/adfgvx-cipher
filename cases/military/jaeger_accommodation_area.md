# An accommodation-area report with unresolved army and place labels

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This native message reports an accommodation area for a German Jaeger division. Its readable proposal repairs one word and fills two printed dashes; the route-like spellings and three globally coupled digit positions remain literal or unresolved. The complete source body matches its advertised 230 slots, with no change to its frame.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p183 excerpt](../../experiments/jaeger_accommodation_area/sources/p183_reviewed.png) · [Inputs](../../experiments/jaeger_accommodation_area/inputs.json) · [Position and change certificates](../../experiments/jaeger_accommodation_area/certificates.json)

The published `Nov10-12` key is unchanged. [Original OCR records](../../experiments/jaeger_accommodation_area/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/jaeger_accommodation_area/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p183 F](#p183-f) | 230 | 110 / 115 | 1 | 2 |

## p183 F

**Source transcription — header:** `F) -- v -- (14.05 p.m., November 12th); 12.10; RICHI-230`

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ANXAOKX1?XZUXDORTX11140XOPXUNTERBRINGUNGSRAUMXDTXJAEGE1XDIVX13?11XMARC?EXSUEDL?HUYXVIERSWTXBARSEXSOHEITXAOKX1?X1XAM
```

**Edited output — 1 observed-coordinate substitution and 2 source-mask fills; no insertion, deletion or reordering:**

```text
ANXAOKX1?XZUXDORTX11140XOPXUNTERBRINGUNGSRAUMXDTXJAEGERXDIVX13?11XMARCHEXSUEDLXHUYXVIERSWTXBARSEXSOHEITXAOKX1?X1XAM
```

**Readable German — exact nonseparator labels of the edited output:**

> An AOK 1?. Zu dort 11140 OP. Unterbringungsraum DT JAEGER DIV 13?11: MARCHE, SUEDL HUY, VIERSWT, BARSE, SOHEIT. AOK 1? 1 AM.

**Meaning:** The message reports an accommodation area for a German Jaeger division, followed by a partially unresolved label and a list of place-like fields. SUEDL HUY is read as south of HUY; the exact referents of MARCHE, VIERSWT, BARSE and SOHEIT are not established independently here. Both AOK fields and the 13?11 label remain unresolved, so the edition does not identify an army or date from those labels.

**Editorial limits.**

- The native body has all 230 printed slots, including two printed dashes in XF--F. No source coordinate is inserted, excluded or reordered.
- The single observed-coordinate proposal JAEGE1 to JAEGER is priced. The two dash fills propose MARC?E to MARCHE and SUEDL?HUY to SUEDLXHUY. These supply readable words and a separator without changing the key.
- VIERSWT and SOHEIT remain literal source spellings. A possible familiar place name is not used to repair them for free.
- The unknown at plaintext index 8 in the opening AOK1? and at 62 in 13?11 comes from the same fully observed GF square cell. Those two occurrences must take the same digit from {5,6,7,8,9}.
- The final AOK1? unknown at plaintext index 109 is a different fully observed XG square cell and must take a different member of {5,6,7,8,9}. No choice is made merely to make the two AOK labels agree.
- The header retains the literal 14.05 p.m. and 12.10. Neither is used to resolve the date-like or reference labels inside the body.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/jaeger_accommodation_area/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
