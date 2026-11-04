# Mackensen withdrawal report: source edition and ninth-part assembly

Prepared by **icekylinx and GPT-6 Astra Pro**. Read the
[full source edition](../../cases/pages/113.md#edition-cases-military-mackensen-withdrawal-report).

This package audits twelve surviving physical parts of the thirteen-part
November 3 report. Childs and Lasry et al. retain the historical decipherment
and prior-body credits. The separately received p113 B9 joins the gap marked
on p115 and in the published Table 3; its 108 labels need no source edits.
Part 2 remains absent. Part 13 remains raw-only:38 of 111 fixed labels and no
conjectural fill of its 62 missing tail coordinates.

The 2,838 literal slots yield1,451 positions under stated geometry:1,334 raw
labels and 1,374 in the conservative edition. There are25 observed-coordinate
substitutions,40 source-mask fills and two modeled missing-coordinate fills.
The Nov1–3 key, all received ordering and all source values remain in their
separate original layer.

All 220 one-loss boundaries for part 11 and 238 for part 12 are costed. The
part 11 zero-substitution boundary 102 is distinct from the visibly short
group at 110. A separate manual source check confirms that tension. Part 12
has four minimum boundaries 141–144, so no unique loss site is claimed.
Retrospective masking tests, all raw tied readings, prior OCR candidates,
rare-label inventories and arbitrary source-preserving forward witnesses
remain available in the package.

```sh
python experiments/mackensen_withdrawal_report/verify.py --verify
python experiments/mackensen_withdrawal_report/verify.py --verify --pdf /path/to/childs.pdf
```

The first command is standard-library only. The optional PDF mode requires
PyMuPDF and Pillow and checks all six images against the pinned source PDF.
