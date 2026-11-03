# An airfield and German troops: the surviving third part on p154

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A native third-part fragment reports an apparent airfield and German troops providing security along a named line. The exact text, three occupied source masks and two proposed coordinate corrections are retained; preceding parts and the geographical referents are not supplied from context.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p154 excerpt](../../experiments/airfield_german_troop_fragment/sources/p154_reviewed.png) · [Inputs](../../experiments/airfield_german_troop_fragment/inputs.json) · [Position and change certificates](../../experiments/airfield_german_troop_fragment/certificates.json)

The published `Nov4-6` key is unchanged. [Original OCR records](../../experiments/airfield_german_troop_fragment/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/airfield_german_troop_fragment/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p154 B3](#p154-b3) | 172 | 83 / 86 | 2 | 3 |

## p154 B3

**Source transcription — header:** `B) ZON v UKS (10.04 p.m., November 7th); 3 TL RICHI-172`

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
ANSCHEINENDDORT?LUGPLATZXXX2XINLINIEXMIROCXBR?APALANKA?SICHERNNURNOCHDEUTSCHETRUPPELXX
```

**Edited output — 2 observed-coordinate substitutions and 3 source-mask fills; no insertion, deletion or reordering:**

```text
ANSCHEINENDDORTFLUGPLATZXXX2XINLINIEXMIROCXBRZAPALANKAXSICHERNNURNOCHDEUTSCHETRUPPENXX
```

**Readable German — exact nonseparator labels of the edited output:**

> Anscheinend dort Flugplatz. 2. In Linie MIROC BRZAPALANKA sichern nur noch deutsche Truppen.

**Meaning:** This surviving third part says there apparently is an airfield at the previously mentioned place. Its next item says that only German troops still provide security along the line designated MIROC and the proposed BRZAPALANKA label. The earlier place reference and precise geographical identification are not supplied.

**Editorial limits.**

- The printed body is explicitly 3 TL and has exactly its advertised 172 occupied slots. This edition identifies no preceding first or second part and does not join the fragment to a different report by geographical resemblance.
- The source has ADX-F and DXU-X: two printed dashes and a U-like non-coordinate glyph occupy three slots. All three are masked in the raw layer and filled explicitly.
- The BR?APALANKA proposal is not a free fill: the raw pair G? has domain {0, 3, 6, O, Q, Y}, which excludes Z. BRZAPALANKA additionally requires source 107 G→F, together with the source-glyph fill. The place spelling remains an editorial proposal.
- TRUPPEL to TRUPPEN is the other observed-coordinate substitution. The item label 2 and MIROC remain literal.
- The Nov4–6 key is unchanged. Its successful decryption does not alter the printed November 7 header or establish the original drafting date.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/airfield_german_troop_fragment/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
