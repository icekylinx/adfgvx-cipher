# Five-part Black Sea evacuation routing order

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.**

Childs pp88–90 preserve a five-part order with the repeated header
`OSM de LP (01.18 p.m., November 1st); SSD BVG KOSPOLI (1/11) 1400 5 TEILE`.
Its source sequence is **p88 C1 → p89 A2 → p89 A3 → p89 A4 → p90 A5**.
The common headings, explicit part count and consecutive numbering establish
the assembly. The source time fields are retained literally. All parts use the
unchanged published **Nov1–3** key.

**p89 A2 is already cataloged and credited to Ayush Agarwal.** Its conservative
source reading is frozen as context in [existing_part2.json](existing_part2.json),
without changing its source, filling its three unknown positions, or counting
it again. The proposal and primary totals cover only the other four records.

| New source edition | Visible source slots | Modeled coordinates | Plaintext positions | Raw fixed | Edited fixed | Observed substitutions | Printed-dash fills | Lost-coordinate fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p88 C1 | 298 | 298 | 149 | 149 | 149 | 1 | 0 | 0 |
| p89 A3 | 258 | 358 | 179 | 81 | 151 | 1 | 1 | 69 |
| p89 A4 | 360 | 360 | 180 | 180 | 180 | 4 | 0 | 0 |
| p90 A5 | 398 | 398 | 199 | 199 | 199 | 2 | 0 | 0 |
| Total | 1,314 | 1,414 | 707 | 609 | 679 | 8 | 1 | 69 |

There are **1,313 valid observed coordinates** and one printed dash. “Fixed”
means a single-symbol algebraic domain, not historical correctness of a received
symbol. Three new parts use native frames and re-encrypt completely after their
stated word repairs. The third part's source-declared loss and conditional text
restoration are the substantial additional result.

## The explicit 100-coordinate loss in p89 A3

The source prints **`(missed 20 groups)`** after five rows totaling **200
visible coordinates**, before `FFVFG`. It supplies another 58 visible slots
after that annotation. The conventional five-coordinate groups therefore add
**100 unknown coordinates at exactly source boundary200**, giving the declared
**358-coordinate** frame. This is fixed by the source annotation and advertised
length, not selected by trying different language-scored gap positions.

The resulting raw reading fixes **81 / 179** positions. A language-based
restoration of its first **127** positions supplies the following continuous
clauses: nothing goes to Braila; ships already on their way there should turn
back; onward movement is to be in whole trains; “destination for ...”. All
supplied letters fit the surviving-coordinate domains except one observed
**L→W** in `UNTERWEGS`. Its exact price is:

- **One observed substitution:** source243 A→G.
- **One printed-dash fill:** source242→A.
- **69 fills of coordinates explicitly missing from the source.**

The remaining tail is preserved exactly as raw. The main candidate fixes
**151 / 179** positions, leaves **28 plaintext positions** unresolved and does
not complete the apparent military, garrison or `BERL??` fragments from context.
The following part's word `BERLIN` is not imported into this tail.

This restoration is an editorial hypothesis constrained by the surviving
ciphertext. The frame's location and size are source-supported; the missing
letter values are not independently supplied by a duplicate. A bounded query of
**230 known-side literal ten-coordinate strings** against all **788** corpus
blocks finds only the two OCR pieces of this record. It finds no independent
literal copy, while leaving re-encryption under another key, short repetitions
and OCR-obscured duplicates outside that conclusion.

## Exact unresolved space and witnesses

After the stated restoration, **31 missing coordinates** remain. They affect
25 plaintext positions with one erased coordinate and three with two. Because
the fixed square and transposition are bijective, the number of distinct
complete compatible plaintexts is exactly

**6^31 = 36^3 × 6^25 = 1,326,443,518,324,400,147,398,656.**

This is a mathematical count, not a full enumeration. The certificate retains
one arbitrary A-valued baseline and all **155** single-coordinate alternatives
that change one of its 31 unknown slots to D, F, G, V or X. Every witness is
decrypted and re-encrypted exactly and preserves all fixed candidate positions.
None is selected as the historical completion. The very large unresolved space
is kept visible alongside the useful restored prefix.

## Other source qualifications

The p89 A4 detail crops confirm G in `GVGAG` and X in `XDXFX`; faint ink could
look C-like or Y-like at lower resolution. The primary transcription uses the
visible G bar and crossed X diagonals. These are source-reading corrections to
the initial visual impression, not editorial changes to the historical cipher.

The name `SIEGFRIED`, routing abbreviations, numerical references and dates
remain literal. No vessel or formation is independently identified. Printed
cleartext following p90 A5 asks for an acknowledgment and gives a transmission
window. That cleartext is preserved separately and does not enter ciphertext
or plaintext-position counts.

## Reproduction and attribution

```bash
python experiments/black_sea_evacuation_routes/verify.py --verify
python experiments/black_sea_evacuation_routes/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default verifier uses the standard library and repository cipher module.
It independently reconstructs the transposition map, accounts for every visible
and missing source slot, checks all raw domains and exact edits, regenerates the
finite completion witnesses, reproduces the unchanged credited part2 context,
and repeats the bounded literal-copy audit. The optional PDF mode requires
PyMuPDF and Pillow and checks the source PDF hash, size and seven crop images
pixel for pixel. No external language model or temporary cache is required.

[Inputs](inputs.json), [certificates](certificates.json),
[prior candidates](prior_candidates.json), [literal-copy audit](literal_copy_audit.json),
[catalog proposal](catalog_proposal.json) and the
[readable case](../../cases/pages/088.md#edition-cases-military-black-sea-evacuation-routes) retain the
complete evidence. The first and fifth bodies already had readable repository
candidates; p89 A2 retains **Ayush Agarwal's 28 October 2026** body credit and the
earlier conservative review. The prior OCR for A3 omitted the declared loss.
Bounded searches of the paper, thesis and cached comments do not establish
historical priority, and no first-solution claim is made.
