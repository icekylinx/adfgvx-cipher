# Explicit editorial reading audit

**icekylinx and GPT-6 Astra Pro · ADFGVX Cipher · 2 November 2026**

The [certificate](../../data/certificates/editorial_readings.json) records readable proposals separately from the retained earlier decipherments. Every additional coordinate change is mapped through the earlier repair and the transposition.

| Case | Reading under review | Changes relative to the earlier reconstructed text |
| --- | --- | --- |
| [p109](../../cases/pages/109.md#edition-cases-p109) | Sava crossing; another enemy division observed toward Belgrade | 22 plaintext positions, 23 coordinates; supported by a separately reviewed near-parallel |
| [p132](../../cases/pages/132.md#edition-cases-p132) | `FUER`, `FUENFTER`, `GEBET VORHER` | Three plaintext positions, three coordinates; `VORHER` was already proposed by Norbert in comment 40, 12 March 2017 |
| [p146](../../cases/pages/146.md#edition-cases-p146) | `ERHAELT AB 12.11 RUFNAMEN` | Four plaintext positions, four coordinates, all inside the earlier reconstructed blocks |

The [source-recovery report](../source_recovery/README.md) gives the stronger p146 model: a literal duplicate deletion and a missing-group fill preserve all 239 retained source coordinates. The p132 sender-error model remains explicit; the proposed text cannot be encrypted as an ordinary even-length message without restoring the separately modeled extra V before transposition.

```sh
python3 -m adfgvx.editorial
```

This checks arithmetic and attribution boundaries. It does not establish that a conjectured word or date was historically transmitted.
