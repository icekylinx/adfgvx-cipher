# Munich couriers carrying radio operating documents

The proposed first part tells the Engineer Inspectorate in Munich that the two named men left at 7 p.m. as couriers carrying radio operating documents for `GRUKONACH?02`. The continuation instructs the recipient to notify that unit and telegraph the arrival back to the sender.

**Complete edition by printed page:** [p. 151](../pages/151.md) · [p. 153](../pages/153.md) · [p. 158](../pages/158.md) · [p. 162](../pages/162.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Source and certificate](../../experiments/courier_recovery/README.md) · [Reading conventions](../../docs/reading-conventions.md)

Five records intercepted on 9 November concern couriers carrying radio operating documents to Munich: first parts p153 E1 / p162 A1 and continuations p151 D2 / p153 D2 / p158 C2. The best continuation fixes **67 of 68 positions** under the published Nov7–9 key; the damaged first part has a conditional 134-position reconstruction. The unit numeral remains **{5,6}** in the key, with a historical argument for **6** below.

## Most likely reading

The first part is an editorial reconstruction with the source costs below:

**Readable German:**

> An Ingenieurinspektion Muenchen. Gefr. Geraus und Feldgr. Mahrer als
> Kurier mit Funkbetriebsunterlagen fuer Grukonach{5,6}02 7 Uhr abds.
> nach dort abgefahren.

The best-preserved second-part witness, p158 C2, reads directly without any
source-coordinate change:

**Readable German:**

> Grukonach{5,6}02 benachrichtigen. Eintreffen hierher drahten.
> Nachrchef 4 B 49909.

**Meaning:** The proposed first part tells the Engineer Inspectorate in
Munich that the two named men left at 7 p.m. as couriers carrying radio
operating documents for `GRUKONACH?02`. The continuation instructs the
recipient to notify that unit and telegraph the arrival back to the sender.

The names `GERAUS` and `MAHRER` remain unidentified; their U and H are not supported across every fit of both alignment models. The reading retains the unexpanded `FELDGR` and singular `ALS KURIER`.

## What is directly supported

All three second-part records contain exactly 136 coordinates. Under the
known partial square, each fixes 67 of 68 plaintext positions. The p158 C2
text is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
GRUKONACH?02BENACHRICHTIGENEINTREFFENHIERHERDRAHTENXNACHRCHEF4B49909
```

</details>

The p151 D2 repeat has `GRU1ONACH` at the beginning, and p153 D2 has
`BENACHWICHTIGEN`; the source edition preserves both. The unaltered p158
witness independently supplies the readable forms of both words.

The question mark denotes the observed pair **VF**, whose unassigned square value is **5 or 6**.

### A separately linked conditional reading: GRUKONACH602

The [November 9 operational reports](../military/nov9_operational_reports.md#historical-identification-most-likely-the-6th-reserve-division) use the same **VF** cell for a reserve-division numeral. A contemporary French telegram identifies the matching formation as the **6th Reserve Division**. Under that historical identification, **VF=6**, and both courier fields read **GRUKONACH602** with no additional source-coordinate changes.

This is one historical inference applied through a shared key cell. The base domain remains 5/6; the first-part reconstruction and its association with the continuation retain the assumptions below. The [context certificate](../../experiments/p170_continuation/military_context.json) records the external source, its date limits and the earlier p176b application.

## First-part damage and explicit reconstruction cost

The first parts both advertise 268 coordinates but actually preserve 259
and 264 slots. Both visibly contain the six-letter group `VXDVDD`, which
the transcription retains. One overstruck glyph in p162 A1 is masked as a
source erasure; its displayed reading is kept separately.

Comparing the two sources without the key finds a five-slot relative gap:
all 260 possible gap starts were tested, and seven tied starts, 151–157,
leave only two known-coordinate disagreements. This does not locate the
other four slots missing from the longer witness.

For the **stated 134-position candidate**, exact alignment gives:

| Alignment model | p153 E1 | p162 A1 |
|---|---|---|
| Retain every source coordinate | Insert 9 slots; change 6 known coordinates; 32 tied minimum fits | Insert 4 slots; change 8 known coordinates; 2 tied minimum fits |
| Delete one received coordinate | Delete 1, insert 10; change 4 known coordinates; 192 tied minimum fits | Delete 1, insert 5; change 6 known coordinates; 14 tied minimum fits |

Every deletion position and tied optimum is retained. A fill of the overstruck p162 glyph is charged separately from observed-coordinate changes.

Within the first model, **123/134 proposed positions** have an unchanged coordinate pair in at least one witness for every combination of minimum fits. Requiring that support under both models gives **118/134**. These counts are conditional on the proposed wording and alignment families. The [certificate](../../experiments/courier_recovery/certificate.json) includes all raw masked-frame readings and exact costs.

## Association, source and credit

The two first-part records explicitly say first part of two, and all three
continuations say second part. The p153 D/E headers both read `RVV v N4` on
the same morning; the first-part `2120 (SY)` field also fits the p151 D
`SY v N4` continuation. Both bodies use the same unresolved `GRUKONACH?02`
field, and the instruction to report arrival follows naturally from the
departure notice. These facts support the association, but the typed log
does not explicitly cross-reference the parts as one original transmission.
The direct continuation remains readable independently of that association.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed pp. 151, 153, 158 and 162 / PDF pp. 154, 156, 161 and 165,
in the [public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [source inputs](../../experiments/courier_recovery/inputs.json) give
literal rows, headers and reproducible image rectangles. The Nov7–9 key
retains its historical and George Lasry / coauthor attribution in
[the key register](../../data/keys.json).

Source inspection, repeated-copy recovery, reconstruction and edition: **icekylinx and GPT-6 Astra Pro**.

```sh
python3 experiments/courier_recovery/build.py --verify
python3 experiments/courier_recovery/verify.py
```

</details>
<!-- CASE-EDITION:END -->
