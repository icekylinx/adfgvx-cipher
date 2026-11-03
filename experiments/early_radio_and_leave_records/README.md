# Early radio and leave records

Four source-reviewed native records: p87 A1, p119 A, p127 A3 and p127 B1. Their 812 source slots yield 406 plaintext positions: 391 fixed in raw output and 400 after three observed-coordinate substitutions and nine source-mask fills. Six positions remain unresolved. All source lengths, published keys and numeral labels are retained.

p119 A is a complete 143-position direct reading with no edits. The other records preserve an unresolved opening label, unit and place labels, and the literal NICT defect.

Run from repository root:

```sh
python experiments/early_radio_and_leave_records/verify.py --verify
python experiments/early_radio_and_leave_records/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

See [inputs](inputs.json), [certificates](certificates.json) and [catalog proposal](catalog_proposal.json). Every case has raw output, a counted edited stream, readable German, English meaning, source details, uncertainty and prior attribution.

The separate [optional OSM field](osmanie_field.json) completes p127 B1's
`OS?` with one additional printed-mask fill, supported by station context and
Hopman's independent 5 November diary notice. It preserves the original raw
and edited layers, literal `NICT`, conflicting source dates and unread part 2;
it adds no physical body. Its optional total is one observed substitution and
four source-mask fills, reaching 80/80 positions. The existing four-record
certificate and totals above stay unchanged.

```sh
python experiments/early_radio_and_leave_records/verify_osmanie.py --verify
```

Add `--pdf /path/to/childs.pdf` for the original cipher-crop pixels and
`--hopman-image /path/to/00646_full1800.jpg` for the exact public IIIF page
bytes and RGB pixels. Without those arguments, the external diary image's
pixels are explicitly unchecked. No new image asset is distributed.
