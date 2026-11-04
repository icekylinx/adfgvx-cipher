# March and aerial reconnaissance report

The report places the unresolved unit `211?IVD` in the area of `TITELC` by `9 / 11`. An `A. H. Q?` field gives `5 / 11` and the conditionally completed `NAGQBECSEREK`. The final clause reports no substantial aerial-reconnaissance findings.

**Complete edition by printed page:** [p. 127](../pages/127.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Case index](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

## p127 A3

**Readable German — conditional place completion; two fields unresolved:**

> 211?IVD marschiert bis 9 / 11 in Raum um TITELC. A. H. Q? 5 / 11 NAGQBECSEREK. Luftaufklaerung nichts Wesentliches.

The report places the unresolved unit `211?IVD` in the area of `TITELC` by `9 / 11`. An `A. H. Q?` field gives `5 / 11` and the conditionally completed `NAGQBECSEREK`. The final clause reports no substantial aerial-reconnaissance findings.

**Reading:** 90/100 positions are fixed by the original coordinates. The proposal reaches **98/100**, using two observed-coordinate substitutions and eight printed-mask fills under the unchanged Nov4–6 key. The unit and `Q?` fields remain unresolved.

### Two letters from a related station report

The [p120 C setup notice](../radio/nov4_eilvese_and_setup.md#p120-c) contains the fully observed place string `NAGQBESCEREK`. Both sources name **ZON** as sender and give the origin day as **4**: `2000 (4)` here and `2332 (4)` in p120 C. Their shared `NAGQBE` opening and `EREK` ending support two missing letters in this report.

| Source or layer | Place field |
| --- | --- |
| p120 C, native reading | `NAGQBESCEREK` |
| p127 A3, native reading | `N?GQBECSER?K` |
| p127 A3, conditional completion | `NAGQBECSEREK` |

The two new letters cost **two mask fills and no further observed substitution**. `A` belongs to the surviving `V?` domain `8ABGIR`; `E` belongs to the `?A` domain `1EJORT`. The comparison selects them as a place-name hypothesis. Each source retains its own observed `CS` or `SC` sequence and its literal `Q`.

<details>
<summary>Original source, exact readings and coordinate account</summary>

**Source:** printed p127, heading *4th NOVEMBER, 1918*. Receipt: `A) UKH v ZON (4.30 a.m., November---)`; origin: `2000 (4)`; part label: `3 TL RICHI-200`. The interception day is absent.

![Source p127 A3](../../experiments/early_radio_and_leave_records/sources/p127_A3.png)

**Raw output — native 200-coordinate frame:**

```text
211?IVDXMARS?HIERCBI?9X11XINR?UMUMTIT?LCXAXHXQ?X5X11XN?GQBECSER?KXXLUFT?UFKLAERU?ZNICHTSWESENTLICHES
```

**Edited output — two observed substitutions and eight printed-mask fills:**

```text
211?IVDXMARSCHIERTBIS9X11XINRAUMUMTITELCXAXHXQ?X5X11XNAGQBECSEREKXXLUFTAUFKLAERUNGNICHTSWESENTLICHES
```

The earlier 96-position proposal filled six of the ten leading dashes. The present extension fills source slots 6 and 7, yielding `A` at plaintext 54 and `E` at 63. The earlier proposal and its exact additional cost remain in the input record. All indices below are zero-based.

| Source index | Printed | Proposed | Cost |
| ---: | --- | --- | --- |
| 108 | `D` | `A` | Observed-coordinate substitution |
| 150 | `F` | `V` | Observed-coordinate substitution |
| 1 | `-` | `X` | Source-mask fill |
| 2 | `-` | `G` | Source-mask fill |
| 3 | `-` | `V` | Source-mask fill |
| 4 | `-` | `A` | Source-mask fill |
| 6 | `-` | `F` | New place-field fill |
| 7 | `-` | `F` | New place-field fill |
| 8 | `-` | `F` | Source-mask fill |
| 9 | `-` | `X` | Source-mask fill |

`TITELC`, including its final `C`, is unchanged. The two remaining dashes supply the unknowns in `211?IVD` and `Q?`.

</details>

### Evidence and attribution

The [input and place-comparison record](../../experiments/early_radio_and_leave_records/inputs.json) preserves both proposals and binds the independent p120 C source. The [certificate](../../experiments/early_radio_and_leave_records/certificates.json) traces each shared donor letter to two observed coordinates and records the target's half-coordinate domains. The [verifier](../../experiments/early_radio_and_leave_records/verify.py) recomputes the readings, exact costs and displayed German.

Source edition and place comparison: **icekylinx and GPT-6 Astra Pro (2026)**. Childs supplies the historical collection. The unchanged published key is credited to Lasry, Niebel, Kopal and Wacker, with Lasry's published period-key list. Earlier repository OCR remains in the [attribution record](../../experiments/early_radio_and_leave_records/prior_candidates.json).

</details>
<!-- CASE-EDITION:END -->
