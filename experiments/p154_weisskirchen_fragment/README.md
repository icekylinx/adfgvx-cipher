# p154 A2 — Weisskirchen fragment

Discovery and review: **icekylinx and GPT-6 Astra Pro**. Apache-2.0.

The unchanged Nov4–6 key gives a new partial edition of p154 A2: raw 36/81,
then 56/81 after two observed substitutions and 20 added-slot fills. The frame
separately excludes source 28 `D` from the six-character `VDFDVD` group and
adds 45 unknown prefix slots. The complete 118-coordinate transcription stays
unchanged. All 20 newly fixed word positions have one observed half-coordinate.

- [Source edition and readable excerpts](../../cases/military/p154_weisskirchen_fragment.md)
- [Exact input and frame](inputs.json)
- [Coordinate domains, repairs and complete witnesses](certificates.json)
- [Search scope and fresh controls](search_provenance.json)
- [Contemporary spelling evidence](historical_context.json)

## Verify the edition

```sh
python experiments/p154_weisskirchen_fragment/verify.py --verify
python experiments/p154_weisskirchen_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The first command checks literal source, key, mapping, raw domains, the complete
repair ledger and re-encryption. It also recomputes the word-conditioned
comparison with 119 single 44-loss models and 12,900 group-boundary two-gap
models. Their minima are 10 and 7 observed substitutions for the same two
phrases, versus 2 here plus the separately priced exclusion. This bounded
comparison does not prove an unrestricted historical optimum.

The second command additionally authenticates the original PDF bytes and
freshly rendered source crop. Without the PDF, source pixels are explicitly
reported as unchecked. Generic arithmetic is reused from the hash-pinned
Breslau package; no source PDF or binary model is committed.

## Replay the discovery

```sh
python experiments/p154_weisskirchen_fragment/replay_search.py --quad26 /path/to/quad26.bin --output /tmp/p154-search.json
```

Requires NumPy and the external quad26 file pinned by the existing p212 recipe.
The replay rebuilds the coordinate 49 probability model and checks:

| Scope | Model descriptions | Result |
|---|---:|---|
| One surplus glyph within VDFDVD; one 45-slot loss | 708 | source 28 exclusion and 45-slot prefix rank first |
| Prefix only; even total 118–300; six possible exclusions | 552 | all six 162-slot models outrank every other length |
| Prefix plus another loss interval, 45 unknowns total | 32,568 | score improves 1.86; no further word edition adopted |

The last family includes repeated descriptions of the same wire when both
loss intervals meet at boundary 0. These are not counted as independent
readings. The primary remains the simpler one-prefix frame and is not claimed
to maximize the expanded family.

Three fresh source-shaped controls give planted-frame ranks 5, 1, 1. The first
control's leader shifts the missing block by one position and has one wrong
fixed letter; the other two recover the correct fixed text. All roundtrip
and source-accounting checks pass, but the search does not guarantee unique
loss locations.

Forty frequency-preserving shuffled sources, each scanned over the same 708
models, all score below the historical candidate. This is an exploratory
calibration for that declared family, not a multiple-search-adjusted
significance claim. The prior source-preserving 44-loss family did not express
the new surplus-glyph hypothesis.

The proposed fragments remain conditional words. The incomplete opening,
numerals, intervening field and closing are retained; arbitrary witness fills
are used only to verify arithmetic.
