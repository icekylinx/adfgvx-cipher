# September radio listening and acknowledgment procedure

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Three source records on Childs printed p60 give a readable two-part instruction
to listen daily at previously stated times, followed by a separate request
to send radiograms continuously during reception of the Nauen press and
wait until afterward for acknowledgment. The unchanged published `Sep19-21`
key fixes **275 of 278 raw plaintext positions**. The readable edition uses
three observed-coordinate substitutions and four coordinate-erasure fills.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed p60, PDF p63](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [full source page](../../experiments/september_radio_procedure/sources/childs_p60_full.png)
is headed `21st SEPTEMBER, 1918.` All three transcribed lengths exactly match
their printed `RIZI` length markers. There is no inserted, deleted or moved
ciphertext coordinate.

## A1: daily listening times

The [first-part source](../../experiments/september_radio_procedure/sources/childs_p60_A1.png)
has this header:

**Source transcription — clear header and/or literal source record:**

```text
A) COS v NKJ (10.02 p.m., Sept. 21st)
1400 (21) 2 TLE
1 TL  RIZI-176
```

The 176 source slots include a printed noncoordinate `T` and `L`. Treating
both as erasures gives the following 88-position reading, with 86 positions fixed:

**Raw output:**

```text
BITTEVONHEUTEABTAEGLICHZUDENVONUNSINDIESSEITX22552255VOM14X14X9XRIZI286ANGEGEBE?ENZEITE?
```

Both unknown positions have the domain `1EGNPZ`. Filling both with `N`
gives the proposed first-part ending `ANGEGEBENENZEITEN`. The rest of the
plaintext remains exactly as received. In readable form, continued by A2:

**Readable German — first-part excerpt; the continuation is separate:**

> Bitte von heute ab täglich zu den von uns in diesseit. `22552255` vom
> `14X14X9`, `RIZI286`, angegebe[n]en Zeite[n] …

The exact repeated strings **`22552255`** and **`14X14X9`**, and the reference
**`RIZI286`**, are directly fixed by the received coordinates. They are
preserved here without collapsing the repetition or supplying a normalized
telegram number or date. The abbreviation `diesseit.` is retained rather
than expanded into an unprinted document description.

## A2: a call at the beginning of every period

The [second-part source](../../experiments/september_radio_procedure/sources/childs_p60_A2.png)
is marked `2 TL RIZI-154`. All 154 coordinates are valid, and all 77 plaintext
positions are read without repair:

**Raw output:**

```text
AUFUNSZUHOERENXXWIRRUFENZUBEGINNJEDERPERIODEAUCHWENNNICHTSVORLIEGTANXXNKJXNKJ
```

The complete readable instruction continues:

**Readable German — second-part continuation; the opening is in the separate first part:**

> … auf uns zu hören. Wir rufen zu Beginn jeder Periode, auch wenn nichts
> vorliegt, an. NKJ NKJ.

Thus A asks the recipient to listen for the sender daily at the referenced
times. The sender will call at the start of each period even when there is
no traffic. The repeated `NKJ` signature is retained. A1 and A2 are decrypted
as their own 176- and 154-slot frames before their prose is joined.

## B: traffic during reception of the Nauen press

The [B source](../../experiments/september_radio_procedure/sources/childs_p60_B.png)
has a separate clear service annotation above its encrypted body:

**Source transcription — clear header and/or literal source record:**

```text
B) ASO v NKJ (1.30 a.m., Sept. 21st)
2 TL RICHI-180 NV VON GFGGV BIS SCHLUSS WH 3 TL RICHI-126
VE 2100 (21)
RIZI-226
```

The annotation is retained literally. Its references to other parts are not
counted as additional recovered records or included in the cipher frame.
`NV`, `WH` and `VE` are left unexpanded. The reception and origin-line time
strings are preserved without silently resolving their chronology.

The 226-slot body has a printed dash and one damaged group-initial glyph.
The latter looks R/E-like and may be a damaged `F`; the conservative
transcription treats it as an erasure. Both erased coordinates feed the
same plaintext position. The raw reading therefore fixes 112 of 113 positions:

**Raw output:**

```text
RITTEFUNKSPRXFUERCOSANUNSWAEHRENDAUFNAHMENAUENPRESSEIMMEROHGEUNTYRBRECHUNGGEBENXXQUITTUNGFOLGTNACHPRESSE?CHLUSSXX
```

Three coordinate substitutions repair `RITTE`, `OHGE` and `UNTYRBRECHUNG`.
Two coordinate fills supply the missing `S` in `PRESSESCHLUSS`:

**Edited output:**

```text
BITTEFUNKSPRXFUERCOSANUNSWAEHRENDAUFNAHMENAUENPRESSEIMMEROHNEUNTERBRECHUNGGEBENXXQUITTUNGFOLGTNACHPRESSESCHLUSSXX
```

Readable German, with abbreviation and grammar expansions bracketed:

**Readable German:**

> Bitte Funkspr[üche] für COS an uns während Aufnahme [der] Nauen-Presse
> immer ohne Unterbrechung geben. Quittung folgt nach Presseschluss.

The instruction asks for radiograms intended for COS to be sent continuously
to the sender while it receives the Nauen press; the acknowledgment will
follow after the press transmission ends.

### Exact repair and erasure ledger

Source indices are zero-based; printed group and within-group positions are
one-based. The source images and certificate also record the printed row.

| Record | Source index | Printed group / position | Received glyph or coordinate | Proposal | Type | Effect |
| --- | ---: | --- | --- | --- | --- | --- |
| A1 | 39 | 8 / 5 | printed `T` | `D` | Erasure fill | `ZEITE?` → `ZEITEN` |
| A1 | 79 | 16 / 5 | printed `L` | `D` | Erasure fill | `ANGEGEBE?EN` → `ANGEGEBENEN` |
| B | 30 | 7 / 1 | damaged uncertain glyph | `F` | Erasure fill | First coordinate of the missing `S` |
| B | 87 | 18 / 3 | `X` | `D` | Substitution | `OHGE` → `OHNE` |
| B | 113 | 23 / 4 | `X` | `D` | Substitution | `RITTE` → `BITTE` |
| B | 173 | 35 / 4 | printed dash | `X` | Erasure fill | Second coordinate of the missing `S` |
| B | 221 | 45 / 2 | `D` | `G` | Substitution | `UNTYRBRECHUNG` → `UNTERBRECHUNG` |

Under the conservative transcription, B's unknown plaintext position has
all 36 square labels as its domain. A separate visual interpretation of the
[damaged glyph as F](../../experiments/september_radio_procedure/sources/childs_p60_B_uncertain.png)
restricts that domain to `8EHISY` and reduces the fill count by one. It leaves
the raw fixed-position count unchanged. The edition does not use the readable
word alone to certify that visual interpretation.

## Reproducibility, numerals and prior credit

The [inputs](../../experiments/september_radio_procedure/inputs.json) retain
all manual rows, glyph notes, exact headers, the published key and image
provenance. The [certificate](../../experiments/september_radio_procedure/certificates.json)
records every plaintext domain, both source-coordinate origins, each repair,
each fill and the complete re-encrypted witnesses. It counts the conditional
visual variant separately, so the corpus contribution is **three records**.

| Baseline quantity | Count |
| --- | ---: |
| Source slots / valid received coordinates | 556 / 552 |
| Raw fixed plaintext positions | 275 / 278 |
| Proposed positions supported by unchanged complete pairs | 272 / 278 |
| Valid-coordinate substitutions / erasure fills | 3 / 4 |
| Insertions, deletions, block moves or square changes | 0 |

The published `Sep19-21` key is credited to **George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
and to George Lasry's [2017-02-24 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR-derived candidates existed. This edition contributes
manual source checking, exact frame recovery and repair accounting using
that prior key; it makes no universal first-decipherment claim.

Exact re-encryption establishes arithmetic consistency and the stated costs.
Editorial repairs, fills and abbreviation expansions remain distinct from
direct readings. The raw numerical labels are preserved rather than assigned
additional historical meaning.

```sh
python experiments/september_radio_procedure/verify.py --verify
```
