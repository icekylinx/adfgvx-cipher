# November 9 operational reports: Serbian cavalry and the retreat north

[ADFGVX Cipher](../../README.md) · [All cases](../README.md) · [Source certificate](../../experiments/p170_continuation/military_records.json) · [Reading conventions](../../docs/reading-conventions.md)

The three-part report on p166 and two-part report p170 B describe Serbian cavalry entering towns, German formations marching north and preparations to transport the Alpenkorps. Our comparison with the p167 reception restores the **twenty-coordinate prefix** missing from p166 part 3 and recovers its order footer. The readings use the published **Nov7–9** key.

## Read the reports

The German readings follow the edited witnesses. Brackets mark the expansions, repairs and unresolved numeral explained below.

### p166 A, with its p167 A continuation

**Readable German — the stated edited witness, with the linked 5/6 cell left unresolved:**

> O.H.L., O.P. Lage 11. Armee, 8.11., abends: Serb[ische] Kavallerie [in] Peterwardein und Fehertemplom eingerückt.
>
> Abmarsch 217. I.D. und **[5. oder 6.] R.D.** nach Norden ohne Feindberührung. Alpenkorps wird Umverbasz (Fragezeichen) zum Abtransport bereitgestellt.
>
> 219., 217. und **[5. oder 6.] R.D.** setzen 9.11. Marsch in Lin[i]e Nagybeskerek–Werschetz fort. O.K.M., 1a, No. 11319 op.

**Meaning.** An evening situation report describes Serbian cavalry entering Peterwardein and Fehertemplom. The 217th Infantry Division and a reserve division are marching north without enemy contact. The Alpenkorps is being assembled for onward transport at a place transmitted as `UMVERBASZ`, followed by the literal word `FRAGEZEICHEN` (“question mark”). The 219th and 217th divisions and the same reserve division continue their march on 9 November along the Nagybeskerek–Werschetz line. The footer is retained as `O.K.M., 1a, No.11319 op.`

The p170 parallel supports the conditional place reading **Ujverbasz**. The reserve-division numeral remains **5/6** in the key; the historical comparison below supports **6th Reserve Division**.

### p170 B, parts 1 and 2

**Readable German — the stated edited witness and prose-only additions identified below:**

> Aben[d]meldung: Serb[ische] Kavallerie [in] Peterwa[r]dein und Fehertemplom eingerückt. Abmarsch 217. I.D. und **[5. oder 6.] R.D.** nach Norden ohne Fein[d]berührung.
>
> Alpenkorps wird U[j]verbasz zum Abtransport bereitgestellt. 219., 217. und **[5. oder 6.] R.D.** setzen 9.11. Marsch in Linie Nagybeskerek–Werschetz fort.

**Meaning.** This reception repeats the operational account and directly confirms **217**, **219** and the onward-march date **9.11**. Its proposed J in `UJVERBASZ` fills an erasure; other bracketed letters expand the prose. The two cipher frames retain 118 and 119 positions.

| Display form | Editorial category | What remains separate |
|---|---|---|
| `Serb[ische]` | Abbreviation expansion | The extra prose letters are not encoded positions. |
| `[in]` | Supplied grammar | The exact streams do not acquire a new word. |
| `Aben[d]meldung`, `Peterwa[r]dein`, `Fein[d]berührung`, `Lin[i]e` | Prose-only spelling normalization | The same-length edited witnesses still retain their missing letters. |
| `U[j]verbasz` | Priced source-erasure fill | J is a candidate coordinate fill, not an abbreviation expansion. |
| `[5. oder 6.]` | Linked key-cell alternatives | Every occurrence uses the same unresolved cell; the choices are not independent. |

## Historical identification: most likely the 6th Reserve Division

General Franchet d'Esperey's telegram **5.956/3**, sent from Salonique to Clemenceau and Foch on **19 November 1918 at 22:40**, describes the situation on **11 November**. Its paragraph on the reconstituted German 11th Army names the Alpenkorps, the 217th and 219th divisions around Nagy-Backskerek–Verschatz, and explicitly the **6th Reserve Division**. The relevant short passage reads: “217° — 219° D.I. Nagy-Backskerek—Verschatz) 6° D.I. réserve”. The matching formations and geography support the same identification in these German reports of 9 November; the French telegram is two days later in its reported situation and ten days later in transmission.

The telegram appears as document 39, pp79–82, in *Documents diplomatiques français sur l'histoire du Bassin des Carpates, 1918–1932*, vol. I (1993). [Source PDF, p153](https://real-eod.mtak.hu/19844/13/documents.pdf).

