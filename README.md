# ADFGVX Cipher

Reading notation and evidence layers: [Reading conventions](docs/reading-conventions.md).

Readings, source criticism, and reproducible cryptanalysis of German radio traffic from 1918.

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**icekylinx and GPT-6 Astra Pro** · [Read the messages](cases/README.md) · [Repository map](docs/repository-map.md) · [Research status](docs/research-status.md) · [Methods](docs/methods.md) · [Sources](sources/README.md) · [Citation](CITATION.cff)

A research edition of the **German radio cryptograms in Childs's 1918 collection**: the 22 Lasry–Schmeh challenge entries and a growing catalogue of other messages, with readable plaintexts, original source transcriptions, earlier credits and reproducible decryption evidence.

[This extension in detail](docs/extension-review-2026-11-02.md) · [Exact before/after inventory](experiments/session_review/README.md)

<!-- READING-CATALOG:START -->
## Browse by source page

[Open the complete page index](cases/pages/README.md). The page ranges below lead to short tables for each printed manuscript page, with each record's content, status and credit.

### The 22 challenge entries

These retain all original challenge identifiers. Page numbers alone do not identify a message: p198 is section D, while p198 B/C/E are separate records.

| Printed source pages | Entries | Challenge identifiers |
|---|---:|---|
| [pp. 50–74](cases/pages/050-074/README.md) | 1 | [p73](cases/p73.md) |
| [pp. 100–124](cases/pages/100-124/README.md) | 3 | [p100](cases/p100.md), [p105](cases/p105.md), [p109](cases/p109.md) |
| [pp. 125–149](cases/pages/125-149/README.md) | 2 | [p132](cases/p132.md), [p146](cases/p146.md) |
| [pp. 150–174](cases/pages/150-174/README.md) | 8 | [p152](cases/p152.md), [p153a](cases/p153a.md), [p153b](cases/p153b.md), [p158](cases/p158.md), [p164a](cases/p164a.md), [p164b](cases/p164b.md), [p170](cases/p170.md), [p171](cases/p171.md) |
| [pp. 175–199](cases/pages/175-199/README.md) | 6 | [p176a](cases/p176a.md), [p176b](cases/p176b.md), [p187](cases/p187.md), [p187b](cases/p187b.md), [p189](cases/p189.md), [p198](cases/p198.md) |
| [pp. 200–224](cases/pages/200-224/README.md) | 2 | [p215](cases/p215.md), [p217](cases/p217.md) |

### Other ciphertexts — 577 reviewed records

Multipart messages and repeated transmissions have separate source records even when they share a case page. Direct readings, source-supported reconstructions and conjectural repairs keep their stated limits in the detailed page tables.

| Printed source pages | Reviewed records | Pages represented |
|---|---:|---:|
| [pp. 50–74](cases/pages/050-074/README.md) | 40 | 17 |
| [pp. 75–99](cases/pages/075-099/README.md) | 63 | 25 |
| [pp. 100–124](cases/pages/100-124/README.md) | 85 | 25 |
| [pp. 125–149](cases/pages/125-149/README.md) | 71 | 25 |
| [pp. 150–174](cases/pages/150-174/README.md) | 95 | 25 |
| [pp. 175–199](cases/pages/175-199/README.md) | 88 | 24 |
| [pp. 200–224](cases/pages/200-224/README.md) | 107 | 25 |
| [pp. 225–249](cases/pages/225-249/README.md) | 28 | 6 |

The catalogue covers source-reviewed records with published reading evidence; the wider OCR search pool contains additional unreviewed ciphertext candidates. Earlier authors retain their credits. Current source review and new research use **icekylinx and GPT-6 Astra Pro**; a review credit does not assert first-decipherment priority.
<!-- READING-CATALOG:END -->

## Selected results

The [accounting-copy reconciliation](experiments/accounting_copy_reconciliation/README.md) restores two unresolved labels in p175 from an independently received p172 companion. Its conservative reading reaches 100/102 fixed positions with the original four observed-coordinate changes; the ending disagreement and shared word repairs remain explicit.

Latest source additions include a [third silk-resale continuation](cases/finance/nov6_silk_resale_continuation.md), a [Sevastopol food-dispatch list](cases/caucasus/sevastopol_supply_dispatch.md), and a [two-part request to stop further provisions](cases/military/nov25_provisions_and_evening_report.md). Their original quantities, reference labels and message boundaries remain explicit.

Other recent recoveries include the [second part of Mackensen’s withdrawal report](cases/military/mackensen_withdrawal_part2.md), [independent Ringbahn instruction copies](cases/radio/nov6_ringbahn_key_witnesses.md), and the [Siegfried cancellation order](cases/people/siegfried_assignment_cancellation.md). Each keeps its raw output, explicit reconstruction costs and earlier credits.

<details>

<summary>Selected recoveries and source editions</summary>

