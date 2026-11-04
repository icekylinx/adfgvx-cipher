# Reduced provisioning strength and a separate evening report

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Two physically numbered parts request a complete stop to provisions after a reduction in the strength being provisioned. Their association is explicit across the p219/p220 page break. A separate evening report on p220 preserves its unresolved unit and place labels. All three use their complete native printed frames and the unchanged Nov25–28 key.

Read the [complete source edition](../../cases/pages/219.md#edition-cases-military-nov25-provisions-and-evening-report).

| Scope | Count |
| --- | ---: |
| Physical source records | 3 |
| Printed source slots | 630 |
| Plaintext positions | 315 |
| Fixed raw labels | 315 |
| Fixed primary edited labels | 315 |
| Observed-coordinate substitutions | 6 |
| Source-mask fills | 0 |
| Inserted, deleted or reordered source coordinates | 0 |

The counts use the primary edition and unchanged key. Optional lexical proposals are separate alternatives within the same physical record; they are not extra recovered telegrams. Literal numerical labels and unresolved square cells or source masks remain explicit.

## Reproduce

```sh
python experiments/nov25_provisions_and_evening_report/verify.py --verify
python experiments/nov25_provisions_and_evening_report/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and repository helpers; the optional image check uses PyMuPDF and Pillow. Source hashes, coordinate maps, all edits, global completions and literal readable-label preservation are checked.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
