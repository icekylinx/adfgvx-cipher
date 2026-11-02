# ADFGVX Cipher

Readings, source criticism, and reproducible cryptanalysis of German radio traffic from 1918.

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**icekylinx and GPT-6 Astra Pro** · [Read the messages](cases/README.md) · [Research status](docs/research-status.md) · [Methods](docs/methods.md) · [Sources](sources/README.md) · [Citation](CITATION.cff)

A research edition of the **German radio cryptograms in Childs's 1918 collection**: the 22 Lasry–Schmeh challenge entries and a growing catalogue of other messages, with readable plaintexts, original source transcriptions, earlier credits and reproducible decryption evidence.

## Selected results

- **Wider-corpus readings:** [p85 B](cases/other/p85_B.md) explains Hungarian telephone censorship, [p96 B](cases/other/p96_B.md) grants family entry permission, and [p111 B](cases/other/p111_B.md) orders radio use for important messages. Each has an inspected source image, a direct decode and an exact map of any editorial repairs.

- **[p153a](cases/p153a.md) / [p153b](cases/p153b.md): new substantial partial decipherment.** A shared 18-column key recovers 60 of 66 plaintext positions in part 5 and 33 of 54 raw positions in part 6. The ammunition-report reconstruction and separator interpretation yield a 50/54-position conditional template. Every fill, emendation and remaining date/number dependency is explicit.
- **[p146](cases/p146.md):** a literal duplicate-group repair preserves all 239 retained coordinates and fixes 117/122 plaintext positions before filling the missing group. The most likely text announces a new radio call sign.
- **[p187b](cases/p187b.md):** one adjacent coordinate swap explains both of Norbert's earlier word corrections, `NICHT` and `ARBEITET`. The other 140 coordinates and all seven unresolved ending positions remain unchanged.
- **[p109](cases/p109.md):** a same-page near-parallel and an exact multi-witness decoder support the report of an enemy division marching toward Belgrade. The river-name alternatives `SAVE`/`SAVA` and the remaining editorial word choices stay visible.
- **[p215](cases/p215.md):** `Korps Kosch` fits the damaged closing with two known-coordinate changes, compared with five for the earlier `KORPSFRISCH`. Contemporary command records support the interpretation; the full message remains partial.
- **[p152](cases/p152.md):** the damaged challenge fragment matches the fuller p136 transmission. The parallel recovers the body and continuation; every supplied or changed coordinate is recorded.
- **[p158](cases/p158.md):** the challenge combines portions of two separate messages. An exhaustive alignment identifies the split; repaired component copies decrypt and re-encrypt exactly.
- **[p189](cases/p189.md):** a clearer p185 near-parallel supports a conditional partial reading. All ten optimal source-preserving alignments are retained.
- **Earlier results remain part of the edition.** The 2017 readings and September 2026 p176b/p217 publications retain their original authorship. Raw decipherment, conjectural repair, and historical interpretation are distinguished.

Among the 22 challenge entries, three remain wholly open: **p73, p170, p198**. A source-linked recovery or contextual reading is not counted as an independently solved original ciphertext.

All current source reviews, arithmetic audits, and new editorial work are by **icekylinx and GPT-6 Astra Pro**. The tables credit the earlier public reading or the present recovery/review named in that row. Each case gives the most likely readable text, its meaning, and unresolved details.

<!-- READING-CATALOG:START -->
## The 22 challenge entries

These retain the original challenge identifiers. Page numbers alone do not identify a message: p198 is section D, while p198 B/C/E are separate records below.

