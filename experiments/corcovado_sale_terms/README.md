# Corcovado sale terms and the following status report

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

Six independently transcribed source records recover the 9 November sale
terms for Corcovado and a 10 November report that the vessel already had a
Turkish crew. They complement the 15 November order in
[`black_sea_shipping`](../black_sea_shipping/README.md). These are distinct
messages, not duplicate plaintexts.

The full reading, interpretation, residual uncertainty and attribution are
in [the case](../../cases/pages/165.md#edition-cases-naval-corcovado-sale-terms). The source is
J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed
pp165 and 173 (PDF page 168 and 176). All six cropped images are retained
under `sources/`; their coordinates and hashes are in `inputs.json`.

## Source and repair scope

| Record | Printed slots | Valid coordinates | Raw fixed / length | Candidate fixed | Observed changes | Erasure fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| p165 A1 | 380 | 380 | 190/190 | 190 | 2 | 0 |
| p165 A2 | 458 | 456 | 227/229 | 229 | 4 | 2 |
| p165 A3 | 380 | 380 | 190/190 | 190 | 1 | 0 |
| p165 A5 | 500 | 497 | 246/250 | 248 | 3 | 2 |
| p173 A1 | 242 | 242 | 119/121 | 119 | 6 | 0 |
| p173 A2 | 160 | 159 | 79/80 | 80 | 1 | 1 |
| **Total** | **2,120** | **2,114** | **1,051/1,060** | **1,056** | **17** | **5** |

All advertised lengths agree with the literal transcriptions. There are
no inserted, deleted or reordered coordinates. Invalid printed glyphs
remain erasures in the raw decryptions; proposed ordinary-word fills and
substitutions are listed individually in `certificates.json`. Every fixed
count includes any received garbles, so it is not a count of error-free
German letters. The header says `4 TEILE`, but the four source blocks are
labelled `1`, `2`, `3`, `5 TL`; the edition retains **A5** without inventing
a missing block.

## Conditional office-prefix digits

The later p200 B2 message has the complete observed word `SECHS` in
`MARIN?AMTXAXSECHSXS????0`. Its five letters require no source repair or
unknown square cell. The conditional hypothesis is that the related
p165, p173 and p200 Corcovado traffic uses the same Marineamt `A6S`
office/file prefix and that the two earlier prefix pairs are correctly
copied. The reference tails are different and are never equated.

| Key | Conditional assignment | Direct source position | Local physical characters fixed |
| --- | --- | --- | ---: |
| Nov7–9 | `VF=6` | p165 A5 plaintext 239, source 473/98 | 1 |
| Nov7–9 | `XA=5`, by the remaining-symbol constraint | No occurrence in these six records | 0 |
| Nov10–12 | `XX=6` | p173 A1 plaintext 8, source 121/167 | 1 |

Indices are zero-based. The certificate checks all six raw models and all
six repaired candidates, retaining every raw/domain change and every
remaining uncertain position. After ordinary repairs plus this conditional
layer, **1,058/1,060** positions are fixed locally. The two unresolved
reference positions remain p165 A5 position 244 (`?D`, domain `02ACLR`) and
p173 A1 position 10 (`XG`, domain `5789`).

The published partial squares and the earlier complete-square hypotheses
are retained unchanged. In particular, these conditional assignments
conflict with the earlier completed hypotheses `VF=5`, `XA=6` and `XX=9`.
All source-compatible digit alternatives are explicitly enumerated; exact
re-encryption alone cannot choose a numerical label.

The earlier [military-context layer](../p170_continuation/military_context.json)
already supports `VF=6`, `XA=5` through identification of the 6th Reserve
Division. Its consequences were also propagated in
[`withdrawal_recovery`](../withdrawal_recovery/README.md). The Corcovado
prefix supplies independent textual corroboration of those same conditional
Nov7 assignments, not a newly discovered Nov7 cell. The military-identity
assumption and the stable-office-prefix assumption remain separate.
The Nov10 `XX=6` constraint is stated as its own conditional layer.

## Attribution and limits

The transposition orders and known square cells are prior published keys,
credited in `inputs.json`. This contribution is a reproducible source
edition and a separately stated cross-key office-prefix constraint.

A bounded check found no explicit Corcovado body discussion in the checked
Lasry–Niebel–Kopal–Wacker paper, the ADFGVX chapter of Lasry's dissertation,
or the cached 55 comments on the 2017 ScienceBlogs post. This is not a
claim of universal historical priority. The paper's explicit prior body
identification of the separate p199 cargo message is credited in the
shipping package. Source files and hashes for the bounded check are
listed in `inputs.json`.

The directly decrypted price is `10XMILL`; currency is unstated. The
10 November report is not proof of the ship's ultimate disposition. The
source spelling `CORCOVAUO` in p165 is retained in the raw text; its
same-length `CORCOVADO` repair is independently supported by the complete
observed spelling in p173, conditional on the same-vessel association.

## Reproduce

```bash
python experiments/corcovado_sale_terms/verify.py --verify
python experiments/corcovado_sale_terms/verify.py --verify --pdf /path/to/childs.pdf
```

The first command recomputes the independent transposition mapping, raw
plaintext domains, exact repair paths, the direct price and ship-name
witnesses, and every conditional digit effect. It binds the later
`black_sea_shipping/inputs.json` by SHA-256 and rederives the five-letter
`SECHS` witness from its literal source. The second command additionally
checks the full primary PDF hash and rerenders every crop pixel-for-pixel.

## Independent office context

The Bundesarchiv's institutional description of the Reichsmarineamt lists
A VI S as the maritime transport division in 1914 and describes its 1917
organization. This independently supports the office interpretation used
above. The [source note](office_context.json) distinguishes the
retrieved institutional catalogue from the underlying uninspected business
plans. Identifying particular telegram fields with that office and assuming
they were copied correctly remain conditional; no source certificate or
published square is changed.
