# Research status

**icekylinx and GPT-6 Astra Pro · 3 November 2026**

[Read the messages](../cases/README.md) · [Page index](../cases/pages/README.md) · [Methods](methods.md) · [Experiments](../experiments/README.md) · [Source images](../sources/reviewed-crops.md)

## Established contributions

**We recovered a new shared key and partial plaintext for the two p153 CHI fragments, built a source-reviewed edition across the wider collection, and developed exact reconstruction tools for damaged traffic.** Earlier decipherments and keys are credited in their individual cases.

The [whole-material census](whole-material-coverage.md) registers **679 ciphertext bodies on 175 printed log pages**. The live [page index](../cases/pages/README.md) gives the reviewed catalogue; the census lists the remaining source gaps and independently recomputes supported frame and label counts. The [twelve instructional examples](../experiments/childs_instructional_examples/README.md) are fully reproduced separately.

| Contribution | Established result | Evidence |
|---|---|---|
| New p153 key and partial decipherment | Shared 18-column key with nineteen ordinary-letter cells; part 5 fixes 60/66 positions without source changes. Part 6 fixes 33/54 raw positions and has an explicitly repaired 50/54-position template. | [Recovery](../experiments/p153_recovery/README.md), [part 5](../cases/p153a.md), [part 6](../cases/p153b.md) |
| Exact p153 validation | Every integer width from 14 through 26 is checked over 3,492,604 length-class layouts; only width 18 fits the sixty-letter crib. The width-18 check leaves two equivalent partial-key representations. | [Even widths](../experiments/p153_even_widths/README.md), [odd widths](../experiments/p153_odd_widths/README.md), [independent crib checks](../experiments/p153_crib/README.md) |
| Restored source frames | Correct transcription and printed part boundaries recover 487 direct positions in the Orient report and 243 in the allowances report without changing observed coordinates. The complete editions fix 1,009/1,010 and 877/880 raw positions respectively. | [Orient intelligence](../cases/military/orient_intelligence.md), [military allowances](../cases/finance/military_allowances.md) |
| Independent-copy recovery | November 14 copies restore an 85-coordinate missing prefix. Silk-resale witnesses jointly supply native pair support for all 135 continuation positions; the Seifert arrival copies support all 37 positions. | [Retransmissions](../cases/radio/nov14_radio_retransmissions.md), [silk resale](../cases/finance/nov6_silk_resale_continuation.md), [Seifert](../cases/radio/seifert.md) |
| Exact damaged-text optimization | Multi-witness dynamic programming covers all `2^42` minimum-cost p109 readings. Joint scattered-loss optimization covers 8,670,506,592,384 five-loss witnesses per fixed complete key. | [Multi-witness decoder](../experiments/parallel_decoder/README.md), [joint loss decoder](../experiments/p198_joint_exact/README.md) |
| Exact p198 category frontier | All 40,320 completions of the declared partial key are covered. An 85-character reading with three digits requires at least thirteen Q/Y positions; a Q/Y-free reading requires at least ten digits. | [Frontier and attaining witnesses](../experiments/p198_category_frontier/README.md) |
| Source and attribution review | Original scans, keys, earlier readings, corrections and explicit repair ledgers are assembled into one navigable edition. The latest 40 source crops are published with file and RGB hashes. | [Review ledger](../data/review_ledger.json), [source images](../sources/reviewed-crops.md), [reading conventions](reading-conventions.md) |

## Current source refinements

The cases contain the full readings and exact repair accounts. These recent examples show how source review and independent witnesses improve recovery.

