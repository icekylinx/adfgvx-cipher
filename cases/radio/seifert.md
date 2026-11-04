# Station control and the Seifert service exchange

[ADFGVX Cipher](../../README.md) · [All cases](../README.md) · [Source certificate](../../experiments/p170_continuation/seifert_records.json) · [Reading conventions](../../docs/reading-conventions.md)

**Nine source records, seven message groups.** The November 7–9 and November 10–12 published keys recover a sequence of radio-station reports and short service messages. Two pairs are repeated transmissions. These records are outside the original 22-entry challenge; the open p170 challenge is section **A**, not any of these neighboring records.

Source transcription, cipher checks and editorial work: **icekylinx and GPT-6 Astra Pro**. The station-control interpretations of p168 A and B were already published by **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**; their author manuscript discusses both on printed p. 23 / PDF p. 24. The keys retain their recorded historical and modern provenance. This page provides a source-level edition, without claiming a first historical decipherment.

## Conditional shared digits

The paired monitoring orders each gain their hundreds digit: **500**. Both physical receptions have the same complete ciphertext; repetition preserves the value once the shared square is interpreted. No source coordinate is changed. The [joint reconstruction](../../experiments/nov10_joint_completion/README.md) combines the earlier Marineamt and formation interpretations with the army-number constraint and the mobilization decree; the reversed 7/9 assignment is retained there.

**Conditional interpretation — readable German under the joint square:**

> Sofort US 500 hoeren.

<details>
<summary>Exact conditional labels</summary>

**Edited output — p172_B, conditional shared square; 20/20 fixed positions:**

```text
SOFORTXUSX500XHOEREN
```

**Edited output — p174_D, conditional shared square; 20/20 fixed positions:**

```text
SOFORTXUSX500XHOEREN
```

</details>


## Read the messages

The prior body credit for p168 A also applies to its repeated content at
**p169 A**. Identification of the repeat, its exact coordinate differences,
and the present source edition remain our contribution.

Square brackets mark supplied letters or abbreviation expansions. Punctuation, capitalization and word spacing are editorial.

| Source | Readable German | Meaning and exact qualification |
|---|---|---|
| **p168 A**; repeated with errors at **p169 A** | Stehe ab 2200 unter Aufsicht Sol[d]atenrats. Stat[ion und] Personal fest in meiner Hand. Betrieb unverändert. Seifert. | From 22:00 the sender is under the soldiers' council's supervision; station/personnel remain firmly under his control and operation is unchanged. All 92 raw positions of p168 A decode exactly; the source spells `SOLATENRATS` without `D`. The connecting words in the `STATPERSONAL` expansion are editorial. |
| **p168 B** | Soldatenrat Cöln wird bald Funkstelle besetzen. Versucht schon Funksprüche aufzugeben. | Cologne's soldiers' council is expected to occupy the radio station and is already trying to submit radio messages. The raw text has `SOLDATENRA9` and `SCKON`; the readable version requires two explicit coordinate substitutions. |
| **p172 A** | Akten [s]ämtlich vernichtet. Schlüssel in pers[önlicher] Obhut noch vorhanden. Seifert. | All records have been destroyed; the cipher keys remain in personal custody. The source fixes 67/68 plaintext positions. One invalid printed glyph leaves the initial letter of `SAEMTLICH` unresolved; `S` is a supported reading, not a source-observed letter. |
| **p174 B** | Wenn Seifert eingetroffe[n], bitte Nachr[icht]. TOF. | Please report when Seifert has arrived. The source fixes 36/37 positions. One doubtful glyph permits `N`; a `G` interpretation of that glyph instead produces separator `X` after the raw spelling `EINGETROFFE`. `TOF` is not expanded. |
| **p174 C** | Wann Rückkunft Seifert? RE. | When will Seifert return? All 24 plaintext positions decode exactly. `RE` remains unexpanded. |
| **p172 B / p174 D** | Sofort US ?00 hören. | An immediate listening instruction. The two 40-coordinate copies are identical. The unknown hundreds digit can be **5, 6, 7, 8 or 9** under a globally consistent completion of the published square. The role of `US` and the units of the number are not established. |
| **p174 E** | Seifert abgefahren. RENTE. | Seifert has departed. The raw text is `SQIFQRTABGEFAHRENXRENTE`; restoring the name requires two explicit `G → X` coordinate substitutions. `RENTE` is retained literally. |

The shared surname connects the service records, but the surviving headers do not establish Seifert's full name or a complete itinerary. The printed time expressions are preserved in the certificate, including the anomalous `17.28 p.m.` in p174 E. The day digit in p172 B is overtyped; the identical p174 D copy is explicitly dated 12 November.

## Raw decipherments

The table above does not overwrite these source-derived strings.

### p168 A — 184 coordinates / 92 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
STEHEAB2200UNTERAUFSICHTSOLATENRATSXSTATPERSONALFESTINMEINERHANDXBETRIEBUNVERAENDERTXSEIFERT
```

</details>

No cipher correction is required. Supplying `D` in `Soldatenrats` and expanding `STAT` are editorial reading choices only. The source is available in the [p168 A/B excerpt](../../sources/excerpts/childs_p168_AB.png).

### p168 B — 160 coordinates / 80 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
SOLDATENRA9XCOELNXWIRDBALDFUNKSTELLEBESETZENXVERSUCHTSCKONFUNKSPRUECHEAUFZUGEBEN
```

</details>

