# Two complete multipart messages from p205

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Six source-checked parts form two readable messages: [a request for thirty million kroner](../../cases/other/p205_A.md), with an initial payment of five million, and [naval reporting instructions](../../cases/other/p205_B.md) after dissolution of the Seekriegsleitung. All **1,514 printed coordinates** are preserved in the analytical source layers. The unchanged published Nov16–18 partial square directly fixes **750 of 757 plaintext positions**. Four separate one-coordinate editorial changes produce the most likely readings; six remaining digit positions are not filled.

| Message | Parts | Coordinate slots | Directly fixed plaintext | Editorial changes |
|---|---:|---:|---:|---|
| p205 A | 4 | 972 | 481/486 | `Z2R → ZUR`, `ETAPPENVWRWALTUNG → ETAPPENVERWALTUNG`, `BERL2N → BERLIN`; one source coordinate each |
| p205 B | 2 | 542 | 269/271 | The initial `?IND → SIND` requires one source-coordinate substitution; an unknown square-cell assignment cannot supply `S` |

The six unresolved positions after the four editorial changes are reference digits. They share the same injective square and are not six independent free choices. Every marginal domain and square-cell index is retained in [p205_readings.json](p205_readings.json).

## Sources and arithmetic

[p205_inputs.json](p205_inputs.json) contains the complete groups, headers, source-image hashes, OCR differences and every proposed correction. [The first crop](sources/p205_A.png) contains all four financial parts; [the second](sources/p205_B.png) contains both naval parts. The exact source PDF hash is recorded; the complete book is not redistributed.

The builder preserves the raw source and separately calculates the changes for each editorial proposal. It also produces one arbitrary completion solely as a reversible arithmetic witness. That completion is never treated as a historical key or used to fill the reader-facing digits.

The separate audit imports the project cipher functions, compares all direct readings and marginal domains, verifies every letter-to-coordinate pair, confirms the unchanged key against the main catalogue, and independently checks each editorial source cost and the six unresolved positions.

```sh
python3 experiments/corpus_joint/build_readings.py \
  experiments/corpus_joint/p205_inputs.json \
  experiments/corpus_joint/p205_readings.json --verify
python3 experiments/corpus_joint/verify_p205.py
```

The period-key recovery retains the authorship documented in [data/keys.json](../../data/keys.json). The present contribution is source assembly, verification, repair accounting and a readable edition, with no claim to first historical decipherment of these messages.
