# Source editions: equipment disposal and troop return on pp207–208

Prepared by **icekylinx and GPT-6 Astra Pro**.

This package supplies seven manually source-reviewed records under the unchanged, conservative published **Nov16–18** key. The readable case is [Equipment disposal, Alpenkorps return, and Finland evacuation orders](../../cases/military/repatriation_orders.md). The main gains are whole first rows omitted by the older OCR extraction, a printed copy that supplies five erasures, and a clearly limited 221-to-220-coordinate interpretation.

## Completed work

| Scope | Completed result |
|---|---:|
| Physical source records | 7 |
| Printed source slots, including dashes and the final extra X | 1,589 |
| Observed ADFGVX coordinates | 1,572 |
| Working coordinates | 1,588 |
| Working plaintext positions | 794 |
| Fixed working raw labels | 753 |
| Fixed editorial labels | 771 |
| Observed-coordinate substitutions | 11 |
| Printed-dash fills | 17 |
| Conditionally excluded transmitted coordinates | 1 |
| Retrospective single-exclusion placements priced | 221 |
| Published square cells changed | 0 |

The working totals include p207 A2's **conditional** 220-coordinate interpretation. They are not counts for an unchanged 221-coordinate original. All seven literal sources and their unmodified readings are preserved; the 221-slot source has an unpaired coordinate in its unmodified reading.

- **p208 A1/A2:** 123/123 and 109/114 raw labels, with no coordinate edits. The command routes the Alpenkorps's Prussian formations to Silesia and Bavarian formations to Bavaria, subject to conditions. Five numeral labels remain unassigned.
- **p207 B:** the same 228-coordinate ending, with 222 agreeing known coordinates, one differing known coordinate and five dashes. The p208 witness supplies `127 G→F` and `165–169 ADAGX`. Four additional letters become fixed, while the numerical reference remains partial. These are distinct printed witnesses; independent transmissions are not established.
- **p207 A1:** equipment and horses that cannot reach Germany by march or rail are to be sold, with protection against leaving the troops entirely without them. The source edition requires seven known-coordinate substitutions and twelve dash fills.
- **p207 A2:** 221 printed coordinates against the label 220. Excluding its final X gives a readable addressee/reference continuation with no source substitutions. All 221 possible single exclusions were priced against the retrospective known-letter and unassigned-digit-cell template. Index 220 is the sole zero-substitution placement within that comparison. This does not establish a padding convention or universal damage mechanism.
- **p207 C1/C2:** a two-part message to the German general in Finland about differing situation assessments and early transport away. One and two coordinate substitutions are priced. The doubled A in `ABTRAANSPORT` remains literal; no character is deleted from that word.

## Boundaries and key treatment

The eight unfilled square cells retain the domain `03456789`. Their original coordinate pairs are retained in every unresolved numerical field. The p207 B copy restores one erased coordinate in such a field, without selecting a digit. In p207 C2, the raw unknown label inside `ABTRAAN?PORT` belongs to that numeral domain; the proposed S therefore requires an observed-coordinate substitution, not a square fill.

The verifier uses a sorted interim-index permutation to undo transposition, with a separate column-slice forward direction. It checks exact source rows, counts, raw domains, coordinate origins, each repair, every retrospective geometry cost, and all unchanged known numeral labels. One arbitrary global bijective completion of the partial square certifies a full encryption round trip; it is explicitly not a historical numeral assignment. The copy comparison is checked against the complete literal p208 A2 source, not only against its readable words.

No language model was trained or tuned for this edition. The 221-position comparison is a retrospective constraint calculation, not a blind recovery experiment or an exclusion bound on other models.

## Source and prior evidence

Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed pp207–208, PDF pages 210–211. Exact scan SHA-256:

```text
157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06
```

`inputs.json` records seven row-level transcriptions, both page headings, all visible headers, the complete unchanged key and its prior publication references, and nine image crop/scale/pixel certificates. Message and reception time fields are recorded literally.

`prior_evidence.json` preserves all seven earlier OCR-screen records from these pages, with the full original screen's SHA-256. The earlier screen already contained partial readings of the duplicate ending and p207 C2. It omitted complete first rows of p207 A1/C1 and p208 A1 and miscounted p207 A2. This package adds source-reviewed readings and exact costs without erasing that earlier candidate history or claiming first historical decipherment. The published key retains credit to George Lasry, the historical Childs appendix, and the research of Lasry, Niebel, Kopal and Wacker.

## Reproduce

From the repository root:

```bash
python experiments/repatriation_orders/verify.py --verify
python experiments/repatriation_orders/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default verifier requires only the Python standard library. The optional source check requires PyMuPDF and verifies the PDF hash plus the exact rendered pixels of both full pages and seven crops. `certificates.json` contains the independently replayable results; `catalog_proposal.json` supplies seven physical-record proposals for the parent-maintained catalog.
