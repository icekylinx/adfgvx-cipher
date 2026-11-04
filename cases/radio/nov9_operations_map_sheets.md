# Operations-map sheets for the Gleiwitz garrison

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source restoration and edition: icekylinx and GPT-6 Astra Pro.**

## p151 E2

This surviving second part lists operations-map sheets at the directly
read scale **1 zu 100000**, with named sheet areas and quantities, followed
by a Gleiwitz garrison-office address. The complete printed body has
**224 slots** and decrypts under the unchanged published **Nov7–9** key.
Two explicitly priced word substitutions and two printed-erasure fills
produce 110 fixed labels out of 112. The final two labels remain globally
coupled unknown digits; no reference number is selected.

The [Childs source, printed p151, section E](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
prints `LP v NKJ`, `7.09 a.m., November 9th`, `2 TL` and `RICHI-224`.
Its full page and enlarged E crop were directly inspected. The source PDF,
page, crop rectangle, dimensions and decoded-pixel digest are pinned in
[the inputs](../../experiments/nov9_operations_map_sheets/inputs.json).
The [verifier](../../experiments/nov9_operations_map_sheets/verify.py)
recreates those pixels when given the PDF; the source is not represented
by an unavailable image link.

The manuscript has 44 five-slot groups and the four-character final group
`XDVV`. Group 16 is **GGVVX**. Earlier repository OCR gave **GGVVXX**, an
extra unprinted `X`, which changed the length to 225. Restoring the actual
five-coordinate group repairs the digital transcription; it excludes no
coordinate from the manuscript. The OCR snapshot and its odd-length
arithmetic remain in the experiment for comparison.

## Raw and optional edited readings

<details>
<summary>Source and cipher evidence</summary>

**Raw output — all 224 printed source slots in order, with the two dashes and unknown key cells retained:**

```text
OPERATIONSKA0TE1ZU100000SALZ?URGWIENLE?BERGBRESLAUJE40BLATTXWARSCHAU10BLATTANGARNISONKDOGLEIWVTZFSXAOK11X1D70??X
```

**Edited output — two observed-coordinate substitutions and two printed-mask fills; no insertion, deletion or changed key:**

```text
OPERATIONSKARTE1ZU100000SALZBURGWIENLEMBERGBRESLAUJE40BLATTXWARSCHAU10BLATTANGARNISONKDOGLEIWITZFSXAOK11X1D70??X
```

</details>

**Readable German — complete optional stream, retaining the literal separators, quantities and closing labels:**

> Operationskarte 1 zu 100000 Salzburg Wien Lemberg Breslau je 40 Blatt X Warschau 10 Blatt an Garnisonkdo Gleiwitz FS X AOK 11 X 1D70?? X.

**Conditional interpretation:** The fragment lists operations maps at
1:100,000, forty sheets each for the areas labeled Salzburg, Wien, Lemberg
and Breslau, and ten sheets for Warschau. It gives the garrison command at
Gleiwitz as the delivery address. The `FS`, `AOK11` and `1D70??` fields are
retained without reconstructing their administrative meaning. The absent
first part and any evidence of actual dispatch or receipt are not supplied.

The named-place spellings in this reading are source-language labels. Two
of their letters are fills and one is a substitution, as shown below;
identifying a familiar name does not make the supplied letter an observation.

## Exact word costs

All indices are zero-based. Every received coordinate stays in its original
slot; the two dashes in printed group `XGG--` are source slots 103 and 104.

| Plaintext position | Raw → proposed label | Raw pair → edited pair | Source operation | Word |
| ---: | --- | --- | --- | --- |
| 12 | `0` → `R` | `VD` → `AD` | Source 1, `V` → `A` | `KA0TE` → `KARTE` |
| 28 | `?` → `B` | `G?` → `GX` | Fill printed dash 103 with `X` | `SALZ?URG` → `SALZBURG` |
| 38 | `?` → `M` | `A?` → `AF` | Fill printed dash 104 with `F` | `LE?BERG` → `LEMBERG` |
| 93 | `V` → `I` | `GA` → `GG` | Source 53, `A` → `G` | `GLEIWVTZ` → `GLEIWITZ` |

Before the fills, the two name positions have domains **29BITV** and
**MPRUWY**, respectively. The proposed `B` and `M` belong to those domains,
but the surviving half-pairs do not uniquely select them. The scale
`1ZU100000`, quantities `40` and `10`, and `AOK11` are already raw labels;
none is introduced by the word repairs.

## The two unresolved digits are coupled

The remaining unknown positions use **different unassigned square cells**.
All source coordinates in these two pairs are observed.

| Plaintext position | Observed pair | Original source indices | Literal domain |
| ---: | --- | --- | --- |
| 109 | `VF` | 212, 43 | `5` or `6` |
| 110 | `XA` | 66, 134 | `5` or `6` |

A single injective square must govern both cells. The only complete
assignments and corresponding closing strings are:

| VF label | XA label | Literal closing field |
| --- | --- | --- |
| 5 | 6 | `1D7056` |
| 6 | 5 | `1D7065` |

Both full-key witnesses re-encrypt the complete edited stream exactly.
They are mathematical alternatives, not historical numeral assignments;
`1D7055` and `1D7066` would violate the unchanged square's injectivity.
The main reading therefore retains **1D70??**.

## Evidence and reproduction

The [certificate](../../experiments/nov9_operations_map_sheets/certificates.json)
contains all 112 raw and edited pair maps, the four changes, both unresolved
domains, both complete global-key witnesses and the retained earlier OCR
comparison. The experiment's [reproduction guide](../../experiments/nov9_operations_map_sheets/README.md)
gives the source metadata and optional original-PDF pixel check.

**Reviewed source crops:** [p151_reviewed.png](../../experiments/nov9_operations_map_sheets/sources/p151_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

```sh
python experiments/nov9_operations_map_sheets/verify.py --verify
python experiments/nov9_operations_map_sheets/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The source is **J. Rives Childs**. The published period keys retain the
credit of **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker** (2016)
and George Lasry's 2017 key disclosure, as recorded in the unchanged key
metadata. This edition is a source restoration and explicit editorial
review by **icekylinx and GPT-6 Astra Pro**, with earlier repository OCR
preserved and no claim to universal first-decipherment priority.
