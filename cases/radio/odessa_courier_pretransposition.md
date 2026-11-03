# Odessa courier report: a conditional loss before transposition

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

Printed p201 C has **324 received coordinates**, exactly its advertised count. Much of the direct reading concerns Elsner, Wilna, arriving here and further couriers, but a run in its opening is garbled. A bounded alternative inserts two missing coordinates **before transposition**: undo the **324-coordinate transposition**, restore two fractionation positions, and read **163 labels** from 326 coordinates. The opening becomes an address to the German representative in Odessa, followed by **KURIER ELSNER**.

This is a conditional error model, not a change to the source transcription. Every one of the 324 printed slots remains accounted for. Two added fractionation fills recover the opening without changing an observed coordinate there; **four later observed-coordinate substitutions** support the remaining word proposals. The primary edition fixes **160/163 positions** and preserves three coupled unknown reference labels.

Research and editorial work: **icekylinx and GPT-6 Astra Pro**. The published Nov16–18 key retains the credit of George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. The [same-page native address witness](../finance/odessa_wagon_sale.md#p201-a1) retains its earlier body credit. No first historical decipherment or unique original wording is claimed.

## p201 C

Literal header: `C) NKJ (RAT) v LP (4.15 p.m., November 16th); FUER RAT 1720 (16) SSS BERLIN 15/11 (16); RICHI-324`.

The source and two enlarged crops were visually reviewed locally. Their PDF page, rectangles, scales, dimensions and RGB hashes are pinned in [inputs.json](../../experiments/odessa_courier_pretransposition/inputs.json). **Reviewed source crops:** [p201_C_reviewed.png](../../experiments/odessa_courier_pretransposition/sources/p201_C_reviewed.png) · [p201_C_overstrike.png](../../experiments/odessa_courier_pretransposition/sources/p201_C_overstrike.png). [File and pixel verification](../../sources/reviewed-crops.md#verify). The optional `--pdf` check reproduces the reviewed pixels from the original Childs scan; ordinary verification explicitly reports that source-pixel checking was not requested.

**Source transcription — all 324 native slots, with the two overstruck X-like glyphs retained:**

```text
AGXGA XDDXG ADDFD GDGAX XDAGA FFGDV XGAXA VAFAD
VXGXX XAXFD GXXDV GAGFA XDVFX DXXDD GGDVD AAAXG
XGDFX ADFDD XAFDD DGFVV VVFGD ADFVA GVDDA AAGDF
DDVGV GXGVX DXFXX XXXVA DAADD GDADF AAAXD GADDG
DFXXX DFFXF VDGAV AAAGD GFXXF XXFGA AGXAG AAAXD
VXGAA AADXG GDXVG XGXAX GVGVA AGDAA ADXDA DXDXX
GGXAG AADDD FFGDA VFXAA GDDAG AAGGX FVFAX FAGAV
DXXFD FFXAD DXXFX DXFVD DAFDF FXGGX XDGAX AAXAX
GXVG
```

Group 11, source 50–54, appears as **GXXDV**. Both X skeletons at **51 and 52** are visible beneath the heavy overstrike, but the image does not establish ink order or make either reading unambiguous. The primary transcription uses the visible X readings. A conservative **G??DV** analysis is separately retained below; the deciphered words do not select the glyphs. Thus 324 slots have primary ADFGVX readings, of which 322 are not affected by this overstrike qualification.

An independent source audit corrected the initial draft’s row 1 group 4 from DDGAX to the clearly printed **GDGAX**. The [transcription audit](../../experiments/odessa_courier_pretransposition/source_transcription_audit.json) preserves both literal streams and the earlier artifact hashes. Source 15 is therefore already G, and BERLIN is present in the raw reading. This source-reading correction is not charged as a historical ciphertext substitution.

The earlier OCR retained only 315 slots in its p201 block 6. Reading the complete printed rows restores the native 324-slot body. That OCR correction is separate from the two missing fractionation coordinates hypothesized later.

## The direct native layer

**Raw output — unchanged Nov16–18 key, all 324 printed coordinates in the native transposition:**

```text
DEUTSCHENBEVOLLMAEANO?NO?TJ?S?ETRJV?KERELSNERHEUTBBEBERWILNAHIEREINGETROFFENSOLLENKURIERENACHDORTNOCHABFAHR?NXVERBINDXOFFZXOXROEMX2XDERXOXHXLCBERLINXZT?NRX1?111?X
```

This layer fixes **153/162 positions**. ELSNER, WILNA, HIER EINGETROFFEN, SOLLEN KURIERE NACH DORT NOCH and much of the closing are already present. The opening BEVOLLMAEANO… is retained here exactly. The conservative G??DV source analysis fixes 151/162 positions; it does not erase any printed slot from the record.

## What the two-loss model means

All indices below are zero-based. The inverse column permutation always has length **324**. Its output is a 324-coordinate intermediate stream. The proposed original fractionated stream has length **326**, with missing positions **36 and 74**. Inserting **X** and **A** there makes complete plaintext pairs.

The forward check is equally explicit:

1. Fractionate the proposed 163-label plaintext into 326 coordinates.
2. Remove the coordinates at the stated two fractionation positions.
3. Apply the published column permutation to the remaining **324** coordinates.

Before the later word repairs, this process reproduces the entire native received source exactly. After those repairs it reproduces a 324-slot received stream differing from the source at precisely the four disclosed indices. Applying a 326-coordinate column permutation would be a different model and is not used here.

The first missing X can be described at position **36 or 37**, next to the same observed X. Both descriptions produce the same filled fractionated stream. They retain different origin maps and different unfilled pair domains; neither alias is selected as the historical location.

**Raw output — conditional 326-coordinate fractionation frame, with both added coordinates still unknown:**

```text
DEUTSCHENBEVOLLMAE?HTIGTENXODESSAXKUR?ERELSNERHEUTBBEBERWILNAHIEREINGETROFFENSOLLENKURIERENACHDORTNOCHABFAHR?NXVERBINDXOFFZXOXROEMX2XDERXOXHXLCBERLINXZT?NRX1?111?X
```

This unfilled model fixes **157/163 positions**. The restored pair boundaries already expose most of the address and courier wording. Its two question marks at the inserted coordinates remain source absences rather than observed values.

**Conditional interpretation — same fractionation frame after the two explicit X/A fills, before the four ordinary-word repairs:**

```text
DEUTSCHENBEVOLLMAECHTIGTENXODESSAXKURIERELSNERHEUTBBEBERWILNAHIEREINGETROFFENSOLLENKURIERENACHDORTNOCHABFAHR?NXVERBINDXOFFZXOXROEMX2XDERXOXHXLCBERLINXZT?NRX1?111?X
```

The X/A fills fix **159/163 positions**. They are not two additions to the received ciphertext. The received length and the transposition remain 324.

## Bounded placement evidence

The search uses five retrospective prefix spans at fixed offsets: DEUTSCHEN, BEVOLLMAECHTIGTEN, ODESSA, KURIER and ELSNER. It compares every pair of missing positions in a 326-coordinate fractionated stream with the **unchanged 324-coordinate intermediate source**. All **52,975** pairs are priced in each scope. The objective counts conflicts with observed coordinates; inserted values are separately supplied from the chosen word stencil.

| Retrospective word scope | Minimum observed changes | All tied missing-position pairs |
| --- | ---: | ---: |
| All five prefix spans | 0 | 2 |
| ODESSA omitted | 0 | 2 |
| Address words only | 0 | 522 |
| KURIER omitted | 0 | 32 |

The first two scopes retain exactly **[36,74] and [37,74]**. ODESSA therefore appears without being forced by that second stencil. The broader address-only and courier-omitted minima remain in full; they show what depends on the selected courier vocabulary. These are sensitivity checks after the reading was seen, not blind predictions.

Repeating the same scans with both overstruck source glyphs masked leaves the same minimum sets. That protects the geometry comparison from choosing the X readings through the prefix words. Completing the two glyph masks as X would nevertheless be two additional mask fills in that conservative branch.

The existing p201 A1 body directly reads **BEVOLLMAECHTIGTEN** followed by **ODESSA**, with complete observed pairs. Its exact source indices are rechecked in the certificate. This independently attests the recipient vocabulary. It is not an identical courier report and supplies no name, travel route, date or reference number to this body.

## Four separately priced word repairs

The opening recovery and the following spelling proposals have different costs. The latter change four already observed source coordinates, after the fractionation-loss model has been fixed.

| Received source index | Printed coordinate | Proposed coordinate | Role in the word proposal |
| ---: | :---: | :---: | --- |
| 210 | G | F | HEUTBBEBER → HEUTEUEBER |
| 227 | D | A | HEUTBBEBER → HEUTEUEBER |
| 267 | G | A | ABFAHR?N → ABFAHREN |
| 287 | X | F | O H L C → O H L X separator |

The unknown character in ABFAHR?N comes from an unassigned square cell in the unedited frame. Replacing its observed GG pair by the known E pair is a source-coordinate substitution; it does not assign that unknown square cell or alter the reference fields that also use it.

**Edited output — 2 added fractionation fills and 4 observed received-coordinate substitutions:**

```text
DEUTSCHENBEVOLLMAECHTIGTENXODESSAXKURIERELSNERHEUTEUEBERWILNAHIEREINGETROFFENSOLLENKURIERENACHDORTNOCHABFAHRENXVERBINDXOFFZXOXROEMX2XDERXOXHXLXBERLINXZT?NRX1?111?X
```

**Readable German — the complete primary edited stream, with spacing and punctuation only:**

> Deutschen Bevollmaechtigten Odessa. Kurier Elsner heute ueber Wilna hier eingetroffen. Sollen Kuriere nach dort noch abfahren. Verbind. Offz. O Roem 2 der O. H. L. Berlin. ZT? Nr. 1?111?.

**Conditional interpretation — report and enquiry:**

The proposed body addresses the German representative in Odessa, reports that courier Elsner has arrived here via Wilna, and asks whether further couriers will still leave for the destination. The closing gives the literal liaison-officer wording and Berlin. “Here” is not expanded into an independently established location, Elsner is not assigned a full identity, and no arrival time is reconstructed. The question is punctuated with a period in the exact quotation so that ? remains reserved for unknown labels.

VERBIND, OFFZ, O, ROEM 2 and the final ZT? NR field remain as decoded; abbreviations and numbers are not silently expanded.

## Conservative overstrike sensitivity

Keeping source 51 and 52 masked, applying the same two fractionation fills and only the same four observed substitutions gives the following **158/163-position** edition. It does not add source-glyph fills.

**Edited output — conservative G??DV branch, with the two source glyph masks still unresolved:**

```text
DEUTS?HENBEVOLL?AECHTIGTENXODESSAXKURIERELSNERHEUTEUEBERWILNAHIEREINGETROFFENSOLLENKURIERENACHDORTNOCHABFAHRENXVERBINDXOFFZXOXROEMX2XDERXOXHXLXBERLINXZT?NRX1?111?X
```

Completing those two masks as X reproduces the primary visible-X reading, but it would cost **two additional source-mask fills** in this branch. The source image supports the X skeletons; the mathematical completion does not make the overstrike unambiguous.

## Reference labels and exact reproduction

The three remaining primary unknowns occur at plaintext positions **152, 157 and 161**, from the distinct square cells **AF, GG and FD**. Each has the individual domain **0,3,4,5,6,7,8,9**. Because the square is one-to-one, their three labels must be distinct. The literal known 1s and ROEM 2 do not select the missing labels.

All **40,320** assignments to the eight unknown square cells are checked with the forward loss-before-transposition process. They yield **336 distinct ordered reference triples**. One full-square witness for every triple is retained. These are proofs of alternatives, not historical choices of a date, serial or telegram number.

| Quantity | Primary edition |
| --- | ---: |
| Native received slots / advertised slots | 324 / 324 |
| Received transposition length | 324 |
| Reconstructed fractionation length | 326 |
| Plaintext positions | 163 |
| Native fixed positions | 153/162 |
| Unfilled loss-model fixed positions | 157/163 |
| After X/A fills / after four word changes | 159/163 / 160/163 |
| Added fractionation slots / fills | 2 / 2 |
| Received source insertions / exclusions | 0 / 0 |
| Observed substitutions / primary source-mask fills | 4 / 0 |

[The portable verifier](../../experiments/odessa_courier_pretransposition/verify.py) binds the native source, both origin maps, all placement minima and cost-distribution hashes, every word repair, the conservative glyph branch, the live complete displays, the independent address-word pairs and all global reference alternatives. [The certificate](../../experiments/odessa_courier_pretransposition/certificates.json) contains the complete evidence. [The frozen OCR record](../../experiments/odessa_courier_pretransposition/ocr_snapshot.json) preserves the earlier incomplete transcription.

```sh
python experiments/odessa_courier_pretransposition/verify.py --verify
python experiments/odessa_courier_pretransposition/verify.py --verify --pdf /path/to/childs.pdf
```

The exact forward reproduction establishes the arithmetic of the proposed model. It does not authenticate a historical omission mechanism, replace the native reading, or prove global optimality over other keys and error models.
