# State-bank accounting request and dispatched cheques

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The two-part message addresses Staatsbank Berlin, asks for an accounting amount connected to the Generalkriegskasse, and requests notice of arrival of dispatched cheques. It contains no recovered payment amount. The first part needs one explicitly modeled missing coordinate; the second part uses its complete native frame.

## Source and frame

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p172 excerpt](../../experiments/staatsbank_accounting_cheques/sources/p172_reviewed.png) · [Inputs](../../experiments/staatsbank_accounting_cheques/inputs.json) · [All coordinate and insertion certificates](../../experiments/staatsbank_accounting_cheques/certificates.json)

The source page heading says November 10. Section D has an interception header dated November 11 and an originating line `VON UKS LP 2127 (9/11) 2 TLE`. The published Nov7–9 key is retained with its two unresolved square cells; none of these date layers is silently normalized.

The first part advertises 198 coordinates but contains 197 occupied slots. Its sixth group is the four-coordinate `ADAX`. The model adds one unknown coordinate at one of that group’s five boundaries. It does not add a complete plaintext letter or change the period key. The second part has exactly its advertised 204 positions.

| First-part insertion boundary | Observed substitutions for displayed proposal | Printed-mask fills | Additional-slot fills |
| --- | ---: | ---: | ---: |
| 25 | 4 | 3 | 1 |
| 26 | 3 | 3 | 1 |
| 27 | 2 | 3 | 1 |
| 28 | 2 | 3 | 1 |
| 29 | 3 | 3 | 1 |

All indices are zero-based. Boundaries **27 and 28 tie**, and inserting the proposed A at either side of the already printed A gives the same completed ciphertext. The primary display uses boundary 28. This equality leaves the precise loss location unresolved; a minimum against proposed German words is not a unique historical diagnosis. The native 197-coordinate diagnostic, including its unpaired intermediate coordinate and source provenance, remains in the certificate.

## p172 D1

**Source transcription — header:** `D) LP v NKJ (6.06 p.m., November 11th); VON UKS LP 2127 (9/11) 2 TLE; 1 TL RICHI-198`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 198-coordinate frame after one modeled insertion; 95/99 fixed positions:**

```text
STAATSBANKBERLINXERBITTENDRINLICHOTFUNKSPRU?HFUERBEST?RREICHERABRECHNUNGBETRAGD?RGENE?ALKRIEGSKASSE
```

**Edited output — 2 observed-coordinate substitutions, 3 printed-mask fills and one additional-slot fill; the insertion remains conditional.**

```text
STAATSBANKBERLINXERBITTENDRINLICHSTFUNKSPRUCHFUEROESTERREICHERABRECHNUNGBETRAGDERGENERALKRIEGSKASSE
```

</details>

**Readable German — preserves the exact nonseparator labels of the edited output:**

> Staatsbank Berlin. Erbitten DRINLICHST Funkspruch fuer OESTERREICHER Abrechnung Betrag der Generalkriegskasse

**Meaning:** The first part addresses Staatsbank Berlin and asks urgently by radio for an accounting amount concerning the Generalkriegskasse. The proposed word OESTERREICHER is left unexpanded; it is not used to identify a person or prove an Austrian institutional connection. The request continues in part 2.

**Editorial limits.**

- The source has 197 slots against the printed 198, with the four-coordinate group ADAX. One additional modeled slot is required for the disclosed 198-coordinate frame.
- All five insertion boundaries around ADAX are retained. Boundaries 27 and 28 tie for the lowest observed-change cost under the stated word proposal and yield the same completed ciphertext; neither is asserted as the unique historical loss location.
- DRINLICHOT to DRINLICHST and BEST?RREICHER to OESTERREICHER are explicitly priced lexical proposals. DRINLICHST remains a source-length spelling without inserting a G.
- The two printed dashes in DVX-- and C-shaped glyph in ACAXA occupy source slots and are filled separately from the additional coordinate.
- The page heading says November 10, this section's interception header says November 11, and its originating line says 9/11. All three source layers are retained; the Nov7–9 key is unchanged.

## p172 D2

**Source transcription — header:** `D) LP v NKJ (6.06 p.m., November 11th); VON UKS LP 2127 (9/11) 2 TLE; 2 TL RICHI-204`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 204-coordinate frame; 97/102 fixed positions:**

