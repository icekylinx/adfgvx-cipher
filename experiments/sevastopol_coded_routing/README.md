# Sevastopol routing amendment with opaque numerical groups

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p139 A1/A2/A3, PDF page 142, form a source-labeled three-part message
with native lengths **200 / 220 / 212**. It uses the unchanged published
**Nov4–6** key. The [reading case](../../pages/139.md#edition-cases-military-sevastopol-coded-routing)
preserves the routing opening, the distribution and all twelve five-figure
groups following **CUJOMAREMO**.

Those groups are recovered outer-ADFGVX plaintext. Their possible
codebook or other underlying meaning has **not** been identified or
decoded. They are not presented as quantities, and no digit assignment or
translation is inferred from them. The leading zero in **04376** remains
part of the literal group.

## Source and reading layers

A1's enlarged heading clearly reads **RICHI-200**. An initial small-image
impression of 300 was rejected before publication. The visible body has
200 coordinates. Earlier OCR omitted one X at source index **11**, leaving
199 and preventing a native pair decryption. The exact old input and
single source-visible correction are frozen in `ocr_snapshot.json` and
replayed by the verifier. This repairs the OCR, not the historical source.

A2 begins with a visible invalid **B** in **BVAGD**. Masking this occupied
slot gives raw `XAX?RX11120...`; the unknown position has domain **4CMNST**.
The primary edited candidate chooses **N** for the abbreviation **NR**,
requiring one invalid-glyph fill, source **0 B→X**. All six raw complete
compatibility witnesses are retained. This is an explicit contextual
choice, not a unique deduction from the damaged coordinate.

A1 and A3 use no source edits. The raw fields **YU**, **NACAR**, **GROSZ**
and **ER** remain literal. The readable German keeps **EZ/Ez.**, rather
than silently changing it to EX/Ex. All command references and numerical
groups are preserved.

## Counts, provenance and reproduction

Three physical records contain **632 visible slots**, **631 valid source
coordinates**, and **316 plaintext positions**. The raw layers fix
**315 / 316** positions; the edited layers fix **316 / 316**, with **zero
observed-coordinate substitutions and one invalid-glyph fill**. There are
no frame or key changes. All three complete edited streams re-encrypt
exactly. Fixed numerical labels are not the same as interpreted code
groups or recovered German words.

`inputs.json` freezes source rows, headers, crop geometry and key
provenance. `certificates.json` records every coordinate pair, source
index, domain, fill and complete witness. `prior_candidates.json` retains
earlier repository screens, including the readable distribution and the
odd-length opening, plus bounded publication checks. This edition makes
no historical first-solution claim. `catalog_proposal.json` counts only
the three physical parts.

From the repository root:

```sh
python experiments/sevastopol_coded_routing/verify.py --verify
```

This uses the standard library and checked-in cipher module. Optional
original-PDF crop verification requires PyMuPDF and Pillow:

```sh
python experiments/sevastopol_coded_routing/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The PDF's frozen byte count and SHA-256 are checked before all four crops
are regenerated and compared pixel for pixel. Scratch files are not
runtime dependencies.
