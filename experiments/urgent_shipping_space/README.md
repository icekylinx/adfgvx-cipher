# Urgent shipping capacity and probable reliance on sea transport

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The surviving second and third parts request urgent shipping capacity and say that all troops will probably need sea transport. The source explicitly marks the first part missing. Repeated capacity labels, differing command fields and the unresolved source-mask position remain literal.

Read the [complete source edition](../../pages/218.md#edition-cases-naval-urgent-shipping-space).

| Scope | Count |
| --- | ---: |
| Physical source records | 2 |
| Printed source slots | 388 |
| Plaintext positions | 194 |
| Fixed raw labels | 193 |
| Fixed primary edited labels | 193 |
| Observed-coordinate substitutions | 1 |
| Source-mask fills | 0 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/urgent_shipping_space/verify.py --verify
python experiments/urgent_shipping_space/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
