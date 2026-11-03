# Alpenkorps departure and march report

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

A conditional second-part reading concerns preparations to transport the Alpenkorps and the continuation of a march. The source is dated 8 November 1918; the receipt header is 11.44 p.m. on 8 November. The first part of this physical p160 transmission has not been identified. The place-like strings NAGYBESKEREK and WERGCHEEZ are left exactly as decoded.

Source: Childs, printed pp.160–161 (PDF pp.163–164). [Source images and inputs](../../experiments/nov8_radio_keys_and_reports/inputs.json), [certificates](../../experiments/nov8_radio_keys_and_reports/certificates.json), [method and limitations](../../experiments/nov8_radio_keys_and_reports/README.md). All indices below are zero-based.

## p160 A2

Header: `A) UKS v ZON (11.44 p.m., November 8th); 1915 (8/11) 2 TLE; 2 TL; RICHI-238`.

Literal 240 versus advertised 238. The two six-character groups occupy source 15–20 and 26–31; the primary conditional frame excludes 19 and 26. The first part of this physical p160 transmission is not identified. ZON is a separate cleartext footer. WERGCHEEZ and NAGYBESKEREK stay literal.

The source has **240 slots** (239 valid coordinates). The conditional model has 238 slots / 119 plaintext positions: 117 fixed raw, 118 fixed after the stated edits.

**Cost:** 4 observed-coordinate substitutions; 1 printed-mask fill; 2 observed-coordinate exclusions; 0 mask exclusions; no inserted coordinates.

**Raw output** — under the explicitly conditional exclusion frame:

```text
ALPENKOYPSW2RDUJVERBASZZUMABTRFNSPORTBEREIT?ESTELLTXX219X217XUNU?XREXSETZEN9X11XMARSCHINLINIENAGYBESKEREKXWERGCHEEZFORT
```

**Edited output** — changes and source offsets are enumerated in the certificate:

```text
ALPENKORPSWIRDUJVERBASZZUMABTRANSPORTBEREITGESTELLTXX219X217XUND?XREXSETZEN9X11XMARSCHINLINIENAGYBESKEREKXWERGCHEEZFORT
```

**Readable German** — spacing, case, punctuation and conventional umlaut rendering only; all non-`X` labels match the edited output:

> Alpenkorps wird Ujverbasz zum Abtransport bereitgestellt. 219, 217 und ? Re. setzen 9.11 Marsch in Linie Nagybeskerek, Wergcheez fort.

## Parallel traffic and an additional interpretation

The previously reviewed [p170 B1/B2 and p166/p167 reports](nov9_operational_reports.md)
provide related earlier-part context and a near-identical second part. The
source headers differ: this p160 transmission is received on November 8,
while p170 B is received on November 9. The parallel does not identify the
missing physical first part of this particular p160 transmission.

Under the explicitly stated 238-slot p160 exclusion frame, its alignment
with p170 B2 has **230 known-coordinate agreements, six known disagreements
and two complementary masks**. P160 frame25 (literal source27) supplies X
where p170 has a mask, supporting the latter's proposed J in `UJVERBASZ`.
P170 frame183 supplies D where p160 source185 is a dash, supporting the
p160 fill in `BEREITGESTELLT`. These are conditional cross-witness supports;
all six disagreements remain recorded.

**Conditional interpretation:** substituting the parallel's `RD` and
`WERSCHETZ` for the primary `RE` and `WERGCHEEZ` costs **three additional
observed-coordinate substitutions** at p160 source18 D→X, source48 G→X
and source192 D→G. Its total is seven observed substitutions, one printed-mask
fill and two observed exclusions. This separately priced interpretation is
not substituted into the primary edited or readable stream above.

The [parallel certificate](../../experiments/nov8_radio_keys_and_reports/parallel_witnesses.json)
retains every source and plaintext difference, prior record identity and both
complete 5/6 key witnesses. The earlier operational case's historical unit
identification remains a separate context layer; no unknown digit is filled
in this source edition. No previously cataloged parallel is counted again.

## Shared uncertainty and credit

The two missing square cells `VF` and `XA` jointly contain `5` and `6`. Both complete assignments are retained as compatibility witnesses; every occurrence of a cell shares the same digit. The displayed `?` positions therefore must not be treated as independent digit choices. In p160 B2 one additional source coordinate remains unfilled; its domain can include letters as well as digits.

The published Nov7–9 period key and earlier OCR candidates are credited in the inputs. This edition adds source inspection, separate repair costs and exact readable-text mappings. It does not claim new recovery of the period key.
