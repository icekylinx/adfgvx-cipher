# An airfield and German troops: the surviving third part on p154

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

A native third-part fragment reports an apparent airfield and German troops providing security along a named line. The exact text, three occupied source masks and two proposed coordinate corrections are retained; preceding parts and the geographical referents are not supplied from context.

Read the [complete source edition](../../pages/154.md#edition-cases-military-airfield-german-troop-fragment).

| Scope | Count |
| --- | ---: |
| Physical source records | 1 |
| Printed source slots | 172 |
| Plaintext positions | 86 |
| Fixed raw labels | 83 |
| Fixed primary edited labels | 86 |
| Observed-coordinate substitutions | 2 |
| Source-mask fills | 3 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/airfield_german_troop_fragment/verify.py --verify
python experiments/airfield_german_troop_fragment/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
