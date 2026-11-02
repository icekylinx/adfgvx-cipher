# Contributing

## Present a readable result

Begin a case with the best-supported German reading, a concise English meaning, and the unresolved words or numbers. Keep exact compact plaintext and ciphertext below it. Use square brackets for editorial restoration and `?` for unresolved characters; explain case-specific notation.

Distinguish a source-fixed reading, a partial decipherment, a source-linked recovery, and an editorial hypothesis. Do not count a supplementary or contextual record as another challenge entry.

## Place a new case

Use the appropriate folder under `cases/`: `caucasus`, `naval`, `military`,
`radio`, `finance` or `people`. The original challenge, context and supplementary
pages retain their established locations. The [repository map](docs/repository-map.md)
describes the topic boundaries and the stable research-package locations.

Add each reviewed physical record to `data/reading_catalog.json`, then run
`python -m adfgvx.catalog` and `python -m adfgvx.navigation`. These regenerate the
same two complete reader tables and the topic indexes from the live catalogue.
Check both with `--check`. Topic coverage, local links and retained section
anchors are verified by the navigation check.

`cases/other/` now preserves earlier URLs. Its short compatibility pages are
generated from `data/case_path_aliases.json`; complete case bodies belong in
their canonical topic folders. Preserve old anchors when revising a published
heading. Keep established source images, certificates, models and experiment
packages at their recorded locations.

## Preserve evidence and attribution

Keep source transcriptions unchanged. Record all insertions, deletions, known-coordinate substitutions, and erasure fills separately, with an explicit indexing convention. Retain competing source glyphs and alternative optimal alignments.

Name the original decipherer, source, and date for earlier work. Credit our research and editorial contributions consistently as **icekylinx and GPT-6 Astra Pro**. Historical publication titles and external authorship are preserved as published. A reproduced result is credited as reproduction or review.

Use the project title **ADFGVX Cipher** in repository metadata and citations. The project contributions use **Apache-2.0**; preserve the source status and notices of third-party material.

## Make the claim reproducible

Provide a compact certificate and an independent arithmetic check for a new accepted claim. Record exact search bounds, deterministic seeds where applicable, model provenance, and relevant controls. Separate diagnostic best fits from accepted historical readings.

Run `python3 -m adfgvx.verify` and the specific checks affected by the change. The [GitHub workflow](.github/workflows/verify.yml) lists maintained checks; the [experiment index](experiments/README.md) gives their scopes. Check relative links and avoid committing generated executables, downloaded corpora, model binaries, or duplicate source archives.
