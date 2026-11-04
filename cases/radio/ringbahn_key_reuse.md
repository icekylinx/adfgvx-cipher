# November Ringbahn keys and postponed December change

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

The edited first part says to retain the November Ringbahn key and postpone the December key. Its wording continues into the unedited second part: 1 December is to use the key as on the tenth of November, continuing through 21 December as on 30 November. These are literal instructions in the traffic; they do not independently recover the secret key material or verify that the instruction was followed.

Source: Childs, printed pp.160–161 (PDF pp.163–164). [Source images and inputs](../../experiments/nov8_radio_keys_and_reports/inputs.json), [certificates](../../experiments/nov8_radio_keys_and_reports/certificates.json), [method and limitations](../../experiments/nov8_radio_keys_and_reports/README.md). All indices below are zero-based.

## Conditional digit reading

The [shared Nov7–9 digit interpretation](../../experiments/nov7_9_joint_digits/README.md) gives **Nach Chef 4 B 49859** in part 2, at no additional source edit or fill. The opposite square gives 49869; the date schedule itself is unchanged.

## p160 C1

Header: `C) NKJ v LP (03.23 a.m., November 9th); FUER RAT 2000 (8/11) 2 TLE; 1 TL; RICHI-308`.

Literal 309 versus advertised 308. FAGVGD is a six-character group at 280–285; the primary conditional frame excludes 281. Source dashes 304/305 remain separately priced fills.

The source has **309 slots** (307 valid coordinates). The conditional model has 308 slots / 154 plaintext positions: 152 fixed raw, 154 fixed after the stated edits.

**Cost:** 4 observed-coordinate substitutions; 2 printed-mask fills; 1 observed-coordinate exclusion; 0 mask exclusions; no inserted coordinates.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — under the explicitly conditional exclusion frame:

```text
NOVEMBERXRINGBAHNSCHLVESSELNICHTVERN9CHTENXNACHXCHEFX4XBX48929XDEZEMBERXRINGBAFNSCHLUESSELTRITTVORLAEUFIGNIC?TINKRAFTX?AFUERSCHLUESSEL1XDEZEMBERWIEZEHNTER
```

**Edited output** — changes and source offsets are enumerated in the certificate:

```text
NOVEMBERXRINGBAHNSCHLUESSELNICHTVERNICHTENXNACHXCHEFX4XBX48929XDEZEMBERXRINGBAHNSCHLUESSELTRITTVORLAEUFIGNICHTINKRAFTXDAFUERSCHLUESSEL1XDEZEMBERWIEZEHNTER
```

</details>

**Readable German** — spacing, case, punctuation and conventional umlaut rendering only; all non-`X` labels match the edited output:

> November Ringbahnschlüssel nicht vernichten. Nach Chef 4 B 48929. Dezember Ringbahnschlüssel tritt vorläufig nicht in Kraft. Dafür Schlüssel 1. Dezember wie zehnter

## p160 C2

Header: `Same p160 C header; 2 TL; RICHI-144`.

Native 144. The cleartext footer NF NKJ v LP UM follows the cipher body and is not encrypted input. The date relationship continues the preceding ZEHNTER word without changing its letters.

The source has **144 slots** (144 valid coordinates). The native model has 144 slots / 72 plaintext positions: 71 fixed raw, 71 fixed after the stated edits.

**Cost:** 0 observed-coordinate substitutions; 0 printed-mask fills; 0 observed-coordinate exclusions; 0 mask exclusions; no inserted coordinates.

<details>
<summary>Raw decoded text</summary>

**Raw output** — native source frame:

```text
NOVEMBERUSWXBIS21XDEZEMBERWIE30XNOVEMBERXEMPFANGSBESTGXXNACHCHEF4B498?9X
```

</details>

**Readable German** — spacing, case, punctuation and conventional umlaut rendering only; all non-`X` labels match the edited output:

> November usw. bis 21. Dezember wie 30. November. Empfangsbestg. Nach Chef 4 B 498?9.

## Earlier related schedule edition

The [p211 lower-B schedule](p211_key_schedule.md) already records the same
November/December reuse instruction in three differently worded parts. Its
published key is `Nov4-6`; these p160 parts use `Nov7-9`. The source headings,
receipt dates, abbreviations, reference fields and written-versus-numeral day
forms differ. The [parallel certificate](../../experiments/nov8_radio_keys_and_reports/parallel_witnesses.json)
compares the named raw/edited plaintext layers and preserves those differences.
It makes no ciphertext-coordinate comparison across the two keys and does not
use the older fields to complete the new unresolved reference digit.

The p211 source assembly and readable edition retain their existing
**icekylinx and GPT-6 Astra Pro** attribution; the published keys retain their
original credits. These are two additional physical source parts, with no
claim to be the first identification of the key-use instruction.

## Shared uncertainty and credit

The two missing square cells `VF` and `XA` jointly contain `5` and `6`. Both complete assignments are retained as compatibility witnesses; every occurrence of a cell shares the same digit. The displayed `?` positions therefore must not be treated as independent digit choices. In p160 B2 one additional source coordinate remains unfilled; its domain can include letters as well as digits.

The published Nov7–9 period key and earlier OCR candidates are credited in the inputs. This edition adds source inspection, separate repair costs and exact readable-text mappings. It does not claim new recovery of the period key.
