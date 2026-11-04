# Reval: steamers for troops, provisions and raw materials

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

This edition covers the three explicitly numbered parts on the lower half of Childs p213, under **23 November 1918**. They are separate from the previous day's medical continuation at the top of the page. The header is `KOW v LP (06.20 p.m., November 23rd); FUER RVA 20.00 (23/11) 3 TLE`. The stated receipt precedes the origin time on the printed date; both values are retained without a chronological correction.

The message says two steamers for troops and provisions are expected in Reval by the end of November, further tonnage will follow, and raw-material transport is also being arranged. The three vessel-like fields are retained as **`PETERXBENVIT`, `B9VERN`, `BAC4LON`**. No actual vessel identity, normalized name or historical tonnage is asserted.

See the [reading edition](../../cases/pages/213.md#edition-cases-naval-reval-steamer-notice), [inputs](inputs.json), [certificates](certificates.json), and [source crops](sources/).

## Source readings and repairs

The source lengths are exactly 200, 208 and 162 slots. Part 1 needs no ordinary-word repair. In source group 13, the third glyph is overprinted; the primary reading is D in `GDDVF`, producing the raw quantity `Y5111`. A V alternative produces `YP111`. A dedicated ten-times-scale crop and both full decryptions are retained. Neither is presented as an actual numerical quantity.

Part 2 has one printed C at source index 181. Filling it as G gives `FOLGT`. Three observed-coordinate substitutions repair `TANNAGE`, `TRANSPHRT` and `HE8TE`; all vessel-like names remain unchanged.

Part 3 has three printed dashes at indices 137–139. Filling only index 137 as F, and changing observed index 159 F to X, yields `KRIEGSDEP`. The other two erasures remain unresolved in the closing reference. The received `ROHAVAL` is not expanded as a code word.

| Record | Source slots | Fixed raw positions | Fixed candidate positions | Observed substitutions | Printed-glyph fills |
|---|---:|---:|---:|---:|---:|
| p213 A1 | 200 | 100 | 100 | 0 | 0 |
| p213 A2 | 208 | 103 | 104 | 3 | 1 |
| p213 A3 | 162 | 78 | 79 | 1 | 1 |
| **Total** | **570** | **281** | **283** | **4** | **2** |

The fixed-position counts are labels under the published `Nov22-24` square. The raw names, amount, `RPHAX` and reference are not semantically resolved merely because their labels are fixed. No rank or key is changed, and no missing coordinate is inserted.

## Attribution and verification

Parts 1/2 already had recognizable unreviewed repository candidates. The relevant earlier strings and hashes are frozen. Bounded checks of the Lasry–Niebel–Kopal–Wacker paper, Lasry dissertation and cached 2017 discussion found no explicit body discussion; that is not a proof of priority. This is a source edition and repair audit, not a first historical decipherment claim.

Run from the repository root using Python 3.10 or later:

```sh
python experiments/reval_steamer_notice/verify.py --verify
python experiments/reval_steamer_notice/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The standard-library verifier independently builds the inverse transposition, every position/domain and the complete raw-label inventory, verifies all edits and the alternative glyph reading, and compares the frozen certificate. The optional PDF check uses PyMuPDF and Pillow to reproduce all crops pixel for pixel after checking the PDF hash.
