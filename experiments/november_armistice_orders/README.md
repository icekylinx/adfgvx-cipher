# Source editions of the p179 November instructions

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Five physical records produce two readable case pages:

- [Radio equipment moved east of the Rhine](../../cases/pages/179.md#edition-cases-radio-right-rhine-equipment), p179 A.
- [Citadel surrender, local armistice conditions and leave](../../cases/pages/179.md#edition-cases-military-armistice-and-leave-orders), p179 B/C/D1/D2.

The main source-recovery gains are A and D1. A's literal 271-coordinate
transcript includes a visibly cancelled duplicate `ADADG`; excluding those
five observed coordinates restores the advertised 266-coordinate frame and
a coherent radio-service order. Seven further observed-coordinate
substitutions repair its ordinary words. D1's actual 190-coordinate source,
instead of the older 191-slot OCR stream, gives a readable discharge-delay
notice with no source repair.

## Complete prices

| Record | Literal source slots | Working coordinates | Raw fixed labels | Edition fixed labels | Known substitutions | Observed coordinates excluded |
|---|---:|---:|---:|---:|---:|---:|
| p179 A | 271 | 266 | 128 / 133 | 130 / 133 | 7 | 5, at printed cancellation |
| p179 B | 158 | 158 | 76 / 79 | 76 / 79 | 1 | 0 |
| p179 C | 232 | 232 | 116 / 116 | 116 / 116 | 3 | 0 |
| p179 D1 | 190 | 190 | 91 / 95 | 91 / 95 | 0 | 0 |
| p179 D2 | 212 | 212 | 100 / 106 | 100 / 106 | 0 | 0 |
| **Total** | **1,063** | **1,058** | **511 / 529** | **513 / 529** | **11** | **5** |

Every received source slot is a valid coordinate. Remaining question marks
come from the partial keys; there are no source-erasure fills, added
coordinates, block moves or key changes. A is explicitly **not** a zero-edit
record: its five-coordinate exclusion is counted separately from its seven
substitutions.

The source label `U.S.` is left unexpanded, with no American-origin
inference. D1 retains the raw year form `1560U61`. D is explicitly headed
November 12 but reads with the published key named Nov13–15b; both are
retained without a conjectural chronology. C retains `BEDING` as an
abbreviation, and B's citadel is not assigned a city absent from its body.

Earlier unreviewed B/C/D2 body candidates and the prior period keys are
credited. A and D1 are source-recovery gains, without a universal
first-decipherment claim. Exact source rows, image metadata, all coordinate
prices and raw numeric/rare-letter inventories are recorded in the
[certificate](certificates.json).

```sh
python experiments/november_armistice_orders/verify.py --verify
python experiments/november_armistice_orders/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Default verification uses the existing independent column/domain/reencryption
helpers. The optional PDF check independently regenerates all five delivered
source crops and compares their dimensions, channels and pixels. Witness
completions prove arithmetic compatibility, not original numerical values.
