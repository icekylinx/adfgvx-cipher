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

This comparison supports **17 conditional digit positions in ten source
parts**, with **no additional observed-coordinate substitution or mask
fill**. It leaves the published partial square and the existing source
editions intact.

| Source | Conditional reading | Opposite assignment | New digit positions |
| --- | --- | --- | ---: |
| [p162 B1](../../cases/radio/map_sheet_request.md) | 50 copies; map scale 1:75,000 | 60 copies; 1:76,000 | 2 |
| [p160 B1](../../cases/radio/radio_equipment_sale_prices.md) | Siemens field 21600 | 21500 | 1 |
| [p160 C2](../../cases/radio/ringbahn_key_reuse.md) | Nach Chef 4 B 49859 | 49869 | 1 |
| [p160 D1](../../cases/people/awaloff_return_request.md) | Nr. 641; Telegramm Nr. 585 | 541; 686 | 3 |
| [p155 C1](../../cases/radio/nov7_eighth_part_repetition.md) | 25.10 | 26.10 | 1 |
| [p155 C2](../../cases/radio/nov7_eighth_part_repetition.md) | RM 5 Nr. 153303 | RM 6 Nr. 163303 | 2 |
| [p172 D2](../../cases/finance/staatsbank_accounting_cheques.md) | am 6. gesandte Cheks | am 5. | 1 |
| [p151 E2](../../cases/radio/nov9_operations_map_sheets.md) | AOK 11, 1d 7065 | 7056 | 2 |
| [p161 C1](../../cases/people/military_mission_recalls.md) | ZU2NR45610 | ZU2NR46510 | 2 |
| [p175 B2](../../cases/finance/hauptwechselamt_accounting.md) | am 6.; literal closing 892409116 | am 5.; 892409115 | 2 |

The same-reference relation is a documentary inference: the orders have
matching named personnel and cancellation language, but different wording
and receptions. It is stated once and propagated consistently through the
shared key. The later date mask in `2X?1`, p155’s `AL?CHIS` and every other
source erasure remain unresolved. The final p175 digit remains a literal
label; no date normalization is made.

## Verify

```sh
python experiments/nov7_9_joint_digits/verify.py --verify
```

The standard-library verifier independently reconstructs the columns,
decodes both reference fields, tests both complete square assignments,
checks the ten retained source streams and identifies every newly fixed
position. It records whether each pair is fully observed in its own
original source, verifies the public conditional notes, and re-encrypts
complete witnesses for both assignments.

[Inputs](inputs.json) · [Certificate](certificates.json).
The period keys retain the credit of Lasry, Niebel, Kopal and Wacker;
this reference comparison and its propagation are by icekylinx and
GPT-6 Astra Pro.
