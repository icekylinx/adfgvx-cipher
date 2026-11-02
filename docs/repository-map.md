# Repository map

Start with the [case guide](../cases/README.md) to read the messages. Its six
topic guides collect related subjects and then show each physical source
record with its reading status and credit. The complete challenge and other
record tables remain available in both the case guide and the
[main README](../README.md).

Prepared by **icekylinx and GPT-6 Astra Pro**. Topic placement is an editorial
reading aid; each case retains its own keys, source relationships and limits.

## Read by subject

| Folder | Reading focus |
|---|---|
| [cases/caucasus](../cases/caucasus/README.md) | Tiflis administration, staffing, procurement and diplomatic appointments |
| [cases/naval](../cases/naval/README.md) | Ships, Black Sea cargo, sale terms, embarkation and naval orders |
| [cases/military](../cases/military/README.md) | Army movements, withdrawal, internment, position reports and supplies |
| [cases/radio](../cases/radio/README.md) | Station control, keys, call signs, couriers, retransmissions and message routing |
| [cases/finance](../cases/finance/README.md) | Funds, currency, banknotes, allowances and purchasing decisions |
| [cases/people](../cases/people/README.md) | Staff transfers, personnel inquiries, travel permissions and civilian affairs |

The 22 challenge case pages retain their original paths directly under
`cases/`. Shared contextual witnesses remain in `cases/context/`, and the
earlier supplementary editions remain in `cases/supplementary/`. Topic guides
link these pages into the appropriate reading groups. A physical source record
has one primary topic in the other-record catalogue; related challenge links
keep their separate challenge status.

Earlier `cases/other/` URLs remain as short [compatibility pages](../cases/other/README.md).
They preserve the original section anchors and lead to the complete edition in
its topic folder. Each complete body has one canonical location.

## Follow a reading to its evidence

| Location | Purpose |
|---|---|
| [cases/](../cases/README.md) | Readable German, English meaning, qualifications, original credits and evidence links |
| [data/reading_catalog.json](../data/reading_catalog.json) | Authoritative record identifiers, subjects, statuses, credits and current case paths |
| [data/reading_groups.json](../data/reading_groups.json) | Topic directories, shared case membership and related challenge links |
| [data/case_path_aliases.json](../data/case_path_aliases.json) | Earlier and current case paths, preserved section anchors and original Markdown digests |
| [data/](../data/README.md) | Core challenge transcriptions, key provenance, earlier readings, certificates and review ledgers |
| [experiments/](../experiments/README.md) | Source editions and verifiers, search implementations, completed results, controls and model provenance |
| [sources/](../sources/README.md) | Bibliography, source registry, page excerpts and historical context |
| [adfgvx/](../adfgvx/) | Shared cipher arithmetic, core verification and catalogue/navigation generation |

A case page points to the particular experiment or certificate that supports
its reading. The [experiment index](../experiments/README.md) groups the existing
packages into source review, p153 recovery, damaged-text optimization and open
target searches. Their original package locations are retained: code can depend
on folder depth, another package's files, or an exact recorded source hash.

Source images, literal transcriptions, model inputs, result ledgers and
certificates stay with their established verifiers. Directory organization does
not change their source coordinates, numerical labels or accepted-reading
status.

## Update the live reading guides

Create a new standalone case in the appropriate topic folder. Add its reviewed
physical records to `data/reading_catalog.json`, retaining each record's status,
credit and evidence paths. Pages in a topic folder are classified automatically;
the `additional_case_paths` entries in `data/reading_groups.json` handle shared
challenge, context and supplementary pages.

Then regenerate and check the guides:

```sh
python -m adfgvx.catalog
python -m adfgvx.navigation
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.verify
```

The catalogue command generates the two complete tables from one data source.
The navigation command generates the topic indexes and compatibility pages. Its
check verifies complete topic coverage, current status/credit rendering, alias
destinations, retained section anchors, and local reading links, including
links to evidence files. These checks use Python's standard library.

When editing a published case heading, preserve its older anchor if a retained
alias uses it. New cases that have never had an earlier path do not need an
alias. Further research and source-edition checks remain documented beside
their own experiments and in the [verification workflow](../.github/workflows/verify.yml).

## Historical reports keep their own snapshots

The [first extension inventory](../experiments/session_review/README.md) compares
its preserved start and end catalogues. Its end snapshot contains 195 other
records and keeps the paths and credits recorded at that time. The live
catalogue and topic guides can grow without rewriting that historical report.
Old paths in prior catalogues, ledgers and experiment proposals continue to work
through the compatibility pages.

For research boundaries, use the [current research status](research-status.md).
The [publication history](publication-history.md) maps the original local
commits to their exact-content public equivalents.
For the distinction between a direct reading, source-linked reconstruction and
editorial repair, use the [methods guide](methods.md).
