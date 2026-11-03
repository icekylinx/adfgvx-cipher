# Military-intendant addresses and responsibilities

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

A four-part message distinguishes the work of the **Generalintendant in
Berlin** from that of the **Generalintendant at `GRHQU`**. It supplies a new
Berlin address on Augsburger Strasse, assigns organization, personnel and
administrative-finance questions to Berlin, and assigns supply transport,
delivery, clothing and related matters to the headquarters office. The
address number and several reference fields remain unresolved.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed p202, PDF p205](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
Its [preserved section image](../../experiments/military_intendant_remit/sources/p202_B.png)
has this header:

**Source transcription — clear header and/or literal source record:**

```text
B) NKJ v LP (4.00 p.m., November 16th)
FUER UKS 1200 (16) 4 TEILE SS GRHQU 14/11 FLUGPOST O K M
HERMANNSTADT (16)
```

The page heading is `16th NOVEMBER, 1918.`. The published `Nov16-18` key
is used unchanged, including all eight unassigned square cells.

## B1: new address and Berlin responsibilities

The first part advertises `RICHI-228` but contains only **223 valid
coordinates**. A 228-coordinate working frame with five consecutive missing
coordinates produces a clear body. The representative below puts that gap
before received index **145**, before printed group **30**. Its raw reading
is conditional on that placement:

**Raw output — conditional five-coordinate gap before source 145; representative placement:**

```text
NEUBADRESSEX?XGENERALI?TENDANTB?RLINAUGSB?RGERSTRX??XFUERKRIEGSGL?EDERUNGENPERSONALIENFUERREINEVERWALTUNG?SACHENIW
```

Four observed-coordinate substitutions and three fills of added slots give:

**Edited output — same representative gap model, with the stated substitutions and added-slot fills:**

```text
NEUEADRESSEX?XGENERALINTENDANTBERLINAUGSBURGERSTRX??XFUERKRIEGSGLIEDERUNGENPERSONALIENFUERREINEVERWALTUNGSSACHENIN
```

This announces a new address and names the Berlin Generalintendant on
Augsburger Strasse. The street number and the field before the office name
are not supplied. The duties begin with war organization, personnel, and
purely administrative matters; the sentence continues in B2.

The five added coordinates are `?DGD?` in this representative. The two
question marks remain unknown. Every one of the 223 received coordinates
remains in its original order, and the four observed-coordinate changes
are recorded separately from added-coordinate fills.

### Competing placements are retained

The [gap audit](../../experiments/military_intendant_remit/gap_audit.json)
enumerates all **224** places to insert five unknown coordinates. Using an
ordinary-word template with the address and reference fields masked gives
a minimum of two observed-coordinate changes at **142 and 143**. Including
the proposed address gives three changes at **143 and 144**. Among the
**46** printed-group boundaries or final end position, the full proposed
body has its minimum of four changes at **145**; the masked comparison
instead favors **140**.

The templates were constructed after reading the candidates. These are
conditional edit-cost comparisons, not independent plaintext evidence.
The earlier book and radio language scores both favored position **146**,
and their full score rows are retained. Because marginal scores can favor
unknown characters, that ranking does not establish the original geometry.
The edition therefore uses an explicit representative and makes no unique
loss-location or loss-mechanism claim. The ordinary-language body is much
better constrained than the number fields and the precise placement.

## B2: administrative, cash and levy matters

The second part contains exactly **220 slots**, agreeing with `RICHI-220`.
At received index 86 the source prints the non-coordinate letter `Q` in
`XQFDG`. A heavily overprinted final glyph in `GAAD?`, index 169, is also
left undecided. Both are masked before decryption. The raw body is:

**Raw output:**

```text
VERPFLEGUNGSANGELEGENHEIRENFUERGELDXKASSENXGEBUEHRNISANGELE?ENHEITENFUE?KONTRIBUTIONSGELDERUNDZWANGSAUFLAGENXX
```

One observed-coordinate change and two masked-slot fills give:

**Edited output:**

```text
VERPFLEGUNGSANGELEGENHEITENFUERGELDXKASSENXGEBUEHRNISANGELEGENHEITENFUERKONTRIBUTIONSGELDERUNDZWANGSAUFLAGENXX
```

Together with B1, this assigns Berlin administrative victualling matters,
money and treasury business, pay or allowance matters, contribution money
and compulsory levies. No numeral is inserted into the body.

## B3: the headquarters supply office

The third part contains exactly **210 valid coordinates**, agreeing with
`RICHI-210`. Its raw reading is:

**Raw output:**

```text
2XGENERALINTENDANTXGRHQUXALLENACHSCHUBANGELEGENHEITENSOWEITSIEMITTRANSPORT?NDHERANFUEHRUNNZUSAMMENHAENGEB
```

Four observed-coordinate substitutions give:

**Edited output:**

```text
2XGENERALINTENDANTXGRHQUXALLENACHSCHUBANGELEGENHEITENSOWEITSIEMITTRANSPORTUNDHERANFUEHRUNGZUSAMMENHAENGEN
```

The message assigns the Generalintendant at `GRHQU` all supply matters
insofar as they concern transport and delivery. The direct published-square
label `2` at the beginning is retained.

## B4: clothing, meat, sutlery and wartime services

The final part contains exactly **224 slots**, agreeing with `RICHI-224`.
Three coordinates are masked: a faded `C/G`-shaped glyph in `VDA?D`, a
faded glyph in `XAA?D`, and the printed non-coordinate `R` in `ARFXD`.
Enlarged crops preserve the visible appearances. The raw reading is:

**Raw output:**

```text
BEKL?IDUNGXUXA?SRUESTUNGFLEISCHVERSORGUNG?ARKETENDEREIWESENKRIEGSLEISTUNGENXGENERALIWTENDANTXRMX?XAX????XAX11X1?
```

One observed-coordinate change and three masked-slot fills give:

**Edited output:**

```text
BEKLEIDUNGXUXAUSRUESTUNGFLEISCHVERSORGUNGMARKETENDEREIWESENKRIEGSLEISTUNGENXGENERALINTENDANTXRMX?XAX????XAX11X1?
```

The list continues with clothing and equipment, meat provision,
*Marketendereiwesen* (sutlery), and wartime services or requisitions.
The literal `UX` abbreviation is retained. The signature says
`GENERALINTENDANT`; six positions in its reference remain unresolved.

## Exact costs and limits

| Part | Received slots | Working frame | Raw fixed positions | Edition fixed positions | Known-coordinate changes | Masked-slot fills | Added-slot fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | 223 | 228, conditional | 106 / 114 | 111 / 114 | 4 | 0 | 3 |
| B2 | 220 | 220 | 108 / 110 | 110 / 110 | 1 | 2 | 0 |
| B3 | 210 | 210 | 104 / 105 | 105 / 105 | 4 | 0 | 0 |
| B4 | 224 | 224 | 103 / 112 | 106 / 112 | 1 | 3 | 0 |
| **Total** | **877** | **882** | **421 / 441** | **432 / 441** | **10** | **5** | **3** |

The [inputs](../../experiments/military_intendant_remit/inputs.json) preserve
every manual row, ambiguous glyph, header and image hash. The
[certificates](../../experiments/military_intendant_remit/certificates.json)
map each plaintext position to both working-frame and original-source
coordinates, list all repairs and retain the complete unresolved domains.
There are no deletions, block moves or changes to the published square.
The two unknown inserted coordinates remain unknown.

Each partial reading has a globally consistent square/source completion
witness. Those witnesses choose arbitrary missing digits and coordinates
to demonstrate arithmetic consistency; they are explicitly **not proposed
original readings**. Repeated square cells couple the unresolved domains,
so their values cannot all be selected independently.

The period key is prior work by **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
B2 and B3 already appeared as unreviewed OCR-derived candidates in the
frozen p73 retrieval corpus. The present work supplies visual source
certification, the newly coherent opening and final-part bodies and their
explicit conditional models and costs. No explicit discussion of this
message was located in the bounded author-paper, supplementary-reading
and catalog check; this does not establish universal historical priority.

```sh
python experiments/military_intendant_remit/verify.py --verify
```
