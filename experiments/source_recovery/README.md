# Source-guided reading improvements

**icekylinx and GPT-6 Astra Pro · ADFGVX Cipher · 2 November 2026**

## p146: delete a literal duplicate, retain the received coordinates

The source prints two adjacent `XAAXV` groups at zero-based offsets 220 and 225. Delete either copy and insert a five-coordinate gap at offset 45, as in the earlier missing-group approach. The 244-slot result retains **239 observed coordinates without substitution**, fixes **117/122 plaintext positions**, and leaves exactly **6^5 = 7,776** possible completions.

The most likely fill `AAXAA` produces:

> FUNKSTELLE KERTSCH ERHAELT AB 12.[11] RUFNAMEN RICHARD EMIL KARL. FUNKSTELLEN DORTIGEN BEREICHS BENACHRICHTIGEN. NACHRICHTENCHEF 4BG7834

The fill supplies `L, 1, N, E, F`; the bracketed month is conditional on ordinary date notation. The missing group is inferred, not visibly marked in the scan. The closing reference remains uninterpreted.

Norbert's 2017 repair inserted `FVXAA` and replaced the ten-coordinate block `XAAXVXAFDX` with `XAAXX`. The new repair instead retains the observed `XAFDX` intact and deletes the adjacent repeated `XAAXV`. Its four changed repaired coordinates all lie inside the earlier reconstructed material. This is a more transparent repair of an earlier-readable body, not discovery of a new cipher key.

For this complete proposed plaintext, exhaustive comparison of every five-coordinate deletion and insertion finds eighteen exact alignments: deletion starts 219–227 and insertion starts 44 or 45. Their ambiguity comes from repeated source symbols. The two alignments on printed group boundaries delete either of the identical groups and insert `AAXAA` at 45.

See the [case](../../cases/p146.md), [certificate](../../data/certificates/p146_duplicate_group.json), and [independent review](../../data/reviews/p146_duplicate_independent.json).

## p109: use the neighboring imperfect witness

Printed p109 B and the challenge's section D are near-parallel 248-position ciphertexts after Norbert's earlier D repair. B has six erasures; of its 242 known coordinates, 200 agree with D and 42 disagree. Its raw reading supports `SAVA / UEBERGANG` and `BELGRAD ERKANNT`, improving the earlier `UNTERBRINGUNG` and `BELGRADER KAVV` interpretations.

The readable 124-character proposal still needs 23 coordinate changes relative to each witness. Under a shared-plaintext hypothesis, 42 total substitutions are unavoidable; the proposal needs 46. The additional four occur at three plaintext positions. The different timestamps and endings remain unresolved, and the exact common-plaintext hypothesis is not asserted as historical fact.

See the [case](../../cases/p109.md), [source comparison](../../data/certificates/p109_parallel.json), and [complete change maps](../../data/certificates/editorial_readings.json).

## Reproduce

```sh
python3 experiments/editorial_review/build_certificate.py
python3 experiments/source_recovery/build_certificates.py
python3 -m adfgvx.editorial
python3 -m adfgvx.source_recovery
```

Both checks are also included in `python3 -m adfgvx.verify`. The encoder, transposition, and domain calculations are cross-checked against the separate arithmetic implementations in `adfgvx.cipher` and `adfgvx.prior`.
