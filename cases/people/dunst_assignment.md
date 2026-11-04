# Major Dunst — cancellation of the Turkey and military-mission assignment

[All cases](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and review: icekylinx and GPT-6 Astra Pro.** This two-part
message cancels the assignment of Major `DUNST` to Turkey and his allocation
to the military mission. The stated earlier posting date, the order reference
and the final number are literal labels under the published November 1–3 key;
no historical biography or numerical reassignment is used to obtain them.

Childs p. 95 is headed 1 November 1918. The shared source header is
`A) OSM v LP (5.22 p.m., November 1st)`, `SSD GRHQU (1/11)0400 2 TEILE`.
The numbered parts advertise 282 and 464 coordinates. All **746 valid source
coordinates** are retained in those working frames, fixing **373 raw
plaintext positions**. Four observed-coordinate word repairs are proposed.
A separate prefixed dash before the first complete group is preserved and
explicitly excluded from the working first-part frame.

## p95 A1

[Source crop](../../experiments/dunst_assignment/sources/p95_A1.png).
`1 TL RICHI-282`.

### The prefixed dash

The [enlarged beginning](../../experiments/dunst_assignment/sources/p95_A1_prefix.png)
prints `-DGDGX`. The five coordinate letters `DGDGX` begin at the same first-
character alignment as the following rows; the dash lies just to their left.
There are **282 valid coordinate letters**, matching the advertised length,
and **283 displayed slots if the prefixed dash is counted**.

The working reading excludes that one noncoordinate mark. It excludes no
observed ADFGVX coordinate. The certificate preserves the complete 283-slot
literal source, its paired-prefix diagnostic and its unpaired coordinate.
The source does not explain the mark, so the boundary interpretation remains
explicit rather than being silently treated as an absent ciphertext symbol.

A retrospective consistency check evaluated all **283 single-slot exclusions**
against the displayed raw reading. Excluding slot 0, the dash, requires no
other change. Excluding slot 1, the first observed `D`, also gives no known-
coordinate mismatch, but additionally deletes that observed `D` and fills the
retained dash with `D`. All other placements disagree with the fixed target.
The selected slot-0 model preserves every observed coordinate and needs no
fill. This check prices alternatives to that fixed reading; it does not
establish a unique historical copying mechanism.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — 282-coordinate frame, with the prefixed dash excluded.**

```text
DEUTSCHERMILITXBEVOLLMAECHTIGTERKONST1NTINOPELXXAXKXOX26X10X18XXDIEUNTERDEMDEZEMBERX2X1917XBEFOHLENEKOMMANDIERUNGR7SMAJORSXDUNSTXVONDERARMEEX
```

**Edited output — same frame, with three observed-coordinate word repairs.**

```text
DEUTSCHERMILITXBEVOLLMAECHTIGTERKONSTANTINOPELXXAXKXOX26X10X18XXDIEUNTERDEMDEZEMBERX2X1917XBEFOHLENEKOMMANDIERUNGDESMAJORSXDUNSTXVONDERARMEEX
```

</details>

**Readable German — first part, continuing into A2:**

> Deutscher Milit[aer]-Bevollmaechtigter Konstantinopel. A. K. O. 26.10.18. Die unter dem Dezember 2, 1917 befohlene Kommandierung des Majors Dunst von der Armee —

`[aer]` expands the abbreviation `MILIT` in the readable layer only. The dash
at the end of this quotation is display punctuation indicating continuation
into the next numbered part; it is unrelated to the source's prefixed dash.
The date order is retained from `DEZEMBERX2X1917`.

The source-supported repairs change `KONST1NTINOPEL` to `KONSTANTINOPEL`
and `R7S` to `DES` before `MAJORS`. Raw numeral labels `1` and `7` change
only inside those words and at the listed coordinate costs. The fields
`AXKXOX26X10X18`, `DEZEMBERX2X1917` and `DUNST` are unchanged.

All indices below are zero-based; first-part literal indices include the
prefixed dash, while working indices do not.

| Literal source index | Working-frame index | Printed | Proposed | Plaintext effect |
|---:|---:|---|---|---|
| 43 | 42 | `F` | `V` | Position 114: `7` → `E` |
| 64 | 63 | `F` | `G` | Position 37: `1` → `A` |
| 131 | 130 | `D` | `G` | Position 113: `R` → `D` |

## p95 A2

[Source crop](../../experiments/dunst_assignment/sources/p95_A2.png).
`2 TL RICHI-464`. The complete native frame contains 464 valid coordinates.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — all 464 observed coordinates; unchanged key.**

```text
ZULETZTDEMCHEFDESGENERALSTABESDESFELDHEERESZURBESONDERENVERWENDUNGZURVERFUEGUNGGESTELLTXNACHDERTUERKEIUNDZUTEILUNGDESSELBENZURMILITAERMISSIONWIRDAUFGEHOBENXXISTBEORDRTXMITTEILUNGANMILIQAERMISSIONERBETENXXCHEFXGENSTBXFELDHEERX92527XX
```

**Edited output — one observed-coordinate word repair.**

```text
ZULETZTDEMCHEFDESGENERALSTABESDESFELDHEERESZURBESONDERENVERWENDUNGZURVERFUEGUNGGESTELLTXNACHDERTUERKEIUNDZUTEILUNGDESSELBENZURMILITAERMISSIONWIRDAUFGEHOBENXXISTBEORDRTXMITTEILUNGANMILITAERMISSIONERBETENXXCHEFXGENSTBXFELDHEERX92527XX
```

</details>

**Readable German — continuation of A1:**

> — zuletzt dem Chef des Generalstabes des Feldheeres zur besonderen Verwendung zur Verfuegung gestellt — nach der Tuerkei und Zuteilung desselben zur Militaermission wird aufgehoben. Ist beord[e]rt. Mitteilung an Militaermission erbeten. Chef Genstb. Feldheer, 92527.

The message identifies the officer's most recent attachment, cancels the
Turkey assignment and allocation to the military mission, and requests that
the mission be informed. The opening and closing dashes around the
parenthetical attachment are editorial punctuation.

The second occurrence of `MILIQAERMISSION` is repaired to
`MILITAERMISSION`; the earlier occurrence already reads correctly. The
source's abbreviated `BEORDRT` remains unchanged in both machine strings.
`[e]` is a prose spelling completion only, not an inserted decoded character
or a ciphertext repair. The final `92527` is unchanged.

| Literal source index | Working-frame index | Printed | Proposed | Plaintext effect |
|---:|---:|---|---|---|
| 410 | 410 | `V` | `X` | Position 184: `Q` → `T` |

## Evidence, verification and credit

The [full page](../../experiments/dunst_assignment/sources/p95_full.png),
[literal inputs](../../experiments/dunst_assignment/inputs.json),
[coordinate certificates](../../experiments/dunst_assignment/certificates.json)
and [reproduction notes](../../experiments/dunst_assignment/README.md) retain
all source rows, the prefixed mark, unchanged key, exact position maps and
word repairs. The source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, printed p. 95 / PDF p. 98.

The November 1–3 key is prior Lasry-team work and retains its original
provenance. The [prior-evidence snapshot](../../experiments/dunst_assignment/prior_evidence.json)
keeps the earlier unreviewed 243/424-slot OCR frames. Both began with the
second typed row and did not establish these bodies. The complete source
edition and repair ledger are by **icekylinx and GPT-6 Astra Pro**; no universal
first-decipherment or independent identification of Dunst is claimed.

```sh
python3 experiments/dunst_assignment/verify.py --verify
python3 experiments/dunst_assignment/verify.py --verify --pdf /path/to/childs.pdf
```
