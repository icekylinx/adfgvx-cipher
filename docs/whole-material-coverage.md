# Whole-material source coverage

[Catalogue](../cases/README.md) · [Source identity](catalogue-source-identity.md) · [Reading conventions](reading-conventions.md)

Prepared by **icekylinx and GPT-6 Astra Pro**.

## Catalogue coverage

**All 679 reviewed physical ciphertext bodies have one canonical catalogue entry.** They occupy printed pages 56–230 of Appendix B. The 22 original challenge identifiers are preserved, and the other 657 bodies include the four previously uncatalogued unread fragments.

A separately printed part or received copy is one physical body. Surviving damaged fragments count; advertised but absent parts do not. The two literal `AAA` items at p58 A1/A2 remain separately registered ambiguous stubs outside this body count.

| Current navigation state | Sources |
|---|---:|
| READING | 336 |
| PARTIAL | 148 |
| CONDITIONAL | 188 |
| OPEN | 7 |

These states describe the kind of current edition, not a completion percentage. READING does not mean that every character or historical identification is settled; CONDITIONAL may include a partial proposal. OPEN sources have no accepted body reading. Their headers and source transcriptions are still useful evidence.

Catalogue metadata records source review for **679 bodies**. The boundary census records every log page, but it does not claim a fresh transcription of every glyph or a unique key for every body. Dated baseline records remain in the machine-readable census; current coverage is recomputed from the files in this checkout.

## OPEN sources

| Source | Received source slots | Current question |
|---|---:|---|
| [p70_B1](../cases/open/p70_B1.md) | 206 | OPEN; 206 received slots, 199 observed coordinates and 7 printed erasures; interruption boundaries retained |
| [p73](../cases/p73.md) | 178 | Open |
| [p127_B2](../cases/open/p127_B2.md) | 152 | OPEN; 152 received slots, 104 observed coordinates and 48 printed erasures; both printed dates retained |
| [p145_A](../cases/open/p145_A.md) | 192 | OPEN; 192 received slots, 187 observed coordinates and 5 printed erasures; transmitted length unknown |
| [p170](../cases/p170.md) | 106 | Open; exact complete-body coordinate bounds under two adjacent squares |
| [p194_D1](../cases/open/p194_D1.md) | 45 | OPEN; 45 observed coordinates against advertised 214; no accepted plaintext or loss frame |
| [p198](../cases/p198.md) | 165 | Open |

The four newly catalogued OPEN cases preserve 595 native slots: 535 observed coordinates and 60 printed erasures. Their [source-only package](../experiments/open_source_records/README.md) verifies the literal rows and original-PDF crops. It introduces no key, completed loss frame, plaintext or decipherment count.

## Quantitative evidence coverage

The structured adapters independently recompute primary source/model accounting for **559 of the 679 bodies**. The other **120 remain unquantified by these adapters**, including OPEN sources and unsupported legacy certificate formats. This is evidence-tool coverage, not the number of unread messages.

| Verified primary frame class | Physical bodies | Native slots | Model positions | Fixed raw labels, unobserved coordinates unassigned | Extra fixed labels from supplied unobserved coordinates |
|---|---:|---:|---:|---:|---:|
| Native order and length | 471 | 100274 | 50137 | 48885 | 0 |
| Modified frame; stated assumptions apply | 88 | 18603 | 10028 | 8204 | 1 |

**These position totals cover only the quantified subset.** A fully fixed stream can retain garbles or uninterpreted numbers. The checker separates native slots, model additions/exclusions, coordinates supplied by another witness and ordinary-word repairs. Optional readings and alternative frames are never added as extra physical sources.

The JSON output identifies the canonical source, state, evidence path and exact count contract for each body. It gives explicit reasons where a primary record cannot yet be quantified. Restricted evidence aliases resolve older package identifiers without creating catalogue rows.

## Other material in the volume

| Material | Printed pages | Separate accounting |
|---|---|---|
| Childs technical explanation | 1–22 | Reused cipher figures and a numeric teaching example are not additional intercepted messages. |
| Teaching cryptograms I–XII | 19–22 | Twelve instructional items under the published VIKINGSCROWNHOTEL example key, outside the log denominator. |
| Konheim Appendix A | 23–54 | Theory and numerical 5×5 examples, including repeated or excerpted ciphertext figures. |
| Appendix B title | 55 | The ciphertext log begins on p56. |
| Appendix C key tables | 232–244 | Fifteen tables on thirteen pages; all have registered key IDs, with unknown cells retained. |
| Cleartext, stubs, header-only items and missing-part notes | Within the log | Recorded exceptions do not create invented ciphertext bodies. |

The older OCR retrieval pool contains 788 unverified blocks on pp57–230 and omits p56. A block may split, merge or omit a source body; its size is not a historical-message denominator. Repeated receptions and numbered parts remain distinct physical witnesses, not a count of distinct complete messages.

## Reproduction

```sh
python data/reviews/verify_childs_material_coverage.py --verify
python data/reviews/verify_childs_material_coverage.py --json > /tmp/childs-current-coverage.json
python data/reviews/verify_childs_material_coverage.py --verify --pdf /path/to/childs.pdf
python data/reviews/verify_childs_material_coverage.py --write-report
```

`--verify` recomputes the structured contracts without writing. `--write-report` refreshes this page. The optional PDF check authenticates the original file and page count; the boundary inspection remains a recorded manual review.

Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, [scanned volume](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The [machine-readable census](../data/reviews/childs_material_census_20261103.json) records page-level review bases, exceptions and the historical baseline; the live JSON output records current file digests.
