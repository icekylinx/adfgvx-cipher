# Source audit for 21 damaged or short bodies

Source review: **icekylinx and GPT-6 Astra Pro**. The literal audit was recorded on 3 November 2026; catalogue states below are current.

All 21 bodies have an explicit native transcription, slot count and reproducible original-PDF pixel reference. Each now has one canonical catalogue entry, including four OPEN sources with no accepted body reading. Source transcription and plaintext recovery remain separate results.

| Source | Native slots | Valid coordinates | Mask/invalid slots | Advertised length | Current state |
|---|---:|---:|---:|---:|---|
| p70_B1 | 206 | 199 | 7 | 206 | [OPEN](../cases/pages/070.md#edition-cases-open-p70-b1) |
| p71_A2 | 85 | 85 | 0 | 192 | [CONDITIONAL](../cases/pages/071.md#edition-cases-radio-p71-dc-machines-fragment-p71-a2) |
| p84_C | 118 | 111 | 7 | 244 | [CONDITIONAL](../cases/pages/084.md#edition-cases-radio-p84-mother-illness-extension) |
| p127_B2 | 152 | 104 | 48 | 152 | [OPEN](../cases/pages/127.md#edition-cases-open-p127-b2) |
| p137_A6 | 74 | 71 | 3 | Not printed | [CONDITIONAL](../cases/pages/137.md#edition-cases-military-p137-publicity-fragment-p137-a6) |
| p137_B | 135 | 133 | 2 | 138 | [CONDITIONAL](../cases/pages/137.md#edition-cases-radio-p137-station-staff-query-p137-b) |
| p145_A | 192 | 187 | 5 | Not printed | [OPEN](../cases/pages/145.md#edition-cases-open-p145-a) |
| p152_A2 | 128 | 125 | 3 | 128 | [PARTIAL](../cases/pages/152.md#edition-cases-military-p152-crossing-fragment-p152-a2) |
| p154_A2 | 118 | 118 | 0 | 162 | [CONDITIONAL](../cases/pages/154.md#edition-cases-military-p154-weisskirchen-fragment) |
| p163_A16 | 121 | 121 | 0 | Not printed | [CONDITIONAL](../cases/pages/163.md#edition-cases-military-p163-infrastructure-clause-p163-a16) |
| p164_D | 116 | 116 | 0 | 116 | [PARTIAL](../cases/pages/164.md#edition-cases-radio-p164-acknowledgment-p164-d) |
| p167_C1 | 132 | 130 | 2 | 132 | [CONDITIONAL](../cases/pages/167.md#edition-cases-radio-p167-mission-address-p167-c1) |
| p167_D | 187 | 183 | 4 | 190 | [CONDITIONAL](../cases/pages/167.md#edition-cases-people-p167-captain-dispatch-fragment-conditional-name-proposal) |
| p176_A6 | 160 | 74 | 86 | 160 | [PARTIAL](../cases/pages/176.md#edition-cases-military-p176-coal-train-fragment-p176-a6) |
| p194_D1 | 45 | 45 | 0 | 214 | [OPEN](../cases/pages/194.md#edition-cases-open-p194-d1) |
| p198_A | 247 | 237 | 10 | 244 | [CONDITIONAL](../cases/pages/198.md#edition-cases-naval-p198-shipping-query-p198-a) |
| p212_A4 | 197 | 197 | 0 | Not printed | [CONDITIONAL](../cases/pages/212.md#edition-cases-military-p212-medical-fragment-p212-a4) |
| p215_A | 390 | 372 | 18 | 392 | [CONDITIONAL](../cases/pages/215.md#edition-cases-military-p215-breslau-dispatch) |
| p215_B1 | 145 | 140 | 5 | 220 | [CONDITIONAL](../cases/pages/215.md#edition-cases-military-p215-train-departure-fragment-p215-b1) |
| p215_B3 | 219 | 200 | 19 | 234 | [CONDITIONAL](../cases/pages/215.md#edition-cases-military-p215-third-positions-fragment) |
| p219_C | 284 | 284 | 0 | 294 | [CONDITIONAL](../cases/pages/219.md#edition-cases-military-p219-kiev-unrest-p219-c) |

The 21 literal transcriptions contain **3,451 source slots: 3,232 valid coordinates and 219 printed masks or invalid glyphs**. Source annotations are retained separately from coordinates.

The main boundary corrections are p84 C’s final four-dash group, p145 A’s left-margin designator, p154 A2’s six-coordinate group, and p215 A’s final two-coordinate group. The p163 A16 label is a local identifier for the unlabelled fragment between printed parts 15 and 17. The p198 A C/G glyph alternatives, p215 B1 X/A alternative, and p219 C parentheses, duplicate prefix and jamming boundary remain explicit in the audit.

Searches proceeded across source-directed loss frames, published square/rank components, source-copy constraints retaining half-coordinates, and calibrated word or unknown-rank searches. A failed search does not exclude a key, a different original length or another loss model. The linked editions carry their own exact repair prices and complete witnesses; fluency scores do not establish historical text.

[Literal source audit and pixel recipes](../data/reviews/source_gap_audit_20261103.json) · [Live whole-material census](whole-material-coverage.md) · [Reading conventions](reading-conventions.md)

Reproduce the count/link checks with `python data/reviews/verify_source_gap_audit.py --verify`. Add `--pdf /path/to/childs.pdf` to authenticate the original PDF and compare all 21 recorded crop pixel digests. Without that argument, the verifier explicitly reports that original-PDF pixels were not checked.
