# ADFGVX Cipher

Readings, source criticism, and reproducible cryptanalysis of German radio traffic from 1918.

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**icekylinx and GPT-6 Astra Pro** · [Read the messages](cases/README.md) · [Research status](docs/research-status.md) · [Methods](docs/methods.md) · [Sources](sources/README.md) · [Citation](CITATION.cff)

A unified edition of the **22 German radio cryptograms** in Klaus Schmeh and George Lasry's challenge: original source transcription, earlier decipherments, corrections, new source relationships, and reproducible verification.

## Selected results

- **[p153a](cases/p153a.md) / [p153b](cases/p153b.md): new substantial partial decipherment.** A shared 18-column key recovers 60 of 66 plaintext positions in part 5 and 33 of 54 raw positions in part 6. The ammunition-report reconstruction and separator interpretation yield a 50/54-position conditional template. Every fill, emendation and remaining date/number dependency is explicit.
- **[p146](cases/p146.md):** a literal duplicate-group repair preserves all 239 retained coordinates and fixes 117/122 plaintext positions before filling the missing group. The most likely text announces a new radio call sign.
- **[p187b](cases/p187b.md):** one adjacent coordinate swap explains both of Norbert's earlier word corrections, `NICHT` and `ARBEITET`. The other 140 coordinates and all seven unresolved ending positions remain unchanged.
- **[p109](cases/p109.md):** a same-page near-parallel and an exact multi-witness decoder support the report of an enemy division marching toward Belgrade. The river-name alternatives `SAVE`/`SAVA` and the remaining editorial word choices stay visible.
- **[p215](cases/p215.md):** `Korps Kosch` fits the damaged closing with two known-coordinate changes, compared with five for the earlier `KORPSFRISCH`. Contemporary command records support the interpretation; the full message remains partial.
- **[p152](cases/p152.md):** the damaged challenge fragment matches the fuller p136 transmission. The parallel recovers the body and continuation; every supplied or changed coordinate is recorded.
- **[p158](cases/p158.md):** the challenge combines portions of two separate messages. An exhaustive alignment identifies the split; repaired component copies decrypt and re-encrypt exactly.
- **[p189](cases/p189.md):** a clearer p185 near-parallel supports a conditional partial reading. All ten optimal source-preserving alignments are retained.
- **Earlier results remain part of the edition.** The 2017 readings and September 2026 p176b/p217 publications retain their original authorship. Raw decipherment, conjectural repair, and historical interpretation are distinguished.

Three entries remain wholly open: **p73, p170, p198**. A source-linked recovery or contextual reading is not counted as an independently solved original ciphertext.

All current source reviews, arithmetic audits, and new editorial work are by **icekylinx and GPT-6 Astra Pro**. The final column credits the earlier public reading or the new recovery named in that row. Each case gives the most likely readable text, its meaning, and unresolved details.

## The 22 challenge entries

| Entry | Current result | Reading or recovery credit |
|---|---|---|
| [p73](cases/p73.md) | Open | — |
| [p100](cases/p100.md) | Prior body reading; source audit | Armin (2017) |
| [p105](cases/p105.md) | Prior body reading; source audit | Norbert (2017) |
| [p109](cases/p109.md) | Prior body; new source parallel | Norbert (2017) |
| [p132](cases/p132.md) | Prior body reading; source audit | Thomas (fragment) and Norbert (body), 2017 |
| [p146](cases/p146.md) | Prior body; duplicate-group repair | Norbert (2017) |
| [p152](cases/p152.md) | Source-linked body | icekylinx and GPT-6 Astra Pro (2026) |
| [p153a](cases/p153a.md) | New partial: 60/66 ordinary-letter positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p153b](cases/p153b.md) | New raw partial; conditional body and footer | icekylinx and GPT-6 Astra Pro (2026) |
| [p158](cases/p158.md) | Composite sources identified | icekylinx and GPT-6 Astra Pro (2026) |
| [p164a](cases/p164a.md) | Prior partial; constraint audit | Norbert (2017) |
| [p164b](cases/p164b.md) | Prior partial; constraint audit | Norbert (2017) |
| [p170](cases/p170.md) | Open | — |
| [p171](cases/p171.md) | Prior body reading; source audit | Norbert (2017) |
| [p176a](cases/p176a.md) | Prior body reading; source audit | Norbert (2017) |
| [p176b](cases/p176b.md) | Prior contextual reading; constraint audit | Prinz and GPT-6 Astra (2026) |
| [p187](cases/p187.md) | Prior body reading; source audit | George Lasry and Norbert (2017) |
| [p187b](cases/p187b.md) | Prior body; adjacent-swap explanation | George Lasry and Norbert (2017) |
| [p189](cases/p189.md) | Conditional partial | icekylinx and GPT-6 Astra Pro (2026) |
| [p198](cases/p198.md) | Open | — |
| [p215](cases/p215.md) | Prior partial; conditional Kosch interpretation | Norbert (2017) |
| [p217](cases/p217.md) | Prior body reading; correction verified | Prinz and GPT-6 Astra (2026); correction: Christian Horvat |

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

[Four further p197/p198 witnesses](cases/context/transport_197_198.md) identify equipment for Darmstadt and a lorry/trailer/petrol-pump instruction. A literal duplicate-group deletion restores one source's declared length. Their readable composites retain exact edit costs, unresolved digits and linked number fields; they do not solve the p198 D challenge.

