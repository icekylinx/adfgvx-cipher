# Repository map

**icekylinx and GPT-6 Astra Pro**

Start with the [case guide](../cases/README.md) for readable messages or the [page index](../cases/pages/README.md) for a printed source location. Every case connects the readable text to its original ciphertext, key, repair ledger and credits. Symbols and evidence layers follow the [reading conventions](reading-conventions.md).

## Read by page or subject

The page index groups the Childs collection into 25-page ranges, then short tables for each printed page. Challenge entries and other reviewed records have separate tables. Use the printed page number together with its section and part label.

| Topic guide | Contents |
|---|---|
| [Caucasus](../cases/caucasus/README.md) | Tiflis administration, appointments, staffing and procurement |
| [Naval](../cases/naval/README.md) | Ships, cargo, sale terms, embarkation and naval orders |
| [Military](../cases/military/README.md) | Army movements, withdrawal, internment, reports and supplies |
| [Radio](../cases/radio/README.md) | Stations, keys, couriers, call signs and repeated transmissions |
| [Finance](../cases/finance/README.md) | Funds, currency, banknotes, allowances and purchases |
| [People](../cases/people/README.md) | Transfers, travel, personnel inquiries and civilian affairs |

The 22 challenge pages retain their paths directly under `cases/`. Shared witnesses in `cases/context/` and supplementary editions in `cases/supplementary/` also appear in the topic guides. Earlier `cases/other/` links redirect to the canonical edition and preserve their section anchors.

## Evidence and code

| Location | Purpose |
|---|---|
| [cases/](../cases/README.md) | Readable German, English meaning, raw and edited text, status and credit |
| [data/reading_catalog.json](../data/reading_catalog.json) | Authoritative record identifiers, source locations, statuses, credits and case paths |
| [data/reading_groups.json](../data/reading_groups.json) | Topic membership and shared case links |
| [data/](../data/README.md) | Challenge transcriptions, keys, prior readings, certificates and review ledgers |
| [experiments/](../experiments/README.md) | Source-edition verifiers, attacks, exact results, controls and model provenance |
| [sources/](../sources/README.md) | Bibliography, historical context, excerpts and the [latest reviewed crops](../sources/reviewed-crops.md) |
| [adfgvx/](../adfgvx/) | Shared cipher arithmetic, verification and index generation |

Each case links its supporting package. Source images, inputs and certificates stay beside the relevant verifier; established package paths retain their recorded hash and import relationships. The [source-overlap register](catalogue-source-overlaps.md) reconciles later editions of a shared physical source, and [case aliases](../data/case_path_aliases.json) preserve earlier URLs.

## Maintain the reading guides

Add a new case to its topic folder and its reviewed source records to `data/reading_catalog.json`. The `additional_case_paths` entries in `data/reading_groups.json` handle shared challenge, context and supplementary pages. Then regenerate and check:

```sh
python -m adfgvx.catalog
python -m adfgvx.navigation
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.verify
```

The catalogue generator builds the homepage summaries, page index and page-range tables. Navigation builds the topic guides and compatibility pages. Checks cover every record, topic assignment, local link, retained anchor, status and credit. Preserve older anchors when changing a published heading. Edition-specific checks are listed in each package and the [verification workflow](../.github/workflows/verify.yml).

## Research and publication records

The [research status](research-status.md) presents established contributions and current targets. The [whole-material census](whole-material-coverage.md) tracks the 679-body collection and remaining catalogue gaps. The [initial extension inventory](../experiments/session_review/README.md) and [post-publication inventory](../experiments/post_push_review/README.md) preserve their publication snapshots; live guides continue to grow from the current catalogue. The [publication history](publication-history.md) maps earlier local commits to their public equivalents.
