# p215 B1 — Train-departure fragment of an evening report

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Partial recovery: icekylinx and GPT-6 Astra Pro.** The source's missing-groups
note and advertised length define a conditional 220-slot frame with **37/110
fixed raw labels**. A limited lexical proposal reaches **77/110**, preserving
all 33 remaining unknowns and changing no observed coordinate.

## p215 B1

**Readable German — partial lexical proposal; 3 printed-mask fills and 39 added-slot fills under the declared 220-slot frame:**

> Abendmeldung ?J. G??0?????TE???L?????INU??N?????. Szeged??. Weitere Zuege vom ALPEN???? abgefahren. DIV ST ?U Szeged ???.

The proposed clause concerns further trains departing. `ALPEN????` stays
unfinished; the ending retains `DIV ST ?U`, without expanding its unresolved
label into a preposition. The two `SZEGED` spellings are lexical proposals.
The intervening fields and the literal `J` and `0` retain their source limits.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — 75 added slots and every printed mask unassigned:**

```text
??END??L?????JXG??0?????TE???L?????INU??N?????XSZ??E?????ITE??Z?????OMA????????XAB??F?????XDI????????SZE??D???
```

**Edited output — same conditional frame; zero observed substitutions, 3 printed-mask fills and 39 added-slot fills:**

```text
ABENDMELDUNG?JXG??0?????TE???L?????INU??N?????XSZEGED??WEITEREZUEGEVOMALPEN????XABGEFAHRENXDIVXSTX?UXSZEGED???
```

</details>

The proposed words satisfy every retained half-pair together under one unchanged,
complete Nov22–24 square. Both source-glyph readings below admit the same
partial template and separate complete re-encryption witnesses. A source-compatible
word proposal does not establish unique historical wording.

## Source and frame

Childs, printed p215 / PDF p218, B1, `RICHI-220`; `UKS v ZON (03.20 a.m.,
November 23rd)`, `0009 KR 3 TLE`. The page heading is November 22.

[Original PDF](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
· [Source edition and verifier](../../experiments/p215_train_departure_fragment/README.md)
· [Per-position certificates](../../experiments/p215_train_departure_fragment/certificates.json).

The source prints **145 slots**, including five dashes, and marks
`(jmd several groups Missing)` after its first ten coordinates. Inserting 75
unknown slots there yields the advertised 220. The model retains every printed
slot, without exclusions or reordering. The verifier separately prices the
proposed opening over 21 nearby even lengths; it does not claim that the
historical length or loss mechanism is unique.

<details>
<summary>Literal source transcription</summary>

**Source transcription — primary X-like glyph layer; coordinate 42 also has an A-like alternative:**

```text
GG-VA FXFDF GAFGA AXX-V
FAXVX AAFAD VVXGA AXVXG XVXVG GDGAF A-G-G FDVDA
DXAAD GXAGF VAGVV FDAAG FVFAA GXVFG GD-DX DXVDA
DAAGF VDFFA FFVAA FXXGG FXFAF AGADV FVFAG VXDVX
VFXXA
```

</details>

At native source index 42 the damaged third glyph in `XVXVG` can also be read
as `A`, giving `XVAVG`. Both layers have 140 valid coordinates and five printed
masks. They differ only in the domain of plaintext position 77, which remains
unresolved in the proposal. Neither variant is selected by language score.

## Exact scope

| Layer | Fixed positions | Observed substitutions | Printed-mask fills | Added-slot fills |
|---|---:|---:|---:|---:|
| Unfilled conditional frame | 37/110 | 0 | 0 | 0 |
| Partial lexical proposal | 77/110 | 0 | 3 | 39 |

All 110 character domains, both glyph layers, all 33 unresolved positions and
the 38 still-unfilled coordinate slots are retained in the certificates.
`ALPENKORPS`, `ZU` and `IN` are not supplied. The [second part](nov22_divisional_positions_part2.md)
provides the report's surrounding divisional-position context; it is a separate
source part, rather than an independent copy of these proposed words.

Published key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016),
and Lasry's 2017 key list. Earlier repository OCR is preserved in the source
package. Conditional frame, partial lexical recovery and exact coordinate
accounting: **icekylinx and GPT-6 Astra Pro**.