| Ciphertext | Most likely content | Reading status | Reading or review credit |
|---|---|---|---|
| [p73](cases/p73.md) | Message routed to General von Kress | Open | — |
| [p100](cases/p100.md) | Enemy divisions approaching Belgrade | Prior body reading; source audit | Armin (2017) |
| [p105](cases/p105.md) | Naval telegram acknowledgments | Prior body reading; source audit | Norbert (2017) |
| [p109](cases/p109.md) | Evening report; likely Sava crossing | Prior body; new source parallel | Norbert (2017) |
| [p132](cases/p132.md) | Repeat-transmission instructions for Eilvese | Prior body reading; source audit | Thomas (fragment) and Norbert (body), 2017 |
| [p146](cases/p146.md) | Kerch radio call-sign instruction | Prior body; duplicate-group repair | Norbert (2017) |
| [p152](cases/p152.md) | Silk purchases and transport from the Caucasus | Source-linked body | icekylinx and GPT-6 Astra Pro (2026) |
| [p153a](cases/p153a.md) | Earlier orders; action still to be completed | New partial: 60/66 ordinary-letter positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p153b](cases/p153b.md) | Rearguard artillery ammunition report | New raw partial; conditional body and footer | icekylinx and GPT-6 Astra Pro (2026) |
| [p158](cases/p158.md) | Routing and army-key instructions | Composite sources identified | icekylinx and GPT-6 Astra Pro (2026) |
| [p164a](cases/p164a.md) | Temesvar / MIRCO contextual fragments | Prior partial; constraint audit | Norbert (2017) |
| [p164b](cases/p164b.md) | Height 828 and an uneventful situation report | Prior partial; constraint audit | Norbert (2017) |
| [p170](cases/p170.md) | Short intercept; original length uncertain | Open | — |
| [p171](cases/p171.md) | Ruble rates and expectations about Russia | Prior body reading; source audit | Norbert (2017) |
| [p176a](cases/p176a.md) | Breakthrough toward the north or northeast | Prior body reading; source audit | Norbert (2017) |
| [p176b](cases/p176b.md) | Army positions near Peterreve and Versecz | Prior contextual reading; constraint audit | Prinz and GPT-6 Astra (2026) |
| [p187](cases/p187.md) | Monitoring Russian and Polish army traffic | Prior body reading; source audit | George Lasry and Norbert (2017) |
| [p187b](cases/p187b.md) | Teleprinter failure and written reporting | Prior body; adjacent-swap explanation | George Lasry and Norbert (2017) |
| [p189](cases/p189.md) | Apparent vehicle request / await orders | Conditional partial | icekylinx and GPT-6 Astra Pro (2026) |
| [p198](cases/p198.md) | CHI intercept with a five-coordinate shortfall | Open | — |
| [p215](cases/p215.md) | Apparent Entente troop-transport report | Prior partial; conditional Kosch interpretation | Norbert (2017) |
| [p217](cases/p217.md) | British cruiser and Allied squadron at Sevastopol | Prior body reading; correction verified | Prinz and GPT-6 Astra (2026); correction: Christian Horvat |

## Other ciphertexts — 34 reviewed records

Each row identifies a separate source record outside the 22-entry challenge. Multipart messages and repeated transmissions have separate rows even when one case page discusses them together. Direct readings, source-supported reconstructions and conjectural repairs retain their stated limits.

