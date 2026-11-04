# Repository collaboration instructions

## Established presentation

Repository content is in English. Credit the current research and editorial
work to **icekylinx and GPT-6 Astra Pro**, while preserving earlier authors'
specific contributions. The project uses Apache-2.0.

Keep the home page concise and organize the reading catalogue by printed
manuscript page. The generated page and topic indexes come from
`data/reading_catalog.json`; use `python -m adfgvx.catalog` and
`python -m adfgvx.navigation` to refresh them.

The home-page page-number table must link **directly** to the dedicated
`cases/pages/NNN.md` edition for each of the 175 printed source pages, never
through a range index or a case substitute. Those pages contain the complete
ciphertext readings and explanations. The historical studies are a separate
research layer, organized by historical questions and dated source relations.
Preserve source and cipher evidence when revising that layer.

Edit a canonical case body inside its CASE-EDITION markers and keep
`data/case_view_summaries.json` current. Then run
`python -m adfgvx.case_views --write`, `python -m adfgvx.catalog`,
`python -m adfgvx.navigation`, and `python -m adfgvx.page_editions`.
Keep the dedicated page editions complete and existing source citations valid.

Keep one catalogue entry per physical source and public OPEN pages for
unread targets. Remove obsolete presentation snapshots and repeated displays
when their current evidence and useful attribution are preserved.
Use the current [reading conventions](docs/reading-conventions.md): lead with
the readable message and its historical significance, keep uncertainty local,
and place detailed machine streams in expandable evidence sections. Preserve
literal unknown positions, numerical labels, source evidence, repair costs
and earlier contributions. Old presentation snapshots are not a requirement
to preserve duplicated prose or an obsolete page structure.
