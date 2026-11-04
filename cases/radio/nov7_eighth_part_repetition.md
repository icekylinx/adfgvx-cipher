# Request to repeat an unreadable eighth part

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and conditional edition: icekylinx and GPT-6 Astra Pro.**

Childs p155 C is a two-part request to check and repeat an earlier eighth part that could not be deciphered. The second part reads directly under the published Nov7–9 key. The first part prints a six-coordinate group where its advertised length requires five; its body is shown under explicitly priced one-coordinate exclusions. The original earlier eighth part is not supplied or solved by this request.

[Reviewed source](../../experiments/nov7_eighth_part_repetition/sources/p155_C.png) · [Exact inputs](../../experiments/nov7_eighth_part_repetition/inputs.json) · [All alternatives and joint witnesses](../../experiments/nov7_eighth_part_repetition/certificates.json)

**Source transcription — header:** `C) NKJ v LP (6.42 a.m., November 8th); FUER COS 2240 (7/11), 2 TLE; 1 TL RICHI-186; 2 TL RICHI-136`.

## Conditional digit reading

The [shared Nov7–9 digit interpretation](../../experiments/nov7_9_joint_digits/README.md) reads **25.10** in part 1 and **RM 5 Nr. 153303** in part 2. The opposite square gives 26.10 and RM 6 Nr. 163303. The first part’s `AL?CHIS` field remains unresolved, and the retained source-frame alternatives are unchanged.

## p155 C1

**Conditional frame.** The literal source has 187 slots, including the six-slot group `VGVXAA`, three noncoordinate glyphs (`H`, `S`, `H`), and no printed dash. The advertised length is 186. The displayed example excludes the observed `G` at source index 61, then masks the three invalid glyphs. Excluding an observed coordinate is a separate frame operation; it is not a zero-cost OCR correction. Other exclusions are retained below.

**Readable German — conditional interpretation**, after that one exclusion and two explicitly recorded source-mask fills:

> Da achter Teil des AL?CHIS 2?X10, Leitstelle 707 POT Nr. 1002 an Sektion Politik Berlin nicht zu entziffern,

**Meaning:** The eighth part of a message identified by the literal token AL?CHIS and the date-like field 2?X10 cannot be deciphered. The routing names Sektion Politik Berlin. The sentence continues in C2.

`AL?CHIS`, the date-like field `2?X10`, and the station/reference labels remain literal. The primary pair `707 / 1002` is one example, not a uniquely recovered identification.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 186-slot frame**, before either word fill:

```text
DAACHTERTEILDESAL?CHISX2?X10XXLEIT?TELLE707POTNRX1002?NSEKTIONPOLITIKBERLINNICHTZUENTZIFFERNX
```

**Edited output — conditional 186-slot frame:** one observed-coordinate exclusion, no observed-coordinate substitution, and two source-mask fills. Two output positions remain unresolved.

```text
DAACHTERTEILDESAL?CHISX2?X10XXLEITSTELLE707POTNRX1002ANSEKTIONPOLITIKBERLINNICHTZUENTZIFFERNX
```

</details>

## p155 C2

**Readable German**, directly from the native 136-slot source frame:

> Pruefung und Wiederholung 8. Teiles erbeten. Nachrichtenchef RMX?NRX1?3303.

**Meaning:** Checking and repetition of the eighth part are requested. The two unknowns in the final reference are the same globally unassigned square cell as the unknown in the first part date.

<details>
<summary>Raw decoded text</summary>

**Raw output — native 136-slot frame:** no source-coordinate edit, fill or change of frame.

```text
PRUEFUNGUNDWIEDERHOLUNG8XTEILESERBETENXNACHRICHTENCHEFRMX?NRX1?3303X
```

</details>

## The overlong group does not determine unique reference labels

All six choices of one excluded coordinate inside the literal `VGVXAA` group are preserved. Each costs one observed-coordinate exclusion. The table records the further word substitutions and source-mask fills needed for the common readable body.

| Excluded source index | Printed coordinate | Station / reference labels | Additional observed substitutions | Source-mask fills |
|---:|---|---|---:|---:|
| 60 | V | `727 / 1002` | 0 | 2 |
| 61 | G | `707 / 1002` | 0 | 2 |
| 62 | V | `707 / 1022` | 0 | 2 |
| 63 | X | `707 / 1022` | 1 | 2 |
| 64 | A | `707 / 1022` | 2 | 2 |
| 65 | A | `707 / 1022` | 2 | 2 |

The first three choices produce different correlated numerical fields with the same repair price. The final two choices delete one of the adjacent As and produce the same frame, but their source indices remain distinct. A plausible duplicated A is not silently treated as the historically correct deletion. Conversely, the cheaper language repair does not prove that the excluded G was a transmitted error.

## One shared unresolved cell, three fields

The unknown in `2?X10` and both unknowns in `RMX?NRX1?3303` all decode from **the same square cell `XA`**. They cannot be chosen independently. Under the published pair of unused labels `{5, 6}`, the two complete shared assignments are:

| XA label | First-part date-like field | Second-part reference |
|---|---|---|
| `5` | `25X10` | `RMX5NRX153303` |
| `6` | `26X10` | `RMX6NRX163303` |

The other unknown cell receives the remaining label, preserving injectivity. Both assignments have joint full roundtrip witnesses for both message parts under every recorded exclusion. These demonstrate compatibility; neither assignment is selected as an authenticated historical date or reference. The separate `AL?CHIS` character remains source-mask uncertainty and is not resolved by this equality alone.

## Evidence and credit

Published Nov7–9 key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed OCR candidates are retained. Source review and conditional geometry/word edition: icekylinx and GPT-6 Astra Pro.

The machine record also preserves the native odd 187-slot diagnostic, including its final unpaired coordinate and the corresponding original source position. It never silently drops that orphan. Each conditional frame maps every retained coordinate back to the original source; all word fills and substitutions are separately listed.

The verifiers independently reconstruct the transposition, check all marginal domains, protect the globally shared cell, verify twelve joint two-part global witnesses and compare every nonseparator label in both readable passages. Optional PDF verification compares every delivered crop pixel with the pinned primary source.

```sh
python experiments/nov7_eighth_part_repetition/verify.py --verify
python experiments/nov7_eighth_part_repetition/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```
