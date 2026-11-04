# p132 A and C — An officer-register request and a garbled-message repeat

[Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p132 contains three separate records: a partly garbled request for
an officer-register extract, a conditional recovery of a repeat-transmission
instruction for Eilvese, and an exact request to repeat a garbled incoming
Caucasus message. The unchanged published `Nov4-6` key applies throughout.
The middle record has its own [canonical p132 case](../p132.md); A and C
have ordinary exact frames and remain separately catalogued physical sources.

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p132, PDF p135](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [full page](../../experiments/november_radio_service/sources/childs_p132_full.png)
is headed `5th NOVEMBER, 1918.`

## A: an officer-register request, with the name unresolved

The [A source](../../experiments/november_radio_service/sources/childs_p132_A.png)
has this header and exactly 242 slots, including one printed dash:

<details>
<summary>Source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
A) OSM v OUI (9.29 p.m., November 5th)
HIER 13 2207
RICHI-242
```

</details>

The raw 121-position reading fixes 120 positions:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
MILLTAEGMISZIONKOSJOIIXUEBERTENDUNGEILESKRIEGSRANGLI?TRNAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNNHEFPAFR53540X
```

</details>

Six observed-coordinate substitutions and one dash fill repair ordinary
words, giving:

<details>
<summary>Exact edited proposal</summary>

**Edited output:**

```text
MILITAERMISZIONKOSJOIIXUEBERSENDUNGEINESKRIEGSRANGLISTENAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNCHEFPAFR53540X
```

</details>

The readable clause is:

**Readable German — complete edited stream, with the literal addressee and name fields:**

> Militärmiszion `KOSJOII`. Übersendung eines Kriegsranglistenauszuges des `GENERALMAJRHYDEWALD`
> erbeten. Feldeisenbahnchef `PAFR53540`.

The readable quotation includes the entire opening `MILITAERMISZIONKOSJOII`. Its Z spelling and unresolved field remain literal; the six substitutions and one dash fill above are unchanged.

It requests an extract from a wartime officer register. **The addressee/place
field `KOSJOII` and the general-name field `GENERALMAJRHYDEWALD` remain
unresolved.** Neither is expanded into an identified person or place. The
raw `MISZION` spelling and `PAFR53540` footer also remain literal. This is a
partial source edition, not a securely identified personnel record.

## B: repeat the fourth-period telegram in the fifth

The complete source/model edition is consolidated in [canonical challenge
p132](../p132.md). That page combines Thomas’s initial fragment, Norbert’s
fuller sender-error reading and `VORHER` proposal, the later three-substitution
and two-erasure-fill account, and all four equivalent intermediate-`V`
positions. `p132_B` survives only as an identifier inside the frozen evidence
package; it is not a second catalogue entry.

## C: request to repeat a garbled incoming message

The [C source](../../experiments/november_radio_service/sources/childs_p132_C.png)
has this header:

<details>
<summary>Source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
C) NKJ v LP (7.45 p.m., November 6th)
FUER COS 2150 (5/11)
RICHI-198
```

</details>

The November 5 origin line and November 6 reception line are retained.
All 198 coordinates and all 99 plaintext labels are fixed without repair:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
KAUKASUSDELEGAXWIEDERHLGVERSTUEMMELTEINGEGXOSKACHIX54GRXSSX1912XANXNACHCHEFERBETENXNACHCHE5X150527X
```

</details>

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

A [separate address-spelling supplement](../../experiments/p132_optional_address/README.md) prices `KOSJOII` → `KOSPOLI` at two additional observed-coordinate substitutions and binds independent raw occurrences in p90, p98 and p148. This optional proposal leaves the primary streams and unresolved name above unchanged.
