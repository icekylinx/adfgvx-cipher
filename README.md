# ADFGVX Cipher

**Recovering the German radio traffic in Childs’s 1918 collection.**

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**icekylinx and GPT-6 Astra Pro** · [Read the messages](cases/README.md) · [Research status](docs/research-status.md) · [Source images](sources/reviewed-crops.md) · [Methods](docs/methods.md) · [Repository map](docs/repository-map.md)

This project brings the **22 Lasry–Schmeh challenge entries and the wider collection into one source-reviewed edition**: readable German, English meaning, original ciphertext, exact reconstruction evidence and credited earlier work. The [whole-material census](docs/whole-material-coverage.md) identifies **679 ciphertext bodies across 175 log pages**.

## Our contributions

- **A new shared key and partial decipherment for p153.** The recovered 18-column key fixes 60 of 66 positions in [part 5](cases/p153a.md) without changing a source coordinate and supports the [rearguard-ammunition reading in part 6](cases/p153b.md). Independent exact checks cover every width from 14 through 26; only width 18 fits the sixty-letter crib. [Recovery and verification](experiments/p153_recovery/README.md).
- **A unified edition of the wider traffic.** Source review restores message boundaries, damaged groups and readable bodies across military, naval, radio, financial and personnel correspondence. The page tables below lead to every reviewed record. The [twelve instructional examples](experiments/childs_instructional_examples/README.md) are also fully reproduced.
- **Missing text recovered from independent copies.** The [November 14 transmissions](cases/radio/nov14_radio_retransmissions.md) restore an 85-coordinate prefix. The [silk-resale witnesses](cases/finance/nov6_silk_resale_continuation.md) jointly support all 135 continuation positions. The new [Arad witness](cases/military/danube_arad_witnesses.md) restores all eleven lost coordinates in p159, fixes **80000 MANN**, and narrows the entire declared source family to eight maps with one completed stream.
- **Exact tools for damaged ciphertext.** The [multi-witness decoder](experiments/parallel_decoder/README.md) optimizes all `2^42` minimum-cost p109 readings. The [joint loss decoder](experiments/p198_joint_exact/README.md) covers 8,670,506,592,384 five-loss witnesses per fixed complete key. Published controls measure which word and numeral ambiguities these methods resolve.

**p73, p170 A and p198 D remain wholly open.** All case pages distinguish raw recovery, explicitly repaired text and conditional interpretation using the shared [reading conventions](docs/reading-conventions.md).

<!-- READING-CATALOG:START -->
## Browse by source page

[Open the complete page index](cases/pages/README.md) or choose a range below. Each printed page has a short table of readings, status and credit.

### The 22 challenge entries

Original challenge identifiers are retained; p198 denotes section D.

| Printed source pages | Entries | Challenge identifiers |
|---|---:|---|
| [pp. 50–74](cases/pages/050-074/README.md) | 1 | [p73](cases/p73.md) |
| [pp. 100–124](cases/pages/100-124/README.md) | 3 | [p100](cases/p100.md), [p105](cases/p105.md), [p109](cases/p109.md) |
| [pp. 125–149](cases/pages/125-149/README.md) | 2 | [p132](cases/p132.md), [p146](cases/p146.md) |
| [pp. 150–174](cases/pages/150-174/README.md) | 8 | [p152](cases/p152.md), [p153a](cases/p153a.md), [p153b](cases/p153b.md), [p158](cases/p158.md), [p164a](cases/p164a.md), [p164b](cases/p164b.md), [p170](cases/p170.md), [p171](cases/p171.md) |
| [pp. 175–199](cases/pages/175-199/README.md) | 6 | [p176a](cases/p176a.md), [p176b](cases/p176b.md), [p187](cases/p187.md), [p187b](cases/p187b.md), [p189](cases/p189.md), [p198](cases/p198.md) |
| [pp. 200–224](cases/pages/200-224/README.md) | 2 | [p215](cases/p215.md), [p217](cases/p217.md) |

### Other ciphertexts — 637 reviewed entries

Numbered parts and received copies are listed individually, with their reviewed reading status.

**659 catalogue entries · 658 physical sources · 636 beyond the challenges.** The [source register](docs/catalogue-source-overlaps.md) accounts for 1 later-edition entry sharing an existing source.

| Printed source pages | Reviewed entries | Pages represented |
|---|---:|---:|
| [pp. 50–74](cases/pages/050-074/README.md) | 44 | 18 |
| [pp. 75–99](cases/pages/075-099/README.md) | 63 | 25 |
| [pp. 100–124](cases/pages/100-124/README.md) | 91 | 25 |
| [pp. 125–149](cases/pages/125-149/README.md) | 75 | 25 |
| [pp. 150–174](cases/pages/150-174/README.md) | 119 | 25 |
| [pp. 175–199](cases/pages/175-199/README.md) | 102 | 25 |
| [pp. 200–224](cases/pages/200-224/README.md) | 114 | 25 |
| [pp. 225–249](cases/pages/225-249/README.md) | 29 | 6 |

Source review and current research: **icekylinx and GPT-6 Astra Pro**. Each detailed entry credits its earlier readings and keys.
<!-- READING-CATALOG:END -->

## Explore the recovered traffic

| Subject | Selected editions |
|---|---|
| Military operations | [Romanian ultimatum report](cases/military/nov11_romanian_ultimatum_report.md), [Orient intelligence](cases/military/orient_intelligence.md), [Mackensen’s withdrawal](cases/military/mackensen_withdrawal_part2.md), [Hungarian armistice instructions](cases/military/hungarian_armistice_instructions.md) |
| Ships and evacuation | [Corcovado sale terms](cases/naval/corcovado_sale_terms.md), [Turkish tonnage](cases/naval/turkish_tonnage.md), [Black Sea routing](cases/military/black_sea_evacuation_routes.md) |
| Radio service | [Eilvese schedule](cases/radio/nov3_eilvese_traffic_schedule.md), [Ringbahn key instructions](cases/radio/nov6_ringbahn_key_witnesses.md), [Seifert witnesses](cases/radio/seifert.md) |
| Finance and procurement | [Crown airlift request](cases/finance/nov9_crown_airlift_and_embassy.md), [Military allowances](cases/finance/military_allowances.md), [ZITAG orders](cases/finance/zitag_purchase_orders.md) |
| People and diplomacy | [Constantinople civilians](cases/people/constantinople_civilians.md), [Polish representation in Tiflis](cases/caucasus/tiflis_appointment.md), [October Caucasus correspondence](cases/caucasus/october_caucasus.md) |

The [research status](docs/research-status.md) highlights current gains and open work. The [experiment index](experiments/README.md) and [review ledger](data/review_ledger.json) provide the complete method and attribution record. The [source-image gallery](sources/reviewed-crops.md) gives direct access to the 40 latest reviewed crops.

## Verify

Python 3.10 or later:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.catalog --check
python3 -m adfgvx.navigation --check
```

These commands check the core cipher certificates and reading indexes. Package-specific commands accompany each edition; the [verification workflow](.github/workflows/verify.yml) runs the full certificate suite. [Source-image verification](sources/reviewed-crops.md#verify) checks the delivered PNGs and can reproduce their pixels from the original scan.

## Citation and reuse

**icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026).** Cite the relevant case and commit with [CITATION.cff](CITATION.cff). Earlier decipherments, keys and corrections retain their individual credits. Project code and editorial work use [Apache-2.0](LICENSE); see [NOTICE](NOTICE) for third-party materials and [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution format.
