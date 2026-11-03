# Receipt request through Nikolajew: the other p105 telegram

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

This is the 300-slot **section A** on Childs p105, a request to confirm receipt of two communications to Mackensen command through Nikolajew. It is separate from the original [p105 challenge](../../cases/p105.md), which is the 290-slot section B. The complete native source yields 150 fixed output labels without changing any coordinate or square cell.

Read the [complete source edition](../../cases/radio/nov2_nikolajew_acknowledgment.md).

| Scope | Count |
| --- | ---: |
| Physical source records | 1 |
| Printed source slots | 300 |
| Plaintext positions | 150 |
| Fixed raw labels | 150 |
| Fixed primary edited labels | 150 |
| Observed-coordinate substitutions | 0 |
| Source-mask fills | 0 |
| Inserted, deleted or reordered source coordinates | 0 |

The primary totals preserve the unchanged published key and native source frame. Conditional proposals are not extra source records or independently authenticated historical readings.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## Reproduce

```sh
python experiments/nov2_nikolajew_acknowledgment/verify.py --verify
python experiments/nov2_nikolajew_acknowledgment/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary check uses the standard library and existing repository helpers. The optional source-pixel check uses PyMuPDF and Pillow.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
