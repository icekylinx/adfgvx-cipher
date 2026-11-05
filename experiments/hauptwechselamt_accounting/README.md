# p175 B2: payments and cheque acknowledgements

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs printed p175 B, PDF page 178, preserves a **second part** concerning
marks paid through the end of October and arrival notices for cheques.
The signature-like ending reads `HAUPTWECHSELAMT` in the edited candidate.
No first part is identified or supplied. Read the
[case](../../pages/175.md#edition-cases-finance-hauptwechselamt-accounting) for all three
presentation layers and the unresolved fields.

The receiving header is `LP v NKJ (6.02 p.m., November 10th)`. Despite
that date, the readable published key is **Nov7–9**, not the Nov10–12
key that reads the neighboring messages. The key is verified through
the actual ciphertext; the page date does not override that result.
No transmission date is inferred from this distinction.

## Native source and exact cost

The [crop](sources/p175_B.png) contains **204** printed slots, matching
`RICHI-204`. Ten are printed dashes, and each remains one coordinate
in the native frame. There is no insertion, deletion or reordering.
The earlier OCR-derived candidate used a shorter stream and was
unreadable; its retained outputs are frozen in
[prior_candidates.json](prior_candidates.json).

| Quantity | Value |
| --- | ---: |
| Physical records | 1 |
| Printed source slots | 204 |
| Observed valid coordinates | 194 |
| Plaintext positions | 102 |
| Raw fixed labels | 90 |
| Edited fixed labels | 98 |
| Observed-coordinate substitutions | 4 |
| Printed-dash fills | 8 |
| Printed dashes left unfilled | 2 |

The four observed substitutions are source **1 A→D**, **32 G→F**,
**38 G→D**, and **165 V→X**. The eight printed-dash fills are
**0→A, 5→G, 7→F, 31→D, 152→F, 166→V, 186→A, and 202→D**.
These indices are zero-based. The source edits, the full independent
inverse permutation, every plaintext pair and all domains are in
[certificates.json](certificates.json).

`OCTOBER` and `CHEKS` are kept as the candidate decodes. No letter is
inserted to impose a different spelling. The paid-mark and cheque
phrases are incomplete clauses because the first part is absent; no
governing verb or transaction amount is reconstructed.

## Unresolved fields and exact completion check

Four plaintext positions remain unknown:

| Plaintext position | Pair | Source coordinates | Domain | Role in the literal candidate |
| ---: | --- | --- | --- | --- |
| 3 | `?G` | 154, 40 | `1GIKNY` | `VOM?8` |
| 62 | `VF` | 6, 108 | `56` | `AM?` |
| 98 | `?F` | 203, 101 | `5679JMZ` | `89240?11?` |
| 101 | `VF` | 71, 153 | `56` | `89240?11?` |

The first field is not forced to be a numerical date. The two `VF`
occurrences must share a value under one key; they are not independent
choices. The existing independent military-context hypothesis for that
cell is not imported into this baseline source edition.

The two unknown square cells admit **two** injective completions. The
two remaining printed erasures admit **36** coordinate combinations
per completion. The verifier enumerates all **72** complete witnesses,
checks that the edited known letters remain unchanged, verifies the
equality of the two `VF` labels, and re-encrypts every complete plaintext.
All 72 are distinct literal plaintexts; none is selected as historical.

## Attribution and reproduction

The published period key retains credit to Lasry and colleagues. The
paper explicitly discusses the separate p175 A travel message; a bounded
check located no explicit p175 B Hauptwechselamt reading. This absence
does not establish historical priority. The new contribution is the
source-exact native frame and a reversible, qualified reading.

From the repository root:

```sh
python experiments/hauptwechselamt_accounting/verify.py --verify
python experiments/hauptwechselamt_accounting/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command needs the standard library and repository cipher code.
The optional PDF check uses PyMuPDF and Pillow to verify the PDF's hash
and the exact crop pixels. The verifier needs no temporary files or
candidate caches. The full published square is left unchanged.
