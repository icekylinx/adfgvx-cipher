# Request for replies and radio priority

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

This two-part telegram asks the Foreign Office in Berlin for replies to
three earlier messages and for brief instructions in plaintext. It then
suggests explicitly telling the radio station to send these telegrams
before others, because military telegrams apparently receive priority.
The signature is the literal `HORSTMANN`; no historical identity is assigned
from the name alone.

Both printed frames are complete: **226 and 282 slots**, under the unchanged
published `Nov4-6` key. Six observed-coordinate substitutions and seven
printed-dash fills give the readable edition. No coordinate is inserted,
removed or reordered, and no square cell is changed.

## Source and the first part

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p128, PDF p131](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [full page](../../experiments/radio_telegram_priority/sources/childs_p128_full.png)
is headed `5th NOVEMBER, 1918.` The shared header is:

**Source transcription — clear header and/or literal source record:**

```text
A) LP v NKJ (7.01 p.m., November 5th)
1130 (5) 2 TLE
```

The [first part](../../experiments/radio_telegram_priority/sources/childs_p128_A1.png)
is labeled `1 TL RICHI-226`. All 226 coordinates are valid and fix all
113 raw plaintext positions:

**Raw output:**

```text
AUSWAERTIGBERLINNUMMER597XANTWORTAUFTELEGRAMME569X592UND598BISHERNICHTEINGETROFFENXZURZEWEISUNGINKLARTEXTERBETENX
```

One coordinate substitution changes `ZURZE` to `KURZE`:

**Edited output:**

```text
AUSWAERTIGBERLINNUMMER597XANTWORTAUFTELEGRAMME569X592UND598BISHERNICHTEINGETROFFENXKURZEWEISUNGINKLARTEXTERBETENX
```

Readable German:

**Readable German:**

> Auswärtig Berlin. Nummer 597. Antwort auf Telegramme 569, 592 und 598
> bisher nicht eingetroffen. Kurze Weisung in Klartext erbeten.

The telegram says that replies to messages **569, 592 and 598** have not
yet arrived and requests brief instructions in plaintext. The message
number **597** and all three references are unchanged labels from the
published square; the edition does not infer a chronology from their order.
The source's `AUSWAERTIG` remains an abbreviation, without inserting an
encoded `AMT` into the plaintext.

## Second part: proposed radio precedence

The [second part](../../experiments/radio_telegram_priority/sources/childs_p128_A2.png)
is labeled `2 TL RICHI-282`. It contains exactly 282 printed slots, including
seven dashes. Its ordinary source frame fixes 134 of 141 positions:

**Raw output:**

```text
ANH9IMGRSTELLTFDNKENSTATIONAUSDRUEK?IC7?NZUHEISENXTELEGRAMMEVORALLENANDERENZUGEBENXD?SCHEINBAR?ILITAER?SCHETELE?RAMME?EVORZUGTWERDNXHORSTMANN
```

Five observed-coordinate substitutions and seven dash fills give:

**Edited output:**

```text
ANHEIMGESTELLTFUNKENSTATIONAUSDRUEKLICHANZUWEISENXTELEGRAMMEVORALLENANDERENZUGEBENXDASCHEINBARMILITAERISCHETELEGRAMMEBEVORZUGTWERDNXHORSTMANN
```

Its meaning is: it is suggested that the wireless station be explicitly
instructed to send these telegrams before all others, because military
telegrams apparently receive preferential treatment. This is a suggestion
to the recipient, not evidence that such an instruction had already been
issued or obeyed.

The literal spellings **`AUSDRUEKLICH`** and **`WERDN`** remain in the edition.
No additional plaintext `C` or `E` is claimed. The signature `HORSTMANN`
already appears unchanged in the raw reading.

An earlier OCR extraction supplied only 281 slots. Manual source review
establishes the advertised 282-slot frame. This is an OCR transcription
correction and supplies no evidence for a historical before-transposition
coordinate loss.

## Exact coordinate costs

All source indices below are zero-based. Printed group numbers and positions
are one-based and counted separately within each part.

| Part | Source index | Printed group / position | Change | Plaintext effect |
| --- | ---: | --- | --- | --- |
| A1 | 156 | 32 / 2 | `V` → `F` | `ZURZE` → `KURZE` |
| A2 | 0 | 1 / 1 | `X` → `A` | Raw `9` → `E` within `ANHEIM` |
| A2 | 121 | 25 / 2 | `G` → `F` | `ZUHEISEN` → `ZUWEISEN` |
| A2 | 183 | 37 / 4 | `V` → `F` | `GRSTELLT` → `GESTELLT` |
| A2 | 184 | 37 / 5 | `F` → `V` | `FDNKEN` → `FUNKEN` |
| A2 | 203 | 41 / 4 | `D` → `G` | Raw `7` → `H` within `AUSDRUEKLICH` |

The seven A2 dash fills, separately charged, are:

| Source index | Printed group / position | Filled coordinate | Proposed plaintext label |
| ---: | --- | --- | --- |
| 26 | 6 / 2 | `F` | `A` in `DA` |
| 54 | 11 / 5 | `V` | `A` in `ANZUWEISEN` |
| 79 | 16 / 5 | `V` | `B` in `BEVORZUGT` |
| 129 | 26 / 5 | `V` | `G` in `TELEGRAMME` |
| 160 | 33 / 1 | `X` | `M` in `MILITAERISCHE` |
| 161 | 33 / 2 | `X` | `I` in `MILITAERISCHE` |
| 220 | 45 / 1 | `X` | `L` in `AUSDRUEKLICH` |

The raw numerical labels `9` and `7` in damaged A2 words remain visible in
the raw reading and the numerical ledger. Their proposed changes are local
coordinate substitutions. They do not alter the square's digit assignments.
Every actual A1 numerical reference remains unchanged.

## Verification and attribution

The [inputs](../../experiments/radio_telegram_priority/inputs.json) preserve
the exact headers, manual groups, key provenance and image hashes. The
[certificate](../../experiments/radio_telegram_priority/certificates.json)
retains every raw domain, source-coordinate origin, repair, dash fill,
numerical label and full forward witness. The standard-library verifier
independently undoes the transposition and rebuilds both witnesses:

```sh
python experiments/radio_telegram_priority/verify.py --verify
```

The period key is prior work by **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also reproduced in George Lasry's [2017-02-24 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR-derived candidates existed. The bounded author-paper
check found no explicit p128 A body example; that does not establish
universal first-decipherment priority. Exact re-encryption certifies the
stated arithmetic and repair prices, not unique historical wording.
