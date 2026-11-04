# p162: map sheets, Tiraspol border fire and an embassy signature

Prepared by **icekylinx and GPT-6 Astra Pro**.

This package preserves three source-reviewed fragments from J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed p162 (PDF page165). The accepted records contain **381 literal source slots**, including seven printed noncoordinate glyphs. Their working frames contain **382 coordinates / 191 plaintext positions**. The primary reading fixes **181 / 191 raw positions and 189 / 191 edited positions**, at a separately recorded cost of **two observed substitutions, seven printed-mask fills and one inserted-coordinate fill**. No observed coordinate is excluded.

The map request needs a conditional length model and retains two coupled numerical labels. The two shorter bodies use their native 100-slot frames. The 117-coordinate preceding C1 fragment remains unread context and is excluded from the three accepted records and all plaintext totals.

## Readings and source models

| Record | Source / working slots | Raw fixed / total | Edited fixed / total | Primary operation counts |
| --- | ---: | ---: | ---: | --- |
| [p162 B1](../../cases/pages/162.md#edition-cases-radio-map-sheet-request-p162-b1) | 181 / 182 | 85 / 91 | 89 / 91 | 2 observed substitutions, 3 source-mask fills, 1 missing-coordinate fill |
| [p162 C2](../../cases/pages/162.md#edition-cases-military-tiraspol-border-report-p162-c2) | 100 / 100 | 49 / 50 | 50 / 50 | 1 source-dash fill |
| [p162 D1](../../cases/pages/162.md#edition-cases-people-constantinople-embassy-signature-p162-d1) | 100 / 100 | 47 / 50 | 50 / 50 | 3 source-C fills |

### B1: a one-coordinate model with two equivalent source origins

The source begins with four-character `DGDD` and prints the uncertain length `RICHI-182?`. The literal source has 181 slots. The displayed 182-slot model inserts one unknown coordinate at boundary 1, giving `D?GDD`, and then supplies D to that new slot. No actual source glyph is silently added or removed.

The fixed edited template reads `STELLVERTRXGENERALSTABBERLINXZUSENDUNGVONJE?0BLAETTERNKARTE1ZU7?000XB1B2B3C1C2C3D1D2D3E2E3X`. Its two numerical unknowns retain the specific pair **XA**. The main substitutions are source **110 F→D**, changing `J` to `A` in `GENERAL`, and source **150 D→V**, changing the raw `2` inside `KAR2E` to `T`. The latter is a local word repair, not a change to the key's numerical assignments. Source Z at 84 and dashes at 85/149 are filled A/V/D respectively; the missing model coordinate is filled D. Source indices are zero-based.

The independent engine actually evaluates **all 182 transmitted-frame insertion boundaries** under that fixed template and pair constraint. Boundaries **0 and 1** tie at two observed substitutions; the first five costs are **2, 2, 3, 4, 4**. Both minima yield the same completed ciphertext with different origins for the inserted D. Boundary 1 is a display convention. The certificate preserves all 182 operation counts, the first five raw readings and origin maps, and the unaltered 181-slot paired prefix with its trailing unpaired coordinate. This retrospective comparison does not prove a unique historical loss or an unrestricted plaintext solution.

### B1: explicitly provisional F and its E sensitivity

The high-resolution [faded-glyph crop](sources/p162_B_faint.png) supports `XVGGA` and `VFXDX`, but leaves the F/E reading in `VFGGD` uncertain at source 110. The primary literal transcription uses **provisional F** and treats it as an observed coordinate. Its change to D therefore remains one of the two observed substitutions.

A second completed scan of **all 182 insertion boundaries** treats that glyph as noncoordinate E. It again has optimum boundaries 0/1 and the same edited reading, but the operation ledger becomes **one observed substitution, four source-mask fills and one missing-coordinate fill**. The primary totals are never replaced by this cheaper alternative. The two scans comprise **364 completed fixed-target evaluations**, with no claim that the scan resolves the visual glyph ambiguity.

### B1: the quantity and scale cannot be completed independently

Plaintext positions 43 and 63 both have pair **XA**, one of the two unfilled cells of the published Nov7–9 square. The two unused labels 5/6 occupy **VF/XA** globally and bijectively. The complete alternatives are:

| VF | XA | Requested quantity field | Scale field |
| --- | --- | ---: | ---: |
| 6 | 5 | 50 | 1:75000 |
| 5 | 6 | 60 | 1:76000 |

The certificate supplies both full square witnesses and re-encrypts all three edited records under each single shared square. A mixed pairing such as 50 with 1:76000 is unsupported. Familiarity of a map scale is not used as independent key evidence. Norbert's earlier proposed completion VF=5 / XA=6 is retained in the key provenance as an earlier hypothesis, without promoting it to a published final-key fact.

### C2 and D1: native-length fragments with source masks

C2 reads `TIRASPOLERHIELTMXGXFEUERANDERGRENZEXAKONACH17ROEM4` after one dash fill at source 36. The literal ending `AKONACH17ROEM4` is not expanded into a new unit or reference. The cleartext footer `NKJ UM` is outside the ciphertext. The preceding C1 has 117 observed coordinates and remains unread; the source's “missed first part” note does not authorize reconstructing it from this short clause.

D1 reads `DEUTSCHEBOTSCHAFTKONSTANTINOPELXUNTERSCHRIFTSTUMMX` after three C masks at source 22/37/79 are filled G. The unusual cleartext origin field **1330 (8/13)** remains literal. It is marked part 1 of two, and no second part is supplied here. The receipt header says November 10 while the body is read under the unchanged Nov7–9 period key. No additional personal identification or telegram linkage is inferred from STUMM.

## Reproduction

From the repository root:

```bash
python experiments/nov8_map_and_boundary/verify.py --verify
```

The default verifier uses only the Python standard library and imports neither the shared cipher engine nor another package verifier. It independently derives the transposition order, coordinate domains and operation ledgers, completes both 182-boundary scans, checks the two globally shared key completions by full re-encryption, reproduces the earlier OCR body checks, and verifies the exact case displays. Their **182 non-X labels include two positional unknowns**, all mapped back to the edited streams.

Optional exact source-pixel verification requires PyMuPDF and the original Childs PDF:

```bash
python experiments/nov8_map_and_boundary/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

All seven source images were freshly rendered after clearing the PDF render cache. [inputs.json](inputs.json) binds each PNG's bytes, uncompressed pixels, PDF page, rectangle, scale and dimensions. The original PDF SHA256 is `157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.

## Prior evidence and package scope

The published key retains George Lasry / Ingo Niebel / Nils Kopal / Arno Wacker attribution and its two unfilled numeral cells. The [prior OCR snapshot](prior_evidence.json) preserves the original screen-file hash and three selected old rows. C2 and D1 already had substantial readable bodies in that screen. The old B1 OCR instead has 183 slots and a poor native-length reading; the present source review uses 181 printed slots and separately charges its conditional extra model slot. This is a source edition and reproducible conditional reading, with no first historical decryption claim.

- [inputs.json](inputs.json) preserves the literal headers, grouped source rows, primary and alternative glyph definitions, readable displays, full key provenance and unread context.
- [certificates.json](certificates.json) preserves every operation, partial domain, source-local placement, global key witness, fixed-target scan and readable-label mapping.
- [catalog_proposal.json](catalog_proposal.json) contains exactly three accepted physical-record proposals. C1 is intentionally absent.
- [sources/p162_full.png](sources/p162_full.png) preserves the complete page, including the neighboring source context.

The executable certificate proves consistency with the stated transcription, partial key and conditional model. It keeps source ambiguity, historical geometry and unresolved global labels explicit rather than treating readability as proof of them.
