# Military-intendant addresses and responsibilities, p202 B

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**
The unchanged `Nov16-18` square and ranks are prior published work by
George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. Parts B2 and B3
already existed as unreviewed OCR-derived candidates in the p73 retrieval
corpus. This package adds the complete visual transcription, a conditional
opening-frame recovery, the final-part reading and exact editorial costs.

The four parts distinguish the Berlin Generalintendant's responsibilities
for organization, personnel and administrative finance from the
Generalintendant at `GRHQU`, responsible for supply transport and delivery,
clothing and equipment, meat provision, sutlery and wartime services.
The opening gives a proposed new Berlin address on Augsburger Strasse;
its number and the message's reference fields remain unresolved.

## Source and counted edition

The [whole section](sources/p202_B.png) is Childs printed p202, PDF p205.
The source advertises four lengths: **228, 220, 210, 224**. Manual counting
finds **223, 220, 210, 224** visible slots. Five received slots are masked:
a printed `Q`, a printed `R`, a heavy overprint and two faded glyphs.
The detailed crops and individual reasons are in [inputs.json](inputs.json).
No uncertain glyph is silently chosen from the expected plaintext.

| Part | Received slots | Working frame | Raw fixed positions | Edition fixed positions | Known-coordinate changes | Masked-slot fills | Added-slot fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | 223 | 228, conditional | 106 / 114 | 111 / 114 | 4 | 0 | 3 |
| B2 | 220 | 220 | 108 / 110 | 110 / 110 | 1 | 2 | 0 |
| B3 | 210 | 210 | 104 / 105 | 105 / 105 | 4 | 0 | 0 |
| B4 | 224 | 224 | 103 / 112 | 106 / 112 | 1 | 3 | 0 |
| **Total** | **877** | **882** | **421 / 441** | **432 / 441** | **10** | **5** | **3** |

The B1 representative inserts five unknown coordinates before received
index **145**, before printed group **30**. Three added coordinates are
filled by the proposed body; two remain unknown. This is a conditional
five-coordinate loss model. There are no deletions, block moves or changes
to the published square. The certificate distinguishes frame indices from
original-source indices and prices every change in the latter wherever
an original slot exists.

## The opening geometry remains conditional

All **224** insertion positions for a five-coordinate gap were examined,
including **46** printed-group boundaries or the final end position.
The [complete finite audit](gap_audit.json) retains every raw candidate,
fixed-position count and editorial price. The ordinary-word template
masks the Berlin address, its reference field and its street number.
Both templates were developed after reading candidates; they are not
independent cribs or blind controls.

| Finite comparison | Minimum known-coordinate changes | All tied gap positions, zero-based |
| --- | ---: | --- |
| Ordinary words, all positions | 2 | 142, 143 |
| Full proposed body, all positions | 3 | 143, 144 |
| Ordinary words, printed-group boundaries or end | 3 | 140 |
| Full proposed body, printed-group boundaries or end | 4 | 145 |

The earlier book and radio candidate-finding scores both favored position
146. Their [224 saved score rows](candidate_scores.json) are retained with
model hashes. These marginal scores can reward unknown characters, as
shown by the earlier p170 group-move controls. The different criteria do
not identify a unique original loss position. The main edition uses one
explicit group-boundary representative, and its common ordinary-language
body is much better determined than the layout or number fields.

## Reproduction

```sh
python experiments/military_intendant_remit/verify.py --verify
```

The default run checks the image hashes, unchanged published key, all
source/edition positions, repair prices, globally consistent completion
witnesses, and the complete 224-position conditional cost comparison.
The shared source reader independently reconstructs physical columns and
checks them against the project cipher implementation. Arbitrary complete
square/source witnesses are marked as such and are not original readings.

To also recompute all 448 saved language scores:

```sh
python experiments/military_intendant_remit/verify.py --verify \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin
```

An optional `--pdf /path/to/adfgvx-childs.pdf` verifies the complete source
PDF hash. The core certificate requires no language model or optimization.
The [readable case](../../cases/military/military_intendant_remit.md) separates
the proposed body, exact edits, source ambiguity and attribution limits.
