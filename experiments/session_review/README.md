# Source-extension inventory: 2 November 2026

**icekylinx and GPT-6 Astra Pro.**

This historical review compares two preserved catalogue snapshots. The exact
catalogue at commit `ffc0c91e75b80e628524d665af9507f123fd664c` is retained in
[baseline_reading_catalog.json](baseline_reading_catalog.json), with 22
challenge entries and 87 other reviewed physical records. The end-of-session
catalogue is retained in [final_reading_catalog.json](final_reading_catalog.json),
with the same 22 challenge entries and 195 other records. Its SHA-256 is
`50784e7b1a7a51a8e4224a088cdaec21a6c6f25285d869b5049110a667630e75`.
[inventory.json](inventory.json) lists every added physical record, groups
them by case, preserves their actual status and credit, and itemizes every
revision to a preexisting row. It also checks that the key catalogue and
challenge-message data remain byte-identical to that baseline.

An added row can be a multipart segment, a repeated intercept, a source
edition of an earlier reading, or a conditional reconstruction. Its count
must not be described as the number of new independent decipherments.
The p153 partial decipherment already exists at the baseline and is not a
new recovery in this extension. p73, p170 and p198 D remain wholly open.

```sh
python experiments/session_review/verify.py --verify
python -m adfgvx.catalog --check
```

The historical check requires only Python's standard library and the preserved
files; it does not need a Git checkout or a network connection. Running it
without `--verify` regenerates the inventory from those same start and end
snapshots. The inventory bytes and its legacy `current_catalogue_sha256` field
remain unchanged; that field identifies the session's final snapshot.

The separate `adfgvx.catalog --check` command checks the live catalogue and both
reader tables. Later readings and navigation changes can therefore be reviewed
without rewriting this earlier extension's counts, paths or attribution.
