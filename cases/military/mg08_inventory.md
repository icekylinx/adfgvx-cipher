# Inventory query for German MG08 machine guns

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p86 A asks how many German `MG08` with tripod mounts are available
in the recipient's area and what caliber they have. It is a request for an
inventory, not a report giving the number available. The source's address,
office and reference fields remain literal.

## Source and reading

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p86, PDF p89](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [source crop](../../experiments/inventory_and_medical_return/sources/childs_p86_A.png)
is under an October 31 heading:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
A) OSM v NKJ (3.35 a.m., November 1st)
1207 (31/10)
RICHI-298
```

</details>

All 298 printed coordinates are valid and give 149 fixed labels under the
unchanged published `Oct28-31` key:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
MGKOMMANDEUROSMANHGRXOSTXWIEVIELDEUTSCHEMG08MITDREIFUSSLAFETTEIMDORTIGEXBER4ICHVORHANDENXWELCHESKALIBERHABENSIEXOSMAN19ABTLGXGRXHXQUXNO835C120X10X18X
```

</details>

Two known-coordinate substitutions repair ordinary words:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
MGKOMMANDEUROSMANHGRXOSTXWIEVIELDEUTSCHEMG08MITDREIFUSSLAFETTEIMDORTIGENBEREICHVORHANDENXWELCHESKALIBERHABENSIEXOSMAN19ABTLGXGRXHXQUXNO835C120X10X18X
```

</details>

Readable core, preserving the telegram's abbreviated grammar:

**Readable German:**

> Wie viel deutsche MG08 mit Dreifußlafette im dortigen Bereich
> vorhanden? Welches Kaliber haben sie?

The address field `MGKOMMANDEUROSMANHGRXOST` is not expanded into an
identified individual or a formally established command title. The closing
also remains unexpanded:

<details>
<summary>Raw decoded text</summary>

**Raw output — unchanged closing-field excerpt:**

```text
OSMAN19ABTLGXGRXHXQUXNO835C120X10X18X
```

</details>

In particular, the **08** in `MG08`, the **19** in `OSMAN19`, and the complete
reference `NO835C120X10X18` are unchanged published-square labels. No unit,
office or date reassignment is inferred from a plausible reading.

## Exact costs

| Source index, zero-based | Printed group / position, one-based | Change | Effect |
| ---: | --- | --- | --- |
| 223 | 45 / 4 | `V` → `F` | `BER4ICH` → `BEREICH` |
| 289 | 58 / 5 | `A` → `X` | `DORTIGEX` → `DORTIGEN` |

The raw `4` inside `BER4ICH` remains visible in the original string and
numerical ledger. Its local word repair does not reassign the square's
digit `4`. There are no source erasures, inserted coordinates, deletions or
square changes. The complete 298-coordinate repaired witness is retained
in the [certificate](../../experiments/inventory_and_medical_return/certificates.json).

```sh
python experiments/inventory_and_medical_return/verify.py --verify
```

The [inputs](../../experiments/inventory_and_medical_return/inputs.json)
preserve the manual rows, source images and key provenance. The period key
is prior work by **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also reproduced in Lasry's 2017 key comment. Earlier unreviewed OCR candidates
existed. The bounded author-paper review does not establish universal
first-decipherment priority; this source edition does not supply an answer
to the inventory question it recovers.
