# Siegfried and Osthoff: later military-mission recall messages

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** Four newly source-reviewed physical parts on Childs p161. The Osthoff body was already identified from p138/p148/p149; this edition adds a later differently keyed witness and directly supports three previously editorial letters.

Source edition and verification: **icekylinx and GPT-6 Astra Pro**. Published period keys: Lasry, Niebel, Kopal and Wacker, unchanged. Earlier unreviewed p161 second-part readings and the existing [Osthoff source-family edition](osthoff.md) retain their prior credit. No existing p138/p148/p149 record is counted again.

## Conditional digit reading

An earlier Siegfried cancellation, [p135 A](siegfried_assignment_cancellation.md), directly supplies **45610** under the Nov4–6 key. If both orders cite the same reference, p161 C1’s observed XA/VF pairs fix **XA=5, VF=6**, so its reference reads **ZU2NR45610**. The two orders differ in wording and reception; [the complete comparison](../../experiments/nov7_9_joint_digits/README.md) retains the alternative 46510. The erased date digit has the separately priced
completion below.

## Conditional complete Siegfried order

A separately priced date completion reads **MK 2.11**. The erased position has native domain **1GIKNY**, so 1 is its only numerical value if this is a day/month date. The distinct Osthoff recall on p161 D1 directly preserves `MKX2X11` in observed pairs. This supports the format and month, rather than treating the two orders as copies.

The completion supplies **F at printed dash 185**, changing `?G` to `FG`.
It adds one source-mask fill and no observed-coordinate substitution.
Together with the 45610 reference interpretation, C1 reaches **102/102
fixed labels** at **four observed substitutions and five printed-erasure
fills**. C2 is already an unchanged 77-label source reading.

**Readable German — complete conditional C1–C2 order; source abbreviations and spellings retained:**

> SS Doppel GR. HQ. MK. 2.11. Militaermiszion Konstantinopel. Zu 2 Nr. 45610. Komdo Oberlts Siegfried nach Tuerkei u deszen Zuteilung zur Milmiszion ist aufgehoben. AKO folgt. Allerh. Bef. Chef Milkab Frhr Marschall.

The two parts therefore have **179/179 conditional fixed labels**. The
spelling `DESZEN`, the abbreviation `u` and the received `MISZION` spellings
remain literal. The calendar reading does not force the reference
assignment: under the opposite 5/6 square the same date reads 2.11 while
the reference becomes 46510.

## Meaning and exact scope

C is an order cancelling Oberleutnant Siegfried's posting to Turkey and assignment to the Military Mission. D concerns Captain of the Reserve Osthoff: his Turkey posting and mission assignment are cancelled, and he is to be transferred to the replacement battalion of a railway regiment. The cabinet order will follow; the closing is from the Chief of the Military Cabinet, Frhr. Marschall.

These are readings of the telegrams. The edition does not establish a further biographical identity for either officer. The original abbreviations and the recurring spellings `MISZION` and `DESZEN` remain in the literal and edited strings.

Childs printed page 161 / PDF page 164 gives C at 05.57 a.m. on 9 November, `NR16 (9/11) 2 TLE`, and D at 06.05 a.m., `FUER YZ NR17 (9/11) 2 TEILE`. All four parts decrypt under the unchanged Nov7–9 key. Their printed lengths 204/154/254/190 exactly match the counted source slots.

## Counts and source readings

The table retains the baseline editions. With the separate reference and date
completion above, all four parts have **401/401 conditional fixed labels**,
at six observed substitutions and five printed-erasure fills in total.

| Record | Source slots | Raw fixed positions | Edited fixed positions | Observed-coordinate substitutions | Source fills |
|---|---:|---:|---:|---:|---:|
|p161_C1|204|95/102|99/102|4|4|
|p161_C2|154|77/77|77/77|0|0|
|p161_D1|254|127/127|127/127|2|0|
|p161_D2|190|95/95|95/95|0|0|

The physical-record total is **802 coordinate slots / 401 plaintext positions**. Raw fixed positions total 394; the edited layer fixes 398.