| Ciphertext | Most likely content | Reading status | Reading or review credit |
|---|---|---|---|
| [p77 B](cases/context/radio_instructions.md#p77-b--call-sign-instruction-for-konia) | Konia radio call sign and wavelengths | Direct reading; one word normalized | icekylinx and GPT-6 Astra Pro (2026) |
| [p85 B](cases/other/p85_B.md) | Telephone censorship through Budapest | 99/99 raw positions; two word repairs explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p89 A2](cases/supplementary/p89_A2.md) | Shipping and railway routing to Nikolayev | Earlier reading; one source glyph uncertain | Ayush Agarwal; review by D. Bourdeau (2026) |
| [p96 B](cases/other/p96_B.md) | Entry permission for Filittis and family | 180/181 raw positions; Copenhagen repair costed | icekylinx and GPT-6 Astra Pro (2026) |
| [p107 D](cases/supplementary/p107_D.md) | Acknowledgment of operational telegrams | Earlier reading; parenthesized glyphs retained | Ayush Agarwal; review by D. Bourdeau (2026) |
| [p109 B](cases/p109.md) | Evening enemy-division report toward Belgrade | Near-parallel supporting p 109; word alternatives remain | icekylinx and GPT-6 Astra Pro (2026) |
| [p111 B](cases/other/p111_B.md) | Use radio for important messages | 154/154 direct positions; no coordinate edits | icekylinx and GPT-6 Astra Pro (2026) |
| [p134 B](cases/context/radio_instructions.md#p134-b--repeat-a-fourth-period-telegram-in-the-fifth) | Repeat a fourth-period telegram in the fifth | 50/51 raw positions; wording partly editorial | icekylinx and GPT-6 Astra Pro (2026) |
| [p136 B1](cases/p152.md#raw-p136-b1-parallel-plaintext) | Silk purchases in the Caucasus; first part | Full raw reading; supports the p 152 fragment | icekylinx and GPT-6 Astra Pro (2026) |
| [p136 B2](cases/p152.md#raw-continuation-witnesses) | Resell goods whose transport is not assured | Continuation; one coordinate supplied by a parallel | icekylinx and GPT-6 Astra Pro (2026) |
| [p152 E2](cases/p152.md#raw-continuation-witnesses) | Parallel continuation of the silk instruction | Direct raw reading with residual garbles | icekylinx and GPT-6 Astra Pro (2026) |
| [p155 A1](cases/context/p155.md) | Asgard arrival at Poti and troop pickup | 84/85 raw positions; source glyph remains erased | icekylinx and GPT-6 Astra Pro (2026) |
| [p155 A2](cases/context/p155.md) | Asgard/Tresivolus shipping continuation | Conditional single-coordinate loss repair | icekylinx and GPT-6 Astra Pro (2026) |
| [p159 B](cases/p158.md#component-readings) | Munich routing and army-key instruction | Reconstruction from repeated transmissions | Childs (1918); review: icekylinx and GPT-6 Astra Pro |
| [p159 C](cases/p158.md#component-readings) | Munich–Innsbruck routing and army-key instruction | Source-supported one-coordinate deletion | icekylinx and GPT-6 Astra Pro (2026) |
| [p164 A4](cases/context/p164_A4.md) | Dismounted cavalry west of an unidentified MIRCO | 87/99 raw positions; full proposal explicitly repaired | icekylinx and GPT-6 Astra Pro (2026) |
| [p168 C](cases/p158.md#earlier-historical-reading-of-a-component) | Repeated Munich routing order 11338 | Parallel witness to the p 159 B component | Childs (1918); review: icekylinx and GPT-6 Astra Pro |
| [p168 D](cases/p158.md#component-readings) | Repeated Munich–Innsbruck routing instruction | Parallel witness to the p 159 C component | icekylinx and GPT-6 Astra Pro (2026) |
| [p185 C](cases/p189.md) | Vehicle provision impossible; await orders | Direct raw reading; source parallel for p 189 A | icekylinx and GPT-6 Astra Pro (2026) |
| [p185 D](cases/context/transport.md#p185-d-source-and-gap-model) | Movement via DHFN and readiness instruction | 91/99 positions under an unproved five-loss geometry | icekylinx and GPT-6 Astra Pro (2026) |
| [p186 A1](cases/context/p186.md#part-1--richi-170) | Monitor Russian and Polish army traffic | Earlier reading; three explicit erasure fills | Lasry team and Norbert (2017); review: icekylinx and GPT-6 Astra Pro |
| [p186 A2](cases/context/p186.md#part-2--richi-174) | Encrypted reporting and teleprinter failure | 80/87 conservative raw positions; ending unresolved | Lasry team and Norbert (2017); review: icekylinx and GPT-6 Astra Pro |
| [p187 C](cases/supplementary/p187_C.md) | Connection with Mackensen's army | Earlier reading; source correction checked | Ayush Agarwal; review by D. Bourdeau (2026) |
| [p189 C](cases/context/p189_C.md) | Instruction to use the December key; IRRTUM | 61/62 raw positions; two explicit substitutions | icekylinx and GPT-6 Astra Pro (2026) |
| [p189 E](cases/context/transport.md#independent-transport-context) | Pump, cars and trailers | Direct partial reading; counts unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p193 E](cases/context/transport.md#independent-transport-context) | Sprung cart for attachment; a car | Direct partial reading; one unknown cell | icekylinx and GPT-6 Astra Pro (2026) |
| [p194 A](cases/context/transport.md#independent-transport-context) | Arranged departure to Hanau via DHFN | Near-parallel; composite fixes 86/87 positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p196 B](cases/context/transport.md#independent-transport-context) | Repeated arranged departure to Hanau | Near-parallel; time digit remains unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p197 C](cases/context/transport_197_198.md) | Transport of radio equipment to Darmstadt | Missing-group hypothesis checked against p 198 B | icekylinx and GPT-6 Astra Pro (2026) |
| [p197 D](cases/context/transport_197_198.md) | Lorry, trailer and petrol-pump instruction | Partial witness; readable reconstruction costed | icekylinx and GPT-6 Astra Pro (2026) |
| [p197 E](cases/context/transport.md#independent-transport-context) | Lorry departure and men remaining until Sunday | Partial near-parallel; time and count unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p198 B](cases/context/transport_197_198.md) | Repeated equipment transport to Darmstadt | Clearer near-parallel; editorial changes explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p198 C](cases/context/transport.md#independent-transport-context) | Repeated lorry departure and Sunday stay | Direct partial reading; separate from challenge D | icekylinx and GPT-6 Astra Pro (2026) |
| [p198 E](cases/context/transport_197_198.md) | Repeated lorry, trailer and petrol-pump order | Literal duplicate-group deletion; partial reading | icekylinx and GPT-6 Astra Pro (2026) |

The catalogue covers source-reviewed records with published reading evidence; the wider OCR search pool contains additional unreviewed ciphertext candidates. Earlier authors retain their credits. Current source review and new research use **icekylinx and GPT-6 Astra Pro**; a review credit does not assert first-decipherment priority.
<!-- READING-CATALOG:END -->

## Review coverage

The [review ledger](data/review_ledger.json) currently records **98 claims and provenance checks**. It includes the 2017 comment history, earlier square completions, p217's published key images and naval corroboration, p176b's French documentary context, the newly checked October 2026 submissions, and the historical reading of p158's component.

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

- `cases/`: Readings, qualifications, original credits, and source links
- `docs/research-status.md`: Current result boundaries and the next evidence or method that could reduce ambiguity
- `docs/methods.md`: A reader's guide to the cipher, evidence layers, exact searches and their limits
- `data/messages.json`: All 22 source records, legacy transcriptions, and conservative analysis layers
- `data/keys.json`: 25 historical, comparison, reported, or newly recovered partial keys; provenance and unknown cells retained
- `data/prior_readings.json`: 35 attributed earlier readings/fragments and 25 recomputed repair variants
- `data/supplementary_readings.json`: Three October 2026 readings and their primary-source corrections
- `data/review_ledger.json`: Claim-by-claim findings, earlier criticism, and exact attribution
- `data/certificates/`: Machine-readable source, edit, and plaintext evidence
- `adfgvx/`: Independent cipher and verification code
- `experiments/`: Portable attacks, bounded results, controls, and model provenance
- `sources/`: Bibliography and selected source excerpts

Identifiers use the printed page number. `p187` and `p187b` are the two parts listed separately in the original challenge. A question mark means unresolved evidence, never an arbitrary completed square cell. Original German text is preserved as data; editorial material is in English.

## Citation and reuse

icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026). Cite the relevant case and commit using [CITATION.cff](CITATION.cff). Historical records, prior decipherments, key recovery, and later corrections retain their individual attribution. The [Apache-2.0 license](LICENSE) covers this project's code and editorial contributions; third-party materials retain their original status. See [NOTICE](NOTICE) and [Contributing](CONTRIBUTING.md).
