# Repository collaboration instructions

## Presentation and attribution

Repository content is in English. Credit the current research and editorial
work to **icekylinx and GPT-6 Astra Pro**, while preserving earlier authors'
specific contributions. The project uses Apache-2.0.

The public edition has two reading routes:

- **By printed page:** the home page offers eight page ranges. Each range
  opens a page-number table, and each number opens its complete
  `pages/NNN.md` edition. Preserve all 175 printed pages.
- **By subject:** six guides under `topics/` contain 50 curated summaries. Each summary
  links its physical source identifiers directly to the complete numbered
  page editions. Historical studies develop arguments across those sources.

Keep the home page concise. There is no separate public case-view layer.
Keep complete source editions under `pages/`. Do not recreate standalone
case pages or compatibility stubs as navigation steps. Preserve German readings, English interpretations, source
explanations and technical evidence within the full page editions.

## Canonical source and navigation data

`data/source_editions.json` preserves the 307 complete canonical edition texts,
their SHA-256 hashes and earlier path aliases. Original case paths are stable
internal identifiers for the archived texts and research dependencies; they
are not destinations for new public links.

`data/reading_catalog.json` identifies each physical source once, with its
state, attribution and edition association. `data/topic_exploration.json`
contains the curated topic sections, summaries and `source_ids`. Summaries
select and explain sources; they do not replace their complete editions.

Edit the canonical archive text and refresh its SHA-256 hash when changing
an edition. Preserve existing identifiers and anchors. Regenerate the public
views with `python -m adfgvx.catalog`, `python -m adfgvx.navigation` and
`python -m adfgvx.page_editions`; use their `--check` modes for validation.
Run `python -m adfgvx.source_editions --check` to verify archive integrity.
Do not edit generated page files as an alternative to their canonical source.

Use `p153`, `pp152–153` and `p153 A3` in editorial prose; retain original
challenge IDs such as `p153a`. Use day–month–year dates, sentence-case headings
and en dashes for ranges. The full style table is in
[reading conventions](docs/reading-conventions.md#editorial-style).
Shared display formatting belongs in `adfgvx/editorial_style.py`, after page
assembly. Preserve source quotations, code, literals, URLs and legacy anchors;
do not rewrite the archived texts merely to change their typography.

## Research verification

Some frozen research checks still read original case paths. Run
`python -m adfgvx.source_editions --materialize` before those checks and
`python -m adfgvx.source_editions --clean` afterward. Materialized files are
temporary verification inputs. Persist intentional edits in the archive
before cleanup and do not commit the temporary case files.

Keep source transcriptions, raw and edited streams, plaintext positions,
numerical labels, reconstruction costs, alternative frames, certificates
and earlier contributions intact. Preserve source-declared gaps and distinguish
observed substitutions from erased-coordinate and missing-slot fills. Follow
[the reading conventions](docs/reading-conventions.md).

Historical studies belong in `docs/historical-studies/`. Cite complete numbered
page editions and give each external source a specific evidentiary role.
Use descriptive headings and state findings directly. Prefer them to question-led
mini-headings and repeated prompts such as “What this shows”. Keep factual
qualifications beside the affected claim; avoid repetitive general disclaimers. The [repository guide](docs/repository-map.md) and
[contribution guide](CONTRIBUTING.md) describe the maintenance workflow.
