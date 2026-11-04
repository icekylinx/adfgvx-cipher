# Bridges and the wire connection through Budapest

The report describes an interruption of the wire connection through Budapest. A separately received companion asks about direct communication while that link is unavailable.

**Complete edition by printed page:** [p. 100](../pages/100.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p100 B reports that bridges have been blown up and attributes an
interruption of the wire lines through Budapest to the Hungarian National
Council. It ends with the literal headquarters label `A.O.K.11`.
The edition establishes what this telegram reports; it does not independently
verify those events or identify the location meant by `DORT`.

## Source and body

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p100, PDF p103](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [B crop](../../experiments/radio_contacts_and_keys/sources/childs_p100_B.png)
is under a November 1 heading:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
B) UKS v ZÖN (------ November 2nd)
RICHI-194
```

</details>

Manual transcription finds **194 valid coordinates**, matching the printed
length. An earlier 195-slot OCR extraction produced a garbled result; its
extra slot is not treated as a historical cipher error. The unchanged
published `Nov1-3` key fixes all 97 raw plaintext positions:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
BRUECKENXDORTXGESPRENGTXDRAHTLEITUNGENXUEBERXBUDAPESTXDURCHSUNGXNATIONALRATXUNTERBJOCHENXAXOXKX11
```

</details>

Two observed-coordinate substitutions give:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
BRUECKENXDORTXGESPRENGTXDRAHTLEITUNGENXUEBERXBUDAPESTXDURCHXUNGXNATIONALRATXUNTERBROCHENXAXOXKX11
```

</details>

Readable German, expanding only the explicit abbreviation in brackets:

**Readable German:**

> Brücken dort gesprengt. Drahtleitungen über Budapest durch
> ung[arischen] Nationalrat unterbrochen. A.O.K. 11.

| Source index, zero-based | Printed group / position, one-based | Change | Effect |
| ---: | --- | --- | --- |
| 118 | 24 / 4 | `V` → `X` | `DURCHSUNG` → `DURCHXUNG` |
| 130 | 27 / 1 | `V` → `D` | `UNTERBJOCHEN` → `UNTERBROCHEN` |

There are no source erasures, inserted coordinates or square changes. The
final **11** is unchanged in both the raw and repaired readings.

The adjacent [p100 C](../radio/radio_contacts_and_keys.md#p100-c-direct-contact-while-the-wire-is-broken)
asks about direct communication and also says the wire is interrupted.
The separately printed B body is not merged with the earlier
[p100 challenge](../p100.md); that challenge's Belgrade reading retains
**Armin's 2017 comment 13** priority. A multipart relationship is not required
to verify this independent source frame.

## Reproduce

The [inputs](../../experiments/radio_contacts_and_keys/inputs.json) and
[certificate](../../experiments/radio_contacts_and_keys/certificates.json)
preserve the source groups and exact forward witness.

```sh
python experiments/radio_contacts_and_keys/verify.py --verify
```

The key is credited to **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
with full prior-key provenance in the input record. Earlier unreviewed OCR
candidates existed. No first-decipherment priority is claimed from the
bounded absence of an explicit body example in the author-paper review.

</details>
<!-- CASE-EDITION:END -->
