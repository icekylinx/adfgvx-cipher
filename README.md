# ADFGVX 1918

**IceKylin and GPT-6 Astra (OpenAI)** · [Contributors](AUTHORS.md) · [Sources](sources/registry.json)

A unified edition of the **22 German radio cryptograms** in Klaus Schmeh and George Lasry's challenge: original source transcription, earlier decipherments, corrections, new source relationships, and reproducible verification.

## Results

- **p153a / p153b: new substantial partial decipherment.** A shared 18-column key recovers 60 of 66 ordinary-letter positions in part 5 and 33 of 54 raw positions in part 6. A coherent ammunition-report reconstruction requires twelve erasure fills and two explicit coordinate emendations; dates, numbers and trailing text remain unresolved.

- **p152:** the damaged challenge fragment matches the fuller p136 transmission. The parallel recovers the body and continuation; every supplied or changed coordinate is recorded.
- **p158:** the challenge combines portions of two separate messages. An exhaustive alignment identifies the split; repaired component copies decrypt and re-encrypt exactly.
- **p189:** a clearer p185 near-parallel supports a conditional partial reading. All ten optimal source-preserving alignments are retained.
- **Earlier results remain part of the edition.** The 2017 readings and September 2026 p176b/p217 publications retain their original authorship. Raw decipherment, conjectural repair, and historical interpretation are distinguished.

Three entries remain wholly open: **p73, p170, p198**. A source-linked recovery or contextual reading is not counted as an independently solved original ciphertext.

| Entry | Reviewed state | First reading or present contribution |
|---|---|---|
| [p73](cases/p73.md) | Open | — |
| [p100](cases/p100.md) | Prior body reading; source audit | Armin (2017 comment author) |
| [p105](cases/p105.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p109](cases/p109.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p132](cases/p132.md) | Prior body reading; source audit | Thomas (fragment), Norbert (body) |
| [p146](cases/p146.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p152](cases/p152.md) | Source-linked body | This review, 2026 |
| [p153a](cases/p153a.md) | New partial: 60/66 ordinary-letter positions | IceKylin and GPT-6 Astra (2026) |
| [p153b](cases/p153b.md) | New raw partial; conditional 42-letter body | IceKylin and GPT-6 Astra (2026) |
| [p158](cases/p158.md) | Composite sources identified | This review, 2026 |
| [p164a](cases/p164a.md) | Prior partial; constraint audit | Norbert (2017 comment author) |
| [p164b](cases/p164b.md) | Prior partial; constraint audit | Norbert (2017 comment author) |
| [p170](cases/p170.md) | Open | — |
| [p171](cases/p171.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p176a](cases/p176a.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p176b](cases/p176b.md) | Prior contextual reading; constraint audit | Prinz (2026 publication) |
| [p215](cases/p215.md) | Prior partial; constraint audit | Norbert (2017 comment author) |
| [p187](cases/p187.md) | Prior body reading; source audit | George Lasry, Norbert (2017 comment author) |
| [p187b](cases/p187b.md) | Prior body reading; source audit | George Lasry, Norbert (2017 comment author) |
| [p189](cases/p189.md) | Conditional partial | This review, 2026 |
| [p198](cases/p198.md) | Open | — |
| [p217](cases/p217.md) | Prior body reading; correction verified | Prinz (2026 publication), Christian Horvat (later correction) |

## Supplementary frontier results

The October 2026 readings below were first submitted by **Ayush Agarwal** and reviewed by **D. Bourdeau**. This edition checks the original images and corrects source counts or masked coordinates. They do not change the 22-target total.

| Record | Content | Current review |
|---|---|---|
| [p89 A2](cases/supplementary/p89_A2.md) | Shipping and railway routing to Nikolayev | 290 coordinates / 145 letters; one damaged glyph remains uncertain. |
| [p107 D](cases/supplementary/p107_D.md) | Acknowledgment of operational telegrams | 176 coordinates; printed and parenthesized letters retained separately. |
| [p187 C](cases/supplementary/p187_C.md) | Connection with Mackensen's army | 134 coordinates; source `FFXXV` restores `M` in the raw `MIS`. |

