# November 9: a crown airlift request and an urgent embassy address

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Three complete source parts on Childs p167 request **thirty million crowns**
for pay and purchases in Hungary, sent by **giant aircraft to Brasso**, with
an appropriate mix of large and small banknotes. A fourth, separate record
contains an urgent Constantinople embassy address signed Stumm; its second
advertised part is not printed here.

All **624 printed slots** remain in native frames under the unchanged
published **Nov7–9** key. They give **311/312 fixed raw positions**. One
observed-coordinate substitution and one fill of an invalid source glyph
complete the proposed word readings. There is no coordinate insertion,
exclusion, reordering or key change. Published period-key recovery retains
the attribution to George Lasry and collaborators.


**Reviewed source crops:** [p167_B_reviewed.png](../../experiments/nov9_crown_airlift_and_embassy/sources/p167_B_reviewed.png) · [p167_E_reviewed.png](../../experiments/nov9_crown_airlift_and_embassy/sources/p167_E_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p167 B1

[Reviewed B source image — source-PDF reference](../../experiments/nov9_crown_airlift_and_embassy/inputs.json).

<details>
<summary>Literal source transcription</summary>

**Source transcription — shared header and first-part label:**

```text
B) LP v NKJ (07.21 p.m., November 9th
1810 VON UKS 3 TLE
1 TL RICHI-190
```

</details>

The source does not visibly close the parenthesis in this header line.
The part labels, routing and date remain as printed.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 190-slot frame; 94/95 fixed positions:**

```text
OHLXOKMXBITTETFUERLOEHNUNGUNDANKAUFINUNGARNUMSCHREUNIGESE?DUNGVONDREISSIGMILLIONENKRONENMITTELS
```

**Edited output — one observed-coordinate substitution and one source-mask fill; 95/95 fixed positions:**

```text
OHLXOKMXBITTETFUERLOEHNUNGUNDANKAUFINUNGARNUMSCHLEUNIGESENDUNGVONDREISSIGMILLIONENKRONENMITTELS
```

</details>

At zero-based **source index 185**, `A→D` gives `SCHLEUNIGE` in place of raw
`SCHREUNIGE`. The invalid **C** in `DGVXC`, **source index 159**, is filled
with **G** to supply the N in `SENDUNG`. All other accepted coordinates
remain unchanged.

**Readable German — complete edited stream, with spacing and punctuation only:**

> OHL. OKM bittet fuer Loehnung und Ankauf in Ungarn um schleunige Sendung von dreissig Millionen Kronen mittels

The amount is spelled out as **`DREISSIG MILLIONEN`**. Reading it as thirty
million requires no assignment of a numerical square label. The sentence
continues directly in B2.

## p167 B2

<details>
<summary>Source and cipher evidence</summary>

**Source transcription — part label:**

```text
2 TL RICHI-192
```

**Raw output — native 192-slot frame; 96/96 fixed positions:**

```text
RIESENFLUGZEUGNACHBRASSODEUTSCHEETAPPENXVERWALTUNGXANGEMESSENEVERTEILUNGINGROSSENUNDKLEINENNOTEN
```

</details>

**Readable German — complete raw stream, with spacing and punctuation only:**

> Riesenflugzeug nach Brasso, deutsche Etappen Verwaltung. Angemessene Verteilung in grossen und kleinen Noten

No repair is used. The final **`DX`** is visible in the source but was omitted
by earlier OCR; restoring it corrects the machine transcript. The printed
internal space in **`DG DGX`** does not create an extra coordinate slot.
The transmitted recipient designation **`DEUTSCHE ETAPPEN VERWALTUNG`**
keeps its original endings.

## p167 B3

<details>
<summary>Source and cipher evidence</summary>

**Source transcription — part label and following control:**

```text
3 TL RICHI-144
[After the ciphertext:] NKJ DD
```

**Raw output — native 144-slot frame; 72/72 fixed positions:**

```text
ERBETENXXKRONENVORATHIERBESCHRAENKTUNDHOCHIMKURSEXXOKMACKENSEN4ANRX41942
```

</details>

**Readable German — complete raw stream, with spacing and punctuation only:**

> erbeten. Kronen Vorat hier beschraenkt und hoch im Kurse. OK Mackensen 4A Nr 41942.

No repair is used. The source body ends with **`VDXF`**. The separately
printed **`NKJ DD`** is transmission control; its `DD` was incorrectly
appended to the encrypted body in the earlier OCR comparison.

The raw spelling **`VORAT`** has one R and is preserved as **`Vorat`**.
Adding the second R of modern `Vorrat` would change the displayed letter
stream. **`4A`** and **`41942`** remain literal labels, without authentication
of a historical reference number. The text requests transport and describes
the limited stock and high exchange rate; it does not establish that the
requested money was delivered.

## p167 E1

[Reviewed E source image — source-PDF reference](../../experiments/nov9_crown_airlift_and_embassy/inputs.json).

<details>
<summary>Literal source transcription</summary>

**Source transcription — literal header:**

```text
E) XYZ v LP (06.43 a.m., November 10th
0022 (9/11) 2 TEILE
1 TL RICHI-98
```

</details>

The November 10 reception and internal November 9 date remain distinct.
Only part 1 is printed in this section.

<details>
<summary>Raw decoded text</summary>

**Raw output — native 98-slot frame; 49/49 fixed positions:**

```text
DEUTSCHEBOTSCHAFTCONSTANTINOPELDRINGENDXGEZXSTUMM
```

</details>

**Readable German — complete raw stream, with spacing and punctuation only:**

> Deutsche Botschaft Constantinopel. Dringend. Gez. Stumm.

An enlarged inspection resolves the third glyph of **`XGGVX`** as G,
including its internal bar; the source directly supplies `DRINGEND` with
no fill. **`CONSTANTINOPEL`** begins with C in this stream and is not silently
changed to the K spelling of another record. This source part contains the
address, urgency and signature, not a reconstructed substantive message
body or the missing second part.

## Verify

[Source inputs](../../experiments/nov9_crown_airlift_and_embassy/inputs.json) ·
[Certificates](../../experiments/nov9_crown_airlift_and_embassy/certificates.json) ·
[Reproduction notes](../../experiments/nov9_crown_airlift_and_embassy/README.md).

```sh
python experiments/nov9_crown_airlift_and_embassy/verify.py --verify
python experiments/nov9_crown_airlift_and_embassy/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks every source slot and raw position, both priced changes,
complete readable-label mappings and exact re-encryption. The optional PDF
check reproduces both crops and compares their RGB pixels. Earlier OCR and
its unchanged-key comparisons remain separate from the source edition.
No universal first-decipherment priority is asserted.
