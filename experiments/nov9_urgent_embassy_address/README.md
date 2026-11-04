# p161 B1: urgent Constantinople embassy address

Prepared by **icekylinx and GPT-6 Astra Pro**.

The [source edition](../../cases/pages/161.md#edition-cases-people-constantinople-urgent-address-p161-b1) preserves a short native 98-coordinate record from J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed p161 (PDF page 164). Its unchanged Nov7–9 partial key yields **49 / 49 fixed raw plaintext positions**, with **zero historical coordinate substitutions, source fills, insertions or exclusions**:

```text
DEUTSCHEBOTSCHAFTCONSTANTINOPELDRINGENDXGEZXSTUMM
```

The literal C spelling of `CONSTANTINOPEL`, abbreviation `GEZ` and name `STUMM` remain intact. No pair in this message uses either unknown square cell VF/XA, so the incomplete assignment of 5/6 does not affect its 49 labels.

## Two corrections to the working transcription

The initial, unpublished manual draft read `DVGXW` and final `AAA`. Independent high-resolution source inspection gives **DVGXV** and **AXA**:

- Source 69 is V: its stroke overlaps the preceding X. The [V detail](sources/p161_B_lastV.png) retains the overlapping source shapes.
- Source 96 is X: the [final-group detail](sources/p161_B_final_group.png) shows a crossed middle glyph between two clear A forms.

Correcting the first draft error alone gives the diagnostic `DRINGENU`. Correcting the second to the source's `AXA` gives native `DRINGEND`. These changes correct the draft transcription; they are not charged as modifications to the historical ciphertext. The [prior evidence](prior_evidence.json) preserves the exact draft rows, file hash, the old disordered page OCR and the bounded absence of a B entry from the earlier initial screen. No first historical decipherment priority is claimed.

## Date and fragment limits

The subsection heading says **9th NOVEMBER, 1918.**, the receipt header says **November 8th**, and the internal origin field is **(9/11)**. All three source markers remain literal. The source labels this part 1 of 2; a missing second part is not supplied.

The address/signature wording resembles [p162 D1](../../cases/pages/162.md#edition-cases-people-constantinople-embassy-signature-p162-d1), but the two source records have different headers and C/K spellings of the city. This is related wording only, not evidence that they form one telegram. No substantive missing request or external identity for STUMM is inferred.

## Reproduction

From the repository root:

```bash
python experiments/nov9_urgent_embassy_address/verify.py --verify
```

The default verifier uses only the standard library. It independently fills transposition columns, derives all coordinate pairs and domains, re-encrypts the full native ciphertext, checks the draft diagnostics, confirms that the two unknown key cells are unused, and verifies the readable German's **47 non-X labels**. Both possible global 5/6 key completions independently reproduce the same complete reading.

Optional original-PDF pixel reproduction requires PyMuPDF:

```bash
python experiments/nov9_urgent_embassy_address/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The [input](inputs.json) binds four fresh-cache renders: the complete page, the B detail, the overlapping V, and the final AXA group. Each has a PDF page, crop rectangle, scale, dimensions, PNG hash and uncompressed-pixel hash. The original PDF SHA256 is `157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.

The [certificate](certificates.json) preserves each plaintext position and its two native source origins, exact re-encryption, all 47 readable-label mappings, both global key witnesses, the two discarded draft readings and the separate source-date evidence. [catalog_proposal.json](catalog_proposal.json) proposes exactly one physical record.

Published key provenance remains attributed to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, with earlier numeral hypotheses recorded separately in the copied key metadata. This edition recovers neither a new square nor a new transposition key and does not alter any existing package.
