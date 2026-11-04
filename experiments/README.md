# Experiments and source verification

**icekylinx and GPT-6 Astra Pro** · [Read the messages](../cases/README.md) · [Research status](../docs/research-status.md) · [Methods](../docs/methods.md)

Our experiments recovered the shared p153 key, reconstructed damaged transmissions from independent copies, and established exact bounds for the hardest source models. This guide highlights the results and the tools behind them. The [page catalogue](../cases/pages/README.md) lists every source edition and links its complete evidence package.

## Readings, parallels and source review

### Latest source editions and follow-up methods

| Result | Evidence |
|---|---|
| **Original p164a occupation-army fragment** — BESATZUNGSHEER matches 18 observed halves at zero substitutions; revised prior clauses give 104/121 positions with four substitutions | [Cross-key native witnesses and exact word layers](p164_occupation_fragment/README.md) |
| **Personnel-removal governing clause** — p137 A5 reaches an optional 124/126 positions, retaining two unknowns and all repair prices | [Date marker and military-movement proposal](p137_governing_clause/README.md) |
| **German field-post fragment** — p84 C gains a 28/122-position conditional word layer at zero observed substitutions; five source frames and three wholly missing word letters remain explicit | [Source, corpus phrase search and calibrated replay](p84_field_post_fragment/README.md) |
| **Withdrawal report ending** — p116 A13 has a 90/111 route-and-approval proposal; optional shared footer format and historical closing extend it to 97 and 101/111, with zero observed substitutions | [Route and approval](p116_optional_route_fragment/APPROVAL.md), [separate footer layers](p116_optional_route_fragment/FOOTER.md) |
| **Cross-key withdrawal parallel** — 59 letters in p117 C3 support two existing p124 A1 repairs | [Independent observed-source witness](hungarian_armistice_instructions/withdrawal_parallel.json) |
| **Demobilization continuation** — p228 B2 reaches 121/132 positions, or optionally 123/132 using two reference-field fills from part 1 | [Mask relocation and cross-part reference](p228_demobilization_fragment/README.md) |
| **Weisskirchen halt and security fragment** — p154 A2 rises from 36/81 raw to 56/81 with two substitutions and 20 added-slot fills, after one explicit observed-coordinate exclusion | [Source frame and independent review](p154_weisskirchen_fragment/README.md) |
| **Full Munich routing witness** — p168 C fixes 139/140 raw positions; a p159 coordinate fills the last slot and p168 independently supports GEN KDO | [Joint source certificate](p168_munich_routing_witness/README.md) |
| **Breslau horseshoe and nail dispatch** — p215 A has 176/196 raw positions and a 192/196 primary word proposal; alternatives retain the numerical uncertainty | [Dispatch and frame alternatives](p215_breslau_dispatch/README.md) |
| **Divisional positions and railway departure** — p215 B3 has 88/117 raw positions and a 109/117 word proposal, with inherited global J/Y evidence | [Positions and Ruttka–Teschen fragment](p215_third_positions_fragment/README.md) |
| **Hospital and transport fragment** — 129/151 primary positions; optional extension 148/151 at 102 missing-half fills; zero observed-coordinate changes in a conditional 302-slot frame | [p212 A4: all 197 observations retained](p212_medical_fragment/README.md) |
| **Captain-dispatch fragment** — 45 proposed positions mention a chief, a replacement detachment and dispatch; six tied source maps and all 432 primary completions retained | [p167 D: exact partial-word repair account](p167_captain_dispatch_fragment/README.md) |
| **Original p215 closing field** — shared Hungarian Y and the earlier J/numeral hypotheses reduce 90 possibilities to 56, with complete globally consistent witnesses | [Shared-cell propagation across 26 bodies](p215_hungarian_y/README.md) |
| **Station-staff query** — 68/69 positions; all five minimum source maps independently reproduced | [p137 B: 481,032 models](p137_station_staff_query/README.md) |
| **Provision-train completion** — 84/84 positions with one extra mask fill supported by the next part | [A5/A6 joint reading](p176_verpflegs_joint_completion/README.md) |
| **Kiev unrest and soldiers’ council neutrality** — 139/147 positions with zero observed substitutions after resolving printed group alternatives | [p219 C: all 81 source maps](p219_kiev_unrest/README.md) |
| **Wheat-shipping price query** — 118/122 positions, with vessel and quantity alternatives retained | [p198 A: 2,700 maps and 432 completions](p198_shipping_query/README.md) |
| **Technical and transport fragments** — direct-current machines, coal trains via Klausenburg, and further train departures | [p71 A2](p71_dc_machines_fragment/README.md), [p176 A6](p176_coal_train_fragment/README.md), [p215 B1](p215_train_departure_fragment/README.md) |
| **Crossing report, receipt and mission address** — three separately priced partial editions | [p152 A2](p152_crossing_fragment/README.md), [p164 D](p164_acknowledgment/README.md), [p167 C1](p167_mission_address/README.md) |
| **Arad copy restores eleven lost coordinates**, including native support for 80000 MANN | [694,320 source-only maps](danube_arad_witnesses/README.md) |
| **Romanian ultimatum evening report** — complete 98-position body under eight tied source maps | [Exact reconstruction](nov11_romanian_ultimatum_report/README.md) |
| **Third Ringbahn-key reception** — 84 additional directly witnessed coordinates | [Cross-copy recovery](nov13_ringbahn_retransmission/README.md) |
| **Budapest teleprinter report** — all 176 native coordinates, with an intact 51-label report-transmission sentence | [Source edition](nov24_budapest_report/README.md) |

