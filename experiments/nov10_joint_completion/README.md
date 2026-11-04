# Completing the Nov10–12 numeral layer

Research and edition: **icekylinx and GPT-6 Astra Pro**.

A joint interpretation supplies **20 previously unknown labels in eleven source parts**, using twenty complete pairs already present in their sources. Ten parts then have no unknown labels in their existing edited streams. The Romanian mobilization report retains two masked positions. This extension adds no source changes; each part keeps its earlier repair costs and framing conditions.

The resulting readings include the **500** monitoring order, a **5.03 p.m.** Berlin departure, the **9 November** mobilization order, the **AOK 17 / AOK 18** correspondence, and completed naval and radio references. Literal problematic fields, including the crossing report’s `7 X 7 X VORM` and the accommodation report’s `13711`, are retained.

## Historical anchors and the two orders of the divisions

The published partial square lacks five digits. Its **120** bijective completions narrow in four explicit stages:

| Stage | Retained interpretation | Completions |
|---|---|---:|
| Published square | Missing labels are 5, 6, 7, 8, 9 | 120 |
| Office designation | Earlier Marineamt `A6S` interpretation: `XX=6` | 24 |
| Formation set | Earlier p176b identification of 217 and 219, without ordering them: `{XA,GF}={7,9}` | 4 |
| Army number | The final native `AOK1?` in p183 F names an accurately received German army HQ | 2 |
| Mobilization order | p180 B2’s `? X 11 ANGEORDNET` refers to the decree signed on 9 November | 1 |

The [Bundesarchiv’s formation guide](https://www.bundesarchiv.de/im-archiv-recherchieren/archivgut-recherchieren/nach-themen/armeen-armeekorps-und-divisionen-der-preussischen-armee-im-ersten-weltkrieg/) enumerates the First World War army headquarters as 1–19 except 13, 15 and 16. After the office and formation assignments, the final p183 F field has only **15 or 18** available. Reading it as an accurate army designation selects **18**, fixes `XG=8`, and leaves `FD=5`.

The [mobilization poster, museum inventory 1263](https://mvu.ro/product/afisul-prezinta-decretul-3179-din-27-octombrie-emis-de-regele-ferdinand-prin-care-a-proclamat-mobilizarea-generala-a-armatei-romane/), reproduces decree **3179**, dated **27 October 1918**. Its first mobilization day is printed as **28 October / 10 November**. The signature therefore falls on **9 November** in the same calendar as the German report. The [original poster image](sources/romanian_mobilisation_1263.jpg) was checked visually. Connecting the report to this decree selects `XA=9`; the same cell supplies its **9 Uhr abends**. The decree establishes the order’s date, not that later hour independently.

This reverses the previously proposed order of p176b’s two divisions to **219, 217**, retaining **6 R.D.D.** The earlier [French telegram and division-history review](../../data/reviews/p176b_unit_context.json) supports the formation set. It does not dictate the order of their appearance in the German cryptogram. The twenty-coordinate reconstruction and the original Prinz / GPT-6 Astra attribution remain in [p176b](../../cases/p176b.md). Its three already supplied historical digits are excluded from the twenty-position gain.

| Pair | Adopted conditional label | Rival before the decree association |
|---|---:|---:|
| FD | 5 | 5 |
| GF | 7 | 9 |
| XA | 9 | 7 |
| XG | 8 | 8 |
| XX | 6 | 6 |

Both complete squares and all resulting target texts are retained in the certificate. The two branches give p183 F **AOK17 / AOK18** and **AOK19 / AOK18**, respectively; p180 B2 has **9 November / 9 Uhr** and **7 November / 7 Uhr**. The museum date supports the first branch subject to the stated identification. Neither shared-square branch repairs an incorrectly received source label for free.

## Recovered labels and inherited costs

Counts compare each part’s previously displayed edited layer, including its earlier local office assignments, with this joint layer. “Native” describes the two observed coordinates of each added pair; a part’s larger frame or earlier word repairs may remain conditional.

| Source part | Fixed before → after / length | New pairs | Earlier observed changes / mask fills / added fills / excluded coordinates |
|---|---:|---:|---|
| [p172_B](../../cases/radio/seifert.md) | 19 → 20 / 20 | 1 | 0 / 0 / 0 / 0 |
| [p174_D](../../cases/radio/seifert.md) | 19 → 20 / 20 | 1 | 0 / 0 / 0 / 0 |
| [p173_A1](../../cases/naval/corcovado_sale_terms.md) | 120 → 121 / 121 | 1 | 6 / 0 / 0 / 0 |
| [p175_A2](../../cases/people/spa_berlin_delegates.md#p175-a2) | 51 → 52 / 52 | 1 | 1 / 0 / 0 / 0 |
| [p175_C2](../../cases/military/romanian_ultimatum_companions.md#p175-c2) | 102 → 104 / 104 | 2 | 1 / 0 / 0 / 0 |
| [p177_B3](../../cases/naval/turkish_tonnage.md) | 186 → 187 / 187 | 1 | 4 / 0 / 0 / 0 |
| [p178_A5](../../cases/naval/naval_armistice_order.md) | 159 → 161 / 161 | 2 | 2 / 0 / 0 / 0 |
| [p179_A](../../cases/radio/right_rhine_equipment.md) | 130 → 133 / 133 | 3 | 7 / 0 / 0 / 5 |
| [p179_B](../../cases/military/armistice_and_leave_orders.md) | 76 → 79 / 79 | 3 | 1 / 0 / 0 / 0 |
| [p180_B2](../../cases/military/nov11_romanian_mobilization_report.md#p180-b2) | 116 → 118 / 120 | 2 | 4 / 1 / 4 / 0 |
| [p183_F](../../cases/military/jaeger_accommodation_area.md#p183-f) | 112 → 115 / 115 | 3 | 1 / 2 / 0 / 0 |

The identical p172 B and p174 D strings are separate physical receptions; each has one native digit position. The p179 A exclusions belong to its printed cancellation. The p180 B2 tail remains a conditional five-slot extension, with four slots filled by its older word proposals and one left masked.

## Adverse raw consequences

The shared digits also label corrupted ordinary words. The certificate preserves every raw occurrence in the eleven selected parts, including `TAUSEN7`, `E7PFANGS`, `FU6OSTELLEN`, `AUFRECHTERHA9TEN` and `RUMA6N`. Their existing word repairs are separately listed. These occurrences do not become additional readable gains. The extension does not reclassify other corpus records or claim a newly recovered cipher key independent of the historical conditions.

## Reproduction

```sh
python experiments/nov10_joint_completion/verify.py --verify
```

The standard-library verifier reconstructs the inverse column order, every added pair’s two original source indices, all earlier substitutions and fills, and both competing complete readings. It performs **1,320 full-square roundtrips** across all 120 square completions of the eleven selected edited streams. Unresolved source masks receive arbitrary computational fillers only for those roundtrips. Digest-bound dependencies preserve the original source packages and published key; live case checks bind the displayed conditional streams.

[Inputs and source dependencies](inputs.json) · [Exact certificates](certificates.json). The published period key retains the credit to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. The formation interpretation retains the earlier Prinz / GPT-6 Astra credit; this edition establishes and propagates the conditional joint assignment.
