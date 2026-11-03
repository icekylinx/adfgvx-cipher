# A repeated negotiation assessment and a departure-order reference

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The first two printed parts of a four-part heading repeat an assessment that participation in negotiations is pointless and state that earlier messages are dealt with by an order to depart. Both source bodies remain in their complete native frames. No missing later parts, numerical references or execution of the departure order are supplied from context.

Read the [complete source edition](../../cases/military/nov18_negotiation_repetition.md).

| Scope | Count |
| --- | ---: |
| Physical source records | 2 |
| Printed source slots | 484 |
| Plaintext positions | 242 |
| Fixed raw labels | 228 |
| Fixed primary edited labels | 233 |
| Observed-coordinate substitutions | 5 |
| Source-mask fills | 5 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/nov18_negotiation_repetition/verify.py --verify
python experiments/nov18_negotiation_repetition/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
