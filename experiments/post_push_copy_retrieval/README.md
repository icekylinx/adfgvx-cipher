# Literal-coordinate retrieval after publication

Prepared by **icekylinx and GPT-6 Astra Pro**.

This frozen search compares the **113 newly reviewed physical records** in
28 source packages at public commit `d97c61b82d45a9ce2223a7363e128caae253846e`
against all **788 earlier OCR blocks**. It uses 26,745 literal reference slots
and 141,655 target slots. It does not search all 308 catalogue records and
does not substitute editorial repairs, inferred gaps or plaintext for the
received coordinates.

## Method and completed results

An exact ten-coordinate anchor is eligible only when every coordinate is
observed. Source masks are skipped, not treated as wildcards. A retained
pair must cover at least thirty distinct positions in each string. Overlapping
anchors contribute only their union of covered positions. Same-page matches
are preserved separately because a page may contain independent copies or
companions as well as self matches.

| Completed comparison | Result |
| --- | ---: |
| Eligible reference–target pairs | 89,044 |
| Pairs with at least one exact anchor | 222 |
| Exact anchor-position matches | 26,923 |
| Retained pairs | 169 |
| Retained cross-page pairs | 25 |
| Retained same-page pairs | 144 |
| Retained pairs after composition-preserving target shuffle | 0 |

The deterministic shuffle uses seed 20261103 and the identical retrieval
threshold. It is a calibration control, not a probability estimate or a
historical authentication test. Four predeclared known relationships are
recovered: DEUTZITAG p80/p81, Constanza p80/p82, Namur p171/p172, and the
truncated p212/p218 copy.

## Source follow-up

Seven cross-page retrieval pairs produced five body families for manual
review. The two p79 OCR fragments belong to one physical second part, so
the number of retrieval pairs is not the number of new records.

| Literal reference → OCR lead | Manually reviewed outcome |
| --- | --- |
| p125 A4 → p137 block 5 | [p137 B4](../../pages/137.md#edition-cases-military-armistice-clause-witnesses) independently supplies one previously masked coordinate. |
| p126 B → p137 block 6 | [p137 C](../../pages/137.md#edition-cases-military-armistice-clause-witnesses) repeats both earlier corrupt words; their repairs remain editorial. |
| p171 B1/B2 → p166 blocks 4/5 | [Newspaper dispatch copies](../../pages/166.md#edition-cases-radio-newspaper-dispatch-witnesses) preserve complementary evidence and three still unwitnessed editorial letters. |
| p83 B → p79 blocks 2/3 | [Palestine medical-unit dissolution](../../pages/079.md#edition-cases-military-palestine-medical-dissolution) supplies the earlier missing first-part context and an exact second-part copy. |
| p174 A3 → p195 block 1 | [Banknote completion](../../pages/195.md#edition-cases-finance-crown-banknote-completion) supplies nineteen absent coordinates while contradicting one earlier conjectural fill. |

The other eighteen cross-page pairs concern already reviewed DEUTZITAG,
ZITAG, Constanza, Namur and p212/p218 relationships. Every retained pair,
anchor position, coverage set, leading-offset mismatch and control result is
kept in [results.json](results.json). A leading anchor offset is only a local
retrieval aid: an added address may shift multiple transposition columns,
and OCR blocks may split or combine physical parts. It is not a global
alignment proof.

The search's `accepted_new_readings` remains empty deliberately. Acceptance
requires the separate source editions linked above; the retrieval result
alone establishes neither a message identity, a key nor historical wording.

## Reproduce

```sh
python experiments/post_push_copy_retrieval/retrieve.py --verify
```

The standard-library verifier checks all frozen source-package dependencies,
reconstructs the full search and shuffled control, and compares the complete
result. Inputs were frozen before the new source editions were written.
