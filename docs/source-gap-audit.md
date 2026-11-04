# Review of the 21 source gaps

**icekylinx and GPT-6 Astra Pro · 3 November 2026**

This audit covers the 21 physical bodies outside the readable catalogue at `f3badb0`. All 21 have a fresh source transcription, an explicit slot count and a reproducible original-PDF pixel reference. A source audit alone does not turn an unread body into a recovered message. The edition column below uses the current catalogue and includes partial and conditional readings.

| Source | Native slots | Valid coordinates | Mask/invalid slots | Advertised length | Current edition |
|---|---:|---:|---:|---:|---|
| p70_B1 | 206 | 199 | 7 | 206 | No accepted edition |
| p71_A2 | 85 | 85 | 0 | 192 | [Partial/conditional edition](../cases/radio/p71_dc_machines_fragment.md#p71-a2) |
| p84_C | 118 | 111 | 7 | 244 | [Partial/conditional edition](../cases/radio/p84_mother_illness_extension.md) |
| p127_B2 | 152 | 104 | 48 | 152 | No accepted edition |
| p137_A6 | 74 | 71 | 3 | Not printed | [Partial/conditional edition](../cases/military/p137_publicity_fragment.md#p137-a6) |
| p137_B | 135 | 133 | 2 | 138 | [Partial/conditional edition](../cases/radio/p137_station_staff_query.md#p137-b) |
| p145_A | 192 | 187 | 5 | Not printed | No accepted edition |
| p152_A2 | 128 | 125 | 3 | 128 | [Partial/conditional edition](../cases/military/p152_crossing_fragment.md#p152-a2) |
| p154_A2 | 118 | 118 | 0 | 162 | [Partial/conditional edition](../cases/military/p154_weisskirchen_fragment.md) |
| p163_A16 | 121 | 121 | 0 | Not printed | [Partial/conditional edition](../cases/military/p163_infrastructure_clause.md#p163-a16) |
| p164_D | 116 | 116 | 0 | 116 | [Partial/conditional edition](../cases/radio/p164_acknowledgment.md#p164-d) |
| p167_C1 | 132 | 130 | 2 | 132 | [Partial/conditional edition](../cases/radio/p167_mission_address.md#p167-c1) |
| p167_D | 187 | 183 | 4 | 190 | [Partial/conditional edition](../cases/people/p167_captain_dispatch_fragment.md#p167-d) |
| p176_A6 | 160 | 74 | 86 | 160 | [Partial/conditional edition](../cases/military/p176_coal_train_fragment.md#p176-a6) |
| p194_D1 | 45 | 45 | 0 | 214 | No accepted edition |
| p198_A | 247 | 237 | 10 | 244 | [Partial/conditional edition](../cases/naval/p198_shipping_query.md#p198-a) |
| p212_A4 | 197 | 197 | 0 | Not printed | [Partial/conditional edition](../cases/military/p212_medical_fragment.md#p212-a4) |
| p215_A | 390 | 372 | 18 | 392 | [Partial/conditional edition](../cases/military/p215_breslau_dispatch.md) |
| p215_B1 | 145 | 140 | 5 | 220 | [Partial/conditional edition](../cases/military/p215_train_departure_fragment.md#p215-b1) |
| p215_B3 | 219 | 200 | 19 | 234 | [Partial/conditional edition](../cases/military/p215_third_positions_fragment.md) |
| p219_C | 284 | 284 | 0 | 294 | [Partial/conditional edition](../cases/military/p219_kiev_unrest.md#p219-c) |

The 21 literal transcriptions contain **3,451 source slots: 3,232 valid coordinates and 219 printed masks or invalid glyphs**. Source annotations are retained separately from coordinates.

The main boundary corrections are p84 C’s final four-dash group, p145 A’s left-margin designator, p154 A2’s six-coordinate group, and p215 A’s final two-coordinate group. The p163 A16 label is a local identifier for the unlabelled fragment between printed parts 15 and 17. The p198 A C/G glyph alternatives, p215 B1 X/A alternative, and p219 C parentheses, duplicate prefix and jamming boundary remain explicit in the audit.

Searches proceeded across source-directed loss frames, published square/rank components, source-copy constraints retaining half-coordinates, and calibrated word or unknown-rank searches. A failed search does not exclude a key, a different original length or another loss model. The linked editions carry their own exact repair prices and complete witnesses; fluency scores do not establish historical text.

[Literal source audit and pixel recipes](../data/reviews/source_gap_audit_20261103.json) · [Live whole-material census](whole-material-coverage.md) · [Reading conventions](reading-conventions.md)

Reproduce the count/link checks with `python data/reviews/verify_source_gap_audit.py --verify`. Add `--pdf /path/to/childs.pdf` to authenticate the original PDF and compare all 21 recorded crop pixel digests. Without that argument, the verifier explicitly reports that original-PDF pixels were not checked.
