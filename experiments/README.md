# Experiments and source verification

[ADFGVX Cipher](../README.md) · [Readable cases](../cases/README.md) · [Methods guide](../docs/methods.md)

The joint width-18 search produced a **new substantial partial reading of p153a/p153b**. This index also covers source recoveries, editorial checks, exact optimization and searches that yielded no accepted plaintext. A failed heuristic search does not exclude a key or corruption model. The source and edit certificates in `../data/` remain separate from language-ranked candidates.

**Browse:** [Sources and readings](#readings-parallels-and-source-review) · [p153](#p153-recovery-and-exact-constraints) · [Exact optimization](#exact-optimization-of-damaged-texts) · [Open targets](#open-target-searches-and-calibration)


## Readings, parallels and source review

| Experiment | Scope | Calibration and limit |
|---|---|---|
| [Source-reviewed corpus readings](corpus_readings/README.md) | Nine source parts, two assembled multipart messages and one exact repeated suffix | Separate raw and editorial layers; p123 deletion aliases exhaustively checked for the stated candidate; p218 treaty context does not replace source evidence. |
| [Osthoff and Glatz parallel witnesses](corpus_attack/SOURCE_FAMILIES.md) | Six source records, 407 candidate plaintext positions | 403 positions have complete coordinate-pair support; three emendations and one damaged-glyph fill remain explicit. |
| [p205 financial and naval orders](corpus_joint/README.md) | Two messages in six parts; 1,514 source coordinates | 750/757 raw positions fixed; four editorial substitutions; six reference positions remain unknown. |
| [Station control, Seifert and operational reports](p170_continuation/README.md) | Fifteen source records, 2,161 slots; a 20-coordinate prefix supplied by a repeat | Independent arithmetic, conservative source unions and separate historically supported unit identification; both cipher-only digit alternatives retained. |
| [Munich courier reconstruction](courier_recovery/README.md) | Five witnesses, direct 67/68-position continuation, and all minimum fits of two first-part damage models | 118/134 first-part positions have unchanged-pair support across both conditional models; association, names and numeral inference remain qualified. |
| [Cross-key witnesses and conditional digit recovery](open_targets_continuation/README.md) | Fourteen parts, 3,084 slots and 1,490/1,542 direct positions; Kremp, Warsaw, key schedule and order references | Exact source repair costs, independent-key overlaps and separate FD=8 / VA=5 assumptions; no base-key mutation or first-decipherment claim. |
| [p187b adjacent-coordinate repair](p187b_adjacent_swap/README.md) | All 141 adjacent swaps under the published partial key | One swap explains both of Norbert's 2017 word corrections; 140 coordinates remain unchanged and all seven ending unknowns remain. |
| [All-target source retrieval](source_similarity_extension/README.md) | All 22 challenge entries against 788 OCR blocks; 17,336 comparisons | Established parallels recur; same-page self matches are shown separately, and new local candidates remain distinct from source evidence. |
| [p73 primary-source follow-up](p73_primary_followup/README.md) | Late-period Kress memoir, Lepsius documents 439–444 and the institutional Kress-name search | No matching incoming radiogram found in the inspected scopes; an apparent date match belongs to 1917. |
| [Additional transport parallels](transport_followup/README.md) | Four p197/p198 witnesses, all gap/dash alignments and linked number fields | Independent source maps and attainable edit minima; no new historical digit or p198 D solution. |
| [Direct source-similarity retrieval](source_similarity/README.md) | 26,792 comparisons across 788 OCR blocks, with whole-query and local alignment | Established and seeded parallels rank first; image review of each open target's best hit establishes no additional parallel. |
| [p215 Corps Kosch interpretation](p215_context/README.md) | Explicitly costed readable segment and contemporary command/naval context | Two known changes for KORPSXKOSCH versus five for KORPSFRISCH; the broader 92-character segment needs nine changes and fifteen fills. |
| [Additional source and attribution checks](source_followup/README.md) | p77/p134 contextual readings, p109 transcription, p132 prior credit, p186 suffix constraints | Source images reviewed; exact arithmetic and a complete nine-deletion suffix obstruction. |
| [Source-guided recoveries](source_recovery/README.md) | p146 literal duplicate deletion; p109 same-page near-parallel | All retained p146 coordinates preserved; p109 editorial disagreements explicitly counted. |
| [Editorial reading audit](editorial_review/README.md) | p109, p132, p146 same-length readable proposals | Full change maps; Norbert's 2017 VORHER interpretation retains priority. |

## p153 recovery and exact constraints

| Experiment | Scope | Calibration and limit |
|---|---|---|
| [p153 recovered key and text](p153_recovery/README.md) | Blind candidate, complete lineage, nineteen-letter core square, raw and emended layers | Dates and numbers unassigned; twelve erasure fills and two explicit emendations for the proposed part-6 body. |
| [p153 linked footer and date constraints](p153_extension/README.md) | Shared-cell identities, exact date/serial and footer domains, 23 recorded-square exclusions | Full conditional template; 50/54 part-6 positions only under the existing repair and separator hypotheses. No new source-fixed digits. |
| [p153 key construction and phrase search](p153_key_structure/README.md) | Exact shared-keyword exclusions; 724,720 dictionary entries and 8.72 million corpus letters | 128 generated construction controls pass; natural p217 keyword hits calibrate phrase retrieval. The bounded negative results do not complete p153. |
| [p153 exact conditional check](p153_crib/README.md) | Every width-18 segmentation and compatible key for the sixty-letter first crib | Independent C and Python enumerators agree: two equivalent partial keys, both with the same two body contradictions. |
| [p153 even-width validation](p153_even_widths/README.md) | All 2,853,839 segmentations across even widths 14 through 26 | Only width 18 admits the sixty-letter first crib; seven fresh controls and separate exclusion proofs pass. |
| [p153 odd-width validation](p153_odd_widths/README.md) | All 638,765 segmentations at odd widths 15 through 25 | No compatible first-crib key; a separate component-variable solver handles row-crossing digraphs and passes fresh controls. |
| [p153 recovered-component follow-up](p153_followup/README.md) | Canonical blind replay, 36 new-rank fits, direct source checks and digit-convention test | The discovery trace reproduces byte for byte; no additional historical text or numeral is accepted. |
| [p153 recovered-square follow-up](p153_anchored_followup/README.md) | Six arbitrary-rank fits at widths 18/19/20 plus one matched control | No historical reading; the control also fails, so square reuse is not excluded. Exact source/domain checks and the failure are retained. |
| [p153 corpus screen](p153_corpus/README.md) | 788 OCR-derived source blocks, 10,896 explicit models | Both discovery fragments recovered as controls; no additional coherent companion identified. OCR limits prevent exclusion. |
| [p153 independent header review](p153_headers/README.md) | Full-page OCR of printed pages 140–170, approximate call-sign retrieval and source-image checks | Finds the known fragments and rejects two false hits; OCR errors in the known control keep the negative result bounded. |
| [p153 joint search](joint_search/README.md) | All 900,900 width-16 and 18,564 width-18 length-class segmentations; bounded pairing and language searches | Width-18 component-column refinement recovers p153. Successful controls and earlier ordering, half-coordinate and pruning failures are retained. Enumeration of segmentations is not enumeration of keys. |
| [p153 alternative geometry](geometry/README.md) | 48 concatenation cases and 48 continued-column-phase cases over 24 reported keys | Source coordinates preserved; direct known-square checks only. One square has no attested cells and supplies no reading. |

## Exact optimization of damaged texts

| Experiment | Scope | Calibration and limit |
|---|---|---|
| [Exact scattered-loss geometry](p198_exact_sparse/README.md) | Every five-loss mask in a 170-coordinate frame under four fixed complete-key cases | Covers 1,115,034,284 masks; a true-key control exposes a marginal-score failure. No historical p198 reading. |
| [Exact joint loss placement and completion](p198_joint_exact/README.md) | All loss masks and six-valued fills in the same fixed-key regime | Covers 8,670,506,592,384 witnesses, including aliases; both true-key controls have wrong four-gram optima. Independent full-score and source verification. |
| [Model-free partial-square letter bounds](p198_letter_bounds/README.md) | All 40,320 Nov13–15b square completions and every five-loss placement/fill under its fixed ranks | Attainable extrema of 44–82 letters; at least three digits are required, which does not reject the historical key. |
| [Exact six-gram calibration](p198_joint_six/README.md) | Full joint loss/fill optimization with five-letter context under two objectives | Both recover the complete CHI13 control, mask and fills; a feasible wrong Nov13b competitor still beats truth, including under held-out books. |
| [Historical six-gram follow-up](p198_six_historical/README.md) | Every five-loss/fill witness under one frozen CHI13 square completion | A better six-gram optimum remains unreadable; 48 conditional partial-square singleton positions are not recovered historical letters. |
| [Exact category bound](p198_letter_bounds/CATEGORY_BOUNDS.md) | All Nov13–15b completions, fixed ranks and five-loss/fill witnesses | At least ten digits/Q/Y combined; an independent standard-library pairwise solver fully recomputes the optimum. |
| [Exact digit/Q/Y frontier](p198_category_frontier/README.md) | All 28 membership classes and every loss allocation, covering all 40,320 partial-square completions | Three digits require at least thirteen Q/Y positions; eight nondominated count pairs have full source witnesses and independent exact recomputation. |
| [Exact multi-witness decoding](parallel_decoder/README.md) | p109, two language objectives, full/body-only scopes, seven exact edit budgets | No plaintext crib or beam; 280 candidates independently re-encrypt. Agreement and unresolved alternatives are separated from source-fixed letters. |
| [p215 conditional completions](p215_completion/README.md) | Exact top ten under each of three additive language objectives | All 237 known source coordinates preserved; the 6^21 source-compatible strings remain cryptographically unresolved. |
| [p185 D gap ranking](known_key/README.md) | All 194 positions of a five-coordinate gap | Both complete rankings reproduce; their preferred positions differ. The arithmetic certificate retains every geometry. |

## Open-target searches and calibration

| Experiment | Scope | Calibration and limit |
|---|---|---|
| [Extended open-target attacks](open_targets/README.md) | Anchored squares, gap models, literal group transfer and independent coordinate-label permutations | Completed bounds, successful controls and failed calibration branches are retained; no new accepted plaintext. |
| [p73 coordinate-count diagnostic](open_targets/P73_HISTOGRAM.md) | Exact transposition-invariant counts and two held-out German books | Nov7–9 is an empirical mismatch under the tested prose conventions; a failed spacing convention and the historical positive control remain explicit. |
| [Fixed-rank and dictionary searches](fixed_search/README.md) | 144 fixed-rank cases, 1,352 dictionary-selected cases, 136 p198 refinements; completed counts are timestamped in the ledger | Exact input layers, model hashes, warm starts, and legacy limitations are retained. All three case families are complete in the final snapshot. |
| [Coordinate and geometry screen](fixed_search/README.md) | 20,666,880 evaluations across known squares, label permutations and readout conventions | A planted control ranks first; unchanged targets produce no accepted reading. |
| [Anchored squares](anchored_search/README.md) | Two of seventy planned historical cases completed before the p153 breakthrough | Both stronger-budget synthetic controls recover all observed coordinates; both weaker-budget failures remain available. |
| [Known-key truncation](known_key/P170_TRUNCATION_NOTE.md) | 1,291,584 p170 placements over 21 keys | Two implementation controls; upstream training overlaps a control body. A long-suffix control fixes no plaintext letters, so truncation is not excluded. |

## Reproduction and interpretation

Search budgets describe completed computations, not confidence levels. Models, controls, seeds, source hashes, exact solver versions, and dependencies are documented beside each experiment. Large corpora, generated model binaries and executables are excluded. Compact completed-case best fits are retained as explicitly unaccepted diagnostic records. The independent model builder reproduces its recorded hashes; the earlier upstream model is pinned separately because it contains previously solved traffic.

The [methods guide](../docs/methods.md) explains the evidence layers and why an exact language-score optimum can still be a wrong plaintext.

## Further source-reviewed messages

[Additional corpus recovery](corpus_recovery/README.md) preserves seven source records and five readable editions, with independent coordinate arithmetic and exact editorial repair costs.
