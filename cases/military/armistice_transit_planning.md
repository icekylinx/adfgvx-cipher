# Armistice transit and withdrawal planning

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

A six-part report on Childs pp125-126 discusses reported armistice conditions
for Austria-Hungary and their effect on German troop movements. It says
that the terms learned from Hungarian newspapers allow only fifteen days'
transit, describes plans for the **11th Army**, and urgently requests the
actual agreement. Five parts are readable in their ordinary cipher frames.
Part five has an odd 267-slot source and a useful, explicitly conditional
recovery of its latter half. A separate adjacent receipt note is included
as a seventh source record.

## Source and headers

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed pp125-126, PDF pp128-129](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
Both [p125](../../experiments/armistice_transit_planning/sources/childs_p125_full.png)
and [p126](../../experiments/armistice_transit_planning/sources/childs_p126_full.png)
are preserved. The page heading is `4th NOVEMBER, 1918.`, and the report's
repeated header reads:

```text
A) --- v NKJ (6.52 p.m., November 5th)
2345 (4/11) AN LP 6 TLE
```

Parts 1-4 occur on p125 and parts 5-6 continue on p126. The missing addressee
in the reception line is retained as `---`; `AN LP` remains in the origin
line. No date, callsign, reference or numerical label is silently normalized.
The complete published `Nov4-6` square and 17-column rank order are unchanged.

## A1-A3: transit rights and the 11th Army

The [first part](../../experiments/armistice_transit_planning/sources/childs_p125_A1.png)
has exactly 244 valid coordinates and reads without repair:

```text
OXHXLXOPXXNACHSOEBENHIERAUSUNGARISCHENZEITUNGENBEKANNTWERDENDENWAFFENSTILLSTANDSBEDINGUNGENFUEROESTUNGXISTDEUTSCHENTRUPPEN
```

The [second part](../../experiments/armistice_transit_planning/sources/childs_p125_A2.png)
has 238 valid coordinates. Its raw `FUENFXEHN` is repaired to `FUENFZEHN`
by one coordinate substitution:

```text
NURFUENFZEHNTAEGIGESDURCHZUGSRECHTZUGESTANDENXXOXKXMXHATTEBEABSICHTIGTX11XARMEEZUNAECHSTANDONAUZUBELASSENXSIEDEMNAECHST
```

The [third part](../../experiments/armistice_transit_planning/sources/childs_p125_A3.png)
has 200 valid coordinates. One coordinate substitution changes the raw
`RGEUMT` to `RAEUMT`:

```text
FALLSBESATZUNGSHEERWALACHEIRAEUMTXALSSCHUTZRECHTERFLANKEZWISCHENTHEISSUNDGEBIRGEZURUECKGEHENZULASSEN
```

With spaces and ordinary punctuation, the three parts read:

> O.H.L. Op. Nach soeben hier aus ungarischen Zeitungen bekannt werdenden
> Waffenstillstandsbedingungen für Oest.-Ung. ist deutschen Truppen nur
> fünfzehntägiges Durchzugsrecht zugestanden. O.K.M. hatte beabsichtigt,
> 11. Armee zunächst an Donau zu belassen, sie demnächst, falls Besatzungsheer
> Walachei räumt, als Schutz rechter Flanke zwischen Theiss und Gebirge
> zurückgehen zu lassen.

The report says that German troops have only fifteen days' passage under
the conditions just learned from Hungarian newspapers. It describes an
intention to leave the 11th Army on the Danube initially and, if the occupation
army evacuates Wallachia, let it retreat between the Theiss and the mountains
to protect the right flank. This is the report's stated information and
plan; the edition does not independently verify the newspaper terms or
assert that the proposed movement occurred. The raw army label `11` is
preserved exactly.

## A4: Entente transport and occupation rights

The [fourth part](../../experiments/armistice_transit_planning/sources/childs_p125_A4.png)
has 212 slots. A printed noncoordinate `2`/Z-like glyph is one erasure. It
leaves only the `N` in `BEFOERDERUNG` unknown; filling that position gives:

```text
XDIEBESTIMMUNGXDASSENTENTERECHTZURBEFOERDERUNGIHRERTRUPPENASAEMTLICHENEISENBAHNENUNDRECHTDERBESETZUNGALLER
```

The clause describes a provision giving the Entente the right to transport
its troops on the railways and occupy strategic points. The source literally
has `TRUPPENASAEMTLICHEN`; interpreting its `A` as an abbreviation for *auf*
is an editorial expansion, not recovered `UF` coordinates. The sentence
continues into the damaged fifth part.

## A5: conditional recovery of the odd frame

The [fifth part](../../experiments/armistice_transit_planning/sources/childs_p126_A5.png)
is explicitly marked `RICHI-267` and contains exactly **267 slots**, including
two printed dashes. Its original untransposed coordinate stream is odd.
The direct paired reading is:

```text
STRATEGISCHWICHTIGENPU?K?HABENSOLLXWUERDEFUERDIEMIT1A11204GRMELDETEN3L4QL3LCZWFFQ7K7I7I4IQFNCIC9Z9J6WLNL6JQFCX94A2FYZ6KZL6JY94ALFWLFL
```

One final coordinate remains unpaired. The first portion is readable; the
latter portion becomes readable under the opposite pairing phase. This
motivates the following **conditional error model**: a coordinate was lost
from the fractionated intermediate stream before the sender transposed its
267 remaining coordinates.

Keeping the received frame and its ranks intact, insert one unknown at
interim index 136 after untransposition. The conditional raw reading is:

```text
STRATEGISCHWICHTIGENPU?K?HABENSOLLXWUERDEFUERDIEMIT1A11204GRMELDETEN?ONBESONDRERBEDEUTUNGSEINUNDMACHTENTSCHEIDDNGXOBABMKRSCHANGETRETRN
```

The two printed-dash fills, the inserted interim coordinate `F`, and four
observed-coordinate substitutions give this 134-character proposal:

```text
STRATEGISCHWICHTIGENPUNKTHABENSOLLXWUERDEFUERDIEMIT1A11204GEMELDETENVONBESONDRERBEDEUTUNGSEINUNDMACHTENTSCHEIDUNGXOBABMARSCHANGETRETEN
```

It continues the strategic-points clause, invokes the literal reference
`1A11204`, calls the matter of particular significance, and says that a
decision on beginning the march is needed. The grammar around
`FUERDIEMIT1A11204GEMELDETEN` is elliptical; no missing noun is invented.
`PUNKT` and `BESONDRER` also remain as encoded, without adding a plural ending
or an unencoded vowel.

To verify the source-shaped witness, fractionate this proposal, remove its
coordinate at interim index 136, and transpose the remaining 267 coordinates
with the original rank order. That reproduces the source after exactly
the four substitutions and two dash fills. The proposed interim coordinate
has no received source index; all actual received coordinates retain theirs.

The [finite geometry audit](../../experiments/armistice_transit_planning/geometry_audit.json)
preserves 1,070 evaluated candidates: all single insertions and deletions
at both the transmitted and interim stages. The two frozen language models
favor interim insertion positions 136 and 137. For the retrospectively
assembled proposed text, position 136 uniquely minimizes substitutions
among all 268 interim insertion positions. This is a conditional consistency
result. It does not prove the original omission's location or exclude other
multi-error mechanisms, and the recovered tail is not classified as a
direct reading of an ordinary even frame.

## A6: request for the actual agreement

The [sixth part](../../experiments/armistice_transit_planning/sources/childs_p126_A6.png)
returns to an ordinary 242-slot frame. Its raw reading is:

```text
WERDENSOLLXAEUSSERSTDRINGDXXUMANGABEDERTATSAECGLICHENVEREINBARUNGENUEBERWAFFENSTILLSTANDWIRDGEBET?NXXOXKXMX1BNOX11230OPXX
```

Two coordinate substitutions repair the single plaintext `G` in
`TATSAECGLICHEN` to `H`; a printed `T` erasure is filled to give the missing
`E` in `GEBETEN`. Readable wording, continuing A5:

> … werden soll, äußerst dringd. Um Angabe der tatsächlichen Vereinbarungen
> über Waffenstillstand wird gebeten. O.K.M. `1BNOX11230OPXX`

The report requests the actual armistice agreement because the decision
whether to begin the march is extremely urgent. `DRINGD` is retained as an
abbreviation. The footer's numerical and letter labels remain literal.

## B: separate receipt note

The [adjacent B record](../../experiments/armistice_transit_planning/sources/childs_p126_B.png)
is a separate 134-coordinate message, not a seventh part of A:

```text
B) LP v NKJ (6.28 p.m., November 5th)
1201 (4)
RICHI-134
```

All 67 raw positions are fixed. The literal reading is:

```text
OXHXL0XDRBHTUNGRM1XAX11118XOPGEH02XANGXORHALTENXOXK0M0RM1A011232XOP
```

Two observed-coordinate substitutions give `DRAHTUNG` and `ERHALTEN`:

```text
OXHXL0XDRAHTUNGRM1XAX11118XOPGEH02XANGXERHALTENXOXK0M0RM1A011232XOP
```

It is a receipt notification with reference labels including `11118` and
`11232`. All `0`, `1`, other numeral labels and the `RM` strings are retained;
the edition does not turn them into a reconstructed historical numbering
system or infer that B acknowledges the six-part report.

## Exact costs and provenance

| Record | Source slots | Fixed positions | Observed-coordinate substitutions | Source-erasure fills | Other geometry |
| --- | ---: | ---: | ---: | ---: | --- |
| A1 | 244 | 122 / 122 | 0 | 0 | Ordinary |
| A2 | 238 | 119 / 119 | 1 | 0 | Ordinary |
| A3 | 200 | 100 / 100 | 1 | 0 | Ordinary |
| A4 | 212 | 105 / 106 | 0 | 1 | Ordinary |
| A5 | 267 | 131 / 134, conditional | 4 | 2 | One interim insertion before transposition |
| A6 | 242 | 120 / 121 | 2 | 1 | Ordinary |
| B | 134 | 67 / 67 | 2 | 0 | Ordinary |

The [inputs](../../experiments/armistice_transit_planning/inputs.json) preserve
the seven manual transcriptions, literal headers and nine source images.
The [certificate](../../experiments/armistice_transit_planning/certificates.json)
records every plaintext domain and coordinate origin, every change's printed
row/group/position, and the complete re-encrypted witnesses. All transmitted
lengths match the source. The total is 1,537 slots, ten valid-coordinate
substitutions, four source-erasure fills and one conditional interim insertion.
There are no changes to the published square or rank order.

The key is prior work by **George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also published in George Lasry's [2017-02-24 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR-derived candidates and selected retrieval strings
existed. The bounded author-paper audit found no explicit p125/p126 body
example; this edition makes no universal first-decipherment claim.

```sh
python experiments/armistice_transit_planning/verify.py --verify
python experiments/armistice_transit_planning/geometry_audit.py --verify
```

## Later receipt and clause witnesses

The [p137 B4 and C source editions](armistice_clause_witnesses.md) preserve
copies of p125 A4 and p126 B. B4 independently witnesses the previously
masked coordinate in `BEFOERDERUNG`; C reproduces the two corrupt words
in the receipt, so their existing repairs remain editorial. Neither copy
changes the conditional geometry or uncertainty of p126 A5.
