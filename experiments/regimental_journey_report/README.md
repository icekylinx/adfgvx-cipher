# A regimental journey report with unresolved route and unit labels

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

This two-part native report describes a journey and assistance received after minor interruptions. The route, date-like and unit labels remain in their exact source form. The five printed dashes in part 1 are explicit source erasures: four are supplied by priced wording proposals and one remains unresolved. The Nov28–Dec1 square uses Y as the separator; X inside the displayed labels stays literal.

Read the [complete source edition](../../cases/pages/225.md#edition-cases-military-regimental-journey-report).

| Scope | Count |
| --- | ---: |
| Physical source records | 2 |
| Printed source slots | 466 |
| Plaintext positions | 233 |
| Fixed raw labels | 228 |
| Fixed primary edited labels | 232 |
| Observed-coordinate substitutions | 10 |
| Source-mask fills | 4 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/regimental_journey_report/verify.py --verify
python experiments/regimental_journey_report/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
