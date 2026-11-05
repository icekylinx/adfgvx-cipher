# ADFGVX Cipher

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[By page](#browse-by-printed-page) · [By subject](topics/README.md) · [Historical research](docs/historical-studies/README.md) · [Chronology](docs/historical-studies/chronology.md) · [Discoveries](docs/historical-showcase.md)

German military radio traffic from the closing months of 1918 records withdrawal, supply, finance and changing command authority. This edition brings together the ciphertexts preserved by J. Rives Childs and historical studies based on their recovered contents.

The collection comprises **679 physical ciphertexts on 175 printed pages**, including the 22 original Lasry–Schmeh challenges. Seven sources remain [OPEN](topics/open.md).

<!-- READING-CATALOG:START -->
## Browse by printed page

Choose a range to see its pages and message subjects. Each page opens its complete ciphertexts, readings and source explanations.

| Printed pages | Sources |
| --- | ---: |
| [pp56–74](cases/pages/050-074/README.md) | 47 |
| [pp75–99](cases/pages/075-099/README.md) | 64 |
| [pp100–124](cases/pages/100-124/README.md) | 94 |
| [pp125–149](cases/pages/125-149/README.md) | 80 |
| [pp150–174](cases/pages/150-174/README.md) | 133 |
| [pp175–199](cases/pages/175-199/README.md) | 111 |
| [pp200–224](cases/pages/200-224/README.md) | 121 |
| [pp225–230](cases/pages/225-249/README.md) | 29 |

<!-- READING-CATALOG:END -->

## Historical research

| Study | Historical findings |
| --- | --- |
| **[Withdrawal, transit and internment](docs/historical-studies/an-army-trying-to-get-home.md)** | Provisioning at Arad, the armistice transit clock and negotiations with territorial authorities connect the means of withdrawal with its changing political conditions. |
| **[Black Sea shipping and disposal](docs/historical-studies/black-sea-network.md)** | A routing order and its numbered amendment trace a changed destination; diaries and registers place evacuation voyages and a proposed ship sale in a wider record. |
| **[Cash, procurement and liquidation](docs/historical-studies/what-retreat-cost.md)** | Orders to stop buying coexist with demands for pay, small banknotes and local payout. Stranded goods become subjects of resale and redemption. |
| **[Radio authority and personnel](docs/historical-studies/voices-on-the-wireless.md)** | Station handovers, interrupted links, disarmament conditions and traffic transfers show how communications service depended on control of people and equipment. |
| **[Vehicles and the stages of departure](docs/historical-studies/transport-and-demobilisation.md)** | Readiness, waiting, equipment transfer and reported departure appear as separate stages; one truck can leave while personnel remain behind. |

The [historical research guide](docs/historical-studies/README.md) classifies the sources and comparisons. The [chronology](docs/historical-studies/chronology.md) distinguishes dates of events, orders, transmission and interception.

## Selected recoveries

<a id="what-our-recoveries-add"></a>

| Discovery | Result |
| --- | --- |
| **[The p153 shared key](experiments/p153_recovery/README.md)** | A new eighteen-column key fixes **60 of 66 positions** in part 5 without changing the source and supports part 6's instruction to report the rearguard artillery's ammunition stock. |
| **[The Arad strength report](cases/pages/168.md#source-p168-e)** | A second reception restores eleven absent coordinates and establishes **80,000 men and 30,000 animals** in the request for provisions and trains. |
| **[The small-banknote instruction](cases/pages/195.md#edition-cases-finance-crown-banknote-completion)** | A complete reception supplies nineteen absent tail coordinates, locates the interruption and corrects an earlier conjecture. |
| **[The Caucasus silk-resale order](cases/pages/144.md#edition-cases-finance-nov6-silk-resale-continuation)** | Independent receptions give all **135 positions** of the continuation direct support, restoring an instruction to resell goods whose transport could no longer be assured. |

The [research record](docs/research-status.md) gives the exact cryptanalytic results. The [edition and attribution account](docs/edition-and-attribution.md) identifies our contributions alongside earlier keys, decipherments and historical publications.

## Sources and verification

[Childs and the source collection](sources/README.md) · [Original challenges](topics/README.md#original-challenges) · [Reading conventions](docs/reading-conventions.md) · [Repository map](docs/repository-map.md)

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.catalog --check
python3 -m adfgvx.page_editions --check
```

Source-specific checks accompany the editions and [experiments](experiments/README.md). The [verification workflow](.github/workflows/verify.yml) checks the collection; [CONTRIBUTING.md](CONTRIBUTING.md) describes how to extend it.

**icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026).** Cite a source edition or study and its commit using [CITATION.cff](CITATION.cff). Earlier work retains its individual attribution. Project code and editorial work use [Apache-2.0](LICENSE); [NOTICE](NOTICE) identifies third-party materials.
