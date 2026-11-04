# State-bank accounting request and dispatched cheques

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [full two-part edition](../../cases/pages/172.md#edition-cases-finance-staatsbank-accounting-cheques). The first p172 D body contains 197 occupied source slots against advertised 198 and has a four-character ADAX group; the second is a complete native 204-coordinate body. All five positions for the additional first-part coordinate remain replayable. Boundaries 27 and 28 tie and give the same completed ciphertext, so the loss location is not uniquely selected.

Across both stated frames, 192 of 201 labels are fixed raw and 200 are fixed after five observed-coordinate substitutions, seven printed-mask fills and one additional-coordinate fill. The one unresolved label is VF in the date-like AM? field, with domain {5,6}. The complete closing 89240911 remains literal and is not interpreted as an amount. The source-length spellings DRINLICHST and CHEKS remain visible.

## Reproduce

```sh
python experiments/staatsbank_accounting_cheques/verify.py --verify
python experiments/staatsbank_accounting_cheques/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses standard-library code and repository helpers. Optional PyMuPDF/Pillow verification checks the source scan and exact crop pixels. Every coordinate change and both fill categories are priced separately, all local insertion alternatives remain in the certificate, and re-encryption proves compatibility with the disclosed frame and proposals.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
