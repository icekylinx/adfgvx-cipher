# Eleventh Army subordination to Mackensen

A two-part telegram on Childs pp100–101 reports that the 11th Army and all its German elements have been placed under `O.K. MACKENSEN` and asks for orders.

**Complete edition by printed page:** [p. 100](../pages/100.md) · [p. 101](../pages/101.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Prepared by **icekylinx and GPT-6 Astra Pro**.

A two-part telegram on Childs pp100–101 reports that the 11th Army and all
its German elements have been placed under `O.K. MACKENSEN` and asks for
orders. A second copy of the ending provides useful letter evidence but has
an extra five-coordinate group and a weak source glyph. The native reading
and the conditional copy analysis remain distinct.

## p100 D1

The [D1 source](../../experiments/nov1_mackensen_and_orient_reports/sources/p100_D1.png)
reads `UKS v ZON`, received at an unspecified time on November 2, origin
`2312 (1) 2 TLE`, and `1 TL RICHI-136`. There are 136 slots, including the
printed `L` at source 39 and `C` at 56. The following page is explicitly
marked as a continuation.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native source frame**

```text
OXKXMACKENSENX11XARMEE?ITALLENDEUTSCHENTEILENISTLAUT?XHXLXRMX1A11127
```

**Edited output — explicitly priced coordinate repairs and mask fills**

```text
OXKXMACKENSENX11XARMEEMITALLENDEUTSCHENTEILENISTLAUTOXHXLXRMX1A11127
```

</details>

**Readable German — from the edited layer**

> O.K. Mackensen. 11. Armee mit allen deutschen Teilen ist laut O.H.L. RM 1A11127

This first part has 66/68 raw fixed positions. Filling `L39` as `D` and
`C56` as `A` gives 68/68 fixed positions with **no observed-coordinate
substitutions**. It ends in reference `RM 1A11127`, with the sentence
continuing in A2. The source does not supply additional words between the
reference and that continuation.

## p101 A2

The [A2 source](../../experiments/nov1_mackensen_and_orient_reports/sources/p101_A2_B2.png)
has the same `UKS v ZON`, `2312 (1) 2 TLE` heading and is explicitly
`2 TL RICHI-132`. All 132 native coordinates are valid.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native source frame**

```text
DEMOXKXMACKENSENUNTERSTELLTUNDBITTEPUMBEFEHLEXAXOXKX11XRMX1A7011XX
```

**Edited output — explicitly priced coordinate repairs and mask fills**

```text
DEMOXKXMACKENSENUNTERSTELLTUNDBITTETUMBEFEHLEXAXOXKX11XRMX1A7011XX
```

</details>

**Readable German — from the edited layer**

> dem O.K. Mackensen unterstellt und bittet um Befehle. A.O.K. 11. RM 1A7011.

All 66 raw labels are fixed. The single change is source 65 `V`→`F`, giving
`BITTET` in place of `BITTEP`. The second copy below directly supports the
`T` coordinate. The reference `7011` and the two appearances of `11` across
these parts remain literal. The [p99 receipt acknowledgment](../radio/nov1_contact_and_mail.md#p99-d-acknowledgment-of-an-ohl-message)
also names reference `11127`; it remains a separate telegram rather than
an additional part of this text.

## p101 D2

The [D2 source](../../experiments/nov1_mackensen_and_orient_reports/sources/p101_C1_D2.png)
reads `UKS v ZON`, `2.15 a.m., November 2nd`, origin `2352 (1)`, and
`2 TL RIZI-137`. Its origin differs from A2's `2312`. This edition reserves
**137 source slots**, including printed `S` at 19 and an illegible fifth
slot after `XDVV` at 119. The latter is not transcribed as the copy's expected
`X`. The [14× detail](../../experiments/nov1_mackensen_and_orient_reports/sources/p101_D2_illegible.png)
shows a separate upper stroke and lower ink trace in that slot. The advertised
137 supports this interpretation but is not its only evidence. In the source
JSON, `?` at this one location explicitly denotes an illegible ink remnant,
not a printed question mark.

The common-frame model excludes the **five observed coordinates** in
`XDDAF`, source 10–14, to obtain 132 slots. Those exclusions have a cost of
five observed-coordinate operations; they are not free padding removal.
All native 137-slot diagnostics, including the unpaired coordinate, remain
in the certificate.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 132-slot copy-alignment frame**

```text
?EMOXKXMACKENSENUNTERSTELLTUNDBI?TETUMBEFEHLEXAXOXKX11XRMX1A70G1XX
```

**Edited output — same conditional frame; separately priced exclusions**

```text
DEMOXKXMACKENSENUNTERSTELLTUNDBITTETUMBEFEHLEXAXOXKX11XRMX1A7011XX
```

</details>

**Readable German — from the conditional edited layer**

> dem O.K. Mackensen unterstellt und bittet um Befehle. A.O.K. 11. RM 1A7011.

This model has 64/66 raw fixed positions. The selected edited text fills
`S19`→`G` and the illegible source 119→`X`, and changes source 136 `F`→`X`.
The last substitution changes the raw reference `70G1` to `7011`, supported
by A2's unchanged coordinate. Its price is **1 observed substitution,
2 source-mask fills and 5 observed-coordinate exclusions**.

### Equal-cost copy readings

After the declared alignment, the two endings have 128 identical observed
coordinates, two complementary masks, and two observed conflicts. At common
frame index 65, A2 has `V` and D2 has `F`; at 131, A2 has `X` and D2 has `F`.
There are four equally minimum common streams:

| Common word / reference | A2 substitutions | D2 substitutions | Combined substitutions |
|---|---:|---:|---:|
| `BITTEP / 7011` | 0 | 2 | 2 |
| **`BITTET / 7011`** | **1** | **1** | **2** |
| `BITTEP / 70G1` | 1 | 1 | 2 |
| `BITTET / 70G1` | 2 | 0 | 2 |

Every row additionally uses the same two D2 source-mask fills and the
separately stated five exclusions. The chosen readable row combines the
`T` supported by D2 and the numeric reference supported by A2. Equal edit
cost alone does not select it, and the two physical copies do not prove
independent transmission histories.

### Geometry and weak-glyph limits

All **133 contiguous five-coordinate exclusions** in the 137-slot source
were evaluated against the selected common text. Starts **8, 9, 10, 11 and
12** tie at one observed substitution and give exactly the same raw and
edited streams. Their source-origin maps differ. Start 10 is the printed
group boundary used for presentation, not a unique historical loss or
insertion location. This finite test does not exhaust arbitrary five-coordinate
exclusions or alternative plaintexts.

The old OCR's **136-slot interpretation** is retained as an alternate
reading of the weak ink trace. Under that interpretation, the equivalent
132-slot copy model needs five observed exclusions, one newly supplied
coordinate, one source-mask fill and one substitution. It produces the same
final text. The text therefore cannot decide whether the weak fifth slot
was a printed character or a missing coordinate; the primary slot choice
comes from the image review.

## Evidence and attribution

The published `Nov1-3` square and ranks retain the credit of **George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker**. The current source and arithmetic
review is by **icekylinx and GPT-6 Astra Pro**. Earlier unreviewed OCR
candidates are retained in the [prior-evidence snapshot](../../experiments/nov1_mackensen_and_orient_reports/prior_evidence.json).
No first historical decipherment priority is claimed. The existing
[p100 challenge](../p100.md) is a separate A message and keeps Armin's earlier
body credit; its status is unchanged.

[Literal rows, key and source images](../../experiments/nov1_mackensen_and_orient_reports/inputs.json),
[recomputed domains and complete ledgers](../../experiments/nov1_mackensen_and_orient_reports/certificates.json)
and [verification commands](../../experiments/nov1_mackensen_and_orient_reports/README.md)
make the stated frames and repairs reproducible. The verifier also checks
that each readable passage preserves every non-`X` label in its cited stream.

</details>
<!-- CASE-EDITION:END -->
