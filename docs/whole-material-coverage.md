# Whole-material source coverage

Prepared by **icekylinx and GPT-6 Astra Pro**. This dashboard separates source boundaries, catalogue editions, and decipherment evidence.

## Scope and denominator

**Appendix B contains 679 actual printed ciphertext bodies on printed pages 56–230 (175 pages).** A separately printed part or received copy is one physical body. Surviving damaged fragments count; advertised but absent parts do not. The two literal `AAA` items at p58 A1/A2 remain separately registered ambiguous stubs, outside this body count.

Every log page has a recorded boundary review. That review checks where bodies begin and end; it does not claim a fresh transcription of every glyph, a unique key for every body, or complete plaintext recovery.

## Current tree and preserved starting snapshot

| Measure | Current tree | Starting snapshot, 2026-11-03 08:04:46 UTC |
|---|---:|---:|
| Reviewed catalogue edition entries | 659 | 640 |
| Distinct catalogued physical bodies | 658 | 639 |
| Original challenge entries | 22 | 22 |
| Other catalogue entries | 637 | 618 |
| Additional physical bodies beyond challenges | 636 | 617 |
| Bodies outside the current catalogue | 21 | 40 |

Current catalogue metadata records source review for **658 distinct bodies**. This is the existing source-review evidence status, not a number of solved messages. The registered p132 / p132_B overlap is one physical body with two edition entries. The current counts come from the files in this checkout; the fixed baseline is never substituted for them.

There are **0 uncatalogued bodies** with an explicitly registered local review package in this checkout. They remain outside the catalogue count until integration. Publication status and local research status are distinct.

## Quantitative evidence coverage

The bounded structured adapters independently recompute primary source/model accounting for **541 of the 679 bodies**. The other **138 bodies remain unquantified by this dashboard**; that includes unsupported legacy certificate shapes and genuinely missing editions. It does not mean that all of them lack prior decipherment work.

| Verified primary frame class | Physical bodies | Native slots | Model positions | Fixed raw labels, all unobserved coordinates unassigned | Extra fixed labels from supplied unobserved coordinates |
|---|---:|---:|---:|---:|---:|
| Native order and length | 468 | 100002 | 50001 | 48781 | 0 |
| Modified frame; its stated assumptions still apply | 73 | 15739 | 8180 | 7198 | 1 |

These position totals cover only the quantified subset. **They are not a whole-corpus plaintext-completion percentage.** A fully fixed raw stream can retain garbles or uninterpreted numbers. The checker separates native source slots, conditional model additions/exclusions, and coordinates supplied from another witness; it does not combine alternative models or optional prose into a primary total.

The per-body JSON output includes exact evidence paths and explicit reasons when a primary record cannot yet be quantified. Candidate-label and repair counts are included only where the candidate contract can also be independently decoded.

## Complete current catalogue gap list

| Printed page | Actual body sections outside catalogue | Registered local edition or existing artifact lead |
|---:|---|---|
| 70 | B1 | No structured edition registered here |
| 71 | A2 | A2: `experiments/october_caucasus/inputs.json` (lead; coverage not inferred) |
| 84 | C | No structured edition registered here |
| 127 | B2 | No structured edition registered here |
| 137 | A6, B | A6: `experiments/transylvania_situation_report/inputs.json` (lead; coverage not inferred) |
| 145 | A | No structured edition registered here |
| 152 | A2 | No structured edition registered here |
| 154 | A2 | No structured edition registered here |
| 163 | A16 | No structured edition registered here |
| 164 | D | No structured edition registered here |
| 167 | C1, D | No structured edition registered here |
| 176 | A6 | A6: `experiments/romanian_ultimatum_companions/inputs.json` (lead; coverage not inferred) |
| 194 | D1 | No structured edition registered here |
| 198 | A | No structured edition registered here |
| 212 | A4 | A4: `experiments/p212_p218_crosscopy/inputs.json` (lead; coverage not inferred); A4: `experiments/medical_return_transports/inputs.json` (lead; coverage not inferred) |
| 215 | A, B1, B3 | No structured edition registered here |
| 219 | C | No structured edition registered here |

An artifact lead can be a diagnostic or contextual mention. Its existence does not count as a recovered body. The local label A16 at p163 identifies the actual fragment between printed parts 15 and 17; it does not assert a printed `16 TL` heading.

## Other material in the volume

| Material | Printed pages | Separate accounting |
|---|---|---|
| Childs technical explanation | 1–22 | Includes reused cipher figures and an internal numeric teaching example; figures are not new intercepted messages. |
| Twelve numbered teaching cryptograms I–XII | 19–22 | 12 instructional items under the published VIKINGSCROWNHOTEL example key; kept outside the 679-body log denominator. |
| Konheim Appendix A | 23–54 | Theory and numerical 5×5 teaching examples, including repeated or excerpted ciphertext illustrations; no new historical-message count. |
| Appendix B title | 55 | Ciphertext log starts on p56. |
| Appendix C key tables | 232–244 | 15 printed tables on 13 pages, all represented by existing key IDs; unknown cells remain unknown. |
| Cleartext, short stubs, header-only items and missing-part notes | Within the log | Explicit exceptions are retained separately in the census; they do not create invented ciphertext bodies. |

The frozen OCR pool has **788 unverified blocks on pp57–230**, omitting p56. Blocks can split, merge, or omit real bodies; subtracting catalogue entries from 788 does not measure remaining messages. Duplicate transmissions and separately printed parts are retained as physical witnesses. Their number is not a claim about the number of distinct complete historical messages.

## Reproduction

```bash
python data/reviews/verify_childs_material_coverage.py --verify
python data/reviews/verify_childs_material_coverage.py --json > /tmp/childs-current-coverage.json
python data/reviews/verify_childs_material_coverage.py --verify --pdf /path/to/childs.pdf
python data/reviews/verify_childs_material_coverage.py --write-report
```

`--verify` is read-only. `--write-report` explicitly refreshes this dashboard from the live tree. The optional PDF check pins the original file bytes and page count; the source-boundary inspection itself is a recorded manual review, not an automated glyph-recognition claim.

Current catalogue SHA-256: `663c0a47e7a0926e5e1f73c711e505674a537b3660553f57ecaf5f25c41da5f6`.
Census SHA-256: `2edad8ccbe1e589ae5e1b0497dd4d594d197f3ec5a5c1178e499d47f8a37ef87`.

Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, [complete scanned volume](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). See the [machine-readable census](../data/reviews/childs_material_census_20261103.json) for page-level review bases and material exceptions.
