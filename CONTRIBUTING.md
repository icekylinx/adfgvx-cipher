# Contributing

## Reading routes and complete editions

The public edition offers two reading routes. The home page's eight page ranges
lead to page-number tables and then to the complete editions at
`cases/pages/NNN.md`. Six [subject guides](topics/README.md) offer 50 curated
summaries whose source links open those same numbered pages directly.
Historical studies connect the sources through research questions, chronology
and external evidence.

Each of the 175 page editions preserves its German readings, English
interpretations, source explanations and cipher evidence. Long machine
streams may sit in expandable blocks. There is no separate public case-view
layer; a summary supplements the complete edition.

## Edit a source edition

The canonical texts live in [data/source_editions.json](data/source_editions.json).
Its 307 entries retain the original case paths as internal identifiers, with
complete text, SHA-256 hashes and path aliases. Update the relevant entry's
`text` and its hash together. Keep existing section anchors and source
associations. The [repository guide](docs/repository-map.md) explains the
roles of the archive, catalogue and generated files.

Add each physical source exactly once to `data/reading_catalog.json`, with
its READING, PARTIAL, CONDITIONAL or OPEN state. Improvements update the
existing source entry. A new edition needs a canonical archive entry and
the appropriate catalogue association; it does not need a standalone case
page. For public citations, use the numbered page and its source anchor,
such as `cases/pages/165.md#source-p165-a1`.

Curated topic sections, summaries and source selections live in
`data/topic_exploration.json`. Reference catalogue `source_ids` so that the
generator resolves links to the correct pages. Keep claims in a summary
consistent with the full edition, including any material qualification.

Regenerate and check the public views:

```sh
python -m adfgvx.source_editions --check
python -m adfgvx.catalog
python -m adfgvx.navigation
python -m adfgvx.page_editions
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.page_editions --check
```

## Preserve evidence and attribution

Keep literal source transcriptions, raw and edited plaintext, numerical
labels, conditional assignments and competing readings. Record insertions,
deletions, observed-coordinate substitutions, erasure fills and frame
operations separately, with an explicit indexing convention. Retain
alternative source glyphs and optimal alignments. An improved presentation
must preserve the evidence and certificates supporting the existing claims.

Identify the original decipherer, source and date for earlier work. Credit our
research and editorial contributions as **icekylinx and GPT-6 Astra Pro**.
Preserve historical publication titles and external authorship as published.
Credit a reproduced result as reproduction or review.

Use **ADFGVX Cipher** as the project title. Project contributions use
**Apache-2.0**; retain the source status and notices of third-party material.

## Make the claim reproducible

Provide a compact certificate and an independent arithmetic check for a new
accepted claim. Record search bounds, deterministic seeds where applicable,
model provenance and relevant controls. Keep diagnostic fits distinct from
accepted historical readings.

Some frozen verifiers retain dependencies on the original case paths.
Restore those files temporarily from the canonical archive before running
the research checks:

```sh
python -m adfgvx.source_editions --materialize
python -m adfgvx.verify
python data/reviews/check_reading_presentation.py
python data/reviews/verify_live_readable_mappings.py
# Run the source-specific checks affected by the change.
python -m adfgvx.source_editions --clean
```

Materialized files are temporary test inputs. Save intended text changes in
the archive before cleanup, and keep the temporary case files out of commits.
The [verification workflow](.github/workflows/verify.yml) lists the maintained
checks; the [experiment index](experiments/README.md) describes their scopes.
Avoid committing generated executables, downloaded corpora, model binaries
or duplicate source archives.

## Extend the historical research

Historical studies belong in `docs/historical-studies/`. Organize an argument
around a concrete question and cite the full numbered source editions.
Distinguish event, origin and reception dates where they affect the sequence.
Explain the particular corroboration supplied by a diary, register, map or
other contemporary document. Keep necessary qualifications beside the claim
and use concise academic prose. Follow the [reading conventions](docs/reading-conventions.md)
when presenting quotations
or reconstructed passages. In editorial prose, use page references such as
`p153`, `pp152–153` and `p153 A3`, dates such as `4 November 1918`,
sentence-case headings and en dashes for numerical ranges. Preserve literal
quotations, source labels, code and stable identifiers.
