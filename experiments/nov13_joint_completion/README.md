# Headquarters and award-class readings in the 13–15 November key

**Research and edition: icekylinx and GPT-6 Astra Pro.**

Two independent contextual constraints supply **XX=Q** and **VG=2** in the
published Nov13–15b partial square. Together they fix **six further labels
in five existing editions**, with **no new source edit**. The p193 award
notification reaches **37/37** positions within its earlier conditional
frame; the p188 supply request gains its headquarters abbreviation and a
two-day dispatch interval.

## The intendant's address

The native p188 C1 begins `GENERALINTENDANTFELDHEERESXGRXHX?U`. Its unknown
headquarters character is the fully observed **XX** pair, source positions
**53 and 171**. The native p202 B3, under the different Nov16–18 key,
directly reads `GENERALINTENDANTXGRHQU`; its Q requires no source repair.
Reading the p188 address as that headquarters therefore assigns **XX=Q**.

The two messages concern the same office, with a matching abbreviation.
They are not copies of one another, and the abbreviation identification is
the stated assumption. The resulting address is **Generalintendant
Feldheeres, Gr. H. Qu.**

## The award class

The p193 F core is `EK?XVERLIEHENXGLUECKWUNSCH`. If `EK` denotes the Iron
Cross and the following character its class, the candidates are **1 or 2**.
The unknown pair **VG** has the published label domain `234789QY`, while
**DD** carries label **1**. Excluding the first class additionally requires
retaining DD's **numerical value 1**; that value does not follow merely from
the published label. With that numeral interpretation and the stated
award-class identification, the sole compatible class is **2**.

