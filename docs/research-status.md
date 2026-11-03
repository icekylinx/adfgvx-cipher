# Research status

**icekylinx and GPT-6 Astra Pro · 3 November 2026**

[Read the messages](../cases/README.md) · [Page index](../cases/pages/README.md) · [Methods](methods.md) · [Experiments](../experiments/README.md) · [Source images](../sources/reviewed-crops.md)

## Established contributions

**We recovered a new shared key and partial plaintext for the two p153 CHI fragments, built a source-reviewed edition across the wider collection, and developed exact reconstruction tools for damaged traffic.** Earlier decipherments and keys are credited in their individual cases.

The [whole-material census](whole-material-coverage.md) registers **679 ciphertext bodies on 175 printed log pages**. The live [page index](../cases/pages/README.md) gives the reviewed catalogue; the census lists the remaining source gaps and independently recomputes supported frame and label counts. The [twelve instructional examples](../experiments/childs_instructional_examples/README.md) are fully reproduced separately. The [21-source gap audit](source-gap-audit.md) preserves every fresh transcription, boundary judgment and original-PDF pixel recipe from this scan.

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
| [p176 A6 coal-train fragment](../cases/military/p176_coal_train_fragment.md) | A context-conditioned proposal reaches 48/80 positions from 14/80 raw with 44 printed-mask fills and zero observed changes. The routing field, later tail, N/X alternative and all 120 square completions remain explicit. |
| [p71 A2 direct-current machines](../cases/radio/p71_dc_machines_fragment.md) | A conditional 47/96-position technical clause fits all 43 surviving half-pairs in that span with zero observed changes and 51 added-slot fills. Both SCHALTEN/ERHALTEN alternatives and the unread 49-position remainder are retained. |
| [p219 C Kiev unrest](../cases/military/p219_kiev_unrest.md) | Parenthesized groups and the jamming boundary give 122/147 raw positions; seventeen added-slot fills yield a 139/147 zero-substitution word edition. All 81 models and four tied minima are checked; names have separate optional prices. |
| [p215 B1 train-departure fragment](../cases/military/p215_train_departure_fragment.md) | A conditional 220-slot frame gives 37/110 raw positions. Limited lexical fills yield 77/110 with no observed changes, retaining 33 unknowns and both source-glyph alternatives. |
| [p198 A wheat-shipping query](../cases/naval/p198_shipping_query.md) | A source-directed 244-slot model yields 111/122 raw positions; five observed substitutions, six printed-mask fills and one added-slot fill give 118/122. All 2,700 maps and 432 linked completions are retained. |
| [p152 A2 crossing fragment](../cases/military/p152_crossing_fragment.md) | The native frame gives 61/64 raw positions. The partial word proposal reaches 63/64 with seven observed substitutions and two mask fills; its negative wording is proposed, and the place and footer remain literal. |
| [p164 D acknowledgement](../cases/radio/p164_acknowledgment.md) and [p167 C1 mission address](../cases/radio/p167_mission_address.md) | Separate partial editions retain opaque references. The acknowledgement has 58/58 fixed raw positions; the address rises from 61/66 to 63/66 with six observed substitutions and two mask fills, preserving both global digit assignments. |
| [Romanian ultimatum evening report](../cases/military/nov11_romanian_ultimatum_report.md) | The restored 196-slot frame yields 85/98 raw labels and a complete 98-position body with two observed substitutions, ten source-mask fills and five added-slot fills. Both implementations retain all eight minimum maps. |
| [Danube and Arad witnesses](../cases/military/danube_arad_witnesses.md) | The p168 copy supplies all eleven lost p159 coordinates, raising 124→135/136 fixed labels; 80000 uses native pairs. Source-only comparison over 694,320 maps leaves eight origins yielding one completed stream. A p164 glyph correction restores UEBER and supports the parallel Danube passage. |
| [Third Ringbahn-key reception](../cases/radio/nov13_ringbahn_retransmission.md) | The p187 fragment adds 84 directly witnessed coordinates: 33/107 raw→106/107 linked labels; five observed substitutions and one printed-mask fill complete the 107-position part. |
| [Train and position report](../cases/military/nov24_train_report.md) | The conditional p217 B1 frame fixes 76/102 raw labels. Explicit lexical fills give 96/102 without observed-coordinate substitutions; the optional four-substitution layer reaches 99/102. All 400 maps per template are checked. |
| [p217 B2 Budapest teleprinter report](../cases/military/nov24_budapest_report.md) | All 176 native coordinates yield 88 fixed raw labels; the 51-label report-transmission sentence needs zero edits or fills. |
| [Thirty-million-crown airlift request](../cases/finance/nov9_crown_airlift_and_embassy.md) | Four native parts yield 311/312 fixed raw positions, with one substitution and one invalid-glyph fill in the edited reading. |
| [Serbian-cavalry report witness](../cases/military/nov8_serbian_cavalry_parallel.md) | The p170 copy supplies p158’s missing A; all 236 insertion boundaries give four tied minima and the same filled stream. Three of five word substitutions have raw-copy support. |
| [Operations-map request](../cases/radio/nov9_operations_map_sheets.md) | Source review restores the native 224-coordinate fragment and 108/112 fixed raw positions. |

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
