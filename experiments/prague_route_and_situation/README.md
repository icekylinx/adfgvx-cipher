# Upper p211: Oderberg fragment and troop-situation query

Prepared by **icekylinx and GPT-6 Astra Pro**. Published **Nov19–21** key and earlier research retain their separate credit. See the [readable source edition](../../cases/military/prague_route_and_situation.md).

This package adds two physical source records, both with native, even-length frames:

| Record | Source coordinates | Raw labels | Substitutions | Source fills/length changes |
|---|---:|---:|---:|---:|
| p211 A2, upper | 176 | 88/88 | 0 | 0 |
| p211 B, upper | 68 | 34/34 | 3 | 0 |
| **Total** | **244** | **122/122** | **3** | **0** |

A2 is explicitly printed as the second part with **“1st TL missing.”** The earlier OCR screen already recovered its entire body. Its first word is ODERBERG and the surviving clause promises no difficulties, followed by an acknowledgment request and the literal `OHLXRMJAJJ9JJOPXGEH` closing. The missing first part is not supplied by inference.

There is a useful but unproved relationship to p209 A1, whose final text is `AUFSTRECKETESCHEN`: the two fragments form a coherent route-name continuation and have complementary part numbers. The p209 message field is `22.35 (19/11)` with reception November 19; p211 has `2317 (11/20)`, reception November 21 and no recorded callsigns. These differences remain explicit. No same-telegram identity, joined full message or operative permission is certified.

Upper B reads `WIELAGEDORTXWIRVERHALTANDERTRUPPAN`. Three observed-coordinate substitutions give the proposal `WIELAGEDORTXWIEVERHALTENDERTRUPPEN`. No printed character is removed to improve the sentence. The separate lower B key-schedule message on p211 is already cataloged and is not duplicated here.

## Verification

The standalone verifier reconstructs every plaintext pair by sorting row-major interim indices into transmitted order. A separate column-slice encryption direction proves the raw and edited round trips. It checks literal row counts, all three repair coordinates, unchanged known numeral labels, all image hashes and the prior-candidate snapshot. It makes no language-model claim and performs no unrestricted cryptanalytic search.

```bash
python experiments/prague_route_and_situation/verify.py --verify
python experiments/prague_route_and_situation/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default check uses the Python standard library. The optional check uses PyMuPDF and verifies the source PDF digest plus four exact crop pixel hashes, including the enlarged group 26 whose final D is fully observed.

Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed p211, PDF page 214. Exact PDF SHA-256:

```text
157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06
```

The unchanged key object preserves the historical and published references. `prior_evidence.json` stores the old p211 upper-A2 candidate and its original corpus-screen hash. That prior reading is credited explicitly; these artifacts add source review and reproducible costs, not a first historical decipherment claim. `catalog_proposal.json` contains two proposed physical records for parent integration.
