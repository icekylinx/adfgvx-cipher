# Research status

**icekylinx and GPT-6 Astra Pro · 3 November 2026**

[Read the messages](../cases/README.md) · [Page index](../cases/pages/README.md) · [Methods](methods.md) · [Experiments](../experiments/README.md) · [Source images](../sources/reviewed-crops.md)

## Established contributions

**A new shared key and partial decipherment are established for the two p153 CHI fragments.** The 18-column key fixes **60/66 positions** in [part 5](../cases/p153a.md) without changing a source coordinate. [Part 6](../cases/p153b.md) has **33/54 raw positions** and an explicitly repaired **50/54-position template**. Independent exact checks cover 3,492,604 length-class layouts across widths 14–26; only width 18 fits the sixty-letter crib. The [recovery package](../experiments/p153_recovery/README.md) links the discovery and validation evidence.

The [whole-material census](whole-material-coverage.md) registers **679 ciphertext bodies on 175 printed log pages** and distinguishes current catalogue coverage from unresolved source gaps. The [page index](../cases/pages/README.md) is the complete live reading catalogue. The [twelve instructional examples](../experiments/childs_instructional_examples/README.md) are reproduced separately, and the [21-source audit](source-gap-audit.md) preserves the latest transcriptions, boundary judgments and PDF pixel recipes. Earlier decipherments and keys retain their case-specific credits.

## Current source refinements

**Independent copies restore text that language scoring alone cannot establish.** The [Arad witnesses](../cases/military/danube_arad_witnesses.md) supply all eleven missing p159 coordinates and native support for **80000 MANN**; all eight surviving source maps produce one completed stream. The [Romanian ultimatum evening report](../cases/military/nov11_romanian_ultimatum_report.md) now has a complete 98-position body with an exact repair ledger and all eight minimum maps retained.

**Cross-part context also supports explicitly partial word proposals.** The [A6 coal-train fragment](../cases/military/p176_coal_train_fragment.md) reaches 48/80 positions without changing observed coordinates. Its continuation supports an optional one-mask [A5 VERPFLEGSZ completion](../cases/military/romanian_ultimatum_companions.md#optional-verpflegsz-completion), giving 84/84 positions. A6's routing field and tail remain unread. For the earlier [p176a proposal](../cases/p176a.md#source-retention-bound-for-the-earlier-proposal), a new exact bound quantifies its dependence on excluding the final printed mask: retaining every slot with ten insertions requires 68 observed substitutions; excluding that mask with eleven insertions reduces the bound to 13.

The [experiment guide's recent-results table](../experiments/README.md#latest-source-editions-and-follow-up-methods) links the other new editions, including the station-staff query, Kiev unrest, wheat shipping, technical and transport fragments. Individual cases hold the full readings, source images, repair prices and uncertainty records. The [post-publication inventory](../experiments/post_push_review/README.md), [earlier extension report](extension-review-2026-11-02.md) and [initial inventory](../experiments/session_review/README.md) retain their dated publication snapshots.

## Open challenge targets

**p73, p170 A and p198 D remain wholly open.** Other challenge entries have prior readings, new partial recovery or source-linked reconstructions, with the exact status in each case.

| Target | Present constraint | Next useful evidence or method |
|---|---|---|
| [p73](../cases/p73.md) | Date layers conflict; source reuse, square-component reuse and exact substitution-invariant retrieval have been screened. | A longer same-key companion or original dated radiogram. The [archival follow-up](../experiments/p73_primary_followup/ARCHIVE_ACCESS.md) identifies primary-source routes. |
| [p170 A](../cases/p170.md) | Truncation geometry remains unresolved. Recorded square/rank reuse and displaced-group attacks have calibrated controls. | A source-supported original length, missing-prefix boundary or overlapping reception. See [current methods](../experiments/p170_new_methods/README.md). |
| [p198 D](../cases/p198.md) | Exact searches cover their declared fixed-key scopes. Individual-position feasibility remains broad under the five-loss model. | Joint constraints from an authenticated companion, source-supported loss locations or independent plaintext. See [domain witnesses](../experiments/p198_letter_bounds/domain_witnesses.json) and [word/loss search](../experiments/p198_word_search/README.md). |
| [p153 unresolved fields](../experiments/p153_extension/README.md) | The recovered square couples date, serial and part-6 footer cells. | An independently established field or companion part that fixes one shared cell across both fragments. |

## Method results guiding the next attacks

Prioritize native repeated transmissions, source-supported loss geometry and linked square constraints. Exact searches resolve their declared scopes: the [p198 category frontier](../experiments/p198_category_frontier/README.md), for example, covers all 40,320 partial-key completions but leaves substantial word and digit ambiguity.

The [word/loss campaign](../experiments/p198_word_search/README.md) completed 49 jobs, including 18 controls on nine distinct bodies: 12 exact recoveries, five wrong candidates that outrank truth, and one search failure despite a better true score. The [radio model](../experiments/radio_domain_model/README.md) raises hidden-rank recovery from 2/6 to 5/6 on its full-square controls; with partial squares and five losses, both models recover 1/6 exactly. The next scoring improvement should address those demonstrated failures on fresh control bodies. [Digit symmetry](../experiments/radio_domain_model/digit_symmetry/README.md) explains why correct class sequences can still leave many literal assignments tied.

The [reading conventions](reading-conventions.md) and [verification workflow](../.github/workflows/verify.yml) keep source observations, word repairs, conditional interpretations and prior credit separate in every edition.