## p161 C1 — Siegfried posting cancellation, first part

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
SSDOPPELGRXHQXMKX2X?1XMILITA??MISZIONK?GSTANTINOPULXZU2NR4??10XKOMDOOBERLTSSIEGFRIEDNACHT?ERKEI0DESZEN
```

**Edited output:**

```text
SSDOPPELGRXHQXMKX2X?1XMILITAERMISZIONKONSTANTINOPELXZU2NR4??10XKOMDOOBERLTSSIEGFRIEDNACHTUERKEIUDESZEN
```

</details>

## p161 C2 — Siegfried mission assignment cancelled and cabinet-order closing

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ZUTEILUNGZURMILMISZIONISTAUFGEHOBENAKOFOLGTXALLERHBEFXCHEFMILKABFRHRMARSCHALL
```

</details>

## p161 D1 — Osthoff posting and mission assignment cancelled

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
SSDOPPELXGRXHQUXMKX2X11XMILITAERMISZIONKONSTANTINOPELXKOMMRNDODESHPTMSDXRXOSTHOFFNACHTUERKEIENDZUTEILUNGZURMILMISZIONAUFGEHOBEN
```

**Edited output:**

```text
SSDOPPELXGRXHQUXMKX2X11XMILITAERMISZIONKONSTANTINOPELXKOMMANDODESHPTMSDXRXOSTHOFFNACHTUERKEIUNDZUTEILUNGZURMILMISZIONAUFGEHOBEN
```

</details>

## p161 D2 — Osthoff railway battalion reassignment and cabinet-order closing

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DERSELBEISTDEM1XERSBATLEISENBAHNREGMTS1ZUUEBERWEISENXAKOFOLGTXALLERHBEFXCHEFMILKABFRHRMARSCHALL
```

</details>

## Cross-period evidence for the earlier Osthoff edition

The earlier p149 A2 literal source had `UEM`, `ERSBKTL`, and `REGM1S`. Its already published editorial reading proposed `DEM`, `ERSBATL`, and `REGMTS`. The new p161 D2 source directly gives all three proposed letters under the other period key, without an edit to D2:

| Earlier p149 A2 position | Earlier raw → proposed | New p161 D2 observed pair | New original coordinate indices | Result |
|---:|---|---|---|---|
|11|U→D|XV|58,135|Direct D in DEM|
|20|K→A|XD|49,107|Direct A in BATL|
|36|1→T|GV|80,118|Direct T in REGMTS|

Indices are zero-based. The certificate independently decrypts the selected older source, verifies that these were exactly its three preexisting editorial changes, and checks the new complete coordinate pairs. The older source's original repair costs remain unchanged.

The later wording is abbreviated and includes an additional raw `1` after `REGMTS`. It is not an identical ciphertext stream or a proof of a common original at every character. Its value is direct corroboration of the three specific earlier readings.

## Remaining uncertainty

In the unchanged baseline edition, C1's date-like field remains `2X?1`: its erased position 19 has domain **1GIKNY**. The two question marks in `ZU2NR4??10` are different: they arise from the observed XA and VF cells of the published partial square, at plaintext positions 58 and 59. Their joint assignments are **56 or 65**, not independent choices that could both be 5 or both be 6. The conservative streams retain both assignments; the optional cross-period interpretation is given above.

The baseline C1 layer has four known-coordinate changes and four printed-erasure fills; the conditional date completion adds the fifth fill. The local `0→U` proposal before `DESZEN` alone costs two observed-coordinate substitutions; it is not a global reassignment of the digit0 key label. D1 has two word repairs, `KOMMRNDO→KOMMANDO` and `END→UND`. C2 and D2 are entirely unchanged source readings.

## Evidence and reproduction

[The input record](../../experiments/military_mission_recalls/inputs.json) preserves all manual rows, literal irregular glyphs, source headers and crop-rendering metadata. [The certificate](../../experiments/military_mission_recalls/certificates.json) retains all coordinate changes, masks, symbol domains, digit/J/Q/Y labels and round trips. Global witnesses demonstrate consistency only; they do not recover a unique original.

[The README](../../experiments/military_mission_recalls/README.md) provides portable verifier commands, including exact source-crop pixel regeneration from the pinned full scan. Prior candidates and specific earlier source editions are distinguished; the bounded literature check is not a universal priority claim.
