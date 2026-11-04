# p108: naval inquiry and personnel-discharge order

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

This package preserves three physical records on Childs p108, PDF page 111,
under the unchanged published **Nov1–3** key. A is a separate naval inquiry;
B1/B2 form a source-labeled two-part personnel message. They are not joined
merely because they appear on the same page.

Read the [naval inquiry](../../cases/pages/108.md#edition-cases-radio-naval-arrival-inquiry) and the
[personnel order](../../cases/pages/108.md#edition-cases-people-rudolf-discharge). All raw and edited
streams, references, abbreviations and repeated names are preserved.

## Two distinct source problems

**A is a correction to the earlier OCR.** Its printed native length is
282 coordinates. The old corpus omitted the final standalone **FX** row,
leaving 280, and masked the clearly visible F at source index 11. Restoring
the visible row and glyph produces a coherent **141-position** inquiry
without any source-coordinate edit. `ocr_snapshot.json` retains the old
record and its origin hash; the verifier checks the exact difference and
also reproduces the old output under the same key. The old corpus remains
unchanged.

**B2 is a genuinely short printed group.** It contains 135 visible
coordinates against `RICHI-136`. The first row's fifth group is **DAGD**,
with four visible symbols. The model of one missing coordinate somewhere
inside that group is explicit. There are five possible insertion
boundaries, all retained. The primary **D?AGD** frame gives readable words
and leaves only the final reference character unresolved:
`NACHCHEF2BO52?X`, domain **027GQT**. It fills no missing coordinate.

The exact group audit enumerates **5 × 6 = 30 geometry-labeled
completions**, corresponding to **26 distinct complete ciphertexts and
plaintexts**. Under the explicitly stated readable-prefix constraint,
six distinct completions remain, exactly the six completions of the
primary frame. This is a **lexical condition**, not independent proof of
the historical loss position. The adjacent gap placements before D or
after A produce two of those same complete ciphertexts when their missing
coordinates are filled to recover C in CHEF or I in MILITAERDIENST.

| Missing-slot position in the short group | Observed substitutions under the stated prefix | Missing fills | Reference ending |
| --- | ---: | ---: | --- |
| `?DAGD` | 0 | 1 | `2BO522X` |
| `D?AGD` | 0 | 0 | `2BO52?X` |
| `DA?GD` | 0 | 1 | `2BO520X` |
| `DAG?D` | 1 | 1 | `2BO520X` |
| `DAGD?` | 2 | 1 | `2BO520X` |

The table's diagnostic repairs are **not adopted or counted**. No
reference numeral is chosen. A decimal-only assumption would restrict the
unresolved label to 0, 2 or 7, but the main reading retains the full domain.

## Counts and attribution

The primary edition has **547 visible and valid coordinates**, **548
modeled coordinates**, and **274 plaintext positions**, of which **273
are fixed under the stated frames**. All three edited streams are identical
to their raw layers: **zero observed-coordinate substitutions and zero
missing-coordinate fills**. One genuinely missing source coordinate
remains unresolved. A and B1 re-encrypt completely; the verifier enumerates
and re-encrypts every bounded B2 completion.

The two personnel bodies already appeared in earlier unreviewed repository
candidates. The naval inquiry was obscured by the OCR-shortened frame.
Published key provenance, earlier candidates and bounded publication
checks are frozen in `prior_candidates.json`. This package makes no
historical first-solution claim. The three-record `catalog_proposal.json`
excludes every alternative geometry from its physical-record count.

## Reproduce

From the repository root:

```sh
python experiments/p108_naval_and_personnel/verify.py --verify
```

The primary verifier uses the standard library and checked-in cipher
module. Optional original-PDF verification requires PyMuPDF and Pillow:

```sh
python experiments/p108_naval_and_personnel/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The original PDF's frozen size and SHA-256 are checked before the three
source crops are regenerated and compared pixel for pixel. Neither
scratch caches nor their original file locations are runtime dependencies.
