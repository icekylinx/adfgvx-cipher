# September receipt and front-news inquiry

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.**

This source edition covers Childs **p58 B** and **p59 B**, using the unchanged
published **Sep19–21** square and 22-column permutation. Both bodies had already
appeared in an unreviewed repository screen. The contribution here is the exact
source transcription, coordinate ledger, explicit editorial cost and reproducible
reading. No historical first-solution claim is made.

| Record | Native slots | Plaintext positions | Raw fixed | Edited fixed | Observed substitutions | Damaged-glyph fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| p58 B | 148 | 74 | 72 | 74 | 4 | 2 |
| p59 B | 172 | 86 | 86 | 86 | 0 | 0 |
| Total | 320 | 160 | 158 | 160 | 4 | 2 |

There is no insertion, deletion, change of frame or key change. The two C-like
and L-like source glyphs in p58 B are retained literally in the transcription
and modeled as erasures; their intended coordinate identities are not taken for
granted. The exact edited stream uses source **39→G** and **119→D**, alongside
the four recorded substitutions. The candidate retains **SECHZENHUNDERT**, whose
normal German spelling needs an additional H. That extra plaintext character is
not inserted into the encoded stream.

The separate p59 B inquiry reads completely in its native frame. **AKONACH70**,
**PHQ** and **95267** remain literal. Its source gives a receiving time of
01.57 p.m. on 21 September and a `1030 (21.9)` field.

The p58 A material is preserved as **uncounted context**: two `AAA` stubs,
advertised lengths 196 and 212, and a third cleartext stub advertised as 182.
Those headings do not supply complete coordinate bodies, and no omitted
plaintext is reconstructed from them. They are not part of either the table
above or the catalog proposal.

## Files and reproduction

- [Inputs](inputs.json) retain source rows, full key provenance, headers, crops,
  glyph qualifications, limits and the excluded p58 A context.
- [Certificates](certificates.json) retain every raw domain, source-coordinate
  pair, edited coordinate, changed plaintext position and exact re-encryption.
- [Earlier candidates and bounded attribution checks](prior_candidates.json)
  retain the relevant earlier screen outputs. An unsuccessful bounded keyword
  search of the paper, thesis and cached comments is not priority evidence.
- [Catalog proposal](catalog_proposal.json) contains exactly the two physical
  ciphertext records. The parent integration process owns the shared catalog.
- The readable editions are [Kress receipt](../../pages/058.md#edition-cases-finance-kress-money-receipt)
  and [Nazareth inquiry](../../pages/059.md#edition-cases-radio-nazareth-front-inquiry).

From the repository root:

```bash
python experiments/september_receipt_and_front_inquiry/verify.py --verify
python experiments/september_receipt_and_front_inquiry/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the Python standard library and the repository cipher
module. It independently reconstructs the transposition index map and checks it
against the project implementation, verifies all domains, applies the exact
repair ledger, and re-encrypts both full candidates. The optional second command
requires PyMuPDF and Pillow, checks the original PDF hash and size, and verifies
the four source crops pixel for pixel. No external model or temporary cache is
needed to reproduce this package. Exact round trips certify the stated reading
and its editing cost; they do not establish historical uniqueness.
