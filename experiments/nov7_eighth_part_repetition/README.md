# Unreadable eighth part: source and shared-cell reconstruction

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [source edition](../../cases/pages/155.md#edition-cases-radio-nov7-eighth-part-repetition) joins p155 C1 and C2 into a readable request to check and repeat an earlier eighth part. C1 requires an explicit one-coordinate exclusion from an overlong group; C2 is native and unaltered.

## Exact primary scope

| Quantity | Count |
| --- | ---: |
| Physical records | 2 |
| Printed source slots | 323 |
| Modeled coordinates | 322 |
| Raw fixed positions | 155 / 161 |
| Edited fixed positions | 157 / 161 |
| Observed-coordinate exclusions | 1 |
| Observed-coordinate substitutions | 0 |
| Source-mask fills | 2 |

All six single exclusions from `VGVXAA` are retained. Three need no further observed-coordinate substitution but yield different correlated station/reference labels. The displayed primary choice is therefore an example, not a uniquely recovered numerical interpretation.

The date field and the two reference unknowns are all cell `XA`. Both injective global assignments of the remaining labels 5/6 are witnessed across both parts, for twelve joint witnesses across six exclusions. The unknown in `AL?CHIS` is a separate source-mask problem and stays open.

## Reproduce

```sh
python experiments/nov7_eighth_part_repetition/verify.py --verify
python experiments/nov7_eighth_part_repetition/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier preserves the native odd source and its unpaired coordinate, checks all retained-source mappings and exact repair costs, compares both readable passages to their output streams, and independently re-encrypts all joint completions. PDF verification authenticates the source crop location and pixels.

Published Nov7–9 key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed OCR candidates are retained. Source review and conditional geometry/word edition: icekylinx and GPT-6 Astra Pro.
