# Evidence and research methods

[Historical results](../docs/historical-showcase.md) · [Read the messages](../cases/README.md) · [Research status](../docs/research-status.md) · [Method guide](../docs/methods.md)

Each accepted reading links a source-specific package: transcript, key or key
hypothesis, exact coordinate map, repair account and verifier. This index
selects the methods and source relationships that carry the current research.
The [catalogue](../cases/pages/README.md) is the complete index of individual
bodies; this page does not duplicate all 679 entries.

## Readings, parallels and source review

The most informative reconstruction often comes from another reception of
the same traffic. It can supply an observed coordinate where a single-copy
language guess would remain conjectural.

| Reconstruction | Evidence package |
|---|---|
| Arad provisions: eleven lost coordinates and the received 80,000 figure | [Two-way source maps and one completed stream](danube_arad_witnesses/README.md) |
| A 135-position silk-resale continuation | [Two receptions and their separate damage](nov6_resale_and_air_reconnaissance/README.md) |
| November 14 radio traffic with an 85-coordinate missing prefix | [Retransmission comparison](nov14_retransmissions/README.md) |
| Crown-airlift request completed by the later banknote copy | [Cross-copy source reconciliation](retrieved_copy_editions/README.md) |
| Munich routing and independent support for GEN KDO | [Near-complete native reception](p168_munich_routing_witness/README.md) |
| Romanian ultimatum report | [Source reconstruction](nov11_romanian_ultimatum_report/README.md) and [independent implementation](nov11_romanian_ultimatum_report/independent.py) |

### Latest source editions and follow-up methods

The [recent-partials table](../docs/research-status.md#recent-partial-reconstructions)
gives the current proposed readings and their limits. Three methodological
patterns recur:

- **Native word witnesses:** [p164 occupation-army wording](p164_occupation_fragment/README.md)
  and the [p89 guard-battalion continuation](p89_guard_battalion_extension/README.md)
  compare damaged spans with words actually observed under other keys.
- **Coupled passages:** the [p163 rearguard extension](p163_rearguard_continuation/README.md)
  tests one shared word across two received parts, preserving every equal-cost
  alternative and the unresolved numeral relation.
- **Sparse fragments with calibrated language search:** the
  [p163 infrastructure clause](p163_infrastructure_clause/README.md) and
  [p137 publicity fragment](p137_publicity_fragment/README.md) keep inferred
  geometry, wholly absent letters and competing meanings explicit.

The [AOK 11 map comparison](p163_headquarters_map_context/README.md) supplies
independent historical support for a place-name repair. It adds historical
context, not missing ciphertext coordinates.

## p153 recovery and exact constraints

| Question | Result and reproducible method |
|---|---|
| How was the key found? | [Recovery record](p153_recovery/README.md) and [joint square/rank search](joint_search/README.md). |
| Is the sixty-letter crib consistent with other widths? | [Even widths](p153_even_widths/README.md) and [odd widths](p153_odd_widths/README.md): only width 18 fits among widths 14–26, across 3,492,604 length-class layouts. |
| How many width-18 partial keys fit? | [Independent C and Python enumeration](p153_crib/README.md): two equivalent representations under the declared crib. |
| What remains linked but unread? | [Date, serial and cross-part cells](p153_extension/README.md). |
| Can the original key construction resolve the digits? | [Keyword and convention investigation](p153_key_structure/README.md), with its tested scope retained. |

## Exact optimization of damaged texts

| Method | What it establishes |
|---|---|
| [Multi-witness dynamic programming](parallel_decoder/README.md) | Exact ranking of all `2^42` minimum-cost p109 readings under the chosen language objective. |
| [p176a source-retention bound](p176a_source_retention_bound/README.md) | The earlier fixed proposal costs at least 68 substitutions with all slots retained, or 13 after excluding its last printed mask. |
| [Joint five-loss decoder](p198_joint_exact/README.md) | 8,670,506,592,384 loss-position/fill witnesses per fixed complete key. p198 D remains OPEN. |
| [Category and digit bounds](p198_letter_bounds/CATEGORY_BOUNDS.md) | Exact restrictions over all 40,320 completions of the stated Nov13–15b square. |
| [Category frontier](p198_category_frontier/README.md) | The trade-off between digit and Q/Y counts under that fixed-rank loss model. |
| [Crib consistency with source substitutions](substitution_crib_csp/README.md) | Joint unknown-square/rank constraints checked against exhaustive small oracles and hidden-key controls. |
| [Domain-constrained word search](p163_infrastructure_clause/domain_words_oracle.py) | An exact word/bigram recurrence checked on 660 exhaustive small cases. |

A mathematical optimum is a result about its stated model. It becomes a
historical reading only when the source, key and independent evidence support
that interpretation.

## Open-target searches and calibration

The [seven OPEN pages](../cases/open/README.md) give the literal inputs and
current questions. The maintained search families include:

| Approach | Record |
|---|---|
| Coordinate contacts and coincidence, with the same maximization applied to shuffled controls | [All-seven source diagnosis](open_target_contact_diagnosis/README.md) |
| Unknown-square and transposition search | [Joint engine](joint_search/README.md), [anchored search](anchored_search/README.md), [source-error consistency search](substitution_crib_csp/README.md) |
| Partial-key and truncation hypotheses | [p73](p73_new_methods/README.md), [p170](p170_new_methods/README.md), [p170 frame scope](known_key/P170_TRUNCATION_NOTE.md) |
| Loss models and longer-context scoring | [p198 word/loss search](p198_word_search/README.md), [six-gram optimization](p198_joint_six/README.md), [loss before transposition](p198_pretransposition_loss/README.md) |
| Independent-copy retrieval | [Source similarity](source_similarity/README.md), [source recovery](source_recovery/README.md), [follow-up](source_followup/README.md) |
| Language-model calibration | [Radio-domain model and hidden-rank controls](radio_domain_model/README.md) |

Completed older searches remain where a current result or dependency needs
them. Obsolete publication inventories and layout snapshots have been removed;
the current source and cipher checks are the maintained verification target.

## Reproduction and interpretation

```sh
python -m adfgvx.verify
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python data/reviews/check_reading_presentation.py
```

Each package supplies its focused command. The [CI workflow](../.github/workflows/verify.yml)
runs the maintained suite. [Source-evidence modes](../docs/source-evidence-modes.md)
distinguish a stored image check from replay against the original PDF.

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.
