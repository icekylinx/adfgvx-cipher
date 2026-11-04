# Black Sea shipping and supply traffic, 15 November 1918

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

This edition provides exact source readings for two separate multipart messages from Childs pp199–200:
a three-part report in the Feigenhaus/Herkules supply correspondence, and a
two-part order concerning the sale of `CORCOWADO` to Turkey. The source's
wording, frame defects and unknown references remain separate from readable
editorial candidates.

**Prior body credit:** Lasry, Niebel, Kopal and Wacker already identified and
discussed the p199 A supply-message body in their 2016 paper, §6.5, *A Code
within a Code* (author PDF page 25, printed p24; DOI
[10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461)).
For those three records, the present contribution is the literal source
edition, exact deletion/gap alternatives and repair certificates. It is not
a first historical body decipherment. Their prose gives an amount of roughly
ten tons; the conservative source model here retains `1?0` and does not
import that quantity. Full publication metadata are in `inputs.json`.

| Record | Printed slots | Valid coordinates | Declared frame | Fixed raw positions | Conservative candidate |
| --- | ---: | ---: | ---: | ---: | ---: |
| p199 A1 | 293 | 293 | 292 | 145 / 146 | 145 / 146 |
| p199 A2 | 344 | 344 | 344 | 171 / 172 | 172 / 172 |
| p199 A3 | 205 | 203 | 206 | 100 / 103 | 102 / 103 |
| p200 B1 | 394 | 393 | 394 | 195 / 197 | 197 / 197 |
| p200 B2 | 360 | 358 | 360 | 174 / 180 | 176 / 180 |
| **Total** | **1,596** | **1,591** | **1,596** | **785 / 798** | **792 / 798** |

The raw counts use the declared source-frame models before any erasure is
filled or observed coordinate repaired. They include known garbled letters.
No published square or numerical label is changed.

## Source repairs with their limits

**p199 A1 has a surplus coordinate.** Its tenth group is `XAXADV`, six letters,
and the full source has 293 letters against `RICHI-292`. An exhaustive
deletion screen masks names, the unexplained `LEBER` segment and the quantity.
The broad screen has three tied minima, at indices 50, 51 and 52. Requiring
the extra coordinate to lie inside the visibly long group leaves index 50
alone. All three broader fits are retained. The readable candidate then
changes three observed coordinates to repair `ZWOEZFTEN` and `KAKAUPULSER`.

**p199 A3 has a missing coordinate, but no unique gap is claimed.** The group
`VAYA` has only four slots, one of them an invalid `Y`. The next group begins
with an unresolved overstrike, recorded as `?`. All 206 possible one-coordinate
insertions are tested with the entire numeric footer masked. Five positions,
164–168, fit the ordinary body with zero observed-coordinate changes. Each
can be filled to the same 92-character prefix through `ADMIRALSTAB`. The
certificate preserves all five raw footers and their distinct source maps.
Gap 165 is only the representative used for the main displayed raw reading.

The other three records have the advertised length. Their source invalid
glyphs, unreadable marks and exact repair coordinates are retained in the
inputs and certificates. The p200 B2 words `KNN`, `GEMCHT` and `TUEKEI` are
literal received omissions; no plaintext insertion normalizes them.

## Conditional key inventory

The separate Tydelski-based `Nov13-15b FX=Y` hypothesis is checked against all
five source models, six explicit editorial candidates, every other tied
geometry model, and the alternate p199 A3 body candidates: **21 variants**.
It fixes **zero new raw letters** in this edition. Every changed marginal
domain and every unchanged raw text remains visible. No record here uses
the `Nov13-15a DG` transfer layer.

## Readings and reproduction

See the [case study](../../cases/pages/199.md#edition-cases-naval-black-sea-shipping) for complete raw
texts and their meanings. `inputs.json` has the literal source rows, headers,
crop positions and explicitly declared editorial candidates.
`certificates.json` gives all source indices, domains, geometric alternatives
and repair operations. The existing
[p120/p123 case](../../cases/pages/120.md#edition-cases-naval-p120-p123) is related correspondence,
not a duplicate of the new p199 message.

```bash
python experiments/black_sea_shipping/verify.py --verify
python experiments/black_sea_shipping/verify.py --verify --pdf /path/to/ADFGVX.pdf
```

Verification independently recomputes the transposition indices, all plaintext
domains, all geometry minima and every repaired ciphertext. Full plaintext
re-encryption is reported only for candidates without unresolved symbols.
The PDF option also verifies the full source hash and every saved crop pixel.
