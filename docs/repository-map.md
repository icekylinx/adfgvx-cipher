# Repository map

[ADFGVX Cipher](../README.md) · [Catalogue](../cases/README.md) · [Historical studies](historical-studies/README.md)

## Read the collection

| Start here | What it provides |
|---|---|
| [Historical showcase](historical-showcase.md) | A selection of recoveries with the greatest historical interest. |
| [Four historical studies](historical-studies/README.md) | Connected accounts of withdrawal, Black Sea shipping, material costs and individual lives. |
| [Topic guides](../cases/README.md#browse-by-topic) | An ordered reading path and complete index for each subject. |
| [Printed-page catalogue](../cases/pages/README.md) | One entry for each of the 679 physical ciphertext bodies. |
| [Seven OPEN sources](../cases/open/README.md) | The three original open challenges and four other unread bodies. |
| [Reading conventions](reading-conventions.md) | Page format, state labels, unknown text and repair accounts. |

The six subject folders under `cases/` are `caucasus`, `naval`, `military`,
`radio`, `finance` and `people`. The `open` folder holds the four wider unread
bodies and a guide to all seven open targets. Original challenge pages retain
their published paths directly under `cases/`; shared context and supplementary
pages retain their links. The short files under `cases/other/` preserve older
URLs and section anchors.

## Inspect the evidence

| Location | Purpose |
|---|---|
| [cases/](../cases/README.md) | Readable messages, historical explanation and local evidence links. |
| [data/reading_catalog.json](../data/reading_catalog.json) | Canonical source identifiers, states, detailed statuses, credits and case paths. |
| [data/reading_groups.json](../data/reading_groups.json) | Primary topic membership and related original challenges. |
| [data/topic_reading_paths.json](../data/topic_reading_paths.json) | Curated order and explanations for the topic guides. |
| [data/](../data/README.md) | Challenge transcripts, keys, prior readings and exact certificates. |
| [experiments/](../experiments/README.md) | Source-specific verifiers, supported reconstruction methods, controls and exact bounds. |
| [sources/](../sources/README.md) | Bibliography, historical sources and reviewed source images. |
| [adfgvx/](../adfgvx/) | Shared cipher arithmetic, source verification and index generation. |

A case links its supporting package. Its exact streams and repair ledger live
beside the verifier, with the inspected source crops. Historical evidence
aliases are distinct from catalogue entries: see the
[source identity rule](catalogue-source-identity.md).

## Maintain the edition

Add a new physical source once to the catalogue. Revise its existing entry
when a better reconstruction becomes available. Add a source page to its
subject folder, or to `cases/open/` if it has no accepted body reading. Then
regenerate the page and topic guides:

```sh
python -m adfgvx.catalog
python -m adfgvx.navigation
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python data/reviews/check_reading_presentation.py
python -m adfgvx.verify
```

The checks enforce unique source identities, valid states, topic coverage,
working links and current evidence labels. Source-specific checks in the
[workflow](../.github/workflows/verify.yml) verify the readings themselves.
Old layout snapshots are retained in Git history rather than duplicated in
the current edition.

[Research status](research-status.md) · [Material census](whole-material-coverage.md) · [Publication history](publication-history.md)
