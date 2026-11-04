# Sale of communication apparatus: p157 B1–B2

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** Two readable source parts, with one final source-erased symbol still unresolved.

Source edition and repair accounting: **icekylinx and GPT-6 Astra Pro**. Published **Nov7–9** square and ranks: Lasry, Niebel, Kopal and Wacker, unchanged. Earlier unreviewed OCR-derived candidates already identified much of this apparatus-sale message. They, and their frozen p73 retrieval uses where present, are explicitly preserved; the present work provides the source edition and full repair ledger rather than a universal first-decipherment claim.

## Meaning and source

The telegram tells the Nachrichtenchef that selling apparatus is advisable because of transport difficulties. It says the Romanians want to buy Siemens teleprinters and telephone apparatus, and requests permission and a sale price by radio. This is a request in the text; the edition supplies no evidence that the sale was approved or completed.

Childs printed page 157 / PDF page 160 gives `B) LP v NKJ (7.26 p.m., November 7th)`, `1400 (7) VON UKS 2 TLE`, with lengths 170 and 272. The source heading is 7 November 1918. Both native coordinate frames are preserved exactly.

## Source and repair totals

| Part | Source slots | Printed erasures | Raw fixed positions | Edition fixed positions | Known-coordinate substitutions | Erasure fills |
|---|---:|---:|---:|---:|---:|---:|
| p157_B1 |170|4|81/85|85/85|1|4|
| p157_B2 |272|15|121/136|135/136|5|14|
| **Total** |**442**|**19**|**202/221**|**220/221**|**6**|**18**|

A fixed position means a single symbol under the stated source frame and published key. It does not mean every damaged source letter is historically certain.

## p157 B1 — Apparatus sale recommended because of transport difficulties

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
NA?HRICHTENCHEFGRXHX?XWEGENTRANSPORTSC0WIERIGKE?TENVERKAUFVONAPPARATENEMPFEHLE?SWERTX
```

**Edited output:**

```text
NACHRICHTENCHEFGRXHXQXWEGENTRANSPORTSCHWIERIGKEITENVERKAUFVONAPPARATENEMPFEHLENSWERTX
```

</details>

## p157 B2 — Romanian purchase request and request for permission and price

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
RUMA?NENW?LLEN?IEME?SFERNSCHR?IBERUNDFE?NSPRECHAP?AR?TEKAU?ENX?ENEHMIGUNGUNGVERKAUFSP?EISDURCHFUNKSPRUCH?RB?TENNKONAC?18ROEMX3ANRX11023?
```

**Edited output:**

```text
RUMAENENWOLLENSIEMENSFERNSCHREIBERUNDFERNSPRECHAPPARATEKAUFENXGENEHMIGUNGUNDVERKAUFSPREISDURCHFUNKSPRUCHERBETENXKONACH18ROEMX3ANRX11023?
```

</details>

## Repairs and remaining reference

`SIEMENS`, `FERNSCHREIBER` and `FERNSPRECHAPPARATE` are explicitly editorial lexical completions. Most lost letters can be filled without changing an observed coordinate. The A in `APPARATE`, however, requires **one observed-coordinate substitution in addition to its erased-coordinate fill**; the ledger does not count this as a pure erasure restoration.

Part 1 repairs raw `SC0WIERIGKE?TEN` to `SCHWIERIGKEITEN`, changing one observed coordinate and filling the missing I. This repairs a local word and does not assign H to the baseline key's digit0 elsewhere.

Part 2 also repairs raw `GENEHMIGUNGUNG` to `GENEHMIGUNGUND` at a cost of two observed coordinates. Proposed closing punctuation `ERBETENX` replaces raw `ERBETENN`, also at a cost of two observed coordinates. The source reference after it remains `KONACH18ROEMX3ANRX11023?`; its abbreviations and number labels are not expanded or reinterpreted.

The final unknown symbol has source pair `?V` at indices 40 and 245 and exact domain **DEQTUX**. It might be a separator, but this edition does not choose one. Its one printed erasure remains unfilled. No key assignment is made.

## Reproduction and attribution limits

There are **zero added or deleted coordinates, block reorders, baseline key changes or new numeral assignments**. Every printed erasure, observed substitution and remaining plaintext domain is recorded in [the certificate](../../experiments/apparatus_sale_request/certificates.json), alongside raw and edited round trips. Global completion witnesses are consistency examples, not recovered originals.

The [input record](../../experiments/apparatus_sale_request/inputs.json) contains the literal manual rows, original headers and full crop-rendering provenance. The [experiment README](../../experiments/apparatus_sale_request/README.md) gives the default verification and optional exact PDF-pixel comparison commands.

A bounded check of the author paper and the cached complete2017 discussion found no explicit prior body identification for these particular records. Earlier machine-derived body leads remain credited, and this check is not a universal priority search.
