# Urgent embassy address: Constantinopel, signed Stumm

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Source edition and verification: **icekylinx and GPT-6 Astra Pro**. The unchanged published Nov7–9 partial key retains its Lasry / Niebel / Kopal / Wacker attribution. No first historical decipherment priority is claimed.

## p161 B1

This short message in Childs printed p161 (PDF p164) contains an urgent embassy address and the signature STUMM. All **98 native source coordinates** are visible. Their **49 / 49 raw plaintext positions** are fixed without a historical coordinate edit, mask fill or geometry change.

### Source and date evidence

<details>
<summary>Literal source transcription</summary>

**Source transcription — literal cleartext header:**

```text
9th NOVEMBER, 1918.
B) YZ, NKJ v LP (05.49 a.m., November 8th)
NKJ v LP AS BIS 0715
YZ v LP 0022 (9/11) 2 TLE
1 TL RICHI-98
```

</details>

The receipt's **November 8th**, the subsection heading's **9th November**, and the internal **(9/11)** are retained separately. The edition does not force them into one date. The label says part 1 of two; an absent second part is not reconstructed.

The [native source detail](../../experiments/nov9_urgent_embassy_address/sources/p161_B_detail.png) shows the complete body and headers. Two mistakes in the current draft transcription were resolved by closer source inspection:

| Zero-based source index | Initial draft | Source reading | Evidence |
| --- | --- | --- | --- |
| 69 | W | V | The final V of `DVGXV` overlaps the preceding X; [high-resolution crop](../../experiments/nov9_urgent_embassy_address/sources/p161_B_lastV.png). |
| 96 | A | X | The final three-character group is `AXA`, with a crossed middle glyph between clear A forms; [high-resolution crop](../../experiments/nov9_urgent_embassy_address/sources/p161_B_final_group.png). |

These are corrections to the unpublished working transcription, not repairs to historical ciphertext. Keeping the mistaken final `AAA` would produce `DRINGENU`; the independently reviewed source `AXA` gives `DRINGEND` directly. The discarded draft and both intermediate readings remain in the certificate.

### Native reading

<details>
<summary>Raw decoded text</summary>

**Raw output — native 98-coordinate frame, published Nov7–9 partial key:**

```text
DEUTSCHEBOTSCHAFTCONSTANTINOPELDRINGENDXGEZXSTUMM
```

</details>

The edited output is identical to the raw output. None of its coordinate pairs uses either unfilled key cell, VF or XA, so the unresolved global assignment of 5 and 6 has no effect on this body.

**Readable German — exact nonseparator labels, with spacing and punctuation only:**

> Deutsche Botschaft Constantinopel. Dringend. Gez. Stumm.

`CONSTANTINOPEL` keeps its literal **C** spelling. `GEZ` stays abbreviated, and STUMM is not assigned an external identity.

### Scope and verification

The [p162 D1 address/signature fragment](constantinople_embassy_signature.md#p162-d1) provides related wording, but it has different source headers and the spelling `KONSTANTINOPEL`. Similarity does not establish that the two fragments belong to one telegram, and their missing parts are not joined.

The [inputs](../../experiments/nov9_urgent_embassy_address/inputs.json), [certificate](../../experiments/nov9_urgent_embassy_address/certificates.json) and [prior evidence](../../experiments/nov9_urgent_embassy_address/prior_evidence.json) preserve every source row, the partial key's earlier provenance, the old disordered page OCR and the draft corrections. The [standalone verifier](../../experiments/nov9_urgent_embassy_address/verify.py) independently checks all 49 positions, exact re-encryption, the readable display and both possible global key completions. Optional PDF verification reproduces every bound source image.