The [21-source audit](../docs/source-gap-audit.md) records the fresh transcriptions, boundaries and PDF pixel recipes used in this campaign. The [whole-material census](../docs/whole-material-coverage.md) tracks current collection coverage.

### Earlier source editions

The [page index](../cases/pages/README.md) is the complete reading catalogue. Each edition contains its source, earlier attribution, raw output, edited text and reproducible repair ledger. The [initial inventory](session_review/README.md) and [post-publication inventory](post_push_review/README.md) retain their dated publication snapshots.

## p153 recovery and exact constraints

| Result or method | Evidence |
|---|---|
| **New shared 18-column key and partial decipherment** | [Recovery and discovery lineage](p153_recovery/README.md), [joint search](joint_search/README.md) |
| **Only width 18 fits the sixty-letter crib across widths 14–26**; 3,492,604 length-class layouts checked | [Even widths](p153_even_widths/README.md), [odd widths](p153_odd_widths/README.md) |
| **Two equivalent partial-key representations**, independently enumerated | [C and Python crib checks](p153_crib/README.md) |
| Linked date, serial and footer cells across both parts | [Global constraints](p153_extension/README.md) |
| Keyword construction, phrase retrieval and companion search | [Key structure](p153_key_structure/README.md), [corpus screen](p153_corpus/README.md), [source headers](p153_headers/README.md) |

## Exact optimization of damaged texts

| Result or method | Evidence |
|---|---|
| **All `2^42` minimum-cost p109 readings** optimized without a plaintext crib | [Multi-witness decoder](parallel_decoder/README.md) |
| **Exact p176a source-retention bound** — the earlier fixed proposal needs at least 68 substitutions with every slot retained, or 13 after excluding its final printed mask | [All optimal maps and independent programs](p176a_source_retention_bound/README.md) |
| **8,670,506,592,384 five-loss witnesses per fixed complete key**, including loss positions and fills | [Joint loss decoder](p198_joint_exact/README.md) |
| **At least ten digits/Q/Y combined** across all 40,320 Nov13–15b square completions under the fixed-rank five-loss model | [Exact bound](p198_letter_bounds/CATEGORY_BOUNDS.md) |
| **Eight-point digit/Q/Y frontier**; three digits require at least thirteen Q/Y positions | [Independent frontier verification](p198_category_frontier/README.md) |
| Longer-context exact optimization and loss before transposition | [Six-gram decoder](p198_joint_six/README.md), [pre-transposition loss](p198_pretransposition_loss/README.md) |
| p215 source-compatible completions and command interpretation | [Exact completion model](p215_completion/README.md), [Corps Kosch reading](p215_context/README.md) |

## Open-target searches and calibration

The original 22 challenges remain a research priority. **p73, p170 A and p198 D are wholly open**; the other challenge pages document recovered text and remaining fields.

| Target or shared tool | Current method record |
|---|---|
| **p73** | [Square/rank reuse, source retrieval and controls](p73_new_methods/README.md) |
| **p170 A** | [Truncated-source and radio-domain methods](p170_new_methods/README.md), [exact truncation scope](known_key/P170_TRUNCATION_NOTE.md) |
| **p198 D** | [Word/loss campaign](p198_word_search/README.md), [exact bounds and witnesses](p198_category_frontier/README.md) |
| Radio language models and hidden-rank recovery | [Frozen models and calibration](radio_domain_model/README.md), [digit symmetry](radio_domain_model/digit_symmetry/README.md) |
| Joint, anchored and fixed-component searches | [Joint engine](joint_search/README.md), [anchored search](anchored_search/README.md), [fixed search](fixed_search/README.md) |
| Copy retrieval and source reconciliation | [Source similarity](source_similarity/README.md), [source-guided recovery](source_recovery/README.md), [follow-up review](source_followup/README.md) |

## Reproduction and interpretation

Start with the shared verification and current indexes:

```sh
python -m adfgvx.verify
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
```

Each package supplies its exact inputs, verifier and reproduction commands. The [CI workflow](../.github/workflows/verify.yml) runs the full suite. Search controls, model hashes and completed scopes accompany the relevant engines; historical readings are established in the linked source editions, with their explicit repair prices.
