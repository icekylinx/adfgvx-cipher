# November 8 radio-key instructions, apparatus prices and reports

Prepared by **icekylinx and GPT-6 Astra Pro**. The published Nov7–9 key
and earlier OCR candidate work retain their existing credits.

Seven physical source parts on Childs pp.160–161 (PDF pp.163–164) are
transcribed from the page images. The unchanged 34-cell period square
is used throughout. This is a source edition and constraint audit;
these seven physical parts are not presented as seven first decipherments.

## Source and cost accounting

| Source part | Source slots / valid | Model slots | Fixed raw → edited | Observed substitutions | Printed-mask fills | Observed exclusions |
|---|---:|---:|---:|---:|---:|---:|
| p160_A2 | 240 / 239 | 238 | 117 → 118 | 4 | 1 | 2 |
| p160_B1 | 282 / 282 | 282 | 140 → 140 | 1 | 0 | 0 |
| p160_B2 | 84 / 82 | 84 | 39 → 40 | 0 | 1 | 0 |
| p160_C1 | 309 / 307 | 308 | 152 → 154 | 4 | 2 | 1 |
| p160_C2 | 144 / 144 | 144 | 71 → 71 | 0 | 0 | 0 |
| p160_D1 | 140 / 135 | 140 | 62 → 67 | 2 | 5 | 0 |
| p161_A2 | 128 / 126 | 128 | 62 → 64 | 0 | 2 | 0 |

Together: **1,327 source slots**, **1,315 valid observed coordinates**,
**1,324 model slots**, and **662 plaintext positions**. The primary
frames fix 643 positions before editorial changes and 654 afterward.
There are 11 observed substitutions, 11 printed-mask fills and 3 observed
exclusions; no coordinates are inserted and no published key is changed.
The source totals include twelve visible noncoordinate characters:
eight dashes and four invalid printed letter glyphs. Eleven are filled;
the B2 source 83 glyph remains unresolved.

## Conditional framing and exhaustive fixed-template prices

The A2 source really contains 240 slots despite its printed 238 length.
Its first row has two six-character groups, `GDGDXF` and `DXAADG`,
at source 15–20 and 26–31. The selected conditional frame excludes
source 18 (`D`) and 26 (`D`). The verifier prices **all 28,680 unordered
pairs of excluded source positions**, including masks, against the
same 119-position edited template. This choice is the sole minimum at
four observed substitutions; its two observed exclusions are additional
operations. The complete 36 source-local combinations and the full
substitution-cost histogram are retained. The competing local 26→27
choice changes the native name-like token `UJVERBASZ` to `UZVERBASZ`.
The source-only comparison below retains both maps as equal minima; the
supplied edited template, which chooses `UJVERBASZ`, selects one of them.

C1 has 309 source slots against printed 308. The six-character group
`FAGVGD` occupies source 280–285. Excluding its source 281 `A` gives
the primary 308-coordinate frame. All 309 single exclusions are priced
against the same 154-position template. Source 281 is the sole minimum
at four observed substitutions, with one observed exclusion and two
printed-mask fills accounted separately. All six local group choices
are retained.

These are **retrospective fixed-template comparisons**. They establish
neither a blind unique plaintext nor the historical cause of the extra
source characters. Unaltered 240- and 309-slot diagnostics are preserved;
the odd 309-slot diagnostic retains its final unpaired interim coordinate.
The A2 first part of this physical transmission has not been identified.

## Coupled missing key labels

The missing square cells `VF` and `XA` jointly contain the two unused
labels `5` and `6`. The verifier checks both whole-square completions,
without choosing one as historical fact. Every repeated occurrence of
one cell uses the same assigned digit. Question marks in different
positions are therefore not independent digit selections.

Each primary reading has two full-key compatibility witnesses except B2,
which also has one unfilled source coordinate and therefore twelve
binding-and-fill witnesses. All complete witnesses round-trip exactly.
Their per-position unions equal the partial-key domains, including B2's
mixed letter/digit domain. The older published full-square hypothesis
remains part of its prior key provenance; it is not a new deduction here.

