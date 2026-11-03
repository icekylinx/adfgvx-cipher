# November 27: Helsingfors shipping and a vehicle-sale instruction

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Two source records on Childs p223 describe ships secured for Helsingfors
and an instruction addressed through General von Kress to sell trucks and
surplus material. The first uses its native printed frame. The second has
five surplus source slots relative to its questioned length label and is
read under an explicitly priced exclusion model. Both use the unchanged
published **Nov25–28** key, credited to George Lasry and collaborators.

| Record | Printed slots | Analysis-frame slots | Fixed raw positions | Additional reading proposal |
|---|---:|---:|---:|---|
| p223 B | 246 | 246, native | 123/123 | 7 observed-coordinate substitutions |
| p223 C | 235 | 230, conditional exclusion | 113/115 | 2 source-mask fills; no substitution of a retained observed coordinate |

For C, the **five excluded observed coordinates** remain part of the repair
price. They are not counted as a free transcription correction or a visibly
cancelled group. The [reviewed source image — source-PDF reference](../../experiments/nov27_ships_and_vehicle_sale/inputs.json)
retains both messages and their distinct headers.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## p223 B

**Source transcription — literal header:**

```text
B) KOW v RVA (09.25 p.m., November 27th)
1835 (11/27) AN LP v FHR
RICHI-246
```

**Raw output — native 246-slot frame; 123/123 fixed positions:**

```text
ZENIRALFUNKLEITUNGXXELLEXVORBEREIT0GGENXGETRIFFENXSCHIFFEXNACZXMITTEILUNGXREICHSMARINEAMTSXSICHERGESTELLTXXFUSTAHBLSINGFORS
```

**Edited output — seven observed-coordinate substitutions; no fills; 123/123 fixed positions:**

```text
ZENTRALFUNKLEITUNGXXALLEXVORBEREITUNGENXGETROFFENXSCHIFFEXNACHXMITTEILUNGXREICHSMARINEAMTSXSICHERGESTELLTXXFUSTAHELSINGFORS
```

The changes, at zero-based source indices, are **12 F→D**, **56 D→A**,
**78 F→D**, **130 A→X**, **160 F→V**, **165 D→A** and **202 A→D**.
They repair `ZENIRAL`, `ELLE`, `VORBEREIT0GGEN`, `GETRIFFEN`, `NACZ` and
`HBLSINGFORS`. No published square cell changes.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Zentralfunkleitung. Alle Vorbereitungen getroffen. Schiffe nach Mitteilung Reichsmarineamts sichergestellt. Fusta Helsingfors.

The message reports that preparations have been made and ships secured,
according to the Reichsmarineamt. It does not report that troops have
embarked or arrived. The earlier
[Helsingfors transport inquiry](p210_A.md)
belongs to the wider radio record; no absent reference number is supplied to
identify this as a particular reply.

The source has all **246** coordinates. Earlier OCR retained only **239**:
it omitted the final visible `GVGVF D` and malformed another group. Restoring
the actually printed groups repairs the machine transcript without adding
historical coordinates or altering the native frame.

## p223 C

**Source transcription — literal header:**

```text
C) COS v NKJ (------- November 28th)
POT FUER COS GENERAL VON KRESS 1555 (11/27)
RICHI-230?
```

The header retains both the November 28 reception date and the internal
November 27 date. Its question mark after **230** is part of the length
annotation. The source actually prints **235 body slots**, including two
dashes in `DXX--` and these adjacent final-row groups:

**Source transcription — final four groups, excerpt:**

```text
DDFDD GAFDG GDFDG XGGAV
```

The primary analysis excludes the five observed coordinates **`GAFDG` at
source indices 220–224**. The source does not clearly mark that group as
cancelled. This is therefore an explicit conditional source exclusion, with
the original sequence retained in full.

**Raw output — conditional 230-slot frame after the five-coordinate exclusion; 113/115 fixed positions:**

```text
AUFBEFEHLHEERESGRUPPEALLELASTAUTOSS?WIEALLESUE?ERFLUESSIGEMATERIALWEGENUNMOEGLICHKEITABTRANSPORTSVERKAUFENXXBXMXKXX
```

**Edited output — same conditional exclusion; two source-mask fills and no observed-coordinate substitution; 115/115 fixed positions:**

```text
AUFBEFEHLHEERESGRUPPEALLELASTAUTOSSOWIEALLESUEBERFLUESSIGEMATERIALWEGENUNMOEGLICHKEITABTRANSPORTSVERKAUFENXXBXMXKXX
```

Filling the printed dashes at **source indices 83 and 84** with **D** and
**A** supplies the O in `SOWIE` and the B in `UEBERFLUESSIGE`. All retained
observed coordinates are unchanged. The five excluded valid coordinates
remain separately charged.

**Readable German — complete edited stream under the conditional exclusion model:**

> Auf Befehl Heeresgruppe alle Lastautos sowie alles ueberfluessige Material wegen Unmoeglichkeit Abtransports verkaufen. B M K.

The source header addresses General von Kress; the decoded body orders a
sale because transport is impossible. It does not identify the army group
more precisely or report that a sale occurred. The signature-like **`B M K`**
comes from literal **`BXMXKXX`**, with separators spaced and no expansion.

### The two equivalent source alignments

Against this exact 115-position candidate, the verifier checks every one of
the **231 consecutive five-slot exclusions** from the 235-slot source.
There are exactly two windows with no substitution of a retained observed
coordinate:

| Exclusion start, zero based | Excluded source letters | Result |
|---:|---|---|
| 220 | `GAFDG` | Retains the displayed 230-slot stream |
| 221 | `AFDGG` | Retains exactly the same 230-slot stream |

The overlap is possible because the G at either end of that six-coordinate
region can survive. Both alignments give the same raw output and the same
complete repaired ciphertext, but their retained source-coordinate maps
are different. Both maps and all 231 prices are stored in the
[certificate](../../experiments/nov27_ships_and_vehicle_sale/certificates.json).
This is a comparison conditioned on the stated plaintext and one exclusion
family, not proof of a unique historical error mechanism. The untouched
235-slot decode and its unpaired final coordinate remain in the certificate.

## Evidence and verification

[Source inputs](../../experiments/nov27_ships_and_vehicle_sale/inputs.json) ·
[Certificates](../../experiments/nov27_ships_and_vehicle_sale/certificates.json) ·
[Reproduction notes](../../experiments/nov27_ships_and_vehicle_sale/README.md).

```sh
python experiments/nov27_ships_and_vehicle_sale/verify.py --verify
python experiments/nov27_ships_and_vehicle_sale/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check compares the inspected crop with the identified
original's RGB pixels. The verifier checks independent transposition
offsets, every raw domain and repair, both source alignments, exact
re-encryption and the complete readable-label mappings. Earlier OCR,
recomputed comparison outputs and published period-key credits remain
separate from this source review. No universal first-decipherment priority
is asserted.
