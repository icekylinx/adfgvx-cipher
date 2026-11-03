# Radio service: Eilvese repetition and a garbled Caucasus message

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p132 contains three separate records: a partly garbled request for
an officer-register extract, a conditional recovery of a repeat-transmission
instruction for Eilvese, and an exact request to repeat a garbled incoming
Caucasus message. The unchanged published `Nov4-6` key applies throughout.
The middle record is genuinely odd in length and requires a separate
before-transposition error model; the other two have ordinary exact frames.

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p132, PDF p135](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [full page](../../experiments/november_radio_service/sources/childs_p132_full.png)
is headed `5th NOVEMBER, 1918.`

## A: an officer-register request, with the name unresolved

The [A source](../../experiments/november_radio_service/sources/childs_p132_A.png)
has this header and exactly 242 slots, including one printed dash:

```text
A) OSM v OUI (9.29 p.m., November 5th)
HIER 13 2207
RICHI-242
```

The raw 121-position reading fixes 120 positions:

```text
MILLTAEGMISZIONKOSJOIIXUEBERTENDUNGEILESKRIEGSRANGLI?TRNAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNNHEFPAFR53540X
```

Six observed-coordinate substitutions and one dash fill repair ordinary
words, giving:

```text
MILITAERMISZIONKOSJOIIXUEBERSENDUNGEINESKRIEGSRANGLISTENAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNCHEFPAFR53540X
```

The readable clause is:

> Übersendung eines Kriegsranglistenauszuges des `GENERALMAJRHYDEWALD`
> erbeten. Feldeisenbahnchef `PAFR53540`.

It requests an extract from a wartime officer register. **The addressee/place
field `KOSJOII` and the general-name field `GENERALMAJRHYDEWALD` remain
unresolved.** Neither is expanded into an identified person or place. The
raw `MISZION` spelling and `PAFR53540` footer also remain literal. This is a
partial source edition, not a securely identified personnel record.

## B: repeat the fourth-period telegram in the fifth

The [B source](../../experiments/november_radio_service/sources/childs_p132_B.png)
is marked with explicit urgency:

```text
B) LP v NKJ (6.13 p.m., November 5th)
SSD EILT SOFORT LOESEN 1410 (5)
RIZI-155
```

The printed length and manual transcription both give **155 slots**. There
are two printed dashes in group `XFF--`; all other coordinates are retained.
The direct odd-frame reading has 77 paired positions and one unpaired coordinate:

```text
FFEREILVESEXWIEDERHOLETT?LEGGWD3?MYMFLWF7MFFS7KFNT8RLTIWFWUAFQLL3F1QF7PZNMDQQ
```

The latter portion becomes readable under the opposite coordinate-pair
phase. The following **conditional model** produces the cleanest short
telegram wording: one extra `V` was present in the fractionated intermediate
stream before its 155-slot column transposition.

After undoing that original transposition, interim indices **54, 55, 56 and
57** are four identical consecutive `V` coordinates. Removing any one of
them gives the same 154-coordinate stream and this conditional raw reading:

```text
FFEREILVESEXWIEDERHOLETT?LEGRXVO?VIERTERPERIODEINFU1NFTERXGEBETSORHER5MINXVVV
```

Three observed-coordinate substitutions and two printed-dash fills give:

```text
FUEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUENFTERXGEBETVORHER5MINXVVV
```

Readable German, expanding only the telegram abbreviation in brackets:

> Für Eilvese. Wiederholet Telegr[amm] von vierter Periode in fünfter.
> Gebet vorher 5 Min. VVV.

It asks Eilvese to repeat the fourth-period telegram during the fifth period
and send **five minutes of `VVV`** beforehand. The old imperative forms
`WIEDERHOLET` and `GEBET` are preserved. The paper by Lasry and colleagues
separately identifies Eilvese and its OUI callsign in its discussion of
p120/p123; that supplies station context, not prior publication of this p132
body. [DOI 10.1080/01611194.2016.1169461, §6.5](https://doi.org/10.1080/01611194.2016.1169461)

### Exact costs and the four equivalent positions

| Received source index, zero-based | Printed group / position, one-based | Change | Effect |
| ---: | --- | --- | --- |
| 52 | 11 / 3 | `X` → `F` | `SORHER` → `VORHER` |
| 64 | 13 / 5 | `A` → `D` | `FFER` → `FUER` |
| 88 | 18 / 4 | `A` → `F` | `FU1NFTER` → `FUENFTER` |
| 103 | 21 / 4 | printed dash → `F` | Missing `E` in `TELEGR` |
| 104 | 21 / 5 | printed dash → `X` | Missing `N` in `VON` |

The raw numeral label `1` in `FU1NFTER` is retained in both raw readings.
Its change to `E` is an explicit local coordinate repair within a word; it
does not reassign the square's digit `1`. The numerical `5` in `5MIN` remains
unchanged.

The extra coordinate is separately charged as **one extraneous intermediate
coordinate**. It is not silently discarded from the received source. To
reproduce the 155-slot witness, encode the 77-character proposal, reinsert
the same `V` at the selected interim position, and apply the original rank
order. All four choices produce the same transmitted witness after the
five listed repairs/fills. Their differing source origins are retained in
the certificate; there is no uniquely identified extra `V`.

An initial insertion-only search retrieved the useful ending but left
`TELEGAR` or `TELERGR`. Those earlier candidates remain in the
[geometry audit](../../experiments/november_radio_service/geometry_audit.json).
The later extra-coordinate interpretation was selected after inspecting
the source and wording. All 156 one-insertion and 155 one-removal interim
positions are preserved. For this retrospective 77-character template,
the four identical-V removals uniquely form the minimum-cost set of three
substitutions and two dash fills. This is a conditional consistency result,
not independent proof of the historical mechanism.

## C: request to repeat a garbled incoming message

The [C source](../../experiments/november_radio_service/sources/childs_p132_C.png)
has this header:

```text
C) NKJ v LP (7.45 p.m., November 6th)
FUER COS 2150 (5/11)
RICHI-198
```

The November 5 origin line and November 6 reception line are retained.
All 198 coordinates and all 99 plaintext labels are fixed without repair:

```text
KAUKASUSDELEGAXWIEDERHLGVERSTUEMMELTEINGEGXOSKACHIX54GRXSSX1912XANXNACHCHEFERBETENXNACHCHE5X150527X
```

The message addresses the Caucasus delegation and asks for repetition of a
garbled incoming message to `NACHCHEF`. Its literal reference is
`OSKACHI 54GR SS 1912`; the footer is `NACHCHE5 150527`. Those abbreviations
and numerical labels, including the final `5` in `NACHCHE5`, remain as read.
No new numbering interpretation or silent spelling change is introduced.

## Source status and reproducibility

The [inputs](../../experiments/november_radio_service/inputs.json) preserve
manual rows, literal headers, key provenance and source-image hashes. The
[certificate](../../experiments/november_radio_service/certificates.json)
records the raw and conditional readings, all possible label domains,
coordinate origins and exact forward witnesses. A remains partly garbled
at its names; B remains conditional on the extra-coordinate model; C is an
unchanged direct reading.

The period key is prior work by **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also reproduced in George Lasry's [2017-02-24 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR-derived candidates existed. The bounded paper check
found no explicit p132 body example; no universal first-decipherment claim
is made.

```sh
python experiments/november_radio_service/verify.py --verify
python experiments/november_radio_service/geometry_audit.py --verify
```
