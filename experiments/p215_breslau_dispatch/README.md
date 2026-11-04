# p215 A: conditional Breslau–Oderberg dispatch

**icekylinx and GPT-6 Astra Pro · 4 November 2026**

[Read the edition](../../cases/military/p215_breslau_dispatch.md).

A five-mask group relocation and two unfilled short-group coordinates reveal
176/196 raw positions under the unchanged published Nov22–24 key. All 372
observed coordinates retain their values and relative order; no source slot
is excluded. The mask relocation is a conditional repair, not what the source
prints. A separately priced ordinary-word restoration identifies horseshoes,
hoof nails, screw nails and the closing Traindepot Breslau. Numerical labels
and the closing identifier remain uninterpreted.

| Mask destination | Raw fixed | Proposed word fixed | Observed substitutions | Printed-mask fills | Added-slot fills |
|---:|---:|---:|---:|---:|---:|
| 270, primary whole-group discovery | 176/196 | 192/196 | 6 | 14 | 2 |
| 268, blind language-score leader | 176/196 | 193/196 | 4 | 15 | 2 |
| 266, fewest changes for the proposed words | 176/196 | 194/196 | 3 | 16 | 2 |

The three word layers share 192 positions; their quantity evidence is not
pooled. Each word layer has 54 equivalent source-ownership descriptions and
one corrected ciphertext. These do not prove a unique historical frame.

`inputs.json` records the literal source and exact frame. `verify.py` constructs
the map directly, checks all nine mask-identity aliases, computes every domain
with independent ragged-grid arithmetic, cross-checks the repository cipher,
and verifies complete forward witnesses and every word-layer repair price.
`certificates.json` is generated. `historical_context.json` identifies a
visually checked 1918 institution-name witness, not a copy of the dispatch.
The optional PDF argument checks the pinned original PDF and source crop pixels.

```sh
python experiments/p215_breslau_dispatch/verify.py --verify
```

The compact discovery replay retains the original 225,250 whole-group
operation descriptions and the 9,700 coordinate-level mask destinations,
with two matched controls for each. It reconstructs the fixed-length joint
four-pattern probability model from the pinned p212 language inputs. The
external model, compiler output and reconstructed binary remain temporary.
It needs NumPy, a C compiler and the exact external `quad26` file described
in `search_provenance.json`:

```sh
python experiments/p215_breslau_dispatch/replay_search.py --quad26 /path/to/quad26.bin
```

The 270 model was the initial whole-group discovery; 268 wins the wider
blind language ranking; 266 was selected retrospectively for lower word-repair
cost. None of those selection rules alone authenticates the historical text.
