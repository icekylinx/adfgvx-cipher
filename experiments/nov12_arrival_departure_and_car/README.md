# Short arrival, departure and car enquiries on November 12

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Four short native records report arrival and departure, request an arrival notification, and enquire about a car. The arrival enquiry and departure text have earlier p174 parallels already published in this repository; the new witnesses add source support to those readings. In particular, the two complementary arrival-enquiry witnesses now supply every coordinate and every plaintext pair without changing an observed coordinate under the conservative glyph masks. The previously catalogued witnesses are not counted again.

Read the [complete source edition](../../cases/radio/nov12_arrival_departure_and_car.md).

| Scope | Count |
| --- | ---: |
| Physical source records | 4 |
| Printed source slots | 220 |
| Plaintext positions | 110 |
| Fixed raw labels | 103 |
| Fixed primary edited labels | 110 |
| Observed-coordinate substitutions | 1 |
| Source-mask fills | 8 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/nov12_arrival_departure_and_car/verify.py --verify
python experiments/nov12_arrival_departure_and_car/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted. The arrival-enquiry and departure wording was already presented for p174 B/E in cases/radio/seifert.md. The new p183 witnesses add coordinate support and a separately priced comparison, not a new claim to that wording or extra message groups.
