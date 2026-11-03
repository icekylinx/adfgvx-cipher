# Caucasus ammunition: a request for loading instructions

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

The native p102 C frame asks whether ammunition still held at the reporting location should be loaded for the destination. The quantity is the literal **5280625** under the published Nov1–3 key. This source edition resolves three unknown labels in the earlier OCR reading; it uses no coordinate repair.

Prepared by **icekylinx and GPT-6 Astra Pro**. Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed p102 (PDF page105). The Nov1–3 square and column ranks are the published key credited to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. Earlier OCR bodies are retained in [prior evidence](../../experiments/nov1_ammunition_and_leave/prior_evidence.json); this is not a claim of first historical body recovery.

## p102 C

### Source and frame

**Source transcription — literal cleartext header:**

```text
C) POT v NKJ (1.00 a.m., November 3rd)
DEUTSCHE DELEG KAUK 1622 (1)
RICHI-262
```

The [full page](../../experiments/nov1_ammunition_and_leave/sources/p102_full.png) and [native C/D detail](../../experiments/nov1_ammunition_and_leave/sources/p102_C_D_detail.png) show all 262 coordinates, matching the advertised length. The source frame contains no masks, added slots or excluded coordinates.

| Layer | Fixed plaintext positions | Observed substitutions | Source fills | Added / excluded coordinates |
| --- | ---: | ---: | ---: | ---: |
| Raw output, native 262-coordinate frame | 131 / 131 | 0 | 0 | 0 / 0 |
| Edited output | Same as raw | 0 | 0 | 0 / 0 |

### Raw output

**Raw output — published Nov1–3 key, native source frame:**

```text
ZUDORTASRM1NR2078XLAGERNHIERNOCH5280625RUSSXISXDRAHTETOBMUNXNACHDORTVERLADENWERDENSOLLXMUVVERMITTLXSTELLESUEDOSTNR6829HITTMERXHPTMX
```

### Readable German

**Readable German — spacing and punctuation only; umlauts display their literal two-letter equivalents:**

> Zu dort. A. S. R. M. 1 Nr. 2078. Lagern hier noch 5280625 russ. I. S. Drahtet, ob Mun. nach dort verladen werden soll. M. U. V. Vermittl. Stelle Südost Nr. 6829. Hittmer, Hptm.

`ASRM1`, `RUSSXIS`, and `MUV` are retained literally. The readable display separates their letters but does not expand these abbreviations or identify an ammunition type. It does not insert thousands separators into `5280625`. The references `2078` and `6829`, and the signature `HITTMER`, require no digit or letter repair. No external identity is assigned to Hittmer.

The earlier OCR had coordinate masks at source indices 3, 12 and 256. Native inspection reads `G`, `D` and `G` there. These restore the missing labels in `52?0625`, `WERDE?` and `H?TTMER`. They are corrections to the earlier OCR transcription, not historical ciphertext fills.

### Evidence and limits

The [input transcription](../../experiments/nov1_ammunition_and_leave/inputs.json) preserves every source row, the published key and the exact readable display. The [certificate](../../experiments/nov1_ammunition_and_leave/certificates.json) maps each plaintext position to its two source coordinates, preserves all numeral labels, and checks every non-`X` label in the displayed German. The [standalone verifier](../../experiments/nov1_ammunition_and_leave/verify.py) re-encrypts the native plaintext to the full observed ciphertext. Its optional PDF mode also reproduces the source images exactly.

No historical inference changes the source, key, numerals or personal-name spellings. Punctuation and abbreviation segmentation are editorial choices, so grammatical attachment and full abbreviations may remain uncertain even when all cipher labels are fixed.
