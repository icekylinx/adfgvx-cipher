# Six-part Orient intelligence report

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

This edition recovers **p92 B1, p93 A2–A4 and p94 A5–A6**, a six-part
report received on 1 November 1918. Its matching headers read
`OSM v LP (4.20 p.m., November 1st)` and `(1/11) 0415 6 TEILE`.
The final signature is `ABT FREMDE HEERE`. The separate p92 A courier
message belongs to an earlier edition and is not included here.

The report corrects an earlier note, describes expected landings around
Alexandretta after convoy and ship observations, and relays an English
Orient report about fighting near `KALAT SHERGAT` on the Tigris. Its
reported sightings, forecasts and qualifications remain distinct in the
[case](../../cases/military/orient_intelligence.md).

## Recovery of the missing part boundaries

Earlier OCR merged all of p93 into one **977-slot** block. The source
explicitly marks three separate parts of **252, 394 and 328 coordinates**,
totaling 974. Applying the unchanged Nov1–3 key to those printed frames
gives **487 readable plaintext positions with no coordinate repairs**.
Their three complete readings encrypt back to their literal source
ciphertexts.

The source form `FLIEGERMELUNG` remains in part two; an apparent missing
`D` is not invented. Part three preserves the received `SZ` spellings
and the place field `XARSUSX`. Part four reads the anticipation of
imminent landing attempts in full, without correction.

## Complete edition

| Part | Printed slots | Raw fixed positions | Observed substitutions | Printed-erasure fills |
|---|---:|---:|---:|---:|
| p92 B1 | 328 | 164/164 | 3 | 0 |
| p93 A2 | 252 | 126/126 | 0 | 0 |
| p93 A3 | 394 | 197/197 | 0 | 0 |
| p93 A4 | 328 | 164/164 | 0 | 0 |
| p94 A5 | 368 | 183/184 | 1 | 1 |
| p94 A6 | 350 | 175/175 | 0 | 0 |
| **Total** | **2,020** | **1,009/1,010** | **4** | **1** |

B1's candidate repairs `DEUTSCQER` to `DEUTSCHER`, also witnessed by the
clear header, and `ODED` to `ODER`. A5 fills the printed dash in `GDGV-`
to a separator and repairs `7NGLISCHER` to `ENGLISCHER` with one observed
coordinate substitution. It does not relabel other occurrences of `7`.

All date, convoy, distance and military-unit fields remain unchanged.
The certificate inventories every numeral and `J/Q/Y` occurrence, the
single repaired digit within an ordinary word, the retained unusual
spelling and the report's qualifications. No source length, square cell
or transposition rank is changed.

## Historical and attribution limits

`ANSCHEINEND`, `ANGEBLICH` and the expectation of forthcoming landings
are retained. The edition is evidence of the report, not independent
verification of the sightings, convoy counts, landing attempts or
cavalry action. The earlier 30 October note mentioned in B1 is not
reconstructed by assuming what it must have said.

Parts one, five and six already had readable unreviewed repository
candidates. The prior single-frame p93 output was unreadable; its exact
body and frame length are frozen with the other prior candidates.
Lasry et al. discuss Foreign Armies intelligence generally, but the
bounded paper, dissertation and comment-thread checks did not locate
explicit discussion of this six-part body. This is a source recovery
and exact edition, not a claim to first historical decipherment.

## Reproduce

```bash
python experiments/orient_intelligence/verify.py --verify
python experiments/orient_intelligence/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks header and part agreement, independent mappings,
domains, edits, all unchanged fields and exact re-encryption. The optional
PDF check verifies the source hash and every retained crop's pixels.
The six proposed catalog rows are kept separate from the shared catalog.
