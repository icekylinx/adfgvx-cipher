# November 1 contact times, service mail and the Sava evening report

Prepared by **icekylinx and GPT-6 Astra Pro**. This source edition covers
five physical records on Childs printed p99 (PDF p102). The published
`Nov1-3` key is unchanged. Two reader pages separate the
[radio and mail messages](../../cases/pages/099.md#edition-cases-radio-nov1-contact-and-mail)
from the [Sava-crossing report](../../cases/pages/099.md#edition-cases-military-sava-crossing-evening-report).

## Accepted scope

| Record | Literal slots / valid coordinates | Working slots | Fixed raw / total labels | Fixed edited / total labels | Observed substitutions | Source-mask fills | Missing-coordinate fills |
|---|---:|---:|---:|---:|---:|---:|---:|
| p99 A | 133 / 109 | 134, conditional | 43 / 67 | 67 / 67 | 0 | 24 | 1 |
| p99 B1 | 172 / 172 | 172 | 86 / 86 | 86 / 86 | 0 | 0 | 0 |
| p99 C1 | 136 / 122 | 136 | 54 / 68 | 68 / 68 | 3 | 14 | 0 |
| p99 C2 | 102 / 97 | 102 | 46 / 51 | 51 / 51 | 0 | 5 | 0 |
| p99 D | 100 / 100 | 100 | 50 / 50 | 50 / 50 | 0 | 0 | 0 |
| **Total** | **643 / 600** | **644** | **279 / 322** | **322 / 322** | **3** | **43** | **1** |

All 643 literal source slots are retained. A supplies one additional model
coordinate; no observed coordinate is excluded. The table's raw count for A
is conditional on that geometry. Its literal 133-slot paired prefix and
unpaired coordinate are also preserved, without presenting them as a readable
native body. “Fixed” means a singleton label under the stated key/frame or
edited stream, not independent proof of the transmitted text.

A conditionally asks for proposed communication times between Ringbahn periods,
with literal `ZWISCEN` displayed as `zwisc[h]en`. The bracketed letter is not
encrypted. B1 reports crossing the Sava and keeps
unit labels `30 I.D.` and `G.K.39`. C1/C2 route service mail through Gleiwitz
for aircraft collection. D acknowledges receipt of reference `11127`; its
literal `GAH` and `E.O.K.11` are not repaired.

## p99 A: one extra model coordinate, without source alteration

The page itself has 133 slots and advertises `RIZI-133`. It includes 22
printed dashes and two noncoordinate `E` glyphs, at source 38 and 40. They
remain visible in the literal layer. The primary model appends one unknown
coordinate to obtain 134 transmitted slots. The current conditional reading
uses no observed-coordinate substitutions and fills all 24 source masks plus
that missing coordinate. All 109 valid received coordinates remain unchanged.

Raw plaintext positions 35–41 are `?WI??E?`. The earlier partial edition
supplied the first unknown as `X`; this separator was an editorial completion
of source dash 10, not a source observation. Supplying that dash as `F`
instead, together with source 18=`D`, 26=`D` and 40=`G`, yields literal
`ZWISCEN`. Each of the four chosen letters keeps its other, observed
half-coordinate. The raw position count remains 43/67; the conditional edited
count rises from 64/67 to 67/67. The certificate preserves the former
partial template and its 21-mask-fill ledger separately.

The seven-position span has 1,296 coordinate-compatible local completions
before language is considered. `ZWISCEN` is a contextual candidate, not
a uniqueness result. Its display-only spelling completion is explicitly
declared: only the bracketed `h` is removed during readable-label checking.
No `H` or extra coordinate is inserted into the candidate.

The earlier full `WIEDER` candidate remains separately costed at **3 observed
substitutions, 24 source-mask fills and 1 missing-coordinate fill**. It is
excluded from the primary totals above. The current proposal supplies the
phrase at zero observed substitutions. The known neighboring p110/p117
radio messages support the term `RINGBAHN`; they do not establish either
whole phrase or prove this loss mechanism. Their exact selected raw strings and input-file
hashes are snapshotted in [inputs.json](inputs.json).

### Completed diagnostic and fixed-template comparison

[one_coordinate_screen.json](search/one_coordinate_screen.json) retains all
**534 completed configurations**: 134 insertion boundaries and 133 deletion
indices in each of two distinct layers, transmitted and fractionated. The
known-quad objective comes from the frozen book model whose
[provenance](../joint_search/models/provenance.json) predates this source
edition. No model is retrained. The 188 model cells actually queried are
preserved in [queried_model_cells.json](search/queried_model_cells.json),
with the full binary's SHA-256. The verifier regenerates all candidates and
scores from those cells; an optional argument checks them against the full
binary. The replay is not merely a check of a reported best candidate.

The score uses only fully known four-letter windows. The top result has
only nine such windows. This was a short, damaged-text diagnostic without
a new blind control; its score is not an independent confirmation of a
historical plaintext or geometry. The readable fragments and exact coordinate
constraints are the evidence retained here.

The fixed-template comparison evaluates all **134 transmitted insertion
boundaries** against the current complete candidate. Boundaries **132 and
133** both require zero observed substitutions and a supplied `D`, yielding
the same completed ciphertext. Both source-origin maps, raw inverses and
fill ledgers are preserved independently. Their raw support differs: boundary
132 fixes 42/67 positions, while the displayed boundary 133 fixes 43/67.
Appending is a presentation convention; the data do not choose between those
two origins. This retrospective comparison does not turn the candidate into
a blind recovery or exclude other loss/repair mechanisms.

## Native records and source cautions

- B1 has 172 valid coordinates. Its earlier 132-coordinate OCR frame omitted
  the first visible row. This is a source-transcription recovery, not a
  transmitted-coordinate insertion.
- C1 has 136 slots, including 14 dashes. Source 122–124 are visibly `AAA`;
  the candidate changes them to `DGV` at a cost of three observed substitutions.
  The resulting local repairs are raw label 3 `9`→`X`, 12 `D`→`N`, and
  22 `O`→`E`. The rest of its supplied reading comes from explicit dash fills.
- C2 has 102 slots and begins with five dashes. Filling them with `VDFAG`
  yields the aircraft-collection continuation without an observed substitution.
  The C source header says **2 TLE**, not the earlier OCR's 3.
- D is an unchanged 100-coordinate frame. Its final `VXFGD` resolves the
  earlier OCR candidate's one unknown label; that earlier body is credited.
- B1 and the existing p100 challenge share `UKS v ZON` and `2016 (1)`.
  Their headers differ as `3 TLE` versus `2 TLE`. The p100 header crop is
  included as a limited association witness. No p100 record is duplicated,
  and its earlier body remains credited to **Armin, March 1, 2017**.

## Verification

From the repository root:

```bash
python experiments/nov1_contact_mail_and_sava/verify.py --verify
python experiments/nov1_contact_mail_and_sava/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
python experiments/nov1_contact_mail_and_sava/verify.py --verify --quad /path/to/german_military36_quad.bin
```

The default verifier uses only the Python standard library. Optional PDF
verification requires PyMuPDF. It binds all eight source images to the full
PDF hash, page number, rectangle, scale and pixel bytes. The full model-binding
option reads a little-endian float32 binary and checks its hash and every
queried cell. Both optional checks were completed for this edition.

The cipher verifier implements column slicing and row reconstruction
independently of the shared package. It recomputes raw plaintext domains,
source origins, every repair and fill, all frame counts, all diagnostic
configurations, both equal minimum origin maps and the earlier partial and
`WIEDER` ledgers. The former partial edition's arbitrary completions remain
arithmetic witnesses only. The current full candidate re-encrypts exactly,
with the displayed `h` absent from its seven-label `ZWISCEN` word. Each of
the five readable German passages must retain every non-`X` label, including
numerals, after only the explicitly declared display expansion is removed.

## Provenance and attribution

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*.
The full PDF hash is
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
The full published key and its provenance are copied into
[inputs.json](inputs.json); the key retains the credit of **George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker**.

The [prior-evidence snapshot](prior_evidence.json) retains the earlier
unreviewed OCR candidates and the explicit p100 attribution. The source
edition and arithmetic review are by **icekylinx and GPT-6 Astra Pro**.
No first historical decipherment priority is claimed. The
[catalog proposal](catalog_proposal.json) adds only these five physical p99
records and leaves challenge statuses unchanged.
