# Repository guide

[ADFGVX Cipher](../README.md) · [Historical research](historical-studies/README.md) · [Ciphertext pages](../cases/pages/README.md)

## Read the edition

| Part | Contents |
|---|---|
| [Printed-page editions](../cases/pages/README.md) | 175 dedicated Markdown files containing the ciphertexts, German readings, English meanings, source explanations and evidence. Every page number in the home-page table opens its edition directly. |
| [Historical studies](historical-studies/README.md) | Five investigations of withdrawal, shipping, finance, radio authority and practical departure, with a classified source guide. |
| [Chronology](historical-studies/chronology.md) | A cross-subject sequence distinguishing event, origin, transmission and reception dates. |
| [Research highlights](historical-showcase.md) | Selected new keys, restored readings and historical connections. |
| [Cipher research](research-status.md) | Exact cryptanalytic results, partial reconstructions and remaining open sources. |
| [Edition and attribution](edition-and-attribution.md) | Earlier publications and the contributions of individual researchers. |

The [source index](../cases/README.md) locates all 679 ciphertext bodies,
including the 22 original challenges and seven OPEN sources. Its subject
indexes classify individual messages. The historical studies connect material
across those classifications.

## Source and research files

| Location | Role |
|---|---|
| [cases/pages/](../cases/pages/README.md) | Complete editions named by printed page, such as [185.md](../cases/pages/185.md). |
| [cases/](../cases/README.md) | Canonical source accounts, with short English meanings and full evidence; original challenge paths remain stable. |
| [docs/historical-studies/](historical-studies/README.md) | Historical arguments, comparisons and chronology. |
| [data/reading_catalog.json](../data/reading_catalog.json) | Physical source identifiers, reading states, attribution and canonical paths. |
| [data/case_view_summaries.json](../data/case_view_summaries.json) | The short meanings displayed above individual source accounts. |
| [data/topic_reading_paths.json](../data/topic_reading_paths.json) | Curated subject-guide entries. |
| [data/](../data/README.md) | Keys, transcripts, earlier readings, certificates and review records. |
| [experiments/](../experiments/README.md) | Reproducible cipher reconstructions, searches, controls and source comparisons. |
| [sources/](../sources/README.md) | Bibliography, inspected source excerpts and provenance. |
| [adfgvx/](../adfgvx/) | Cipher arithmetic, verification and generation of the source editions and indexes. |

The six source folders classify Caucasus affairs, naval traffic, military
operations, radio service, finance and people. Their boundaries serve the
index; a historical question may involve several folders. Existing paths
under `cases/other/` retain older citations.

<a id="maintain-the-edition"></a>

## Maintain the source edition

Edit the complete canonical case body inside its CASE-EDITION markers, and
update its short meaning in `data/case_view_summaries.json`. Keep physical
source identity, original text, reconstruction costs and attribution intact.
The numbered page files are generated from those canonical bodies.

```sh
python -m adfgvx.case_views --write
python -m adfgvx.catalog
python -m adfgvx.navigation
python -m adfgvx.page_editions
```

Check the views and the cipher evidence:

```sh
python -m adfgvx.case_views --check
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.page_editions --check
python data/reviews/check_reading_presentation.py
python data/reviews/verify_live_readable_mappings.py
python -m adfgvx.verify
```

The full [workflow](../.github/workflows/verify.yml) includes the source-specific
checks. Install its dependencies from [REQUIREMENTS.txt](../REQUIREMENTS.txt).

## Extend the historical research

Add a study or revise an existing argument around a concrete question. Link
its principal passages to the numbered page editions, identify the date and
kind of each source, and explain what the comparison establishes. Update the
research guide and chronology when the result changes their account.
[CONTRIBUTING.md](../CONTRIBUTING.md) and the [reading conventions](reading-conventions.md)
give the editorial rules.