```text
VOM18XBISENDEOOTOBERGEZAHLTENYAYKXFERNERA?KUNFTSANZ?IGEUEBERA??XGESANDTECHEKSXHAUPTWECHSE?AMT89240911X
```

**Edited output — 3 observed-coordinate substitutions, 4 printed-mask fills; no source coordinate inserted, removed or moved.**

```text
VOM18XBISENDEOCTOBERGEZAHLTENMARKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSELAMT89240911X
```

</details>

**Readable German — preserves the exact nonseparator labels of the edited output:**

> Vom 18 bis Ende October gezahlten Mark. Ferner Ankunftsanzeige ueber am ? gesandte CHEKS. Hauptwechselamt 89240911.

**Meaning:** The continuation concerns the amount of marks paid in the period represented by 18 through the end of October, and asks for notice of arrival of cheques dispatched on an unresolved date. The closing is Hauptwechselamt followed by the literal reference 89240911; that reference is not treated as the requested payment amount.

**Editorial limits.**

- The native 204-slot second part needs no length adjustment. OOTOBER to OCTOBER and YAYK to MARK are priced observed-coordinate changes; four printed dashes are filled explicitly.
- CHEKS is retained without supplying an extra letter. The footer 89240911 is not silently split into a date or interpreted as a currency quantity.
- The unresolved date-like position after AM is square cell VF, whose remaining domain is {5, 6}. The value is not inferred from the source date or the earlier baseline completion.
- No amount paid is recovered: the telegram asks for an amount. The first part and this continuation must not be read as reporting that the footer is a monetary total.

## Joint meaning and unresolved labels

Read together, the parts ask for a radio report of an accounting amount connected with marks paid by the Generalkriegskasse in the period represented by `18` through the end of October, followed by a request for arrival information about cheques. The prose does not turn the closing reference `89240911` into either a payment amount or a reconstructed date.

The proposed OESTERREICHER reading costs a source change and a separately disclosed erasure fill. Its administrative referent is unresolved. DRINLICHST and CHEKS remain source-length spellings; no omitted G or extra C is supplied as formatting. The question mark after AM is cell VF with domain `{5, 6}`. Choosing either digit would also constrain the other unresolved Nov7–9 square cell; no such historical assignment is made. Specifically, VF must be the opposite label from the three shared XA positions in the [p155 C1/C2 repetition edition](../radio/nov7_eighth_part_repetition.md).

| Joint account | Count |
| --- | ---: |
| Physical source records | 2 |
| Printed source slots | 401 |
| Modeled coordinates | 402 |
| Plaintext positions | 201 |
| Fixed raw labels under the stated frames | 192 |
| Fixed edited labels | 200 |
| Observed-coordinate substitutions | 5 |
| Printed-mask fills | 7 |
| Inserted-coordinate fills | 1 |

## Credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The [earlier unreviewed candidates](../../experiments/staatsbank_accounting_cheques/prior_candidates.json) and [original OCR snapshot](../../experiments/staatsbank_accounting_cheques/ocr_snapshot.json) retain their attribution separately. Verification reconstructs the source-to-model mapping, replays all five local insertion choices, prices every edit and fill, and checks all plaintext domains and readable labels. Complete candidates and an injective completion witness for the partial second part re-encrypt exactly; the witness assigns no historical digit value.

```sh
python experiments/staatsbank_accounting_cheques/verify.py --verify
python experiments/staatsbank_accounting_cheques/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Optional PDF verification checks the original scan digest and exact source-crop pixels. No chronological or monetary claim is established merely by a numerical-looking decoded label.

**Later copy evidence.** The [p172 D2 / p175 B2 reconciliation](../../experiments/accounting_copy_reconciliation/README.md)
compares the two native second parts without changing this edition. They
agree at 185 of 190 jointly observed source coordinates and have disjoint
masks. This supplies two previously unknown labels to the conservative
p175 reading; the final X remains a separately priced change in that copy.
Neither complete source pair supports the proposed M in MARK or L in
HAUPTWECHSELAMT, and the unresolved AM label remains VF in `{5, 6}`.