- **[Post-publication source-recovery inventory](experiments/post_push_review/README.md):** the continuing review preserves its own starting catalogue, per-package source counts, exact artifact hashes and independent PDF-pixel checks. The [repository map](docs/repository-map.md) explains the six reading topics and stable earlier URLs.
- **[Restored multipart readings](cases/military/orient_intelligence.md) and [military allowances](cases/finance/military_allowances.md):** correcting source transcription and printed part boundaries recovers 730 readable positions from previously broken OCR frames without changing any observed coordinate. The full editions retain received spellings, numerical labels and reported-event qualifications.
- **[Crown airlift](cases/finance/crown_airlift.md), [ZITAG purchase orders](cases/finance/zitag_purchase_orders.md), [Liman troop reports](cases/military/liman_troop_reports.md), [intendant responsibilities](cases/military/military_intendant_remit.md) and [Neuhof demobilization](cases/military/neuhof_demobilization.md):** further source editions preserve exact repair costs, competing gap placements and the explicitly unread part of the damaged Neuhof message.
- **[Corcovado sale terms](cases/naval/corcovado_sale_terms.md) and [Turkish tonnage purchases](cases/naval/turkish_tonnage.md):** nine parts describe a proposed ship sale, immediate cash, seizure risk, interest, German resale rights and evacuation use. A later telegram spells out the Marineamt office number; cross-key propagation preserves both the useful reference constraints and an inconvenient resulting garble. The separate [Black Sea cargo edition](cases/naval/black_sea_shipping.md) retains the Lasry team's earlier supply-message body credit.
- **Money and banknotes:** the [lei-note redemption instructions](cases/finance/lei_note_exchange.md) and [Arad crown-cash requests](cases/finance/crown_cash_requests.md) add six parts on stamped notes, banking arrangements, advances and a severe banknote shortage. Complete amount and reference pairs are mapped back to the scan; their raw numerical labels remain unassigned.
- **[German civilians in Constantinople](cases/people/constantinople_civilians.md):** four parts ask the Swedish legation to verify reported departures and describe an appeal to the Supreme War Council. Contemporary diplomatic texts independently corroborate that appeal and routing. The numerical headcount remains the literal `0YY`; competing missing-coordinate frames and every word repair are retained.
- **[Polish representation in Tiflis](cases/caucasus/tiflis_appointment.md):** three parts link forwarding via General von Kress to an appointment for Waclaw v. Ostrowski. Name-masked screens locate a displaced group and a missing group; an independently attested Tydelski identity supports a separate conditional Y assignment, without changing the published squares.
- **October personnel, supplies and radio traffic:** the [Caucasus correspondence](cases/caucasus/october_caucasus.md), [staffing orders](cases/caucasus/october_staffing.md), and [routing/weather requests](cases/caucasus/october_requests.md) cover 22 source parts. Readable material includes the 4th Bavarian Cavalry Brigade appointment, Grundherr's replacement assignment, suspended manganese purchases, Westernhagen's return and funds for Kress. Heavily damaged or technical passages stay provisional or unasserted.
- **[Boots and clothing for Oderberg](cases/military/p191_A.md):** one displaced five-coordinate group restores the second part, with 196/200 positions fixed after explicitly costed repairs. All single-group moves and a fresh control are checked. A primary 1917 Breslau decree supports only a separate optional one-coordinate unit emendation. The [Siedlce withdrawal report](cases/military/p200_A.md) receives an independently corroborated von Zedlitz signature, while an unlocated battalion remains unlocated.
- **Repeated messages recover missing text.** The [November 14 copies](cases/radio/nov14_radio_retransmissions.md) restore 85 missing prefix coordinates and support relay wording across different keys. [Warsaw service traffic](cases/radio/warsaw_service_messages.md) distinguishes checked and unchecked messages. Earlier [Munich](cases/radio/courier_munich.md), [Kremp](cases/people/kremp.md), [Osthoff](cases/people/osthoff.md) and [Glatz](cases/people/glatz.md) source families keep their own evidence and limits.
- **[Late key-sharing instructions](cases/radio/late_november_cipher_instructions.md):** two complete parts explicitly agree on the BSL–UKS key while preserving all 320 coordinates. Related notices document missing December tables and unreadable ITOCHI traffic. The separate [Ringbahn schedule](cases/radio/p211_key_schedule.md) instructs December reuse of November keys; an instruction alone does not prove compliance.
- **Earlier project recoveries remain available:** the shared 18-column [p153 partial decipherment](cases/p153a.md), its [ammunition-report continuation](cases/p153b.md), [p205 finance and naval administration](cases/finance/p205_A.md), and the [courier, Helsinki and personnel editions](experiments/corpus_recovery/README.md). Their raw positions, conditional fills, numbers and source dates remain explicit.
- **Prior readings receive source editions and exact repair accounts.** These include the [naval armistice order](cases/naval/naval_armistice_order.md), [Kiel radio-control order](cases/radio/kiel_radio_control.md), [Mackensen internment letter](cases/military/mackensen_internment.md), [Feigenhaus instruction](cases/naval/p120_p123.md), and [Seifert traffic](cases/radio/seifert.md). The Childs, Lasry-team and other earlier body credits are retained; a [bounded attribution audit](experiments/p170_new_methods/lasry_attribution_audit.md) distinguishes body readings from key or header references.

</details>

Among the 22 challenge entries, three remain wholly open: **p73, p170, p198**. A source-linked recovery or contextual reading is not counted as an independently solved original ciphertext.

New [word/loss searches](experiments/p198_word_search/README.md), [radio-language controls](experiments/radio_domain_model/README.md), [p73 source-reuse retrieval](experiments/p73_new_methods/README.md), and [p170 square/rank and group-move tests](experiments/p170_new_methods/README.md) retain every completed scope and failed control. Model scores can favor wrong words or numerals; exact source roundtrips establish compatibility, not historical identity.

All current source reviews, arithmetic audits, and new editorial work are by **icekylinx and GPT-6 Astra Pro**. The tables credit the earlier public reading or the present recovery/review named in that row. Each case gives the most likely readable text, its meaning, and unresolved details.

## Review coverage

The [review ledger](data/review_ledger.json) currently records **104 claims and provenance checks**. It includes the 2017 comment history, earlier square completions, p217's published key images and naval corroboration, p176b's French documentary context, the newly checked October 2026 submissions, and the historical reading of p158's component.

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

- [cases/](cases/README.md): Page-number indexes and six topic guides, with canonical source editions grouped by subject
- [docs/repository-map.md](docs/repository-map.md): Reading routes, directory responsibilities, stable evidence locations and navigation maintenance
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
