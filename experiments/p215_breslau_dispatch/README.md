# p215 A: conditional Breslau–Oderberg dispatch

**icekylinx and GPT-6 Astra Pro · 4 November 2026**

[Read the edition](../../cases/military/p215_breslau_dispatch.md).

A five-mask group relocation and two unfilled short-group coordinates reveal
176/196 raw positions under the unchanged published Nov22–24 key. All 372
observed coordinates retain their values and relative order; no source slot
is excluded. The mask relocation is a conditional repair, not what the source
prints. No numerical interpretation or word restoration is included yet.

`inputs.json` records the literal source and exact frame. `verify.py` constructs
the map directly, checks all nine mask-identity aliases, computes every domain
with independent ragged-grid arithmetic, cross-checks the repository cipher,
and verifies complete forward witnesses. `certificates.json` is generated.
The optional PDF argument checks the pinned original PDF and source crop pixels.

```sh
python experiments/p215_breslau_dispatch/verify.py --verify
```
