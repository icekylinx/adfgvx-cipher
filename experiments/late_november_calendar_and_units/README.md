# Dates and formations across the late-November traffic

**Research and source comparison: icekylinx and GPT-6 Astra Pro.**

A valid November date and an independent military account supply two further
assignments in the shared Nov28–Dec1 interpretation: **GA=0** and **VG=7**.
Together they fix **13 numeral positions in seven edited texts**, without
adding a source-coordinate change or erasure fill. The existing 24 complete
square possibilities narrow to **six**, then **two**; only DX/FX = 4/5 remains
interchangeable.

## The date constraint

The native opening of p229 A1 has the published labels `26YXX`. Under the
existing numeral and separator interpretation, this becomes `3?X11`.
The four remaining values of its unknown digit give 30, 34, 35 or 37.
Reading the field as a November date admits only **30 November**, assigning
its original `GA` pair to `0`. The photographed originating header separately
reads `1930 (30/11) FUR OKM 3 TEILE`.

This is a calendar interpretation of a transmitted field. It keeps the
228-slot source intact; the earlier `M3T→MIT` word repair still costs one
observed coordinate. [Childs source crop](../late_transport_dispatches/sources/p229_A.png).

## Historical comparison

Béla Barkóczy-Klopsch's *Mackensen vezértábornagy hadseregének átvonulása
Magyarországon az összeomlás után* (Budapest: Stephaneum, 1923) supplies the
formation comparison. Its order of battle names the **7th Bavarian cavalry
brigade**; its 16 December situation groups the **217th, 219th and 6th Reserve
divisions** around Szolnok. These support `VG=7` in the p230 brigade field
and p229's `21?` division. The later situation identifies formations, without
establishing their 30 November locations.

The same account gives **29 November** for the decision to stop German
transports and lists the **89th Division**. Both corroborate the existing
`5→9` interpretation, previously dependent on queried French evidence.

