# Childs p188: conditional armistice request and native provisions fragments

Prepared by **icekylinx and GPT-6 Astra Pro**. Published Nov13–15b partial key: Lasry, Niebel, Kopal and Wacker. Earlier machine candidates and bounded prior-body checks are retained in `prior_candidates.json`.

The complete readable edition is [armistice_provisions_requests.md](../../cases/pages/188.md#edition-cases-military-armistice-provisions-requests).

## Scope and price

| Record | Analysis-frame slots | Raw fixed → edited fixed | Observed substitutions | Mask fills | Geometry |
|---|---:|---:|---:|---:|---|
| p188 A | 224 of 225 visible slots | 104/112 → 112/112 | 14 | 7 | Conditional exclusion of one extra K/X-like visible mark, costing 0–1 known-coordinate deletion |
| p188 B2 | 176 | 84/88 → 88/88 | 10 | 0 | Native; “jammed to end” note remains |
| p188 C1 | 268 | 130/134 → 130/134 | 4 | 0 | Native; literal E at source140 remains masked |

A is not an unqualified solved message: its geometry and wording are conditional, with no exhaustive optimality/uniqueness claim. Its raw `AVK1P` becomes `AOK1P`, preserving the original `1P` suffix despite the independent `AOK11` footer. Five dashes, one B-shaped glyph and one damaged glyph at source118 are filled separately from the extra-marker exclusion.

The third row ends `GDGAG AV?XF`. The [source detail](sources/p188_A_damaged_glyph.png), full row and original embedded image pixels do not establish X at source118; the earlier frozen OCR also masked this same glyph. Its raw pair at plaintext42 is `?V`, with domain `234789ACMQVXY`. The certificate preserves X only as an explicit sensitivity branch: 105 raw fixed positions, 15 substitutions and six fills, producing the same edited stream. The main ledger uses 104, 14 and seven respectively. This is a correction to source certainty, with one substitution reclassified as a fill; it is not a recovered letter or a lower total repair cost.

B2 retains `LAENGSTENSOCH` and `FELDINTENTENDANT`; neither is silently normalized. C1's headquarters abbreviation, dispatch interval and portions remain unknown. B2/C1 are plausible companions on the printed matching reference, part numbers and subject, not a proved unique historical assembly. Dates/times, all raw digit/J/Q/Y labels, and the unchanged partial key remain explicit.

## Reproduction

From the repository root, with Python 3.10 or later:

```sh
python experiments/armistice_provisions_requests/verify.py --verify
```

The default verifier uses the standard library and repository cipher code. It authenticates image bytes and inputs, independently inverts the columns, checks the project decoder and global injectivity, maps all frame positions to original source slots, recomputes the exact edit prices and checks the saved certificate.

For the pinned primary PDF and all crop pixels, additionally install PyMuPDF and run:

```sh
python experiments/armistice_provisions_requests/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The PDF digest is pinned in `inputs.json`; page191 is printed188. Each crop records its page, PDF rectangle, rendering scale and SHA-256. No baseline key changes, numeric assignments, added coordinate slots or block reorderings occur. Unknown cells remain globally coupled; arbitrary completion witnesses are never promoted to historical readings.