The retrospective battle calendar *Ruhmeshalle unserer alten Armee*, vol. I, fifth revised edition, places the 6th Reserve Division on the return march from the Balkans through Hungary from 6 November (p385). It places the 5th Reserve Division at the Antwerp–Meuse position on 5–11 November (p382). [Calendar extract, PDF pp43 and 46](https://denstorekrig1914-1918.dk/wp-content/uploads/2021/05/Ruhmeshalle_unsere_alten_Armee_5_Aufl_Bd-1_s_342-497s.pdf).

<details>
<summary>Bibliographic details and earlier use of the sources</summary>

The French document collection is vol. I, *Octobre 1918 – Août 1919*, collected by Magda Ádám, György Litván and Mária Ormos, edited by Ádám, Akadémiai Kiadó, Budapest, 1993, ISBN 963 05 6659 1. The telegram's archival reference, printed on p82, is **AG.4N58 c/63. d/10.** [Library catalogue](https://real-eod.mtak.hu/19844/).

The battle-calendar extract is the fifth revised edition, Verlag für Militärgeschichte und deutsches Schrifttum, Berlin/Fürstenwalde; its publication year is absent from the extract. This later compilation from official archival material is distinct from the contemporary telegram.

Both sources were previously reviewed for [p176b](../../data/reviews/p176b_unit_context.json). Their application here concerns the separate **Nov7–9 square** and the newly edited p166/p167/p170 B reports.

</details>

The [context certificate](../../experiments/p170_continuation/military_context.json) records the consequences separately:

| Layer | Reserve-division digit | Effect on the ciphertext |
|---|---|---|
| Published partial square and cipher arithmetic | `5` or `6`, at cell `VF` | Both alternatives retain exact global witnesses. |
| Historical identification supported by the French telegram | **`6`** at `VF`; consequently `5` at the other unused cell `XA` | **Zero additional coordinate edits** in each of the four readable frames. |

The historical identification selects one shared cell in four occurrences. Both complete squares remain exact cipher witnesses, and the [published key](../../data/keys.json) retains its unresolved domain. Applying the preferred value elsewhere therefore carries the same historical assumption.

## The recovered prefix

| Witness | Header length | Printed slots | Source observation |
|---|---:|---:|---|
| **p166 A3** | 204 | 184 | The first four five-coordinate groups are absent from this copy. |
| **p167 A3** | 204 | 204 | The beginning survives; one later coordinate is erased. Terminal cleartext `NKJ` is separate service metadata. |

The p167 copy begins:

<details>
<summary>Literal source transcription</summary>

**Source transcription:**

```text
ADFVF DDDVX DGVDD XVDAF
```

</details>

Its following 184 slots align with the complete p166 A3 fragment: **179 known matches, four known disagreements and one erasure**. Among all **21 contiguous placements** of the 184-slot fragment in the 204-slot copy, this offset 20 placement uniquely minimizes known-coordinate disagreements. The next-best placement has 136 disagreements.

Prepending those **20 observed source coordinates** to p166 A3 preserves every one of its **184 received coordinates** and restores the advertised frame. It decrypts to:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional prefix placement from p167; all p166 observed coordinates retained:**

```text
BEREITGESTELLBX219XX217XUND?XLXDXSETZSN9X11XMARSCHINLINENAGYBESKEREKXWERSCHETZFORTXOXKXMX1AXNO11319OPX
```

</details>

The restored frame fixes **101 of 102 positions**, with its source errors retained. The question mark is the globally shared **5/6** square ambiguity.

Keeping both source values at every known disagreement gives a more conservative combined template with **97/102 singleton positions**:

**Conditional interpretation — joint source constraints; disagreements retained:**

```text
BEREITGESTELL?X219XX217XUND?X?XDXSETZSN?X11XMARSC?INLINENAGYBESKEREKXWERSCHETZFORTXOXKXMX1AXNO11319OPX
```

| Plaintext position, zero-based | Source-supported domain |
|---:|---|
| 13 | `B` or `T` |
| 27 | `5` or `6` |
| 29 | `2` or `L` |
| 39 | `5`, `6` or `9` |
| 49 | `H` or `W` |

Choosing the p167 value at full-frame coordinate **41** gives `BEREITGESTELLT`; using the p166 values in the later damaged group gives `9.11` and `MARSCH`. That source-supported composite still has `L.D.` and `SETZSN`. The readable `R.D.` / `SETZEN` reconstruction makes **two additional explicit coordinate substitutions**. Against the separate original witnesses, the total cost is:

- **p166 A3:** the observed 20-coordinate prefix, plus **three substitutions** among its 184 retained coordinates.
- **p167 A3:** **four substitutions and one erasure fill** among its 204 slots.

`Lin[i]e` expands the transmitted `LINE` in prose only.

## All six raw readings

### p166 A1 — 174 coordinates / 87 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
OXHXLXOXPXLAGE11XARMEE8X11HABENDSXSERBXKAVALLERIEPETERWARDEINUNDF3HERTEMPLOMEINGSRUECKT
```

</details>

The readable same-length edition uses three coordinate substitutions for the anomalous `H` after `8.11`, `F3HERTEMPLOM → FEHERTEMPLOM`, and `EINGSRUECKT → EINGERUECKT`. The certificate gives each coordinate map.

### p166 A2 — 212 coordinates / 106 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ABMARSCH217XIXDXUND?XRXFXNACHNORDENOHNEFEINDBERUEHRUNGXALPENKORPSWIRDUMVERBASZXFRAGEZEICHENXZUMABTRANSPQRT
```

</details>

The question mark is exactly **5/6**. Two explicit substitutions give `R.D.` in place of raw `R.F.` and `ABTRANSPORT` in place of `ABTRANSPQRT`. The raw `UMVERBASZ` and its following `FRAGEZEICHEN` remain unchanged.

### p166 A3 — source-linked 204-coordinate frame / 102 positions

The raw restoration and combined template appear above. The literal input has 184 slots; the comparison supplies its twenty-coordinate prefix.

### p167 A3 — 204 slots / 102 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
BEREITGESTELLTX219XX217XUND?X2XDXSETZSN?X11XMARSCWINLINENAG?BESKEREKXWERSCHETZFORTXOXKXMX1AXNO11319OPX
```

</details>

The printed group `VGVA-` keeps one erased coordinate. The raw square also leaves two digit occurrences unresolved. The companion p166 copy improves the ending of this damaged group without requiring a completed square.

### p170 B1 — 236 coordinates / 118 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ANENMELDUNGXSERBXKAVALLERIEPETERWADEINUNDFEHERTEMPLOMEINGSRUECKTXXABMARSCH217XIXDXUND?XRXDNACHNORDENOHNEFEINBELUEHRUNG
```

</details>

The recorded same-length candidate makes **four coordinate substitutions**, yielding `ABENMELDUNG`, `EINGERUECKT`, and `FEINBERUEHRUNG`. The readings `Aben[d]meldung`, `Peterwa[r]dein` and `Fein[d]berührung` additionally supply **three prose letters** absent from the raw frame; these additions are not claimed as a ciphertext recovery.

### p170 B2 — 238 slots / 119 positions

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ALPENKORPSWIRDU?VERBASZZUMABTRFNSPORTBEREITGESTELLTXX219X217XUND?XRDXSETZEN9X11XMARSCHINLINIENAGYBESKEREKXWERSCHETZFORT
```

</details>

At plaintext position **15**, the erasure permits `{5,6,7,9,J,M,Z}`. Filling received coordinate **25** with `X` selects `J` in `UJVERBASZ`. Changing coordinate **134** from `X` to `D` gives `ABTRANSPORT`. The second question mark, at plaintext position **64**, remains **5/6**.

## Evidence and verification

The [certificate](../../experiments/p170_continuation/military_records.json) contains all raw rows, advertised and received lengths, every declared fill/substitution, all 21 prefix-placement comparisons, the source-only union domains and globally consistent witnesses for both remaining digit assignments.

```sh
python experiments/p170_continuation/verify_military.py
python experiments/p170_continuation/verify_military.py --json
python experiments/p170_continuation/verify_military_context.py
```

The verifiers check **six records and 1,248 received source slots**, the copied prefix, all repair costs, both global square assignments and the historical application to four occurrences. Optional `--french-pdf` and `--calendar-pdf` arguments check the external source hashes.

Source images: [p166 A](../../sources/excerpts/childs_p166_A_military.png), [p167 A](../../sources/excerpts/childs_p167_A_military.png), [p170 B](../../sources/excerpts/childs_p170_B_military.png). They come from printed pp. 166, 167 and 170 / PDF pp. 169, 170 and 173 of the [Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The published key's original sources remain in [keys.json](../../data/keys.json).

Source recovery, transcription and edition: **icekylinx and GPT-6 Astra Pro**. Period-key recovery retains the [original credits](../../data/keys.json).
