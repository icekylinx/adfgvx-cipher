# November 1 contact times, service mail and receipt acknowledgment

Prepared by **icekylinx and GPT-6 Astra Pro**. These four physical records
appear on Childs printed p99, under the November 1 heading. They use the
published `Nov1-3` square and column ranks. The accompanying
[Sava-crossing report](../military/sava_crossing_evening_report.md) is a · [Reading conventions](../../docs/reading-conventions.md)
separate message on the same page.

The [full page](../../experiments/nov1_contact_mail_and_sava/sources/p99_full.png),
[literal source rows](../../experiments/nov1_contact_mail_and_sava/inputs.json)
and [coordinate certificate](../../experiments/nov1_contact_mail_and_sava/certificates.json)
retain the distinction between printed masks, observed coordinates, and
conditional missing coordinates.

## p99 A: requested contact times and a damaged Ringbahn phrase

The header reads `UKS v ZON`, reception `0.48 a.m., November 2nd`, origin
`1825 (1)`, and `RIZI-133`. The
[A crop](../../experiments/nov1_contact_mail_and_sava/sources/p99_A.png)
contains exactly **133 source slots**: 109 valid coordinates, 22 printed
dashes, and two printed `E` glyphs at source indices 38 and 40. The final
printed group is the three-letter `GAD`. The odd count is not silently
changed in the transcription.

A bounded diagnostic examined one-coordinate insertion and deletion in
either the transmitted stream or the fractionated stream. Its 534 completed
configurations are retained in the [search log](../../experiments/nov1_contact_mail_and_sava/search/one_coordinate_screen.json).
Adding one coordinate at the end of the transmitted stream gives a coherent
partial body. This is an explicit **134-slot conditional frame**, retaining
all 133 source slots. The literal 133-slot output and its unpaired coordinate
remain in the certificate.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 134-slot frame, with one appended unknown coordinate**

```text
??BITTE?V??SCHLA?FU??V?RKE?R??EITEN?WI??E?RIN?B?HNZEI??NX?KONA?H?L?
```

**Edited output — same conditional frame; no observed-coordinate substitutions**

```text
ERBITTENVORSCHLAGFUERVERKEHRSZEITENXWI??E?RINGBAHNZEITENXAKONACHELF
```

</details>

The edited layer has **64/67 fixed positions**. It fills 21 source masks
(20 dashes and the `E` at source 38) and the one missing coordinate. The
`E` at source 40 and dashes at 18 and 26 remain unresolved. It changes no
observed coordinate. The three question marks in `WI??E?` are three distinct
unknown positions, not punctuation.

**Readable German — from the conditional edited layer**

> Erbitten Vorschlag fuer Verkehrszeiten. `WI??E?` Ringbahnzeiten. Akonach Elf.

The readable content requests a proposal for communication times, then
contains an unresolved phrase before *Ringbahnzeiten*. `AKONACHELF` is
retained without expanding or identifying its abbreviated office. The
[November 3 notice](nov3_ringbahn_notice.md) and
[radio schedule](../../experiments/nov3_radio_and_pioneer/inputs.json)
independently contain the literal term `RINGBAHN`; this supports reading it
as a radio-service term here. It does not determine the missing phrase or
the location of the proposed loss.

**Conditional interpretation — an additional word repair, outside the primary edition**

```text
ERBITTENVORSCHLAGFUERVERKEHRSZEITENXWIEDERRINGBAHNZEITENXAKONACHELF
```

`WIEDER` would make the phrase “Wieder Ringbahnzeiten.” It requires three
additional observed-coordinate substitutions, at source 103 `D`→`A`,
110 `V`→`G`, and 124 `G`→`D`, plus three additional source-mask fills.
Its total cost is **3 substitutions, 24 source-mask fills and 1 missing-coordinate
fill**. This plausible word is not established by the neighboring notices;
the primary edition keeps `WI??E?`.

A separate fixed-template comparison evaluated every one of the 134 possible
transmitted-coordinate insertion boundaries. **132 and 133 are equally
minimum at zero observed substitutions** and produce the same edited stream.
They have different source-origin maps. Appending is the displayed convention,
not a uniquely established historical loss position. The template was assembled
after the initial diagnostic, so this is a consistency check, not a blind
recovery or an independently calibrated language-model result.

## p99 C1: service mail routed through Gleiwitz

