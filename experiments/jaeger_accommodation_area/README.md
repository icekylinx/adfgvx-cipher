# An accommodation-area report with unresolved army and place labels

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

This native message reports an accommodation area for a German Jaeger division. Its readable proposal repairs one word and fills two printed dashes; the route-like spellings and three globally coupled digit positions remain literal or unresolved. The complete source body matches its advertised 230 slots, with no change to its frame.

Read the [complete source edition](../../pages/183.md#edition-cases-military-jaeger-accommodation-area).

| Scope | Count |
| --- | ---: |
| Physical source records | 1 |
| Printed source slots | 230 |
| Plaintext positions | 115 |
| Fixed raw labels | 110 |
| Fixed primary edited labels | 112 |
| Observed-coordinate substitutions | 1 |
| Source-mask fills | 2 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/jaeger_accommodation_area/verify.py --verify
python experiments/jaeger_accommodation_area/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
