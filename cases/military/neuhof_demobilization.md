# Demobilization at Neuhof, south of Fulda

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

The opening of this three-part telegram directs a Flak unit, whose number
remains unresolved, toward demobilization at **Neuhof, south of Fulda**.
The middle part now supports a conditional continuation naming the Hanau–Fulda
line, enclosures 1 and 2, and formations undergoing demobilization within a
deputy command's district. The final part explicitly directs the relevant
field-army items to Neuhof.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed p228, PDF p231](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [preserved section](../../experiments/neuhof_demobilization/sources/p228_B.png)
appears under `30th NOVEMBER, 1918.` with the header:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
B) ZON v BSL (01.33 a.m., December 1st)
NO 152 1512 3 TLE
```

</details>

All three parts use the unchanged published `Nov28-Dec1` square and ranks.
The source edition retains raw `Y` separators, numeral labels and rare
letters. The separate shared interpretation below supplies part of B1's
numerical fields.

## B1: the destination instruction

The first part advertises `RICHI-246` and has exactly **246 slots**, including
six printed dashes. Its earlier OCR stream had 241 coordinates and did not
produce a coherent reading. The visual transcription gives:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
0OKXXYYZUMERLYVJXYXXZX4NRP680YX4GEHYAY3YANLGYXLF?YNRYX4SPALTE9FLAKABTEILUNG?0WIRDNI?L3NDARMJT?DTSONDERNINYNEU?OFYSUEDHFUL?A
```

</details>

Five observed-coordinate substitutions and five fills of printed dashes give:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
AOKXXYYZUMERLYVJXYXXZX4NRP680YX4GEHYAY3YANLGYXLFDYNRYX4SPALTE9FLAKABTEILUNG?0WIRDNICHINDARMSTADTSONDERNINYNEUHOFYSUEDLFULDA
```

</details>

The ordinary body names a Flak unit and places its destination at Neuhof,
south of Fulda, with Darmstadt appearing in the negative part of the
instruction. It retains the shortened `NICHIN`: the expected German phrase
would normally contain `NICHT IN`, but no `T` is inserted into the fixed
source frame. The Flak unit field remains `?0`. Its number, the order
number, date-like fields and column-reference label remain uninterpreted.

The [joint calendar and unit interpretation](../../experiments/late_november_calendar_and_units/README.md)
adds `GA=0` and `VG=7`, fixing three more numeral positions without additional
source changes:

| Field | Published-key labels | Joint interpretation |
|---|---|---|
| Order reference | `P680` | **P067** |
| Flak unit field | `?0` | **?7** |

This interpreted layer fixes **120/123 positions**. The leading unit character
remains an erasure, and two other fields retain the shared `4/5` ambiguity.
The body continues into the middle part with the demobilization wording.

## B2: the demobilization continuation

The [current B2 edition](p228_demobilization_fragment.md) reaches **125/132
positions** through a conditional relocation of five printed mask slots,
word proposals and two shared-reference transfers from B1. It preserves all
221 observed coordinates in their original relative order. Five observed
substitutions and 36 mask fills support the combined reading; seven positions,
including the command field and the prefix before `CKFORMATIONEN`, remain
unresolved.

<details>
<summary>Earlier native-frame opening</summary>

The second part advertises `RICHI-264` and has **264 slots**, including
**43 printed dashes**. Its direct label reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
A?ST??CKE?ANK?FUL?AD1?OBI?G5D??HT?I1??CHA?LL??UJD5S1??Y26U03??GEHX0Z??MBEDES??DESIT7???YYADA???MX8A8???OBPL2???ENREN???CKS?R???I4CEH
```

</details>

The proposed original-language span is limited to **positions 0-32**:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — partial proposed span only; positions 0–32:**

```text
ANSTRECKEHANAUFULDADEMOBILGEMACHT
```

</details>

It says “demobilized on the Hanau-Fulda line.” This is a conditional
editorial reconstruction requiring **five observed-coordinate changes and
ten erasure fills**. It joins the preceding location instruction coherently,
but its exact wording is not independently witnessed. All changes are
confined to these 33 plaintext positions.

The remaining **99 positions** retain their source-derived labels and
domains for later work. No original wording is proposed for that remainder,
and the label count below does not turn it into a recovered body.

</details>

## B3: routing to Neuhof

The source heading is literally **`RICHI-196?`**. Counting the received
groups gives **186 slots**, including one printed dash. The edition uses
that actual 186-slot frame and preserves the questioned header length.
It does not insert ten hypothetical coordinates. Its direct reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DESFELDHEERESSINDDAHERNICHTNACHDAR?SADTSONDERNNACHNEUHOFZULEITENYCMTRUPPENDEPY3025YXXYX4YAY3Y
```

</details>

Filling the one printed dash at source index **15**, group **4**, coordinate
**1**, with `X` gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
DESFELDHEERESSINDDAHERNICHTNACHDARMSADTSONDERNNACHNEUHOFZULEITENYCMTRUPPENDEPY3025YXXYX4YAY3Y
```

</details>

The final instruction says the relevant field-army items must therefore
be directed to Neuhof. The preceding plural subject lies in the unread
middle portion, so the edition does not invent a specific unit or equipment
category. The city string remains `DARMSADT`, without an added `T`.
The office label `CMTRUPPENDEP` and its numerical reference remain literal.

## Source accounting for the native-frame edition

| Part | Actual slots | Printed dashes | Raw fixed labels | Edition fixed labels | Known-coordinate changes | Erasure fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | 246 | 6 | 117 / 123 | 122 / 123 | 5 | 5 |
| B2 | 264 | 43 | 89 / 132 | 99 / 132 | 5 | 10 |
| B3 | 186 | 1 | 92 / 93 | 93 / 93 | 0 | 1 |
| **Total** | **696** | **50** | **298 / 348** | **314 / 348** | **10** | **16** |

There are **no insertions, deletions, block moves or changes to the period
key**. The 314 fixed labels include untouched, uninterpreted values in B2's
unread remainder. The [certificate](../../experiments/neuhof_demobilization/certificates.json)
lists every repair, its source and plaintext positions, and every numeral
or `J/Q/Y` occurrence, including those changed by explicitly priced
ordinary-word repairs. This is not a silent numerical substitution.

The [inputs](../../experiments/neuhof_demobilization/inputs.json) preserve all
manual rows, headers, image hashes and the limited middle-part template.
Globally consistent source-fill witnesses prove arithmetic consistency of
the partial readings. Their arbitrary erased-coordinate values are
explicitly marked as nonhistorical witnesses.

The published key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
B3 had already appeared as an unreviewed OCR-derived candidate. The present
work adds the exact source edition, the readable opening instruction and
the separately limited middle proposal. No explicit p228 B example was
located in the bounded author-paper, supplementary-reading and catalog
check; no universal first-decipherment claim is made.

```sh
python experiments/neuhof_demobilization/verify.py --verify
```
