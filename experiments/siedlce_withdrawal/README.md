# p200 A: the Siedlce garrison withdrawal report

**A complete 165-character source edition reports that the Siedlce and
Minsk Maziowicki garrisons have reached Thorn, while the whereabouts of
Battalion Ostrowo are unknown.** The signature reads General von Zedlitz,
hitherto military governor of Siedlce. The edition requires **eleven
known-coordinate substitutions and one printed-dash fill**, with no
insertion, deletion, or key change.

The Nov13–15b square and column order are prior published work by
**George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**. The source
transcription, explicit repairs, independent identity witness and
arithmetic certificate here are by **icekylinx and GPT-6 Astra Pro**.
This is a source-level edition, with no first historical decipherment
priority claim.

## Literal reading and proposed edition

The [source crop](sources/childs_p200_A.png) is Childs, printed p200 /
PDF p203, record A. Its header is
`WAU v LP (08.05 p.m., November 15th); 16.44 (15/11); RICHI-330`.
The page heading gives 15 November 1918. There are 66 five-coordinate
groups, including the printed `FFDF-` group: 329 visible coordinates and
one erased coordinate slot. The two recorded times are retained without
an assumed conversion.

With the unchanged published key, the literal source gives:

```text
ANGENERALG0UVERNEMENTWARSCHAUXGARISONXSIEDLCEXUNDMINSKMAZIOWICKIINXTHORJXEINGETROFFENVERBLEIBBWTLXOSTRVKOXNECHTBEKANNTXGENERALVZEDLIIZBI?HERMILIEAERGOUV?RNEURVIEDLCE
```

The square fixes 163 of the 165 positions. “Fixed” means determined by
the source and key, including conspicuous source errors; it does not mean
that every such character is already correct German.

The proposed edition is:

```text
ANGENERALGOUVERNEMENTWARSCHAUXGARISONXSIEDLCEXUNDMINSKMAZIOWICKIINXTHORNXEINGETROFFENVERBLEIBBATLXOSTROWOXNICHTBEKANNTXGENERALVZEDLITZBISHERMILITAERGOUVERNEURSIEDLCE
```

A readable interpretation is: “To General Government Warsaw. The
garrisons of Siedlce and Minsk Maziowicki have arrived in Thorn. The
whereabouts of Battalion Ostrowo are unknown. General von Zedlitz,
hitherto military governor of Siedlce.” Punctuation and expansion of
`BATL` are editorial. The literal spellings `GARISON` and
`MINSKMAZIOWICKI` remain in the ciphertext-length edition: no additional
letters are inserted to normalize them. No battalion number or signer's
forename is supplied.

## Exact repair cost

| Raw span | Proposed span | Known-coordinate substitutions | Erasure fills |
|---|---|---:|---:|
| `G0UVERNEMENT` | `GOUVERNEMENT` | 1 | 0 |
| `THORJ` | `THORN` | 2 | 0 |
| `BWTL` | `BATL` | 1 | 0 |
| `OSTRVKO` | `OSTROWO` | 2 | 0 |
| `NECHT` | `NICHT` | 1 | 0 |
| `ZEDLIIZ` | `ZEDLITZ` | 1 | 0 |
| `BI?HER` | `BISHER` | 1 | 0 |
| `MILIEAER` | `MILITAER` | 1 | 0 |
| `GOUV?RNEUR` | `GOUVERNEUR` | 0 | 1 |
| `VIEDLCE` | `SIEDLCE` | 1 | 0 |
| **Total** | | **11** | **1** |

The only erased slot is coordinate 225, the fifth position in group 45,
filled with `F`. Every other change alters an observed ADFGVX coordinate
and is counted as a substitution. In particular, the unknown square
cell in raw `BI?HER` does not license inserting `S` into the square: the
edition changes one source coordinate to reach the existing `S` cell.
The `0` in `G0UVERNEMENT` is likewise repaired at the source-coordinate
level, without changing the published digit assignment.

All 165 proposed characters use known cells of the unchanged partial
square and re-encrypt exactly to the recorded edited ciphertext. This
proves the repair cost and consistency under the fixed key. The repairs
remain an editorial proposal; the roundtrip does not prove that the
historical wording was unique.

## Independent contemporary identity witness

The bilingual **Kreisblatt für den Kreis Grojec / Dziennik rozporządzeń
dla powiatu Grójeckiego**, no. 29, published **15 October 1918**, contains
a notice dated **16 September 1918** at Siedlce. On printed p211 / PDF
p4, its German and Polish signatures identify **Freiherr von Zedlitz,
Generalmajor**, as the military governor. The [title crop](sources/grojec_1918_29_title.png)
and [signature crop](sources/grojec_1918_29_p211_signature.png) were
visually inspected against the [public scan](http://mbc.cyfrowemazowsze.pl/Content/15317/15317.pdf).

This independently supports the name and office in the proposed
signature. It does not independently establish the November withdrawal,
the Thorn destination, the Minsk spelling, or the battalion identity.

## Reproduce

```sh
python experiments/siedlce_withdrawal/verify.py --verify
python experiments/siedlce_withdrawal/verify.py --verify \
  --pdf /tmp/adfgvx-childs.pdf \
  --context-pdf /tmp/zedlitz_1918_gazette.pdf
```

`inputs.json` freezes the literal grouped source, source hashes, key,
editorial wording and contextual witness. `certificate.json` records all
raw character domains, source-coordinate pairs, eleven substitutions,
the single fill, and the same-length re-encryption result. No unknown
square cell is promoted into the published key.
