# Contributing

## Source editions and historical research

Every printed source page has its own complete Markdown edition at
`cases/pages/NNN.md`. The home-page page numbers link there directly. Keep
the German readings, English interpretations and source explanations complete;
place long machine streams in expandable evidence blocks.

Historical studies belong in `docs/historical-studies/`. Organize them around
a historical question, connect the relevant sources, and cite the full page
editions. Distinguish origin, event, transmission and reception dates, and
separate an instruction from a report that it was carried out. Record the
specific contribution of an external source rather than attaching general
background references.

The individual case files supply a concise English meaning and preserve the
complete canonical source body. Edit that body inside its CASE-EDITION markers,
and maintain the short account in `data/case_view_summaries.json`. Preserve
literal unknowns, all reconstruction costs, competing readings and earlier
attribution when reorganizing the presentation.

## Place a new case

Use the appropriate folder under `cases/`: `caucasus`, `naval`, `military`,
`radio`, `finance` or `people`; use `open` for a body with no accepted reading. The original challenge, context and supplementary
pages retain their established locations. The [repository map](docs/repository-map.md)
describes the topic boundaries and the stable research-package locations.

Add each physical source exactly once to `data/reading_catalog.json`, with its explicit READING, PARTIAL, CONDITIONAL or OPEN state. Improved editions update the same source entry. Then run
`python -m adfgvx.case_views --write`, `python -m adfgvx.catalog`,
`python -m adfgvx.navigation` and `python -m adfgvx.page_editions`. These
regenerate the case views, direct page links, subject guides and full editions. Curated topic order and explanations live in `data/topic_reading_paths.json`.
Check the generated views with `--check`. Topic coverage, local links and retained section
anchors are verified by the navigation check.

`cases/other/` now preserves earlier URLs. Its short compatibility pages are
generated from `data/case_path_aliases.json`; complete case bodies belong in
their canonical topic folders. Preserve old anchors when revising a published
heading. Keep the evidence needed to reproduce current claims. Remove superseded layout snapshots and redundant displays; Git history preserves earlier editions. Update dependent references when retiring an unused package.

## Preserve evidence and attribution

Keep source transcriptions unchanged. Record all insertions, deletions, known-coordinate substitutions, and erasure fills separately, with an explicit indexing convention. Retain competing source glyphs and alternative optimal alignments.

Name the original decipherer, source, and date for earlier work. Credit our research and editorial contributions consistently as **icekylinx and GPT-6 Astra Pro**. Historical publication titles and external authorship are preserved as published. A reproduced result is credited as reproduction or review.

Use the project title **ADFGVX Cipher** in repository metadata and citations. The project contributions use **Apache-2.0**; preserve the source status and notices of third-party material.

## Make the claim reproducible

Provide a compact certificate and an independent arithmetic check for a new accepted claim. Record exact search bounds, deterministic seeds where applicable, model provenance, and relevant controls. Separate diagnostic best fits from accepted historical readings.

Run `python3 -m adfgvx.verify` and the specific checks affected by the change. The [GitHub workflow](.github/workflows/verify.yml) lists maintained checks; the [experiment index](experiments/README.md) gives their scopes. Check relative links and avoid committing generated executables, downloaded corpora, model binaries, or duplicate source archives.
