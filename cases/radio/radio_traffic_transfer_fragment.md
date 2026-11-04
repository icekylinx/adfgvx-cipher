# A radio-traffic transfer in a surviving second part

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A surviving second part reports that DNZW takes over radio traffic and gives further call-name and place-like fields. The source expressly marks the first part missing. The repeated location identifies Grosswardein. One additional coordinate correction completes its opening spelling; the second occurrence keeps GROSSVARDEIN. The date and SCHWERE field retain two coupled readings.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p226 excerpt](../../experiments/radio_traffic_transfer_fragment/sources/p226_reviewed.png) · [Inputs](../../experiments/radio_traffic_transfer_fragment/inputs.json) · [Position and change certificates](../../experiments/radio_traffic_transfer_fragment/certificates.json)

The published `Nov28-Dec1` key is unchanged. [Original OCR records](../../experiments/radio_traffic_transfer_fragment/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/radio_traffic_transfer_fragment/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

The earlier word edition has the following account; the place completion is
priced separately below.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p226 A2](#p226-a2) | 186 | 89 / 93 | 1 | 3 |

## p226 A2

**Source transcription — header:** `A) BSL v UKS (10.27 p.m., November 30th); 1700 (11/29); (1st Tl Missing); 2 TL RICHI-186`

### A date and station field that must be read together

The [shared late-November interpretation](../../experiments/late_november_calendar_and_units/README.md)
leaves only **4/5** interchangeable. The opening `?DEZ` has the pair `F?`;
if it denotes a December day, either surviving square requires the missing
coordinate at source position 23 to be `X`. This adds **one mask fill** to
the earlier edition, giving **1 observed substitution and 4 fills**, while
leaving the day unresolved. The adjacent `SCHWERE1?` field uses the other
4/5 cell. A separate station notice on [p230 C](nov30_radio_personnel.md#p230-c)
uses that same cell for its hour.

| Opening date, if calendrical | `SCHWERE` field | p230 C hour |
|---|---|---|
| **4 December** | **15** | **5** |
| **5 December** | **14** | **4** |

Both assignments survive. The November transmission and interception
dates do not choose between them. The first place field becomes
`GROSSW7RDEIN`, still damaged; the second remains `GROSSVARDEIN`.
[Exact coordinate and branch check](../../experiments/late_november_calendar_and_units/traffic_certificate.json).

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
?DEZGROSSW0RDEINYYDNZWUEBERNIMMTVERKAHRFUEROKMSCHWEREX9RUFZYNATANADOLFUR?UL?YINGRO?SVARDEINYY
```

**Edited output — 1 observed-coordinate substitution and 3 source-mask fills; no insertion, deletion or reordering:**

```text
?DEZGROSSW0RDEINYYDNZWUEBERNIMMTVERKEHRFUEROKMSCHWEREX9RUFZYNATANADOLFURSULAYINGROSSVARDEINYY
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> ?DEZ GROSSW0RDEIN. DNZW uebernimmt Verkehr fuer OKM SCHWEREX9 RUFZ: Natan Adolf Ursula in GROSSVARDEIN.

**Meaning:** The surviving second part states that DNZW takes over communications traffic for OKM, followed by the literal field SCHWEREX9 and RUFZ, then the proposed spoken-name sequence Natan Adolf Ursula and a place-like label. RUFZ may abbreviate Rufzeichen, or call sign. The missing first part and the exact identity of DNZW, the station and the location are not reconstructed.

**Editorial limits.**

- The source explicitly says the first part is missing. This is an edition of the complete native 186-slot second part, not a reconstruction of the missing first part.
- Four printed dashes remain occupied source positions. The earlier edition fills three in UR?UL? and GRO?SVARDEIN. The optional date interpretation above fills the fourth; its value remains 4/5 under the shared square.
- The only observed-coordinate word change is VERKAHR to VERKEHR. Natan Adolf Ursula is an explicit source-mask completion proposal, not an independently identified person or station.
- GROSSW0RDEIN keeps the numeral 0 and W in the first place-like field; GROSSVARDEIN keeps V in the second. Neither field is silently normalized to a modern or historical place name.
- Without the calendar interpretation, the opening shared-square domain is `{4, 5, D, I, J, N, U}`.
- Y is the separator label. X and 9 inside SCHWEREX9 remain literal; DNZW and RUFZ are not expanded in the exact readable quotation.

## The repeated place: Grosswardein

The opening `GROSSW0RDEIN` and closing `GROSSVARDEIN` identify the same
place with different V/W spellings. The second field's A is an unchanged
`VD` pair at source positions **57 and 149**. Applying that letter to the
opening field changes source **81 G→D**, turning its `VG` into `VD` and
giving **GROSSWARDEIN**. The original G is clearly printed: this is an
editorial repair, with no additional fill or key assignment.

The [3 August 1913 *Bácskaer Volkszeitung*, PDF p2](https://epa.oszk.hu/05600/05686/00377/pdf/EPA05686_bacskaer_volkszeitung_1913_031.pdf#page=2)
independently prints **Großwardein**. Its spelling supports the location;
the second cipher occurrence remains **Grossvardein** in the quotation.

**Conditional interpretation — readable German; the two calendar branches are paired in order:**

> {4/5}. Dez., Grosswardein. DNZW uebernimmt Verkehr fuer OKM, schwere {15/14}. Rufz.: Natan Adolf Ursula in Grossvardein.

The notice announces a transfer of radio traffic to DNZW at Grosswardein
and gives the spoken call-name sequence Natan Adolf Ursula. Reading the
opening as **4 December** gives **SCHWERE 15**; **5 December** gives
**SCHWERE 14**. Neither the place comparison nor the calendar selects
between them. The missing first part is still absent.

The complete proposal costs **two observed substitutions and four mask fills**:
VERKAHR→VERKEHR, the new place-letter repair, the three earlier word fills
and the earlier calendar fill. Both complete square branches re-encrypt
exactly; **91/93 positions** agree between them. Without the calendar
assumption, the place repair costs two substitutions and three fills in total,
with **92/93 baseline labels** fixed. This recovers a readable place word;
it does not increase the fixed-label count.

[Exact source comparison, retained branches and historical provenance](../../experiments/late_place_comparison/README.md).

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/radio_traffic_transfer_fragment/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
