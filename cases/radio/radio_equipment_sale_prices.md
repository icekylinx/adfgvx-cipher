# Radio apparatus sale and estimated value

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

The two source parts concern permission to sell apparatus and a value estimate of 80 to 90 percent. The readable edition retains abbreviations, 380L, 170M and the incomplete 21?00 field. It does not supply a currency, price separator or missing digit.

Source: Childs, printed pp.160–161 (PDF pp.163–164). [Source images and inputs](../../experiments/nov8_radio_keys_and_reports/inputs.json), [certificates](../../experiments/nov8_radio_keys_and_reports/certificates.json), [method and limitations](../../experiments/nov8_radio_keys_and_reports/README.md). All indices below are zero-based.

## p160 B1

Header: `B) NKJ v LP (06.32 a.m., November 9th); FUER UKS (8/11) 2000 2 TLE; 1 TL; RICHI-282`.

Native 282. AVVGD is read VV, not WW. Apparate/price abbreviations, 380L, 170M and 21?00 remain literal; no currency or amount normalization.

The source has **282 slots** (282 valid coordinates). The native model has 282 slots / 141 plaintext positions: 140 fixed raw, 140 fixed after the stated edits.

**Cost:** 1 observed-coordinate substitution; 0 printed-mask fills; 0 observed-coordinate exclusions; 0 mask exclusions; no inserted coordinates.

**Raw output** — native source frame:

```text
0KONACHX18DZU1A11023XAPPARATEVERKGENEHMVERKFSPREISSIEMENSX21?00FERNSCHREIBERX380LXTISCHGEHAEUSEX170MXXHIERVONZEITWERTNACHSCHAETZGXANRECHNENXX
```

**Edited output** — changes and source offsets are enumerated in the certificate:

```text
AKONACHX18DZU1A11023XAPPARATEVERKGENEHMVERKFSPREISSIEMENSX21?00FERNSCHREIBERX380LXTISCHGEHAEUSEX170MXXHIERVONZEITWERTNACHSCHAETZGXANRECHNENXX
```

**Readable German** — spacing, case, punctuation and conventional umlaut rendering only; all non-`X` labels match the edited output:

> Akonach. 18 D zu 1 A 11023. Apparateverk genehm. Verkfspreis Siemens. 21?00 Fernschreiber. 380 L. Tischgehäuse. 170 M. Hiervon Zeitwert nach Schätzg anrechnen.

## p160 B2

Header: `Same p160 B header; 2 TL; RICHI-84`.

Native 84 includes printed C at 8 and B at 83, both represented as source masks. C8 is filled; B83 remains unresolved.

The source has **84 slots** (82 valid coordinates). The native model has 84 slots / 42 plaintext positions: 39 fixed raw, 40 fixed after the stated edits.

**Cost:** 0 observed-coordinate substitutions; 1 printed-mask fill; 0 observed-coordinate exclusions; 0 mask exclusions; no inserted coordinates.

**Raw output** — native source frame:

```text
VERMU?LICH80BIS90PROZENTXNACHCHEF3C111?0?X
```

**Edited output** — changes and source offsets are enumerated in the certificate:

```text
VERMUTLICH80BIS90PROZENTXNACHCHEF3C111?0?X
```

**Readable German** — spacing, case, punctuation and conventional umlaut rendering only; all non-`X` labels match the edited output:

> Vermutlich 80 bis 90 Prozent. Nach Chef 3 C 111?0?.

## Shared uncertainty and credit

The two missing square cells `VF` and `XA` jointly contain `5` and `6`. Both complete assignments are retained as compatibility witnesses; every occurrence of a cell shares the same digit. The displayed `?` positions therefore must not be treated as independent digit choices. In p160 B2 one additional source coordinate remains unfilled; its domain can include letters as well as digits.

The published Nov7–9 period key and earlier OCR candidates are credited in the inputs. This edition adds source inspection, separate repair costs and exact readable-text mappings. It does not claim new recovery of the period key.
