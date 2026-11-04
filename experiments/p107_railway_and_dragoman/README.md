# p107 railway instructions and dragoman-return inquiry

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p107 B1/B2 form one source-labeled two-part railway message; C is a
separate inquiry about dragoman Schaefer's return as his leave ends. All
three use the unchanged published **Nov1–3** key. Read the
[railway case](../../cases/pages/107.md#edition-cases-military-chemnitz-verbetz-trains) and the
[return inquiry](../../cases/pages/107.md#edition-cases-people-schaefer-return-inquiry).

## Source corrections and conservative readings

The earlier B1 corpus OCR omitted the visible final **FDGD** row, screening
160 coordinates instead of the printed **164**. It also masked source
152, visibly D. `ocr_snapshot.json` freezes that old record and origin
hash; the verifier checks the exact source-visible differences and
reproduces the earlier output under the same key. This recovers the
correct native frame from the scan. The subsequent editorial reading
still costs **five observed-coordinate substitutions**, including source
160 F→V in the restored final row; OCR restoration is not used to hide
that additional source repair.

B2 has the advertised **110 slots**, including a printed dash at source
39. Its candidate costs **three substitutions** and leaves that dash
unknown. The closing remains **?BAXAEK11X10502**, with domain **3BFKQS**
for the first unknown character. All six complete compatibility witnesses
are retained and re-encrypted. No familiar acronym is forced into it.
**PFESS**, **VERBETZ**, the address labels and the train numbers remain
literal.

C has **348 source slots**, with **347 unambiguous coordinates and one
damaged or overstruck glyph**. Its candidate costs **three observed
substitutions and one glyph fill**. The opaque address **GEHEIMRATENDERHEIDENBRAILA**, the
spelling **SCHAEFER**, and the conditional clause **SOFERN UEBERHAUPT
AUSFUEHRBAR** remain intact. The message asks whether return is desired and
expedient, and requests a telegraphic report; it does not order a completed
return or identify the people independently.

### C source 45: uncertainty instead of a definite X

The second row's second group now reads **`?XGFF`**. The first glyph has
V-like upper strokes and lower feet consistent with overprinting or damage;
the scan does not establish either X or V unconditionally. The new
[detail crop](sources/p107_C_source45.png) is bound to original PDF page 110,
rectangle `[188,551,227,568]`, scale 16, dimensions 624×272, PNG hash and
RGB pixel hash. The existing full C crop supplies the wider context.

The conservative source has **173/174 raw fixed positions**, with pair
`A?` and domain `9FILOU` at plaintext position 85. The unchanged full
candidate fills the damaged slot with V to read `SOFERN`; its other three
changes are source 182 F→V, 253 X→V and 292 D→A. The previous account was
four substitutions and no fills. The new account is three substitutions
and one fill, still **four coordinate operations**.

Two explicit branches retain the X and V glyph assumptions. Assuming X
reproduces the earlier `SO9ERN` raw output and requires one replacement of
that assumption in addition to the three observed substitutions. Assuming
V gives `SOFERN` at that position before the three other repairs. Each
fully assigned branch fixes 174 raw positions, but neither is an independent
source observation, parallel copy or additional record. Their hypothetical
counts do not replace the conservative primary account.

The frozen earlier OCR already contained `?` at source 45. Its cipher stream
and `SO?ERN` output exactly match the conservative source now used. That
is an earlier transcription of the same scan, not independent corroboration.
The verifier checks this provenance and retains both hypothetical streams.

## Counts and evidence

Three physical records contain **622 visible slots**, **620 unambiguous
coordinates** and **311 plaintext positions**. The raw layer fixes
**309/311 positions**; the edited layer fixes **310/311**. The total cost is
**11 observed-coordinate substitutions and one damaged-glyph fill**, with
the one printed B2 dash unresolved.
All native lengths match; there are no historical source insertions,
deletions, rank changes, square changes or global numerical relabelings.
B1 and C re-encrypt completely; all six B2 witnesses re-encrypt exactly.

`inputs.json` preserves literal rows, headers, crop geometry and key
provenance. `certificates.json` retains every source index, coordinate pair,
domain and change. `prior_candidates.json` retains earlier body candidates,
unread OCR frames and bounded publication checks. This edition makes no
historical first-solution claim. The proposal counts only B1, B2 and C;
previously reviewed D and the separate RIZI message A are excluded.

## Reproduce

From the repository root:

```sh
python experiments/p107_railway_and_dragoman/verify.py --verify
```

This uses the standard library and checked-in cipher module. Optional
original-PDF crop verification requires PyMuPDF and Pillow:

```sh
python experiments/p107_railway_and_dragoman/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier checks the original PDF's frozen byte count and SHA-256,
then compares all four regenerated crops pixel for pixel. It also verifies
the damaged-glyph source map, both X/V assumption branches, all repair and
fill ledgers, the unchanged C reading and its complete readable-label mapping.
Scratch caches are not runtime dependencies.