| Edition | Result |
|---|---|
| [p136 Gokieloff glyph correction](../experiments/p136_source_glyph_correction/README.md) | The printed `XAFFF` corrects the earlier transcription `XAFFX`, restoring raw `ZU DORT` with zero additional historical repair cost. |
| [p105 combined-source supplement](../experiments/p105_optional_two_deletions/README.md) | A 288-slot proposal yields 144 paired labels with two source exclusions and three observed-coordinate substitutions. All 12 full-word minima and 55 prefix minima are retained. |
| [p109 duplicate-pair supplement](../experiments/p109_optional_duplicate_pair/README.md) | An independent received copy constrains minimum alignments and preserves the `SAVE`/`SAVA` alternatives with their exact costs. |
| [Accounting-copy reconciliation](../experiments/accounting_copy_reconciliation/README.md) | The p172 companion resolves two additional p175 labels, reaching 100/102 fixed positions with the existing four substitutions. The final-label disagreement remains visible. |
| [Eilvese traffic schedule](../cases/radio/nov3_eilvese_traffic_schedule.md) | A complete 176-position conditional body follows a ten-slot exclusion and three substitutions. Eight no-fill exclusion maps give the same stream. |
| [Thirty-million-crown airlift request](../cases/finance/nov9_crown_airlift_and_embassy.md) | Four native parts yield 311/312 fixed raw positions, with one substitution and one invalid-glyph fill in the edited reading. |
| [Serbian-cavalry report witness](../cases/military/nov8_serbian_cavalry_parallel.md) | The p170 copy supplies p158’s missing A; all 236 insertion boundaries give four tied minima and the same filled stream. Three of five word substitutions have raw-copy support. |
| [Operations-map request](../cases/radio/nov9_operations_map_sheets.md) | Source review restores the native 224-coordinate fragment and 108/112 fixed raw positions. |
| [Baku personnel inquiry](../cases/caucasus/baku_personnel_inquiry.md) | The duplicate-block reconstruction compares all 538 declared maps. Six minimum maps yield two distinct ciphertexts, with the alternatives recorded. |

The complete reading collection is organized into [Caucasus](../cases/caucasus/README.md), [naval](../cases/naval/README.md), [military](../cases/military/README.md), [radio](../cases/radio/README.md), [finance](../cases/finance/README.md) and [personnel](../cases/people/README.md) guides. The [post-publication inventory](../experiments/post_push_review/README.md) records the source packages and their counts; the earlier [extension report](extension-review-2026-11-02.md) and [initial inventory](../experiments/session_review/README.md) retain their own publication snapshots.

## Open challenge targets

**p73, p170 A and p198 D remain wholly open.** Other challenge entries have prior readings, new partial recovery or source-linked reconstructions, with the exact status in each case.

| Target | Present constraint | Next useful evidence or method |
|---|---|---|
| [p73](../cases/p73.md) | Date layers conflict; source reuse, square-component reuse and exact substitution-invariant retrieval have been screened. | A longer same-key companion or original dated radiogram. The [archival follow-up](../experiments/p73_primary_followup/ARCHIVE_ACCESS.md) identifies primary-source routes. |
| [p170 A](../cases/p170.md) | Truncation geometry remains unresolved. Recorded square/rank reuse and displaced-group attacks have calibrated controls. | A source-supported original length, missing-prefix boundary or overlapping reception. See [current methods](../experiments/p170_new_methods/README.md). |
| [p198 D](../cases/p198.md) | Exact searches cover their declared fixed-key scopes. Individual-position feasibility remains broad under the five-loss model. | Joint constraints from an authenticated companion, source-supported loss locations or independent plaintext. See [domain witnesses](../experiments/p198_letter_bounds/domain_witnesses.json) and [word/loss search](../experiments/p198_word_search/README.md). |
| [p153 unresolved fields](../experiments/p153_extension/README.md) | The recovered square couples date, serial and part-6 footer cells. | An independently established field or companion part that fixes one shared cell across both fragments. |

## Method results guiding the next attacks

Independent copies and source-frame corrections have produced the strongest recovery gains. Continue joining native repeated transmissions and cross-key plaintext overlaps, then propagate supported coordinate or square constraints through every linked record.

Language optimization has measured strengths and failure modes. The [word/loss campaign](../experiments/p198_word_search/README.md) completed 49 jobs, including 18 controls on nine distinct bodies: 12 exact recoveries, five wrong candidates that outrank truth, and one search failure despite a better true score. The [radio model](../experiments/radio_domain_model/README.md) improves hidden-rank recovery from 2/6 to 5/6 on its six full-square controls; with partial squares and five losses, both models recover 1/6 exactly. Further scoring work should target the demonstrated word and numeral errors using fresh control bodies.

The [digit-symmetry audit](../experiments/radio_domain_model/digit_symmetry/README.md) identifies why a correct class sequence can leave hundreds or millions of literal digit assignments tied. The [six-gram controls](../experiments/p198_joint_six/README.md) recover one planted full text and its loss mask, while another control has a higher-scoring wrong competitor. These results direct the next method toward shared evidence and equality constraints.

New editions follow the [reading conventions](reading-conventions.md): source, key and geometry; raw and edited output; exact edits and unresolved fields; prior credit; and a reproducible re-encryption witness. The [verification workflow](../.github/workflows/verify.yml) checks the accepted evidence and compact search certificates.
