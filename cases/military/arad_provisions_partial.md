<a id="arad-provisions-and-strength-report-conditional-partial-recovery"></a>

# Arad provisions and reported strength: the restored copies

The report requests provisions and trains for Arad for 80,000 men and 30,000 animals, with action through the Hungarian government. A second reception directly supports the strength figures and restores eleven missing coordinates in the damaged copy.

**Complete edition by printed page:** [p. 159](../pages/159.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**The second reception turns an uncertain strength field into an observed
80000 MANN.** The report addresses provisions, trains to Arad and an approach
to the Hungarian government; it also gives 30000 TIERE. Its two durations,
14 and 10 days, remain in the transmitted order without an invented
explanation of how they relate.

The p159 A source is damaged by repeated groups and missing coordinates.
The independently received [p168 E copy](danube_arad_witnesses.md#p168-e)
now supplies all eleven missing values and fixes the duration separator as
X, replacing the earlier optional U. The current source-linked reading has
**135 of 136 fixed labels under the published partial square**. The last
uncertainty in that layer is a shared footer cell,
not the strength figure.

**Source recovery and edition:** icekylinx and GPT-6 Astra Pro.
The unchanged Nov7–9 key is credited to George Lasry, Ingo Niebel, Nils
Kopal and Arno Wacker. Earlier OCR and the original reconstruction remain
attributed in their evidence packages.

## Conditional digit reading

The [shared Nov7–9 reference interpretation](../../experiments/nov7_9_joint_digits/README.md) supplies **6** in the footer, giving **RM 1C 186 GEH** and **136/136 conditional edited labels**. The opposite assignment gives 185 GEH. This adds no coordinate change or fill to the current seven-substitution collation. The pair is originally observed in all eight retained source maps; raw p159 still ends 186 GLH before the separately priced GEH repair.

## What can be read, and under which model

**Readable German — current p159 common reading; seven observed substitutions, source-supported fills, footer unresolved:**

> An OHL. Verpflegung noch 14 Tage. 10 Tage. Verpfleg. Zuege nach Arad. Arad bei ungar. Regierung erwirken. STAEKE 80000 Mann, 30000 Tiere. AOK11. RM 1C18?GEH.

The message asks for provision trains to Arad and for something to be
obtained through the Hungarian government. It records the military and
administrative work of sustaining movement: food, trains, permission and
reported manpower and animals appear in one compact telegram. It does not
establish that the trains arrived or independently authenticate the strength
as an actual headcount.

`STAEKE` stays as its six transmitted labels; no R is inserted. The repeated
`ARAD` and the separate 14-day/10-day statements are retained. The common
edited footer is `18?GEH`, with ?={5,6}; adopting the p168 E spelling in p159
costs one of the seven observed-coordinate substitutions. Raw p159 ends
`GLH`, and that disagreement remains in the source-linked stream below.

<details>
<summary>Current p159 source-linked and explicitly repaired streams</summary>

**Raw output — p159 primary geometry with all 11 missing coordinates supplied from observed p168 pairs:**

```text
0NOHLXVERPOLEGUNGNOCH14TAGEX10TAGEXXVERPFLEGXEUEGENACHARADXARADNEIUNGARXREGIERUNGERWIRKENXSTAEKE80000MANNX30000TISREXAOK11XRMX1CX18?GLHX
```

**Edited output — current p159 collation; seven observed substitutions and eleven source-supported added-coordinate fills:**

```text
ANOHLXVERPFLEGUNGNOCH14TAGEX10TAGEXXVERPFLEGXZUEGENACHARADXARADBEIUNGARXREGIERUNGERWIRKENXSTAEKE80000MANNX30000TIEREXAOK11XRMX1CX18?GEHX
```

</details>

## Explicit structural cost

The copy supplies source evidence for the missing values; it does not erase
the reconstruction’s structural assumptions. The current collation uses
the same finite family of duplicated groups and gaps, now compared against
observed coordinates in the second reception.

| Operation in the current p159 collation | Count or result |
|---|---|
| Native p159 source | 271 observed coordinates; header advertises 272 |
| Exclude one copy of each repeated `VDAGG` and `FFXDF` | 10 observed coordinates |
| Add two five-slot gaps and one slot in `GDDA` | 11 slots; model length 272 |
| Supply those additions from directly observed p168 coordinates | All 11; no donation uses p168’s borrowed or missing values |
| Minimum source-to-source disagreement | 5 differences across 258 jointly observed comparisons |
| Retained source-origin maps | 8, all producing the same completed ciphertext |
| Common word proposal | 7 observed p159 substitutions; 135/136 fixed labels |

The source-only comparison examines 173,580 canonical layouts and 694,320
source-origin maps. The eight minima replace the earlier 64 word-conditioned
maps and remove their P0000 alternatives. This is a minimum within a declared
source-edit family, not proof of a unique historical transmission failure.
The [cross-copy certificate](../../experiments/danube_arad_witnesses/certificates.json)
records every origin, price and both globally consistent footer assignments.

## Native source and literal header

<details>
<summary>Original p159 header, literal ciphertext and odd-frame diagnostic</summary>

**Literal header:** `A) UKS? v ZON (11.12 p.m., November 8th); AN LP 2000 KR; RICHI-272; following control: ZON`

The question mark after `UKS` is present in the source header. The reception
time is **11.12 p.m.**, not the earlier OCR's 11.18. The final `ZON` is a
source control, separate from the cipher body.

**Source transcription — all 271 printed coordinates, including both copies of each repeated group:**

```text
FDVDD FXAAX XGVDD XADVV XFVXD VDAGG VDAGG ADVDV
VADDA VDDGV DDGGX GVVGX GVXVG XDDVF VGXXA ADDVV
FFXDF FFXDF XDXXV DGAGF VDAXV VXDDG VXAAV GDDA
DVFDX GDGVG VGDDX VXVAG VDVDD DDGVG DXXVX GDDGX
DDGAA GVAVD VVGAA VGDVD VVDVG GGGDF XGDGD DDDVV
VFVGF VDGDD VXDAD XDADV GVVVV GDVDD DDVGG VVDGG
DVVVV VAFVA DXXXV VVVFA FFADV DAXVV FV
```


**Raw output — native odd-frame diagnostic, before any exclusions or additions:**

```text
HAQSTYKGWPOG3IRIDD1CXCKETTPUC0BCEEQXUEYPNCLK0L0XEEAAQFEYTKKAREAGYIEAEAYQRUN2GQYNSDRSKUP0AXLZADKE3A000DNGAXXLH0KNTWZE10QK8?KLSXLEH18EL0I
```


The last unpaired intermediate coordinate is
`V` at source index
**40**. This diagnostic and the complete
unaltered source remain in the certificate; they are not replaced by the
conditional readable frame.

</details>

## Earlier reconstruction, before the complete-copy evidence

<details>
<summary>Superseded word-conditioned baseline — exact displays and historical tests</summary>

The sections in this drawer document the earlier reconstruction before
p168 supplied the missing source values. They remain available for comparison;
their U, unresolved strength and P0000 alternatives are not the current reading.

## Raw output — conditional 272-coordinate frame

**Raw output — ten valid exclusions and eleven unfilled additions:**

```text
0NOHLXVERPOLEGUNG?OCH14TAGE?10TAGEXX??RPFLEGXEU?GENACHAR??XARADNEI?NGARXREGI?RUNGERWIR?ENXSTAEKE?0000MANNX30000TISREXAOK11XRMX1CX18?GLHX
```

The early frame fixed 124 of 136 positions while all eleven additions were
left unknown.

## Edited output — primary partial proposal

**Edited output — six observed substitutions and ten added-slot fills; one added slot remains unknown:**

```text
ANOHLXVERPFLEGUNGNOCH14TAGEU10TAGEXXVERPFLEGXZUEGENACHARADXARADBEIUNGARXREGIERUNGERWIRKENXSTAEKE?0000MANNX30000TIEREXAOK11XRMX1CX18?GLHX
```

The early proposal changed observed source indices 60, 65, 68, 69, 210 and
235, filled ten added coordinates, and left the strength and footer open.
Its exact readable display was:

**Readable German — exact nonseparator labels of the primary partial proposal:**

> An OHL. Verpflegung noch 14 Tage U10 Tage. Verpfleg. Zuege nach Arad. Arad bei ungar. Regierung erwirken. STAEKE ?0000 Mann, 30000 Tiere. AOK11. RM. 1C. 18?GLH.

Its duration U was a lexical supply. It should no longer compete on equal
evidence with the directly observed p168 separator X.

## Every tied source map is retained

The earlier text-conditioned search covered 173,580 canonical layouts and
694,320 source-origin maps: either instance of each duplicated group could
be excluded, a single slot was added around GDDA, and two five-slot gaps
were placed at the remaining boundaries. It retained 64 minimum source
maps at six observed-coordinate changes. Those old prices and every map
remain in the [original certificate](../../experiments/arad_provisions_partial/certificates.json).

The new coordinate-only comparison retains eight maps with one completed
stream. Its five-disagreement objective compares two sources, rather than
a supplied plaintext template; these are different costs, not competing
claims about the same repair count.

## The first quantity and footer stay linked

Before the complete copy was inspected, the primary strength pair had domain
{3,4,5,6,8,P,V}. Sixteen word-minimum maps left it open; forty-eight produced
literal P0000 and filled all eleven additions. The latter display was:

**Conditional interpretation — one tied map retaining literal P0000; six substitutions and eleven added-slot fills:**

```text
ANOHLXVERPFLEGUNGNOCH14TAGEU10TAGEXXVERPFLEGXZUEGENACHARADXARADBEIUNGARXREGIERUNGERWIRKENXSTAEKEP0000MANNX30000TIEREXAOK11XRMX1CX18?GLHX
```

These were alternative maps, not independent witnesses or votes for P.
The new observed p168 pairs fix 80000 and eliminate those P0000 alternatives
within the tested source family. Only the footer’s shared VF={5,6} choice
remains unresolved. The original twelve global completion witnesses and
map-specific compatibility records remain historical calculation evidence.

## Exploration, verification and credit

The original vocabulary search followed a provisions/strength lead; it was
not a blind test. Its [portable script](../../experiments/arad_provisions_partial/explore.py)
and [retained results](../../experiments/arad_provisions_partial/exploration.json)
remain reproducible, alongside the fixed-template audit:

**Reproduction commands:**

```sh
python experiments/arad_provisions_partial/verify.py --verify
python experiments/arad_provisions_partial/verify.py --verify --pdf /path/to/childs.pdf
python experiments/arad_provisions_partial/explore.py --verify
```

</details>

The [current witness edition](danube_arad_witnesses.md#arad-cross-copy-restoration)
explains the source relationship; the [original experiment](../../experiments/arad_provisions_partial/README.md)
keeps the earlier search and candidate unchanged. The reviewed [p159 crop](../../experiments/arad_provisions_partial/sources/p159_A_reviewed.png)
and p168 crop are bound to the authenticated Childs PDF.

```sh
python experiments/danube_arad_witnesses/verify.py --verify
python experiments/danube_arad_witnesses/verify.py --verify --pdf /path/to/childs.pdf
```

</details>
<!-- CASE-EDITION:END -->
