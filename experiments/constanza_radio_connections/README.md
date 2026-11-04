# Constanza naval-radio and telephone connections

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

This source edition recovers the four-part communications explanation on Childs p82 A1–A4 and the independent p80 B1/B2 copies of its first two parts. The message reports how telegrams for foreign stations are routed over German lines to Bucharest or Braila, and how the naval radio station is connected to the main and naval-department telephone exchanges. It describes those arrangements; it is not an independent test of their operation.

The [reading edition](../../cases/pages/080.md#edition-cases-radio-constanza-radio-connections) contains every raw and candidate string. [inputs.json](inputs.json), [certificates.json](certificates.json) and the [crops](sources/) retain all source coordinates, word repairs, source annotation and length discrepancy.

## Source-positive gains

The old OCR combined parts 1 and 2 and misplaced their boundaries. The corrected source boundaries recover their **245-position text**. Parts 3 and 4 were already substantially readable in unreviewed screens and are credited accordingly. The full message has 409 plaintext positions; the two additional physical copies add 245 repeated positions to the source edition, not 245 independent unique words.

Part 1 provides a useful length control. The p82 heading says `RICHI-342`, but there are exactly 242 printed coordinates. The separate p80 copy says `RICHI-242` and differs at only one coordinate. We decrypt the 242 observed coordinates and explicitly retain the apparent length-label error. We do not insert 100 hypothetical missing coordinates.

Part 2 provides a visible correction witness. In p80 B2, a supralinear **F** sits above typed **G** at source index 55. The literal baseline preserves G. The separate annotation layer applies F and becomes exactly identical to the independently typed p82 A2 ciphertext. The annotation's author and date are unknown; it is not described as a modern editorial correction or attributed to a named solver.

## All repairs

All indices are zero-based. The five ordinary-word candidate substitutions are:

| Record | Source index | Source → candidate | Result | Evidence |
|---|---:|:---:|---|---|
| p80 B1 | 94 | X → D | NAPH → NACH | Unchanged p82 A1 source |
| p80 B2 | 55 | G → F | FR9MD → FREMD | Supralinear F and typed p82 A2 |
| p80 B2 | 142 | G → X | PACH → NACH | Ordinary-word candidate; both copies have PACH |
| p82 A2 | 142 | G → X | PACH → NACH | Same common error, priced separately |
| p82 A3 | 64 | G → F | ANG9SCHLOSSEN → ANGESCHLOSSEN | Ordinary-word candidate |

The two copies' common `PACH` is not presented as an error corrected by copying a clean witness. After the annotation alone, it still remains. The raw 9 occurrences and their local repairs remain visible; no digit is globally reassigned. The repeated `13558`, `ROEMX1`, all reference numbers and all date labels are unchanged.

Both source groups have origin `0730 (30) 4 TEILE` and explicit numbered parts. Their receipt times differ: p80 says `6.20 p.m.` and p82 says `6.10 p.m.`, both on 30 October. The edition keeps both times.

## Reproducibility and attribution

Six physical records preserve 1,308 observed coordinates and 654 fixed plaintext labels. There are five substitutions, including one directly supported by the source annotation, and no erasures, insertions, deletions, rank changes or square changes. Fixed labels are reported separately from the four ordinary-word defects repaired in the reading layer.

Earlier repository candidate strings and hashes are frozen, including the defective merged frames and the readable later parts. A bounded check of the Lasry–Niebel–Kopal–Wacker paper, Lasry dissertation and cached 2017 discussion found general Constanza/callsign references, but no explicit discussion of this reference/switchboard body. That is not a proof of priority. The edition makes no claim of first historical decipherment and does not rely on a callsign-to-place assignment to select the plaintext.

From the repository root with Python 3.10 or later:

```sh
python experiments/constanza_radio_connections/verify.py --verify
python experiments/constanza_radio_connections/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The standard check independently rebuilds every inverse-transposition index and plaintext domain, verifies the source-copy differences, replays the annotation separately, checks all five repairs by full re-encryption, and reproduces the frozen certificate. The PDF option additionally requires PyMuPDF and Pillow and checks every crop against the hashed PDF pixel for pixel.
