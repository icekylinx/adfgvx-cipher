# Conditional recovery of the p217 B1 train report

**icekylinx and GPT-6 Astra Pro** · [Read the edition](../../cases/pages/217.md#edition-cases-military-nov24-train-report)

A source-directed repeated-group model recovers a further part of the evening
report adjacent to the Budapest teleprinter message. The primary completion
reads `8 WEITERE ZUEGE ABGEROLLT` and `RD ANFANG OROSHAZA` without changing
an observed coordinate. Literal numerical labels remain unchanged.

The selected model excludes five observed coordinates from one genuinely
repeated `FXXXF` group and inserts five unknown slots near the damaged prefix.
Its 102 positions contain **76 fixed raw labels** before any fills.
Sixteen printed-mask fills and four added-slot fills give **96 fixed labels**.
A separately priced four-substitution word edition gives **99/102**, with
three exact unknown positions, and proposes `BEKESCSABA`.

## Complete declared geometry check

For each of the two duplicate origins, the verifier checks every integer
insertion boundary from 0 through 199 in the retained 199-slot stream.
The 400 prices are recomputed directly from the encoded template and native
observed half-pairs. Every minimum map, its fill costs and both resulting
edited streams are retained.

The zero-substitution template has 16 minimum maps. The canonical map
(delete source 45–49, add five slots at retained boundary 12) uses 20 fills;
the other seven gap positions at each duplicate origin use 21. The optional
word template has 20 minima at four observed substitutions, using 23 or 24
fills. A footer position differs between the two resulting streams. These
checks price the declared retrospective templates and do not establish a
unique historical corruption mechanism.

## Reproduce

```sh
python experiments/nov24_train_report/verify.py --verify
python experiments/nov24_train_report/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification checks the original source snapshot, unchanged published
key, full coordinate-origin map, native and conditional raw outputs, all edits
and fills, complete re-encryption witnesses, all 400 maps for both templates,
and the actual Markdown strings and readable quotations. The PDF option
authenticates the original scan and reproduces the reviewed crop pixels.

`inputs.json` keeps the source and assumptions. `certificates.json` contains
the source/pair and repair ledgers. `catalog_proposal.json` proposes only B1;
the already accepted B2 record is not added again. All machine indices are
zero-based.

Period-key credits remain with Lasry, Niebel, Kopal and Wacker and the 2017
key list. The preceding repository source review had checked this literal
body but kept it unread. The conditional recovery and exact enumeration here
are by **icekylinx and GPT-6 Astra Pro**.
