# Oderberg transport fragment and a troop-situation query

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Two additional physical records from the upper part of Childs p211 have source-reviewed readings.** The 176-coordinate second part is readable without repairs. A separate 68-coordinate query asks about the situation and the troops' behavior, with three word repairs. The lower three-part key-schedule message on the same page is [already cataloged separately](../radio/p211_key_schedule.md).

Prepared by **icekylinx and GPT-6 Astra Pro**. The unchanged published Nov19–21 key retains the credit of George Lasry and the research of Lasry, Niebel, Kopal and Wacker. The earlier OCR screen already recovered the complete second-part body; this edition supplies manual source review and exact accounting, without a first-decipherment claim.

| Record | Literal source coordinates | Raw fixed labels | Source edits | Geometry |
|---|---:|---:|---|---|
| p211 A2, upper section | 176 | 88/88 | None | Native frame |
| p211 B, upper section | 68 | 34/34 | 3 coordinate substitutions | Native frame |

Both lengths agree with the printed RICHI labels. No coordinate is inserted, deleted, excluded or reordered. “Fixed” means fixed under the published square; it does not independently authenticate numeral or reference labels.

## A2: the first part is explicitly missing

The upper section is headed **INTERCEPTED BY BRITISH STATIONS**, **20 November 1918**. The A header gives unknown sender and receiver, reception on **November 21**, and the message field **2317 (11/20)**. Immediately above the ciphertext it says **“1st TL missing”**, followed by **2 TL, RICHI-176**.

The literal 88-label reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ODERBERGKEINESCHWIERIGKEITENINDENWEGLEGENWIRDXXEMPFANGSBESTAETIGUNGXXOHLXRMJAJJ9JJOPXGEH
```

</details>

The surviving clause ends with “will place no difficulties in the way,” followed by a request to acknowledge receipt. Its beginning names Oderberg. The missing first part contains the subject and preceding context, so this fragment alone does not identify who made the undertaking, what complete route was involved, or a final permission decision. The closing `OHL X RMJAJJ9JJ OP X GEH` remains exactly as deciphered; no J or 9 is normalized into a different reference format.

The final glyph in printed group 26 is D, as confirmed by the enlarged source crop. It is retained as an observed coordinate, not treated as an erasure or a conjectural fill.

### Possible relationship to the Prague fragment on p209

The [p209 A1 edition](transport_and_disarmament_orders.md) is explicitly part 1 of a two-part message. Its final words are `AUFSTRECKETESCHEN`. This p211 part begins `ODERBERGKEINESCHWIERIGKEITENINDENWEGLEGENWIRD`. The two fragments therefore make a coherent **Teschen–Oderberg** route-name continuation, and both use the published Nov19–21 key.

That textual fit is useful, but the headers do not establish that these are the two parts of the same telegram:

| Evidence | p209 A1 | p211 A2 |
|---|---|---|
| Printed part | 1 of 2 | 2; first part explicitly missing |
| Sender/receiver | `ZO'N v LP` | Not recorded |
| Message field | `22.35 (19/11)` | `2317 (11/20)` |
| Reception date | November 19 | November 21 |

The relationship is therefore recorded as a **possible companion**, with the date and time mismatch retained. Neither package's frozen source is changed, and no complete combined message or definitive transport permission is asserted.

## B, upper section: situation and conduct of troops

This is the short B immediately below the transport fragment, before the horizontal division and the separate November 19 key-schedule message. Its header reads `ZON v LP (04.49 p.m., November 20th)`, `1645 (11/20)`, `RICHI-68`.

The unchanged source yields:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
WIELAGEDORTXWIRVERHALTANDERTRUPPAN
```

</details>

The editorial proposal is:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
WIELAGEDORTXWIEVERHALTENDERTRUPPEN
```

</details>

With spacing and punctuation: **“Wie Lage dort? Wie Verhalten der Truppen?”** It asks about the situation there and the behavior of the troops. The context does not identify which troops or location.

The proposal costs exactly three observed-coordinate substitutions, using zero-based indices:

| Source index | Printed → proposed | Affected word |
|---:|---|---|
| 22 | V → F | `VERHALTAN` → `VERHALTEN` |
| 23 | V → F | `TRUPPAN` → `TRUPPEN` |
| 34 | G → D | `WIR` → `WIE` |

All three are local word repairs under the unchanged square. There are no source-mask fills or additional plaintext characters.

## Evidence and reproduction

The [inputs](../../experiments/prague_route_and_situation/inputs.json) preserve both diplomatic transcriptions, all header fields, the published key provenance and four source crops. The [certificates](../../experiments/prague_route_and_situation/certificates.json) record every plaintext pair's source coordinates and all three repairs. The [earlier candidate snapshot](../../experiments/prague_route_and_situation/prior_evidence.json) preserves the prior complete A2 reading.

```bash
python experiments/prague_route_and_situation/verify.py --verify
python experiments/prague_route_and_situation/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default verifier uses only the Python standard library. Optional PyMuPDF verification checks the exact source PDF hash and crop pixels. The [experiment README](../../experiments/prague_route_and_situation/README.md) states the finite scope and the unresolved relationship between the two transport fragments.