The [p155 Kress-route shipping message](cases/context/p155.md) adds two source-checked parts. Its Asgard/Tresivolus context is independently corroborated in a contemporary diary; it does not determine p73's date or key.

[The p77 and p134 radio instructions](cases/context/radio_instructions.md) add source-checked call-sign and repeat-transmission context for p146 and p132.

[p189 C](cases/context/p189_C.md) adds a key-use instruction with 61/62 raw positions fixed. Two explicitly mapped substitutions give its most likely wording. The directly decoded `DEZEMBER` and `IRRTUM` remain visible alongside the 15 November header; no explanation of that date tension is assumed.

## Review coverage

The [review ledger](data/review_ledger.json) currently records **97 claims and provenance checks**. It includes the 2017 comment history, earlier square completions, p217's published key images and naval corroboration, p176b's French documentary context, the newly checked October 2026 submissions, and the historical reading of p158's component.

A September 2026 mass-solution claim is retained with its [reproducibility assessment](data/reviews/unsupported_claim_checks.json) and **Jozef Krajcovic's earlier critique**. Its published constants and selected substrings do not provide a reproducible full reading; no target is marked solved on that basis.

## Verify

Python 3.10 or later; standard library only:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.verify --json
```

This checks the core source, cipher and reconstruction certificates, including 25 explicit repair variants of 14 earlier-readable entries and the three supplementary records. It reproduces source maps, retained-coordinate roundtrips, uncertainty domains and contradictory editorial completions. Odd-length ciphertext cannot silently lose a coordinate.

The [verification workflow](.github/workflows/verify.yml) also runs focused transport, p153 linked-field/key-structure, p215 interpretation, p109 ranking-summary and recorded open-target checks. Individual case and experiment pages provide their commands. Rebuilding corpus models or rerunning large searches is documented separately from checking the compact certificates.

## Search methods

The [experiment index](experiments/README.md) records completed search bounds, positive controls, scoring failures, and reproducible code. The p153 work enumerates column-length segmentations at widths 14, 16 and 18, then uses bounded pairing, order and square searches. The width-18 refinement produced the new partial reading. A separate exact post-discovery crib check, independently implemented twice, establishes its narrow key-equivalence and emendation constraints. Complete checks over every integer width from 14 through 26 leave only width 18 for the sixty-letter crib.

The [multi-witness decoder](experiments/parallel_decoder/README.md) adds exact language-ranked optimization under a declared source-edit budget. For p109, dynamic programming covers all `2^42` minimum-cost plaintexts without a beam or a plaintext crib. Its successes, model failures, 280 ranked candidates and word-level costs are retained together.

The [joint scattered-loss decoder](experiments/p198_joint_exact/README.md) exactly optimizes both missing positions and their values. For p198's five-loss hypothesis it covers 8,670,506,592,384 witnesses per fixed complete key, including aliases. Its four-gram controls expose wrong global optima even under true keys; those failures and all source-preserving witnesses are retained. The [p73 coordinate-count diagnostic](experiments/open_targets/P73_HISTOGRAM.md) provides a separate, transposition-independent way to prioritize key hypotheses.

The [six-gram extension](experiments/p198_joint_six/README.md) recovers one complete control, its exact loss positions and their values under two objectives. A second control still has a better-scoring wrong competitor. These calibrated successes and failures guide further attacks without changing the historical target statuses.

The [exact digit/Q/Y frontier](experiments/p198_category_frontier/README.md) supplies a language-model-free constraint on all 40,320 completions of one p198 partial key: an 85-character reading with just three digits must have at least thirteen Q/Y positions; a Q/Y-free reading needs at least ten digits. Two implementations recompute the full finite scope, and concrete witnesses attain every reported boundary point. This sharpens future proposal checks without declaring a plaintext or excluding the key.

## Contents

| Path | Contents |
|---|---|
| `cases/` | Readings, qualifications, original credits, and source links |
| `docs/research-status.md` | Current result boundaries and the next evidence or method that could reduce ambiguity |
| `docs/methods.md` | A reader's guide to the cipher, evidence layers, exact searches and their limits |
| `data/messages.json` | All 22 source records, legacy transcriptions, and conservative analysis layers |
| `data/keys.json` | 25 historical, comparison, reported, or newly recovered partial keys; provenance and unknown cells retained |
| `data/prior_readings.json` | 35 attributed earlier readings/fragments and 25 recomputed repair variants |
| `data/supplementary_readings.json` | Three October 2026 readings and their primary-source corrections |
| `data/review_ledger.json` | Claim-by-claim findings, earlier criticism, and exact attribution |
| `data/certificates/` | Machine-readable source, edit, and plaintext evidence |
| `adfgvx/` | Independent cipher and verification code |
| `experiments/` | Portable attacks, bounded results, controls, and model provenance |
| `sources/` | Bibliography and selected source excerpts |

Identifiers use the printed page number. `p187` and `p187b` are the two parts listed separately in the original challenge. A question mark means unresolved evidence, never an arbitrary completed square cell. Original German text is preserved as data; editorial material is in English.

## Citation and reuse

icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026). Cite the relevant case and commit using [CITATION.cff](CITATION.cff). Historical records, prior decipherments, key recovery, and later corrections retain their individual attribution. The [Apache-2.0 license](LICENSE) covers this project's code and editorial contributions; third-party materials retain their original status. See [NOTICE](NOTICE) and [Contributing](CONTRIBUTING.md).
