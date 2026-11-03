# Early radio and leave records

Four source-reviewed native records: p87 A1, p119 A, p127 A3 and p127 B1. Their 812 source slots yield 406 plaintext positions: 391 fixed in raw output and 400 after three observed-coordinate substitutions and nine source-mask fills. Six positions remain unresolved. All source lengths, published keys and numeral labels are retained.

p119 A is a complete 143-position direct reading with no edits. The other records preserve an unresolved opening label, unit and place labels, and the literal NICT defect.

Run from repository root:

```sh
python experiments/early_radio_and_leave_records/verify.py --verify
python experiments/early_radio_and_leave_records/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

See [inputs](inputs.json), [certificates](certificates.json) and [catalog proposal](catalog_proposal.json). Every case has raw output, a counted edited stream, readable German, English meaning, source details, uncertainty and prior attribution.