The separate [p186 B1 troop-movement message](../../pages/186.md#edition-cases-military-oberost-troop-movement-obliterations-p186-b1)
has the native field `GENXVX10X11XISTANOBOSTGEDRAHTET`. Within its existing
conditional obliteration frame, all ten coordinates of `10X11` are
originally observed and unchanged:

| Plaintext index, zero-based | Published label | Native pair | Original source indices, zero-based |
| ---: | --- | --- | --- |
| 47 | 1 | DD | 150, 24 |
| 48 | 0 | DX | 63, 208 |
| 49 | X | DV | 83, 266 |
| 50 | 1 | DD | 170, 122 |
| 51 | 1 | DD | 305, 6 |

**If this field is a day/month date**, the two identical month digits must
denote **11**, the only valid repeated-digit month. This is independent
contextual support for numerical **DD=1**, obtained without either new
XX or VG assignment. The date reading remains a condition; it is not a
claim that arbitrary numeral labels have been historically identified.
Without retaining numerical DD=1, square injectivity alone says only that
DD and VG are different cells and does not exclude a first-class award.

The royal renewal decree of **5 August 1914**, reprinted in *Die Presse*
(Thorn), no. 184, **8 August 1914**, p1, establishes two classes and a
Grand Cross. It also specifies the distinction between the first and second
classes. The original newspaper pages were checked in the institutional
scan:

[Full issue](https://kpbc.umk.pl/Content/168740/KM_01427_1914_184.pdf)
· [Masthead](sources/die_presse_1914_title.png)
· [Decree and clause 1](sources/die_presse_1914_decree.png)
· [Class provisions](sources/die_presse_1914_classes.png).

That source establishes the award system. Identifying this telegram's
`EK` with the Iron Cross remains the local interpretation; neither the
recipient nor the opaque `JTN`, `KR` and `S R` is identified.

All four earlier p193 endpoint exclusions—source positions **0, 1, 73 and
74**—retain the same original VG pair at source positions **19 and 60**.
The class value therefore does not distinguish these source geometries.
The terminal-X representative reads:

**Conditional interpretation — existing 74-slot frame and word repair, with EK2:**

```text
JTNXKRXEK2XVERLIEHENXGLUECKWUNSCHXSXR
```

## Shared consequences

| Record | Before → after | Consequence |
| --- | ---: | --- |
| [p193 F](../../pages/193.md#edition-cases-people-nov13-conditional-congratulation) | 36 → **37/37** | **EK2 verliehen**, under the stated award interpretation |
| [p188 C1](../../pages/188.md#edition-cases-military-armistice-provisions-requests-c1-flour-and-oats-to-szolnok) | 130 → **132/134** | **GR H QU**; **alle 2 Tage** |
| [p179 D2](../../pages/179.md#edition-cases-military-armistice-and-leave-orders-d-discharge-delayed-and-urgent-home-leave-suspended) | 100 → **101/106** | Reference **RM1A11?2?** |
| [p197 A2](../../pages/197.md#edition-cases-radio-nov15-radio-personnel-and-key-notice-p197-a2) | 68 → **69/72** | Reference **2??6?5** |
| [p186 B1](../../pages/186.md#edition-cases-military-oberost-troop-movement-obliterations-p186-b1) | 152 → **153/154** | The opaque `?M` becomes `2M`; no ordinary word is recovered |

The p188 portion quantity remains `??0000`. Its four earlier observed
substitutions are unchanged. The p193 representative still costs one
observed exclusion and one substitution; the p186 obliteration model is
also retained. All six new labels arise from complete observed pairs.

The Q assignment has an adverse effect in the [p191 boot request](../../pages/191.md#edition-cases-military-p191-a-compatibility-with-the-shared-headquarters-reading):
its quantity becomes `?0Q0`. A decimal reading requires a further source
repair; that field is not counted as a recovered quantity.

The square has **40,320** completions before these constraints, **5,040**
after Q, and **720** after the class assignment. The independent
[Tydelski/FX=Y interpretation](../tiflis_appointment/README.md) is compatible
but is not required here. Combining it would leave **120** completions;
its previously reported gain is not counted again.

## Reproduce

```sh
python experiments/nov13_joint_completion/verify.py --verify
python experiments/nov13_joint_completion/verify.py --verify --historical-pdf /path/to/KM_01427_1914_184.pdf
```

The verifier checks the native address donor, the untouched p186 date-field
coordinates and its conditional repeated-month constraint, the class-domain
intersection, source positions, unchanged repair costs, all four p193 endpoint variants,
both current German quotations and the displayed reference fields. It
re-encrypts the five records and four variants under all 720 surviving
squares. The optional PDF argument regenerates the historical source crops
and verifies their pixels.

[Inputs and source provenance](inputs.json) · [Position certificates](certificates.json).

## Further traffic: a cargo quantity and four references

The same VG=2 assignment fixes **six more observed-pair digits in five
records**, with no new source edit. These consequences inherit both the
award-class interpretation and the conditional numerical value DD=1
explained above; they supply no independent evidence for those assumptions.

| Record | Before → after | Conditional field |
| --- | ---: | --- |
| [p199 A1](../../pages/199.md#edition-cases-naval-black-sea-shipping-a1-incoming-steamers-and-a-garbled-cargo-description) | 145 → **146/146** | Cargo **120 tonnes** |
| [p200 B2](../../pages/199.md#edition-cases-naval-black-sea-shipping-b2-payment-in-germany-before-ownership-transfer) | 176 → **178/180** | Closing reference **S22??0** |
| [p199 B1](../../pages/192.md#edition-cases-caucasus-tiflis-appointment-part-1-on-p199-the-recipient-and-a-floating-group) | 129 → **130/131** | Tiflis reference **21?** |
| [p192 A](../../pages/192.md#edition-cases-radio-warsaw-service-messages-p192-a-request-to-kretzschmar-in-bucharest) | 172 → **173/175** | Bucharest reference **2??**, with equal unknowns |
| [p192 B](../../pages/192.md#edition-cases-radio-warsaw-service-messages-p192-b-lp-relays-traffic-in-both-directions) | 132 → **133/134** | War-department reference **?521115** |

The cargo edition retains its earlier single-coordinate exclusion and three
word repairs. All three equally priced broader exclusion models remain in
the certificate: deleting source 50 or 51 gives **120**, while deleting 52
gives **1G0**. Only source 50 is inside the visibly overlong group. The new
digit does not establish a unique exclusion position or explain the code
words `LEBER` and `OPERETTE`.

```sh
python experiments/nov13_joint_completion/verify_traffic.py --verify
```

The extension checks all 720 surviving squares, the live cargo quotation,
each displayed reference and the three cargo geometry alternatives.

[Traffic inputs](traffic_inputs.json) · [Traffic certificates](traffic_certificates.json).

## The transport exchange: two vehicles and two trailers

The native 94-slot [p189 E report](../../pages/189.md#edition-cases-context-transport-two-vehicles-and-two-trailers--p189-e)
has two complete VG count fields and one invalid printed coordinate in
`ANH?ENGER`. VG=2 supplies both counts; replacing the invalid `B` at source
81 with **V** supplies the missing **A**. The message reaches **47/47**
positions, from 44/47, with **one mask fill and no observed-coordinate
change**. The source crop was inspected and its literal B is preserved.

**Readable German — conditional shared VG=2 and the stated word fill:**

> Ja, Hebepumpe aus Blech. Kommen 2 Autos. Hier 2 Anhaenger.

The joint square also sharpens an earlier transport comparison. Four
distinct decimal fields—planned hour/tonnage, reported hour, readiness
hour and men remaining—now have **120** assignments, reduced from 360.
Requiring the reported departure to precede its same-day `13.45` origin
time leaves **24**, all with **AF=3** and a reported departure at **13:00**.
Adding the further assumption that this was the same movement and did not
leave early gives **zero** assignments. That older scenario required
**FV=2**, incompatible with the new **VG=2**.

The chronological branch remains separate from the displayed readings.
Its incompatibility identifies a limit on combining semantic assumptions;
it does not establish that the source's times or movement identities are
correct.
The p198 C header gives `13.03 p.m.` for receipt and `13.45` for origin,
an internal discrepancy preserved in the certificate.

```sh
python experiments/nov13_joint_completion/verify_transport.py --verify
```

The check recomputes both source-hour pairs, enumerates all 720 squares,
verifies the three new p189 E positions and its live quotation, and preserves
the earlier independent scenario record.

[Transport inputs](transport_inputs.json) · [Transport certificate](transport_certificate.json).

## A numerical conflict in the boot request

The p191 quantity contains the same observed XX pair as the p188 headquarters
abbreviation. Under XX=Q it reads **`?0Q0`**. The source crop was checked:
the coordinate concerned is a printed **X**, not an unreadable glyph.

Adding the separately supported FX=Y interpretation leaves one
one-coordinate numerical repair of that Q: change source **102** from
**X to D**, making **DX=0** and the quantity **`?000`**. The possible values
are **3000, 4000, 7000, 8000 and 9000**. Without the Y assumption, changing
that coordinate to F also allows five other digit values; no unique repair
then follows. None of these alternatives is added to the recovery total.

```sh
python experiments/nov13_joint_completion/verify_compatibility.py --verify
```

[Compatibility inputs](compatibility_inputs.json) · [Exact numerical-repair alternatives](compatibility_certificate.json).
