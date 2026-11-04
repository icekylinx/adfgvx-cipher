# A shared digit reading from the Siegfried cancellation

**icekylinx and GPT-6 Astra Pro**

Two orders cancel Oberleutnant Siegfried’s posting to Turkey and assignment
to the Military Mission. The earlier [p135 A](../../cases/people/siegfried_assignment_cancellation.md)
reads reference **45610** with the Nov4–6 key. The later
[p161 C1](../../cases/people/military_mission_recalls.md) gives **4??10**
under Nov7–9: the two question marks are fully received pairs in the two
unassigned square cells, XA and VF.

If the two orders cite the same reference, **XA=5 and VF=6** is the sole
bijective assignment that agrees with the earlier number. The opposite
assignment gives 46510. All ten coordinates of each reference are observed.
The earlier reference precedes both permitted surplus-coordinate exclusions,
so its digits are unchanged by either source frame or the word repairs.

This comparison supports **26 conditional digit positions in fifteen source
parts**, with **no additional observed-coordinate substitution or mask
fill in the shared-digit layer**. A separate local date completion adds one
printed-mask fill and completes the Siegfried first part. The published
partial square and the existing source editions remain intact.

| Source | Conditional reading | Opposite assignment | New digit positions |
| --- | --- | --- | ---: |
| [p162 B1](../../cases/radio/map_sheet_request.md) | 50 copies; map scale 1:75,000 | 60 copies; 1:76,000 | 2 |
| [p160 B1](../../cases/radio/radio_equipment_sale_prices.md) | Siemens field 21600 | 21500 | 1 |
| [p160 B2](../../cases/radio/radio_equipment_sale_prices.md) | Reference 111?05 | 111?06 | 1 |
| [p160 C2](../../cases/radio/ringbahn_key_reuse.md) | Nach Chef 4 B 49859 | 49869 | 1 |
| [p160 D1](../../cases/people/awaloff_return_request.md) | Nr. 641; Telegramm Nr. 585 | 541; 686 | 3 |
| [p155 C1](../../cases/radio/nov7_eighth_part_repetition.md) | 25.10 | 26.10 | 1 |
| [p155 C2](../../cases/radio/nov7_eighth_part_repetition.md) | RM 5 Nr. 153303 | RM 6 Nr. 163303 | 2 |
| [p172 D2](../../cases/finance/staatsbank_accounting_cheques.md) | am 6. gesandte Cheks | am 5. | 1 |
| [p151 E2](../../cases/radio/nov9_operations_map_sheets.md) | AOK 11, 1d 7065 | 7056 | 2 |
| [p161 C1](../../cases/people/military_mission_recalls.md) | ZU2NR45610 | ZU2NR46510 | 2 |
| [p175 B2](../../cases/finance/hauptwechselamt_accounting.md) | am 6.; literal closing 892409116 | am 5.; 892409115 | 2 |
| [p167 C1](../../cases/radio/p167_mission_address.md) | Roem 5; KR 130615 | Roem 6; KR 130516 | 3 |
| [p167 D](../../cases/people/p167_captain_dispatch_fragment.md) | positions 41/49/91: 6/5/6 | 5/6/5 | 3 |
| [p168 E](../../cases/military/danube_arad_witnesses.md#p168-e) | footer RM 1C 186 GEH | RM 1C 185 GEH | 1 |
| [p159 A](../../cases/military/arad_provisions_partial.md) | footer RM 1C 186 GEH | RM 1C 185 GEH | 1 |

The extension to p167 and the two Arad copies adds eight positions to the
earlier seventeen-position set. The second apparatus-sale part adds one
further native XA pair, giving twenty-six gained pairs, all originally
observed. In the selected edited layers, p167 C1 reaches **66/66**, p167 D
**92/95**, and each Arad copy **136/136** fixed labels. Eleven of the fifteen
selected layers are label-complete under the shared assignment alone; p160
B2, p155 C1, p161 C1 and p167 D then retain one, one, one and three
source-mask positions respectively. The separate date completion below resolves the p161 mask.
Opaque fixed fields are not thereby interpreted.

The p167 D source has a fourth affected position, 77, where raw VF now reads
6. The existing word proposal separately changes that pair to T; it therefore
does not add another edited position. The verifier preserves all six retained
p167 frames, its optional Zimmermann layer, p167 C1's optional MIL separator,
and all eight Arad source maps. The raw p159 closing still reads **186 GLH**;
its seven-substitution common word layer separately adopts **186 GEH**.
These alternative views do not add physical records or positions to the total.

The same-reference relation is a documentary inference: the orders have
matching named personnel and cancellation language, but different wording
and receptions. It is stated once and propagated consistently through the
shared key. This alone does not resolve the date mask in `2X?1`, p155’s
`AL?CHIS` or other source erasures. The final p175 digit remains a literal
label; no date normalization is made.

## Completing the Siegfried date

The p161 C1 date-like field `2X?1` has native pair `?G` at plaintext 19,
with source origins 185/31 and domain **1GIKNY**. If the field is a numeric
day/month date, **1 is its only numerical choice**. The separate p161 D1
Osthoff order directly preserves `MKX2X11` in seven fully observed pairs.
That witness supports the format and month; the two orders are not copies.

Filling the printed dash at source **185 with F** gives `FG=1`, hence
**2.11**. It adds **one mask fill and no observed substitution**, taking
C1 from 101/102 to **102/102 conditional fixed labels**. Its full source
price becomes four observed substitutions and five printed-erasure fills.
Together with its unchanged 77-label second part, the Siegfried order has
**179/179 conditional fixed labels** and a complete readable German display
in [the case](../../cases/people/military_mission_recalls.md#conditional-complete-siegfried-order).

The final package therefore records **26 shared-key numeral gains plus one
local mask completion: 27 added fixed positions**. Twelve of its fifteen
selected edited layers become label-complete when both stated assumptions
are used. The raw domain and the opposite 46510 reference remain explicit;
the date completion by itself chooses no 5/6 assignment.

## Verify

```sh
python experiments/nov7_9_joint_digits/verify.py --verify
```

The standard-library verifier independently reconstructs the columns,
decodes both reference fields, tests both complete square assignments,
checks the fifteen retained source streams and identifies every newly fixed
position. It records whether each pair is fully observed in its own
original source, verifies the public conditional notes, and re-encrypts
complete witnesses for both assignments.

[Inputs](inputs.json) · [Certificate](certificates.json).
The period keys retain the credit of Lasry, Niebel, Kopal and Wacker.
The same optional 5/6 assignment was already supported by the
[6th Reserve Division identification](../p170_continuation/military_context.json)
and the [Corcovado office prefix](../corcovado_sale_terms/README.md).
The Siegfried reference supplies a separate documentary rationale; the local
propagation and source comparisons here are by icekylinx and GPT-6 Astra Pro.
