# Medical arrangements for transports returning from Turkey

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

Five source editions are recorded from Childs pp212–213 (22 November 1918): four readable medical passages and an interposed oil-cartel dispatch query. The medical passages recommend a heated sick wagon, cooking equipment and continuously available hot tea, and ask for the arrangements to be made as far as possible from Constantinople. They cite an appeal to the German governor at received `NIKOLA9EW`. They do not establish that the requested arrangements were made.

The [medical reading](../../pages/212.md#edition-cases-military-medical-return-transports) and [separate oil query](../../pages/212.md#edition-cases-finance-oil-cartel-dispatch-query) retain every raw string. [inputs.json](inputs.json), [certificates.json](certificates.json), [source crops](sources) and the verifier supply exact coordinates, mappings and repairs.

The later [p212 A4 partial edition](../p212_medical_fragment/README.md) supplies a separately verified 302-slot hypothesis and 129/151 labels. The original five-record certificate below remains unchanged; A4 is counted once through its new catalogue entry.

## Framing and the two unread fragments

The p212 header says `XYZ v LP (03.54 p.m., November 22nd); ----- 7 TLE`. Numbered parts 1/2/4/5 occur on that page, and 6/7 continue under the same date on p213. The 224-coordinate oil query between parts 2 and 4 has **no visible “3 TL” label**. `p212_A3` is its positional catalog identifier; the edition does not treat its different subject as medical content or claim to reconstruct a complete seven-part message.

Two additional frames are preserved outside the certificate's `records` list, in `contextual_unread_records`:

| Source frame | Observed coordinates | Printed length / condition | Reading claim |
| --- | ---: | --- | --- |
| p212 A2 | 160 | Advertised 284 | None |
| p212 A4 | 197 | “Missed start”; no readable total | None |

They add **zero** records or positions to the readable summary and catalog proposal. Their crops and literal rows remain available for future work. Neither is padded into a plausible message or joined to the oil query.

## Conditional reconstruction of p212 A1

The source advertises 344 coordinates but prints 339, including invalid printed Y at source index 248. A single five-coordinate gap makes a 172-position model. The proposed ordinary-word text fits at a minimum cost of **nine observed-coordinate substitutions plus six fills** (five missing coordinates and the printed Y).

This fit is **not unique**. Exhausting all 340 possible gap positions gives four equally economical placements: **104, 105, 107 and 108**, all zero-based. The primary presentation uses 105 because it is the only tied minimum at a five-coordinate group boundary. That is an additional source-group assumption, not proof that 105 is the historical loss location.

All four raw model strings, all source-index mappings, all repair events, and every gap cost are frozen. Each variant re-encrypts the same proposed plaintext exactly, while its source edits and missing group differ. The candidate itself is not called an independent witness. The retained exploratory language ranking is a retrieval aid only and is independently replayed; its score is not historical evidence.

The received abbreviation `BEIMOSANOFFMILMISZ` is left unexpanded. `NIKOLA9EW` remains a raw published-square spelling, with no global 9-to-J assignment.

## Conservative later readings

| Record | Ordinary-coordinate substitutions | Printed-glyph fills | Remaining uncertainty |
| --- | ---: | ---: | --- |
| p212 A3, oil query | 5 | 0 | Reference label 2 unchanged; association with medical parts unasserted |
| p212 A5, sick wagon and kitchen | 5 | 1 | Instruction label 2 unchanged |
| p213 A6, forwarding and water points | 5 | 0 | `5T` bridge and erased position before DEPARTEMENT retained |
| p213 A7, arrangements from Constantinople | 0 | 1 | `NIKOLA9EW` and complete raw reference unchanged |

A6's unfilled position is plaintext index 118, received pair `?X`, source indices 39 and 242, domain `1GJKWX`. The literal dash at source index 39 remains a dash in the source and an erasure in both reading layers. The two received labels `5T` after `SPRUCH` are fixed under the square but remain semantically unresolved. Fixed labels must not be mistaken for fully understood wording.

All three `NIKOLA9EW` occurrences, the A5 instruction marker, the A3 reference marker and the entire A7 footer `KMXAXDXNRQJ0XXYYXY5XAYY` have unchanged coordinate witnesses. No later-period key relabeling is imported. Ordinary-word corrections of raw numeral labels in damaged words are local ciphertext edits and appear in the complete before/after inventory.

## Counts and attribution

The five proposed reading records preserve 1,437 printed source slots, of which 1,433 are valid coordinates. With A1's five-position gap they model 1,442 coordinates and 721 plaintext positions. The primary raw models fix 712 positions; the conservative candidates fix 720. Across the five records there are 24 observed-coordinate substitutions, three printed-glyph fills, five missing-coordinate fills, one printed erasure still unresolved, and no key/rank changes or deletions. A1's four alternative geometries are not counted as four physical records.

Earlier unreviewed repository candidates already recognized the oil query, the sick-wagon instruction and the final medical paragraph. Their strings and hashes are frozen. The source edition adds exact frames, conditional first-part reconstruction, costed repairs and explicit gaps. Bounded checks of the Lasry–Niebel–Kopal–Wacker paper, Lasry dissertation and cached 2017 comments found no explicit discussion of these bodies; this does not establish historical priority. No first historical decipherment is claimed.

## Reproduce

From the repository root, with Python 3.10 or later:

```sh
python experiments/medical_return_transports/verify.py --verify
python experiments/medical_return_transports/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The standard check uses the standard library, the repository cipher module and the already frozen repository quadgram weights. It independently builds every inverse-transposition index/domain, exhausts the exact gap-cost screen, replays all tied repairs and the exploratory ranking, checks untouched labels, and compares the frozen certificate. The PDF option additionally needs PyMuPDF and Pillow and reproduces the crops pixel for pixel after checking the PDF hash.

The preserved exploratory ranking is verified by hypothesis identity, exact raw text and counts, and the frozen model hash. Score recomputation allows an absolute difference of at most `1e-12` to accommodate float-summation differences between Python versions; the original ranking and all source/geometry conclusions are unchanged.
