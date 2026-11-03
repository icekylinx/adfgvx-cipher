# Demobilization at Neuhof, south of Fulda

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

The opening of this three-part telegram directs a Flak unit, whose number
remains unresolved, toward demobilization at **Neuhof, south of Fulda**.
The middle part supports a conditional opening identifying the Hanau-Fulda
line. The final part explicitly repeats that the relevant field-army
items are to be sent to Neuhof. Most of the badly damaged middle part
still has no proposed coherent original-language reading.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed p228, PDF p231](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [preserved section](../../experiments/neuhof_demobilization/sources/p228_B.png)
appears under `30th NOVEMBER, 1918.` with the header:

```text
B) ZON v BSL (01.33 a.m., December 1st)
NO 152 1512 3 TLE
```

All three parts use the unchanged published `Nov28-Dec1` square and ranks.
Raw `Y` separators, numeral labels and rare letters remain as recorded.
No optional late-key relabelling is applied.

## B1: the destination instruction

The first part advertises `RICHI-246` and has exactly **246 slots**, including
six printed dashes. Its earlier OCR stream had 241 coordinates and did not
produce a coherent reading. The visual transcription gives:

```text
0OKXXYYZUMERLYVJXYXXZX4NRP680YX4GEHYAY3YANLGYXLF?YNRYX4SPALTE9FLAKABTEILUNG?0WIRDNI?L3NDARMJT?DTSONDERNINYNEU?OFYSUEDHFUL?A
```

Five observed-coordinate substitutions and five fills of printed dashes give:

```text
AOKXXYYZUMERLYVJXYXXZX4NRP680YX4GEHYAY3YANLGYXLFDYNRYX4SPALTE9FLAKABTEILUNG?0WIRDNICHINDARMSTADTSONDERNINYNEUHOFYSUEDLFULDA
```

The ordinary body names a Flak unit and places its destination at Neuhof,
south of Fulda, with Darmstadt appearing in the negative part of the
instruction. It retains the shortened `NICHIN`: the expected German phrase
would normally contain `NICHT IN`, but no `T` is inserted into the fixed
source frame. The Flak unit field remains `?0`. Its number, the order
number, date-like fields and column-reference label remain uninterpreted.

The body continues into the middle part with the demobilization wording.

## B2: a limited opening, followed by an unread remainder

The second part advertises `RICHI-264` and has **264 slots**, including
**43 printed dashes**. Its direct label reading is:

```text
A?ST??CKE?ANK?FUL?AD1?OBI?G5D??HT?I1??CHA?LL??UJD5S1??Y26U03??GEHX0Z??MBEDES??DESIT7???YYADA???MX8A8???OBPL2???ENREN???CKS?R???I4CEH
```

The proposed original-language span is limited to **positions 0-32**:

```text
ANSTRECKEHANAUFULDADEMOBILGEMACHT
```

It says “demobilized on the Hanau-Fulda line.” This is a conditional
editorial reconstruction requiring **five observed-coordinate changes and
ten erasure fills**. It joins the preceding location instruction coherently,
but its exact wording is not independently witnessed. All changes are
confined to these 33 plaintext positions.

The remaining **99 positions** retain their source-derived labels and
domains for later work. No original wording is proposed for that remainder,
and the label count below does not turn it into a recovered body.

## B3: routing to Neuhof

The source heading is literally **`RICHI-196?`**. Counting the received
groups gives **186 slots**, including one printed dash. The edition uses
that actual 186-slot frame and preserves the questioned header length.
It does not insert ten hypothetical coordinates. Its direct reading is:

```text
DESFELDHEERESSINDDAHERNICHTNACHDAR?SADTSONDERNNACHNEUHOFZULEITENYCMTRUPPENDEPY3025YXXYX4YAY3Y
```

Filling the one printed dash at source index **15**, group **4**, coordinate
**1**, with `X` gives:

```text
DESFELDHEERESSINDDAHERNICHTNACHDARMSADTSONDERNNACHNEUHOFZULEITENYCMTRUPPENDEPY3025YXXYX4YAY3Y
```

The final instruction says the relevant field-army items must therefore
be directed to Neuhof. The preceding plural subject lies in the unread
middle portion, so the edition does not invent a specific unit or equipment
category. The city string remains `DARMSADT`, without an added `T`.
The office label `CMTRUPPENDEP` and its numerical reference remain literal.

## Exact source accounting

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