C has header `UKS v ZON`, reception `11.35 p.m., November 1st`, origin
`2000 (1) AN LP 2 TLE`. Its first part is `1 TL RICHI-136`. The
[C crop](../../experiments/nov1_contact_mail_and_sava/sources/p99_C.png)
shows 136 slots, including 14 dashes. Its last line contains the visible
three-coordinate group `AAA` after two dashes. Those three `A` characters
are retained as observed coordinates.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 136-slot frame**

```text
OXH9L?OPXDIEDS?POSTXFUOR?AXOXKX?L?XNACHGA???SONKOM???DOXGLEI???ZXOXS
```

**Edited output — 3 observed substitutions and 14 source-mask fills**

```text
OXHXLXOPXDIENSTPOSTXFUERXAXOXKXELFXNACHGARNISONKOMMANDOXGLEIWITZXOXS
```

</details>

**Readable German — from the edited layer**

> O.H.L. Op. Dienstpost fuer A.O.K. Elf nach Garnisonkommando Gleiwitz O.S.

The candidate sends service mail for `A.O.K. ELF` to the garrison command
at Gleiwitz `O.S.`. It becomes 68/68 fixed after explicitly changing source
122–124 from `AAA` to `DGV` and filling the 14 dashes. Those substitutions
change raw label 3 `9`→`X`, label 12 `D`→`N`, and label 22 `O`→`E`.
The `9` lies inside the damaged `O.H.L.` sequence; this local repair does
not relabel the key or any historical numeric field. The completion of the
place and office names remains an editorial hypothesis constrained by the
observed coordinates, not a uniqueness claim.

## p99 C2: collection by aircraft

The same C header identifies the second part, `2 TL RICHI-102`. Its 102
source slots begin with five printed dashes. The 97 valid coordinates are
unchanged in both layers.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 102-slot frame**

```text
DORTA?HOLUNGDUR?HFLUGZEU?XAXOXKXEL?XRMXLXDX?RX7011X
```

**Edited output — 5 source-mask fills, no observed substitutions**

```text
DORTABHOLUNGDURCHFLUGZEUGXAXOXKXELFXRMXLXDXNRX7011X
```

</details>

**Readable German — from the edited layer**

> Dort Abholung durch Flugzeug. A.O.K. Elf. RM L D Nr. 7011.

The continuation requests collection there by aircraft. Reference `7011`
is literal and unchanged. `RM L D` remains an unexplained abbreviated
sequence. The five source-mask fills are at source 0–4, with values `VDFAG`.
The native source and shared header support the two-part association; no
missing third part is invented from the earlier OCR header error.

## p99 D: acknowledgment of an OHL message

D has header `UKS v ZON`, an unspecified reception time on November 1,
origin `2015 (1) AN LP`, and `RICHI-100`. The
[D crop](../../experiments/nov1_contact_mail_and_sava/sources/p99_D.png)
contains 100 valid coordinates. The final group is `VXFGD`.

<details>
<summary>Raw decoded text</summary>

**Raw output — unchanged native 100-slot frame**

```text
ANXOXHXLXXEINSXAXNRX11127XGAHXOPXERHALTENXEXOXKX11
```

</details>

**Readable German — from the unchanged raw layer**

> An O.H.L. Eins A Nr. 11127 GAH Op. erhalten. E.O.K. 11.

This acknowledges receipt of the cited message. All 50 plaintext positions
are fixed without edits. `11127`, `11`, `GAH`, and the unusual closing
`E.O.K.` remain literal; no cleaner headquarters abbreviation is substituted.
The earlier OCR-derived candidate already had this body with one unresolved
label. The source check fixes that reading without a historical transmission
repair and retains the earlier candidate in the provenance record.

## Evidence, limits and reproduction

The published key retains the credit of **George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker**. The current source and arithmetic review is by
**icekylinx and GPT-6 Astra Pro**. This package makes no first historical
body-reading claim. Its [prior-evidence record](../../experiments/nov1_contact_mail_and_sava/prior_evidence.json)
retains the earlier unreviewed OCR outputs and explains their missing rows.
The separate [p100 challenge](../p100.md) keeps Armin's earlier body credit.

The [experiment README](../../experiments/nov1_contact_mail_and_sava/README.md)
gives the standard-library verifier, optional source-pixel verification,
exact model-binding check and the distinction between the primary edition
and the optional `WIEDER` hypothesis. Every readable passage is checked
character by character against all non-`X` labels in its cited stream,
including the three retained unknowns in A.