## Contextual records

[p164 A4](cases/context/p164_A4.md) supports a conditional reading about dismounted cavalry west of an unidentified `MIRCO`. The source fixes 87 of 99 letters; the complete editorial hypothesis requires nine known-coordinate substitutions and thirteen erasure fills. It does not change p164a or p164b to solved.

[The p185/p189 transport conversation](cases/context/transport.md) adds seven source records. Two near-parallel transport orders combine to fix 86 of 87 letters; a separate p185 D missing-group hypothesis fixes 91 of 99 letters conditionally. All 194 possible gap placements and both pairs of disagreeing witnesses remain available.

The [p155 Kress-route shipping message](cases/context/p155.md) adds two source-checked parts. Its Asgard/Tresivolus context is independently corroborated in a contemporary diary; it does not determine p73's date or key.

## Review coverage

The [review ledger](data/review_ledger.json) currently records **66 claims and provenance checks**. It includes the 2017 comment history, earlier square completions, p217's published key images and naval corroboration, p176b's French documentary context, the newly checked October 2026 submissions, and the historical reading of p158's component.

A September 2026 mass-solution claim is retained with its [reproducibility assessment](data/reviews/unsupported_claim_checks.json) and **Jozef Krajcovic's earlier critique**. Its published constants and selected substrings do not provide a reproducible full reading; no target is marked solved on that basis.

## Verify

Python 3.10 or later; standard library only:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.verify --json
```

The verifier checks independent ADFGVX arithmetic, eight full source roundtrips, the p152 suffix alternatives, the p158 splice and glyph variants, every p189 source-preserving alignment and plaintext domain, and 25 explicit reconstructions of 14 earlier-readable entries. Three supplementary source and published layers are verified as well. The p164 A4 editorial hypothesis and seven transport-context records have separate certificates and independent coordinate/domain checks. The p164/p215 checks also reproduce uncertainty counts and contradictions in later completions. The p153 certificate verifies the unchanged sources, all coordinate mappings, the nineteen-letter square, and the exact twelve-fill/two-emendation body hypothesis. Odd-length ciphertext cannot silently lose a coordinate.

## Search methods

The [experiment index](experiments/README.md) records completed search bounds, positive controls, scoring failures, and reproducible code. The p153 work enumerates column-length segmentations at widths 14, 16 and 18, then uses bounded pairing, order and square searches. The width-18 refinement produced the new partial reading. A separate exact post-discovery crib check, independently implemented twice, establishes its narrow key-equivalence and emendation constraints.

## Contents

| Path | Contents |
|---|---|
| `cases/` | Readings, qualifications, original credits, and source links |
| `data/messages.json` | All 22 source records, legacy transcriptions, and conservative analysis layers |
| `data/keys.json` | 25 historical, comparison, reported, or newly recovered partial keys; provenance and unknown cells retained |
| `data/prior_readings.json` | 34 attributed earlier readings/fragments and 25 recomputed repair variants |
| `data/supplementary_readings.json` | Three October 2026 readings and their primary-source corrections |
| `data/review_ledger.json` | Claim-by-claim findings, earlier criticism, and exact attribution |
| `data/certificates/` | Machine-readable source, edit, and plaintext evidence |
| `adfgvx/` | Independent cipher and verification code |
| `experiments/` | Portable attacks, bounded results, controls, and model provenance |
| `sources/` | Bibliography and selected source excerpts |

Identifiers use the printed page number. `p187` and `p187b` are the two parts listed separately in the original challenge. A question mark means unresolved evidence, never an arbitrary completed square cell. Original German text is preserved as data; editorial material is in English.

## Credit and reuse

The present review is by **[IceKylin](https://github.com/icekylinx) and GPT-6 Astra (OpenAI)**. Historical records, prior decipherments, key recovery, and later corrections have separate attribution in each case and the source catalog. New code and editorial material use the [MIT license](LICENSE); third-party source material retains its own status.
