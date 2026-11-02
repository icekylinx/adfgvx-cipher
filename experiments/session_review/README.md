# Source-extension inventory: 2 November 2026

**icekylinx and GPT-6 Astra Pro.**

This review compares the current two reader tables with the exact catalogue
at commit `ffc0c91e75b80e628524d665af9507f123fd664c`, preserved in
[baseline_reading_catalog.json](baseline_reading_catalog.json). The baseline
has 22 challenge entries and 87 other reviewed physical records.
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
```

This check requires only Python's standard library and the preserved files;
it does not need a Git checkout or a network connection. Running without
`--verify` explicitly regenerates the inventory after a catalogue revision.