## Display and historical limits

The [reading conventions](../../docs/reading-conventions.md) apply.
Raw output uses the stated native or conditional frame. Edited output
has an explicit source-offset ledger. Readable German is checked against
all nonseparator labels of the edited output: spacing, case, punctuation
and German umlaut notation may change; letters, numbers and unresolved
positions may not. No abbreviation is expanded in that layer.

- The Ringbahn message says to keep November key material, postpone the
  December change, and use the listed November/December day relationship.
  It gives instructions, not newly recovered secret key contents.
- The sale message keeps `21?00`, `380L`, `170M`, shortened words and
  reference fields literally. The 80–90 percent estimate is the actual
  following part, not an amount inferred from the first part.
- The movement report leaves `NAGYBESKEREK` and `WERGCHEEZ` as decoded.
  The personnel report leaves `LI`, `TSCHENKE`, `AWALOFF` and `STUMM`
  without added identity claims.
- The cleartext footer `ZON` follows A2; `NF NKJ v LP UM` follows C2.
  Neither footer is encrypted input or part of the plaintext counts.

## Independent and parallel checks

The [independent audit](independent_source_audit.json) uses its own cipher
implementation and embedded image-reviewed rows. It agrees on all seven
source transcripts, 28,989 exhaustive exclusion comparisons, costs and full
witnesses. It also enumerates the **12 global completions across all seven
records**: two shared 5/6 assignments times six values of B2's unfilled
source 83 coordinate. The ordinary script's per-record witness lists are not
independent digit assignments between messages.

The [parallel audit](parallel_witnesses.json) binds seven source/key files
and eleven source-image digests. It checks p160 A2 against the earlier p170 B2
source. All **28,680 two-exclusion maps** are independently priced against
the untouched p170 coordinates, without a plaintext template or language
score. Exactly `[18,26]` and `[18,27]` minimize observed disagreements;
both give **231 agreements, five disagreements and two complementary masks**.
Both retain literal source19 `X` and source199 `V`, reading `D` at plaintext67
in `RD` without substitution. The previous `[19,26]` frame gave `RE` and
six disagreements. This source constraint improves the primary frame.

The two best maps give `UJVERBASZ` and `UZVERBASZ`. Their p170 counterpart
is masked, so neither the source alignment nor the copy establishes `J`;
the displayed `UJVERBASZ` branch remains conditional. Each map fixes 117 raw
positions, with 116 common fixed labels across both. The p160 printed dash
in `BEREITGESTELLT` is filled from the same p170 coordinate under either map.
The optional `WERSCHETZ` reading costs two extra observed substitutions,
six total instead of seven under the old frame. The five remaining source
disagreements and the shared `ABTRFNSPORT` error stay explicit. The independent
audit checks the source-only minimum and both paths using a separate dynamic
program, in addition to its fixed-template enumerations. Related p166/p167
context and the earlier p211 key-use edition retain their identities and
credits. Since p211 uses a different published key, that branch compares
plaintext wording only, with no cross-key coordinate match or digit fill.

## Reproduce

```sh
python experiments/nov8_radio_keys_and_reports/verify.py --verify
python experiments/nov8_radio_keys_and_reports/independent_source_audit.py --verify
python experiments/nov8_radio_keys_and_reports/parallel_witnesses.py --verify
python experiments/nov8_radio_keys_and_reports/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The main verifier rechecks literal rows, every primary frame, all costs,
all complete compatibility witnesses, both exhaustive exclusion tables,
exact readable mappings and source image hashes. The PDF invocation additionally
rerenders all seven frozen source images from the SHA256-pinned original
PDF and compares pixel bytes. It does not download the PDF or any model.
The independent source/candidate audit is recorded separately.

[Inputs](inputs.json), [certificates](certificates.json),
[readable mappings](readable_mapping.json),
[earlier OCR context](prior_candidates.json),
and [catalogue proposal](catalog_proposal.json) preserve distinct layers.
