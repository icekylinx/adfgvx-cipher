# p228 B2 — demobilization continuation

Recovery and review: **icekylinx and GPT-6 Astra Pro**. Apache-2.0.

Five printed mask slots, moved from source[195:200] to boundary 246 after
removal, expose the continuation of the Neuhof demobilization order.
The frame keeps all 264 source slots and all 221 observed coordinates in their
original relative order. It adds no slots and uses the published Nov28–Dec1
key unchanged.

The raw layer fixes 90/132 positions. The word proposal fixes 121/132 for
five observed substitutions and 32 printed-mask fills. Its 95 proposed word
positions extend the earlier 33-position opening; the other 26 fixed labels
belong to retained reference and routing fields. The 22 newly fixed tail-word
positions each retain one observed half. Position 4 in the earlier opening
has both halves missing and is explicitly a lexical completion.

The conditional mask relocation reduces the price of the unchanged opening
from five observed substitutions to one, with ten mask fills in either frame.
The new tail spans identify an enclosure/order reference, the deputy command's
district, demobilization and a word ending in FORMATIONEN. The prefix ???CK,
remaining fields and all numeral values remain unresolved.

## Verify

```sh
python experiments/p228_demobilization_fragment/verify.py --verify
python experiments/p228_demobilization_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks every source identity and observed value/order, all 132
coordinate domains, the selected spans, five repairs, 32 fills, 24 mask-ownership
aliases and complete forward-encryption witnesses. It also recomputes the
unchanged opening in both frames. The PDF option authenticates source bytes
and freshly rendered pixels; without it, source pixels are explicitly reported
as unchecked.

The arithmetic helper is pinned to the existing Breslau package; the previous
Neuhof inputs are also pinned. Earlier source editions and displays are
preserved. No source image or trained model is duplicated.

## Optional discovery replay

```sh
python experiments/p228_demobilization_fragment/replay_search.py --quad26 /path/to/quad26.bin --output /tmp/p228-replay.json
```

This rebuilds the frozen probability model, exchanges X and Y only in its
language-scoring shadow, and repeats 124,628 mask-move descriptions. The scoring
projection is bijective; it does not alter the decryption key or displayed
labels. All 24 best descriptions yield the same raw text.

Two fresh source-shaped controls recover 90/90 and 89/89 correct fixed letters.
The second control's higher-scoring frame differs from the planted one;
its unknown pattern is also different. These controls demonstrate the stated
search's ability to recover partial language, while retaining its failure to
identify unique mask geometry.

Additional group-order and short-length diagnostics are summarized separately
in [search provenance](search_provenance.json). An observed-group move has a
slightly higher language score but changes observed order; it is not silently
substituted for this mask-only frame. No claim of exhaustive source-error
correction is made.

- [Readable edition](../../pages/228.md#edition-cases-military-p228-demobilization-fragment)
- [Exact inputs](inputs.json)
- [Per-position certificates](certificates.json)
- [Earlier three-part source edition](../neuhof_demobilization/README.md)

**Optional repeated-reference witness.** B1's original observed `X4GEH`
supplies the two missing labels in B2's `??GEH`, conditional on a shared
order reference. The [separate certificate](reference_witness.json) reaches
123/132 positions with two additional mask fills and no additional observed
substitution. It retains the neighboring `P680` / `2680` disagreement and
does not interpret the numbers. Both donor pairs are original observations.
Run `python experiments/p228_demobilization_fragment/verify_reference.py --verify`
to check the coordinate transfers and full witnesses under one unchanged square.

**Enclosure extension.** B1's fully observed `ANLGYX` also supplies the two
missing labels of B2's `ANLG??UJ`. The same verifier now preserves a separate
**125/132-position** layer: two further mask fills, with the same five observed
substitutions. Under the shared late-period numeral interpretation, this
reads **Anlg. 1 u. 2**. The original source pairs `AX` and `GX` support both
fills; the combined layer has 36 mask fills. It retains the order-reference
disagreement `P067` / `3067` and the seven remaining unknown positions.
