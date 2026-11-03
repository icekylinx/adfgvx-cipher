# p107 railway instructions and dragoman-return inquiry

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p107 B1/B2 form one source-labeled two-part railway message; C is a
separate inquiry about dragoman Schaefer's return as his leave ends. All
three use the unchanged published **Nov1–3** key. Read the
[railway case](../../cases/military/chemnitz_verbetz_trains.md) and the
[return inquiry](../../cases/people/schaefer_return_inquiry.md).

## Source-positive correction and conservative readings

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

C has **348 valid coordinates** and a candidate costing **four observed
substitutions**. The opaque address **GEHEIMRATENDERHEIDENBRAILA**, the
spelling **SCHAEFER**, and the conditional clause **SOFERN UEBERHAUPT
AUSFUEHRBAR** remain intact. The message asks whether return is desired and
expedient, and requests a telegraphic report; it does not order a completed
return or identify the people independently.

## Counts and evidence

Three physical records contain **622 visible slots**, **621 valid
coordinates** and **311 plaintext positions**. Raw and edited layers each
fix **310 / 311 positions**. The total cost is **12 observed-coordinate
substitutions and zero fills**, with the one printed dash unresolved.
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
then compares all three regenerated crops pixel for pixel. Scratch caches
are not runtime dependencies.
