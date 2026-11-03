# p176 A6: contextual coal-train fragment

**Partial proposal and source audit: icekylinx and GPT-6 Astra Pro.**

This source-retaining edition proposes `KOHLENZUEGENUEBERKLAUSENBURG`
at positions 0–27 and `GERECHNETWERDEN` at 41–55. The preceding A5 part
supplies grammatical context. The result is explicitly conditional and
partial: the 13-position routing field and full 24-position tail retain
the raw output, including their fixed labels and unresolved positions.

[Read the edition](../../cases/military/p176_coal_train_fragment.md)
· [Reviewed inputs](inputs.json)
· [Prior A5/A6 source snapshot](context_snapshot.json)
· [Per-position certificate and witnesses](certificates.json)

## Accounting and limits

The native 160-slot source has 74 valid observed coordinates and 86 printed
dashes. The unchanged Nov10–12 partial key fixes **14/80 raw positions**.
The contextual proposal fixes **48/80**, with **zero observed-coordinate
substitutions**, **44 printed-mask fills**, and **42 masks still unresolved**.
No insertion, deletion, reordering, source copying or key repair occurs.
The exact fill ledger and all 32 unresolved plaintext positions are retained.

The dative `N` at position 11 is contextual: an equal-price separator `X`
requires the alternative fill source 151 G instead of D. No routing place
is selected. Historical uniqueness is not asserted, and language-model
ranking is not a proof.

A5 is frozen separately with its prior raw and edited strings, three observed
substitutions, four source-mask fills and unresolved `VERPFLEG?Z` field.
It is excluded from all new-record totals. Its source assembly supports the
continuation hypothesis; no A5 ciphertext coordinate is copied into A6.

All five missing square cells remain distinct over digits 5–9. The verifier
checks all 120 completions and produces full source-retaining witnesses.
Each witness arbitrarily fills the 42 remaining coordinate masks with A;
these fills are compatibility devices and never enter the published partial
candidate. Both the common arithmetic and an independently constructed
column encoder verify the full round trips.

## Reproduce

```sh
python experiments/p176_coal_train_fragment/verify.py --verify
python experiments/p176_coal_train_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks the input/source snapshot, unchanged key, A5 prices,
all proposed mask fills and retained output intervals, the N/X alternative,
global injectivity, complete witness round trips, and every actual Markdown
raw, edited, earlier-reading, source and German display. The PDF option
checks the pinned original and all three crop recipes: header, A5 and A6.
Without that option it explicitly reports no source-pixel comparison.
Crop metadata uses external PDF references; no new image file is packaged.

The period key remains credited to Lasry, Niebel, Kopal and Wacker, and
Lasry's 2017 list. Earlier part-4 work by Norbert and Max Baertl keeps its
separate credit. The source review and contextual partial proposal are by
**icekylinx and GPT-6 Astra Pro**.
