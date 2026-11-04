# p215 B3 — positions and railway departure fragment

Research and review: **icekylinx and GPT-6 Astra Pro**. Apache-2.0.

This edition preserves the 219 literal source slots, including all 200 observed
coordinates. A conditional 234-slot frame inserts fifteen unknowns and relocates
eight printed masks; the unchanged published Nov22–24 key fixes 88/117 positions.
The no-relocation frame is retained because it already contains much of the same
language. Neither the loss allocation nor the mask placement is historically
unique.

The primary word proposal fixes 109/117 positions for two observed substitutions,
14 printed-mask fills and ten inserted-slot fills. Positions 82, 93 and 104 have
no observed half-coordinate and are explicitly lexical completions. An optional
Alsosimand extension fixes 111/117 for four observed substitutions, 15 printed
fills and eleven inserted fills. These counts include uninterpreted labels;
they are not counts of authenticated historical letters.

The existing global J/Y assumptions from `p215_hungarian_y` give Gyula and
Kisjenoe without additional coordinate changes. The complete partial square,
eight-symbol injective remainder, and a full-square roundtrip witness are
included. The baseline key register is unchanged; arbitrary witness values are
not historical fills.

## Reproduce

```sh
python experiments/p215_third_positions_fragment/verify.py --verify
python experiments/p215_third_positions_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The first command verifies the source transcript hash, all source-slot identities,
observed order, coordinate domains, exact repair ledgers, global shared-square
constraints and complete re-encryption. It explicitly reports source pixels as
unchecked when the PDF is absent. The second also authenticates the original
PDF bytes and freshly rendered crop against the recorded hashes.

The optional discovery replay uses the pinned external `quad26.bin` and NumPy:

```sh
python experiments/p215_third_positions_fragment/replay_search.py --quad26 /path/to/quad26.bin --output /tmp/p215-b3-replay.json
```

It rebuilds the existing probability model, checks two fresh same-shape controls,
and reproduces 406,656 historical frame descriptions. The 136 source-run loss
allocations and 217 other contiguous-loss frames each test the same 1,152 mask
operations. The primary source-run leaders tie at mask destinations 85 and 86.
Control fixed positions were all correct (88/88 and 83/83); the first control
had a better-scoring geometry than the planted one, so these tests do not
establish unique loss locations. Both controls and that limitation are frozen
in `search_provenance.json`.

`verify.py` reuses only the pinned, model-free arithmetic helpers from the
adjacent Breslau package. No trained model or large source PDF is committed.

- [Reading and limitations](../../cases/military/p215_third_positions_fragment.md)
- [Inputs and exact frames](inputs.json)
- [Recomputed certificate](certificates.json)
- [Independent contemporary geographical references](historical_context.json)
- [Search scope and controls](search_provenance.json)

The source-gap audit is a dated snapshot; its original “no accepted reading”
observation is preserved. Live catalogue and coverage reports record this later
conditional edition. Earlier negative exact-copy tests addressed a different
hypothesis and remain valid within their stated scope.
