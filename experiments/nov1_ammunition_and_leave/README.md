# p102 C/D: ammunition loading and leave arrangements

Prepared by **icekylinx and GPT-6 Astra Pro**.

This package verifies two native Nov1–3-key records from J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed p102 (PDF page105). Both frames are complete and use only observed ADFGVX coordinates. Their 520 source coordinates give **260 / 260 fixed plaintext positions with no substitutions, fills, insertions, exclusions or key changes**.

The main source improvement is in p102 C: three masks in the earlier OCR become the literal `8` in `5280625`, `N` in `WERDEN`, and `I` in `HITTMER`. The earlier screen already contained the substantial body of C and the complete body of D. This edition therefore claims native source verification and exact reading at those three formerly unresolved positions, not first historical body recovery.

## Readings

| Source record | Native coordinates | Raw fixed / total plaintext positions | Source result |
| --- | ---: | ---: | --- |
| [p102 C](../../cases/caucasus/caucasus_ammunition_loading.md#p102-c) | 262 | 131 / 131 | Request to telegraph whether the remaining ammunition should be loaded; quantity `5280625`, reference `2078`, office reference `6829`, signature `HITTMER` |
| [p102 D](../../cases/people/roesler_leave_and_travel.md#p102-d) | 258 | 129 / 129 | Leave and departure on the next ship; both occurrences of `ROESLER`, the reference `109`, and signature `HOENIGSCHMID` retained |

The full published Nov1–3 square and 19-column ranks are retained with their Lasry / Niebel / Kopal / Wacker provenance in [inputs.json](inputs.json). No numeral relabeling is performed. `ASRM1`, `RUSSXIS`, `MUV`, `EXH`, and `SXMXSTXPERS` remain literal; the readable layer supplies spacing and punctuation without expanding them. The D header’s `UNG`, `BARON FRANKENSTEIN`, `HPTM BENEDIKT` and `ÖST` are cleartext source evidence, separate from the recovered body.

## Reproduction

From the repository root:

```bash
python experiments/nov1_ammunition_and_leave/verify.py --verify
```

The default verifier uses only the Python standard library. It independently reconstructs the column transposition and coordinate pairs, re-encrypts all 260 labels to the exact native ciphertexts, verifies the zero-cost ledger, compares the two earlier OCR frames and decoded bodies, preserves every numeral position, and maps all **236 non-X labels** of the readable German back to the raw streams. It also checks that both exact displayed quotes are present in the case pages.

Optional exact source-image verification requires PyMuPDF and the original 156 MB Childs PDF:

```bash
python experiments/nov1_ammunition_and_leave/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The input binds the full PDF SHA256, page number, crop rectangle, scale, image dimensions, PNG hash and uncompressed pixel hash. The optional check reproduces the full page and C/D detail images directly from that PDF. The exact PDF SHA256 is `157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.

## Files and limits

- [inputs.json](inputs.json): literal grouped source rows, headers, full key, readable displays and source-image bindings.
- [certificates.json](certificates.json): each plaintext pair and source origin; all digit labels; exact re-encryption and readable-layer mappings; earlier OCR comparison.
- [prior_evidence.json](prior_evidence.json): the two earlier screen rows with their exact old plaintexts and original screen-file hash.
- [catalog_proposal.json](catalog_proposal.json): two physical-record entries for integration by the catalogue owner.
- [sources/p102_full.png](sources/p102_full.png) and [sources/p102_C_D_detail.png](sources/p102_C_D_detail.png): source page and readable source detail.

The displayed German has no bracketed supplies or added letters. Punctuation and abbreviation segmentation remain editorial: in particular, the repeated `ROESLER` does not uniquely determine grammatical attachment. This package does not identify the named people externally, expand the ammunition abbreviation `IS`, or infer an ammunition type or numeric grouping from `5280625`. It does not alter the neighboring p102 A/B editions, the published key, or any challenge status.
