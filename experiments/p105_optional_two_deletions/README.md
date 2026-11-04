# An optional two-deletion reading of p105 B

[Reading conventions](../../docs/reading-conventions.md)

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

Original challenge **p105** has a more economical, fully paired alternative:
exclude two explicitly identified printed coordinates, retain **288 of 290**,
and read **144 labels** with the unchanged **Nov1–3** key. Three separately
priced coordinate substitutions produce the optional ordinary-word edition
below. Its total declared cost is **two source exclusions plus three observed
substitutions**, with no inserted coordinates, fills or changed key.

This is a separate proposal. The [primary p105 case](../../cases/p105.md),
Norbert's 2017 reading and Max Baertl's proposed words remain intact. The new
work concerns source accounting, competing geometries and the conditional
cost of the reading. It does not claim the first decipherment of this message.
The source visibly prints both coordinates that the proposed model excludes;
their historical status as surplus characters is not established.

## Source and unchanged baselines

[Childs, printed p105, section B](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
prints `--- v ---`, an intercept time of `9.22 p.m., November 2nd`, an origin
line `2020 (2/11)` and `RICHI-290`. The complete 58-group body was checked
against the page pixels. In particular, groups 21/22 are `DDFFX DADDG` and
groups 46/47 are `DGGVF XGDGD`. No cancellation is visible on the two `DD`
runs. The crop's PDF coordinates, dimensions and decoded-pixel hash are
recorded in [inputs.json](inputs.json), so the image can be checked directly
from the source PDF without a new image asset.

**Source transcription — all 290 printed coordinates; none silently removed:**

```text
GAGVA AXADF XVAXV XGVDA XDGAF ADFFG FXXXV DAGDX
DXDXX VVGGX AVDAG GGFDG GAFXD XAGAA FFDGD XGDVD
VGGAF XDXAF AVDXF VVDGX DDFFX DADDG VGDGD XVXXG
DGDDG FFFGV ADVXD VXFXD GXAAD DVXXG VDAXX VAXDX
GFDDV VFVDA VXADD GFAFD GAVXA GVDGA FFDDD GAGAG
DGFDF XFDXG GFDDG VGAFA XFGAV DGGVF XGDGD FDXVX
XAXGD XGGGV GDXGX XGVDF VXAAV GDXDX DGADX GVAAD
FXGGV DGGAX
```

**Raw output — all 290 printed coordinates with no source exclusion or word repair:**

```text
GMCM4N6Y4TA59EBUV55ABQIBONMHXXBYEDK4DTEUJEMRRL1IS2VNWO9CNLR8RC6IZ3OR65TALVAUXWZXB8QL2TE89X321CHXDGX6XX9XX1HVONM8BVRCALMDB7KXA8IIDYZG6ANF323D8HBRM
```

[Norbert's 2017 repair](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-852622)
excludes source indices **49, 97 and 98**, leaving 287 coordinates. Its paired
prefix has 143 labels and an unpaired final intermediate `D`. The existing
review also represents the latter explicitly by excluding source **244**,
giving a fully paired 286-coordinate frame with the same 143-label body.
Both versions and the source origin of the orphan are recomputed here.

**Recomputed prior reading — unchanged 143-label body from the earlier three-exclusion repair, or its four-exclusion complete counterpart:**

```text
GERMANIAATAPPEKONSTANTINOPELXRFUERMITTEHMEERDIVIC9VNZUXTEL9VRX62XDOV2TTELEGRXN0X58XISTELTX32141XQ4XAXVOMX4CNOVEMBERNULEDIGTXA8MIRALSTAFX32398XB
```

## The explicit double-D hypothesis

All source and plaintext indices below are **zero-based**. Group numbers
are one-based. The representative optional frame excludes source **100**
and **107**, one `D` from each of the two adjacent printed `DD` runs.

| Original source indices | Printed group | Representative exclusion | Remaining group after that exclusion |
| --- | --- | ---: | --- |
| 100–104 | Group 21, `DDFFX` | 100, `D` | `DFFX` |
| 105–109 | Group 22, `DADDG` | 107, `D` | `DADG` |

Excluding 101 instead of 100, or 108 instead of 107, gives the same retained
ciphertext. All four descriptions **[100,107], [100,108], [101,107] and
[101,108]** have their own original-source maps in the certificate. Selecting
one coordinate from an identical run does not identify which printed
coordinate, if either, was historically surplus.

**Raw output — optional 288-coordinate frame after exclusions [100,107], before all word repairs:**

```text
GERMANIAATAPPEKONSTANTINOPELXXFUERMITTELMEERDIVISIVNZUXTELXNRX62XDORTTTELEGRXNRX58XISTELTX32141XB2XAXVOMX1XNOVEMBERVRLEDIGTXADMIRALSTABX32398XBR
```

The ordinary formulae `TELXNRX`, `TELEGRXNRX` and `ADMIRALSTAB` now occur
in raw output. The final `R` is a paired decoded label; this model has no
unpaired suffix. The new raw output also changes reference fields. Those
changes are consequences of the declared geometry, not independently
confirmed historical corrections.

## Three optional ordinary-word repairs

| Plaintext index | Raw label → proposed label | Pair change | Original source-coordinate change | Proposed word |
| ---: | --- | --- | --- | --- |
| 8 | `A` → `E` | `XG` → `VG` | 154, `X` → `V` | `GERMANIAETAPPE` |
| 50 | `V` → `O` | `DG` → `AG` | 174, `D` → `A` | `MITTELMEERDIVISION` |
| 115 | `V` → `E` | `DG` → `VG` | 58, `D` → `V` | `ERLEDIGT` |

These are the only changes between the preceding raw stream and the
following edition. The source deletion ledger remains separate. Every
remaining coordinate, the opaque internal wording and all numeral/letter
labels are retained literally. The ordinary words were already suggested
by the earlier credited reading; the new contribution is their exact,
reduced repair cost in this alternative source frame.

**Edited output — optional 144-label edition, two source exclusions and three observed-coordinate substitutions:**

```text
GERMANIAETAPPEKONSTANTINOPELXXFUERMITTELMEERDIVISIONZUXTELXNRX62XDORTTTELEGRXNRX58XISTELTX32141XB2XAXVOMX1XNOVEMBERERLEDIGTXADMIRALSTABX32398XBR
```

**Readable German — complete optional edition, retaining every literal label and the opaque wording:**

> Germania [Etappe] Konstantinopel XX fuer [Mittelmeerdivision] zu X Tel X Nr X 62 X `DORTTTELEGR` X Nr X 58 X `ISTELT` X 32141 X B2 X A X vom X 1 X November [erledigt] X Admiralstab X 32398 X BR.

**Conditional interpretation:** Under this frame and the three word repairs,
the message concerns the Mediterranean naval division, earlier telegram
references and a matter described as dealt with. The Germania/Constantinople
address and Admiralstab footer are readable. `DORTTTELEGR`, `ISTELT`, `B2`,
`A`, `BR` and the reference numbers remain literal. The model does not settle
the damaged reference syntax, a historical office expansion, or the actual
date of the referred-to telegram.

## What the geometry search actually establishes

Ten spans were selected from the earlier reading: `GERMANIAETAPPE`,
`KONSTANTINOPEL`, `XXFUER`, `MITTELMEERDIVISION`, `ZUXTELXNRX`,
`TELEGRXNRX`, `VOM`, `NOVEMBER`, `ERLEDIGT` and `ADMIRALSTAB`, at the
explicit offsets in the inputs. **Every numeral, date numeral, reference
label and opaque intervening field is masked during this search.**

For each allowed retained length, a dynamic program examines all ordered
source subsequences with the prescribed number of exclusions. It minimizes
observed-coordinate mismatches against the encoded word stencil, counts
all tied descriptions and enumerates every minimum. The key and retained
source order are fixed. There is no insertion or source-reordering model.

| Frame or exact search | Source exclusions | Substitutions for the same ten word spans | Sum at one unit per excluded/changed coordinate |
| --- | ---: | ---: | ---: |
| Native 290, unchanged geometry | 0 | 83 | 83 |
| Earlier complete 286, exclusions [49,97,98,244] | 4 | 13 | 17 |
| Intermediate 286, exclusions [53,100,107,244] | 4 | 4 | 8 |
| Minimum over every two-exclusion description | 2 | 3 | 5 |
| Minimum over every four-exclusion description | 4 | 3 | 7 |

The last two rows use the same word-only objective. The **12** two-exclusion
minima are every combination of first exclusion **99–104** and second
exclusion **107 or 108**. They give **four distinct raw streams**. The
selected double-D family accounts for four of those descriptions; its
historical uniqueness is not claimed.

| First exclusion | Number of tied descriptions | Internal raw token | Second internal raw token | Date-field raw token |
| --- | ---: | --- | --- | --- |
| 99 | 2 | `DOR2TTELEGR` | `ISTELT` | `1XNOVEMBER` |
| 100 or 101 | 4 | `DORTTTELEGR` | `ISTELT` | `1XNOVEMBER` |
| 102 or 103 | 4 | `DORTTTELEGR` | `ISTEIT` | `1XNOVEMBER` |
| 104 | 2 | `DORTTTELEGR` | `ISTEIT` | `1ZNOVEMBER` |

All twelve preserve `B2`, raw `VRLEDIGT`, `ADMIRALSTAB` and the closing
`32398XBR`. All four complete raw streams and every source-exclusion list
are included in [the certificate](certificates.json).

The scope is deliberately finite: zero, two or four exclusions under the
published key and these fixed word offsets. The equal-weight sum is a
transparent edit count, not a probability model. These minima do not prove
optimality among other keys, shifted word hypotheses, insertions or every
possible German message.

## Retrospective held-out spans

The same two-exclusion optimization was repeated after omitting selected
word groups. These are sensitivity checks after the old reading was known,
not blind tests or evidence that the chosen words are unique.

| Word stencil | Minimum observed changes | All tied descriptions | Distinct raw streams |
| --- | ---: | ---: | ---: |
| All ten spans | 3 | 12 | 4 |
| Prefix only, through `MITTELMEERDIVISION` | 2 | 55 | 30 |
| Address spans omitted | 2 | 30 | 16 |
| `ADMIRALSTAB` omitted | 3 | 18 | 8 |
| `MITTELMEERDIVISION` omitted | 2 | 12 | 4 |

Omitting `MITTELMEERDIVISION` leaves exactly the same twelve minimizing
source descriptions. Prefix-only selection still fixes the later literal
numeral **1**, the `STAB` suffix and closing **32398XBR** across all 55
minima, although the full office token remains `A?MIRALSTAB` and the
separator after 1 can be `C`, `X` or `Z`. Omitting the footer also leaves
`A?MIRALSTAB`. The certificate preserves these exact cross-frame consensus
strings; their `?` symbols mark variation among modeled readings, not
unprinted source glyphs.

## Independent vocabulary, without importing references

Three other source-reviewed records supply native, unrepaired witnesses.
Their cited words decode from fully observed pairs at the exact source
indices recorded in this supplement.

| Independent record | Native key | Directly decoded word span | Source image |
| --- | --- | --- | --- |
| p103 B1 | Nov1–3 | `ERLEDIGT`, `TELEGRXNRX` | [p103 B1](../zitag_purchase_orders/sources/p103_B1.png) |
| p108 A | Nov1–3 | `ADMIRALSTAB` | [p108 A](../p108_naval_and_personnel/sources/p108_A.png) |
| p165 A1 | Nov7–9 | `MITTELMEERDIVISION` | [p165 A1](../corcovado_sale_terms/sources/p165_A1.png) |

These attest the ordinary vocabulary and formulae, not the p105 geometry,
its message identity or its numerical fields. No independent exact native
`GERMANIAETAPPE` witness is claimed. That particular correction remains the
earlier credited lexical proposal, explicitly priced at one coordinate.

## Reference alternatives remain visible

The original 143-label reconstruction gives **Q4** and **4CNOVEMBER**. An
earlier exploratory four-exclusion target, which included the old reference
labels, gives raw **Q2** and **4XNOVEMBER** under exclusions
**[53,100,107,244]**. The new twelve-minimum word-only family instead gives
**B2** and **1[X/Z]NOVEMBER**. Its broader prefix-only family also permits
**1CNOVEMBER**.

The exploratory full target and all four of its minimizing descriptions
are retained separately in the certificate. Its seven-change cost concerns
a different, more restrictive objective and is not substituted for the
four-change word-only cost in the comparison table. No date or label is
chosen because it better fits the intercept header. The change of geometry
also explains why the new model retains a final `R`, while the earlier
complete models end in `B`.

## Reproduce

The verifier checks the unchanged core files, the earlier source record and
reading, native and repaired roundtrips, every original-source map, all
minimum descriptions, the three word changes, the held-out comparisons and
the four independently observed word spans. It also pins all existing p105
case headings, fences and quotations. The optional PDF check reproduces the
reviewed p105 crop pixels and the three already published witness images.

```sh
python experiments/p105_optional_two_deletions/verify.py --verify
python experiments/p105_optional_two_deletions/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

Default verification uses the standard library and repository data. PDF
pixel reproduction additionally uses PyMuPDF. This supplement adds no new
physical message to the catalogue, does not rewrite the primary reading,
and makes no claim that a mathematically exact reconstruction authenticates
the original transmission or the historical error mechanism.
