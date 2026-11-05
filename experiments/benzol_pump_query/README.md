# Benzol-pump inquiry with an explicit missing-coordinate model

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [complete source edition](../../pages/189.md#edition-cases-context-benzol-pump-query). The received p189 D body has 101 occupied positions against advertised 102 and a four-character XVGF group. A conditional 102-coordinate frame gives 47/51 fixed raw labels; six observed substitutions, one source-glyph fill and one additional-coordinate fill give the displayed 51-position question about a benzol pump and a prompt answer.

All 102 possible insertion boundaries are priced. Only 37 and 38 attain the six-substitution minimum for the disclosed words, and both alternatives remain in the certificate. No observed coordinate is deleted or moved. The neighboring pump reply supports the topic but supplies neither missing ciphertext nor an independently established signature.

## Reproduce

```sh
python experiments/benzol_pump_query/verify.py --verify
python experiments/benzol_pump_query/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The normal verifier uses standard-library code and repository helpers. Optional PDF verification uses PyMuPDF and Pillow. The raw odd-frame orphan, all prices, source maps, coupled unknowns, exact changes and the full re-encryption remain reproducible.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
