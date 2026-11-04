# German tonnage and the proposed Turkish purchases

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

Three parts of Childs p177 B preserve an instruction concerning sales of
German ships to Turkey. It says to sell only in the most extreme emergency,
warns that the Turkish interest may be in acquiring tonnage rather than
transporting Germans, requires immediate payment and authorization, and
quotes terms associated with `GENERAL` and raw `KERKIJRA` / `KEHKYRA`.
The full raw and proposed readings are in
[the case](../../cases/pages/177.md#edition-cases-naval-turkish-tonnage).

The primary source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, printed p177, PDF p180. The page heading says November 11;
the receipt header says November 12 at 2.55 a.m.; the origin line reads
`1410 (11/11)`. All three are preserved. The published `Nov10-12` key is
used without changing any cell.

| Record | Source slots | Valid coordinates | Modeled coordinates | Raw fixed | Candidate fixed | Observed changes | Source erasure fills | Lost coordinate fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p177 B1 | 330 | 329 | 330 | 161/165 | 164/165 | 3 | 1 | 0 |
| p177 B2 | 295 | 295 | 296 | 146/148 | 148/148 | 2 | 0 | 1 |
| p177 B3 | 374 | 374 | 374 | 183/187 | 184/187 | 4 | 0 | 0 |
| **Total** | **999** | **998** | **1,000** | **490/500** | **496/500** | **9** | **1** | **1** |

B2 has a four-letter `GDXV` group. All 296 single-loss boundaries are
screened uniformly against the proposed ordinary-word body. Boundaries
**232 and 233** tie globally at two observed-coordinate substitutions.
Both lie within the deficient group, both fill `X`, and both give the
same complete corrected ciphertext. Neither boundary is claimed unique.
The certificate retains their different raw erasure positions and domains.

## Conditional key propagation

The independent Corcovado package supplies a separately stated
[`XX=6` office-prefix hypothesis](../corcovado_sale_terms/README.md).
This package propagates it to all eight source/candidate variants,
including both B2 frames. It does not derive the key anew.

Four physical raw positions change: B1 date position 20, B2 ordinary-word
position 139, and B3 office/reference positions 180 and 184. The B2 change
is explicitly inconvenient: `V?RKAUFEN` becomes `V6RKAUFEN`. Its ordinary-word
candidate separately repairs the observed pair to `E`. Thus only three
conditional changes persist in repaired candidates, which then fix
**499/500** positions. The remaining final reference cell is `GF`, domain
`5789`; its value is unassigned.

The full inventory retains every changed marginal domain, including the
alternate B2 frame and the raw `TAUSEN?` occurrence of `GF`. The latter is
repaired by a source-coordinate substitution to `D`, not by assigning a
digit cell to a letter. The conditional date `6/11` does not independently
establish which earlier telegram was being answered.

## Credit and reproduction

Published key provenance is retained in `inputs.json`. The bounded prior
body check covers the Lasry–Niebel–Kopal–Wacker paper, its corresponding
dissertation chapter and the cached 55 ScienceBlogs comments; no explicit
body discussion of this instruction was located there. This is a new
repository source edition, without a universal priority claim.

```bash
python experiments/turkish_tonnage/verify.py --verify
python experiments/turkish_tonnage/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier independently reconstructs the transposition and plaintext
domains, checks all source/candidate mappings and exact repairs, reproduces
the complete gap search and binds the conditional key dependency by
SHA-256. The PDF option checks the full primary scan hash and every crop
pixel. The source inputs, proposed catalog entries, images and complete
machine-readable certificates are retained in this directory.
