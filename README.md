# ADFGVX Cipher

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[Selected discoveries](docs/historical-showcase.md) · [Read the messages](cases/README.md) · [Original challenges](cases/README.md#the-original-22-challenges) · [Research](docs/research-status.md) · [Methods](docs/methods.md)

In the last weeks of 1918, German radio stations carried orders for withdrawal, requests for food and money, and brief enquiries after people trying to get home. Preserved in J. Rives Childs's collection, these messages record both the decisions of headquarters and the daily work of an army's departure.

This edition brings together **679 physical ciphertext sources**, including the **22 original Lasry–Schmeh challenges**. Each has one catalogue entry linking its German reading, English interpretation and source evidence. Seven sources remain [OPEN](cases/open/README.md); partial and conditional readings identify the passages still unresolved.

## Selected research contributions

Our work combines new cryptanalysis with the recovery of text from damaged or repeated receptions. These results materially extend what can be read in the collection.

| Result | What we recovered |
|---|---|
| **[A shared key for the p153 fragments](experiments/p153_recovery/README.md)** | A new eighteen-column key fixes **60 of 66 positions** in part 5 without changing the source and supports part 6's instruction to report the rearguard artillery's ammunition stock. |
| **[The Arad strength report](cases/military/danube_arad_witnesses.md#p168-e)** | A second reception restores eleven missing coordinates and establishes **80,000 men and 30,000 animals** in a request for provisions and trains. |
| **[The interrupted banknote instruction](cases/finance/crown_banknote_completion.md)** | A complete reception supplies nineteen absent tail coordinates, resolves the gap's location and corrects an earlier conjecture in the request for small-denomination notes. |
| **[The Caucasus silk-resale order](cases/finance/nov6_silk_resale_continuation.md)** | Comparison of independent receptions gives every position of the **135-position continuation** direct support, restoring an order to resell material whose transport could no longer be assured. |

The [research account](docs/research-status.md) gives the full results and methods; the [publication and attribution review](docs/historical-studies/README.md#what-this-edition-contributes) identifies our discoveries alongside earlier contributions.

## Historical studies

The [selected discoveries](docs/historical-showcase.md) introduce the recovered messages. Four studies examine them alongside contemporary maps, diaries, newspapers and diplomatic records.

| Study | Principal subjects |
|---|---|
| [An army trying to get home](docs/historical-studies/an-army-trying-to-get-home.md) | Arad provisions, Hungarian transit, the Romanian ultimatum and internment. |
| [The Black Sea network runs in reverse](docs/historical-studies/black-sea-network.md) | Supply cargoes, evacuation routes, *Asgard*'s movements and the proposed *Corcovado* sale. |
| [What retreat cost](docs/historical-studies/what-retreat-cost.md) | Crown airlift requests, banknote shortages, payment through Vienna and transport equipment. |
| [Voices on the wireless](docs/historical-studies/voices-on-the-wireless.md) | Radio authority, arrival enquiries, departures, medical personnel and civilian return. |

<!-- READING-CATALOG:START -->
## Browse by source page

Pages follow the printed Childs volume; the [complete index](cases/pages/README.md) lists each message.

| Printed source pages | Sources | OPEN |
|---|---:|---:|
| [pp. 56–74](cases/pages/050-074/README.md) | 47 | 2 |
| [pp. 75–99](cases/pages/075-099/README.md) | 64 | 0 |
| [pp. 100–124](cases/pages/100-124/README.md) | 94 | 0 |
| [pp. 125–149](cases/pages/125-149/README.md) | 80 | 2 |
| [pp. 150–174](cases/pages/150-174/README.md) | 133 | 1 |
| [pp. 175–199](cases/pages/175-199/README.md) | 111 | 2 |
| [pp. 200–224](cases/pages/200-224/README.md) | 121 | 0 |
| [pp. 225–230](cases/pages/225-249/README.md) | 29 | 0 |

<!-- READING-CATALOG:END -->

## Verify and contribute

The core verifier uses Python 3.10 or later:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.catalog --check
python3 -m adfgvx.navigation --check
```

Source-specific commands accompany the cases and [experiments](experiments/README.md); the [verification workflow](.github/workflows/verify.yml) checks the wider edition. See the [reading guide](docs/reading-conventions.md) for editorial terms, the [repository map](docs/repository-map.md) for code and sources, and [CONTRIBUTING.md](CONTRIBUTING.md) to contribute.

## Citation and reuse

**icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026).** Cite the relevant case and commit with [CITATION.cff](CITATION.cff). Earlier decipherments, keys and corrections retain their individual credits. Project code and editorial work use [Apache-2.0](LICENSE); [NOTICE](NOTICE) identifies third-party materials.
