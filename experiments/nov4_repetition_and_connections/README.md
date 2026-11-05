# 4 November: repetition, communications and a money acknowledgment

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Five physical records on Childs pp121–122 preserve **1,030 source slots**,
**1,029 valid coordinates** and **515 modeled plaintext positions**. The
unchanged published Nov4–6 key fixes **514/515 positions** before editorial
repairs. The complete edited candidates require **7 observed-coordinate
substitutions** and **1 source-mask fill**, with no insertion, deletion,
group movement or key modification. They give 515/515 fixed positions;
these counts are compatibility evidence, not a new numeral interpretation.

The [radio edition](../../pages/121.md#edition-cases-radio-nov4-repetition-and-connections)
contains a two-part request to repeat the first part of a telegram to Kress,
and a two-part inquiry about Constanza, the Bucharest connection, its cable
and AOK 11. Matching printed part labels pair p121 B1 with p122 A2 while
preserving their different reception times and page-local section letters.
The [cash acknowledgment](../../pages/122.md#edition-cases-finance-cash-arrival-acknowledgment)
reads directly, without a single coordinate change.

`inputs.json` preserves literal rows, the noncoordinate Z-like glyph,
headers, unchanged key, crop geometry and source hashes. `certificates.json`
contains every transposition index, pair/domain, changed coordinate and
complete re-encryption. The independent column-offset implementation and
repair-account helper are pinned by hash. Every complete spaced German
reading is also checked against its exact edited stream after removing only
punctuation, whitespace and the justified separator X labels.

`prior_candidates.json` freezes the relevant earlier unreviewed repository
OCR candidates. This is their source-audited edition, not a first-solution
claim. The published key retains its full provenance.

## Reproduce

```sh
python experiments/nov4_repetition_and_connections/verify.py --verify
python experiments/nov4_repetition_and_connections/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command needs the standard library and checked-in modules. The
optional second command also needs PyMuPDF and Pillow; it verifies the
original PDF byte count and SHA-256, regenerates the four crops and checks
every RGB pixel. Scratch caches are not runtime dependencies.
