# Optional footer fields in p116 A13

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source comparison and review: icekylinx and GPT-6 Astra Pro.**

Original fields in two other telegrams support the optional footer
`XKXMXRMX1XA` at positions 91–102, end exclusive. Added to the unchanged
[90-position approval proposal](APPROVAL.md), it gives **97/111 fixed
positions with zero observed substitutions**. All seven new labels retain
an observed half-coordinate; the proposal fills one printed mask and six
lost-tail slots.

| Original donor | Raw span, zero based | Original field | Proposed target start |
|---|---:|---|---:|
| [p164 D](../../cases/radio/p164_acknowledgment.md) | 41–50 | `XKXMXRMX1` | 91 |
| [p105 C1](../../cases/radio/nov2_telegram_acknowledgments.md) | 77–84 | `XRMX1XA` | 95 |

Both donor fields consist entirely of original observed pairs. Their common
`XRMX1` permits the joined eleven-position proposal, which has fifteen
observed target coordinates. This is a contextual reuse of a field format,
not a repeated reception or a transfer of encrypted coordinates. The p105
donor uses the same November 1–3 key as the target, including the literal `1`.
The p164 donor has a different period key; both completions of its unfilled
5/6 cells reproduce the same original body and donor field.

**Edited output — optional footer; 97/111 positions, 12 printed-mask fills and 49 lost-tail fills:**

```text
TEILENDERX???ARMEEDENMARSCHDURCHUNGARNAUFOBERSCHLESIENANZUTRETEN?EINVERSTAENDNIS?ERBETEN???XKXMXRMX1XA?1G?????X
```

The added positions are 93, 94, 95, 96, 98, 99 and 100. The wholly missing
preceding position 90 remains unknown; no `O` is supplied to turn `K M` into
`O K M`. Position 102 also stays unknown: its domain `1346AY` excludes `X`.
No historical number, abbreviation expansion or full signature is asserted.

**Separate historical closing proposal.** The published reconstruction in
[Lasry et al., Table 3, row 13, printed p20 / PDF p21](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf#page=21)
ends “(Signed) K.M. I A GR-OP”. This is an English reconstruction partly based
on Childs, not an independent German coordinate witness. It supports testing
`GR?XOPX` at positions 104–111 while leaving the intervening label unknown.
Four further lost-tail fills at positions 105, 107, 108 and 109 fit their
observed halves without a source change. The same-key p105 C1 independently
contains the original observed suffix `OPX` at positions 61–64; this supports
the closing format without identifying the telegrams as copies.

**Edited output — further optional closing; 101/111 positions, 12 printed-mask fills and 53 lost-tail fills:**

```text
TEILENDERX???ARMEEDENMARSCHDURCHUNGARNAUFOBERSCHLESIENANZUTRETEN?EINVERSTAENDNIS?ERBETEN???XKXMXRMX1XA?1GR?XOPX
```

The ten remaining positions are 10, 11, 12, 64, 80, 88, 89, 90, 102 and 106.
The inherited word proposal still contains its two wholly missing letters
at 68 and 87; the eleven new footer/closing labels each have an observed half.
The earlier optional doubled-S spelling is kept separately in its own edition.

The initial search compared 331 raw JSON donor fields with five partial
targets and found no new match of at least twelve characters. Adding 314
distinct raw case displays and lowering the exploratory length threshold to
eight exposed the p164 field. The shorter p105 suffix completes the joined
template; it is not a single long blind corpus match. Exact compatibility
and historical context support these optional proposals without proving
unique original wording.

[The certificate](footer_extension.json) preserves both original donor
streams and every donor pair, the unchanged recipient frame, both fill
ledgers, remaining domains and full reencryption witnesses.

```sh
python experiments/p116_optional_route_fragment/verify_footer.py --verify
```

Historical decipherment: J. Rives Childs and the separately credited 2016
authors. The present contribution is the explicit source-compatible footer
proposal and its coordinate account.
