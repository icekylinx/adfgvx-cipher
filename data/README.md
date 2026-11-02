# Research data

[ADFGVX Cipher](../README.md) · [Readable cases](../cases/README.md) · [Methods guide](../docs/methods.md) · [Experiments](../experiments/README.md)

| File or directory | Content |
|---|---|
| [messages.json](messages.json) | The 22 challenge entries, original and legacy transcriptions, conservative analysis layers, and header conventions |
| [reading_catalog.json](reading_catalog.json) | The common source for both reader-facing tables: 22 challenge entries and individually identified source-reviewed ciphertexts elsewhere in the collection |
| [keys.json](keys.json) | Historical, comparison, reported, and newly recovered partial keys, with provenance and unknown cells preserved |
| [prior_readings.json](prior_readings.json) | Earlier attributed readings, exact repair variants, and recomputed arithmetic |
| [supplementary_readings.json](supplementary_readings.json) | The October 2026 supplementary readings and their primary-source corrections |
| [review_ledger.json](review_ledger.json) | Claim-by-claim findings, original contributions, corrections, and unresolved limits |
| [certificates/](certificates/) | Coordinate maps, explicit edits, source relationships, and plaintext constraints |
| [reviews/](reviews/) | Focused source, attribution, historical, and reproducibility audits |

Question marks retain unresolved source evidence or square cells. They are never silently filled by a language-model best fit. Case pages present readable editorial text; these records preserve the exact evidence behind it.

Research and editorial attribution: **icekylinx and GPT-6 Astra Pro**. Earlier readings retain their individually recorded authors and dates.

Additional source editions live with their verifiers in
[corpus_readings](../experiments/corpus_readings/README.md),
[corpus_attack](../experiments/corpus_attack/SOURCE_FAMILIES.md),
[corpus_joint](../experiments/corpus_joint/README.md),
[p170_continuation](../experiments/p170_continuation/README.md),
[courier_recovery](../experiments/courier_recovery/README.md) and
[open_targets_continuation](../experiments/open_targets_continuation/README.md).
The reading catalogue links each individual source record to its case and
the exact evidence files, including repeated transmissions and multipart messages.

After adding a reviewed case to the reading catalogue, run
`python3 -m adfgvx.catalog` to regenerate both tables. The `--check` option
checks their agreement, unique identifiers and evidence links without editing.
Uninspected OCR candidates belong in the research inputs, not in the reviewed
reading table.