[Institutional scan](https://real-eod.mtak.hu/8911/1/MTA_AKisAkademiaKonyvtara_043.pdf)
· [p11: brigade and division list](sources/barkoczy_p11.png)
· [p22: transport decision](sources/barkoczy_p22.png)
· [p28: the 217/219/6 group](sources/barkoczy_p28.png).

The three extracts were checked against the original page images. The
retrospective study cites Hungarian military archives and demobilization
records; it is not another reception of the telegrams. This scanned copy
includes a later introduction before the 1923 text. The input records the
exact printed/PDF page correspondence, file hash and crop geometry.

## Consequences in the received texts

The counts below compare the previous **FA=J interpretation** with the two
new assignments. They count fixed labels within these conditional readings.

| Record | Before → after | Newly determined fields |
|---|---:|---|
| [p225 B2](../../cases/pages/225.md#edition-cases-military-regimental-journey-report-p225-b2) | 105 → **106/106** | Arrival during the night of **27** |
| [p227 D](../../cases/pages/227.md#edition-cases-military-avoid-fighting-instruction-p227-d) | 135 → **136/136** | OHL reference **11367** |
| [p229 A1](../../cases/pages/229.md#edition-cases-military-late-transport-dispatches-a-the-evening-report-and-halted-railway-transports) | 112 → **114/114** | **30/11** and **217** |
| p229 B1 | 130 → **132/134** | **7** motor columns; zero in `RM1?10?363` |
| p229 B2 | 121 → **123/124** | Two sevens in the reference `7?87` |
| [p230 A4](../../cases/pages/230.md#edition-cases-military-p230-a) | 113 → **115/115** | **7** Bavarian cavalry brigade; zero in `11U30` |
| [p228 B1](../../cases/pages/228.md#edition-cases-military-neuhof-demobilization-b1-the-destination-instruction) | 117 → **120/123** | Order **P067**; unit remains **?7** |

All thirteen positions retain both originally observed coordinates. The
verifier preserves the earlier word-repair ledgers and separately shows
the native interpretations. For example, p230 still contains the damaged
division field `3L3`; assigning its labels does not repair that word. Existing
source erasures, remaining reference characters and the shared 4/5 choice
are retained.

## A separately priced 303rd Division proposal

The same printed p11 order of battle lists the **89th Infantry Division
and 303rd Landsturm Division** under the 63rd Bavarian corps. It supports
reading p230 A4's received `3L3` as **303**, giving **89 und 303 Div. um
Kronstadt**. This is a further historical proposal, separate from the
thirteen no-edit numeral assignments above.

At plaintext position 7, the original pair is `GG`, from source positions
0 and 86. One observed substitution, **source 86 G→A**, changes it to
`GA=0`. The full 230-slot frame and all other coordinates are preserved.
Part 4 then costs **two observed substitutions**, including its earlier
`HEUPT→HAUPT` repair; both surviving parts together cost nine. No source
mask or additional key cell is filled.

The [division certificate](division_certificate.json) enumerates the
equally cheap numeric fields **303, 313, 373 and 383**. The historical
formation list supports 303; the cipher edit cost alone does not select
it. Both existing full-square completions re-encrypt the complete proposed
115-position reading exactly. The older calendar/unit certificate remains
unchanged and continues to display the native `3L3` field.

[Proposal and source provenance](division_inputs.json).

```sh
python experiments/late_november_calendar_and_units/verify_division.py --verify
```

## Additional aviation and radio traffic

The same two squares extend to four further records. In [p229 C](../../cases/pages/229.md#edition-cases-military-late-transport-dispatches-c-an-aviation-unit-and-a-park-at-craiova),
one source-mask fill completes the separator in `WIRD?BITTE`. The interpreted
body fixes **162/165** positions, including **Kofl 11** and **Fliegerabtl. 38**;
`HK?` and the two closing reference positions remain unresolved. Its total
cost is **3 observed substitutions and 32 mask fills**.

In [p226 A2](../../cases/pages/226.md#edition-cases-radio-radio-traffic-transfer-fragment), reading the
opening `?DEZ` as a day requires one further coordinate fill. It does not
select the date: **4 December / SCHWERE 15** and **5 December / SCHWERE 14**
are the two possible assignments. The same cell makes the [p230 C](../../cases/pages/230.md#edition-cases-radio-nov30-radio-personnel-p230-c)
hour **5** in the first branch and **4** in the second. Both source variants
of C are retained.

The unaltered [p230 D](../../cases/pages/230.md#edition-cases-radio-nov30-radio-personnel-p230-d)
footer becomes **98179**. Its fourth digit supplies one further occurrence
of `VG=7` outside the thirteen positions counted above. Two more occurrences
are fixed in the still-damaged `GROSSW7RDEIN` and `7Z12` fields; their words
remain unresolved. These additions
leave both square possibilities intact and add no observed-coordinate
substitution.

[Extension inputs](additional_traffic.json) · [Exact source positions and branches](traffic_certificate.json).

```sh
python experiments/late_november_calendar_and_units/verify_traffic.py --verify
```

## Reproduce the calendar and unit comparison

```sh
python experiments/late_november_calendar_and_units/verify.py --verify
```

The verifier enumerates all 24 prior squares, tests the calendar and unit
constraints, and re-encrypts every record under both surviving full squares.
It checks the two new German readings against their exact interpreted
streams and verifies the displayed numerical fields. Source-mask values in
round-trip witnesses are consistency examples.

To regenerate the historical crop pixels from the pinned institutional PDF:

```sh
python experiments/late_november_calendar_and_units/verify.py --verify --historical-pdf /path/to/MTA_AKisAkademiaKonyvtara_043.pdf
```

[Inputs and source provenance](inputs.json) · [Position certificates](certificates.json)
· [Previous shared-J interpretation](../late_november_joint_completion/README.md).
