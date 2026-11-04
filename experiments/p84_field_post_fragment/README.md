# p84 C — German field-post fragment

Discovery and review: **icekylinx and GPT-6 Astra Pro**. Apache-2.0.

The unchanged October 28–31 key and a source-directed 244-slot frame support
**DEUTSCHE FELDPOST**. All five possible positions of a missing coordinate in
`FDFG` are retained. Their common raw stream fixes 14/122 positions; the word
layer fixes 28/122 with **zero observed substitutions, two printed-mask fills
and fifteen added-tail fills**. H53, F55 and T62 are wholly unobserved lexical
completions. The missing short-group slot is not filled by the proposal.

- [Source edition](../../cases/radio/p84_field_post_fragment.md)
- [Source, key and five frame assumptions](inputs.json)
- [Coordinate domains, exact costs and full witnesses](certificates.json)
- [Discovery scope and controls](search_provenance.json)
- [Frozen raw-donor field manifest](donor_manifest.json)

## Verify

```sh
python experiments/p84_field_post_fragment/verify.py --verify
python experiments/p84_field_post_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

Both commands reproduce all five maps, 610 plaintext domains, source accounting,
word costs and complete re-encryption witnesses. The second also authenticates
the original PDF and freshly rendered crop. Without the PDF, pixels are
reported as unchecked. Generic arithmetic is reused from the hash-pinned
Breslau package. No full PDF or model binary is committed.

## Replay discovery

```sh
python experiments/p84_field_post_fragment/replay_search.py --output /tmp/p84-phrases.json
python experiments/p84_field_post_fragment/replay_search.py --quad26 /path/to/quad26.bin --output /tmp/p84-full-search.json
```

NumPy is required. The first command reloads 331 literal raw donor fields and
checks every target/donor substring alignment under all five 244-slot frames.
Donor unknowns break a match. It then repeats the hundred frequency-preserving
shuffle controls and two fresh source-shaped planted-phrase controls. The
second additionally reconstructs the existing book/radio probability mixture
and reruns the 12,617-model key/length diagnostic and four length controls.

The unique qualifying donor text is p210 C's raw `XDEUTSCLEFELDPOST`, with
fifteen observed target coordinates. The donor's typo is retained in discovery
evidence; the target's proposed H is explicitly unobserved. No donor coordinate
is transferred and no repeated-telegram claim is made.

The shuffled maximum is eleven observed supporting coordinates; none reaches
fifteen. Each shuffle includes the full donor corpus and all five frame
choices. Earlier key/length selection is outside this calibration, so it is
not a multiple-search-adjusted significance result.

The primary 244-slot frame is the top length/key candidate. The four fresh
length controls have planted-geometry ranks 2, 2, 5 and 1, with respectively
14/14, 22/22, 10/10 and 18/18 correct displayed letters. They demonstrate the
use of half-coordinate evidence but do not establish unique loss geometry.

Both fresh phrase controls retrieve their planted eighteen-letter phrase at the
correct position. Their maximal matches also extend into one or three incorrect
surrounding letters. This is why the historical edition supplies neither a
leading X nor a following separator from the broader vocabulary match.
