# ADFGVX Cipher

**Recovering the German radio traffic in Childs’s 1918 collection.**

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[Historical showcase](docs/historical-showcase.md) · [Read the messages](cases/README.md) · [Open problems](cases/open/README.md) · [Research](docs/research-status.md) · [Methods](docs/methods.md)

An army asks how to feed its men on the way home. A field treasury asks for
small banknotes by aircraft. Radio operators arrange a departure and ask
whether supper will be waiting. These messages preserve the practical life
of the German withdrawal from eastern and southeastern Europe in 1918.

We bring **all 679 ciphertext bodies into one source edition**, including the
22 original Lasry–Schmeh challenges. Each physical source has one catalogue
entry, with readable German where available, English explanation, the
original ciphertext and reproducible evidence. **Seven bodies remain OPEN**;
partial and conditional readings retain their own unresolved fields.

## Read the history

The [showcase](docs/historical-showcase.md) selects the most revealing recoveries.
Four connected studies follow the messages beyond the individual cipher:

| Historical study | What the traffic reveals |
|---|---|
| [An army trying to get home](docs/historical-studies/an-army-trying-to-get-home.md) | Withdrawal orders, the Romanian ultimatum, provisions at Arad and the prospect of internment. |
| [The Black Sea network runs in reverse](docs/historical-studies/black-sea-network.md) | Shipping routes, cargo, evacuation and the changing purpose of an overseas communications network. |
| [What retreat cost](docs/historical-studies/what-retreat-cost.md) | Cash shortages, banknote denominations, transport, contracts and assets left behind. |
| [Voices on the wireless](docs/historical-studies/voices-on-the-wireless.md) | Soldiers’ councils, civilian uncertainty, illness, departures and the personal exchanges inside military traffic. |

The studies connect the recovered wording with contemporary records. Each
case distinguishes an order from its execution and a reported event from
what independent evidence confirms.

## Our research contributions

- **A new shared key and partial decipherment for p153.** Our 18-column key
  fixes **60/66 positions** in [part 5](cases/p153a.md) without changing a source
  coordinate and supports the [rearguard-ammunition reading in part 6](cases/p153b.md).
  Independent exact checks cover widths 14–26; only width 18 fits the sixty-letter
  crib. [Discovery and verification](experiments/p153_recovery/README.md).
- **Lost text restored from independent receptions.** Our [Arad reconstruction](cases/military/danube_arad_witnesses.md)
  restores eleven lost coordinates and establishes the received **80000 MANN**
  wording. The [silk-resale witnesses](cases/finance/nov6_silk_resale_continuation.md)
  support all 135 continuation positions; the [November 14 copies](cases/radio/nov14_radio_retransmissions.md)
  restore an 85-coordinate prefix.
- **A complete source register and a connected historical edition.** We restore
  source boundaries, compare damaged copies and explain the military,
  financial and personal content. Earlier keys and decipherments retain their
  individual credits; our source reconstructions and interpretations are
  identified at the point of use.
- **Exact methods for damaged ciphertext.** Our [multi-witness decoder](experiments/parallel_decoder/README.md)
  optimizes all `2^42` minimum-cost p109 readings. The [joint loss decoder](experiments/p198_joint_exact/README.md)
  covers 8,670,506,592,384 five-loss witnesses per fixed complete key.
  Controls and exact bounds distinguish a promising candidate from an accepted reading.

[Current results and open work](docs/research-status.md) · [Evidence and experiments](experiments/README.md) · [Source images](sources/reviewed-crops.md)

<!-- READING-CATALOG:START -->
## Browse by source page

**679 physical sources, one entry each; 7 OPEN.** Page numbers refer to the printed Childs volume. [Complete page index](cases/pages/README.md).

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

Python 3.10 or later:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.catalog --check
python3 -m adfgvx.navigation --check
```

These check the core cipher certificates and current indexes. Source-specific
commands accompany each case; the [verification workflow](.github/workflows/verify.yml)
checks the wider edition. The [reading guide](docs/reading-conventions.md)
defines the presentation and evidence terms, and the [repository map](docs/repository-map.md)
locates the code and sources.

## Citation and reuse

**icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026).** Cite the relevant case
and commit with [CITATION.cff](CITATION.cff). Earlier decipherments, keys and
corrections retain their individual credits. Project code and editorial work
use [Apache-2.0](LICENSE); see [NOTICE](NOTICE) for third-party materials and
[CONTRIBUTING.md](CONTRIBUTING.md) for the contribution format.
