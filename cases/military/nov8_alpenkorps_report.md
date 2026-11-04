# Alpenkorps departure and march report

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

A conditional second-part reading concerns preparations to transport the Alpenkorps and the continuation of a march. The source is dated 8 November 1918; the receipt header is 11.44 p.m. on 8 November. The first part of this physical p160 transmission has not been identified. The place-like strings NAGYBESKEREK and WERGCHEEZ are left exactly as decoded.

Source: Childs, printed pp.160–161 (PDF pp.163–164). [Source images and inputs](../../experiments/nov8_radio_keys_and_reports/inputs.json), [certificates](../../experiments/nov8_radio_keys_and_reports/certificates.json), [method and limitations](../../experiments/nov8_radio_keys_and_reports/README.md). All indices below are zero-based.

## p160 A2

Header: `A) UKS v ZON (11.44 p.m., November 8th); 1915 (8/11) 2 TLE; 2 TL; RICHI-238`.

Literal 240 versus advertised 238. The two six-character groups occupy source 15–20 and 26–31; the primary conditional frame excludes 18 and 26. This is one of the two best alignments with the independently transcribed p170 B2 source. Both retain the observed coordinates that give `RD`; they differ between `UJVERBASZ` and `UZVERBASZ`, which the parallel's mask cannot resolve. The displayed reading retains the former branch. The first part of this physical p160 transmission is not identified. ZON is a separate cleartext footer. WERGCHEEZ and NAGYBESKEREK stay literal.

The source has **240 slots** (239 valid coordinates). The conditional model has 238 slots / 119 plaintext positions: 117 fixed raw, 118 fixed after the stated edits.

**Cost:** 4 observed-coordinate substitutions; 1 printed-mask fill; 2 observed-coordinate exclusions; 0 mask exclusions; no inserted coordinates.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — under the explicitly conditional exclusion frame:

```text
ALPENKOYPSW2RDUJVERBASZZUMABTRFNSPORTBEREIT?ESTELLTXX219X217XUNU?XRDXSETZEN9X11XMARSCHINLINIENAGYBESKEREKXWERGCHEEZFORT
```

**Edited output** — changes and source offsets are enumerated in the certificate:

```text
ALPENKORPSWIRDUJVERBASZZUMABTRANSPORTBEREITGESTELLTXX219X217XUND?XRDXSETZEN9X11XMARSCHINLINIENAGYBESKEREKXWERGCHEEZFORT
```

</details>

**Readable German** — spacing, case, punctuation and conventional umlaut rendering only; all non-`X` labels match the edited output:

> Alpenkorps wird Ujverbasz zum Abtransport bereitgestellt. 219, 217 und ? Rd. setzen 9.11 Marsch in Linie Nagybeskerek, Wergcheez fort.

## Parallel traffic and an additional interpretation

The previously reviewed [p170 B1/B2 and p166/p167 reports](nov9_operational_reports.md)
provide related earlier-part context and a near-identical second part. The
source headers differ: this p160 transmission is received on November 8,
while p170 B is received on November 9. The parallel does not identify the
missing physical first part of this particular p160 transmission.

The source-only audit compares **all 28,680 two-coordinate exclusion maps**
with the untouched 238-slot p170 B2 source. It uses no proposed German text,
word score or completed square to choose the maps. Exactly two maps attain
the minimum of five observed disagreements:

| Excluded p160 source positions | Known agreements / disagreements / masks | Native name-like token | Native abbreviation |
|---|---:|---|---|
| 18, 26 | 231 / 5 / 2 | `UJVERBASZ` | `RD` |
| 18, 27 | 231 / 5 / 2 | `UZVERBASZ` | `RD` |

The previous frame excluded 19 and 26 and had six disagreements. Both new
minimum maps instead exclude source 18 `D`, retaining source 19 `X`.
Together with source 199 `V`, that observed coordinate gives square cell
`XV` = `D` at plaintext position 67. **`RD` therefore needs no coordinate
substitution under either minimum map.** This sharpens the frame without
increasing the fixed-position count: each map fixes 117 of 119 raw positions,
and 116 positions have the same fixed label across both maps.

The second exclusion remains conditional. Retaining source 27 `X` gives
`J`; retaining source 26 `D` gives `Z`. P170 frame 25 is a mask, so the
source comparison cannot independently select `UJVERBASZ`. By contrast,
p170 frame 183 supplies `D` where p160 source 185 is a dash under both
maps, supporting the fill in `BEREITGESTELLT`. All five observed disagreements
remain recorded.

**Conditional interpretation:** substituting the parallel's `WERSCHETZ`
for the primary `WERGCHEEZ` costs **two additional observed-coordinate
substitutions**, at p160 source 48 G→X and source 192 D→G. Its total is
**six observed substitutions**, one printed-mask fill and two observed
exclusions: one fewer substitution than under the previous frame. This
separately priced interpretation is not substituted into the primary edited
or readable stream above. The shared `ABTRFNSPORT` raw spelling still needs
its stated editorial correction; agreement between copies does not correct it.

The [parallel certificate](../../experiments/nov8_radio_keys_and_reports/parallel_witnesses.json)
retains every source and plaintext difference, both minimum source-alignment
maps, prior record identity and both complete 5/6 key witnesses. The earlier operational case's historical unit
identification remains a separate context layer; no unknown digit is filled
in this source edition. No previously cataloged parallel is counted again.

## Shared uncertainty and credit

The two missing square cells `VF` and `XA` jointly contain `5` and `6`. Both complete assignments are retained as compatibility witnesses; every occurrence of a cell shares the same digit. The displayed `?` positions therefore must not be treated as independent digit choices. In p160 B2 one additional source coordinate remains unfilled; its domain can include letters as well as digits.

The published Nov7–9 period key and earlier OCR candidates are credited in the inputs. This edition adds source inspection, separate repair costs and exact readable-text mappings. It does not claim new recovery of the period key.
