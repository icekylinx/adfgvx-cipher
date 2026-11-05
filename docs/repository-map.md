# Repository guide

[ADFGVX Cipher](../README.md) · [Historical research](historical-studies/README.md) · [Ciphertext pages](../pages/README.md)

## Read by page or subject

The edition contains **679 physical ciphertexts on 175 printed pages**.
The home page offers eight page ranges; each opens a page-number table leading
to the complete `pages/NNN.md` editions. Each edition contains the
ciphertexts, German readings, English interpretations, explanations and
evidence for that printed page.

The six subject guides offer **50 curated summaries**, grouped under military
affairs, naval traffic, finance, radio service, people and the Caucasus.
The guides live in `topics/`; their source links open the same full page
editions directly. A source may
contribute to several historical questions while retaining its single
catalogue identity. Seven [OPEN sources](../topics/open.md) remain available as a secondary
research filter. There is no intermediate standalone case-view layer.

| Reading resource | Contents |
| --- | --- |
| [Printed-page index](../pages/README.md) | Page ranges, page-number tables and complete editions. |
| [Subject exploration](../topics/README.md) | Six guides with source summaries and direct links to numbered pages. |
| [Historical studies](historical-studies/README.md) | Arguments connecting withdrawal, shipping, finance, radio authority and departure. |
| [Chronology](historical-studies/chronology.md) | A cross-subject sequence distinguishing event, origin and reception dates. |
| [Selected discoveries and methods](../README.md#selected-discoveries-and-methods) | Selected key recoveries, restored readings and historical connections. |
| [Cipher research](research-status.md) | Cryptanalytic results, partial reconstructions and open sources. |
| [Edition and attribution](edition-and-attribution.md) | Earlier publications and individual research contributions. |

## Canonical data and research files

| Location | Role |
| --- | --- |
| [data/source_editions.json](../data/source_editions.json) | Archive of 307 complete edition texts, their hashes and original path aliases. Original case paths are internal identifiers. |
| [data/reading_catalog.json](../data/reading_catalog.json) | Physical source identifiers, reading states, attribution and edition associations. |
| [data/topic_exploration.json](../data/topic_exploration.json) | Curated topic sections, summaries and catalogue `source_ids`. |
| [pages/](../pages/README.md) | Generated complete editions, named by printed page. |
| [docs/historical-studies/](historical-studies/README.md) | Historical arguments, source comparisons and chronology. |
| [data/](../data/README.md) | Keys, transcripts, certificates, earlier readings and review records. |
| [experiments/](../experiments/README.md) | Reproducible reconstructions, searches, controls and source comparisons. |
| [sources/](../sources/README.md) | Bibliography, inspected excerpts and provenance. |
| [adfgvx/](../adfgvx) | Cipher arithmetic, verification and generation of editions and navigation. |

The archive preserves complete canonical texts under their original case
identifiers. Those identifiers also support frozen research dependencies;
they are not a public navigation layer. Cite a numbered page and source
anchor in new reader-facing material.

<a id="maintain-the-edition"></a>

## Maintain the source edition

Edit the canonical archive entry's `text` and refresh its SHA-256 hash.
Preserve physical-source identity, original transcriptions, plaintext,
reconstruction accounts, certificates and attribution. Update the catalogue
association when needed. Topic summaries and their source selections are
edited in `data/topic_exploration.json`.

Regenerate the public views from those inputs:

```sh
python -m adfgvx.source_editions --check
python -m adfgvx.catalog
python -m adfgvx.navigation
python -m adfgvx.page_editions
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.page_editions --check
```

The page generator carries the complete source text into the numbered
editions. Shared editorial typography is applied by `adfgvx/editorial_style.py`
without changing archived quotations or research fixtures. Navigation checks
cover source links and retained section anchors.

## Replay the research checks

Frozen research checks may still read the original case paths. Materialize
the archive temporarily, run the checks, then clean up those files:

```sh
python -m adfgvx.source_editions --materialize
python -m adfgvx.verify
python data/reviews/check_reading_presentation.py
python data/reviews/verify_live_readable_mappings.py
# Run the affected source-specific verifiers listed in the workflow.
python -m adfgvx.source_editions --clean
```

Persist any intended edition changes in the archive before cleanup. The
materialized case files are temporary verification inputs and do not belong
in the public tree or a commit. The full
[workflow](../.github/workflows/verify.yml) lists the maintained checks;
[REQUIREMENTS.txt](../REQUIREMENTS.txt) supplies their dependencies.

## Extend historical research

Develop a concrete question using the complete source editions. Explain how
reference numbers, multipart joins or independent documents support the
argument. Update the relevant topic summary and chronology when a finding
changes their account. [CONTRIBUTING.md](../CONTRIBUTING.md) and the
[reading conventions](reading-conventions.md) give the editorial rules.

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.
