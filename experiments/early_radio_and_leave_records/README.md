# Early radio and leave records

Four source-reviewed native records: p87 A1, p119 A, p127 A3 and p127 B1. Their 812 source slots yield 406 plaintext positions: 392 fixed in raw output and 403 after three observed-coordinate substitutions and eleven source-mask fills. Three positions remain unresolved. All source lengths, published keys and numeral labels are retained.

p87 A1 and p119 A are complete direct readings, of 83 and 143 positions. Review of p87 A1 identifies the first-row final group as `DGAGF`; correcting our earlier `EGAGF` transcription restores the separator after `AKONACH18`. The p127 A3 proposal reaches 98/100 positions: the related ZON setup notice at p120 C supports two missing letters in `NAGQBECSEREK`. Its unit and `Q?` fields remain unresolved. The p127 B1 text retains its literal `NICT` defect and final `OS?` field.

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