At zero-based ciphertext positions **89** and **141**, `F → V` and `G → X` give `SOLDATENRAT` and `SCHON`. The other **158 coordinates remain unchanged**. These are proposed source emendations, not alternative square assignments.

### p172 A — 136 slots / 68 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
AKTEN?AEMTLICHVERNICHTETXSCHLUESSELINPERSOBHUTNOCHVORHANDENXXSEIFERT
```

</details>

The [source](../../sources/excerpts/childs_p172_AB.png) prints `DAAGC`: its final `C` is outside the ADFGVX alphabet and becomes one erasure at ciphertext position **119**. The plaintext domain at position **5** is exactly `{F,I,K,N,O,S}`. Filling that coordinate with `G` gives `S` and preserves all **135 valid received coordinates**. `PERSOBHUT` is retained; the readable expansion is *pers[önlicher] Obhut*.

### p174 B — 74 slots / 37 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
WENNSEIFERTEINGETROFFE?BITTENACHRXTOF
```

</details>

The [source excerpt](../../sources/excerpts/childs_p174_BCDE.png) shows a `C`-like or defective `G` glyph at the start of group `CVXXF`, ciphertext position **20**. Its conservative analysis is `?VXXF`. The uncertain plaintext position **22** has domain `{1,5,6,7,8,9,E,N,V,X}`.

The readable `N` completion uses **D** at the source erasure and preserves all **73 certain coordinates**. Reading the doubtful glyph as **G** instead gives:

**Conditional interpretation — alternate G reading of the doubtful source glyph:**

```text
WENNSEIFERTEINGETROFFEXBITTENACHRXTOF
```

Within that single-source analysis, both alternatives are retained; the complete word `EINGETROFFEN` is an editorial inference.

An independent [p183 B witness](nov12_arrival_departure_and_car.md#p183-b)
now supplies observed `D` at source index 20 and therefore `N` at plaintext
position 22. Together the two conservative source transcriptions support
every target pair. The original C/G-like appearance and its G-reading
alternative remain in the earlier certificate and source analysis above.

### p174 C — 48 coordinates / 24 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
WANNRUECKKUNFTSEIFERTXRE
```

</details>

No glyph change, erasure fill, square completion or length repair is needed.

### p172 B / p174 D — 40 coordinates / 20 positions each

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
SOFORTXUSX?00XHOEREN
```

</details>

Both copies have the same ciphertext. All 40 coordinates are legible; the unknown digit comes solely from an unassigned cell in the published November 10–12 square. The verifier constructs a full bijective square witness for **each** candidate digit 5–9. The duplicate therefore confirms the transmitted coordinates but does not select a digit.

### p174 E — 46 coordinates / 23 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
SQIFQRTABGEFAHRENXRENTE
```

</details>

Changing ciphertext positions **2** and **28** from `G` to `X` gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
SEIFERTABGEFAHRENXRENTE
```

</details>

The other **44 coordinates remain unchanged**. The two corrections restore the same name directly present in the surrounding service traffic; the original `Q`s remain part of the raw edition.

The [p183 C witness](nov12_arrival_departure_and_car.md#p183-c) supports `X`
at source index 2, directly corroborating the second `E` of the name. Both
witnesses retain `G` at source index 28, so the first `E` remains a
separately priced contextual repair in each. The joint complete-name
proposal costs three observed-coordinate substitutions.

## The p169 A repeat

[p169 A](../../sources/excerpts/childs_p169_A.png) carries the same `SY v GK`, `2000` and `RICHI-184` metadata as p168 A, with a later intercept time. It prints **185 coordinates**, including the six-character group `DGDGGX`.

Deleting either adjacent `G` at zero-based source position **158** or **159** gives the same 184-coordinate conditional layer and this raw decipherment:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional deletion of source 158 or 159; equivalent aliases retained:**

```text
STEHEAB2200UNTEYAUFSICHTSOLATENRATWXSTATPERSONALFESTINMEIKERHANDXBETRIEBUNVERAENDURTXSEIFERT
```

</details>

It supports the repeated-message identification but is less clean than p168 A. Both deletion aliases are recorded. The untouched odd-length source is retained and is never silently decoded after dropping its last coordinate.

## Evidence and reproduction

The [certificate](../../experiments/p170_continuation/seifert_records.json) contains all nine literal source transcriptions, original headers, partial keys, raw plaintext domains, cropped-image hashes and exact proposed edits. It applies the already published keys; no unknown square cell is fixed by the prose.

```sh
python experiments/p170_continuation/verify_seifert.py
python experiments/p170_continuation/verify_seifert.py --json
```

The independent verifier checks **913 source slots**, every source-preserving fill, the four explicit coordinate substitutions, the p169 deletion aliases, both identical service copies, and all five globally attainable digit readings. A local copy of the source PDF can additionally be bound by SHA-256 with `--pdf /path/to/childs.pdf`.

### Sources and priority

- **J. Rives Childs collection:** printed pp. 168, 169, 172 and 174; PDF pp. 171, 172, 175 and 177 in the [public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The certificate retains its hash and the exact section headers.
- **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker:** *Deciphering ADFGVX messages from the Eastern Front of World War I*, [author manuscript](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf), printed p. 23 / PDF p. 24. This earlier work explicitly identifies the p168 A/B station-control reports; it also credits Childs's wartime decipherment of the Cologne message. The present edition does not reassign that priority.
- **Published keys:** [key catalog](../../data/keys.json), entries `Nov7-9` and `Nov10-12`, retaining original table and solver provenance.
