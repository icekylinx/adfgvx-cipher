# Meal allowances, communal provisioning and a refused supplement

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source:** J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
printed p129 B1, p133 A2–A3 and p134 A4; PDF pp132, 136 and 137.
**Edition:** icekylinx and GPT-6 Astra Pro.

These four numbered parts form one message. The repeated receipt header
is `NKJ FUER COS v LP (7.18 a.m., November 6th)`, and the origin line is
`2400 (5/11) 4 TEILE`. The pages carry the heading 5 November 1918 and
explicit continuation annotations. The matching headers and numbers
provide the cross-page link despite the intervening pages of other
traffic.

The message disputes high cash meal allowances, requires rates to be
reduced, promotes communal purchasing and provision of food in kind,
and refuses an application for a cost-of-living supplement. It supplies
no actual allowance rate. The [experiment](../../experiments/military_allowances/README.md)
contains every source crop, coordinate and candidate edit.

## p129 B1

The source advertises and prints **398 slots**, including a dash in
`XVFX-` and an invalid `C` in `CFGVV`. Their raw 199-position reading is:

```text
?UXMXRMX30NRX228XFUERSELBSTVERPFLEGERDORTFESTGESETETEBEKOESTBGUNGSGELDERSINUZUHOCHUNDMUESSENAUCHFUERRUECKLIEGENDEZEITBEANSTANDETWERDENXSCHWEDISCHEGEVUE?RNISSEKOENNENNICHTALSSASSGEBENDANGESEHENWERDENX
```

The ordinary-word candidate is:

```text
ZUXMXRMX30NRX228XFUERSELBSTVERPFLEGERDORTFESTGESETZTEBEKOESTIGUNGSGELDERSINDZUHOCHUNDMUESSENAUCHFUERRUECKLIEGENDEZEITBEANSTANDETWERDENXSCHWEDISCHEGEBUEHRNISSEKOENNENNICHTALSMASSGEBENDANGESEHENWERDENX
```

It requires **five observed-coordinate substitutions and two printed
erasure fills**. The initial reference remains unexpanded. With
editorial spacing, the substantive passage reads:

> Für Selbstverpfleger dort festgesetzte Beköstigungsgelder sind zu hoch und müssen auch für rückliegende Zeit beanstandet werden. Schwedische Gebührnisse können nicht als maßgebend angesehen werden.

This does not identify any particular Swedish schedule or numerical rate.

## p133 A2

The source advertises and prints **452 slots**. The opening `VXDVV` group
is five characters, and the last group of the seventh row is the literal
`VAXGL`, with an invalid final `L`. The raw text is:

```text
HOHESELBSTBEKOESTIGUNGSGELDERBILDENDAUERNDERANREIZSICHDERALSREGELGEDACHTENNATURALVERPFLEGUNGZUENTZIEHENXHERABSETZ?NGDAHERDNBEDINGTERFORDERLICHXBEINEUFESTSETZUNGSINDDIEFUEREINEFELDKOSTPORTIONAUFZUWENDENDENPREISEZUGRUNDEZDLEGENX
```

The candidate costs **four observed-coordinate substitutions and one
printed-glyph fill**:

```text
HOHESELBSTBEKOESTIGUNGSGELDERBILDENDAUERNDENANREIZSICHDERALSREGELGEDACHTENNATURALVERPFLEGUNGZUENTZIEHENXHERABSETZUNGDAHERUNBEDINGTERFORDERLICHXBEINEUFESTSETZUNGSINDDIEFUEREINEFELDKOSTPORTIONAUFZUWENDENDENPREISEZUGRUNDEZULEGENX
```

With editorial spacing:

> Hohe Selbstbeköstigungsgelder bilden dauernden Anreiz, sich der als Regel gedachten Naturalverpflegung zu entziehen. Herabsetzung daher unbedingt erforderlich. Bei Neufestsetzung sind die für eine Feldkostportion aufzuwendenden Preise zugrunde zu legen.

`BEI NEUFESTSETZUNG` is already present in the source-aligned raw reading;
it is not an added editorial phrase.

## p133 A3

This part is advertised as **486 coordinates**, and the literal source
contains exactly 486. Earlier OCR made the first group `VAGAG` seven
slots and omitted the complete final `GXFVD A`, leaving an incorrect
482-slot stream. Correcting the transcription produces the following
**243-letter direct reading**:

```text
NATURALVERPFLEGUNGMUSSREGELBILDENXDIESEDURCHGEMEINSAMENEINKAUFXUMPREISENICHTUNNOETIGINHOEHEZUTREIBENUNDDURCHEINRICHTUNGDEUTSCHERSPEISEHAEUSERNACHMOEGLICHKEITFOERDERNSODASSSELBSTVERPFLEGUNGAUFTATSAECHLICHNICHTZUUMGEHENDEFAELLEBESCHRAENKTBLEIBTX
```

Every plaintext pair is complete. **No source coordinate is changed or
filled.** The text encrypts back exactly to the observed source using
the unchanged Nov4–6 key.

With editorial spacing:

> Naturalverpflegung muss Regel bilden. Diese durch gemeinsamen Einkauf, um Preise nicht unnötig in Höhe zu treiben, und durch Einrichtung deutscher Speisehäuser nach Möglichkeit fördern, sodass Selbstverpflegung auf tatsächlich nicht zu umgehende Fälle beschränkt bleibt.

The passage calls for communal purchasing to avoid unnecessary price
increases and for German dining facilities to reduce reliance on cash
self-provisioning. It does not state that such facilities had already
been established.

## p134 A4

The source advertises and prints **424 valid coordinates**. Its raw
212-character text is:

```text
BALDIGEMITTEILUNGDESDORTSEITSVERANLASSTENERBETEN0BEANTRAGTETEUERUNGSZULAGEKANNNICHTGEWAEHRTWERDENXZULAGEREGELUNGMUSSNACHPASCHEXRMX2XVORSCHRIFTERFOLGENXKRIEGSMINISTERIUMARMEEVERWALTUNGSDEPARTEMENTXNRX1235X18XGXBX1
```

The candidate changes only the raw `0` after `ERBETEN` to `X`, costing
**one coordinate substitution**. The substantive reading is:

> Baldige Mitteilung des dortseits Veranlassten erbeten. Beantragte Teuerungszulage kann nicht gewährt werden. Zulageregelung muss nach PASCHE X RM X 2 Vorschrift erfolgen. Kriegsministerium, Armeeverwaltungsdepartement …

The `PASCHE X RM X 2` wording and full closing
`NR X 1235 X 18 X G X B X 1` are retained as received. No unverified title,
author, edition or regulation is supplied for `PASCHE`. The `0→X` repair
does not imply a global relabeling of zero elsewhere.

## Attribution, counts and verification

The period key is previously published. Parts one, two and four also
predate this edition as readable unreviewed repository candidates.
Part three was unreadable under its earlier OCR frame; the old outputs
are frozen alongside the corrected source edition. The contribution
here is complete source assembly, recovery of that direct reading and
reversible candidate repairs. The bounded paper, dissertation and
comment-thread check does not establish historical decipherment priority.

The four records contain **1,760 printed source slots**, of which
**1,757** are valid ADFGVX coordinates. They yield **880 plaintext
positions**: 877 fixed in the raw models and all 880 in the explicit
candidates. Total cost is **10 observed substitutions and three printed
erasure fills**, with no key, rank or length changes. These counts describe
the edition's coverage, not the number of newly solved key symbols.

```bash
python experiments/military_allowances/verify.py --verify
python experiments/military_allowances/verify.py --verify --pdf /path/to/childs.pdf
```
