# 1 November Mackensen and Orient reports

Prepared by **icekylinx and GPT-6 Astra Pro**. This package edits eight
physical source records on Childs pp100–102 with the published full `Nov1-3`
key. The reader pages cover [Eleventh Army subordination](../../pages/100.md#edition-cases-military-mackensen-subordination)
and [parallel Orient reports](../../pages/101.md#edition-cases-military-orient-south-slav-reports).
The existing p100 A challenge is a separate record and is unchanged.

## Completed source editions

| Record | Source slots / valid coordinates | Working slots | Raw fixed / total | Edited fixed / total | Observed substitutions | Source-mask fills | Observed exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p100 D1 | 136 / 134 | 136 | 66 / 68 | 68 / 68 | 0 | 2 | 0 |
| p101 A2 | 132 / 132 | 132 | 66 / 66 | 66 / 66 | 1 | 0 | 0 |
| p101 B2 | 200 / 199 | 200 | 99 / 100 | 100 / 100 | 3 | 1 | 0 |
| p101 C1 | 190 / 157 | 190 | 64 / 95 | 93 / 95 | 5 | 31 | 0 |
| p101 D2 | 137 / 135 | 132, conditional | 64 / 66 | 66 / 66 | 1 | 2 | 5 |
| p102 B1 | 208 / 208 | 208 | 104 / 104 | 104 / 104 | 2 | 0 | 0 |
| p102 B2 | 200 / 200 | 200 | 100 / 100 | 100 / 100 | 6 | 0 | 0 |
| p102 B3 | 192 / 192 | 192 | 96 / 96 | 96 / 96 | 1 | 0 | 0 |
| **Total** | **1,395 / 1,357** | **1,390** | **659 / 695** | **693 / 695** | **19** | **36** | **5** |

No coordinate is inserted into the primary models, and the key is unchanged.
“Fixed” means fixed under the stated source/frame or repaired stream; it is
not an independent historical correctness score. The two remaining unknown
positions are the p101 C1 date. D2's source count explicitly includes one
weak but visibly occupied glyph slot; the alternate 136-slot interpretation
is also retained below.

## Command assignments and operational reports

<a id="what-the-records-say"></a>

- p100 D1 and p101 A2 share origin `2312 (1)` and numbered parts 1/2. They
  state that the 11th Army, including all German elements, is placed under
  `O.K. MACKENSEN` under reference `1A11127` and asks for orders. A2's `BITTEP`
  is repaired to `BITTET` with direct coordinate support from D2.
- p101 D2 repeats the ending with origin `2352 (1)` and a damaged source
  frame. The copy supports the word repair in A2; A2 supports reference
  `7011` in place of D2's raw `70G1`. The two observed conflicts remain
  equal-cost alternatives in a joint edit-count model.
- p101 C1 and p102 B1 cite an Orient report on South-Slav units and Montenegro.
  Their recipient strings, origin numbers, date evidence and `VON`/`IN`
  wording differ. They are related reports, without treating the whole first
  part as an exact copy. The p102 date `28` is not supplied in p101's unknowns.
- p101 B2 and p102 B2 describe a detachment with two infantry and two cavalry
  regiments and mountain artillery. Seven observed conflicts and a shared
  word error are preserved and separately priced.
- p102 B3 attributes the report to a Serbian officer and gives unit/reference
  labels. `DONAUDIE`, `VODOHL`, `2429`, `19.10.` and `0626` remain literal;
  no cleaner unit name or clock-time interpretation is introduced.

## Copy evidence and finite checks

### Mackensen ending

After the declared alignment, A2/D2 have **128 identical observed positions,
2 observed conflicts and 2 complementary source masks**. Both copies have
an observed value at each conflict, so there are **4 minimum common streams**,
each requiring 2 aggregate substitutions. The selected `BITTET / 7011`
stream uses one substitution in each record. The full alternatives, including
`BITTEP` and `70G1`, are retained in [certificates.json](certificates.json).
These substitution counts are additional to D2's 5 observed exclusions and
2 source-mask fills. Copy agreement does not prove independent transmission
lineage.

### Detachment passage

The two native 200-slot records have **192 identical observed positions,
7 observed conflicts and 1 complementary mask**. All **128 minimum common
streams** are evaluated and retained, with aggregate substitution cost 7.
The chosen edited reading costs 3 substitutions in p101 and 6 in p102,
for a total of 9. The extra 2 operations repair the shared source-44 error,
`A`→`G` in each copy, to change `SUEUSLAVISCHEN` to `SUEDSLAVISCHEN`.
The fluent shared word is therefore an additional repair, not unchanged
mutual confirmation.

The p102 unit repair `MRGTR`→`2RGTR` uses p101's literal numeral as source
support and is explicitly costed. Its `AR5L`→`ARTL` is a local word repair,
without changing a square cell or unrelated numeral fields. The first copy's
last character is visibly `C` in `GVXDC`; it is not silently transcribed as
the other copy's `G`.

### p101 D2 geometry and weak source slot

The source advertises `RIZI-137`. The `XDVV` group is followed by distinct
upper and lower ink remnants in the fifth position. Two visual reviews
of the same [detail image](sources/p101_D2_illegible.png) support reserving
one illegible source slot; they are not independent historical witnesses.
The JSON's `?` at source 119 is an explicit illegible-glyph notation, not a
printed question mark or a source transcription of the expected `X`.

The primary model excludes source 10–14, the five valid coordinates `XDDAF`,
leaving 132 slots. All **133 possible contiguous-five exclusions** were
completed against the selected common text. Starts **8–12** tie at one
substitution and give the same raw/edited stream; all five origin maps are
retained. The group-boundary start 10 is the displayed convention. The
verifier also prices source-mask exclusions separately when evaluating other
starts. No search over arbitrary five-coordinate deletion sets is claimed.

The old OCR's 136-slot length is represented by an alternate optical model
that omits the weak fifth-slot remnant. That model then requires a missing
coordinate in addition to the five observed exclusions: one substitution,
one source-mask fill and one missing-coordinate fill yield the same final
text. Its origin map refers to positions in the primary 137-slot transcription,
with `null` for the newly supplied model coordinate. The plaintext cannot
resolve the optical ambiguity. This alternative is not an additional record
and does not contribute to the primary totals.

## Source and presentation checks

The first 40 coordinates of p100 D1, p101 A2 and p101 B2 are visible on the
page but absent from the earlier selected OCR frames. Restoring these rows
is a source-transcription recovery, not an insertion into an old transmission.
The earlier p102 OCR candidates already contained much of their message
bodies and remain credited in [prior_evidence.json](prior_evidence.json).

Source-specific details include the invalid `L39`/`C56` in p100 D1,
`C199` in p101 B2, `C92` and 32 dashes in p101 C1, and `S19` plus the weak
slot 119 in D2. The `GGGDA` group in p101 C1 and `VGDGD` in p102 B3 were
checked with dedicated crops; their visible `G` and `D` are retained as
observed coordinates. All source counts, substitutions, fills, exclusions,
unknown domains and numeric/reference changes are independently recomputed.

Each of the eight readable German passages is checked against its exact
case section and every non-`X` label in the edited stream. The two p101 date
question marks remain visible. Abbreviations and irregular endings are
preserved instead of being expanded without a marked interpretation.

## Reproduction

From the repository root:

```bash
python experiments/nov1_mackensen_and_orient_reports/verify.py --verify
python experiments/nov1_mackensen_and_orient_reports/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default verifier uses only the Python standard library and imports no
shared cipher functions. It implements column slicing, pair-domain decoding,
forward constraints, re-encryption witnesses, the 4/128 complete copy-witness
inventories and all 133 contiguous-five exclusions. The optional PDF check
requires PyMuPDF and verifies all 11 crops/full-page images against page,
rectangle, scale and pixel hashes. Both default and exact pixel checks were
completed for this edition.

The full source PDF SHA-256 is
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
Printed pp100–102 correspond to PDF pages 103–105. The source is J. Rives Childs,
*General Solution of the ADFGVX Cipher System*. The full key provenance is
copied into [inputs.json](inputs.json) and retains the credit of **George
Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**.

The source edition and arithmetic review are by **icekylinx and GPT-6 Astra
Pro**. No first historical body-reading priority is claimed. The separate
[p100 challenge](../../pages/100.md#edition-cases-p100) keeps **Armin's 1 March 2017** credit.
The [catalog proposal](catalog_proposal.json) adds only these eight physical
records and changes no challenge status.
