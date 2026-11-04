# Postponed departure, a supper query and a farewell

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Three separate service messages retain their complete native source frames: a postponed departure with reassurance, a proposed warm supper and headcount enquiry, and a short farewell. Source-transcription corrections recover the positions omitted by earlier OCR; ordinary-word repairs, printed-dash fills and literal abbreviations remain explicit.

Read the [complete source edition](../../cases/pages/193.md#edition-cases-radio-nov14-15-departure-and-supper).

| Scope | Count |
| --- | ---: |
| Physical source records | 3 |
| Printed source slots | 368 |
| Plaintext positions | 184 |
| Fixed raw labels | 181 |
| Fixed primary edited labels | 184 |
| Observed-coordinate substitutions | 7 |
| Source-mask fills | 2 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/nov14_15_departure_and_supper/verify.py --verify
python experiments/nov14_15_departure_and_supper/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
